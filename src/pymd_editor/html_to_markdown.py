"""
HTML到Markdown转换器
提供更准确的HTML内容转换为Markdown格式的功能
"""

import re
from html.parser import HTMLParser
from typing import List, Dict, Optional


class HTMLToMarkdownConverter(HTMLParser):
    """HTML到Markdown转换器"""
    
    def __init__(self):
        super().__init__()
        self.reset()
        self.markdown_lines: List[str] = []
        self.current_line = ""
        self.tag_stack: List[Dict] = []
        self.list_stack: List[Dict] = []
        self.in_pre = False
        self.in_code = False
        self.table_data: List[List[str]] = []
        self.current_row: List[str] = []
        self.in_table = False
        
    def handle_starttag(self, tag: str, attrs: list):
        """处理开始标签"""
        attrs_dict = dict(attrs)
        
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self._flush_line()
            level = int(tag[1])
            self.tag_stack.append({'tag': 'header', 'level': level})
            
        elif tag == 'p':
            self._flush_line()
            self.tag_stack.append({'tag': 'paragraph'})
            
        elif tag == 'br':
            self.current_line += '  \n'  # Markdown换行
            
        elif tag in ['strong', 'b']:
            self.tag_stack.append({'tag': 'bold'})
            self.current_line += '**'
            
        elif tag in ['em', 'i']:
            self.tag_stack.append({'tag': 'italic'})
            self.current_line += '*'
            
        elif tag == 'code':
            if not self.in_pre:
                self.tag_stack.append({'tag': 'inline_code'})
                self.current_line += '`'
                self.in_code = True
                
        elif tag == 'pre':
            self._flush_line()
            self.tag_stack.append({'tag': 'code_block'})
            self.in_pre = True
            self.markdown_lines.append('```')
            
        elif tag == 'blockquote':
            self._flush_line()
            self.tag_stack.append({'tag': 'blockquote'})
            
        elif tag == 'a':
            href = attrs_dict.get('href', '')
            self.tag_stack.append({'tag': 'link', 'href': href})
            self.current_line += '['
            
        elif tag in ['ul', 'ol']:
            self._flush_line()
            list_type = 'ordered' if tag == 'ol' else 'unordered'
            self.list_stack.append({'type': list_type, 'counter': 0})
            
        elif tag == 'li':
            self._flush_line()
            if self.list_stack:
                list_info = self.list_stack[-1]
                if list_info['type'] == 'ordered':
                    list_info['counter'] += 1
                    prefix = f"{list_info['counter']}. "
                else:
                    prefix = "- "
                
                indent = "  " * (len(self.list_stack) - 1)
                self.current_line = indent + prefix
                
        elif tag == 'table':
            self._flush_line()
            self.in_table = True
            self.table_data = []
            
        elif tag == 'tr':
            if self.in_table:
                self.current_row = []
                
        elif tag == 'td' or tag == 'th':
            if self.in_table:
                # 开始新的单元格
                pass
                
        elif tag == 'img':
            src = attrs_dict.get('src', '')
            alt = attrs_dict.get('alt', '')
            title = attrs_dict.get('title', '')
            
            if title:
                self.current_line += f'![{alt}]({src} "{title}")'
            else:
                self.current_line += f'![{alt}]({src})'
                
    def handle_endtag(self, tag: str):
        """处理结束标签"""
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            if self.tag_stack and self.tag_stack[-1]['tag'] == 'header':
                level = self.tag_stack[-1]['level']
                header_line = '#' * level + ' ' + self.current_line
                self.markdown_lines.append(header_line)
                self.current_line = ""
                self.tag_stack.pop()
                
        elif tag == 'p':
            if self.tag_stack and self.tag_stack[-1]['tag'] == 'paragraph':
                self._flush_line()
                self.tag_stack.pop()
                
        elif tag in ['strong', 'b']:
            if self.tag_stack and self.tag_stack[-1]['tag'] == 'bold':
                self.current_line += '**'
                self.tag_stack.pop()
                
        elif tag in ['em', 'i']:
            if self.tag_stack and self.tag_stack[-1]['tag'] == 'italic':
                self.current_line += '*'
                self.tag_stack.pop()
                
        elif tag == 'code':
            if self.tag_stack and self.tag_stack[-1]['tag'] == 'inline_code':
                self.current_line += '`'
                self.tag_stack.pop()
                self.in_code = False
                
        elif tag == 'pre':
            if self.tag_stack and self.tag_stack[-1]['tag'] == 'code_block':
                self.markdown_lines.append('```')
                self.tag_stack.pop()
                self.in_pre = False
                
        elif tag == 'blockquote':
            if self.tag_stack and self.tag_stack[-1]['tag'] == 'blockquote':
                # 处理引用内容
                self._process_blockquote()
                self.tag_stack.pop()
                
        elif tag == 'a':
            if self.tag_stack and self.tag_stack[-1]['tag'] == 'link':
                href = self.tag_stack[-1]['href']
                self.current_line += f']({href})'
                self.tag_stack.pop()
                
        elif tag in ['ul', 'ol']:
            if self.list_stack:
                self.list_stack.pop()
                self._flush_line()
                
        elif tag == 'li':
            self._flush_line()
            
        elif tag == 'table':
            if self.in_table:
                self._process_table()
                self.in_table = False
                
        elif tag == 'tr':
            if self.in_table and self.current_row:
                self.table_data.append(self.current_row)
                self.current_row = []
                
        elif tag in ['td', 'th']:
            if self.in_table:
                self.current_row.append(self.current_line)
                self.current_line = ""
                
    def handle_data(self, data: str):
        """处理文本数据"""
        if self.in_pre:
            self.markdown_lines.append(data)
        else:
            # 清理多余的空白符，但保留单个空格
            cleaned_data = re.sub(r'\s+', ' ', data)
            self.current_line += cleaned_data
            
    def _flush_line(self):
        """将当前行刷新到结果中"""
        if self.current_line.strip():
            # 处理引用
            if any(tag_info.get('tag') == 'blockquote' for tag_info in self.tag_stack):
                self.current_line = '> ' + self.current_line.strip()
                
            self.markdown_lines.append(self.current_line.strip())
            self.current_line = ""
        elif self.markdown_lines and self.markdown_lines[-1] != "":
            # 添加空行
            self.markdown_lines.append("")
            
    def _process_blockquote(self):
        """处理引用块"""
        # 引用内容已经在handle_data中处理，这里只需要添加空行
        self._flush_line()
        
    def _process_table(self):
        """处理表格"""
        if not self.table_data:
            return
            
        # 添加表格标题行
        if self.table_data:
            header_row = "| " + " | ".join(self.table_data[0]) + " |"
            self.markdown_lines.append(header_row)
            
            # 添加分隔行
            separator = "| " + " | ".join(["---"] * len(self.table_data[0])) + " |"
            self.markdown_lines.append(separator)
            
            # 添加数据行
            for row in self.table_data[1:]:
                data_row = "| " + " | ".join(row) + " |"
                self.markdown_lines.append(data_row)
                
        self.table_data = []
        
    def convert(self, html: str) -> str:
        """将HTML转换为Markdown"""
        self.reset()
        self.markdown_lines = []
        self.current_line = ""
        self.tag_stack = []
        self.list_stack = []
        self.in_pre = False
        self.in_code = False
        self.table_data = []
        self.current_row = []
        self.in_table = False
        
        # 清理HTML
        html = self._clean_html(html)
        
        # 解析HTML
        self.feed(html)
        
        # 处理剩余内容
        self._flush_line()
        
        # 清理结果
        result = self._clean_markdown('\n'.join(self.markdown_lines))
        return result
        
    def _clean_html(self, html: str) -> str:
        """清理HTML内容"""
        # 移除HTML注释
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        
        # 移除script和style标签及其内容
        html = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # 标准化空白符
        html = re.sub(r'\r\n|\r', '\n', html)
        
        return html
        
    def _clean_markdown(self, markdown: str) -> str:
        """清理Markdown内容"""
        lines = markdown.split('\n')
        cleaned_lines = []
        
        # 移除多余的空行
        prev_empty = False
        for line in lines:
            if line.strip() == "":
                if not prev_empty:
                    cleaned_lines.append("")
                    prev_empty = True
            else:
                cleaned_lines.append(line)
                prev_empty = False
                
        # 移除开头和结尾的空行
        while cleaned_lines and cleaned_lines[0] == "":
            cleaned_lines.pop(0)
        while cleaned_lines and cleaned_lines[-1] == "":
            cleaned_lines.pop()
            
        return '\n'.join(cleaned_lines)


def html_to_markdown(html: str) -> str:
    """便捷函数：将HTML转换为Markdown"""
    converter = HTMLToMarkdownConverter()
    return converter.convert(html)


# 用于测试的简单转换函数（向后兼容）
def simple_html_to_markdown(html: str) -> str:
    """简单的HTML到Markdown转换（向后兼容）"""
    text = html
    
    # 处理标题
    text = re.sub(r'<h([1-6])[^>]*>(.*?)</h[1-6]>', 
                  lambda m: '\n' + '#' * int(m.group(1)) + ' ' + m.group(2).strip() + '\n', 
                  text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理段落
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理粗体
    text = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理斜体
    text = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理链接
    text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理内联代码
    text = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理代码块
    text = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', r'```\n\1\n```', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理列表项
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<[uo]l[^>]*>(.*?)</[uo]l>', r'\1\n', text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理引用
    text = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', 
                  lambda m: '\n'.join('> ' + line.strip() for line in m.group(1).strip().split('\n') if line.strip()) + '\n', 
                  text, flags=re.IGNORECASE | re.DOTALL)
    
    # 处理换行
    text = re.sub(r'<br[^>]*>', '\n', text, flags=re.IGNORECASE)
    
    # 清理HTML标签
    text = re.sub(r'<[^>]*>', '', text)
    
    # 清理HTML实体
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    
    # 清理多余的空行
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()