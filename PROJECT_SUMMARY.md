# PyMD — 项目总结

## 定位

PyMD 是一个**本地优先**的文档工作区，专注于 Markdown 编辑与多格式文档转换。用户可以完全在本地运行，也可以将其部署为个人服务器，作为多设备共享或小团队使用的 File/DataHub。

## 第一阶段功能

| 功能 | 说明 |
|------|------|
| Markdown 编辑 | 实时预览、WYSIWYG 模式、深色/浅色主题 |
| PDF 转换 | PDF → Markdown / Word / Excel / PowerPoint（后端驱动） |
| Markdown 导出 | Markdown → Word / PDF |
| 文件浏览 | 浏览和管理 `.md`、`.pdf` 文件夹 |
| PDF 工具 | 预览、合并、拆分、提取页面 |
| AI 助手 | 可选的写作辅助聊天面板 |

## 技术栈

| 层 | 技术 |
|----|------|
| 桌面端 | Python 3.9+, PyQt6 |
| Web 前端 | HTML/CSS/JS（静态，无框架） |
| 后端 | FastAPI + Python |
| 容器 | Docker / docker-compose |
| 文档转换 | python-docx, pdfplumber, weasyprint |

## 部署模式

1. **本地模式（默认）** — 前后端均在用户机器上运行，无需联网
2. **个人服务器 / File DataHub** — 后端运行在用户自己的服务器，多设备共享文档
3. **Windows 桌面应用** — 独立 Qt 应用（`run_editor.bat` 或打包 EXE）
4. **Docker** — 容器化的个人服务器

## 项目结构

```
src/pymd_editor/
  main.py              # 入口；路由 Qt 或 Web 模式
  app.py               # MainWindow（Qt GUI）
  renderer.py          # Markdown → HTML
  exporter.py          # Word / PDF 导出
  wysiwyg_editor.py    # WYSIWYG 编辑模式
  three_column_layout.py  # 三栏布局 + AI 面板
  ai_framework.py      # AI 提供商抽象
  server/
    serve.py           # FastAPI 应用
    api.py             # REST 接口
    static/            # Web UI 静态资源
```

## 许可证

MIT

## ✅ 已完成功能

### 核心功能 (MVP)
1. ✅ **Markdown 编辑器**
   - QTextEdit 文本编辑控件
   - 自动 Undo/Redo 支持
   - 实时字数统计

2. ✅ **实时预览**
   - PyQt6 WebEngineView 渲染
   - Markdown → HTML 转换（markdown2）
   - 支持扩展语法：代码块、表格、任务列表、删除线等
   - < 200ms 防抖优化

3. ✅ **文件管理**
   - 新建文档 (Ctrl+N)
   - 打开 .md 文件 (Ctrl+O)
   - 保存 (Ctrl+S)
   - 另存为 (Ctrl+Shift+S)
   - 未保存更改提示

4. ✅ **主题系统**
   - 浅色/深色模式切换 (Ctrl+T)
   - 自定义 CSS 样式
   - 编辑器和预览区同步主题

5. ✅ **导出功能**
   - Word 导出 (.docx) - 使用 python-docx (Ctrl+Shift+W)
   - PDF 导出 - 使用 weasyprint (Ctrl+Shift+P)
## 许可证

MIT
