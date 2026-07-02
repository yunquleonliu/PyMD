WeChat CSV -> Markdown tools
================================

tools/wechat_csv_to_md.py
- Converts a CSV exported from WeChat (or normalized CSV with common columns) into per-conversation Markdown files.

Quick start:

```bash
python tools/wechat_csv_to_md.py --input data/wechat_export.csv --out output/wechat_md
```

Notes:
- The script attempts to detect common CSV column names automatically.
- If timestamps are in non-standard formats, install `python-dateutil` (already added to `requirements.txt`).

tools/wechat_db_to_md.py
- 自动扫描 db_storage/message/ 下所有 message_*.db，导出为 Markdown（支持关键词筛选）。

用法示例：
```bash
python tools/wechat_db_to_md.py --root D:/xwechat_files/wxid_xxx --out output/wechat_md_db --keyword 关键词1 关键词2
```
