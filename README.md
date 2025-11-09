# PyMD Editor

A modern Markdown editor with AI assistance, WYSIWYG editing, and powerful export capabilities. Built with Python + PyQt6.

## ✨ Key Features

### 🤖 1. AI-Powered Assistance
- **Integrated AI Assistant**: Get help with writing, formatting, and content improvement
- **Smart Suggestions**: AI-powered content recommendations while you write
- **Context-Aware**: Three-column layout with dedicated AI panel

### 📝 2. WYSIWYG Editing
- **Rich Text Editor**: Visual editing mode for users who prefer rich text
- **Seamless Switching**: Toggle between Markdown source and WYSIWYG modes
- **Real-time Preview**: Live HTML preview with syntax highlighting
- **Image Support**: Drag-and-drop images with automatic path handling

### 📄 3. Professional Export
- **Print Preview** (Ctrl+P): Open rendered Markdown in PDF viewer for printing
- **PDF Export** (Ctrl+Shift+P): Native Qt-based PDF generation (no external dependencies)
- **Word Export** (Ctrl+Shift+W): Export to `.docx` format
- **Math Formulas**: Full LaTeX/MathJax support for equations
- **Page Breaks**: Support for page breaks in PDF output

### Additional Features
- ✅ **Dark/Light Themes**: Toggle with Ctrl+T
- ✅ **Multi-language**: Chinese and English interface
- ✅ **File Association**: Register `.md` files to open with PyMD
- ✅ **Markdown Extensions**: Code blocks, tables, task lists, strikethrough

## 🚀 Quick Start

### Option 1: Download Windows Executable (Recommended)
Download the latest release from [Releases](https://github.com/yunquleonliu/PyMD/releases) and run `PyMDEditor.exe`.

### Option 2: Run from Source

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the Editor**:
```bash
python -m pymd_editor.main
```

Or use the provided scripts:
- Windows: `run_editor.bat` or `run_editor.ps1`
- After installation: `install.bat` then `run_editor.bat`

### Option 3: Build Windows Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build distribution
create_distribution.bat
```

The executable will be in `dist\PyMDEditor\PyMDEditor.exe`.

## 📦 Dependencies

Core dependencies:
- **PyQt6** - GUI framework
- **PyQt6-WebEngine** - HTML preview engine
- **markdown2** - Markdown to HTML conversion
- **python-docx** - Word document generation

All dependencies are listed in `requirements.txt`.

> **注意**: Windows 上 weasyprint 可能需要 GTK3 运行时。如遇问题，Word 导出功能仍然可用。

## ⌨️ 快捷键

| 功能 | 快捷键 |
|------|--------|
## ⌨️ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New File | Ctrl+N |
| Open File | Ctrl+O |
| Save | Ctrl+S |
| Save As | Ctrl+Shift+S |
| Print Preview | Ctrl+P |
| Export PDF | Ctrl+Shift+P |
| Export Word | Ctrl+Shift+W |
| Insert Image | Ctrl+Shift+I |
| Toggle Theme | Ctrl+T |

## 📁 Project Structure

```
PyMD/
├── src/
│   └── pymd_editor/
│       ├── __init__.py              # Package initialization
│       ├── main.py                  # Entry point
│       ├── app.py                   # Main window and UI logic
│       ├── renderer.py              # Markdown → HTML renderer
│       ├── exporter.py              # PDF/Word exporters
│       ├── wysiwyg_editor.py        # WYSIWYG editor
│       ├── ai_framework.py          # AI assistant integration
│       └── three_column_layout.py   # Three-column UI layout
├── requirements.txt                 # Python dependencies
├── PyMDEditor.spec                  # PyInstaller configuration
├── create_distribution.bat          # Build script
└── README.md                        # This file
```

## 🛠️ Development

This project is open source under the MIT License:
- ✅ Free to use and modify
- ✅ Source code available
- ✅ Contributions welcome

### Contributing

Contributions are welcome! The project structure is modular and easy to extend:
- `renderer.py` - Modify rendering styles or add Markdown extensions
- `exporter.py` - Add new export formats
- `app.py` - Add UI features or toolbar buttons
- `ai_framework.py` - Enhance AI capabilities

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

Built with:
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- [markdown2](https://github.com/trentm/python-markdown2) - Markdown parser
- [MathJax](https://www.mathjax.org/) - Math formula rendering
- [python-docx](https://python-docx.readthedocs.io/) - Word document generation

---

**Made with ❤️ by yunquleonliu**
# 安装开发依赖
& ".venv\Scripts\pip.exe" install pytest

# 运行测试 (待添加)
& ".venv\Scripts\python.exe" -m pytest
```

## 📄 License

MIT License - 详见 LICENSE 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**开发工具**: Python 3.13 + PyQt6  
**目标平台**: Windows 10/11  
**开发日期**: 2025年10月
