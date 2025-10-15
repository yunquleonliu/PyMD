from __future__ import annotations

import os
from pathlib import Path

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QAction, QCloseEvent
from PyQt6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QStatusBar,
    QTextEdit,
    QToolBar,
)
from PyQt6.QtWebEngineWidgets import QWebEngineView

from .renderer import MarkdownRenderer
from .exporter import WordExporter, PDFExporter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyMD Editor - MVP")
        self.resize(1200, 800)

        # State
        self._current_file: Path | None = None
        self._dark_mode: bool = False
        self._dirty: bool = False

        # Core widgets
        self.editor = QTextEdit(self)
        self.preview = QWebEngineView(self)
        self.renderer = MarkdownRenderer()
        self.word_exporter = WordExporter()
        self.pdf_exporter = PDFExporter()

        # Live preview debounce timer
        self._render_timer = QTimer(self)
        self._render_timer.setSingleShot(True)
        self._render_timer.setInterval(150)  # ms
        self._render_timer.timeout.connect(self.render_preview)

        # Splitter layout
        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Orientation.Horizontal)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)
        splitter.setSizes([600, 600])
        self.setCentralWidget(splitter)

        # Status bar
        self.status = QStatusBar(self)
        self.setStatusBar(self.status)

        # Connect editor change
        self.editor.textChanged.connect(self._on_text_changed)

        # Actions and toolbars
        self._init_actions()
        self._init_toolbar()

        # Initial render
        self.render_preview()

    # UI setup
    def _init_actions(self):
        self.new_action = QAction("新建", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.new_file)

        self.open_action = QAction("打开", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction("保存", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_file)

        self.save_as_action = QAction("另存为", self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.save_as_action.triggered.connect(self.save_file_as)

        self.toggle_theme_action = QAction("切换主题", self)
        self.toggle_theme_action.setShortcut("Ctrl+T")
        self.toggle_theme_action.triggered.connect(self.toggle_theme)

        self.export_pdf_action = QAction("导出 PDF", self)
        self.export_pdf_action.setShortcut("Ctrl+Shift+P")
        self.export_pdf_action.triggered.connect(self.export_pdf)

        self.export_word_action = QAction("导出 Word", self)
        self.export_word_action.setShortcut("Ctrl+Shift+W")
        self.export_word_action.triggered.connect(self.export_word)

    def _init_toolbar(self):
        tb = QToolBar("Main", self)
        tb.addAction(self.new_action)
        tb.addAction(self.open_action)
        tb.addAction(self.save_action)
        tb.addAction(self.save_as_action)
        tb.addSeparator()
        tb.addAction(self.export_pdf_action)
        tb.addAction(self.export_word_action)
        tb.addSeparator()
        tb.addAction(self.toggle_theme_action)
        self.addToolBar(tb)

    # Slots
    def _on_text_changed(self):
        self._dirty = True
        text = self.editor.toPlainText()
        self.status.showMessage(f"字数: {len(text)}", 1500)
        self._render_timer.start()

    def render_preview(self):
        html = self.renderer.to_html(self.editor.toPlainText(), dark=self._dark_mode)
        self.preview.setHtml(html)

    # File ops
    def new_file(self):
        if not self._confirm_discard_changes():
            return
        self.editor.clear()
        self._current_file = None
        self._dirty = False
        self._update_title()
        self.render_preview()

    def open_file(self):
        if not self._confirm_discard_changes():
            return
        path, _ = QFileDialog.getOpenFileName(self, "打开 Markdown 文件", str(Path.home()), "Markdown (*.md)")
        if not path:
            return
        self.load_file(Path(path))

    def load_file(self, file_path: Path):
        """加载指定的文件（供外部调用，如命令行参数）"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.editor.setPlainText(f.read())
            self._current_file = file_path
            self._dirty = False
            self._update_title()
            self.render_preview()
            self.status.showMessage(f"已打开: {file_path}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "打开失败", str(e))

    def save_file(self):
        if self._current_file is None:
            return self.save_file_as()
        try:
            with open(self._current_file, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self._dirty = False
            self._update_title()
            self.status.showMessage("已保存", 2000)
        except Exception as e:
            QMessageBox.critical(self, "保存失败", str(e))

    def save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "另存为", str(Path.home() / "untitled.md"), "Markdown (*.md)")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self._current_file = Path(path)
            self._dirty = False
            self._update_title()
            self.status.showMessage(f"已保存为: {path}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "保存失败", str(e))

    def toggle_theme(self):
        self._dark_mode = not self._dark_mode
        self.render_preview()

    def export_pdf(self):
        """Export current document to PDF."""
        path, _ = QFileDialog.getSaveFileName(
            self, "导出 PDF", str(Path.home() / "document.pdf"), "PDF Files (*.pdf)"
        )
        if not path:
            return
        try:
            text = self.editor.toPlainText()
            self.pdf_exporter.export(text, Path(path), dark=self._dark_mode)
            self.status.showMessage(f"已导出 PDF: {path}", 3000)
            QMessageBox.information(self, "导出成功", f"PDF 已保存到:\n{path}")
        except ImportError as e:
            QMessageBox.warning(
                self,
                "导出失败",
                f"PDF 导出需要安装 weasyprint 库:\n\n{str(e)}\n\n"
                "可运行: pip install weasyprint\n"
                "注意: Windows 上可能需要安装 GTK3 运行时"
            )
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出 PDF 时出错:\n{str(e)}")

    def export_word(self):
        """Export current document to Word."""
        path, _ = QFileDialog.getSaveFileName(
            self, "导出 Word", str(Path.home() / "document.docx"), "Word Documents (*.docx)"
        )
        if not path:
            return
        try:
            text = self.editor.toPlainText()
            self.word_exporter.export(text, Path(path))
            self.status.showMessage(f"已导出 Word: {path}", 3000)
            QMessageBox.information(self, "导出成功", f"Word 文档已保存到:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出 Word 时出错:\n{str(e)}")

    def _update_title(self):
        name = self._current_file.name if self._current_file else "未命名"
        star = "*" if self._dirty else ""
        self.setWindowTitle(f"PyMD Editor - {name}{star}")

    def _confirm_discard_changes(self) -> bool:
        if not self._dirty:
            return True
        resp = QMessageBox.question(self, "放弃更改?", "当前文档有未保存更改，是否放弃？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return resp == QMessageBox.StandardButton.Yes

    # Events
    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        if self._dirty:
            ok = self._confirm_discard_changes()
            if not ok:
                event.ignore()
                return
        event.accept()
