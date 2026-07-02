# PyMD Editor - 可执行文件位置统一说明

## 问题分析

### 1. 可执行文件在哪里?

之前的构建配置导致每次生成的可执行文件位置不一致:

- **旧位置(带版本号)**: `dist\PyMDEditor_v0.2.0\PyMDEditor.exe`
- **新位置(固定)**: `dist\PyMDEditor\PyMDEditor.exe`

问题根源:
- `build_exe.spec` 文件中的 `COLLECT` 配置使用了 `name='PyMDEditor_v0.2.0'`
- 导致输出目录名包含版本号,每次版本更新都会创建新目录

### 2. 为什么有些版本不能运行?

**关键原因**: 缺少 `python313.dll`

- PyInstaller 在 Python 3.13 下不会自动包含 `python313.dll`
- 没有这个 DLL 文件,可执行文件启动时会报错:
  ```
  Failed to load Python DLL 'python313.dll'
  ```

## 解决方案

### 已完成的修改

1. **统一输出位置**
   - 修改 `build_exe.spec`:
     ```python
     coll = COLLECT(
         ...
         name='PyMDEditor',  # 不再使用版本号
     )
     ```
   - 以后所有构建都输出到: `dist\PyMDEditor\`

2. **自动包含 python313.dll**
   - 在 `build_exe.spec` 中添加:
     ```python
     python_dll = r'D:\InstalledTools\Python313\python313.dll'
     a.binaries += [(os.path.basename(python_dll), python_dll, 'BINARY')]
     ```
   - 构建后自动复制到 dist 目录

3. **完整构建流程**
   - 创建了 `rebuild_unified.bat` 脚本
   - 包含清理、构建、复制 DLL、打包、测试等完整步骤

### 下一步操作

运行统一构建脚本:

```batch
.\rebuild_unified.bat
```

这个脚本会:
1. 清理所有旧的构建文件
2. 重新构建到固定位置 `dist\PyMDEditor\`
3. 确保包含 `python313.dll`
4. 创建 release 包
5. 生成 ZIP 压缩包
6. 自动测试可执行文件

## 固定位置总结

### 开发时使用
- **可执行文件**: `dist\PyMDEditor\PyMDEditor.exe`
- **包含所有依赖**: `dist\PyMDEditor\` 目录下的所有文件
- **必须文件**: `python313.dll` (已自动包含)

### 发布时使用
- **Release 包**: `release\PyMD-v0.2.0-Windows\`
- **ZIP 归档**: `release\PyMD-v0.2.0-Windows.zip`
- **上传到 GitHub Release**: 使用 ZIP 文件

## 快速测试

直接运行可执行文件:

```powershell
cd "dist\PyMDEditor"
.\PyMDEditor.exe
```

## 注意事项

1. **Python 版本**: 确保使用 Python 3.13.1
2. **DLL 位置**: `D:\InstalledTools\Python313\python313.dll` 必须存在
3. **输出目录**: 永远是 `dist\PyMDEditor\` (不再有版本号)
4. **每次构建**: 旧文件会被自动清理并重新生成

## 构建要求

- PyInstaller 6.16.0
- PyQt6 6.6.0
- Python 3.13.1
- Windows 11

## 文件结构

```
PyMD/
├── build_exe.spec          # PyInstaller 配置(已修改)
├── rebuild_unified.bat     # 统一构建脚本(推荐使用)
├── fix_build_and_package.bat  # 旧的构建脚本(已更新)
├── dist/
│   └── PyMDEditor/         # 固定输出位置 ✓
│       ├── PyMDEditor.exe
│       ├── python313.dll   # 必须包含 ✓
│       └── ... (其他依赖文件)
└── release/
    ├── PyMD-v0.2.0-Windows/
    └── PyMD-v0.2.0-Windows.zip
```

## 问题排查

### 如果可执行文件不运行

1. 检查 `python313.dll` 是否存在:
   ```powershell
   Test-Path "dist\PyMDEditor\python313.dll"
   ```

2. 如果不存在,手动复制:
   ```powershell
   Copy-Item "D:\InstalledTools\Python313\python313.dll" -Destination "dist\PyMDEditor\" -Force
   ```

3. 重新测试:
   ```powershell
   cd "dist\PyMDEditor"
   .\PyMDEditor.exe
   ```

### 如果构建失败

1. 清理构建缓存:
   ```powershell
   Remove-Item -Recurse -Force dist, build
   ```

2. 重新运行构建:
   ```batch
   .\rebuild_unified.bat
   ```

## 总结

✅ **统一位置**: `dist\PyMDEditor\` (固定不变)  
✅ **自动包含 DLL**: 构建脚本自动处理  
✅ **一键构建**: 运行 `rebuild_unified.bat`  
✅ **易于测试**: 直接运行 `dist\PyMDEditor\PyMDEditor.exe`  
✅ **易于发布**: 使用 `release\PyMD-v0.2.0-Windows.zip`
