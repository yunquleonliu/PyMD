"""
AI集成测试脚本
测试Personal AI和智能路由功能
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加src到路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from pymd_editor.ai_framework import AIManager, AIRequest, PersonalAIProvider
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject


class TestAI:
    """AI功能测试类"""
    
    def __init__(self):
        # 创建Qt应用（AI管理器需要事件循环）
        self.app = QApplication(sys.argv)
        
        # 创建AI管理器
        self.ai_manager = AIManager()
        
        # 连接信号
        self.ai_manager.response_received.connect(self.on_response_obj)
        self.ai_manager.status_changed.connect(self.on_status)
        
        self.response_received = False
        self.last_response = ""
        self.last_error = ""
        
    def on_response_obj(self, response_obj):
        """响应处理"""
        if response_obj.success:
            print(f"\n✅ AI Response received:")
            print(f"📝 {response_obj.content}")
            self.last_response = response_obj.content
        else:
            print(f"\n❌ AI Error: {response_obj.error_message}")
            self.last_error = response_obj.error_message
        self.response_received = True
        self.app.quit()
        
    def on_status(self, status: str):
        """状态更新处理"""
        print(f"🔄 Status: {status}")
        
    def test_personal_ai(self):
        """测试Personal AI"""
        print("🚀 Testing Personal AI Integration...")
        print(f"🌐 API Endpoint: https://dataflowxx.dpdns.org/")
        
        # 创建测试请求
        test_content = "Hello, this is a test message. Please respond with a simple greeting."
        context = {
            "action": "test",
            "timestamp": "2024-01-01 12:00:00",
            "content_length": len(test_content)
        }
        
        # 发送请求
        print(f"📤 Sending request: {test_content[:50]}...")
        self.ai_manager.process_request("improve", test_content, context)
        
        # 启动事件循环
        self.app.exec()
        
        return self.response_received, self.last_response, self.last_error
        
    async def test_direct_api(self):
        """直接测试API连接"""
        print("\n🔍 Testing direct API connection...")
        
        provider = PersonalAIProvider()
        
        from pymd_editor.ai_framework import TaskType
        
        request = AIRequest(
            task_type=TaskType.IMPROVE_TEXT,
            content="Hello world, please improve this text.",
            context={"test": True}
        )
        
        try:
            response = await provider.generate(request)
            print(f"✅ Direct API Success: {response.content[:100]}...")
            return True, response.content
        except Exception as e:
            print(f"❌ Direct API Error: {str(e)}")
            return False, str(e)


def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 PyMD Editor AI Integration Test")
    print("=" * 60)
    
    # 测试1: Qt集成测试
    print("\n1️⃣ Testing Qt AI Manager Integration...")
    tester = TestAI()
    success, response, error = tester.test_personal_ai()
    
    if success and response:
        print(f"✅ Qt Integration: SUCCESS")
    else:
        print(f"❌ Qt Integration: FAILED - {error}")
    
    # 测试2: 直接API测试
    print("\n2️⃣ Testing Direct API Connection...")
    async def run_direct_test():
        tester = TestAI()
        return await tester.test_direct_api()
    
    # 运行异步测试
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        success, result = loop.run_until_complete(run_direct_test())
        if success:
            print(f"✅ Direct API: SUCCESS")
        else:
            print(f"❌ Direct API: FAILED - {result}")
    finally:
        loop.close()
    
    print("\n" + "=" * 60)
    print("🏁 Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()