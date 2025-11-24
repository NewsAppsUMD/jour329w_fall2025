#!/usr/bin/env python3
"""Strip pre-story boilerplate from each story's `content`.

Removes everything from the start of `content` up through the first occurrence
of the phrase "Read News Document" (inclusive), then left-strips newlines/spaces.
Creates a backup `source_stories.json.bak12` before writing.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source_stories.json"
if not SRC.exists():
    print(f"ERROR: {SRC} not found")
    sys.exit(2)

bak = ROOT / (SRC.name + ".bak12")
bak.write_bytes(SRC.read_bytes())

data = json.loads(SRC.read_text())
total = len(data)
modified = 0

for story in data:
    content = story.get("content")
    if not isinstance(content, str) or not content:
        continue
    key = "Read News Document"
    idx = content.find(key)
    if idx != -1:
        # remove through the key and any following newlines/spaces
        end = idx + len(key)
        # skip following whitespace/newlines
        while end < len(content) and content[end] in "\r\n \t":
            end += 1
        new_content = content[end:]
        # also strip leading punctuation/newlines if any remain
        new_content = new_content.lstrip('\r\n ')
        if new_content != content:
            story["content"] = new_content
            modified += 1

SRC.write_text(json.dumps(data, ensure_ascii=False, indent=2))
print(f"WROTE: {SRC} — modified={modified}, total={total}, backup={bak}")
