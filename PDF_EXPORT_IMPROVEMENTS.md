# PDF 导出功能改进

## 问题诊断

### 1. libgobject 错误原因
- **根本原因**：旧版使用 `weasyprint` 库导出 PDF，该库依赖 GTK3 运行时环境
- **Windows 问题**：GTK3 在 Windows 上需要额外安装 `libgobject-2.0-0.dll` 等动态库
- **打包困难**：PyInstaller 难以正确打包所有 GTK 依赖，导致分发包缺失 DLL

### 2. 新的解决方案
改用 **Qt 原生 PDF 打印**，完全避免 GTK 依赖：
- 使用 `QWebEngineView.page().printToPdf()` 直接输出 PDF
- 无需任何外部库（GTK/weasyprint）
- 打包后的 exe 可独立运行，无 DLL 依赖问题

## 功能更新

### 新增功能
1. **打印预览** (Ctrl+P)
   - 显示标准打印对话框
   - 可直接打印到物理打印机
   - 可保存为 PDF 文件
   - 支持页面设置和缩放

2. **改进的 PDF 导出** (Ctrl+Shift+P)
   - 直接使用渲染后的预览页面
   - 保留完整的 CSS 样式和布局
   - 支持明/暗主题
   - 无需任何外部依赖

### 技术优势
- ✅ **零依赖**：不再需要 weasyprint 和 GTK
- ✅ **所见即所得**：PDF 输出与预览窗口完全一致
- ✅ **完美打包**：PyInstaller 能正确打包所有 Qt 组件
- ✅ **跨平台**：Windows/Linux/macOS 均可运行

## 使用方法

### 打印预览
1. 点击工具栏"打印预览"按钮，或按 `Ctrl+P`
2. 在预览窗口中调整页面设置
3. 可选择：
   - 打印到物理打印机
   - 保存为 PDF 文件

### 导出 PDF
1. 点击"导出 PDF"按钮，或按 `Ctrl+Shift+P`
2. 选择保存路径
3. 自动生成 PDF 文件

## 代码变更

### exporter.py
- 保留 `PDFExporter` 类但标记为 fallback（需要 weasyprint）
- 新增 `export_via_webengine()` 方法使用 Qt 原生打印

### app.py
- `export_pdf()` 改用 `QWebEngineView.printToPdf()`
- 新增 `print_preview()` 方法使用 `QPrintPreviewDialog`
- 添加"打印预览"菜单项和工具栏按钮

## 重新打包建议

运行 `create_distribution.bat` 重新生成发行包：
```batch
.\create_distribution.bat
```

新的发行包将：
- 不再包含 GTK 依赖
- 文件体积更小
- 启动更快
- 无 DLL 缺失问题
