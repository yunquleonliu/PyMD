# 🚀 PyMD Editor 快速启动指南

## 立即开始！（3种方法）

### 🥇 方法 1：拖拽打开（零配置，最简单！）

**一次性准备**（30秒）：
```
1. 右键 run_editor.bat
2. 发送到 → 桌面快捷方式
3. （可选）重命名快捷方式为"PyMD Editor"
```

**以后每次使用**：
```
拖拽任意 .md 文件到桌面快捷方式图标 → 自动打开编辑
```

✅ **优点**：无需任何配置，零权限要求

---

### 🥈 方法 2：双击运行

**直接启动编辑器**：
```
双击: run_editor.bat
```

然后在编辑器中 `Ctrl+O` 打开文件。

---

### 🥉 方法 3：右键关联（一次设置）

**设置步骤**：
```
1. 右键任意 .md 文件
2. 打开方式 → 选择其他应用
3. 浏览并选择 run_editor.bat
4. ☑️ 勾选"始终使用此应用打开 .md 文件"
5. 确定
```

**以后使用**：
```
双击任意 .md 文件 → 自动用 PyMD Editor 打开
```

---

## 第一次使用？

### 1. 打开示例文档
启动编辑器后：
- 点击工具栏 **"打开"** 按钮
- 选择 `EXAMPLE.md` 文件
- 在右侧查看实时预览效果

### 2. 试试这些功能

#### 编辑 Markdown
- 在左侧编辑区输入 Markdown 文本
- 右侧会自动显示渲染效果
- 支持：标题、列表、代码块、表格、任务列表等

#### 保存文档
- `Ctrl+S` - 保存当前文件
- `Ctrl+Shift+S` - 另存为新文件

#### 切换主题
- `Ctrl+T` - 在浅色/深色主题之间切换
- 预览区会同步更新样式

#### 导出文档
- `Ctrl+Shift+W` - 导出为 Word (.docx)
- `Ctrl+Shift+P` - 导出为 PDF（需先安装 weasyprint）

---

## 导出 PDF 功能设置

Word 导出已经可用！如果需要 PDF 导出：

```powershell
# 在项目根目录运行
& ".venv\Scripts\pip.exe" install weasyprint
```

> **提示**: Windows 上 weasyprint 可能需要额外的系统依赖。如果安装失败，可以只使用 Word 导出功能。

---

## 常见问题

### Q: 双击启动脚本没反应？
**A**: 右键点击 `run_editor.bat`，选择"以管理员身份运行"。

### Q: 出现 ModuleNotFoundError？
**A**: 确保虚拟环境已激活。使用启动脚本会自动处理。

### Q: 如何更新依赖？
**A**: 
```powershell
& ".venv\Scripts\pip.exe" install --upgrade PyQt6 markdown2 python-docx
```

### Q: 可以在其他文件夹打开 .md 文件吗？
**A**: 当然！使用 `Ctrl+O` 可以打开任意位置的 Markdown 文件。

---

## 快捷键速查表

| 功能 | 快捷键 |
|------|--------|
| 新建 | `Ctrl+N` |
| 打开 | `Ctrl+O` |
| 保存 | `Ctrl+S` |
| 另存为 | `Ctrl+Shift+S` |
| 导出 PDF | `Ctrl+Shift+P` |
| 导出 Word | `Ctrl+Shift+W` |
| 切换主题 | `Ctrl+T` |
| 撤销 | `Ctrl+Z` |
| 重做 | `Ctrl+Y` |

---

## 技术支持

- 📖 完整文档: 查看 `README.md`
- 📋 项目总结: 查看 `PROJECT_SUMMARY.md`
- 📝 示例文档: 打开 `EXAMPLE.md`

---

**享受写作吧！ 🎉**
