# PyMD Editor

一个简单的 Windows Markdown 编辑器，支持实时预览和多格式导出。使用 Python + PyQt6 开发。

## ✨ 功能特性

### 已实现 (MVP)
- ✅ **实时编辑与预览**: 左侧编辑区 + 右侧实时 HTML 预览
- ✅ **文件管理**: 新建、打开、保存、另存为 `.md` 文件
- ✅ **主题切换**: 浅色/深色模式 (Ctrl+T)
- ✅ **导出 Word**: 导出为 `.docx` 格式 (Ctrl+Shift+W)
- ✅ **导出 PDF**: 导出为 PDF 格式 (Ctrl+Shift+P，需安装 weasyprint)
- ✅ **Markdown 扩展**: 支持代码块、表格、任务列表等

### 即将添加
- ⏳ 语法高亮编辑器
- ⏳ 自定义导出样式
- ⏳ 用户偏好设置持久化
- ⏳ 插件系统

## 🚀 快速开始

### 方法 1: 使用启动脚本 (推荐)

双击运行：
```
run_editor.bat       (批处理)
run_editor.ps1       (PowerShell)
```

### 方法 2: 命令行启动

```powershell
Set-Location -LiteralPath "C:\Users\Leon Liu\Desktop\微观社会经济\src"
& "C:\Users\Leon Liu\Desktop\微观社会经济\.venv\Scripts\python.exe" -m pymd_editor.main
```

## 📦 依赖安装

所有依赖已安装在 `.venv` 虚拟环境中：

核心依赖 (已安装):
- PyQt6 - GUI 框架
- PyQt6-WebEngine - HTML 预览引擎
- markdown2 - Markdown 转 HTML
- python-docx - Word 文档生成

可选依赖 (PDF 导出):
```powershell
& ".venv\Scripts\pip.exe" install weasyprint
```

> **注意**: Windows 上 weasyprint 可能需要 GTK3 运行时。如遇问题，Word 导出功能仍然可用。

## ⌨️ 快捷键

| 功能 | 快捷键 |
|------|--------|
| 新建 | Ctrl+N |
| 打开 | Ctrl+O |
| 保存 | Ctrl+S |
| 另存为 | Ctrl+Shift+S |
| 导出 PDF | Ctrl+Shift+P |
| 导出 Word | Ctrl+Shift+W |
| 切换主题 | Ctrl+T |

## 📁 项目结构

```
微观社会经济/
├── .venv/                      # Python 虚拟环境
├── src/
│   └── pymd_editor/
│       ├── __init__.py         # 包初始化
│       ├── main.py             # 启动入口
│       ├── app.py              # 主窗口和 UI 逻辑
│       ├── renderer.py         # Markdown → HTML 渲染器
│       └── exporter.py         # PDF/Word 导出器
├── requirements.txt            # 依赖列表
├── run_editor.bat             # Windows 批处理启动脚本
├── run_editor.ps1             # PowerShell 启动脚本
└── README.md                  # 本文档
```

## 🛠️ 开发说明

此项目采用开源模式开发，基于 MIT 许可证：
- ✅ 免费使用，无需预付费
- ✅ 源代码公开
- ✅ 可自由修改和分发
- 💡 未来如有服务端功能（如云同步），仅收取服务费用

### 添加新功能

项目结构清晰，易于扩展：
- `renderer.py` - 修改渲染样式或添加 Markdown 扩展
- `exporter.py` - 添加新的导出格式
- `app.py` - 添加 UI 功能或工具栏按钮

### 运行测试

```powershell
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
