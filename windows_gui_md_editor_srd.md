# Software Development Document: Windows GUI Markdown Editor

## 1. 项目概述

**项目名称**: PyMD Editor  

**项目目标**:  
开发一个 Windows 平台的 Markdown 编辑器，具备以下功能：
- 实时 Markdown 编辑与渲染预览
- 文件导入/导出（.md）
- 输出 PDF 和 Word（.docx）格式
- 界面友好，操作简便
- 可扩展插件或样式支持

**主要用户群**:  
- 内容创作者、技术文档编写者
- 想要在本地编辑 Markdown 并导出高质量 PDF/Word 的用户

**主要开发语言**: Python 3.11+  
**主要 GUI 框架**: PyQt6 / Tkinter（推荐 PyQt6，界面美观，跨平台可拓展）

---

## 2. 功能需求

### 2.1 编辑功能
- 文本输入区，支持 Markdown 语法高亮  
- 支持 Undo/Redo  
- 文件操作：新建、打开、保存、另存为

### 2.2 预览功能
- Markdown 渲染预览（HTML/CSS 渲染）
- 支持常用 Markdown 扩展（表格、代码块、高亮、公式等）
- 实时同步更新（编辑区修改 → 预览区即时刷新）

### 2.3 导出功能
- **PDF**：利用 `markdown → HTML → PDF` 转换流程
  - 推荐库：`weasyprint` 或 `pdfkit` + wkhtmltopdf
- **Word（.docx）**：利用 `python-docx` 将 Markdown 内容转换为 Word 文档
- 可自定义导出样式（字体、主题、页边距）

### 2.4 界面功能
- 左右或上下分屏布局：编辑区 + 预览区
- 工具栏：文件操作、导出、主题切换、字体大小
- 可选择深色/浅色模式
- 状态栏显示文件路径、字数、行数

---

## 3. 非功能需求
- **平台**: Windows 10/11（x64）
- **性能**: 预览实时刷新延迟 < 200ms
- **可维护性**: 代码模块化，便于扩展功能（插件、主题、导出格式）
- **依赖库**: 尽量选活跃、稳定、易安装的 Python 库

---

## 4. 系统架构设计

```
+------------------------------------------------------+
| GUI (PyQt6)                                         |
|  +----------------+   +------------------------+  |
|  | Markdown Editor|   | Preview Renderer       |  |
|  +----------------+   +------------------------+  |
|          |                       |                 |
|          |                       |                 |
|      File Manager ------------- Conversion Engine  |
|          |                       |                 |
|          |                       |                 |
|     Markdown Files          PDF / Word Export       |
+------------------------------------------------------+
```

### 4.1 模块划分

1. **GUI 模块**  
   - 编辑器控件、预览控件、工具栏、状态栏
2. **文件管理模块**  
   - 文件读取、写入、另存为
3. **Markdown 渲染模块**  
   - Markdown → HTML（使用 `markdown` 或 `markdown2` 库）  
   - HTML → GUI WebView 渲染
4. **导出模块**  
   - HTML → PDF  
   - Markdown → Word
5. **配置与主题模块**  
   - 保存用户偏好：主题、字体、窗口大小

---

## 5. 技术选型

| 功能 | 技术/库 | 说明 |
|------|---------|------|
| GUI | PyQt6 | 美观、可分屏、支持 WebView 渲染 |
| Markdown 转 HTML | markdown2 / markdown | 支持扩展语法 |
| HTML 渲染 | PyQt6 WebEngineView | 实时预览 Markdown |
| PDF 导出 | weasyprint / pdfkit + wkhtmltopdf | HTML 转 PDF 高质量 |
| Word 导出 | python-docx | Markdown 内容生成 .docx |
| 主题/样式 | CSS | 可选深色/浅色模式 |
| 文件操作 | Python 内置 io | 新建、打开、保存 |

---

## 6. 功能流程示意

### 6.1 打开文件流程
```
用户点击“打开” → 文件管理模块读取 .md → 编辑器显示内容 → Markdown 渲染模块同步更新预览
```

### 6.2 保存文件流程
```
用户点击“保存” → 编辑器内容写入文件 → 更新状态栏
```

### 6.3 导出 PDF/Word
```
用户点击“导出” → Markdown 渲染模块生成 HTML → PDF/Word 导出模块处理 → 文件保存
```

### 6.4 实时预览流程
```
编辑器文本变化 → Markdown 转 HTML → WebView 渲染 → 预览区更新
```

---

## 7. 用户界面设计

- **主界面**: 左编辑区，右预览区（可拖拽分割）
- **工具栏**: 新建、打开、保存、导出 PDF、导出 Word、主题切换
- **状态栏**: 显示文件路径、行数、字数
- **快捷键**: Ctrl+N, Ctrl+O, Ctrl+S, Ctrl+Shift+P (PDF), Ctrl+Shift+W (Word)

---

## 8. 扩展功能（可选）

- 支持 Markdown 扩展语法（数学公式、脚注）
- 内置主题模板
- 支持导出带目录 PDF
- 可通过插件添加导出格式或渲染方式

---

## 9. 开发计划（建议迭代）

1. **MVP 版本**  
   - 编辑 + 实时预览 + 打开/保存 .md
2. **基础导出版本**  
   - PDF/Word 导出
3. **界面优化版本**  
   - 主题、工具栏、状态栏
4. **扩展功能版本**  
   - Markdown 扩展语法、插件系统

---

## 10. 测试计划

- **功能测试**: 文件打开/保存、导出 PDF/Word、实时预览
- **性能测试**: 大文件渲染、延迟测试
- **用户体验测试**: 界面布局、快捷键、主题切换
- **边界测试**: 空文件、超大文件、特殊字符

---

## 11. 参考库链接

- PyQt6: https://pypi.org/project/PyQt6/  
- markdown2: https://pypi.org/project/markdown2/  
- weasyprint: https://weasyprint.org/  
- python-docx: https://python-docx.readthedocs.io/  
- pdfkit: https://pypi.org/project/pdfkit/  

---

*文档完成：Windows GUI Markdown 编辑器软件开发说明书*

