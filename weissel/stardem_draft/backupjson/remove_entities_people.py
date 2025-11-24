#!/usr/bin/env python3
"""Remove `entities_people` from every story in source_stories.json.
Creates a backup `source_stories.json.bak8` before writing.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source_stories.json"
if not SRC.exists():
    print(f"ERROR: {SRC} not found")
    sys.exit(2)

backup = ROOT / (SRC.name + ".bak8")
data_bytes = SRC.read_bytes()
backup.write_bytes(data_bytes)

data = json.loads(data_bytes)
total = len(data)
modified = 0
for story in data:
    if "entities_people" in story:
        del story["entities_people"]
        modified += 1

SRC.write_text(json.dumps(data, ensure_ascii=False, indent=2))
print(f"WROTE: {SRC} — modified={modified}, total={total}, backup={backup}")
