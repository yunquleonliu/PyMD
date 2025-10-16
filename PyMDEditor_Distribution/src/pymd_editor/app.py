from __future__ import annotations

import os
from pathlib import Path

from PyQt6.QtCore import QTimer, Qt, QUrl
from PyQt6.QtGui import QAction, QCloseEvent
from PyQt6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QStatusBar,
    QTextEdit,
    QToolBar,
    QTabWidget,
    QWidget,
    QHBoxLayout,
)
from PyQt6.QtWebEngineWidgets import QWebEngineView

from .renderer import MarkdownRenderer
from .exporter import WordExporter, PDFExporter
from .wysiwyg_editor import EnhancedWYSIWYGEditor
from .three_column_layout import ThreeColumnLayout, AIAssistantPanel
from .ai_framework import AIManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyMD Editor - MVP")
        self.resize(1200, 800)

        # State
        self._current_file: Path | None = None
        self._dark_mode: bool = False
        self._dirty: bool = False
        self._current_language = 'zh'  # 初始化语言设置

        # Core widgets
        self.editor = QTextEdit(self)
        self._setup_drag_drop()  # 启用拖放功能
        self.preview = QWebEngineView(self)
        # Enable image loading and mixed content
        from PyQt6.QtWebEngineCore import QWebEngineSettings
        settings = self.preview.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
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
        self.ai_manager = AIManager()
        
        # 连接AI信号
        self.ai_assistant.ai_request.connect(self.ai_manager.process_request)
        self.ai_manager.response_received.connect(self._on_ai_response)
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
        
        # 添加标签页
        self.tab_widget.addTab(self.three_column_layout, self._get_text('three_column_mode'))
        self.tab_widget.addTab(self.wysiwyg_container, self._get_text('wysiwyg_mode'))
        
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
                'export_pdf': '导出 PDF',
                'export_word': '导出 Word',
                'toggle_theme': '切换主题',
                'three_column_mode': '三栏编辑',
                'wysiwyg_mode': 'WYSIWYG 编辑'
            },
            'en': {
                'file_menu': 'File',
                'view_menu': 'View',
                'language_menu': 'Language', 
                'new': 'New',
                'open': 'Open',
                'save': 'Save',
                'save_as': 'Save As',
                'export_pdf': 'Export PDF',
                'export_word': 'Export Word',
                'toggle_theme': 'Toggle Theme',
                'three_column_mode': 'Three Column Editor',
                'wysiwyg_mode': 'WYSIWYG Editor'
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
        self.export_pdf_action.setText(self._get_text('export_pdf'))
        self.export_word_action.setText(self._get_text('export_word'))
        self.toggle_theme_action.setText(self._get_text('toggle_theme'))
        
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

        self.toggle_theme_action = QAction("切换主题", self)
        self.toggle_theme_action.setShortcut("Ctrl+T")
        self.toggle_theme_action.triggered.connect(self.toggle_theme)

        self.export_pdf_action = QAction("导出 PDF", self)
        self.export_pdf_action.setShortcut("Ctrl+Shift+P")
        self.export_pdf_action.triggered.connect(self.export_pdf)

        self.export_word_action = QAction("导出 Word", self)
        self.export_word_action.setShortcut("Ctrl+Shift+W")
        self.export_word_action.triggered.connect(self.export_word)
        
        # 插入图片动作
        self.insert_image_action = QAction("插入图片", self)
        self.insert_image_action.setShortcut("Ctrl+Shift+I")
        self.insert_image_action.triggered.connect(self.insert_image)

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

    def _init_toolbar(self):
        tb = QToolBar("Main", self)
        tb.addAction(self.new_action)
        tb.addAction(self.open_action)
        tb.addAction(self.save_action)
        tb.addSeparator()
        tb.addAction(self.insert_image_action)
        tb.addAction(self.save_as_action)
        tb.addSeparator()
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
        file_menu.addAction(self.export_pdf_action)
        file_menu.addAction(self.export_word_action)
        file_menu.addSeparator()
        file_menu.addAction(self.insert_image_action)
        
        # View menu
        view_menu = menubar.addMenu(self._get_text('view_menu'))
        view_menu.addAction(self.toggle_theme_action)
        view_menu.addSeparator()
        view_menu.addAction(self.toggle_ai_action)
        
        # Language menu
        lang_menu = menubar.addMenu(self._get_text('language_menu'))
        lang_menu.addAction(self.lang_chinese_action)
        lang_menu.addAction(self.lang_english_action)

    # Slots
    def _on_text_changed(self):
        self._dirty = True
        text = self.editor.toPlainText()
        self.status.showMessage(f"字数: {len(text)}", 1500)
        self._render_timer.start()

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
