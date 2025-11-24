#!/usr/bin/env python3
"""Backup and remove `llm_classification_meta` from every story.
Run from the repository root or any path — uses relative path to the draft folder.
"""
import json
import shutil
from pathlib import Path

P = Path(__file__).parent / "source_stories.json"
if not P.exists():
    raise SystemExit(f"File not found: {P}")

# Backup
bak = P.with_name(P.name + ".bak5")
shutil.copy2(P, bak)

with P.open("r", encoding="utf-8") as f:
    data = json.load(f)

modified = 0
for story in data:
    if "llm_classification_meta" in story:
        del story["llm_classification_meta"]
        modified += 1

with P.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"WROTE: {P} — modified={modified}, total={len(data)}, backup={bak}")
