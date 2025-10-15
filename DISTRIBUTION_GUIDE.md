# PyMD Editor - 分发与部署指南

## 🎯 目标：让用户获取工具尽可能简单

根据您的要求：**简单、无忧、自愿付费**

---

## 📦 方案 1: GitHub Release（推荐）

### 优势
✅ 完全免费托管  
✅ 自动版本管理  
✅ 用户一键下载  
✅ 支持更新通知  

### 部署步骤

1. **创建 GitHub 仓库**
   ```bash
   # 在 GitHub 创建新仓库 "pymd-editor"
   git init
   git add .
   git commit -m "Initial release v1.0.0"
   git remote add origin https://github.com/你的用户名/pymd-editor.git
   git push -u origin main
   ```

2. **创建 Release**
   - 访问 GitHub 仓库 → Releases → Create a new release
   - Tag: `v1.0.0`
   - 上传: `PyMDEditor_v1.0.0.zip`

3. **用户下载链接**
   ```
   https://github.com/你的用户名/pymd-editor/releases/latest
   ```

### 用户使用流程（3步）
```
1. 下载 PyMDEditor_v1.0.0.zip
2. 解压后运行 install.bat
3. 运行 register_md_association.bat（可选，关联 .md 文件）
```

---

## 📦 方案 2: 一键安装脚本（最简单）

### 原理
用户只需运行一条命令，自动完成下载和安装。

### 创建安装器

**文件：`install_from_web.bat`**
```batch
@echo off
echo 正在从 GitHub 下载 PyMD Editor...
powershell -command "Invoke-WebRequest -Uri 'https://github.com/你的用户名/pymd-editor/archive/refs/heads/main.zip' -OutFile 'pymd.zip'"
powershell -command "Expand-Archive -Path 'pymd.zip' -DestinationPath '%USERPROFILE%\PyMDEditor' -Force"
cd /d "%USERPROFILE%\PyMDEditor\pymd-editor-main"
call install.bat
```

### 用户使用（1步）
```
运行 install_from_web.bat
```

---

## 📦 方案 3: PyPI 发布（专业级）

### 优势
✅ 标准 Python 生态  
✅ `pip install pymd-editor` 一键安装  
✅ 自动管理依赖  

### 准备工作

1. **添加 `setup.py`**
   ```python
   from setuptools import setup, find_packages
   
   setup(
       name="pymd-editor",
       version="1.0.0",
       packages=find_packages("src"),
       package_dir={"": "src"},
       install_requires=[
           "PyQt6>=6.9.0",
           "PyQt6-WebEngine>=6.9.0",
           "markdown2>=2.5.0",
           "python-docx>=1.2.0",
       ],
       entry_points={
           "console_scripts": [
               "pymd-editor=pymd_editor.main:main",
           ],
       },
   )
   ```

2. **发布到 PyPI**
   ```bash
   pip install twine
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

### 用户使用（1条命令）
```bash
pip install pymd-editor
pymd-editor  # 直接启动
```

---

## 🎯 推荐策略：混合方案

### 阶段 1：快速启动（当前）
- ✅ **GitHub Release** - 提供 ZIP 下载
- ✅ **一键安装脚本** - `install.bat`
- ✅ **文件关联** - `register_md_association.bat`

**用户获取方式**：
```
https://github.com/你的用户名/pymd-editor/releases
→ 下载 ZIP → 运行 install.bat
```

### 阶段 2：规模化（未来）
- 🔄 **PyPI 发布** - `pip install pymd-editor`
- 🔄 **自动更新功能** - 编辑器内检查更新
- 💡 **云服务集成** - 付费同步、协作功能

---

## 🔗 .md 文件关联方案对比

### 方案 A：Windows 注册表（已实现）
✅ **优点**：系统级关联，双击直接打开  
⚠️ **缺点**：需要管理员权限  
📝 **使用**：运行 `register_md_association.bat`

### 方案 B：右键"打开方式"
✅ **优点**：无需管理员权限  
⚠️ **缺点**：每次需手动选择  
📝 **使用**：右键 .md → 打开方式 → 选择 `run_editor.bat`

### 方案 C：拖拽打开
✅ **优点**：最简单，零配置  
📝 **使用**：拖拽 .md 文件到 `run_editor.bat` 图标

---

## 📊 推荐分发流程

### 对于普通用户（3 步）
```
1. 访问 GitHub Release 页面
2. 下载最新版 PyMDEditor_v1.0.0.zip
3. 解压后双击 install.bat
```

### 对于技术用户（1 条命令）
```bash
pip install pymd-editor  # 需先发布到 PyPI
```

### 对于企业内部（最简单）
```
1. 在内网服务器放置 ZIP 包
2. 提供内部下载链接
3. 用户解压运行 install.bat
```

---

## 💰 自愿付费策略

### 当前（免费开源）
- ✅ 完全免费使用
- ✅ MIT 许可证
- ✅ 源代码公开

### 未来（可选付费服务）
- 💡 **云同步服务** - 多设备 Markdown 同步
- 💡 **协作编辑** - 团队实时协作
- 💡 **高级模板** - 专业导出模板库
- 💡 **优先支持** - 技术支持和定制开发

**实现方式**：
- 基础编辑器永久免费
- 云服务按月订阅（如 $5/月）
- 提供免费试用期

---

## 🚀 立即行动

### 现在就可以做：

1. **创建 GitHub 仓库**
   ```bash
   运行: create_distribution.bat
   上传到 GitHub
   ```

2. **测试文件关联**
   ```bash
   以管理员身份运行: register_md_association.bat
   双击任意 .md 文件测试
   ```

3. **分享给朋友测试**
   ```
   发送 PyMDEditor_v1.0.0.zip
   让他们运行 install.bat
   ```

---

## 📞 用户支持

### 文档清单
- ✅ `START_HERE.txt` - 首次使用指引
- ✅ `QUICKSTART.md` - 快速入门
- ✅ `README.md` - 完整文档
- ✅ `EXAMPLE.md` - 功能演示

### 问题反馈
- GitHub Issues（推荐）
- Email 支持
- 社区论坛

---

**总结**：GitHub Release + install.bat 是目前最简单的分发方式！
