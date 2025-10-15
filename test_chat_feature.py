"""
快速测试新增的AI聊天功能
"""

import sys
import asyncio
from pathlib import Path

# 添加src到路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from pymd_editor.ai_framework import AIManager, AIRequest, TaskType
from PyQt6.QtWidgets import QApplication


def test_chat_functionality():
    """测试聊天功能"""
    print("🧪 Testing AI Chat functionality...")
    
    app = QApplication(sys.argv)
    ai_manager = AIManager()
    
    # 模拟聊天请求
    def on_response(response_obj):
        if response_obj.success:
            print(f"✅ Chat Response: {response_obj.content[:100]}...")
        else:
            print(f"❌ Chat Error: {response_obj.error_message}")
        app.quit()
    
    def on_status(status):
        print(f"🔄 Status: {status}")
    
    ai_manager.response_received.connect(on_response)
    ai_manager.status_changed.connect(on_status)
    
    # 发送聊天消息
    chat_context = {"is_chat": True, "action": "chat"}
    ai_manager.process_request("chat", "Hello! Can you help me write better?", chat_context)
    
    app.exec()
    print("✅ Chat test completed!")


if __name__ == "__main__":
    test_chat_functionality()