#!/usr/bin/env python3
"""Convert a WeChat-exported CSV into per-conversation Markdown files.

Usage:
  python tools/wechat_csv_to_md.py --input data/wechat_export.csv --out output/wechat_md

The script attempts to detect common CSV column names. Supported columns:
  - timestamp / time / datetime / date
  - sender / from / nickname / user
  - receiver / to / participant
  - chat / conversation / group
  - content / message / text
  - media / media_path / attachment

If a `chat`/`conversation` column exists, messages are grouped by it; otherwise grouped by sender/receiver pair.
"""
from __future__ import annotations

import argparse
import csv
import os
import re
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional

try:
    from dateutil import parser as dateparser
except Exception:
    dateparser = None


COMMON_TS = ["timestamp", "time", "datetime", "date"]
COMMON_SENDER = ["sender", "from", "nickname", "user"]
COMMON_RECEIVER = ["receiver", "to", "participant"]
COMMON_CHAT = ["chat", "conversation", "group"]
COMMON_CONTENT = ["content", "message", "text", "body"]
COMMON_MEDIA = ["media", "media_path", "attachment", "file"]


def detect_column(fieldnames: List[str], candidates: List[str]) -> Optional[str]:
    lower = {f.lower(): f for f in fieldnames}
    for c in candidates:
        if c in lower:
            return lower[c]
    return None


def safe_filename(s: str) -> str:
    s = s.strip()
    s = re.sub(r"[\\/:*?\"<>|]+", "-", s)
    s = re.sub(r"\s+", "_", s)
    return s[:200]


def parse_time(s: str) -> Optional[datetime]:
    if not s:
        return None
    s = s.strip()
    if not s:
        return None
    if dateparser:
        try:
            return dateparser.parse(s)
        except Exception:
            pass
    # fallback common iso formats
    fmts = [
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
    ]
    for f in fmts:
        try:
            return datetime.strptime(s, f)
        except Exception:
            continue
    return None


def row_to_msg(row: Dict[str, str], mapping: Dict[str, Optional[str]]):
    ts = row.get(mapping.get("ts") or "")
    sender = row.get(mapping.get("sender") or "") or ""
    receiver = row.get(mapping.get("receiver") or "") or ""
    chat = row.get(mapping.get("chat") or "") or ""
    content = row.get(mapping.get("content") or "") or ""
    media = row.get(mapping.get("media") or "") or ""
    parsed = parse_time(ts)
    return {
        "time": parsed,
        "time_raw": ts,
        "sender": sender,
        "receiver": receiver,
        "chat": chat,
        "content": content,
        "media": media,
    }


def main():
    p = argparse.ArgumentParser(description="WeChat CSV -> Markdown converter")
    p.add_argument("--input", "-i", required=True, help="Input CSV file")
    p.add_argument("--out", "-o", required=True, help="Output directory for markdown files")
    p.add_argument("--group", "-g", choices=["chat", "pair"], default="chat", help="Group by chat name (if present) or pair")
    args = p.parse_args()

    os.makedirs(args.out, exist_ok=True)

    with open(args.input, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        cols = reader.fieldnames or []

        mapping = {
            "ts": detect_column(cols, COMMON_TS),
            "sender": detect_column(cols, COMMON_SENDER),
            "receiver": detect_column(cols, COMMON_RECEIVER),
            "chat": detect_column(cols, COMMON_CHAT),
            "content": detect_column(cols, COMMON_CONTENT),
            "media": detect_column(cols, COMMON_MEDIA),
        }

        groups: Dict[str, List[Dict]] = defaultdict(list)

        for row in reader:
            msg = row_to_msg(row, mapping)
            if args.group == "chat" and msg.get("chat"):
                key = msg.get("chat")
            else:
                a = msg.get("sender") or "unknown"
                b = msg.get("receiver") or "unknown"
                # make pair key deterministic
                k1, k2 = sorted([a, b])
                key = f"{k1}__{k2}"
            groups[key].append(msg)

    # write files
    for key, msgs in groups.items():
        # sort by time when possible
        msgs.sort(key=lambda m: (m["time"] is None, m["time"] or datetime.min))

        title = key
        filename = safe_filename(title) or "conversation"
        out_path = os.path.join(args.out, f"{filename}.md")

        participants = set()
        times = []
        for m in msgs:
            if m.get("sender"):
                participants.add(m["sender"])
            if m.get("receiver"):
                participants.add(m["receiver"])
            if m.get("time"):
                times.append(m.get("time"))

        start = min(times).isoformat() if times else ""
        end = max(times).isoformat() if times else ""

        with open(out_path, "w", encoding="utf-8") as out:
            out.write("---\n")
            out.write(f"title: \"{title}\"\n")
            out.write(f"participants: {sorted(participants)}\n")
            out.write(f"start: \"{start}\"\n")
            out.write(f"end: \"{end}\"\n")
            out.write("source: WeChat CSV\n")
            out.write("---\n\n")

            for m in msgs:
                ts = m.get("time")
                if ts:
                    ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    ts_str = m.get("time_raw") or ""
                sender = m.get("sender") or ""
                content = m.get("content") or ""
                media = m.get("media") or ""

                out.write(f"- {ts_str} — **{sender}**: {content}\n")
                if media:
                    out.write(f"  - attachment: {media}\n")

        print(f"Wrote {out_path} ({len(msgs)} messages)")


if __name__ == "__main__":
    main()
