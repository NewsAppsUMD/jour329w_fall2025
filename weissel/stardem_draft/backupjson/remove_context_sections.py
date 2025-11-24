#!/usr/bin/env python3
"""Remove `context` keys and 'Context:' blocks from story `content`.

Backs up `source_stories.json` to `source_stories.json.bak13` before writing.
"""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source_stories.json"
if not SRC.exists():
    print(f"ERROR: {SRC} not found")
    sys.exit(2)

bak = ROOT / (SRC.name + ".bak13")
bak.write_bytes(SRC.read_bytes())

data = json.loads(SRC.read_text())
total = len(data)
modified = 0

# regex to find 'Context:' block up to the next blank line (inclusive)
pattern = re.compile(r"\n\s*Context[:\-]?\s.*?(?:\n\s*\n|$)", re.IGNORECASE | re.DOTALL)

for story in data:
    changed = False
    # remove key named 'context' if present
    if 'context' in story:
        del story['context']
        changed = True

    content = story.get('content')
    if isinstance(content, str) and content:
        new_content = pattern.sub('\n\n', content)
        # also remove leading 'Context:' at start of content
        new_content = re.sub(r"^\s*Context[:\-]?\s.*?(?:\n\s*\n|$)", '', new_content, flags=re.IGNORECASE | re.DOTALL)
        # clean up: collapse multiple leading newlines
        new_content = re.sub(r"\A[\n\r\s]+", '', new_content)
        if new_content != content:
            story['content'] = new_content
            changed = True

    if changed:
        modified += 1

SRC.write_text(json.dumps(data, ensure_ascii=False, indent=2))
print(f"WROTE: {SRC} — modified={modified}, total={total}, backup={bak}")
