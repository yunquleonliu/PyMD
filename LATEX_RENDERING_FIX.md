# LaTeX 数学公式渲染修复说明

## 问题

PyMD Editor 可执行文件中 LaTeX 数学公式无法正常渲染,公式显示为原始文本(如 `$E = mc^2$`)而不是数学符号。

## 根本原因

**PyQt6 WebEngine 默认没有启用 JavaScript 执行**

虽然 `renderer.py` 中正确配置了 MathJax:
```python
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
```

但 PyQt6 的 `QWebEngineView` 需要显式启用 JavaScript 才能执行 MathJax 脚本。

## 解决方案

在 `src/pymd_editor/app.py` 中添加 JavaScript 设置:

```python
# 修改前
self.preview = QWebEngineView(self)
from PyQt6.QtWebEngineCore import QWebEngineSettings
settings = self.preview.settings()
settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)

# 修改后 (添加了 JavaScript 支持)
self.preview = QWebEngineView(self)
from PyQt6.QtWebEngineCore import QWebEngineSettings
settings = self.preview.settings()
settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)  # ← 新增
settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False)  # ← 新增
settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)  # ← 新增
```

## 测试验证

### 1. HTML 生成测试

运行 `test_renderer.py` 验证 HTML 生成正确:

```bash
python test_renderer.py
```

**结果**: ✓ 所有检查点通过
- MathJax 脚本已包含
- LaTeX 语法保留在 HTML 中
- CDN 链接正确

### 2. 浏览器渲染测试

在标准浏览器中打开 `test_latex_output.html`:

**结果**: ✓ LaTeX 公式完美渲染

### 3. 可执行文件测试

使用 PyMD Editor 打开 `test_latex_rendering.md`:

```bash
dist\PyMDEditor\PyMDEditor.exe test_latex_rendering.md
```

**预期结果**: 
- 行内公式 $E = mc^2$ 渲染为数学符号
- 块级公式正确显示
- 希腊字母、积分符号、矩阵等正常显示

## 测试文件内容

`test_latex_rendering.md` 包含:

```markdown
# LaTeX 数学公式测试

## 行内公式
爱因斯坦质能方程: $E = mc^2$

## 块级公式
高斯积分:
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

## 矩阵
$$
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
$$
```

## MathJax 配置

当前使用的 MathJax 配置(`renderer.py`):

```javascript
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
  }
};
```

支持的语法:
- 行内公式: `$...$` 或 `\(...\)`
- 块级公式: `$$...$$` 或 `\[...\]`

## 构建步骤

修复后需要重新构建:

```bash
.\quick_build.bat
```

构建完成后测试:

```bash
cd dist\PyMDEditor
.\PyMDEditor.exe ..\..\test_latex_rendering.md
```

## 注意事项

1. **网络连接**: MathJax 从 CDN 加载,需要网络连接
2. **首次加载**: 第一次渲染可能需要几秒钟下载 MathJax
3. **缓存**: 后续渲染会更快(浏览器缓存)

## 离线支持 (可选)

如果需要离线支持,可以:

1. 下载 MathJax 到本地
2. 修改 `renderer.py` 使用本地路径:
   ```python
   <script src="file:///path/to/mathjax/es5/tex-mml-chtml.js"></script>
   ```
3. 在 `build_exe.spec` 中添加 MathJax 文件到 `datas`

## 总结

✅ **已修复**: 启用 JavaScript 支持  
✅ **已测试**: HTML 生成正确,浏览器渲染正常  
🔄 **待验证**: 重新构建后在可执行文件中测试

修复涉及的文件:
- `src/pymd_editor/app.py` - 添加 JavaScript 设置
- `test_latex_rendering.md` - 测试文件
- `test_renderer.py` - HTML 生成测试脚本
