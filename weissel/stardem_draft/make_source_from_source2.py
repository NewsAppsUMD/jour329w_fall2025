#!/usr/bin/env python3
"""Create `source_stories.json` from `source_stories2.json` by taking every other story.
Backs up existing `source_stories.json` to `source_stories.json.bak11`.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
SRC2 = ROOT / "source_stories2.json"
DST = ROOT / "source_stories.json"

if not SRC2.exists():
    print(f"ERROR: {SRC2} not found")
    sys.exit(2)

data2 = json.loads(SRC2.read_text())
total2 = len(data2)

# backup existing DST if present
backup = None
if DST.exists():
    backup = ROOT / (DST.name + ".bak11")
    backup.write_text(DST.read_text())

# take every other story starting at index 0 (even indices)
selected = [story for i, story in enumerate(data2) if i % 2 == 0]

DST.write_text(json.dumps(selected, ensure_ascii=False, indent=2))

print(f"WROTE: {DST} — selected={len(selected)}, total_source2={total2}, backup={backup}")
