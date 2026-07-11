# 🎯 PyMD Editor - 文件关联完全指南

## 问题 1：如何让 .md 文件与 PyMD Editor 关联？

我们提供 **3种方法**，按简单程度排序：

---

## 🥇 方法 1：拖拽打开（零配置，推荐！）

### 优点
- ✅ **最简单** - 无需任何配置
- ✅ **零权限** - 不需要管理员权限
- ✅ **即开即用** - 立即生效

### 使用方法

**方式 A：拖拽文件到图标**
```
1. 找到任意 .md 文件
2. 用鼠标拖拽到 run_editor.bat 图标上
3. 松开鼠标，编辑器自动打开该文件
```

**方式 B：创建桌面快捷方式（更方便）**
```
1. 右键 run_editor.bat
2. 发送到 → 桌面快捷方式
3. 可选：重命名为"PyMD Editor"
4. 以后直接拖文件到桌面图标即可
```

**提示**：可以一次拖拽多个 .md 文件（会依次打开）

---

## 🥈 方法 2：右键"打开方式"（推荐）

### 优点
- ✅ 无需管理员权限
- ✅ 集成到右键菜单
- ✅ 可设为默认程序

### 设置步骤

**一次性设置**：
```
1. 右键任意 .md 文件
2. 打开方式 → 选择其他应用
3. 点击"更多应用" → 下拉到底部
4. 点击"在这台电脑上查找其他应用"
5. 浏览到 run_editor.bat 并选择
6. ☑️ 勾选"始终使用此应用打开 .md 文件"
7. 确定
```

**以后使用**：
- 双击任意 .md 文件即可自动用 PyMD Editor 打开
- 右键 → 打开方式 也会显示 PyMD Editor

---

## 🥉 方法 3：注册表关联（系统级）

### 优点
- ✅ 系统级关联
- ✅ 双击直接打开
- ✅ 图标和描述完整

### ⚠️ 缺点
- 需要管理员权限
- 会修改注册表

### 使用方法

**注册关联**：
```
1. 右键 register_md_association.bat
2. 以管理员身份运行
3. 按提示完成设置
```

**取消关联**：
```
1. 右键 unregister_md_association.bat
2. 以管理员身份运行
```

**效果**：
- 双击任意 .md 文件自动用 PyMD Editor 打开
- 右键任意文件显示"用 PyMD Editor 打开"选项

---

## 📊 三种方法对比

| 方法 | 简单度 | 权限要求 | 推荐度 |
|------|--------|----------|--------|
| 拖拽打开 | ⭐⭐⭐⭐⭐ | 无 | 🥇 最推荐 |
| 右键打开方式 | ⭐⭐⭐⭐ | 无 | 🥈 推荐 |
| 注册表关联 | ⭐⭐⭐ | 需管理员 | 🥉 可选 |

---

## 🎬 推荐工作流

### 给新用户（最简单）
```
1. 解压 PyMD Editor 到任意文件夹
2. 右键 run_editor.bat → 发送到桌面快捷方式
3. 拖拽 .md 文件到桌面快捷方式图标
✅ 完成！无需任何配置
```

### 给频繁使用者（一次设置）
```
1. 右键任意 .md 文件
2. 打开方式 → 选择 run_editor.bat
3. 勾选"始终使用"
✅ 以后双击 .md 文件自动打开
```

### 给高级用户（系统集成）
```
1. 以管理员运行 register_md_association.bat
✅ 完整的系统级集成
```

---

## 🔧 故障排除

### Q: 拖拽文件无反应？
**A**: 确保拖拽到的是 `run_editor.bat`，不是文件夹

### Q: 提示找不到 Python？
**A**: 检查 `.venv` 文件夹是否存在，运行 `install.bat` 重新安装

### Q: 双击 .md 文件打开了其他程序？
**A**: 右键文件 → 打开方式 → 选择 PyMD Editor

### Q: 如何恢复 .md 的默认程序？
**A**: 
- 方法2：右键 → 打开方式 → 选择其他程序
- 方法3：运行 `unregister_md_association.bat`

---

## 💡 高级技巧

### 创建 SendTo 菜单项
```
1. Win+R 输入 shell:sendto 打开 SendTo 文件夹
2. 在 SendTo 文件夹创建 run_editor.bat 的快捷方式
3. 重命名为"PyMD Editor"
4. 以后右键任意文件 → 发送到 → PyMD Editor
```

### 命令行使用
```batch
# 打开指定文件
run_editor.bat "C:\path\to\file.md"

# 从命令行启动
cd C:\PyMDEditor\src
..\venv\Scripts\python.exe -m pymd_editor.main file.md
```

---

## 🎯 最佳实践建议

**对于个人用户**：
- 使用 **方法1（拖拽）**，最简单无配置

**对于团队/公司**：
- 统一使用 **方法2（右键）**，一次设置永久使用

**对于开发者**：
- 使用 **方法3（注册表）**，完整系统集成

---

## 📌 总结

**最推荐**：创建桌面快捷方式 + 拖拽打开
- 零配置
- 零权限
- 零学习成本

**操作只需 30 秒**：
```
1. 右键 run_editor.bat → 发送到桌面快捷方式
2. 拖拽 .md 文件到桌面图标
3. 开始编辑！
```

✅ 简单、无忧、随时可用！


---

## Additional Notes (merged from MD_FILE_ASSOCIATION_GUIDE.md)

# PyMD Editor - .md 文件关联指南

## 问题

**"我可以在 dist 里面打开,但是如果想把 .md 关联到这个文件不行"**

## 原因

旧的 `register_md_association.bat` 是为**开发环境**设计的,使用的是:
```
src\.venv\Scripts\python.exe
```

但现在你需要关联到**可执行文件**:
```
dist\PyMDEditor\PyMDEditor.exe
```

## 解决方案

### 步骤 1: 使用新的注册脚本

我已经创建了专门为可执行文件设计的脚本:

**注册 .md 文件关联:**
```batch
.\register_md_for_dist.bat
```

**取消 .md 文件关联:**
```batch
.\unregister_md_for_dist.bat
```

### 步骤 2: 以管理员身份运行

1. 右键点击 `register_md_for_dist.bat`
2. 选择 **"以管理员身份运行"**
3. 确认操作

### 步骤 3: 测试

双击任意 `.md` 文件,应该会用 PyMD Editor 打开!

## 功能特性

注册后你可以:

✅ **双击 .md 文件** - 自动用 PyMD Editor 打开  
✅ **右键任意文件** - 选择 "用 PyMD Editor 打开"  
✅ **图标显示** - .md 文件显示自定义图标

## 文件说明

| 文件 | 用途 | 需要管理员 |
|------|------|-----------|
| `register_md_for_dist.bat` | 注册 .md 文件关联到可执行文件 | ✓ 是 |
| `unregister_md_for_dist.bat` | 取消 .md 文件关联 | ✓ 是 |
| `register_md_association.bat` | 旧版本(开发环境用) | - |
| `unregister_md_association.bat` | 旧版本(开发环境用) | - |

## 注册表修改内容

脚本会修改以下注册表项:

```
HKEY_CLASSES_ROOT\.md
  └─ (默认值) = "PyMDEditor.Document"

HKEY_CLASSES_ROOT\PyMDEditor.Document
  ├─ (默认值) = "Markdown Document"
  ├─ DefaultIcon
  │   └─ (默认值) = "C:\...\dist\PyMDEditor\PyMDEditor.exe,0"
  └─ shell\open\command
      └─ (默认值) = "C:\...\dist\PyMDEditor\PyMDEditor.exe" "%1"

HKEY_CLASSES_ROOT\*\shell\PyMDEditor
  ├─ (默认值) = "用 PyMD Editor 打开"
  └─ command
      └─ (默认值) = "C:\...\dist\PyMDEditor\PyMDEditor.exe" "%1"
```

## 常见问题

### Q1: 提示"需要管理员权限"

**A**: 修改注册表需要管理员权限。请:
1. 右键脚本
2. 选择 "以管理员身份运行"

### Q2: 提示"未找到 PyMD Editor 可执行文件"

**A**: 请先构建可执行文件:
```batch
.\quick_build.bat
```

确认 `dist\PyMDEditor\PyMDEditor.exe` 存在。

### Q3: 注册后双击 .md 文件没反应

**A**: 
1. 检查可执行文件是否能独立运行:
   ```batch
   cd dist\PyMDEditor
   .\PyMDEditor.exe test.md
   ```

2. 重新注册:
   ```batch
   .\unregister_md_for_dist.bat
   .\register_md_for_dist.bat
   ```

3. 重启 Windows 资源管理器:
   ```powershell
   taskkill /f /im explorer.exe
   start explorer.exe
   ```

### Q4: 想恢复默认的 .md 打开方式

**A**: 运行取消关联脚本:
```batch
.\unregister_md_for_dist.bat
```

然后在 Windows 设置中选择其他默认程序。

### Q5: 移动了可执行文件位置后不工作

**A**: 如果移动了 `dist\PyMDEditor\` 目录,需要重新注册:
```batch
.\unregister_md_for_dist.bat
.\register_md_for_dist.bat
```

## 发布时的建议

如果你要把程序打包给其他用户,建议:

1. **复制整个 dist\PyMDEditor 目录**
2. **在发布包中包含注册脚本**:
   - `register_md_for_dist.bat`
   - `unregister_md_for_dist.bat`
3. **修改脚本路径**为相对路径

或者在安装程序中自动注册文件关联。

## 测试步骤

完整测试流程:

```batch
# 1. 构建可执行文件
.\quick_build.bat

# 2. 测试可执行文件
cd dist\PyMDEditor
.\PyMDEditor.exe

# 3. 注册文件关联(管理员)
cd ..\..
.\register_md_for_dist.bat

# 4. 测试双击 .md 文件
# 找一个 .md 文件双击

# 5. 如需取消关联(管理员)
.\unregister_md_for_dist.bat
```

## 总结

✅ **问题 1 已解决**: build 目录已删除,以后构建也会自动清理  
✅ **问题 2 已解决**: 使用 `register_md_for_dist.bat` 关联 .md 文件到可执行文件

**快速开始**:
```batch
.\register_md_for_dist.bat  # 以管理员身份运行
```
