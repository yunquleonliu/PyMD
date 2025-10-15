"""
AI Settings and Provider Management
Similar to VSCode's AI provider system, allowing users to configure multiple AI services
"""

import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
from PyQt6.QtCore import QSettings, QObject, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QGroupBox, QFormLayout, QCheckBox,
    QMessageBox, QTabWidget, QTextEdit, QSpinBox, QDialog, QDialogButtonBox
)


class AIProviderType(Enum):
    """AI提供商类型"""
    PERSONAL_AI = "personal_ai"
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"
    CUSTOM = "custom"


@dataclass
class AIProviderConfig:
    """AI提供商配置"""
    provider_type: AIProviderType
    name: str
    api_key: str = ""
    base_url: str = ""
    model: str = ""
    max_tokens: int = 4096
    temperature: float = 0.7
    enabled: bool = True
    description: str = ""
    avatar_url: str = ""
    personality: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider_type": self.provider_type.value,
            "name": self.name,
            "api_key": self.api_key,
            "base_url": self.base_url,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "enabled": self.enabled,
            "description": self.description,
            "avatar_url": self.avatar_url,
            "personality": self.personality
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIProviderConfig':
        return cls(
            provider_type=AIProviderType(data.get("provider_type", "custom")),
            name=data.get("name", ""),
            api_key=data.get("api_key", ""),
            base_url=data.get("base_url", ""),
            model=data.get("model", ""),
            max_tokens=data.get("max_tokens", 4096),
            temperature=data.get("temperature", 0.7),
            enabled=data.get("enabled", True),
            description=data.get("description", ""),
            avatar_url=data.get("avatar_url", ""),
            personality=data.get("personality", "")
        )


class AIProviderManager(QObject):
    """AI提供商管理器"""

    providers_changed = pyqtSignal()  # 提供商列表改变信号
    current_provider_changed = pyqtSignal(str)  # 当前提供商改变信号

    def __init__(self):
        super().__init__()
        self.settings = QSettings()
        self.providers: Dict[str, AIProviderConfig] = {}
        self.current_provider_id: str = ""
        self._load_providers()

    def _load_providers(self):
        """加载提供商配置"""
        # 默认提供商
        default_providers = {
            "personal_ai": AIProviderConfig(
                provider_type=AIProviderType.PERSONAL_AI,
                name="Personal AI",
                base_url="https://dataflowxx.dpdns.org",
                description="免费的个人AI服务",
                personality="我是您的个人AI助手，可以帮助您处理文档和文本。",
                avatar_url="🤖"
            ),
            "gemini": AIProviderConfig(
                provider_type=AIProviderType.GEMINI,
                name="Google Gemini",
                base_url="https://generativelanguage.googleapis.com",
                model="gemini-pro",
                description="Google的Gemini AI模型",
                personality="我是Google Gemini，一个强大的AI助手。",
                avatar_url="🤖"
            )
        }

        # 从设置加载用户配置
        providers_data = self.settings.value("ai/providers", {})
        if isinstance(providers_data, str):
            try:
                providers_data = json.loads(providers_data)
            except:
                providers_data = {}

        # 合并默认和用户配置
        for provider_id, config_data in providers_data.items():
            if provider_id in default_providers:
                # 更新默认配置
                default_config = default_providers[provider_id]
                user_config = AIProviderConfig.from_dict(config_data)
                # 保留用户设置，但更新描述等
                updated_config = AIProviderConfig(
                    provider_type=user_config.provider_type,
                    name=user_config.name or default_config.name,
                    api_key=user_config.api_key,
                    base_url=user_config.base_url or default_config.base_url,
                    model=user_config.model or default_config.model,
                    max_tokens=user_config.max_tokens,
                    temperature=user_config.temperature,
                    enabled=user_config.enabled,
                    description=default_config.description,
                    avatar_url=default_config.avatar_url,
                    personality=default_config.personality
                )
                self.providers[provider_id] = updated_config
            else:
                self.providers[provider_id] = AIProviderConfig.from_dict(config_data)

        # 添加未配置的默认提供商
        for provider_id, config in default_providers.items():
            if provider_id not in self.providers:
                self.providers[provider_id] = config

        # 设置当前提供商
        current_id = self.settings.value("ai/current_provider", "personal_ai")
        if current_id in self.providers:
            self.current_provider_id = current_id
        else:
            self.current_provider_id = next(iter(self.providers.keys()))

    def save_providers(self):
        """保存提供商配置"""
        providers_data = {}
        for provider_id, config in self.providers.items():
            providers_data[provider_id] = config.to_dict()

        self.settings.setValue("ai/providers", json.dumps(providers_data))
        self.settings.setValue("ai/current_provider", self.current_provider_id)
        self.providers_changed.emit()

    def get_current_provider(self) -> Optional[AIProviderConfig]:
        """获取当前提供商"""
        return self.providers.get(self.current_provider_id)

    def set_current_provider(self, provider_id: str):
        """设置当前提供商"""
        if provider_id in self.providers:
            self.current_provider_id = provider_id
            self.settings.setValue("ai/current_provider", provider_id)
            self.current_provider_changed.emit(provider_id)

    def add_provider(self, config: AIProviderConfig) -> str:
        """添加新提供商"""
        provider_id = f"{config.provider_type.value}_{len(self.providers)}"
        self.providers[provider_id] = config
        self.save_providers()
        return provider_id

    def update_provider(self, provider_id: str, config: AIProviderConfig):
        """更新提供商"""
        if provider_id in self.providers:
            self.providers[provider_id] = config
            self.save_providers()

    def remove_provider(self, provider_id: str):
        """删除提供商"""
        if provider_id in self.providers and provider_id != self.current_provider_id:
            del self.providers[provider_id]
            self.save_providers()

    def get_enabled_providers(self) -> List[AIProviderConfig]:
        """获取启用的提供商"""
        return [config for config in self.providers.values() if config.enabled]

    def get_provider(self, provider_id: str) -> Optional[AIProviderConfig]:
        """获取指定提供商"""
        return self.providers.get(provider_id)


class AIProviderWidget(QWidget):
    """AI提供商配置Widget"""

    def __init__(self, provider_config: AIProviderConfig, parent=None):
        super().__init__(parent)
        self.provider_config = provider_config
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # 基本信息
        basic_group = QGroupBox("基本信息")
        basic_layout = QFormLayout()

        self.name_edit = QLineEdit(self.provider_config.name)
        basic_layout.addRow("名称:", self.name_edit)

        self.description_edit = QTextEdit(self.provider_config.description)
        self.description_edit.setMaximumHeight(60)
        basic_layout.addRow("描述:", self.description_edit)

        self.avatar_edit = QLineEdit(self.provider_config.avatar_url)
        basic_layout.addRow("头像:", self.avatar_edit)

        self.personality_edit = QTextEdit(self.provider_config.personality)
        self.personality_edit.setMaximumHeight(80)
        basic_layout.addRow("个性:", self.personality_edit)

        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)

        # API配置
        api_group = QGroupBox("API配置")
        api_layout = QFormLayout()

        self.api_key_edit = QLineEdit(self.provider_config.api_key)
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        api_layout.addRow("API Key:", self.api_key_edit)

        self.base_url_edit = QLineEdit(self.provider_config.base_url)
        api_layout.addRow("Base URL:", self.base_url_edit)

        self.model_edit = QLineEdit(self.provider_config.model)
        api_layout.addRow("Model:", self.model_edit)

        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(1, 32768)
        self.max_tokens_spin.setValue(self.provider_config.max_tokens)
        api_layout.addRow("Max Tokens:", self.max_tokens_spin)

        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        # 启用状态
        self.enabled_check = QCheckBox("启用此提供商")
        self.enabled_check.setChecked(self.provider_config.enabled)
        layout.addWidget(self.enabled_check)

        layout.addStretch()

    def get_config(self) -> AIProviderConfig:
        """获取当前配置"""
        return AIProviderConfig(
            provider_type=self.provider_config.provider_type,
            name=self.name_edit.text(),
            api_key=self.api_key_edit.text(),
            base_url=self.base_url_edit.text(),
            model=self.model_edit.text(),
            max_tokens=self.max_tokens_spin.value(),
            temperature=self.provider_config.temperature,
            enabled=self.enabled_check.isChecked(),
            description=self.description_edit.toPlainText(),
            avatar_url=self.avatar_edit.text(),
            personality=self.personality_edit.toPlainText()
        )


class AISettingsDialog(QDialog):
    """AI设置对话框"""

    settings_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.provider_manager = AIProviderManager()
        self.provider_manager.providers_changed.connect(self._refresh_provider_list)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.setWindowTitle("AI 设置")
        self.resize(600, 500)

        # 当前提供商选择
        current_group = QGroupBox("当前AI提供商")
        current_layout = QHBoxLayout()

        current_layout.addWidget(QLabel("选择AI提供商:"))
        self.provider_combo = QComboBox()
        self._refresh_provider_combo()
        self.provider_combo.currentTextChanged.connect(self._on_current_provider_changed)
        current_layout.addWidget(self.provider_combo)

        current_group.setLayout(current_layout)
        layout.addWidget(current_group)

        # 提供商管理
        tab_widget = QTabWidget()

        # 现有提供商
        self.existing_tab = QWidget()
        existing_layout = QVBoxLayout(self.existing_tab)

        self.provider_list_combo = QComboBox()
        self.provider_widget = None  # Initialize before refresh
        existing_layout.addWidget(QLabel("选择要编辑的提供商:"))
        existing_layout.addWidget(self.provider_list_combo)

        self.provider_list_combo.currentTextChanged.connect(self._on_provider_selected)

        existing_layout.addWidget(QLabel("配置:"))
        self.config_container = QWidget()  # Initialize before refresh
        existing_layout.addWidget(self.config_container)

        self._refresh_provider_list()  # Call after UI elements are created

        # 保存按钮
        save_btn = QPushButton("保存更改")
        save_btn.clicked.connect(self._save_provider_config)
        existing_layout.addWidget(save_btn)

        tab_widget.addTab(self.existing_tab, "现有提供商")

        # 添加新提供商
        self.new_tab = QWidget()
        new_layout = QVBoxLayout(self.new_tab)

        new_layout.addWidget(QLabel("添加新的AI提供商:"))

        provider_type_combo = QComboBox()
        for provider_type in AIProviderType:
            provider_type_combo.addItem(provider_type.value)
        new_layout.addWidget(QLabel("提供商类型:"))
        new_layout.addWidget(provider_type_combo)

        add_btn = QPushButton("添加提供商")
        add_btn.clicked.connect(lambda: self._add_new_provider(provider_type_combo.currentText()))
        new_layout.addWidget(add_btn)

        new_layout.addStretch()
        tab_widget.addTab(self.new_tab, "添加新提供商")

        layout.addWidget(tab_widget)

        # 底部按钮 - 使用标准对话框按钮
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def _refresh_provider_combo(self):
        """刷新当前提供商下拉框"""
        self.provider_combo.clear()
        for provider_id, config in self.provider_manager.providers.items():
            if config.enabled:
                display_name = f"{config.name} ({config.provider_type.value})"
                self.provider_combo.addItem(display_name, provider_id)

        # 设置当前选择
        current_provider = self.provider_manager.get_current_provider()
        if current_provider:
            for i in range(self.provider_combo.count()):
                if self.provider_combo.itemData(i) == self.provider_manager.current_provider_id:
                    self.provider_combo.setCurrentIndex(i)
                    break

    def _refresh_provider_list(self):
        """刷新提供商列表"""
        self.provider_list_combo.clear()
        for provider_id, config in self.provider_manager.providers.items():
            display_name = f"{config.name} ({config.provider_type.value})"
            self.provider_list_combo.addItem(display_name, provider_id)

        # 自动选择第一个
        if self.provider_list_combo.count() > 0:
            self.provider_list_combo.setCurrentIndex(0)
            self._on_provider_selected(self.provider_list_combo.currentText())

    def _on_current_provider_changed(self, text: str):
        """当前提供商改变"""
        provider_id = self.provider_combo.currentData()
        if provider_id:
            self.provider_manager.set_current_provider(provider_id)
            self.settings_changed.emit()

    def _on_provider_selected(self, text: str):
        """选择要编辑的提供商"""
        provider_id = self.provider_list_combo.currentData()
        if provider_id:
            config = self.provider_manager.get_provider(provider_id)
            if config:
                # 移除旧的widget
                if self.provider_widget:
                    self.config_container.layout().removeWidget(self.provider_widget)
                    self.provider_widget.deleteLater()

                # 添加新的widget
                self.provider_widget = AIProviderWidget(config)
                if self.config_container.layout() is None:
                    self.config_container.setLayout(QVBoxLayout())
                self.config_container.layout().addWidget(self.provider_widget)

    def _save_provider_config(self):
        """保存提供商配置"""
        if self.provider_widget and self.provider_list_combo.currentData():
            provider_id = self.provider_list_combo.currentData()
            new_config = self.provider_widget.get_config()
            self.provider_manager.update_provider(provider_id, new_config)
            QMessageBox.information(self, "成功", "AI提供商配置已保存！")
            self.settings_changed.emit()

    def _add_new_provider(self, provider_type_str: str):
        """添加新提供商"""
        try:
            provider_type = AIProviderType(provider_type_str)
            config = AIProviderConfig(
                provider_type=provider_type,
                name=f"New {provider_type.value.title()} Provider",
                description=f"A new {provider_type.value} AI provider"
            )
            provider_id = self.provider_manager.add_provider(config)
            self._refresh_provider_list()
            self._refresh_provider_combo()

            # 切换到现有提供商标签页
            QMessageBox.information(self, "成功", f"新提供商已添加！请在'现有提供商'标签页中配置。")
            self.settings_changed.emit()

        except Exception as e:
            QMessageBox.warning(self, "错误", f"添加提供商失败: {str(e)}")


# 全局AI管理器实例
_ai_manager_instance = None

def get_ai_manager() -> AIProviderManager:
    """获取全局AI管理器实例"""
    global _ai_manager_instance
    if _ai_manager_instance is None:
        _ai_manager_instance = AIProviderManager()
    return _ai_manager_instance