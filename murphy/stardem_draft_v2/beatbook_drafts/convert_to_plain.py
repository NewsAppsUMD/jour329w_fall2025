#!/usr/bin/env python3
import re

# Read the markdown file
with open('beatbook_v2_enhanced.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove markdown formatting
# Remove headers (# ## ###)
content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)

# Remove bold (**text**)
content = re.sub(r'\*\*([^\*]+)\*\*', r'\1', content)

# Remove italic (*text*)
content = re.sub(r'\*([^\*]+)\*', r'\1', content)

# Remove horizontal rules (---)
content = re.sub(r'^---+\s*$', '', content, flags=re.MULTILINE)

# Remove links but keep text [text](url) -> text
content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)

# Convert bullet points to simple indentation
content = re.sub(r'^-\s+', '  • ', content, flags=re.MULTILINE)

# Remove extra blank lines (more than 2 consecutive)
content = re.sub(r'\n{3,}', '\n\n', content)

# Write the plain text version
with open('beatbook_v2_enhanced_plain.txt', 'w', encoding='utf-8') as f:
    f.write(content)

print("Conversion complete! Created: beatbook_v2_enhanced_plain.txt")
