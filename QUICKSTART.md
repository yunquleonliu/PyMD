# PyMD 快速启动

## 方式一：Web 服务器模式（推荐）

在本地启动完整服务器，浏览器访问：

```bash
pip install -r requirements.txt
pip install -e .
python -m pymd_editor.server.serve --dir data --host 127.0.0.1 --port 8765 --no-browser
```

打开 `http://127.0.0.1:8765`。

### 个人服务器 / File DataHub

在你的服务器机器上运行，供多设备访问：

```bash
python -m pymd_editor.server.serve --dir /path/to/docs --host 0.0.0.0 --port 8765
```

---

## 方式二：Windows 桌面应用

直接双击启动（无需浏览器）：

```
run_editor.bat
```

支持拖拽 `.md` 文件到桌面快捷方式图标直接打开。

---

## 方式三：Docker

```bash
docker compose up --build
```

---

## 快捷键（桌面应用）

| 功能 | 快捷键 |
|------|--------|
| 新建 | `Ctrl+N` |
| 打开 | `Ctrl+O` |
| 保存 | `Ctrl+S` |
| 另存为 | `Ctrl+Shift+S` |
| 导出 Word | `Ctrl+Shift+W` |
| 导出 PDF | `Ctrl+Shift+P` |
| 切换主题 | `Ctrl+T` |

---

详见 [DEPLOYMENT_MODES.md](DEPLOYMENT_MODES.md)。
