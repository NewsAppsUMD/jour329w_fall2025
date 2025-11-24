#!/usr/bin/env python3
"""Remove one random story from `source_stories_every_other.json`.
Creates a backup `source_stories_every_other.json.bak15` before writing.
Prints the removed story title and new count.
"""
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source_stories_every_other.json"
if not SRC.exists():
    print(f"ERROR: {SRC} not found")
    sys.exit(2)

backup = ROOT / (SRC.name + ".bak15")
backup.write_bytes(SRC.read_bytes())

data = json.loads(SRC.read_text())
total_before = len(data)
if total_before == 0:
    print("File empty; nothing to remove")
    sys.exit(0)

idx = random.randrange(total_before)
removed = data.pop(idx)

SRC.write_text(json.dumps(data, ensure_ascii=False, indent=2))
print(f"WROTE: {SRC} — removed_index={idx}, removed_title={removed.get('title')!r}, new_count={len(data)}, backup={backup}")
