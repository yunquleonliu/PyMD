#!/usr/bin/env python3
"""
PyMD Editor WYSIWYG演示脚本
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication, QMessageBox
from src.pymd_editor.app import MainWindow


def main():
    """启动演示应用程序"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("PyMD Editor - WYSIWYG Demo")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("PyMD")
    
    try:
        # 创建主窗口
        window = MainWindow()
        window.show()
        
        # 显示欢迎信息
        QMessageBox.information(
            window, 
            "欢迎使用PyMD Editor!", 
            "🎉 PyMD Editor现在支持所见即所得编辑！\n\n"
            "✨ 新功能：\n"
            "• 双模式编辑：传统模式 + WYSIWYG模式\n"
            "• 实时内容同步\n"
            "• 智能HTML到Markdown转换\n"
            "• 直观的格式化工具栏\n\n"
            "💡 使用提示：\n"
            "• 点击底部的'所见即所得'标签页开始体验\n"
            "• 使用'编辑模式'按钮开启直接编辑\n"
            "• 两种模式可以自由切换\n\n"
            "📁 可以打开 test_wysiwyg.md 文件进行测试"
        )
        
        # 加载测试文件（如果存在）
        test_file = Path("test_wysiwyg.md")
        if test_file.exists():
            try:
                window.load_file(test_file)
            except Exception as e:
                print(f"无法加载测试文件: {e}")
        
        # 启动应用程序
        return app.exec()
        
    except Exception as e:
        QMessageBox.critical(
            None,
            "启动失败", 
            f"应用程序启动失败:\n{str(e)}\n\n"
            "请确保已安装所有依赖:\n"
            "pip install -r requirements.txt"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())