from __future__ import annotations

from pathlib import Path

APP_NAME = "PyMD Editor"
APP_ID = "com.pymd.editor"
APP_VERSION = "0.4.0"
UPDATE_MANIFEST_URL = "https://example.com/pymd-editor/releases/latest.json"
DEFAULT_DOWNLOAD_DIR = Path.home() / "Downloads" / "PyMDEditor"


def get_version() -> str:
    return APP_VERSION


def get_manifest_url() -> str:
    return UPDATE_MANIFEST_URL
