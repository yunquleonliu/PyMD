#!/usr/bin/env python3
"""
Extract WeChat messages from message_*.db in db_storage/message/ and export to Markdown files.
Supports keyword filtering and Obsidian-friendly output.

Usage:
  python tools/wechat_db_to_md.py --root D:/xwechat_files/wxid_xxx --out output/wechat_md_db [--keyword 关键词1 关键词2 ...]

- Scans db_storage/message/ for all message_*.db
- Reads messages, optionally filters by keywords
- Outputs per-chat Markdown files (Obsidian vault ready)

Requirements: Python 3.8+, sqlite3, tqdm (optional for progress)
"""
import os
import glob
import sqlite3
import argparse
import re
from collections import defaultdict
from datetime import datetime

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(x, **kwargs):
        return x

def safe_filename(s):
    s = s.strip()
    s = re.sub(r"[\\/:*?\"<>|]+", "-", s)
    s = re.sub(r"\s+", "_", s)
    return s[:200]

def extract_messages(db_path, keywords=None):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Try common table/column names
    # Table: message, Columns: createTime, talker, content, type, isSend
    try:
        cur.execute("SELECT createTime, talker, content, type, isSend FROM message")
    except Exception as e:
        print(f"[WARN] {db_path}: {e}")
        return []
    rows = cur.fetchall()
    messages = []
    for row in rows:
        ts, talker, content, msgtype, issend = row
        if not content:
            continue
        if keywords:
            if not any(k in content for k in keywords):
                continue
        dt = datetime.fromtimestamp(ts/1000) if ts > 1000000000 else datetime.fromtimestamp(ts)
        messages.append({
            "time": dt,
            "chat": talker,
            "content": content,
            "type": msgtype,
            "is_send": issend,
        })
    return messages

def main():
    parser = argparse.ArgumentParser(description="WeChat message_*.db to Markdown")
    parser.add_argument('--root', required=True, help='Root of wxid_xxx directory')
    parser.add_argument('--out', required=True, help='Output directory for Markdown')
    parser.add_argument('--keyword', nargs='*', help='Only export messages containing these keywords')
    args = parser.parse_args()

    db_dir = os.path.join(args.root, 'db_storage', 'message')
    db_files = glob.glob(os.path.join(db_dir, 'message_*.db'))
    if not db_files:
        print(f"No message_*.db found in {db_dir}")
        return
    os.makedirs(args.out, exist_ok=True)
    all_chats = defaultdict(list)
    for dbf in tqdm(db_files, desc='DBs'):
        msgs = extract_messages(dbf, args.keyword)
        for m in msgs:
            all_chats[m['chat']].append(m)
    for chat, msgs in all_chats.items():
        msgs.sort(key=lambda m: m['time'])
        fname = safe_filename(chat) or 'chat'
        out_path = os.path.join(args.out, f'{fname}.md')
        with open(out_path, 'w', encoding='utf-8') as out:
            out.write(f'---\ntitle: "{chat}"\nsource: WeChat DB\n---\n\n')
            for m in msgs:
                ts = m['time'].strftime('%Y-%m-%d %H:%M:%S')
                out.write(f'- {ts}: {m["content"]}\n')
        print(f'Wrote {out_path} ({len(msgs)} messages)')

if __name__ == '__main__':
    main()
