from PyQt6.QtWidgets import QApplication
import sys
from pathlib import Path

from pymd_editor.app import MainWindow


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    
    # 如果从命令行传入文件路径，自动打开
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
        if file_path.exists() and file_path.suffix.lower() == '.md':
            win.load_file(file_path)
    
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
