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
        self.content_label = None
        self._setup_ui()

    def _setup_ui(self):
        """设置气泡UI"""
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setStyleSheet("ChatBubbleWidget { background: transparent; }")

        is_user = self.message.message_type == MessageType.USER

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 4, 8, 4)
        main_layout.setSpacing(0)

        if is_user:
            main_layout.addStretch(1)
            self._create_message_column(main_layout, is_user)
        else:
            self._create_message_column(main_layout, is_user)
            main_layout.addStretch(1)

    def _create_message_column(self, layout: QHBoxLayout, is_user: bool):
        """创建消息列（气泡 + 时间戳）"""
        col = QWidget()
        col.setMaximumWidth(320)
        col_layout = QVBoxLayout(col)
        col_layout.setContentsMargins(0, 0, 0, 0)
        col_layout.setSpacing(3)

        self.content_label = QLabel(self.message.content or "")
        self.content_label.setWordWrap(True)
        self.content_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.content_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.content_label.setContentsMargins(0, 0, 0, 0)

        if is_user:
            self.content_label.setStyleSheet("""
                QLabel {
                    background-color: #e8f0fe;
                    border: 1px solid #d7e3fc;
                    border-radius: 8px;
                    color: #1f2937;
                    font-size: 13px;
                    line-height: 1.5;
                    padding: 9px 13px;
                }
            """)
        else:
            self.content_label.setStyleSheet("""
                QLabel {
                    background-color: #ffffff;
                    border: 1px solid #d1d5db;
                    border-radius: 8px;
                    color: #1f2937;
                    font-size: 13px;
                    line-height: 1.5;
                    padding: 9px 13px;
                }
            """)

        col_layout.addWidget(self.content_label)

        # 时间戳
        ts_label = QLabel(self._format_timestamp())
        ts_label.setStyleSheet("color: #9ca3af; font-size: 10px; padding: 0 2px;")
        ts_label.setAlignment(
            Qt.AlignmentFlag.AlignRight if is_user else Qt.AlignmentFlag.AlignLeft
        )
        col_layout.addWidget(ts_label)

        layout.addWidget(col)

    def update_content(self, new_text: str):
        """更新气泡的文本内容（用于流式追加/覆盖）"""
        try:
            self.message.content = new_text
            if self.content_label is not None:
                self.content_label.setText(new_text)
        except Exception:
            pass

    def _format_timestamp(self) -> str:
        """格式化时间戳"""
        now = datetime.now()
        if self.message.timestamp.date() == now.date():
            return self.message.timestamp.strftime("%H:%M")
        elif self.message.timestamp.year == now.year:
            return self.message.timestamp.strftime("%m-%d %H:%M")
        else:
            return self.message.timestamp.strftime("%Y-%m-%d %H:%M")


class TypingIndicatorWidget(QWidget):
    """打字指示器组件"""

    def __init__(self, avatar: str = "🤖", parent=None):
        super().__init__(parent)
        self.avatar = avatar
        self.dots = []
        self._timer = None
        self._tick = 0
        self._setup_ui()
        self._start_animation()

    def _setup_ui(self):
        """设置UI"""
        self.setFixedHeight(46)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setStyleSheet("TypingIndicatorWidget { background: transparent; }")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(0)

        bubble = QFrame()
        bubble.setFrameStyle(QFrame.Shape.NoFrame)
        bubble.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 8px;
            }
        """)
        bubble_layout = QHBoxLayout(bubble)
        bubble_layout.setContentsMargins(12, 8, 12, 8)
        bubble_layout.setSpacing(6)

        typing_label = QLabel("Thinking")
        typing_label.setStyleSheet("color: #6b7280; font-size: 12px; background: transparent;")
        bubble_layout.addWidget(typing_label)

        for _ in range(3):
            dot = QLabel("●")
            dot.setStyleSheet("QLabel { color: #9ca3af; font-size: 10px; background: transparent; }")
            self.dots.append(dot)
            bubble_layout.addWidget(dot)

        layout.addWidget(bubble)
        layout.addStretch()

    def _start_animation(self):
        """启动波浪点动画（单一定时器）"""
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick_wave)
        self._timer.start(320)

    def _tick_wave(self):
        """每帧更新一个活跃点的颜色"""
        self._tick += 1
        active = self._tick % 3
        for i, dot in enumerate(self.dots):
            color = "#4b5563" if i == active else "#d1d5db"
            dot.setStyleSheet(
                f"QLabel {{ color: {color}; font-size: 10px; background: transparent; }}"
            )

    def stop_animation(self):
        """停止动画"""
        if self._timer:
            self._timer.stop()
            self._timer = None

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
                background-color: #ffffff;
            }
            QScrollBar:vertical {
                width: 5px;
                background-color: transparent;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #d1d5db;
                border-radius: 2px;
                min-height: 24px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #9ca3af;
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
        self.content_widget.setStyleSheet("QWidget { background-color: transparent; }")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(6, 10, 6, 10)
        self.content_layout.setSpacing(6)
        self.content_layout.addStretch()

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

    def update_last_message_append(self, chunk: str):
        """将流式片段追加到最后一条消息（如果最后一条是 AI 消息）。"""
        try:
            if not self.messages:
                return
            last = self.messages[-1]
            if last.message_type != MessageType.AI:
                return
            # 累加文本
            last.content = (last.content or "") + chunk

            # 更新最后一个气泡组件的显示
            # 最后一个 widget 在 content_layout 中靠近末尾（倒数第二个）
            idx = self.content_layout.count() - 2
            if idx >= 0:
                item = self.content_layout.itemAt(idx)
                if item and item.widget():
                    widget = item.widget()
                    if hasattr(widget, 'update_content'):
                        widget.update_content(last.content)

            # 保存历史
            self._save_conversation_history()
        except Exception:
            pass

        self.message_added.emit(last)

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
        self.setFixedHeight(68)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setStyleSheet("""
            ChatInputWidget {
                background-color: #ffffff;
                border-top: 1px solid #d1d5db;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(8)

        # 输入框
        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText("Ask AI anything...")
        self.input_edit.setMaximumHeight(50)
        self.input_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.input_edit.setStyleSheet("""
            QTextEdit {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                background-color: #ffffff;
                font-size: 13px;
                padding: 6px 10px;
                color: #111827;
                selection-background-color: #c7d2fe;
            }
            QTextEdit:focus {
                border-color: #9ca3af;
            }
        """)
        self.input_edit.textChanged.connect(self._on_text_changed)
        self.input_edit.installEventFilter(self)
        layout.addWidget(self.input_edit)

        self.send_button = QPushButton("Send")
        self.send_button.setToolTip("Send (Enter)")
        self.send_button.setFixedSize(56, 36)
        self.send_button.setEnabled(False)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
            QPushButton:pressed {
                background-color: #d1d5db;
            }
            QPushButton:disabled {
                background-color: #f9fafb;
                color: #9ca3af;
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