# PyMD

PyMD 是一个**本地优先**的文档工作区，专注于 Markdown 编辑与多格式文档转换。可完全在本地运行，也可部署到客户 vLAN，并通过 Dataflowxx 分配的 HTTPS 子域作为企业 File/DataHub 使用。

当前项目已经进入“正式化 init”阶段，核心方向是：

- 明确三种正式部署模式：全本地、官方云、客户子域自部署
- 统一 frontend + backend 能力边界
- 引入 workspace sync 作为跨设备基础
- 强化 Agent 协作与验证流程

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

### 客户子域自部署 / File DataHub

在客户 vLAN 机器上运行后端，由 Dataflowxx 分配 HTTPS 子域，例如 `https://customer-a.dataflowxx.dpdns.org`。客户不需要自己购买域名；子域可以通过内网 DNS、隧道或其他部署机制指向客户服务器。

```bash
# 在客户服务器机器上
python -m pymd_editor.server.serve --dir /path/to/docs --host 0.0.0.0 --port 8765
```

Docker 模板见 [deploy/customer-subdomain](deploy/customer-subdomain)。

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
| Official Cloud | `https://dataflowxx.dpdns.org` |
| Custom server | 客户子域、隧道 URL 或私有后端 URL |
| Demo / Lite | 纯浏览器（无需后端） |

`Open Folder` 是浏览器侧能力，打开的是当前用户机器上的本地目录。Chrome/Edge 只在 `localhost` 或 HTTPS 页面中开放该能力；如果直接访问 `http://10.x.x.x:8765` 这类局域网 HTTP 地址，前端会显示禁用状态。正式客户部署应使用 Dataflowxx 分配的 HTTPS 子域，`10.x.x.x:8765` 只作为调试入口。

## 相关文档

- [PROJECT_BLUEPRINT.md](PROJECT_BLUEPRINT.md)
- [DEPLOYMENT_MODES.md](DEPLOYMENT_MODES.md)
- [WORKSPACE_SYNC_ARCHITECTURE.md](WORKSPACE_SYNC_ARCHITECTURE.md)
- [LOCAL_VALIDATION.md](LOCAL_VALIDATION.md)
- [AGENTS.md](AGENTS.md)
- [ARCHITECTURE_v2.0.md](ARCHITECTURE_v2.0.md)
- [AI_USAGE_GUIDE.md](AI_USAGE_GUIDE.md)

## License

MIT
