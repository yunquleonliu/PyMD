# PyMD Editor - Windows 可执行文件构建说明

## 方法1: 使用自动脚本 (推荐)

1. 运行构建脚本:
```powershell
.\build_windows_exe.bat
```

2. 等待构建完成 (约3-5分钟)

3. 运行打包脚本:
```powershell
.\create_windows_release.bat
```

## 方法2: 手动构建

### 步骤1: 安装 PyInstaller
```powershell
pip install pyinstaller>=6.0.0
```

### 步骤2: 构建可执行文件
```powershell
# 进入项目目录
cd "c:\Users\Leon Liu\Desktop\PyMD"

# 使用spec文件构建
pyinstaller build_exe.spec --noconfirm --clean
```

### 步骤3: 测试可执行文件
```powershell
# 运行生成的可执行文件
.\dist\PyMDEditor\PyMDEditor.exe
```

### 步骤4: 创建发布包
```powershell
# 创建发布目录
mkdir release\PyMD-v0.2.0-Windows

# 复制所有文件
xcopy dist\PyMDEditor\* release\PyMD-v0.2.0-Windows\ /E /I /Y

# 添加文档
copy README.md release\PyMD-v0.2.0-Windows\
copy LICENSE release\PyMD-v0.2.0-Windows\
copy QUICKSTART.md release\PyMD-v0.2.0-Windows\

# 创建启动脚本
echo @echo off > "release\PyMD-v0.2.0-Windows\Launch PyMD Editor.bat"
echo start "" "PyMDEditor.exe" %%* >> "release\PyMD-v0.2.0-Windows\Launch PyMD Editor.bat"

# 压缩为zip
cd release
Compress-Archive -Path "PyMD-v0.2.0-Windows\*" -DestinationPath "PyMD-v0.2.0-Windows.zip" -Force
cd ..
```

## 发布到 GitHub

1. 确保 git tag 已创建并推送:
```powershell
git tag -a v0.2.0-chat-enhancement -m "Release v0.2.0 - Enhanced AI Chat Interface"
git push origin v0.2.0-chat-enhancement
```

2. 前往 GitHub Release 页面
3. 使用标签 `v0.2.0-chat-enhancement` 创建新 Release
4. 上传 `PyMD-v0.2.0-Windows.zip` 作为发布资产
5. 填写 Release Notes (可参考 DISCOVERY_RELEASE_NOTES.md)
6. 发布!

## 常见问题

### 问题: 文件被占用无法删除
**解决方案**: 
- 关闭所有正在运行的 PyMDEditor.exe
- 在任务管理器中结束 QtWebEngineProcess.exe
- 重新运行构建脚本

### 问题: 缺少 DLL 文件
**解决方案**: 
- 确保已安装所有依赖: `pip install -r requirements.txt`
- 检查 Python 版本 (需要 3.8+)

### 问题: 可执行文件无法运行
**解决方案**:
- 在 dist\PyMDEditor\ 目录下运行，不要单独复制 .exe
- 确保所有 DLL 和资源文件都在同一目录

## 文件说明

- `build_exe.spec` - PyInstaller 配置文件
- `build_windows_exe.bat` - 自动构建脚本  
- `create_windows_release.bat` - 自动打包脚本
- `dist/PyMDEditor/` - 构建输出目录
- `release/PyMD-v0.2.0-Windows/` - 最终发布包目录
- `release/PyMD-v0.2.0-Windows.zip` - 压缩的发布包

## 预期文件大小

- 可执行文件: ~250 MB (包含 PyQt6 和所有依赖)
- 压缩后: ~100 MB

这是正常的，因为包含了完整的 Python 运行时和 Qt 框架。
