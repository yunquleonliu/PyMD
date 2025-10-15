"""
三栏布局组件
支持左栏编辑器、中栏预览、右栏AI助手的响应式布局
"""

from PyQt6.QtCore import Qt, pyqtSignal, QSettings, QDateTime
from PyQt6.QtWidgets import (
    QWidget, QSplitter, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QToolBar, QComboBox,
    QTextEdit, QScrollArea
)
from .ai_settings import get_ai_manager, AISettingsDialog, AIProviderConfig
from .chat_components import ChatHistoryWidget, ChatInputWidget, ChatMessage, MessageType


class ThreeColumnLayout(QWidget):
    """三栏布局管理器"""
    
    # 信号
    layoutChanged = pyqtSignal(list)  # 当布局比例改变时发出信号
    
    # 预设布局
    LAYOUTS = {
        "default": [40, 40, 20],      # 默认均衡布局
        "focus_writing": [60, 40, 0], # 专注写作模式
        "ai_intensive": [30, 30, 40], # AI辅助模式
        "preview_only": [40, 60, 0],  # 预览优先模式
        "editor_only": [100, 0, 0],   # 纯编辑模式
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings()
        self._setup_ui()
        self._load_layout_preference()
        
    def _setup_ui(self):
        """设置UI结构"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 工具栏
        self.toolbar = self._create_toolbar()
        main_layout.addWidget(self.toolbar)
        
        # 三栏分割器
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setChildrenCollapsible(False)  # 禁止完全折叠
        self.main_splitter.splitterMoved.connect(self._on_splitter_moved)
        
        # 创建三个面板
        self.left_panel = self._create_panel("Editor")
        self.middle_panel = self._create_panel("Preview") 
        self.right_panel = self._create_panel("AI Assistant")
        
        # 添加到分割器
        self.main_splitter.addWidget(self.left_panel)
        self.main_splitter.addWidget(self.middle_panel)
        self.main_splitter.addWidget(self.right_panel)
        
        # 设置默认布局
        self.apply_layout("default")
        
        main_layout.addWidget(self.main_splitter)
        
    def _create_toolbar(self) -> QToolBar:
        """创建布局工具栏"""
        toolbar = QToolBar()
        toolbar.setFixedHeight(32)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #f0f0f0;
                border: none;
                border-bottom: 1px solid #d0d0d0;
                spacing: 8px;
                padding: 4px;
            }
            QToolBar QLabel {
                color: #666;
                font-size: 12px;
                padding: 0 8px;
            }
            QToolBar QPushButton {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
            }
            QToolBar QPushButton:hover {
                background-color: #e0e0e0;
                border-color: #999;
            }
            QToolBar QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QToolBar QPushButton:checked {
                background-color: #007acc;
                color: white;
                border-color: #005a9e;
            }
        """)
        
        # 布局标签
        toolbar.addWidget(QLabel("Layout:"))
        
        # 布局选择器
        self.layout_combo = QComboBox()
        self.layout_combo.addItems([
            "Default", "Focus Writing", "AI Intensive", 
            "Preview Only", "Editor Only"
        ])
        self.layout_combo.currentTextChanged.connect(self._on_layout_combo_changed)
        toolbar.addWidget(self.layout_combo)
        
        toolbar.addSeparator()
        
        # 快速布局按钮
        self.layout_buttons = {}
        
        btn_default = QPushButton("⚖️")
        btn_default.setToolTip("Default Layout (40-40-20)")
        btn_default.setCheckable(True)
        btn_default.clicked.connect(lambda: self.apply_layout("default"))
        self.layout_buttons["default"] = btn_default
        toolbar.addWidget(btn_default)
        
        btn_focus = QPushButton("✍️")
        btn_focus.setToolTip("Focus Writing (60-40-0)")
        btn_focus.setCheckable(True)
        btn_focus.clicked.connect(lambda: self.apply_layout("focus_writing"))
        self.layout_buttons["focus_writing"] = btn_focus
        toolbar.addWidget(btn_focus)
        
        btn_ai = QPushButton("🤖")
        btn_ai.setToolTip("AI Intensive (30-30-40)")
        btn_ai.setCheckable(True)
        btn_ai.clicked.connect(lambda: self.apply_layout("ai_intensive"))
        self.layout_buttons["ai_intensive"] = btn_ai
        toolbar.addWidget(btn_ai)
        
        btn_preview = QPushButton("👁️")
        btn_preview.setToolTip("Preview Focus (40-60-0)")
        btn_preview.setCheckable(True)
        btn_preview.clicked.connect(lambda: self.apply_layout("preview_only"))
        self.layout_buttons["preview_only"] = btn_preview
        toolbar.addWidget(btn_preview)
        
        toolbar.addSeparator()
        
        # 分割线锁定按钮
        self.lock_button = QPushButton("🔒")
        self.lock_button.setToolTip("Lock Splitter")
        self.lock_button.setCheckable(True)
        self.lock_button.toggled.connect(self._toggle_splitter_lock)
        toolbar.addWidget(self.lock_button)
        
        return toolbar
        
    def _create_panel(self, title: str) -> QFrame:
        """创建面板容器"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #d0d0d0;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 面板标题（调试用，后续可移除）
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                background-color: #f5f5f5;
                padding: 4px 8px;
                font-size: 12px;
                font-weight: bold;
                color: #666;
                border-bottom: 1px solid #e0e0e0;
            }
        """)
        layout.addWidget(title_label)
        
        # 内容区域（占位符）
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #fafafa;")
        layout.addWidget(content_widget)
        
        return panel
        
    def _on_layout_combo_changed(self, text: str):
        """布局下拉框改变事件"""
        layout_map = {
            "Default": "default",
            "Focus Writing": "focus_writing", 
            "AI Intensive": "ai_intensive",
            "Preview Only": "preview_only",
            "Editor Only": "editor_only"
        }
        
        layout_key = layout_map.get(text)
        if layout_key:
            self.apply_layout(layout_key)
            
    def apply_layout(self, layout_name: str):
        """应用指定的布局"""
        if layout_name not in self.LAYOUTS:
            return
            
        proportions = self.LAYOUTS[layout_name]
        self._update_splitter_sizes(proportions)
        self._update_button_states(layout_name)
        self._save_layout_preference(layout_name)
        
        # 发出信号
        self.layoutChanged.emit(proportions)
        
    def _update_splitter_sizes(self, proportions: list):
        """更新分割器大小"""
        total_width = self.main_splitter.width()
        if total_width <= 0:
            total_width = 1200  # 默认宽度
            
        sizes = []
        for prop in proportions:
            if prop == 0:
                sizes.append(0)
            else:
                sizes.append(int(total_width * prop / 100))
                
        self.main_splitter.setSizes(sizes)
        
        # 隐藏宽度为0的面板
        for i, size in enumerate(sizes):
            widget = self.main_splitter.widget(i)
            if widget:
                widget.setVisible(size > 0)
                
    def _update_button_states(self, active_layout: str):
        """更新按钮状态"""
        for layout_name, button in self.layout_buttons.items():
            button.setChecked(layout_name == active_layout)
            
        # 更新下拉框
        combo_map = {
            "default": "Default",
            "focus_writing": "Focus Writing",
            "ai_intensive": "AI Intensive", 
            "preview_only": "Preview Only",
            "editor_only": "Editor Only"
        }
        
        combo_text = combo_map.get(active_layout, "Default")
        self.layout_combo.blockSignals(True)
        self.layout_combo.setCurrentText(combo_text)
        self.layout_combo.blockSignals(False)
        
    def _on_splitter_moved(self):
        """分割器移动事件"""
        if not self.lock_button.isChecked():
            # 计算当前比例
            sizes = self.main_splitter.sizes()
            total = sum(sizes)
            
            if total > 0:
                proportions = [int(size * 100 / total) for size in sizes]
                self.layoutChanged.emit(proportions)
                
    def _toggle_splitter_lock(self, locked: bool):
        """切换分割器锁定状态"""
        self.main_splitter.setDisabled(locked)
        if locked:
            self.lock_button.setText("🔓")
            self.lock_button.setToolTip("Unlock Splitter")
        else:
            self.lock_button.setText("🔒")
            self.lock_button.setToolTip("Lock Splitter")
            
    def get_left_panel(self) -> QFrame:
        """获取左侧面板"""
        return self.left_panel
        
    def get_middle_panel(self) -> QFrame:
        """获取中间面板"""
        return self.middle_panel
        
    def get_right_panel(self) -> QFrame:
        """获取右侧面板"""
        return self.right_panel
        
    def set_panel_widget(self, panel: str, widget: QWidget):
        """设置面板内容"""
        panel_map = {
            "left": self.left_panel,
            "middle": self.middle_panel,
            "right": self.right_panel
        }
        
        target_panel = panel_map.get(panel)
        if not target_panel:
            return
            
        # 移除标题和占位符内容
        layout = target_panel.layout()
        while layout.count() > 0:
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # 添加新widget
        layout.addWidget(widget)
        
    def get_current_proportions(self) -> list:
        """获取当前布局比例"""
        sizes = self.main_splitter.sizes()
        total = sum(sizes)
        
        if total > 0:
            return [int(size * 100 / total) for size in sizes]
        else:
            return self.LAYOUTS["default"]
            
    def _save_layout_preference(self, layout_name: str):
        """保存布局偏好"""
        self.settings.setValue("layout/current", layout_name)
        proportions = self.LAYOUTS[layout_name]
        self.settings.setValue("layout/proportions", proportions)
        
    def _load_layout_preference(self):
        """加载布局偏好"""
        layout_name = self.settings.value("layout/current", "default")
        if layout_name in self.LAYOUTS:
            # 延迟应用布局，等待UI初始化完成
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(100, lambda: self.apply_layout(layout_name))


class AIAssistantPanel(QWidget):
    """AI助手面板（右侧面板内容）"""

    # 信号
    ai_request = pyqtSignal(str, str, dict)  # task_type, content, context

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_response = ""
        self.ai_manager = get_ai_manager()
        self.ai_manager.current_provider_changed.connect(self._on_provider_changed)
        self._setup_ui()
        self._connect_signals()
        self._update_ai_display()

    def _setup_ui(self):
        """设置AI助手面板UI"""
        # 设置整体面板样式
        self.setStyleSheet("""
            AIAssistantPanel {
                background-color: #fafafa;
                border-left: 1px solid #e1e5e9;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 现代化头部区域
        self._create_modern_header(layout)

        # 优雅的操作按钮区域
        self._create_action_buttons(layout)

        # 聊天区域
        self._create_chat_area(layout)

    def _create_modern_header(self, layout):
        """创建现代化的头部"""
        header_widget = QWidget()
        header_widget.setFixedHeight(70)
        header_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border-bottom: 1px solid #e9ecef;
            }
        """)

        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(16, 12, 16, 12)
        header_layout.setSpacing(12)

        # AI头像区域 - 更大的、更现代的
        avatar_container = QWidget()
        avatar_container.setFixedSize(44, 44)
        avatar_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 22px;
                border: 2px solid #ffffff;
            }
        """)

        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setContentsMargins(0, 0, 0, 0)

        self.ai_avatar_label = QLabel("🤖")
        self.ai_avatar_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: white;
                background: transparent;
            }
        """)
        self.ai_avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_layout.addWidget(self.ai_avatar_label)

        header_layout.addWidget(avatar_container)

        # 信息区域 - 更清晰的层次
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        self.ai_name_label = QLabel("AI Assistant")
        self.ai_name_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #1a1a1a;
                background: transparent;
            }
        """)
        info_layout.addWidget(self.ai_name_label)

        self.status_personality_label = QLabel("Ready to help with your writing")
        self.status_personality_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
                background: transparent;
            }
        """)
        self.status_personality_label.setWordWrap(True)
        info_layout.addWidget(self.status_personality_label)

        header_layout.addLayout(info_layout)
        header_layout.addStretch()

        # 设置按钮 - 更现代的样式
        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setToolTip("AI Settings")
        self.settings_btn.setFixedSize(32, 32)
        self.settings_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                font-size: 16px;
                border-radius: 6px;
                color: #6c757d;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                color: #495057;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
        """)
        self.settings_btn.clicked.connect(self._open_ai_settings)
        header_layout.addWidget(self.settings_btn)

        layout.addWidget(header_widget)

    def _create_action_buttons(self, layout):
        """创建优雅的操作按钮区域"""
        buttons_widget = QWidget()
        buttons_widget.setFixedHeight(50)
        buttons_widget.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-bottom: 1px solid #e9ecef;
            }
        """)

        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(16, 8, 16, 8)
        buttons_layout.setSpacing(8)

        # 按钮配置
        button_configs = [
            ("✨", "Improve", "#28a745"),
            ("📝", "Summarize", "#007bff"),
            ("🌐", "Translate", "#6f42c1"),
            ("💡", "Brainstorm", "#fd7e14"),
            ("🗑️", "Clear", "#dc3545")
        ]

        self.action_buttons = []

        for icon, tooltip, color in button_configs:
            btn = self._create_modern_button(icon, tooltip, color)
            buttons_layout.addWidget(btn)
            self.action_buttons.append(btn)

        # 分配按钮引用
        self.improve_btn, self.summarize_btn, self.translate_btn, self.brainstorm_btn, self.clear_chat_btn = self.action_buttons

        layout.addWidget(buttons_widget)

    def _create_modern_button(self, icon, tooltip, color):
        """创建现代化的按钮"""
        btn = QPushButton(icon)
        btn.setToolTip(tooltip)
        btn.setFixedSize(36, 36)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {self._darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(self._darken_color(color))};
            }}
        """)
        return btn

    def _darken_color(self, color):
        """使颜色变暗用于hover效果"""
        # 简单的颜色变暗逻辑
        if color == "#28a745": return "#218838"
        elif color == "#007bff": return "#0056b3"
        elif color == "#6f42c1": return "#5a359a"
        elif color == "#fd7e14": return "#e8680f"
        elif color == "#dc3545": return "#c82333"
        return color

    def _create_chat_area(self, layout):
        """创建聊天区域"""
        chat_widget = QWidget()
        chat_widget.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
            }
        """)

        chat_layout = QVBoxLayout(chat_widget)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(0)

        # 聊天历史
        self.chat_history = ChatHistoryWidget()
        chat_layout.addWidget(self.chat_history)

        # 聊天输入
        self.chat_input = ChatInputWidget()
        self.chat_input.message_sent.connect(self._on_chat_send)
        chat_layout.addWidget(self.chat_input)

        layout.addWidget(chat_widget)
        
    def set_status(self, status: str):
        """设置状态文本"""
        current_provider = self.ai_manager.get_current_provider()
        personality = current_provider.personality if current_provider else "AI assistant ready to help"
        self.status_personality_label.setText(f"{status} • {personality}")
        
    def get_improve_button(self) -> QPushButton:
        return self.improve_btn
        
    def get_summarize_button(self) -> QPushButton:
        return self.summarize_btn
        
    def get_translate_button(self) -> QPushButton:
        return self.translate_btn
        
    def get_brainstorm_button(self) -> QPushButton:
        return self.brainstorm_btn
        
    def _connect_signals(self):
        """连接信号槽"""
        self.improve_btn.clicked.connect(lambda: self._on_ai_action("improve"))
        self.summarize_btn.clicked.connect(lambda: self._on_ai_action("summarize"))
        self.translate_btn.clicked.connect(lambda: self._on_ai_action("translate"))
        self.brainstorm_btn.clicked.connect(lambda: self._on_ai_action("brainstorm"))
        self.clear_chat_btn.clicked.connect(self.clear_chat_history)
        
    def _on_ai_action(self, action: str):
        """处理AI操作"""
        # 获取当前选中的文本或全部内容
        content = self._get_editor_content()
        if not content:
            self.set_status("No content to process")
            return
            
        # 构建上下文
        context = {
            "action": action,
            "timestamp": QDateTime.currentDateTime().toString(),
            "content_length": len(content)
        }
        
        # 保存上下文用于响应处理
        self._last_context = context
        
        # 发射AI请求信号
        self.set_status(f"Processing {action}...")
        self.ai_request.emit(action, content, context)
        
    def _get_editor_content(self) -> str:
        """获取编辑器内容"""
        # 获取父窗口的编辑器内容
        try:
            # 找到主窗口
            main_window = self.parent()
            while main_window and not hasattr(main_window, 'editor'):
                main_window = main_window.parent()
                
            if main_window and hasattr(main_window, 'editor'):
                # 获取选中的文本，如果没有则获取全部文本
                cursor = main_window.editor.textCursor()
                if cursor.hasSelection():
                    return cursor.selectedText()
                else:
                    return main_window.editor.toPlainText()
                    
            return "No content available"
        except Exception as e:
            return f"Error getting content: {str(e)}"
        
    def get_clear_chat_button(self) -> QPushButton:
        return self.clear_chat_btn
        
    def clear_chat_history(self):
        """清空聊天历史"""
        self.chat_history.clear_history()
        self.set_status("Chat history cleared")
        
    def _on_chat_send(self, message: str):
        """发送聊天消息"""
        if not message.strip():
            return
            
        # 创建用户消息
        user_message = ChatMessage(
            message_type=MessageType.USER,
            content=message,
            metadata={"source": "chat_input"}
        )
        
        # 添加到聊天历史
        self.chat_history.add_message(user_message, "👤")
        
        # 显示打字指示器
        current_provider = self.ai_manager.get_current_provider()
        avatar = current_provider.avatar_url if current_provider else "🤖"
        self.chat_history.show_typing_indicator(avatar)
        
        # 构建上下文
        context = {
            "action": "chat",
            "timestamp": QDateTime.currentDateTime().toString(),
            "content_length": len(message),
            "is_chat": True
        }
        
        # 保存上下文用于响应处理
        self._last_context = context
        
        # 发射AI请求信号
        self.set_status("AI is thinking...")
        self.ai_request.emit("chat", message, context)
        
    def _on_chat_text_changed(self):
        """聊天文本变化时启用/禁用发送按钮"""
        has_text = bool(self.chat_input.toPlainText().strip())
        self.chat_send_btn.setEnabled(has_text)
        
    def display_response(self, response: str):
        """显示AI响应"""
        self.current_response = response
        
        # 隐藏打字指示器
        self.chat_history.hide_typing_indicator()
        
        # 如果是聊天响应，添加到聊天历史
        if hasattr(self, '_last_context') and self._last_context.get('is_chat'):
            ai_message = ChatMessage(
                message_type=MessageType.AI,
                content=response,
                metadata={"provider": self.ai_manager.current_provider_id}
            )
            
            current_provider = self.ai_manager.get_current_provider()
            avatar = current_provider.avatar_url if current_provider else "🤖"
            self.chat_history.add_message(ai_message, avatar)
        else:
            # 对于非聊天响应，仍然显示在旧的响应区域（如果存在）
            if hasattr(self, 'response_area'):
                self.response_area.setPlainText(response)
        
        self.set_status("Response received")
        
    def _on_insert_image(self):
        """插入图片按钮处理"""
        # 获取主窗口并调用插入图片方法
        main_window = self.parent()
        while main_window and not hasattr(main_window, 'insert_image'):
            main_window = main_window.parent()
            
        if main_window and hasattr(main_window, 'insert_image'):
            main_window.insert_image()

    def _on_provider_changed(self, provider_id: str):
        """AI提供商改变事件"""
        self._update_ai_display()

    def _update_ai_display(self):
        """更新AI显示信息"""
        current_provider = self.ai_manager.get_current_provider()
        if current_provider:
            self.ai_avatar_label.setText(current_provider.avatar_url or "🤖")
            self.ai_name_label.setText(current_provider.name)
            # 更新状态和个性描述
            personality = current_provider.personality or "AI assistant ready to help"
            self.status_personality_label.setText(f"Ready • {personality}")

    def _open_ai_settings(self):
        """打开AI设置对话框"""
        settings_dialog = AISettingsDialog(self)
        settings_dialog.settings_changed.connect(self._update_ai_display)
        settings_dialog.exec()