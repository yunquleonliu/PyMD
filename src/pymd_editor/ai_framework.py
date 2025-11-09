"""
AI服务集成框架
提供统一的AI调用接口和智能路由功能
"""

import asyncio
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum

import httpx
from PyQt6.QtCore import QObject, pyqtSignal, QThread, QTimer


class AIProvider(Enum):
    """AI服务提供商枚举"""
    PERSONAL_AI = "personal_ai"
    GEMINI = "gemini"


class TaskType(Enum):
    """任务类型枚举"""
    IMPROVE_TEXT = "improve_text"
    SUMMARIZE = "summarize"
    TRANSLATE = "translate"
    BRAINSTORM = "brainstorm"
    GRAMMAR_CHECK = "grammar_check"
    GENERATE_CONTENT = "generate_content"


@dataclass
class AIRequest:
    """AI请求数据结构"""
    task_type: TaskType
    content: str
    context: Dict[str, Any] = None
    user_preferences: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}
        if self.user_preferences is None:
            self.user_preferences = {}
    
    
@dataclass 
class AIResponse:
    """AI响应数据结构"""
    success: bool
    content: str
    provider: AIProvider
    cost: float
    processing_time: float
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseAIProvider(ABC):
    """AI服务提供商抽象基类"""
    
    def __init__(self):
        self.name = ""
        self.base_url = ""
        self.api_key = ""
        self.cost_per_request = 0.0
        self.capabilities = []
        
    @abstractmethod
    async def generate(self, request: AIRequest) -> AIResponse:
        """生成AI响应"""
        pass
    
    @abstractmethod
    def get_cost_estimate(self, request: AIRequest) -> float:
        """估算调用成本"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查服务是否可用"""
        pass
    
    @abstractmethod
    def supports_task(self, task_type: TaskType) -> bool:
        """检查是否支持特定任务类型"""
        pass


class PersonalAIProvider(BaseAIProvider):
    """个人AI服务提供商 - https://dataflowxx.dpdns.org"""
    
    def __init__(self, base_url: str = "https://dataflowxx.dpdns.org"):
        super().__init__()
        self.name = "Personal AI"
        self.base_url = base_url
        self.cost_per_request = 0.0  # 完全免费
        self.capabilities = [
            TaskType.IMPROVE_TEXT,
            TaskType.SUMMARIZE,
            TaskType.TRANSLATE,
            TaskType.BRAINSTORM,
            TaskType.GRAMMAR_CHECK,
            TaskType.GENERATE_CONTENT
        ]
        
    async def generate(self, request: AIRequest) -> AIResponse:
        """调用Personal AI服务"""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # 构造提示词
            prompt = self._build_prompt(request)
            
            # 调用API (跳过SSL验证用于测试)
            async with httpx.AsyncClient(timeout=30.0, verify=False) as client:
                # 根据Personal AI的API格式调整
                payload = {
                    "messages": [{"role": "user", "content": prompt}],
                    "conversation_id": request.context.get("conversation_id"),
                    "stream": False
                }
                
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "PyMD-Editor/2.0"
                    }
                )
                
                response.raise_for_status()
                data = response.json()
                
                # 解析OpenAI格式响应
                content = ""
                if "choices" in data and data["choices"]:
                    choice = data["choices"][0]
                    if "message" in choice and "content" in choice["message"]:
                        content = choice["message"]["content"]
                
                processing_time = asyncio.get_event_loop().time() - start_time
                
                return AIResponse(
                    success=True,
                    content=content,
                    provider=AIProvider.PERSONAL_AI,
                    cost=0.0,
                    processing_time=processing_time,
                    metadata={"tokens_used": len(content.split())}
                )
                
        except Exception as e:
            processing_time = asyncio.get_event_loop().time() - start_time
            return AIResponse(
                success=False,
                content="",
                provider=AIProvider.PERSONAL_AI,
                cost=0.0,
                processing_time=processing_time,
                error_message=str(e)
            )
    
    def _build_prompt(self, request: AIRequest) -> str:
        """构建适合Personal AI的提示词"""
        # 如果是聊天请求，直接返回用户消息
        if request.context.get('is_chat'):
            return request.content
            
        prompts = {
            TaskType.IMPROVE_TEXT: f"请优化以下文本，使其更加清晰、准确和专业：\n\n{request.content}",
            TaskType.SUMMARIZE: f"请总结以下内容的要点：\n\n{request.content}",
            TaskType.TRANSLATE: f"请将以下文本翻译成{request.context.get('target_language', '英语')}：\n\n{request.content}",
            TaskType.BRAINSTORM: f"基于以下主题，请生成5个创意想法：\n\n{request.content}",
            TaskType.GRAMMAR_CHECK: f"请检查以下文本的语法错误并提供修正建议：\n\n{request.content}",
            TaskType.GENERATE_CONTENT: f"请根据以下要求生成内容：\n\n{request.content}"
        }
        
        return prompts.get(request.task_type, request.content)
    
    def get_cost_estimate(self, request: AIRequest) -> float:
        return 0.0  # 免费服务
    
    def is_available(self) -> bool:
        """简单的可用性检查"""
        try:
            import httpx
            return True
        except ImportError:
            return False
    
    def supports_task(self, task_type: TaskType) -> bool:
        return task_type in self.capabilities


class GeminiProvider(BaseAIProvider):
    """Google Gemini API提供商"""
    
    def __init__(self, api_key: str = "", model: str = "gemini-1.5-flash"):
        super().__init__()
        self.name = "Google Gemini"
        self.base_url = "https://generativelanguage.googleapis.com"
        self.api_key = api_key
        self.model = model
        self.cost_per_1k_tokens = 0.002  # 示例价格
        self.capabilities = [
            TaskType.IMPROVE_TEXT,
            TaskType.SUMMARIZE,
            TaskType.TRANSLATE,
            TaskType.BRAINSTORM,
            TaskType.GRAMMAR_CHECK,
            TaskType.GENERATE_CONTENT
        ]
        
    async def generate(self, request: AIRequest) -> AIResponse:
        """调用Gemini API"""
        start_time = asyncio.get_event_loop().time()
        
        if not self.api_key:
            return AIResponse(
                success=False,
                content="",
                provider=AIProvider.GEMINI,
                cost=0.0,
                processing_time=0.0,
                error_message="Gemini API key not configured"
            )
        
        try:
            prompt = self._build_prompt(request)
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": prompt
                        }]
                    }],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 2048,
                    }
                }
                
                response = await client.post(
                    f"{self.base_url}/v1beta/models/{self.model}:generateContent",
                    json=payload,
                    params={"key": self.api_key},
                    headers={"Content-Type": "application/json"}
                )
                
                response.raise_for_status()
                data = response.json()
                
                # 解析Gemini响应
                content = ""
                if "candidates" in data and data["candidates"]:
                    candidate = data["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        content = candidate["content"]["parts"][0].get("text", "")
                
                # 估算成本
                estimated_tokens = len(prompt.split()) + len(content.split())
                cost = estimated_tokens * self.cost_per_1k_tokens / 1000
                
                processing_time = asyncio.get_event_loop().time() - start_time
                
                return AIResponse(
                    success=True,
                    content=content,
                    provider=AIProvider.GEMINI,
                    cost=cost,
                    processing_time=processing_time,
                    metadata={
                        "model": self.model,
                        "estimated_tokens": estimated_tokens
                    }
                )
                
        except Exception as e:
            processing_time = asyncio.get_event_loop().time() - start_time
            return AIResponse(
                success=False,
                content="",
                provider=AIProvider.GEMINI,
                cost=0.0,
                processing_time=processing_time,
                error_message=str(e)
            )
    
    def _build_prompt(self, request: AIRequest) -> str:
        """构建适合Gemini的提示词"""
        prompts = {
            TaskType.IMPROVE_TEXT: f"Improve the following text for clarity, accuracy, and professionalism:\n\n{request.content}",
            TaskType.SUMMARIZE: f"Summarize the key points of the following content:\n\n{request.content}",
            TaskType.TRANSLATE: f"Translate the following text to {request.context.get('target_language', 'English')}:\n\n{request.content}",
            TaskType.BRAINSTORM: f"Generate 5 creative ideas based on the following topic:\n\n{request.content}",
            TaskType.GRAMMAR_CHECK: f"Check the following text for grammar errors and provide corrections:\n\n{request.content}",
            TaskType.GENERATE_CONTENT: f"Generate content based on the following requirements:\n\n{request.content}"
        }
        
        return prompts.get(request.task_type, request.content)
    
    def get_cost_estimate(self, request: AIRequest) -> float:
        estimated_tokens = len(request.content.split()) * 2  # 估算输入+输出tokens
        return estimated_tokens * self.cost_per_1k_tokens / 1000
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def supports_task(self, task_type: TaskType) -> bool:
        return task_type in self.capabilities


class AIRouter:
    """AI服务智能路由器"""
    
    def __init__(self):
        self.providers: Dict[AIProvider, BaseAIProvider] = {}
        self.user_preferences = {
            "prefer_free": True,
            "max_cost_per_request": 0.01,
            "timeout": 30.0
        }
        
    def register_provider(self, provider: BaseAIProvider, provider_type: AIProvider):
        """注册AI服务提供商"""
        self.providers[provider_type] = provider
        
    def route_request(self, request: AIRequest) -> AIProvider:
        """智能选择最适合的AI服务"""
        
        # 1. 过滤支持该任务的提供商
        suitable_providers = [
            (provider_type, provider) 
            for provider_type, provider in self.providers.items()
            if provider.supports_task(request.task_type) and provider.is_available()
        ]
        
        if not suitable_providers:
            raise ValueError("No suitable AI provider available for this task")
        
        # 2. 根据用户偏好和任务复杂度选择
        if self.user_preferences.get("prefer_free", True):
            # 优先使用免费服务
            for provider_type, provider in suitable_providers:
                if provider.get_cost_estimate(request) == 0.0:
                    return provider_type
        
        # 3. 复杂任务选择高级服务
        if self._is_complex_task(request):
            # 选择最强大的服务（通常是付费的）
            premium_providers = [
                (provider_type, provider)
                for provider_type, provider in suitable_providers
                if provider_type == AIProvider.GEMINI
            ]
            if premium_providers:
                return premium_providers[0][0]
        
        # 4. 默认选择第一个可用的服务
        return suitable_providers[0][0]
    
    def _is_complex_task(self, request: AIRequest) -> bool:
        """判断是否为复杂任务"""
        complex_indicators = [
            len(request.content) > 1000,  # 长文本
            request.task_type in [TaskType.GENERATE_CONTENT],  # 复杂任务类型
            "detailed" in request.context.get("requirements", "").lower(),
            "analysis" in request.context.get("requirements", "").lower()
        ]
        
        return any(complex_indicators)
    
    def set_user_preferences(self, preferences: Dict[str, Any]):
        """设置用户偏好"""
        self.user_preferences.update(preferences)


class AIWorker(QThread):
    """AI异步工作线程"""
    
    # 信号
    response_ready = pyqtSignal(AIResponse)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, provider: BaseAIProvider, request: AIRequest):
        super().__init__()
        self.provider = provider
        self.request = request
        
    def run(self):
        """运行AI请求"""
        try:
            # 创建新的事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # 执行异步调用
            response = loop.run_until_complete(
                self.provider.generate(self.request)
            )
            
            # 发出信号
            self.response_ready.emit(response)
            
        except Exception as e:
            self.error_occurred.emit(str(e))
        
        finally:
            loop.close()


class AIManager(QObject):
    """AI服务管理器（主要接口） - 集成新的提供商管理系统"""

    # 信号
    response_received = pyqtSignal(AIResponse)
    status_changed = pyqtSignal(str)

    def __init__(self, provider_manager=None):
        super().__init__()
        from .ai_settings import get_ai_manager
        self.provider_manager = provider_manager or get_ai_manager()
        self.router = AIRouter()
        self.current_worker = None
        self._setup_providers()

    def _setup_providers(self):
        """初始化AI服务提供商 - 使用新的提供商管理系统"""
        # 从提供商管理器获取当前启用的提供商
        enabled_configs = self.provider_manager.get_enabled_providers()

        for config in enabled_configs:
            if config.provider_type.value == "personal_ai":
                provider = PersonalAIProvider(
                    base_url=config.base_url
                )
                self.router.register_provider(provider, AIProvider.PERSONAL_AI)
            elif config.provider_type.value == "gemini":
                provider = GeminiProvider(
                    api_key=config.api_key,
                    model=config.model
                )
                self.router.register_provider(provider, AIProvider.GEMINI)
            # 可以在这里添加更多提供商类型
        
    def configure_gemini(self, api_key: str):
        """配置Gemini API密钥"""
        if AIProvider.GEMINI in self.router.providers:
            self.router.providers[AIProvider.GEMINI].api_key = api_key
            
    def request_ai(self, task_type: TaskType, content: str, context: Dict = None, user_prefs: Dict = None):
        """发送AI请求"""
        if self.current_worker and self.current_worker.isRunning():
            self.status_changed.emit("Previous request still processing...")
            return
        
        # 构建请求
        request = AIRequest(
            task_type=task_type,
            content=content,
            context=context or {},
            user_preferences=user_prefs or {}
        )
        
        try:
            # 使用当前选择的提供商，而不是自动路由
            current_config = self.provider_manager.get_current_provider()
            if not current_config:
                raise ValueError("No AI provider selected")

            # 根据配置创建提供商实例
            if current_config.provider_type.value == "personal_ai":
                provider = PersonalAIProvider(base_url=current_config.base_url)
                provider_type = AIProvider.PERSONAL_AI
            elif current_config.provider_type.value == "gemini":
                provider = GeminiProvider(
                    api_key=current_config.api_key,
                    model=current_config.model
                )
                provider_type = AIProvider.GEMINI
            else:
                raise ValueError(f"Unsupported provider type: {current_config.provider_type.value}")

            # 检查提供商是否可用
            if not provider.is_available():
                raise ValueError(f"Provider {current_config.name} is not available. Please check configuration.")

            # 检查是否支持任务
            if not provider.supports_task(request.task_type):
                raise ValueError(f"Provider {current_config.name} does not support this task type")

            # 创建工作线程
            self.current_worker = AIWorker(provider, request)
            self.current_worker.response_ready.connect(self._on_response_ready)
            self.current_worker.error_occurred.connect(self._on_error_occurred)
            self.current_worker.finished.connect(self._on_worker_finished)

            # 启动异步请求
            self.status_changed.emit(f"Requesting {current_config.name}...")
            self.current_worker.start()
            
        except Exception as e:
            self.status_changed.emit(f"Error: {str(e)}")
    
    def _on_response_ready(self, response: AIResponse):
        """处理AI响应"""
        self.response_received.emit(response)
        
        if response.success:
            provider_name = response.provider.value.replace("_", " ").title()
            self.status_changed.emit(f"Response from {provider_name} (${response.cost:.4f})")
        else:
            self.status_changed.emit(f"Error: {response.error_message}")
    
    def _on_error_occurred(self, error_message: str):
        """处理错误"""
        self.status_changed.emit(f"Error: {error_message}")
    
    def _on_worker_finished(self):
        """工作线程完成"""
        self.current_worker = None
        
    def is_busy(self) -> bool:
        """检查是否正在处理请求"""
        return self.current_worker is not None and self.current_worker.isRunning()
        
    def process_request(self, action: str, content: str, context: dict = None):
        """处理字符串格式的请求（兼容接口）"""
        # 映射字符串操作到TaskType
        task_mapping = {
            "improve": TaskType.IMPROVE_TEXT,
            "summarize": TaskType.SUMMARIZE,
            "translate": TaskType.TRANSLATE,
            "brainstorm": TaskType.BRAINSTORM,
            "grammar": TaskType.GRAMMAR_CHECK,
            "generate": TaskType.GENERATE_CONTENT,
            "chat": TaskType.GENERATE_CONTENT  # 聊天使用通用生成任务
        }
        
        task_type = task_mapping.get(action.lower(), TaskType.IMPROVE_TEXT)
        self.request_ai(task_type, content, context or {})