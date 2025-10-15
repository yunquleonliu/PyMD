# PyMD Editor

A simple Windows Markdown editor with live preview and multi-format export. Built with Python + PyQt6.

## ✨ Features

### Implemented (MVP)
- ✅ **Live editing & preview**: Left editor + right real-time HTML preview
- ✅ **File management**: New, Open, Save, Save As `.md`
- ✅ **Theme switching**: Light/Dark mode (Ctrl+T)
- ✅ **Export to Word**: Export as `.docx` (Ctrl+Shift+W)
- ✅ **Export to PDF**: Export as PDF (Ctrl+Shift+P, requires weasyprint)
- ✅ **Markdown extensions**: Code blocks, tables, task lists, etc.

### Coming soon
- ⏳ Syntax highlighting editor
- ⏳ Custom export styles
- ⏳ User preferences persistence
- ⏳ Plugin system

## 🚀 Quick Start

### Method 1: Use the launch script (recommended)

Double-click to run:
```
run_editor.bat       (Batch)
run_editor.ps1       (PowerShell)
```

### Method 2: Command line launch

```powershell
Set-Location -LiteralPath "C:\Users\Leon Liu\Desktop\微观社会经济\src"
& "C:\Users\Leon Liu\Desktop\微观社会经济\.venv\Scripts\python.exe" -m pymd_editor.main
```

## 📦 Dependencies

All dependencies are installed in the `.venv` virtual environment:

Core dependencies (already installed):
- PyQt6 - GUI framework
- PyQt6-WebEngine - HTML preview engine
- markdown2 - Markdown to HTML
- python-docx - Word document generation

Optional (PDF export):
```powershell
& ".venv\Scripts\pip.exe" install weasyprint
```

> **Note**: On Windows, weasyprint may require GTK3 runtime. If issues occur, Word export remains available.

## ⌨️ Shortcuts

| Feature | Shortcut |
|---------|----------|
| New     | Ctrl+N   |
| Open    | Ctrl+O   |
| Save    | Ctrl+S   |
| Save As | Ctrl+Shift+S |
| Export PDF | Ctrl+Shift+P |
| Export Word | Ctrl+Shift+W |
| Toggle Theme | Ctrl+T |

## 📁 Project Structure

```
微观社会经济/
├── .venv/                      # Python virtual environment
├── src/
│   └── pymd_editor/
│       ├── __init__.py         # Package init
│       ├── main.py             # Entry point
│       ├── app.py              # Main window & UI logic
│       ├── renderer.py         # Markdown → HTML renderer
│       └── exporter.py         # PDF/Word exporter
├── requirements.txt            # Dependency list
├── run_editor.bat              # Windows batch launch script
├── run_editor.ps1              # PowerShell launch script
└── README_en.md                # This document
```

## 🛠️ Development Notes

This project is open source under the MIT license:
- ✅ Free to use, no upfront payment
- ✅ Source code is public
- ✅ Free to modify and distribute
- 💡 Future server-side features (like cloud sync) will be paid services only

### Adding new features

The project is modular and easy to extend:
- `renderer.py` - Change rendering style or add Markdown extensions
- `exporter.py` - Add new export formats
- `app.py` - Add UI features or toolbar buttons

### Running tests

```powershell
# Install dev dependencies
& ".venv\Scripts\pip.exe" install pytest

# Run tests (to be added)
& ".venv\Scripts\python.exe" -m pytest
```

## 📄 License

MIT License - see LICENSE file

## 🤝 Contributing

Issues and Pull Requests welcome!

---

**Dev tools**: Python 3.13 + PyQt6  
**Target platform**: Windows 10/11  
**Dev date**: October 2025
