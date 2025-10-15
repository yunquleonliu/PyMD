# 图片渲染测试文档

## 测试各种图片格式

### 1. 在线图片测试
这是一个在线图片示例：

![Online Image](https://via.placeholder.com/400x200/0066cc/ffffff?text=Online+Image+Test)

### 2. 本地图片测试
如果你有本地图片，可以测试以下格式：

```markdown
![本地图片](./images/example.png)
![绝对路径](C:/Users/Example/Pictures/photo.jpg)
![相对路径](../assets/logo.svg)
```

### 3. 图片格式说明

支持的图片格式：
- **PNG**: `![PNG图片](image.png)`
- **JPG/JPEG**: `![JPG图片](photo.jpg)` 
- **GIF**: `![动图](animation.gif)`
- **SVG**: `![矢量图](icon.svg)`
- **BMP**: `![BMP图片](bitmap.bmp)`

### 4. 图片样式特性

渲染器现在支持：
- ✅ **响应式设计**: 图片自动适应容器宽度
- ✅ **圆角效果**: 8px圆角边框
- ✅ **阴影效果**: 柔和的阴影增强视觉效果
- ✅ **居中显示**: 图片自动居中对齐
- ✅ **暗色模式**: 不同主题下的优化显示

### 5. 使用技巧

#### 插入图片的几种方式:
1. **快捷键**: `Ctrl+Shift+I`
2. **菜单**: File → 插入图片
3. **工具栏**: 点击图片图标
4. **AI面板**: 点击 🖼️ Insert Image 按钮

#### 最佳实践:
- 使用描述性的alt文本
- 选择适当的图片格式（PNG用于截图，JPG用于照片）
- 考虑文件大小，避免过大的图片影响加载速度

### 6. 路径解析说明

渲染器会智能处理不同类型的图片路径：

| 路径类型 | 示例 | 处理方式 |
|---------|------|---------|
| 在线URL | `https://example.com/image.png` | 直接使用 |
| 绝对路径 | `C:\Pictures\photo.jpg` | 转换为file://URL |
| 相对路径 | `./images/logo.png` | 基于当前文档路径解析 |
| Data URL | `data:image/png;base64,...` | 直接使用 |

---

**测试方法**: 
1. 保存此文档
2. 使用图片插入功能添加本地图片
3. 查看预览面板中的渲染效果
4. 测试不同主题下的显示效果

享受增强的图片渲染体验！ 🖼️✨