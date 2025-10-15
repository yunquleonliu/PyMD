from __future__ import annotations

import markdown2


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
            "metadata",
        ]

    def to_html(self, text: str, dark: bool = False) -> str:
        html_body = markdown2.markdown(text or "", extras=self._extras)
        css = DARK_CSS if dark else LIGHT_CSS
        return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset=\"utf-8\" />
<style>
{css}
</style>
</head>
<body>
<div class=\"content\">{html_body}</div>
</body>
</html>
"""


LIGHT_CSS = """
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; margin: 0; padding: 0; }
.content { padding: 16px 24px; max-width: 1000px; margin: 0 auto; }
pre, code { background: #f5f5f7; border-radius: 6px; }
pre { padding: 12px; overflow-x: auto; }
blockquote { border-left: 4px solid #e0e0e0; margin: 0; padding: 8px 16px; color: #555; background: #fafafa; }
table { border-collapse: collapse; }
th, td { border: 1px solid #ddd; padding: 6px 10px; }
a { color: #0066cc; }
"""

DARK_CSS = """
body { background: #0f1115; color: #e2e8f0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; margin: 0; padding: 0; }
.content { padding: 16px 24px; max-width: 1000px; margin: 0 auto; }
pre, code { background: #1a1f2b; color: #e2e8f0; border-radius: 6px; }
pre { padding: 12px; overflow-x: auto; }
blockquote { border-left: 4px solid #334155; margin: 0; padding: 8px 16px; color: #94a3b8; background: #0b0e14; }
th, td { border: 1px solid #243247; padding: 6px 10px; }
a { color: #7aa2f7; }
"""
