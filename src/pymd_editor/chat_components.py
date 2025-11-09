"""
聊天组件模块
包含聊天气泡UI、输入指示器、消息时间戳和会话持久化功能
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QSettings, pyqtSignal, QObject
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea,
    QSizePolicy, QTextEdit, QPushButton, QSpacerItem
)
from PyQt6.QtGui import QFont, QPalette, QColor


class MessageType:
    """消息类型枚举"""
    USER = "user"
    AI = "ai"
    SYSTEM = "system"


@dataclass
class ChatMessage:
    """聊天消息数据类"""
    message_type: str
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = None

    def __init__(self, message_type: str, content: str, timestamp: datetime = None, metadata: Dict[str, Any] = None):
        self.message_type = message_type
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式用于序列化"""
        return {
            "message_type": self.message_type,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatMessage':
        """从字典创建消息对象"""
        return cls(
            message_type=data["message_type"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data.get("metadata", {})
        )


class ChatBubbleWidget(QFrame):
    """聊天气泡组件"""

    def __init__(self, message: ChatMessage, avatar: str = "", parent=None):
        super().__init__(parent)
        self.message = message
        self.avatar = avatar
        self._setup_ui()

    def _setup_ui(self):
        """设置气泡UI"""
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # 主布局
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 4, 8, 4)
        main_layout.setSpacing(8)

        # 根据消息类型设置布局方向
        if self.message.message_type == MessageType.USER:
            # 用户消息：头像在右边，气泡在左边
            main_layout.addStretch()
            self._create_bubble_content(main_layout)
            self._create_avatar(main_layout)
        else:
            # AI消息：头像在左边，气泡在右边
            self._create_avatar(main_layout)
            self._create_bubble_content(main_layout)
            main_layout.addStretch()

    def _create_avatar(self, layout: QHBoxLayout):
        """创建头像"""
        avatar_container = QWidget()
        avatar_container.setFixedSize(36, 36)
        avatar_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e2e8f0, stop:1 #cbd5e0);
                border-radius: 18px;
                border: 2px solid #ffffff;
            }
        """)

        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setContentsMargins(0, 0, 0, 0)

        avatar_label = QLabel(self.avatar or "🤖")
        avatar_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                background: transparent;
                color: #4a5568;
            }
        """)
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_layout.addWidget(avatar_label)

        layout.addWidget(avatar_container)

    def _create_bubble_content(self, layout: QHBoxLayout):
        """创建气泡内容"""
        # 气泡容器
        bubble_container = QWidget()
        bubble_layout = QVBoxLayout(bubble_container)
        bubble_layout.setContentsMargins(0, 0, 0, 0)
        bubble_layout.setSpacing(0)

        # 消息内容
        content_label = QLabel(self.message.content)
        content_label.setWordWrap(True)
        content_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        content_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        bubble_layout.addWidget(content_label)

        # 设置气泡样式
        self._set_bubble_style(bubble_container, self.message.message_type)

        layout.addWidget(bubble_container)

    def _set_bubble_style(self, bubble: QWidget, message_type: str):
        """设置气泡样式"""
        if message_type == MessageType.USER:
            # 用户消息样式（现代蓝色渐变，无边框）
            bubble.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #667eea, stop:1 #764ba2);
                    border-radius: 18px;
                    padding: 12px 16px;
                    margin: 4px 12px 4px 40px;
                    max-width: 320px;
                }
                QLabel {
                    color: white;
                    font-size: 13px;
                    line-height: 1.4;
                }
            """)
        else:
            # AI消息样式（现代白色，无边框，通过背景对比创建边界）
            bubble.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #ffffff, stop:1 #f8f9fa);
                    border-radius: 20px;
                    padding: 12px 16px;
                    margin: 4px 40px 4px 12px;
                    max-width: 320px;
                }
                QLabel {
                    color: #2d3748;
                    font-size: 13px;
                    line-height: 1.4;
                }
            """)

    def _format_timestamp(self) -> str:
        """格式化时间戳"""
        now = datetime.now()
        if self.message.timestamp.date() == now.date():
            # 今天的消息只显示时间
            return self.message.timestamp.strftime("%H:%M")
        elif self.message.timestamp.year == now.year:
            # 今年内的消息显示月日时间
            return self.message.timestamp.strftime("%m-%d %H:%M")
        else:
            # 更早的消息显示完整日期时间
            return self.message.timestamp.strftime("%Y-%m-%d %H:%M")


class TypingIndicatorWidget(QWidget):
    """打字指示器组件"""

    def __init__(self, avatar: str = "🤖", parent=None):
        super().__init__(parent)
        self.avatar = avatar
        self.dots = []
        self.animation_timers = []
        self._setup_ui()
        self._start_animation()

    def _setup_ui(self):
        """设置UI"""
        self.setFixedHeight(50)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(12)

        # 头像
        avatar_container = QWidget()
        avatar_container.setFixedSize(36, 36)
        avatar_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e2e8f0, stop:1 #cbd5e0);
                border-radius: 18px;
                border: 2px solid #ffffff;
            }
        """)

        avatar_layout = QVBoxLayout(avatar_container)
        avatar_layout.setContentsMargins(0, 0, 0, 0)

        avatar_label = QLabel(self.avatar)
        avatar_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                background: transparent;
                color: #4a5568;
            }
        """)
        avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_layout.addWidget(avatar_label)

        layout.addWidget(avatar_container)

        # 打字指示器容器
        indicator_container = QWidget()
        indicator_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border-radius: 16px;
                padding: 8px 12px;
                border: 1px solid #e9ecef;
            }
        """)

        indicator_layout = QHBoxLayout(indicator_container)
        indicator_layout.setContentsMargins(8, 4, 8, 4)
        indicator_layout.setSpacing(4)

        # "Typing..." 文本
        typing_label = QLabel("Typing")
        typing_label.setStyleSheet("""
            QLabel {
                color: #718096;
                font-size: 12px;
                font-weight: 500;
            }
        """)
        indicator_layout.addWidget(typing_label)

        # 创建三个点
        for i in range(3):
            dot = QLabel("●")
            dot.setStyleSheet("""
                QLabel {
                    color: #a0aec0;
                    font-size: 8px;
                }
            """)
            dot.setFixedSize(6, 6)
            self.dots.append(dot)
            indicator_layout.addWidget(dot)

        layout.addWidget(indicator_container)
        layout.addStretch()

    def _start_animation(self):
        """开始动画"""
        for i, dot in enumerate(self.dots):
            timer = QTimer(self)
            timer.timeout.connect(lambda idx=i: self._animate_dot(idx))
            timer.start(500 + i * 200)  # 交错开始
            self.animation_timers.append(timer)

    def _animate_dot(self, index: int):
        """动画单个点"""
        dot = self.dots[index]
        current_opacity = dot.property("opacity") or 1.0

        if current_opacity < 0.3:
            new_opacity = 1.0
        else:
            new_opacity = current_opacity - 0.3

        dot.setProperty("opacity", new_opacity)
        # 强制重绘
        dot.update()

    def stop_animation(self):
        """停止动画"""
        for timer in self.animation_timers:
            timer.stop()
        self.animation_timers.clear()

    def hide(self):
        """隐藏时停止动画"""
        self.stop_animation()
        super().hide()


class ChatHistoryWidget(QScrollArea):
    """聊天历史组件"""

    message_added = pyqtSignal(ChatMessage)  # 新消息添加信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.messages: List[ChatMessage] = []
        self.typing_indicator = None
        self._setup_ui()
        self._load_conversation_history()

    def _setup_ui(self):
        """设置UI"""
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f5f7fa;
            }
            QScrollBar:vertical {
                width: 6px;
                background-color: transparent;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e0;
                border-radius: 3px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0aec0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        # 创建内容容器
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(8, 12, 8, 12)
        self.content_layout.setSpacing(12)
        self.content_layout.addStretch()  # 添加底部伸缩空间

        self.setWidget(self.content_widget)

    def add_message(self, message: ChatMessage, avatar: str = ""):
        """添加消息"""
        self.messages.append(message)

        # 移除打字指示器（如果存在）
        if self.typing_indicator:
            self.typing_indicator.stop_animation()
            self.content_layout.removeWidget(self.typing_indicator)
            self.typing_indicator.deleteLater()
            self.typing_indicator = None

        # 创建气泡组件
        bubble = ChatBubbleWidget(message, avatar)
        self.content_layout.insertWidget(self.content_layout.count() - 1, bubble)

        # 发送信号
        self.message_added.emit(message)

        # 自动滚动到底部
        QTimer.singleShot(100, self._scroll_to_bottom)

        # 保存到历史
        self._save_conversation_history()

    def show_typing_indicator(self, avatar: str = "🤖"):
        """显示打字指示器"""
        if self.typing_indicator:
            return

        self.typing_indicator = TypingIndicatorWidget(avatar)
        self.content_layout.insertWidget(self.content_layout.count() - 1, self.typing_indicator)
        QTimer.singleShot(100, self._scroll_to_bottom)

    def hide_typing_indicator(self):
        """隐藏打字指示器"""
        if self.typing_indicator:
            self.typing_indicator.stop_animation()
            self.content_layout.removeWidget(self.typing_indicator)
            self.typing_indicator.deleteLater()
            self.typing_indicator = None

    def clear_history(self):
        """清空历史"""
        self.messages.clear()

        # 清空布局
        while self.content_layout.count() > 1:  # 保留最后的伸缩空间
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 隐藏打字指示器
        if self.typing_indicator:
            self.hide_typing_indicator()

        # 保存空历史
        self._save_conversation_history()

    def get_messages(self) -> List[ChatMessage]:
        """获取所有消息"""
        return self.messages.copy()

    def _scroll_to_bottom(self):
        """滚动到底部"""
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _get_history_file_path(self) -> str:
        """获取历史文件路径"""
        # 使用应用程序目录而不是QSettings目录
        app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        history_dir = os.path.join(app_dir, "data")
        os.makedirs(history_dir, exist_ok=True)
        return os.path.join(history_dir, "chat_history.json")

    def _save_conversation_history(self):
        """保存对话历史"""
        try:
            history_data = {
                "messages": [msg.to_dict() for msg in self.messages],
                "last_updated": datetime.now().isoformat()
            }

            file_path = self._get_history_file_path()
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"保存聊天历史失败: {e}")

    def _load_conversation_history(self):
        """加载对话历史"""
        try:
            file_path = self._get_history_file_path()
            if not os.path.exists(file_path):
                return

            with open(file_path, 'r', encoding='utf-8') as f:
                history_data = json.load(f)

            messages_data = history_data.get("messages", [])
            for msg_data in messages_data:
                message = ChatMessage.from_dict(msg_data)
                self.add_message(message)

        except Exception as e:
            print(f"加载聊天历史失败: {e}")


class ChatInputWidget(QWidget):
    """聊天输入组件"""

    message_sent = pyqtSignal(str)  # 消息发送信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """设置UI"""
        self.setFixedHeight(70)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-top: 1px solid #e9ecef;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # 输入框
        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText("Type your message...")
        self.input_edit.setMaximumHeight(46)
        self.input_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.input_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                background-color: #f8f9fa;
                font-family: 'Segoe UI', -apple-system, sans-serif;
                font-size: 13px;
                padding: 10px 14px;
                color: #2d3748;
                selection-background-color: #667eea;
            }
            QTextEdit:focus {
                border-color: #667eea;
                background-color: #ffffff;
            }
            QTextEdit::placeholder {
                color: #a0aec0;
            }
        """)
        self.input_edit.textChanged.connect(self._on_text_changed)
        self.input_edit.installEventFilter(self)  # 安装事件过滤器
        layout.addWidget(self.input_edit)

        # 发送按钮
        self.send_button = QPushButton("📤")
        self.send_button.setToolTip("Send message (Enter)")
        self.send_button.setFixedSize(44, 44)
        self.send_button.setEnabled(False)
        self.send_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5a67d8, stop:1 #6b46c1);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4c51bf, stop:1 #553c9a);
            }
            QPushButton:disabled {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #cbd5e0, stop:1 #a0aec0);
                color: #718096;
            }
        """)
        self.send_button.clicked.connect(self._on_send_clicked)
        layout.addWidget(self.send_button)

    def eventFilter(self, obj, event):
        """事件过滤器 - 处理键盘事件"""
        if obj == self.input_edit and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                # Return键发送消息，Shift+Return换行
                self._on_send_clicked()
                return True
        return super().eventFilter(obj, event)

    def _on_text_changed(self):
        """文本变化处理"""
        has_text = bool(self.input_edit.toPlainText().strip())
        self.send_button.setEnabled(has_text)

    def _on_send_clicked(self):
        """发送按钮点击"""
        message = self.input_edit.toPlainText().strip()
        if message:
            self.message_sent.emit(message)
            self.input_edit.clear()

    def clear(self):
        """清空输入"""
        self.input_edit.clear()

    def set_focus(self):
        """设置焦点"""
        self.input_edit.setFocus()