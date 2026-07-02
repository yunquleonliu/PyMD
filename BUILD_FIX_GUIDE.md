# PyMD Editor 可执行文件构建和打包说明

## 问题：缺少 python313.dll

### 原因
PyInstaller 在某些情况下不会自动包含 `python313.dll`，导致运行时错误：
```
Failed to load Python DLL 'C:\Users\Leon Liu\Desktop\PyMD\build\build_exe\_internal\python313.dll'
```

### 解决方案

#### 方法1: 手动复制（临时方案）
```powershell
Copy-Item "D:\InstalledTools\Python313\python313.dll" -Destination "dist\PyMDEditor_v0.2.0\" -Force
```

#### 方法2: 修改 spec 文件（永久方案）

spec 文件已经修改为包含 python313.dll，但需要确保它在正确的位置。

运行 `fix_build_and_package.bat` 脚本自动完成以下步骤：
1. 使用 PyInstaller 构建可执行文件
2. 自动复制 python313.dll 到 dist 文件夹
3. 创建发布包
4. 压缩为 ZIP 文件

## 构建步骤

### 1. 清理旧文件
```powershell
Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
```

### 2. 运行 PyInstaller
```powershell
pyinstaller build_exe.spec --noconfirm
```

### 3. 复制 python313.dll
```powershell
Copy-Item "D:\InstalledTools\Python313\python313.dll" -Destination "dist\PyMDEditor_v0.2.0\" -Force
```

### 4. 测试可执行文件
```powershell
cd dist\PyMDEditor_v0.2.0
.\PyMDEditor.exe
```

### 5. 创建发布包
```powershell
.\create_windows_release.bat
```

## 自动化脚本

运行 `fix_build_and_package.bat` 一键完成所有步骤。

## 验证

确保以下文件存在：
- `dist\PyMDEditor_v0.2.0\PyMDEditor.exe`
- `dist\PyMDEditor_v0.2.0\python313.dll` ✅ **关键文件**
- `dist\PyMDEditor_v0.2.0\_internal\` (所有依赖)

## 常见问题

### Q: 为什么 spec 文件的修改没有生效？
A: PyInstaller 有时会缓存旧的配置。解决方法：
```powershell
pyinstaller build_exe.spec --clean --noconfirm
```

### Q: 如何验证 python313.dll 是否正确包含？
A: 运行以下命令：
```powershell
Test-Path "dist\PyMDEditor_v0.2.0\python313.dll"
```
应该返回 `True`

### Q: 可执行文件能运行，但缺少某些功能？
A: 检查 hiddenimports 列表，确保所有必需的模块都已包含。

## 下一步

1. ✅ python313.dll 已复制
2. 测试可执行文件是否正常运行
3. 运行 `create_windows_release.bat` 创建发布包
4. 上传到 GitHub Release
