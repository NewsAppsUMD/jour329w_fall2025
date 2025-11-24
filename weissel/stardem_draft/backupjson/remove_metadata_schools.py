#!/usr/bin/env python3
"""Backup and remove `metadata_schools` from every story in source_stories.json.
Run from the repository root or any path — uses relative path to the draft folder.
"""
import json
import shutil
from pathlib import Path

P = Path(__file__).parent / "source_stories.json"
if not P.exists():
    raise SystemExit(f"File not found: {P}")

# Backup
bak = P.with_name(P.name + ".bak7")
shutil.copy2(P, bak)

with P.open("r", encoding="utf-8") as f:
    data = json.load(f)

modified = 0
for story in data:
    if "metadata_schools" in story:
        del story["metadata_schools"]
        modified += 1

with P.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"WROTE: {P} — modified={modified}, total={len(data)}, backup={bak}")
