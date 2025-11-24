#!/usr/bin/env python3
"""Remove the `content` field from every story in source_stories.json.
Creates a backup `source_stories.json.bak14` before writing.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source_stories.json"
if not SRC.exists():
    print(f"ERROR: {SRC} not found")
    sys.exit(2)

backup = ROOT / (SRC.name + ".bak14")
backup.write_bytes(SRC.read_bytes())

data = json.loads(SRC.read_text())
total = len(data)
modified = 0
for story in data:
    if 'content' in story:
        del story['content']
        modified += 1

SRC.write_text(json.dumps(data, ensure_ascii=False, indent=2))
print(f"WROTE: {SRC} — removed_content={modified}, total={total}, backup={backup}")
