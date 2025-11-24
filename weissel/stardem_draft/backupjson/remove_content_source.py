#!/usr/bin/env python3
"""Create a backup and remove the `content_source` key from every story in source_stories.json.
Run from the `weissel/stardem_draft` directory.
"""
import json
import shutil
from pathlib import Path

P = Path(__file__).parent / "source_stories.json"
if not P.exists():
    raise SystemExit(f"File not found: {P}")

# Backup
bak = P.with_name(P.name + ".bak4")
shutil.copy2(P, bak)

with P.open("r", encoding="utf-8") as f:
    data = json.load(f)

modified = 0
for story in data:
    if "content_source" in story:
        del story["content_source"]
        modified += 1

with P.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"WROTE: {P} — modified={modified}, total={len(data)}, backup={bak}")
