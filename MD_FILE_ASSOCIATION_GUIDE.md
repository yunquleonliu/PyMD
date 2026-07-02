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
