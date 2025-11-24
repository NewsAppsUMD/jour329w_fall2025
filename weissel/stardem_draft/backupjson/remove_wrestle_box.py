#!/usr/bin/env python3
"""Remove stories whose title contains 'WRESTLE BOX' (case-insensitive).
Creates a backup `source_stories.json.bak10` before writing.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source_stories.json"
if not SRC.exists():
    print(f"ERROR: {SRC} not found")
    sys.exit(2)

backup = ROOT / (SRC.name + ".bak10")
data = json.loads(SRC.read_text())
backup.write_text(json.dumps(data, ensure_ascii=False, indent=2))

total = len(data)
keep = []
removed_titles = []
for story in data:
    title = (story.get("title") or "").strip()
    if "WRESTLE BOX" in title.upper():
        removed_titles.append(title)
    else:
        keep.append(story)

removed = total - len(keep)
SRC.write_text(json.dumps(keep, ensure_ascii=False, indent=2))
print(f"WROTE: {SRC} — removed={removed}, total_before={total}, remaining={len(keep)}, backup={backup}")
if removed > 0:
    print("Removed titles (sample up to 20):")
    for t in removed_titles[:20]:
        print(" - ", t)
