from __future__ import annotations

import markdown2
import os
import re
from pathlib import Path
from urllib.parse import urlparse


class MarkdownRenderer:
    def __init__(self):
        # Enable common extras for better Markdown support
        self._extras = [
            "fenced-code-blocks",
            "tables",
            "strike",
            "task_list",
            "code-friendly",
            "toc",
        ]

    def to_html(self, text: str, dark: bool = False, base_path: str = None) -> str:
        # Process images to handle local paths
        processed_text = self._process_images(text or "", base_path)
        
        html_body = markdown2.markdown(processed_text, extras=self._extras)
        css = DARK_CSS if dark else LIGHT_CSS
        return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset=\"utf-8\" />
<style>
{css}
</style>
<!-- MathJax for LaTeX math rendering -->
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true,
    processEnvironments: true
  }},
  options: {{
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
  }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
</head>
<body>
<div class=\"content\">{html_body}</div>
</body>
</html>
"""

    def _process_images(self, text: str, base_path: str = None) -> str:
        """Process image paths to handle local files and relative paths"""
        if not text:
            return text
            
        # Pattern to match markdown images: ![alt](src)
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        
        def replace_image(match):
            alt_text = match.group(1)
            src = match.group(2)
            
            # Handle different types of image sources
            processed_src = self._resolve_image_path(src, base_path)
            
            return f'![{alt_text}]({processed_src})'
        
        return re.sub(image_pattern, replace_image, text)
    
    def _resolve_image_path(self, src: str, base_path: str = None) -> str:
        """Resolve image path for different scenarios"""
        # If it's already a URL, keep it as is
        parsed = urlparse(src)
        if parsed.scheme in ('http', 'https', 'data'):
            return src
        
        # Convert Windows path separators
        src = src.replace('\\', '/')
        
        # If it's an absolute path, convert to file:// URL
        if os.path.isabs(src):
            # Convert to file:// URL for local files
            return Path(src).resolve().as_uri()
        
        # If we have a base path, resolve relative to it
        if base_path:
            base_dir = Path(base_path).parent if os.path.isfile(base_path) else Path(base_path)
            full_path = base_dir / src
            if full_path.exists():
                return full_path.resolve().as_uri()
        
        # Return as-is for relative paths or if file doesn't exist
        return src


LIGHT_CSS = """
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; margin: 0; padding: 0; }
.content { padding: 16px 24px; max-width: 1000px; margin: 0 auto; }
pre, code { background: #f5f5f7; border-radius: 6px; }
pre { padding: 12px; overflow-x: auto; }
blockquote { border-left: 4px solid #e0e0e0; margin: 0; padding: 8px 16px; color: #555; background: #fafafa; }
table { border-collapse: collapse; }
th, td { border: 1px solid #ddd; padding: 6px 10px; }
a { color: #0066cc; }
/* Image styling */
img { 
    max-width: 100%; 
    height: auto; 
    border-radius: 8px; 
    box-shadow: 0 2px 8px rgba(0,0,0,0.1); 
    margin: 10px 0; 
    display: block;
}
.image-caption { 
    text-align: center; 
    font-style: italic; 
    color: #666; 
    font-size: 0.9em; 
    margin-top: 5px; 
}
/* Page break support for printing/PDF */
.pagebreak, div[style*="page-break"] { 
    page-break-after: always; 
    page-break-inside: avoid;
    break-after: page;
    height: 0;
    margin: 0;
    padding: 0;
}
@media print {
    .pagebreak, div[style*="page-break"] {
        page-break-after: always;
        page-break-inside: avoid;
        break-after: page;
    }
}
"""

DARK_CSS = """
body { background: #0f1115; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; margin: 0; padding: 0; }
.content { padding: 16px 24px; max-width: 1000px; margin: 0 auto; }
pre, code { background: #1a1f2b; color: #e2e8f0; border-radius: 6px; }
pre { padding: 12px; overflow-x: auto; }
blockquote { border-left: 4px solid #334155; margin: 0; padding: 8px 16px; color: #94a3b8; background: #0b0e14; }
th, td { border: 1px solid #243247; padding: 6px 10px; }
a { color: #7aa2f7; }
/* Image styling */
img { 
    max-width: 100%; 
    height: auto; 
    border-radius: 8px; 
    box-shadow: 0 2px 8px rgba(0,0,0,0.3); 
    margin: 10px 0; 
    display: block;
}
.image-caption { 
    text-align: center; 
    font-style: italic; 
    color: #94a3b8; 
    font-size: 0.9em; 
    margin-top: 5px; 
}
/* Page break support for printing/PDF */
.pagebreak, div[style*="page-break"] { 
    page-break-after: always; 
    page-break-inside: avoid;
    break-after: page;
    height: 0;
    margin: 0;
    padding: 0;
}
@media print {
    .pagebreak, div[style*="page-break"] {
        page-break-after: always;
        page-break-inside: avoid;
        break-after: page;
    }
}
"""
