from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QUrl, pyqtSignal, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt

from .renderer import MarkdownRenderer
from .html_to_markdown import html_to_markdown


class WYSIWYGEditor(QWidget):
    """所见即所得的Markdown编辑器组件"""
    
    textChanged = pyqtSignal(str)  # 当内容改变时发出信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.renderer = MarkdownRenderer()
        self._markdown_content = ""
        self._dark_mode = False
        self._edit_mode = True  # 始终处于编辑模式
        self._base_path: Path | None = None
        
        self._setup_ui()
        self._setup_web_view()
        
        # 防抖定时器
        self._update_timer = QTimer()
        self._update_timer.setSingleShot(True)
        self._update_timer.setInterval(300)
        self._update_timer.timeout.connect(self._extract_content)
        
    def _setup_ui(self):
        """设置UI布局"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 工具栏 - 只保留格式化按钮
        toolbar = QHBoxLayout()
        
        # 编辑状态指示
        self.status_label = QPushButton("✏️ WYSIWYG编辑模式")
        self.status_label.setEnabled(False)
        self.status_label.setStyleSheet("QPushButton:disabled { color: #666; }")
        toolbar.addWidget(self.status_label)
        
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # Web视图
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
    def _setup_web_view(self):
        """设置Web视图"""
        # 创建自定义页面以处理内容编辑
        self.web_page = WYSIWYGWebPage(self.web_view)
        self.web_view.setPage(self.web_page)
        
        # 连接信号
        self.web_page.contentChanged.connect(self._on_content_changed)
        
    def _ensure_edit_mode(self):
        """确保处于编辑模式"""
        if not self._edit_mode:
            self._edit_mode = True
            self._enable_editing()
            
    def _enable_editing(self):
        """启用编辑功能"""
        # 注入JavaScript使内容可编辑
        js_code = """
        // 使内容可编辑
        var contentDiv = document.querySelector('.content');
        if (contentDiv) {
            contentDiv.contentEditable = true;
            contentDiv.style.outline = 'none';
            contentDiv.style.border = '2px dashed #ccc';
            contentDiv.style.minHeight = '400px';
            contentDiv.style.padding = '16px 24px';
        }
        
        // 添加编辑样式
        var style = document.createElement('style');
        style.setAttribute('data-wysiwyg', 'true');
        style.textContent = `
            .content[contenteditable="true"]:focus {
                border-color: #007acc !important;
            }
            .content[contenteditable="true"] {
                cursor: text;
            }
            .content *:hover {
                background-color: rgba(0, 122, 204, 0.1);
            }
        `;
        document.head.appendChild(style);
        
        // 监听内容变化
        if (typeof window.changeTimer === 'undefined') {
            window.changeTimer = null;
        }
        function notifyChange() {
            clearTimeout(window.changeTimer);
            window.changeTimer = setTimeout(() => {
                console.log('content_changed');
            }, 300);
        }
        
        if (contentDiv) {
            contentDiv.addEventListener('input', notifyChange);
            contentDiv.addEventListener('paste', notifyChange);
            contentDiv.addEventListener('keyup', notifyChange);
            contentDiv.addEventListener('focus', function() {
                console.log('editor_focused');
            });
        }
        """
        
        self.web_view.page().runJavaScript(js_code)
        
    def _disable_editing(self):
        """禁用编辑功能"""
        js_code = """
        var contentDiv = document.querySelector('.content');
        if (contentDiv) {
            contentDiv.contentEditable = false;
            contentDiv.style.border = 'none';
            contentDiv.style.boxShadow = 'none';
            contentDiv.style.cursor = 'default';
        }
        
        // 移除编辑样式
        var styles = document.querySelectorAll('style[data-wysiwyg]');
        styles.forEach(style => style.remove());
        """
        self.web_view.page().runJavaScript(js_code)
        
    def _on_content_changed(self):
        """内容改变时的处理"""
        if self._edit_mode:
            self._update_timer.start()
            
    def _extract_content(self):
        """从HTML中提取Markdown内容"""
        if not self._edit_mode:
            return
            
        js_code = """
        var content = document.querySelector('.content');
        if (content) {
            content.innerHTML;
        } else {
            '';
        }
        """
        
        def handle_result(html_content):
            """处理JavaScript执行结果"""
            if html_content:
                # 使用Python的HTML到Markdown转换器
                markdown_content = html_to_markdown(html_content)
                if markdown_content != self._markdown_content:
                    self._markdown_content = markdown_content
                    self.textChanged.emit(markdown_content)
                
        self.web_view.page().runJavaScript(js_code, handle_result)
        
    def set_markdown(self, text: str):
        """设置Markdown内容"""
        self._markdown_content = text
        self._render_content()
        
    def get_markdown(self) -> str:
        """获取当前Markdown内容"""
        return self._markdown_content
        
    def set_base_path(self, base_path: str | Path | None, *, re_render: bool = True):
        """设置渲染时使用的基础路径，确保图片和资源可以正确解析"""
        if base_path is None:
            self._base_path = Path.cwd()
            if re_render:
                self._render_content()
            return

        path = Path(base_path)
        if path.exists() and path.is_dir():
            self._base_path = path
        elif path.suffix:
            # 认为传入的是文件路径，使用其所在目录
            self._base_path = path.parent
        else:
            self._base_path = path

        if re_render:
            self._render_content()

    def _render_content(self):
        """渲染Markdown内容为HTML"""
        base_dir = self._base_path or Path.cwd()
        html = self.renderer.to_html(
            self._markdown_content,
            dark=self._dark_mode,
            base_path=str(base_dir)
        )

        resolved_dir = base_dir.resolve(strict=False)
        base_url = QUrl.fromLocalFile(str(resolved_dir))
        if not base_url.path().endswith('/'):
            base_url.setPath(base_url.path() + '/')

        self.web_view.setHtml(html, base_url)
        
        # 总是启用编辑模式
        def enable_edit():
            self._enable_editing()
        QTimer.singleShot(100, enable_edit)
            
    def set_dark_mode(self, dark: bool):
        """设置暗色模式"""
        self._dark_mode = dark
        self._render_content()
        
    def is_edit_mode(self) -> bool:
        """返回是否处于编辑模式"""
        return self._edit_mode


class WYSIWYGWebPage(QWebEnginePage):
    """自定义Web页面类，用于处理编辑事件"""
    
    contentChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        """处理JavaScript控制台消息"""
        if message == "content_changed":
            self.contentChanged.emit()
        # 调用父类方法以保持默认行为
        super().javaScriptConsoleMessage(level, message, lineNumber, sourceId)


class EnhancedWYSIWYGEditor(WYSIWYGEditor):
    """增强版WYSIWYG编辑器，包含更多编辑功能"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._add_formatting_toolbar()
        
    def _add_formatting_toolbar(self):
        """添加格式化工具栏"""
        # 在现有工具栏中添加格式化按钮
        toolbar_layout = self.layout().itemAt(0).layout()
        
        # 分隔符
        toolbar_layout.addWidget(self._create_separator())
        
        # 格式化按钮
        self.bold_button = QPushButton("𝐁")
        self.bold_button.setToolTip("粗体 (Ctrl+B)")
        self.bold_button.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.bold_button.clicked.connect(lambda: self._apply_format("bold"))
        toolbar_layout.addWidget(self.bold_button)
        
        self.italic_button = QPushButton("𝐼")
        self.italic_button.setToolTip("斜体 (Ctrl+I)")
        self.italic_button.setStyleSheet("font-style: italic; font-size: 14px;")
        self.italic_button.clicked.connect(lambda: self._apply_format("italic"))
        toolbar_layout.addWidget(self.italic_button)
        
        self.header_button = QPushButton("𝐇")
        self.header_button.setToolTip("标题")
        self.header_button.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.header_button.clicked.connect(lambda: self._apply_format("header"))
        toolbar_layout.addWidget(self.header_button)
        
        self.link_button = QPushButton("🔗")
        self.link_button.setToolTip("插入链接")
        self.link_button.clicked.connect(lambda: self._apply_format("link"))
        toolbar_layout.addWidget(self.link_button)
        
    def _create_separator(self):
        """创建分隔符"""
        separator = QWidget()
        separator.setFixedWidth(1)
        separator.setStyleSheet("background-color: #ccc; margin: 2px 4px;")
        return separator
        
    def _apply_format(self, format_type: str):
        """应用格式化"""
        # WYSIWYG模式下总是可以格式化
            
        format_scripts = {
            "bold": "document.execCommand('bold', false, null);",
            "italic": "document.execCommand('italic', false, null);",
            "header": """
                var selection = window.getSelection();
                if (selection.rangeCount > 0) {
                    var range = selection.getRangeAt(0);
                    var text = range.toString();
                    if (text) {
                        range.deleteContents();
                        var header = document.createElement('h2');
                        header.textContent = text;
                        range.insertNode(header);
                    }
                }
            """,
            "link": """
                var url = prompt('请输入链接地址:', 'https://');
                if (url) {
                    document.execCommand('createLink', false, url);
                }
            """
        }
        
        script = format_scripts.get(format_type, "")
        if script:
            self.web_view.page().runJavaScript(script)