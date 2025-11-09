#!/usr/bin/env python3
"""
AI Provider Router Demo
演示新的AI提供商路由系统功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication
from pymd_editor.ai_settings import AISettingsDialog

def main():
    """演示AI设置对话框"""
    app = QApplication(sys.argv)

    # 创建AI设置对话框
    settings_dialog = AISettingsDialog()
    settings_dialog.setWindowTitle("PyMD AI Provider Settings Demo")

    print("=== PyMD AI Provider Router Demo ===")
    print("这个对话框允许用户：")
    print("1. 选择当前使用的AI提供商")
    print("2. 配置Personal AI (免费)")
    print("3. 配置Gemini API (需要API密钥)")
    print("4. 添加新的AI提供商")
    print("5. 设置AI个性特征")
    print()

    # 显示对话框
    result = settings_dialog.exec()

    if result:
        print("设置已保存！")
    else:
        print("设置已取消")

    print("\nDemo completed!")

if __name__ == "__main__":
    main()