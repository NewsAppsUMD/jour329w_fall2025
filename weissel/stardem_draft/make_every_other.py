#!/usr/bin/env python3
"""Create `source_stories_every_other.json` by selecting every other story
from `source_stories.json` starting at index 0 (even indices).
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source_stories.json"
DST = ROOT / "source_stories_every_other.json"

if not SRC.exists():
    print(f"ERROR: {SRC} not found")
    sys.exit(2)

data = json.loads(SRC.read_text())
selected = [s for i, s in enumerate(data) if i % 2 == 0]

DST.write_text(json.dumps(selected, ensure_ascii=False, indent=2))
print(f"WROTE: {DST} — selected={len(selected)}, source_total={len(data)}")
