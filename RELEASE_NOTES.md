# Release Notes

## v2.2.0 (Latest)

### 🚀 Features
- **AI Chat Integration**: Added AI-powered chat functionality for enhanced editing experience
- **WYSIWYG AI Features**: Optional AI-assisted WYSIWYG editing capabilities
- **Image Insertion Support**: Enhanced image handling with drag-drop and insertion features
- **Three-Column Layout**: Improved user interface with three-column design

### 🐛 Fixes
- **Markdown Image Rendering**: Normalized and fixed image rendering issues
- **Drag-Drop Errors**: Resolved errors when dragging and dropping images
- **Preview Image Loading**: Fixed image rendering in preview with WebEngine settings
- **Runtime Errors**: Fixed various runtime errors and script issues

### 📚 Documentation
- **README Update**: Updated README highlighting AI, WYSIWYG, and Export features
- **Chinese Image Guide**: Added usage guide for images in Chinese
- **Requirements Improvement**: Enhanced requirements.txt with better organization

### 🔧 Other
- **Git Ignore**: Added comprehensive .gitignore to exclude build artifacts and cache files

### 📦 Distribution
- Windows executable available in releases
- Includes all necessary dependencies for standalone operation

### 🔗 Links
- [GitHub Repository](https://github.com/yunquleonliu/PyMD)
- [Issues](https://github.com/yunquleonliu/PyMD/issues)
- [Discussions](https://github.com/yunquleonliu/PyMD/discussions)

---

## v0.2.0 (merged from RELEASE_NOTES_v0.2.0.md)

# PyMD Editor v0.2.0 - 增强 AI 聊天界面

[English](#english-version) | [中文](#chinese-version)

---

## <a name="chinese-version"></a>中文版本

### 🎯 主要更新

#### ✨ 全新 AI 聊天界面
- 现代化聊天气泡设计，带有渐变背景效果
- 实时消息传递与打字指示器
- 自动保存和加载聊天历史
- 流畅的动画效果

#### 🤖 多 AI 提供商支持
- Personal AI
- Google Gemini
- OpenAI
- Anthropic Claude
- 可在设置中快速切换 AI 提供商

#### 🎨 界面优化
- 响应式三栏布局
- 渐变主题设计
- 现代化 UI 风格
- 优化的空间利用率

#### 📝 编辑功能
- 实时 Markdown 预览
- 富文本编辑支持
- 图片拖放插入
- 导出为 DOCX 和 HTML

### 💻 系统要求

- **Windows**: Windows 10 或更高版本
- **无需安装 Python** - 独立可执行文件
- **推荐配置**: 4GB RAM, 600MB 磁盘空间

### 📥 安装使用

#### Windows 用户
1. 下载 `PyMD-v0.2.0-Windows.zip`
2. 解压到任意目录
3. 双击 `Launch PyMD Editor.bat` 或 `PyMDEditor.exe` 启动

#### Python 用户
1. 克隆仓库
2. 安装依赖: `pip install -r requirements.txt`
3. 运行: `python src/pymd_editor/main.py`

### 🚀 快速开始

1. 启动 PyMD Editor
2. 创建或打开 Markdown 文件
3. 在右侧 AI 聊天面板输入问题
4. 获取 AI 辅助写作建议

### 📊 发布信息

- **版本**: v0.2.0-chat-enhancement
- **发布日期**: 2025-11-09
- **包大小**: 206 MB (Windows 可执行文件)
- **包含文件**: 1,774 个

### 🔗 相关链接

- **仓库**: https://github.com/yunquleonliu/PyMD
- **Issues**: https://github.com/yunquleonliu/PyMD/issues
- **文档**: 查看项目中的 QUICKSTART.md

### 🙏 致谢

感谢所有使用和支持 PyMD Editor 的用户！

---

## <a name="english-version"></a>English Version

### 🎯 Key Features

#### ✨ Brand New AI Chat Interface
- Modern chat bubble design with gradient backgrounds
- Real-time messaging with typing indicators
- Auto-save and load chat history
- Smooth animations and transitions

#### 🤖 Multiple AI Provider Support
- Personal AI
- Google Gemini
- OpenAI
- Anthropic Claude
- Quick provider switching in settings

#### 🎨 UI Improvements
- Responsive three-column layout
- Gradient theme design
- Modern UI styling
- Optimized space utilization

#### 📝 Editing Features
- Real-time Markdown preview
- Rich text editing support
- Drag-and-drop image insertion
- Export to DOCX and HTML

### 💻 System Requirements

- **Windows**: Windows 10 or later
- **No Python Installation Required** - Standalone executable
- **Recommended**: 4GB RAM, 600MB disk space

### 📥 Installation

#### Windows Users
1. Download `PyMD-v0.2.0-Windows.zip`
2. Extract to any directory
3. Double-click `Launch PyMD Editor.bat` or `PyMDEditor.exe` to start

#### Python Users
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python src/pymd_editor/main.py`

### 🚀 Quick Start

1. Launch PyMD Editor
2. Create or open a Markdown file
3. Type your question in the AI chat panel on the right
4. Get AI-assisted writing suggestions

### 📊 Release Information

- **Version**: v0.2.0-chat-enhancement
- **Release Date**: November 9, 2025
- **Package Size**: 206 MB (Windows executable)
- **Files Included**: 1,774 files

### 🔗 Links

- **Repository**: https://github.com/yunquleonliu/PyMD
- **Issues**: https://github.com/yunquleonliu/PyMD/issues
- **Documentation**: See QUICKSTART.md in the project

### 🙏 Acknowledgments

Thank you to all users who support PyMD Editor!

---

**Enjoy your AI-enhanced Markdown editing experience!** 🎉


---

## Discovery Release (merged from DISCOVERY_RELEASE_NOTES.md)

# 🚀 PyMD Editor - Discovery Release v0.1.0

## 📋 Release Overview

**Release Date**: November 9, 2025  
**Version**: v0.1.0-discovery  
**Status**: Experimental Discovery Release  

## 🎯 Major Features

### ✨ Complete Chat System
- **Modern Chat Bubbles**: Gradient-based UI with user/AI message differentiation
- **Typing Indicators**: Smooth animations showing AI processing status
- **Message Persistence**: Automatic saving/loading of conversation history
- **Real-time Input**: Return key support for instant message sending
- **Session Management**: JSON-based conversation storage

### 🤖 AI Assistant Integration
- **Provider Router**: VSCode-style AI provider management system
- **Multiple AI Services**: Support for Personal AI, Gemini, OpenAI, Claude
- **Settings Dialog**: Comprehensive AI configuration interface
- **Dynamic Switching**: Runtime AI provider selection

### 🎨 Modern UI Design
- **Gradient Backgrounds**: Contemporary visual design language
- **Responsive Layout**: Optimized space usage in three-column layout
- **Consistent Styling**: Unified color scheme and component design
- **Professional Appearance**: Clean, modern interface

### 📝 Enhanced Markdown Editing
- **Live Preview**: Real-time markdown rendering
- **Syntax Highlighting**: Code block highlighting
- **Image Support**: Drag-and-drop image insertion
- **Export Capabilities**: Multiple output formats

## 🔧 Technical Improvements

### Code Quality
- **Modular Architecture**: Clean separation of chat, AI, and UI components
- **Error Handling**: Robust exception handling and user feedback
- **Qt Compatibility**: Fixed CSS compatibility issues for PyQt6
- **Cross-platform**: Windows/macOS/Linux support

### Performance
- **Efficient Rendering**: Optimized UI component updates
- **Memory Management**: Proper cleanup of resources
- **Responsive Interactions**: Smooth user interactions

## 🐛 Bug Fixes

- Fixed CSS `box-shadow` compatibility issues
- Resolved dialog inheritance problems (QWidget → QDialog)
- Cleaned up duplicate code and imports
- Fixed chat bubble border rendering issues

## 📦 Files Changed

### New Files
- `src/pymd_editor/chat_components.py` - Complete chat system
- `CHAT_ENHANCEMENT_PLAN.md` - Development planning document
- `DESIGN_SYSTEM.md` - UI design guidelines
- `data/chat_history.json` - Conversation persistence

### Modified Files
- `src/pymd_editor/three_column_layout.py` - AI assistant panel
- `src/pymd_editor/ai_settings.py` - AI provider management
- `src/pymd_editor/app.py` - Main application integration
- `src/pymd_editor/main.py` - Entry point improvements
- `src/pymd_editor/renderer.py` - HTML/CSS rendering fixes
- `src/pymd_editor/wysiwyg_editor.py` - Rich text editor updates

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/yunquleonliu/PyMD.git
cd PyMD

# Checkout discovery release
git checkout v0.1.0-discovery

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/pymd_editor/main.py
```

## 🔮 Future Plans

This discovery release serves as a foundation for:
- Advanced AI features and integrations
- Plugin system for extensibility
- Cloud synchronization
- Collaborative editing
- Mobile app versions

## 📞 Feedback

This is an experimental release. Please report any issues or suggestions via:
- GitHub Issues: [PyMD Issues](https://github.com/yunquleonliu/PyMD/issues)
- Feature Requests: [PyMD Discussions](https://github.com/yunquleonliu/PyMD/discussions)

---

**Note**: This discovery release includes experimental features and may contain bugs. Use at your own discretion for testing and feedback purposes.


---

## v1.1.0 Changelog (merged from CHANGELOG_v1.1.0.md)

# PyMD Editor - 更新日志 v1.1.0

## 🎉 新增功能

### 1. 多语言支持
- ✅ **语言菜单**：新增中文/English切换选项
- ✅ **完整本地化**：菜单栏、工具栏、按钮文字全面支持双语
- ✅ **动态切换**：运行时即时切换界面语言，无需重启

**功能位置**：菜单栏 → 语言 → 中文/English

### 2. WYSIWYG模式优化
- ✅ **纯编辑模式**：WYSIWYG标签页现在是纯编辑器，不再有预览/编辑切换
- ✅ **始终可编辑**：打开WYSIWYG标签页即自动进入编辑状态
- ✅ **优化工具栏**：美化格式化按钮，添加Unicode符号和样式
- ✅ **状态指示**：清晰显示当前为WYSIWYG编辑模式

**设计理念**：传统模式已有预览功能，WYSIWYG专注于直接编辑体验

### 3. 界面改进
- ✅ **菜单栏完善**：添加标准的文件/视图/语言菜单结构
- ✅ **按钮美化**：格式化按钮使用特殊Unicode字符和样式
- ✅ **用户体验**：更直观的编辑状态提示

## 🔧 技术实现

### 语言系统架构
```python
def _get_text(self, key: str) -> str:
    """多语言文本获取系统"""
    
def set_language(self, lang: str):
    """动态语言切换"""
    
def _update_ui_texts(self):
    """界面文字实时更新"""
```

### WYSIWYG优化
- **移除模式切换**：简化为纯编辑模式
- **自动激活编辑**：`contentEditable=true`自动设置
- **工具栏优化**：专业的格式化按钮设计

## 📋 支持的语言元素

| 界面元素 | 中文 | English |
|---------|------|---------|
| 文件菜单 | 文件 | File |
| 视图菜单 | 视图 | View |
| 语言菜单 | 语言 | Language |
| 传统模式 | 传统模式 | Traditional Mode |
| WYSIWYG | WYSIWYG 编辑 | WYSIWYG Editor |
| 新建 | 新建 | New |
| 打开 | 打开 | Open |
| 保存 | 保存 | Save |
| 另存为 | 另存为 | Save As |

## 🎯 用户体验提升

### 使用流程优化
1. **语言选择**：菜单栏 → 语言 → 选择中文或English
2. **WYSIWYG编辑**：直接点击"WYSIWYG编辑"标签页开始编辑
3. **格式化操作**：使用美化后的工具栏按钮（𝐁 𝐼 𝐇 🔗）

### 界面更加专业
- **标准菜单栏**：符合桌面应用程序标准
- **双语支持**：国际化用户友好
- **专用编辑器**：WYSIWYG专注编辑，传统模式专注预览

## 📁 文件变更

### 修改的文件
- `src/pymd_editor/app.py` - 添加语言系统和菜单栏
- `src/pymd_editor/wysiwyg_editor.py` - 优化为纯编辑模式

### 新增的文件
- `WYSIWYG_IMPLEMENTATION_CN.md` - 中文实现原理总结

## 🚀 启动方式

```bash
cd "c:\Users\Leon Liu\Desktop\PyMD"
python -m src.pymd_editor.main
```

## 💡 下一步计划

- 添加更多语言支持（日语、法语等）
- 增强WYSIWYG格式化功能（表格编辑、图片插入）
- 优化大文档编辑性能
- 添加自定义快捷键支持

---

**版本**：v1.1.0  
**发布时间**：2025年10月15日  
**兼容性**：保持向后兼容，现有功能不受影响


---

## v0.2.0

# PyMD Editor v0.2.0 - 增强 AI 聊天界面

[English](#english-version) | [中文](#chinese-version)

---

## <a name="chinese-version"></a>中文版本

### 🎯 主要更新

#### ✨ 全新 AI 聊天界面
- 现代化聊天气泡设计，带有渐变背景效果
- 实时消息传递与打字指示器
- 自动保存和加载聊天历史
- 流畅的动画效果

#### 🤖 多 AI 提供商支持
- Personal AI
- Google Gemini
- OpenAI
- Anthropic Claude
- 可在设置中快速切换 AI 提供商

#### 🎨 界面优化
- 响应式三栏布局
- 渐变主题设计
- 现代化 UI 风格
- 优化的空间利用率

#### 📝 编辑功能
- 实时 Markdown 预览
- 富文本编辑支持
- 图片拖放插入
- 导出为 DOCX 和 HTML

### 💻 系统要求

- **Windows**: Windows 10 或更高版本
- **无需安装 Python** - 独立可执行文件
- **推荐配置**: 4GB RAM, 600MB 磁盘空间

### 📥 安装使用

#### Windows 用户
1. 下载 `PyMD-v0.2.0-Windows.zip`
2. 解压到任意目录
3. 双击 `Launch PyMD Editor.bat` 或 `PyMDEditor.exe` 启动

#### Python 用户
1. 克隆仓库
2. 安装依赖: `pip install -r requirements.txt`
3. 运行: `python src/pymd_editor/main.py`

### 🚀 快速开始

1. 启动 PyMD Editor
2. 创建或打开 Markdown 文件
3. 在右侧 AI 聊天面板输入问题
4. 获取 AI 辅助写作建议

### 📊 发布信息

- **版本**: v0.2.0-chat-enhancement
- **发布日期**: 2025-11-09
- **包大小**: 206 MB (Windows 可执行文件)
- **包含文件**: 1,774 个

### 🔗 相关链接

- **仓库**: https://github.com/yunquleonliu/PyMD
- **Issues**: https://github.com/yunquleonliu/PyMD/issues
- **文档**: 查看项目中的 QUICKSTART.md

### 🙏 致谢

感谢所有使用和支持 PyMD Editor 的用户！

---

## <a name="english-version"></a>English Version

### 🎯 Key Features

#### ✨ Brand New AI Chat Interface
- Modern chat bubble design with gradient backgrounds
- Real-time messaging with typing indicators
- Auto-save and load chat history
- Smooth animations and transitions

#### 🤖 Multiple AI Provider Support
- Personal AI
- Google Gemini
- OpenAI
- Anthropic Claude
- Quick provider switching in settings

#### 🎨 UI Improvements
- Responsive three-column layout
- Gradient theme design
- Modern UI styling
- Optimized space utilization

#### 📝 Editing Features
- Real-time Markdown preview
- Rich text editing support
- Drag-and-drop image insertion
- Export to DOCX and HTML

### 💻 System Requirements

- **Windows**: Windows 10 or later
- **No Python Installation Required** - Standalone executable
- **Recommended**: 4GB RAM, 600MB disk space

### 📥 Installation

#### Windows Users
1. Download `PyMD-v0.2.0-Windows.zip`
2. Extract to any directory
3. Double-click `Launch PyMD Editor.bat` or `PyMDEditor.exe` to start

#### Python Users
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python src/pymd_editor/main.py`

### 🚀 Quick Start

1. Launch PyMD Editor
2. Create or open a Markdown file
3. Type your question in the AI chat panel on the right
4. Get AI-assisted writing suggestions

### 📊 Release Information

- **Version**: v0.2.0-chat-enhancement
- **Release Date**: November 9, 2025
- **Package Size**: 206 MB (Windows executable)
- **Files Included**: 1,774 files

### 🔗 Links

- **Repository**: https://github.com/yunquleonliu/PyMD
- **Issues**: https://github.com/yunquleonliu/PyMD/issues
- **Documentation**: See QUICKSTART.md in the project

### 🙏 Acknowledgments

Thank you to all users who support PyMD Editor!

---

**Enjoy your AI-enhanced Markdown editing experience!** 🎉


---

## Discovery Release

# 🚀 PyMD Editor - Discovery Release v0.1.0

## 📋 Release Overview

**Release Date**: November 9, 2025  
**Version**: v0.1.0-discovery  
**Status**: Experimental Discovery Release  

## 🎯 Major Features

### ✨ Complete Chat System
- **Modern Chat Bubbles**: Gradient-based UI with user/AI message differentiation
- **Typing Indicators**: Smooth animations showing AI processing status
- **Message Persistence**: Automatic saving/loading of conversation history
- **Real-time Input**: Return key support for instant message sending
- **Session Management**: JSON-based conversation storage

### 🤖 AI Assistant Integration
- **Provider Router**: VSCode-style AI provider management system
- **Multiple AI Services**: Support for Personal AI, Gemini, OpenAI, Claude
- **Settings Dialog**: Comprehensive AI configuration interface
- **Dynamic Switching**: Runtime AI provider selection

### 🎨 Modern UI Design
- **Gradient Backgrounds**: Contemporary visual design language
- **Responsive Layout**: Optimized space usage in three-column layout
- **Consistent Styling**: Unified color scheme and component design
- **Professional Appearance**: Clean, modern interface

### 📝 Enhanced Markdown Editing
- **Live Preview**: Real-time markdown rendering
- **Syntax Highlighting**: Code block highlighting
- **Image Support**: Drag-and-drop image insertion
- **Export Capabilities**: Multiple output formats

## 🔧 Technical Improvements

### Code Quality
- **Modular Architecture**: Clean separation of chat, AI, and UI components
- **Error Handling**: Robust exception handling and user feedback
- **Qt Compatibility**: Fixed CSS compatibility issues for PyQt6
- **Cross-platform**: Windows/macOS/Linux support

### Performance
- **Efficient Rendering**: Optimized UI component updates
- **Memory Management**: Proper cleanup of resources
- **Responsive Interactions**: Smooth user interactions

## 🐛 Bug Fixes

- Fixed CSS `box-shadow` compatibility issues
- Resolved dialog inheritance problems (QWidget → QDialog)
- Cleaned up duplicate code and imports
- Fixed chat bubble border rendering issues

## 📦 Files Changed

### New Files
- `src/pymd_editor/chat_components.py` - Complete chat system
- `CHAT_ENHANCEMENT_PLAN.md` - Development planning document
- `DESIGN_SYSTEM.md` - UI design guidelines
- `data/chat_history.json` - Conversation persistence

### Modified Files
- `src/pymd_editor/three_column_layout.py` - AI assistant panel
- `src/pymd_editor/ai_settings.py` - AI provider management
- `src/pymd_editor/app.py` - Main application integration
- `src/pymd_editor/main.py` - Entry point improvements
- `src/pymd_editor/renderer.py` - HTML/CSS rendering fixes
- `src/pymd_editor/wysiwyg_editor.py` - Rich text editor updates

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/yunquleonliu/PyMD.git
cd PyMD

# Checkout discovery release
git checkout v0.1.0-discovery

# Install dependencies
pip install -r requirements.txt

# Run the application
python src/pymd_editor/main.py
```

## 🔮 Future Plans

This discovery release serves as a foundation for:
- Advanced AI features and integrations
- Plugin system for extensibility
- Cloud synchronization
- Collaborative editing
- Mobile app versions

## 📞 Feedback

This is an experimental release. Please report any issues or suggestions via:
- GitHub Issues: [PyMD Issues](https://github.com/yunquleonliu/PyMD/issues)
- Feature Requests: [PyMD Discussions](https://github.com/yunquleonliu/PyMD/discussions)

---

**Note**: This discovery release includes experimental features and may contain bugs. Use at your own discretion for testing and feedback purposes.


---

## v1.1.0 Changelog

# PyMD Editor - 更新日志 v1.1.0

## 🎉 新增功能

### 1. 多语言支持
- ✅ **语言菜单**：新增中文/English切换选项
- ✅ **完整本地化**：菜单栏、工具栏、按钮文字全面支持双语
- ✅ **动态切换**：运行时即时切换界面语言，无需重启

**功能位置**：菜单栏 → 语言 → 中文/English

### 2. WYSIWYG模式优化
- ✅ **纯编辑模式**：WYSIWYG标签页现在是纯编辑器，不再有预览/编辑切换
- ✅ **始终可编辑**：打开WYSIWYG标签页即自动进入编辑状态
- ✅ **优化工具栏**：美化格式化按钮，添加Unicode符号和样式
- ✅ **状态指示**：清晰显示当前为WYSIWYG编辑模式

**设计理念**：传统模式已有预览功能，WYSIWYG专注于直接编辑体验

### 3. 界面改进
- ✅ **菜单栏完善**：添加标准的文件/视图/语言菜单结构
- ✅ **按钮美化**：格式化按钮使用特殊Unicode字符和样式
- ✅ **用户体验**：更直观的编辑状态提示

## 🔧 技术实现

### 语言系统架构
```python
def _get_text(self, key: str) -> str:
    """多语言文本获取系统"""
    
def set_language(self, lang: str):
    """动态语言切换"""
    
def _update_ui_texts(self):
    """界面文字实时更新"""
```

### WYSIWYG优化
- **移除模式切换**：简化为纯编辑模式
- **自动激活编辑**：`contentEditable=true`自动设置
- **工具栏优化**：专业的格式化按钮设计

## 📋 支持的语言元素

| 界面元素 | 中文 | English |
|---------|------|---------|
| 文件菜单 | 文件 | File |
| 视图菜单 | 视图 | View |
| 语言菜单 | 语言 | Language |
| 传统模式 | 传统模式 | Traditional Mode |
| WYSIWYG | WYSIWYG 编辑 | WYSIWYG Editor |
| 新建 | 新建 | New |
| 打开 | 打开 | Open |
| 保存 | 保存 | Save |
| 另存为 | 另存为 | Save As |

## 🎯 用户体验提升

### 使用流程优化
1. **语言选择**：菜单栏 → 语言 → 选择中文或English
2. **WYSIWYG编辑**：直接点击"WYSIWYG编辑"标签页开始编辑
3. **格式化操作**：使用美化后的工具栏按钮（𝐁 𝐼 𝐇 🔗）

### 界面更加专业
- **标准菜单栏**：符合桌面应用程序标准
- **双语支持**：国际化用户友好
- **专用编辑器**：WYSIWYG专注编辑，传统模式专注预览

## 📁 文件变更

### 修改的文件
- `src/pymd_editor/app.py` - 添加语言系统和菜单栏
- `src/pymd_editor/wysiwyg_editor.py` - 优化为纯编辑模式

### 新增的文件
- `WYSIWYG_IMPLEMENTATION_CN.md` - 中文实现原理总结

## 🚀 启动方式

```bash
cd "c:\Users\Leon Liu\Desktop\PyMD"
python -m src.pymd_editor.main
```

## 💡 下一步计划

- 添加更多语言支持（日语、法语等）
- 增强WYSIWYG格式化功能（表格编辑、图片插入）
- 优化大文档编辑性能
- 添加自定义快捷键支持

---

**版本**：v1.1.0  
**发布时间**：2025年10月15日  
**兼容性**：保持向后兼容，现有功能不受影响