# WYSIWYG功能实现原理总结（200字）

## 核心技术路径

**WYSIWYG编辑器采用基于HTML的实现方案**，通过PyQt6的QWebEngineView组件作为载体。具体流程如下：

1. **HTML渲染基础**：使用MarkdownRenderer将Markdown文本转换为HTML，在WebView中展示渲染效果

2. **可编辑激活**：通过JavaScript设置DOM元素的`contentEditable=true`属性，使HTML内容变为可直接编辑状态

3. **实时监听机制**：绑定`input`、`paste`、`keyup`等DOM事件，当用户修改内容时触发变化检测

4. **双向同步转换**：
   - 用户编辑时：HTML内容 → HTMLToMarkdownConverter → Markdown文本
   - 内容更新时：Markdown文本 → MarkdownRenderer → HTML显示

5. **智能解析器**：自定义HTMLParser解析器，精确识别HTML结构（标题、粗体、链接、代码块等），转换为对应Markdown语法

6. **防抖优化**：300ms延时机制避免频繁转换，确保编辑流畅性

**核心优势**：真正在渲染结果上编辑，保持视觉一致性；智能转换器确保Markdown语义准确性；JavaScript与Python协同实现高效的编辑体验。这种HTML-based方案既实现了所见即所得，又保持了Markdown格式的严谨性。