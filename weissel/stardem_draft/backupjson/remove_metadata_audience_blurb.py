#!/usr/bin/env python3
"""Remove `metadata_audience_blurb` from every story in source_stories.json.
Creates a backup `source_stories.json.bak9` before writing.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source_stories.json"
if not SRC.exists():
    print(f"ERROR: {SRC} not found")
    sys.exit(2)

backup = ROOT / (SRC.name + ".bak9")
data_bytes = SRC.read_bytes()
backup.write_bytes(data_bytes)

data = json.loads(data_bytes)
total = len(data)
modified = 0
for story in data:
    if "metadata_audience_blurb" in story:
        del story["metadata_audience_blurb"]
        modified += 1

SRC.write_text(json.dumps(data, ensure_ascii=False, indent=2))
print(f"WROTE: {SRC} — modified={modified}, total={total}, backup={backup}")
