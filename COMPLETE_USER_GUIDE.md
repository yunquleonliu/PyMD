# PyMD 用户手册 / User Guide

---

## 启动 / Getting Started

### 本地模式 / Local mode

```bash
pip install -r requirements.txt
pip install -e .
python -m pymd_editor.server.serve --dir data --host 127.0.0.1 --port 8765 --no-browser
```

打开 `http://127.0.0.1:8765`。 / Open `http://127.0.0.1:8765`.

### 个人服务器 / Personal server (File DataHub)

```bash
python -m pymd_editor.server.serve --dir /path/to/docs --host 0.0.0.0 --port 8765
```

从其他设备访问 `http://<服务器IP>:8765`。 / Connect from any device at `http://<server-ip>:8765`.

### Windows 桌面应用 / Windows desktop app

```
run_editor.bat
```

---

## 核心功能 / Core Features

### Markdown 编辑 / Markdown Editing

- 左栏编辑，右栏实时预览 / Left pane editor, right pane live preview
- 支持 WYSIWYG 模式 / WYSIWYG mode supported
- 深色/浅色主题切换（桌面：`Ctrl+T`）/ Dark/light theme (`Ctrl+T` on desktop)

### 文档转换 / Document Conversion

| 转换 / Conversion | 说明 / Notes |
|---|---|
| PDF → Word / Excel / PPT | 需后端 / Requires backend |
| PDF → Markdown | 需后端 / Requires backend |
| Markdown → Word | 需后端 / Requires backend |
| Markdown → PDF | 需后端 / Requires backend |

在 Web UI 工具栏选择文件后点击对应导出按钮。  
Use the toolbar export buttons after selecting a file in the Web UI.

### 文件浏览 / File Browser

左侧面板浏览 `.md` 和 `.pdf` 文件夹。  
Browse `.md` and `.pdf` files in the left sidebar.

### PDF 工具 / PDF Tools

预览、合并、拆分、提取页面——通过 PDF 工具栏操作。  
Preview, merge, split, extract pages — via the PDF toolbar.

### AI 助手 / AI Assistant

右侧 AI 面板可用于写作辅助（需配置 AI 后端）。  
Right-side AI panel for writing assistance (requires AI backend configuration).  
详见 [AI_USAGE_GUIDE.md](AI_USAGE_GUIDE.md).

---

## 快捷键（桌面应用）/ Shortcuts (desktop app)

| 功能 / Action | 快捷键 / Shortcut |
|---|---|
| 新建 / New | `Ctrl+N` |
| 打开 / Open | `Ctrl+O` |
| 保存 / Save | `Ctrl+S` |
| 另存为 / Save As | `Ctrl+Shift+S` |
| 导出 Word / Export Word | `Ctrl+Shift+W` |
| 导出 PDF / Export PDF | `Ctrl+Shift+P` |
| 切换主题 / Toggle Theme | `Ctrl+T` |

---

## 后端选择器 / Backend Selector

Web UI 工具栏可切换后端：  
Switch backend in the Web UI toolbar:

| 模式 / Mode | 目标 / Target |
|---|---|
| Auto | 同源 → localhost → 纯浏览器 / Same-origin → localhost → browser-only |
| Localhost | `http://127.0.0.1:8765` |
| Custom server | 你的服务器地址 / Your server URL |
| Demo / Lite | 纯浏览器，无需后端 / Browser-only, no backend |

---

详见 [DEPLOYMENT_MODES.md](DEPLOYMENT_MODES.md) · [AI_USAGE_GUIDE.md](AI_USAGE_GUIDE.md) · [README.md](README.md)

**为什么推荐**：
- ✅ 零配置（不需要任何设置）
- ✅ 零权限（不需要管理员）
- ✅ 零学习（拖拽就能用）
- ✅ 零风险（不修改系统）

**其他方法**：
- 方法 2：右键 → 打开方式（一次设置，永久使用）
- 方法 3：注册表关联（需管理员，系统级集成）

📖 详见：`FILE_ASSOCIATION_GUIDE.md`

---

## ❓ 问题 2: 用户如何获取这个工具？

### ✅ 最佳答案：3种方式，按简单程度排序

---

### 🥇 方式 1: GitHub Release（推荐！）

**优势**：
- ✅ 完全免费
- ✅ 一键下载
- ✅ 自动更新通知
- ✅ 符合开源理念

**部署步骤**：
```bash
# 1. 创建 GitHub 仓库
git init
git add .
git commit -m "PyMD Editor v1.0.0"
git remote add origin https://github.com/你的用户名/pymd-editor.git
git push -u origin main

# 2. 创建分发包
运行: create_distribution.bat
生成: PyMDEditor_v1.0.0.zip

# 3. 创建 GitHub Release
访问 GitHub → Releases → Create new release
上传 PyMDEditor_v1.0.0.zip
```

**用户获取流程**（3步，2分钟）：
```
1. 访问: https://github.com/你的用户名/pymd-editor/releases
2. 下载: PyMDEditor_v1.0.0.zip
3. 解压并双击: install.bat

✅ 完成！
```

**分享链接**：
```
https://github.com/你的用户名/pymd-editor
```

---

### 🥈 方式 2: 直接下载 ZIP（最简单）

**优势**：
- ✅ 最简单（用户只需解压）
- ✅ 离线可用
- ✅ 适合企业内网

**部署步骤**：
```bash
# 创建分发包
运行: create_distribution.bat

# 上传到任何地方：
- 公司内网服务器
- 网盘（百度云、Google Drive）
- 自己的网站
- 微信/邮件直接发送
```

**用户获取流程**（2步，1分钟）：
```
1. 下载 PyMDEditor_v1.0.0.zip
2. 解压到任意文件夹

✅ 完成！无需安装
```

---

### 🥉 方式 3: PyPI 发布（专业级）

**优势**：
- ✅ Python 标准生态
- ✅ 自动依赖管理
- ✅ 版本更新方便

**部署步骤**：
```bash
# 1. 添加 setup.py（见 DISTRIBUTION_GUIDE.md）
# 2. 发布到 PyPI
pip install twine
python setup.py sdist bdist_wheel
twine upload dist/*
```

**用户获取流程**（1条命令，30秒）：
```bash
pip install pymd-editor
pymd-editor  # 直接启动

✅ 完成！
```

---

## 📊 三种方式对比

| 方式 | 用户门槛 | 分发成本 | 推荐度 |
|------|----------|----------|--------|
| GitHub Release | 低（点击下载） | 零成本 | 🥇 最推荐 |
| 直接分发 ZIP | 极低（解压即用） | 服务器/网盘 | 🥈 推荐 |
| PyPI | 中（需懂 pip） | 需注册账号 | 🥉 可选 |

---

## 🎯 推荐策略：阶段式部署

### 阶段 1：当前（立即可用）

**方式**：直接分发 ZIP
```
1. 运行 create_distribution.bat
2. 发给朋友测试
3. 或上传到网盘分享
```

**用户体验**：
```
下载 → 解压 → 双击 run_editor.bat → 开始使用
```

---

### 阶段 2：正式发布（1-2周后）

**方式**：GitHub Release
```
1. 创建 GitHub 仓库
2. 上传代码
3. 创建 Release 发布
4. 分享 GitHub 链接
```

**用户体验**：
```
访问 GitHub → 下载 → 解压 → 运行 install.bat
```

**额外好处**：
- ⭐ 收集用户反馈（GitHub Issues）
- 📊 统计下载量
- 🔄 版本更新通知
- 🤝 社区贡献

---

### 阶段 3：规模化（未来）

**方式**：PyPI + 官网 + 自动更新
```
1. 发布到 PyPI: pip install pymd-editor
2. 建立官网: https://pymd-editor.com
3. 编辑器内置自动更新检查
4. 云服务集成（付费功能）
```

---

## 💰 商业模式：自愿付费

### 现阶段（免费开源）
```
✅ 完全免费使用
✅ MIT 开源许可
✅ 无需注册
✅ 无广告
```

### 未来（可选付费）
```
💡 云同步服务 - $5/月
   - 多设备同步
   - 版本历史
   - 在线备份

💡 协作编辑 - $10/月
   - 团队协作
   - 实时编辑
   - 评论功能

💡 高级功能 - 按需付费
   - 专业模板库
   - 优先技术支持
   - 定制开发
```

**重要原则**：
- ✅ 基础编辑器永久免费
- ✅ 所有付费功能可选
- ✅ 先试用再决定
- ✅ 随时可取消

---

## 📦 实际操作：3个立即可做的事

### 1️⃣ 测试拖拽打开（10秒）
```
右键 run_editor.bat → 发送到桌面快捷方式
拖拽 EXAMPLE.md 到快捷方式图标
```

### 2️⃣ 创建分发包（30秒）
```
双击运行: create_distribution.bat
获得: PyMDEditor_v1.0.0.zip
```

### 3️⃣ 分享给朋友（1分钟）
```
发送 ZIP 包
附带说明：解压后双击 run_editor.bat
```

---

## 🚀 推广建议

### 社交媒体
```
📱 Twitter/X: "开源免费的 Markdown 编辑器，拖拽即用！"
📘 Reddit: r/opensource, r/Markdown
💬 微信公众号: 技术类自媒体
🎥 B站/YouTube: 功能演示视频
```

### 技术社区
```
🔗 GitHub Awesome Lists
📝 Medium/掘金技术文章
💡 Product Hunt 发布
🎓 开发者论坛
```

### 企业市场
```
💼 企业内网部署
📊 技术培训材料
🏢 办公软件替代方案
```

---

## 📞 用户支持体系

### 文档层次
```
📄 START_HERE.txt           - 30秒速览
📖 QUICKSTART.md           - 5分钟上手
📘 README.md               - 完整文档
📚 FILE_ASSOCIATION_GUIDE.md - 关联指南
🔧 DISTRIBUTION_GUIDE.md   - 分发指南
```

### 反馈渠道
```
🐛 GitHub Issues - Bug 报告
💡 GitHub Discussions - 功能建议
📧 Email - 商业咨询
💬 Discord/Telegram - 社区交流
```

---

## ✅ 总结：最简单的推广路径

### 今天（现在）
```
1. 双击 create_distribution.bat
2. 获得 PyMDEditor_v1.0.0.zip
3. 发给 5 个朋友测试
```

### 本周
```
1. 创建 GitHub 仓库
2. 上传代码
3. 创建第一个 Release
4. 分享到技术社区
```

### 下个月
```
1. 收集用户反馈
2. 迭代优化功能
3. 积累 GitHub Stars
4. 考虑 PyPI 发布
```

### 未来
```
1. 建立官网
2. 开发云服务
3. 构建付费模式
4. 形成社区生态
```

---

## 🎯 核心理念：Keep It Simple

**给用户**：
- 下载 → 解压 → 双击 → 使用（30秒）
- 或拖拽 .md 文件到图标（3秒）

**给开发者**：
- 代码开源 → 社区参与 → 持续改进

**给未来**：
- 基础免费 → 服务付费 → 可持续发展

---

✅ **现在就可以开始分享了！**
