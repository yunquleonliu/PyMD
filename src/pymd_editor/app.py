from __future__ import annotations

import os
from pathlib import Path

from PyQt6.QtCore import QTimer, Qt, QUrl
from PyQt6.QtGui import QAction, QCloseEvent
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QStatusBar,
    QTextEdit,
    QToolBar,
    QTabWidget,
    QTabBar,
    QWidget,
    QHBoxLayout,
)
from PyQt6.QtWebEngineWidgets import QWebEngineView

from .config import APP_NAME, APP_VERSION, UPDATE_MANIFEST_URL
from .renderer import MarkdownRenderer
from .exporter import WordExporter, PDFExporter
from .wysiwyg_editor import EnhancedWYSIWYGEditor
from .three_column_layout import ThreeColumnLayout, AIAssistantPanel
from .ai_settings import get_ai_manager
from .updater import UpdateManager
from .pdf_tools import PDFViewer, PDFConverter, PDFMergeDialog, PDFSplitDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(1200, 800)

        # State
        self._current_file: Path | None = None
        self._dark_mode: bool = False
        self._dirty: bool = False
        self._current_language = 'zh'  # 初始化语言设置
        self._zen_mode: bool = False
        self._current_theme: str = "Default"

        # Core widgets
        self.editor = QTextEdit(self)
        self._setup_drag_drop()  # 启用拖放功能
        self.preview = QWebEngineView(self)
        # Enable image loading, mixed content, and JavaScript for MathJax
        from PyQt6.QtWebEngineCore import QWebEngineSettings
        settings = self.preview.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        self.wysiwyg_editor = EnhancedWYSIWYGEditor(self)
        self.wysiwyg_editor.set_base_path(Path.cwd())
        self.renderer = MarkdownRenderer()
        self.word_exporter = WordExporter()
        self.pdf_exporter = PDFExporter()

        # Live preview debounce timer
        self._render_timer = QTimer(self)
        self._render_timer.setSingleShot(True)
        self._render_timer.setInterval(150)  # ms
        self._render_timer.timeout.connect(self.render_preview)

        # 创建标签页界面
        self.tab_widget = QTabWidget(self)
        
        # 1. 三栏布局模式（新的主要模式）
        self.three_column_layout = ThreeColumnLayout(self)
        self.ai_assistant = AIAssistantPanel(self)
        
        # 设置三栏内容
        self.three_column_layout.set_panel_widget("left", self.editor)
        self.three_column_layout.set_panel_widget("middle", self.preview)
        self.three_column_layout.set_panel_widget("right", self.ai_assistant)
        
        # 连接布局变化信号
        self.three_column_layout.layoutChanged.connect(self._on_layout_changed)
        
        # 2. WYSIWYG模式（专用编辑器）
        # 保持现有的WYSIWYG编辑器

        # 初始化AI管理器
        from .ai_framework import AIManager
        self.ai_manager = AIManager(get_ai_manager())

        # 更新管理器
        self.update_manager = UpdateManager(manifest_url=UPDATE_MANIFEST_URL)

        # 连接AI信号
        self.ai_assistant.ai_request.connect(self.ai_manager.process_request)
        self.ai_manager.response_received.connect(self._on_ai_response)
        # 流式片段信号（用于展示流式输出）
        if hasattr(self.ai_manager, 'response_chunked'):
            self.ai_manager.response_chunked.connect(self.ai_assistant.display_response_chunk)
        self.ai_manager.status_changed.connect(self._on_ai_status_changed)

        # 为WYSIWYG模式创建AI助手容器
        self.wysiwyg_container = QWidget()
        wysiwyg_layout = QHBoxLayout(self.wysiwyg_container)
        wysiwyg_layout.setContentsMargins(0, 0, 0, 0)

        # WYSIWYG编辑器占主要部分
        wysiwyg_layout.addWidget(self.wysiwyg_editor, 3)

        # 可选的AI助手面板
        self.wysiwyg_ai_assistant = AIAssistantPanel(self)
        self.wysiwyg_ai_assistant.ai_request.connect(self.ai_manager.process_request)
        self.wysiwyg_ai_assistant.hide()  # 默认隐藏
        wysiwyg_layout.addWidget(self.wysiwyg_ai_assistant, 1)
        if hasattr(self.ai_manager, 'response_chunked'):
            self.ai_manager.response_chunked.connect(self.wysiwyg_ai_assistant.display_response_chunk)

        # 添加标签页
        self.tab_widget.addTab(self.three_column_layout, self._get_text('three_column_mode'))
        self.tab_widget.addTab(self.wysiwyg_container, self._get_text('wysiwyg_mode'))

        # Enable closable tabs for PDF viewer
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)
        # Hide close buttons for main editors
        try:
            self.tab_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)
            self.tab_widget.tabBar().setTabButton(1, QTabBar.ButtonPosition.RightSide, None)
        except Exception:
            pass  # Fail safe

        self.setCentralWidget(self.tab_widget)

        # Status bar
        self.status = QStatusBar(self)
        self.setStatusBar(self.status)

        # Connect editor changes
        self.editor.textChanged.connect(self._on_text_changed)
        self.wysiwyg_editor.textChanged.connect(self._on_wysiwyg_changed)
        self.tab_widget.currentChanged.connect(self._on_tab_changed)

        # Actions and toolbars
        self._init_actions()
        self._init_toolbar()
        self._init_menubar()

        # Initial render
        self.render_preview()
        
        # 初始化WYSIWYG编辑器
        self.wysiwyg_editor.set_markdown("")
        self.wysiwyg_editor.set_dark_mode(self._dark_mode)

    def _get_text(self, key: str) -> str:
        """Get localized text"""
        texts = {
            'zh': {
                'file_menu': '文件',
                'view_menu': '视图', 
                'language_menu': '语言',
                'new': '新建',
                'open': '打开',
                'save': '保存',
                'save_as': '另存为',
                'print': '打开打印',
                'export_pdf': '导出 PDF',
                'export_word': '导出 Word',
                'toggle_theme': '切换主题',
                'help_menu': '帮助',
                'check_updates': '检查更新',
                'insert_image': '插入图片',
                'import_pdf': '导入 PDF (为 Markdown)',
                'merge_pdf': '合并 PDF…',
                'split_pdf': '拆分 PDF…',
                'pdf_tools_menu': 'PDF 工具',
                'toggle_ai': '显示AI助手',
                'three_column_mode': '三栏编辑',
                'wysiwyg_mode': 'WYSIWYG 编辑',
                'zen_mode': '禅模式',
                'themes': '主题'
            },
            'en': {
                'file_menu': 'File',
                'view_menu': 'View',
                'language_menu': 'Language', 
                'new': 'New',
                'open': 'Open',
                'save': 'Save',
                'save_as': 'Save As',
                'print': 'Open for Print',
                'export_pdf': 'Export PDF',
                'export_word': 'Export Word',
                'toggle_theme': 'Toggle Theme',
                'help_menu': 'Help',
                'check_updates': 'Check for Updates',
                'insert_image': 'Insert Image',
                'import_pdf': 'Import PDF (as Markdown)',
                'merge_pdf': 'Merge PDFs…',
                'split_pdf': 'Split PDF…',
                'pdf_tools_menu': 'PDF Tools',
                'toggle_ai': 'Toggle AI Assistant',
                'three_column_mode': 'Three Column Editor',
                'wysiwyg_mode': 'WYSIWYG Editor',
                'zen_mode': 'Zen Mode',
                'themes': 'Themes'
            }
        }
        return texts.get(self._current_language, {}).get(key, key)

    def set_language(self, lang: str):
        """Set interface language"""
        self._current_language = lang
        
        # Update language menu checkboxes
        self.lang_chinese_action.setChecked(lang == 'zh')
        self.lang_english_action.setChecked(lang == 'en')
        
        # Update UI texts
        self._update_ui_texts()

    def _update_ui_texts(self):
        """Update all UI texts according to current language"""
        # Update action texts
        self.new_action.setText(self._get_text('new'))
        self.open_action.setText(self._get_text('open'))
        self.save_action.setText(self._get_text('save'))
        self.save_as_action.setText(self._get_text('save_as'))
        self.print_action.setText(self._get_text('print'))
        self.export_pdf_action.setText(self._get_text('export_pdf'))
        self.export_word_action.setText(self._get_text('export_word'))
        self.toggle_theme_action.setText(self._get_text('toggle_theme'))
        self.insert_image_action.setText(self._get_text('insert_image'))
        if hasattr(self, 'import_pdf_action'):
            self.import_pdf_action.setText(self._get_text('import_pdf'))
        if hasattr(self, 'merge_pdf_action'):
            self.merge_pdf_action.setText(self._get_text('merge_pdf'))
        if hasattr(self, 'split_pdf_action'):
            self.split_pdf_action.setText(self._get_text('split_pdf'))
        if hasattr(self, 'pdf_tools_menu'):
            self.pdf_tools_menu.setTitle(self._get_text('pdf_tools_menu'))
        self.toggle_ai_action.setText(self._get_text('toggle_ai'))
        self.toggle_ai_action.setText(self._get_text('toggle_ai'))
        self.check_updates_action.setText(self._get_text('check_updates'))
        self.zen_mode_action.setText(self._get_text('zen_mode'))
        self.themes_menu.setTitle(self._get_text('themes'))
        
        # Update tab texts
        self.tab_widget.setTabText(0, self._get_text('three_column_mode'))
        self.tab_widget.setTabText(1, self._get_text('wysiwyg_mode'))
        
        # Recreate menu bar with new texts
        self.menuBar().clear()
        self._init_menubar()

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

        self.toggle_theme_action = QAction("切换深色模式", self)
        self.toggle_theme_action.setShortcut("Ctrl+T")
        self.toggle_theme_action.triggered.connect(self.toggle_theme)

        self.export_pdf_action = QAction("导出 PDF", self)
        self.export_pdf_action.setShortcut("Ctrl+Shift+P")
        self.export_pdf_action.triggered.connect(self.export_pdf)
        
        self.print_action = QAction("打印预览", self)
        self.print_action.setShortcut("Ctrl+P")
        self.print_action.triggered.connect(self.print_preview)

        self.export_word_action = QAction("导出 Word", self)
        self.export_word_action.setShortcut("Ctrl+Shift+W")
        self.export_word_action.triggered.connect(self.export_word)
        
        # 插入图片动作
        self.insert_image_action = QAction("插入图片", self)
        self.insert_image_action.setShortcut("Ctrl+Shift+I")
        self.insert_image_action.triggered.connect(self.insert_image)

        # Import PDF Action
        self.import_pdf_action = QAction("导入 PDF", self)
        self.import_pdf_action.triggered.connect(self.import_pdf_to_markdown)

        # Merge PDF Action
        self.merge_pdf_action = QAction("合并 PDF…", self)
        self.merge_pdf_action.triggered.connect(self.merge_pdfs)

        # Split PDF Action
        self.split_pdf_action = QAction("拆分 PDF…", self)
        self.split_pdf_action.triggered.connect(self.split_pdf)

        # Language menu actions
        self.lang_chinese_action = QAction("中文", self)
        self.lang_chinese_action.setCheckable(True)
        self.lang_chinese_action.setChecked(True)
        self.lang_chinese_action.triggered.connect(lambda: self.set_language('zh'))

        self.lang_english_action = QAction("English", self)
        self.lang_english_action.setCheckable(True)
        self.lang_english_action.triggered.connect(lambda: self.set_language('en'))
        
        # AI助手切换动作
        self.toggle_ai_action = QAction("显示AI助手", self)
        self.toggle_ai_action.setCheckable(True)
        self.toggle_ai_action.setChecked(False)
        self.toggle_ai_action.triggered.connect(self._toggle_wysiwyg_ai)

        # Zen Mode
        self.zen_mode_action = QAction("禅模式", self)
        self.zen_mode_action.setShortcut("F11")
        self.zen_mode_action.setCheckable(True)
        self.zen_mode_action.triggered.connect(self.toggle_zen_mode)

        # Themes
        self.theme_actions = {}
        themes = ["Default", "Midnight Coffee", "Forest Walk", "Paper & Ink"]
        for theme in themes:
            action = QAction(theme, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, t=theme: self.set_theme(t))
            self.theme_actions[theme] = action
        self.theme_actions["Default"].setChecked(True)

        # Update action
        self.check_updates_action = QAction(self._get_text('check_updates'), self)
        self.check_updates_action.triggered.connect(self._on_check_updates)

    def _init_toolbar(self):
        tb = QToolBar("Main", self)
        tb.addAction(self.new_action)
        tb.addAction(self.open_action)
        tb.addAction(self.save_action)
        tb.addSeparator()
        tb.addAction(self.insert_image_action)
        tb.addAction(self.save_as_action)
        tb.addSeparator()
        tb.addAction(self.print_action)
        tb.addAction(self.export_pdf_action)
        tb.addAction(self.export_word_action)
        tb.addSeparator()
        tb.addAction(self.toggle_theme_action)
        self.addToolBar(tb)

    def _init_menubar(self):
        """Initialize menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu(self._get_text('file_menu'))
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.print_action)
        file_menu.addAction(self.export_pdf_action)
        file_menu.addAction(self.export_word_action)
        file_menu.addSeparator()
        file_menu.addAction(self.insert_image_action)
        file_menu.addSeparator()

        # PDF Tools submenu
        self.pdf_tools_menu = file_menu.addMenu(self._get_text('pdf_tools_menu'))
        if hasattr(self, 'import_pdf_action'):
            self.pdf_tools_menu.addAction(self.import_pdf_action)
        self.pdf_tools_menu.addAction(self.merge_pdf_action)
        self.pdf_tools_menu.addAction(self.split_pdf_action)
        
        # View menu
        view_menu = menubar.addMenu(self._get_text('view_menu'))
        view_menu.addAction(self.toggle_theme_action)
        view_menu.addSeparator()
        
        # Themes Submenu
        self.themes_menu = view_menu.addMenu(self._get_text('themes'))
        for action in self.theme_actions.values():
            self.themes_menu.addAction(action)
            
        view_menu.addSeparator()
        view_menu.addAction(self.zen_mode_action)
        view_menu.addSeparator()
        view_menu.addAction(self.toggle_ai_action)
        
        # Language menu
        lang_menu = menubar.addMenu(self._get_text('language_menu'))
        lang_menu.addAction(self.lang_chinese_action)
        lang_menu.addAction(self.lang_english_action)

        # Help menu
        help_menu = menubar.addMenu(self._get_text('help_menu'))
        help_menu.addAction(self.check_updates_action)

    # Slots
    def _on_text_changed(self):
        self._dirty = True
        text = self.editor.toPlainText()
        self.status.showMessage(f"字数: {len(text)}", 1500)
        self._render_timer.start()

    def _on_tab_close_requested(self, index: int):
        # Prevent closing main editor tabs
        if index < 2:
            return
        
        widget = self.tab_widget.widget(index)
        if widget:
            widget.deleteLater()
        self.tab_widget.removeTab(index)

    def _on_check_updates(self):
        self.update_manager.check_for_updates(self)

    def render_preview(self):
        text = self.editor.toPlainText()
        # Pass current file path as base path for image resolution
        base_path = str(self._current_file) if self._current_file else None
        html = self.renderer.to_html(text, dark=self._dark_mode, base_path=base_path)

        base_dir = Path(self._current_file).parent if self._current_file else Path.cwd()
        base_url = QUrl.fromLocalFile(str(base_dir.resolve()))
        # Ensure the base URL is treated as a directory for relative resources
        if not base_url.path().endswith('/'):
            base_url.setPath(base_url.path() + '/')

        self.preview.setHtml(html, base_url)
        
        # 同时更新WYSIWYG编辑器（如果不是当前活动标签页则不更新，避免循环）
        if self.tab_widget.currentIndex() != 1:  # 不是WYSIWYG标签页
            self.wysiwyg_editor.set_markdown(text)

    def _on_wysiwyg_changed(self, markdown_text: str):
        """WYSIWYG编辑器内容改变时的处理"""
        # 更新传统编辑器内容（避免触发textChanged信号）
        self.editor.blockSignals(True)
        self.editor.setPlainText(markdown_text)
        self.editor.blockSignals(False)
        
        # 更新预览
        base_path = str(self._current_file) if self._current_file else None
        html = self.renderer.to_html(markdown_text, dark=self._dark_mode, base_path=base_path)

        base_dir = Path(self._current_file).parent if self._current_file else Path.cwd()
        base_url = QUrl.fromLocalFile(str(base_dir.resolve()))
        if not base_url.path().endswith('/'):
            base_url.setPath(base_url.path() + '/')

        self.preview.setHtml(html, base_url)
        
        # 标记为已修改
        self._dirty = True
        self._update_title()
        
        # 更新状态栏
        self.status.showMessage(f"字数: {len(markdown_text)}", 1500)

    def _on_tab_changed(self, index: int):
        """标签页切换时的处理"""
        if index == 1:  # 切换到WYSIWYG模式
            # 同步传统编辑器的内容到WYSIWYG编辑器
            text = self.editor.toPlainText()
            self.wysiwyg_editor.set_base_path(self._current_file, re_render=False)
            self.wysiwyg_editor.set_markdown(text)
            # 设置暗色模式
            self.wysiwyg_editor.set_dark_mode(self._dark_mode)
        elif index == 0:  # 切换到三栏模式
            # 同步内容到三栏模式的编辑器和预览
            text = self.editor.toPlainText()
            self.render_preview()

    def _on_layout_changed(self, proportions: list):
        """三栏布局比例改变时的处理"""
        # 可以在这里添加布局变化的响应逻辑
        # 例如：调整字体大小、更新UI元素等
        self.status.showMessage(f"Layout: {proportions[0]}%-{proportions[1]}%-{proportions[2]}%", 2000)

    # File ops
    def new_file(self):
        if not self._confirm_discard_changes():
            return
        self.editor.clear()
        self.wysiwyg_editor.set_base_path(None, re_render=False)
        self.wysiwyg_editor.set_markdown("")
        self._current_file = None
        self._dirty = False
        self._update_title()
        self.render_preview()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "打开文件", str(Path.home()), "Markdown (*.md);;PDF Files (*.pdf)")
        if not path:
            return
        
        file_path = Path(path)
        if file_path.suffix.lower() == '.pdf':
            self.open_pdf_viewer(file_path)
            return
            
        if not self._confirm_discard_changes():
            return
        self.load_file(file_path)

    def open_pdf_viewer(self, path: Path):
        """Open PDF in a new viewer tab."""
        viewer = PDFViewer(self)
        try:
            viewer.load_file(str(path))
            # Add tab
            tab_label = path.name
            idx = self.tab_widget.addTab(viewer, f"📄 {tab_label}")
            self.tab_widget.setCurrentIndex(idx)
            self.status.showMessage(f"Opened PDF: {path.name}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open PDF: {e}")

    def import_pdf_to_markdown(self):
        """Import PDF text into current editor."""
        if not self._confirm_discard_changes():
            return
            
        path, _ = QFileDialog.getOpenFileName(self, "Import PDF as Markdown", str(Path.home()), "PDF Files (*.pdf)")
        if not path:
            return
            
        # Show busy cursor
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            md_text = PDFConverter.to_markdown(str(path))
            if md_text:
                self.editor.setPlainText(md_text)
                self.wysiwyg_editor.set_markdown(md_text)
                self._current_file = None 
                self._dirty = True
                self._update_title()
                self.status.showMessage("PDF imported successfully", 3000)
            else:
                QMessageBox.warning(self, "Import Failed", "Could not extract text from PDF.")
        finally:
            QApplication.restoreOverrideCursor()

    def merge_pdfs(self):
        """Open the PDF merge dialog."""
        dlg = PDFMergeDialog(self)
        dlg.exec()

    def split_pdf(self):
        """Open the PDF split dialog."""
        dlg = PDFSplitDialog(self)
        dlg.exec()

    def load_file(self, file_path: Path):
        """加载指定的文件（供外部调用，如命令行参数）"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.editor.setPlainText(content)
                self.wysiwyg_editor.set_base_path(file_path, re_render=False)
                self.wysiwyg_editor.set_markdown(content)
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
            self.wysiwyg_editor.set_base_path(self._current_file)
            self._dirty = False
            self._update_title()
            self.status.showMessage(f"已保存为: {path}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "保存失败", str(e))

    def toggle_theme(self):
        self._dark_mode = not self._dark_mode
        self.render_preview()
        # 同时更新WYSIWYG编辑器的主题
        self.wysiwyg_editor.set_dark_mode(self._dark_mode)

    def toggle_zen_mode(self, checked: bool):
        """Toggle Zen Mode (Distraction Free)"""
        self._zen_mode = checked
        if checked:
            self.menuBar().hide()
            self.status.hide()
            # Hide toolbar if exists (we created it in _init_toolbar but didn't save reference to self, need to find it)
            for toolbar in self.findChildren(QToolBar):
                toolbar.hide()
            self.showFullScreen()
        else:
            self.menuBar().show()
            self.status.show()
            for toolbar in self.findChildren(QToolBar):
                toolbar.show()
            self.showNormal()

    def set_theme(self, theme_name: str):
        """Set application theme"""
        self._current_theme = theme_name
        
        # Update check states
        for name, action in self.theme_actions.items():
            action.setChecked(name == theme_name)
            
        # Apply theme styles
        if theme_name == "Midnight Coffee":
            self.setStyleSheet("""
                QMainWindow { background-color: #2b2b2b; color: #dcdcdc; }
                QTextEdit { background-color: #3c3f41; color: #dcdcdc; border: none; font-family: 'Consolas', 'Monaco', monospace; font-size: 14px; }
                QStatusBar { background-color: #2b2b2b; color: #808080; }
                QMenuBar { background-color: #2b2b2b; color: #dcdcdc; }
                QMenuBar::item:selected { background-color: #3c3f41; }
                QMenu { background-color: #2b2b2b; color: #dcdcdc; border: 1px solid #3c3f41; }
                QMenu::item:selected { background-color: #3c3f41; }
            """)
            self._dark_mode = True
        elif theme_name == "Forest Walk":
            self.setStyleSheet("""
                QMainWindow { background-color: #f0f5f0; color: #2e3b2e; }
                QTextEdit { background-color: #ffffff; color: #2e3b2e; border: 1px solid #d0dcd0; font-family: 'Georgia', serif; font-size: 15px; }
                QStatusBar { background-color: #e0e5e0; color: #4e5b4e; }
            """)
            self._dark_mode = False
        elif theme_name == "Paper & Ink":
            self.setStyleSheet("""
                QMainWindow { background-color: #fdfbf7; color: #1a1a1a; }
                QTextEdit { background-color: #fffefc; color: #1a1a1a; border: none; font-family: 'Times New Roman', serif; font-size: 16px; }
                QStatusBar { background-color: #fdfbf7; color: #5a5a5a; }
            """)
            self._dark_mode = False
        else: # Default
            self.setStyleSheet("")
            self._dark_mode = False
            
        self.render_preview()
        self.wysiwyg_editor.set_dark_mode(self._dark_mode)

    def export_pdf(self):
        """Export current document to PDF using rendered preview."""
        path, _ = QFileDialog.getSaveFileName(
            self, "导出 PDF", str(Path.home() / "document.pdf"), "PDF Files (*.pdf)"
        )
        if not path:
            return
        
        try:
            from PyQt6.QtCore import QMarginsF, QEventLoop
            from PyQt6.QtGui import QPageLayout, QPageSize
            
            # 使用 Qt 原生 PDF 打印（无需 GTK 依赖）
            page_layout = QPageLayout(
                QPageSize(QPageSize.PageSizeId.A4),
                QPageLayout.Orientation.Portrait,
                QMarginsF(15, 15, 15, 15)
            )
            
            # 创建事件循环等待 PDF 生成完成
            loop = QEventLoop()
            
            def on_pdf_printed(file_path, success):
                loop.quit()
                if success:
                    self.status.showMessage(f"已导出 PDF: {path}", 3000)
                    QMessageBox.information(self, "导出成功", f"PDF 已保存到:\n{path}")
                else:
                    QMessageBox.critical(self, "导出失败", "PDF 生成失败")
            
            # 使用预览窗口的渲染结果直接打印
            self.preview.page().printToPdf(str(path), page_layout)
            self.preview.page().pdfPrintingFinished.connect(on_pdf_printed)
            
            # 等待 PDF 生成完成
            loop.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出 PDF 时出错:\n{str(e)}")

    def print_preview(self):
        """Show print/save dialog for the rendered markdown."""
        try:
            from PyQt6.QtCore import QMarginsF, QEventLoop, QUrl
            from PyQt6.QtGui import QPageLayout, QPageSize, QDesktopServices
            import tempfile
            import os
            
            # 创建临时 PDF 文件
            temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
            temp_pdf_path = temp_pdf.name
            temp_pdf.close()
            
            # 设置页面布局
            page_layout = QPageLayout(
                QPageSize(QPageSize.PageSizeId.A4),
                QPageLayout.Orientation.Portrait,
                QMarginsF(15, 15, 15, 15)
            )
            
            # 使用事件循环等待 PDF 生成
            loop = QEventLoop()
            pdf_success = [False]
            
            def on_pdf_ready(file_path, success):
                pdf_success[0] = success
                loop.quit()
            
            # 生成临时 PDF
            self.preview.page().printToPdf(temp_pdf_path, page_layout)
            self.preview.page().pdfPrintingFinished.connect(on_pdf_ready)
            loop.exec()
            
            if pdf_success[0]:
                # 用系统默认 PDF 查看器打开（通常支持打印）
                QDesktopServices.openUrl(QUrl.fromLocalFile(temp_pdf_path))
                self.status.showMessage("已在默认 PDF 查看器中打开，您可以从那里打印", 5000)
            else:
                QMessageBox.warning(self, "预览失败", "无法生成预览 PDF")
                if os.path.exists(temp_pdf_path):
                    os.unlink(temp_pdf_path)
                    
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            QMessageBox.critical(self, "打印预览失败", f"无法显示打印预览:\n{str(e)}\n\n{error_details}")

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


        
    def _on_ai_response(self, response):
        """处理AI响应"""
        if response.success:
            self.ai_assistant.display_response(response.content)
        else:
            self.ai_assistant.set_status(f"Error: {response.error_message}")
            
    def _on_ai_status_changed(self, status: str):
        """处理AI状态变化"""
        self.ai_assistant.set_status(status)
        if hasattr(self, 'wysiwyg_ai_assistant'):
            self.wysiwyg_ai_assistant.set_status(status)
        self.status.showMessage(status, 3000)
        
    def _toggle_wysiwyg_ai(self, checked: bool):
        """切换WYSIWYG模式中的AI助手显示"""
        if hasattr(self, 'wysiwyg_ai_assistant'):
            if checked:
                self.wysiwyg_ai_assistant.show()
            else:
                self.wysiwyg_ai_assistant.hide()
                
    def insert_image(self):
        """插入图片到Markdown文档"""
        # 打开文件对话框选择图片
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片文件",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.gif *.bmp *.svg);;所有文件 (*)"
        )
        
        if not file_path:
            return
            
        # 获取文件名
        import os
        filename = os.path.basename(file_path)
        
        # 决定使用相对路径还是绝对路径
        display_path = self._get_optimal_image_path(file_path)
        
        # 创建Markdown图片语法
        current_tab = self.tab_widget.currentIndex()
        
        if current_tab == 0:  # 三栏模式
            # 插入到文本编辑器
            cursor = self.editor.textCursor()
            if cursor.hasSelection():
                # 如果有选中文本，将其作为alt文本
                alt_text = cursor.selectedText()
                markdown_image = f"![{alt_text}]({display_path})"
            else:
                # 使用文件名作为默认alt文本
                alt_text = os.path.splitext(filename)[0]  # 去掉扩展名
                markdown_image = f"![{alt_text}]({display_path})"
            cursor.insertText(markdown_image)
            
        elif current_tab == 1:  # WYSIWYG模式
            # 插入到WYSIWYG编辑器
            if hasattr(self.wysiwyg_editor, 'insert_image'):
                self.wysiwyg_editor.insert_image(file_path, filename)
            else:
                # 回退方案：显示消息
                QMessageBox.information(
                    self, 
                    "图片插入", 
                    f"图片路径: {display_path}\n请手动复制路径到编辑器"
                )
        
        # 触发预览更新
        self._render_timer.start()
        self.status.showMessage(f"已插入图片: {filename}", 3000)
            
    def _setup_drag_drop(self):
        """设置拖放功能"""
        self.editor.setAcceptDrops(True)
        
        # 重写编辑器的拖放事件
        original_drag_enter = self.editor.dragEnterEvent
        original_drop = self.editor.dropEvent
        
        def drag_enter_event(event):
            if event.mimeData().hasUrls():
                # 检查是否包含图片文件
                for url in event.mimeData().urls():
                    if url.isLocalFile():
                        file_path = url.toLocalFile()
                        if self._is_image_file(file_path):
                            event.acceptProposedAction()
                            return
            original_drag_enter(event)
            
        def drop_event(event):
            if event.mimeData().hasUrls():
                for url in event.mimeData().urls():
                    if url.isLocalFile():
                        file_path = url.toLocalFile()
                        if self._is_image_file(file_path):
                            self._insert_dropped_image(file_path)
                            event.acceptProposedAction()
                            return
            original_drop(event)
            
        self.editor.dragEnterEvent = drag_enter_event
        self.editor.dropEvent = drop_event
        
    def _is_image_file(self, file_path: str) -> bool:
        """检查文件是否为图片格式"""
        import os
        ext = os.path.splitext(file_path)[1].lower()
        return ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg']
        
    def _get_optimal_image_path(self, file_path: str) -> str:
        """获取图片的最佳路径格式"""
        import os
        from pathlib import Path
        
        # 如果当前有打开的文件，尝试使用相对路径
        if self._current_file:
            try:
                current_dir = self._current_file.parent
                image_path = Path(file_path)
                rel_path = os.path.relpath(image_path, current_dir)
                # 如果相对路径不会跳出太多层级，使用相对路径
                if not rel_path.startswith('..\\..\\') and image_path.exists():
                    return rel_path.replace('\\', '/')
            except ValueError:
                # 不同盘符，无法使用相对路径
                pass

        # 对于其他情况，直接返回标准 file:// URI，避免后续再转换
        try:
            return Path(file_path).resolve(strict=False).as_uri()
        except ValueError:
            # 如果路径无法转换为 URI，则退回规范化的 POSIX 格式
            return Path(file_path).resolve(strict=False).as_posix()
        
    def _insert_dropped_image(self, file_path: str):
        """插入拖放的图片"""
        import os
        
        try:
            # 获取文件名和最优路径
            filename = os.path.basename(file_path)
            alt_text = os.path.splitext(filename)[0]
            display_path = self._get_optimal_image_path(file_path)
            
            # 创建Markdown语法
            markdown_image = f"![{alt_text}]({display_path})\n"
            
            # 在当前光标位置插入
            cursor = self.editor.textCursor()
            cursor.insertText(markdown_image)
            
            # 触发预览更新
            self._render_timer.start()
            self.status.showMessage(f"已插入图片: {filename} (拖放)", 3000)
            
            print(f"✅ 拖放成功: {filename}")  # 调试信息
            
        except Exception as e:
            print(f"❌ 拖放错误: {e}")  # 调试信息
            self.status.showMessage(f"拖放图片失败: {str(e)}", 5000)

    # Events
    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        if self._dirty:
            ok = self._confirm_discard_changes()
            if not ok:
                event.ignore()
                return
        event.accept()
