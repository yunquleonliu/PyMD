from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
from packaging.version import Version

from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QInputDialog,
    QMessageBox,
    QProgressDialog,
)

from .config import APP_VERSION, DEFAULT_DOWNLOAD_DIR, UPDATE_MANIFEST_URL


@dataclass
class UpdateManifest:
    version: str
    download_url: str
    sha256: str
    notes: str | None = None
    otp_sha256: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UpdateManifest":
        required = {"version", "download_url", "sha256"}
        missing = required.difference(data)
        if missing:
            raise ValueError(f"Manifest missing fields: {', '.join(sorted(missing))}")
        return cls(
            version=str(data["version"]),
            download_url=str(data["download_url"]),
            sha256=str(data["sha256"]).lower(),
            notes=data.get("notes"),
            otp_sha256=(str(data["otp_sha256"]).lower() if data.get("otp_sha256") else None),
        )

    def is_newer_than_current(self) -> bool:
        try:
            return Version(self.version) > Version(APP_VERSION)
        except Exception:
            return self.version != APP_VERSION


class UpdateManager(QObject):
    """Handles update checks and installations for PyMD Editor."""

    def __init__(self, manifest_url: str | None = None, parent: QObject | None = None):
        super().__init__(parent)
        self.manifest_url = manifest_url or UPDATE_MANIFEST_URL

    def check_for_updates(self, parent=None) -> None:
        try:
            manifest = self._fetch_manifest()
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(parent, self._tr("更新检查失败"), str(exc))
            return

        if not manifest.is_newer_than_current():
            QMessageBox.information(parent, self._tr("已是最新版本"), self._tr("当前已是最新版本。"))
            return

        details = self._build_release_notes(manifest)
        reply = QMessageBox.question(
            parent,
            self._tr("发现新版本"),
            details,
            QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        if manifest.otp_sha256 and not self._verify_otp(parent, manifest.otp_sha256):
            return

        try:
            installer_path = self._download_update(parent, manifest)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(parent, self._tr("下载失败"), str(exc))
            return

        self._prompt_install(parent, installer_path)

    def _fetch_manifest(self) -> UpdateManifest:
        timeout = httpx.Timeout(10.0, read=30.0)
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            response = client.get(self.manifest_url)
            response.raise_for_status()
            try:
                payload = response.json()
            except json.JSONDecodeError as exc:  # noqa: TRY003
                raise ValueError("清单文件不是有效的 JSON") from exc
        return UpdateManifest.from_dict(payload)

    def _verify_otp(self, parent, expected_sha256: str) -> bool:
        for attempt in range(3):
            otp, ok = QInputDialog.getText(
                parent,
                self._tr("需要一次性密码"),
                self._tr("请输入收到的 OTP："),
            )
            if not ok:
                return False
            otp = otp.strip()
            if not otp:
                QMessageBox.warning(parent, self._tr("无效的 OTP"), self._tr("请输入有效的 OTP。"))
                continue
            digest = hashlib.sha256(otp.encode("utf-8")).hexdigest()
            if digest == expected_sha256:
                QMessageBox.information(parent, self._tr("验证通过"), self._tr("OTP 已验证，通过。"))
                return True
            remaining = 2 - attempt
            if remaining >= 0:
                QMessageBox.warning(
                    parent,
                    self._tr("验证失败"),
                    self._tr(f"OTP 不正确，还可以再尝试 {remaining} 次。"),
                )
        QMessageBox.critical(parent, self._tr("验证失败"), self._tr("OTP 验证失败，已取消更新。"))
        return False

    def _download_update(self, parent, manifest: UpdateManifest) -> Path:
        download_dir = DEFAULT_DOWNLOAD_DIR
        download_dir.mkdir(parents=True, exist_ok=True)
        target_path = download_dir / f"PyMDEditor-{manifest.version}.exe"

        progress = QProgressDialog(
            self._tr("正在下载更新包..."),
            self._tr("取消"),
            0,
            100,
            parent,
        )
        progress.setWindowTitle(self._tr("下载更新"))
        progress.setWindowModality(Qt.WindowModality.ApplicationModal)  # type: ignore[name-defined]
        progress.show()

        temp_fd, temp_path = tempfile.mkstemp(prefix="pymd-update-", suffix=".exe")
        os.close(temp_fd)
        hasher = hashlib.sha256()

        timeout = httpx.Timeout(10.0, read=120.0)
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            with client.stream("GET", manifest.download_url) as response:
                response.raise_for_status()
                total = int(response.headers.get("content-length", 0))
                downloaded = 0
                with open(temp_path, "wb") as dst:
                    for chunk in response.iter_bytes(65536):
                        if progress.wasCanceled():
                            raise RuntimeError("用户已取消下载")
                        dst.write(chunk)
                        hasher.update(chunk)
                        downloaded += len(chunk)
                        if total:
                            percent = int(downloaded / total * 100)
                            progress.setValue(min(percent, 100))
                            QApplication.processEvents()
        progress.close()

        if hasher.hexdigest().lower() != manifest.sha256.lower():
            raise ValueError("下载的文件校验失败 (SHA256 不匹配)")

        Path(temp_path).replace(target_path)
        return target_path

    def _prompt_install(self, parent, installer_path: Path) -> None:
        message = self._tr("更新包已下载。是否立即安装？\n\n{path}").format(path=str(installer_path))
        reply = QMessageBox.question(
            parent,
            self._tr("安装更新"),
            message,
            QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            if sys.platform.startswith("win"):
                os.startfile(str(installer_path))  # type: ignore[attr-defined]
            else:
                subprocess.Popen([str(installer_path)])
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(parent, self._tr("安装失败"), str(exc))
            return

        QMessageBox.information(
            parent,
            self._tr("即将退出"),
            self._tr("安装程序已启动，PyMD Editor 将退出以完成更新。"),
        )
        QApplication.quit()

    def _build_release_notes(self, manifest: UpdateManifest) -> str:
        lines = [
            self._tr("检测到新版本: {version}").format(version=manifest.version),
            self._tr("当前版本: {current}").format(current=APP_VERSION),
        ]
        if manifest.notes:
            lines.append("")
            lines.append(self._tr("更新说明:"))
            lines.append(manifest.notes)
        return "\n".join(lines)

    @staticmethod
    def _tr(text: str) -> str:
        return text
