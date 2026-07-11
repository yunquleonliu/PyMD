# PyMD

PyMD 是一个**本地优先**的文档工作区，专注于 Markdown 编辑与多格式文档转换。可完全在本地运行，也可将其部署为个人服务器，作为多设备共享的 File/DataHub 使用。

## 第一阶段功能

- **Markdown 编辑** — 实时预览、WYSIWYG 模式、深色/浅色主题
- **PDF 转换** — PDF → Markdown / Word / Excel / PowerPoint（后端驱动）
- **Markdown 导出** — Markdown → Word / PDF
- **文件浏览** — 浏览和管理 `.md`、`.pdf` 文件夹
- **PDF 工具** — 预览、合并、拆分、提取页面
- **AI 助手** — 可选的写作辅助聊天面板

## 快速启动

### 本地模式（默认）

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
python -m pymd_editor.server.serve --dir data --host 127.0.0.1 --port 8765 --no-browser
```

打开 `http://127.0.0.1:8765`。

### 个人服务器 / File DataHub

在你自己的机器或私有主机上运行后端，从其他设备访问。

```bash
# 在服务器机器上
python -m pymd_editor.server.serve --dir /path/to/docs --host 0.0.0.0 --port 8765
```

### Windows 桌面应用

```
run_editor.bat
```

### Docker

```bash
docker compose up --build
```

## 后端选择器

Web UI 工具栏支持运行时切换后端：

| 模式 | 连接目标 |
|------|---------|
| Auto | 同源 → localhost → 纯浏览器 |
| Localhost | `http://127.0.0.1:8765` |
| Custom server | 你的个人服务器 URL |
| Demo / Lite | 纯浏览器（无需后端） |

## 相关文档

- [DEPLOYMENT_MODES.md](DEPLOYMENT_MODES.md)
- [ARCHITECTURE_v2.0.md](ARCHITECTURE_v2.0.md)
- [AI_USAGE_GUIDE.md](AI_USAGE_GUIDE.md)

## License

MIT
