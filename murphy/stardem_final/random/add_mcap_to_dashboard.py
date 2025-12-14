#!/usr/bin/env python3
"""
Add MCAP data to dashboard school cards
Reads mcap_grade_level_scores.json and updates dashboard.html
"""

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Read MCAP data
mcap_file = Path("/workspaces/jour329w_fall2025/murphy/stardem_final/dashboard/mcap_grade_level_scores.json")
with open(mcap_file) as f:
    mcap_data = json.load(f)

# Organize MCAP data by school name (with code)
school_mcap = {}
for entry in mcap_data:
    school_name = entry['school_name']
    if school_name not in school_mcap:
        school_mcap[school_name] = []
    school_mcap[school_name].append(entry)

print(f"Loaded MCAP data for {len(school_mcap)} schools")

# Read dashboard HTML
dashboard_file = Path("/workspaces/jour329w_fall2025/murphy/stardem_final/dashboard/dashboard.html")
with open(dashboard_file, 'r') as f:
    html_content = f.read()

# Function to find matching MCAP data
def find_mcap_data(school_name):
    """Find MCAP data for a school name"""
    # Direct match
    if school_name in school_mcap:
        return school_mcap[school_name]
    
    # Try without parentheses content
    base_name = re.sub(r'\s*\([^)]*\)', '', school_name).strip()
    for mcap_name in school_mcap:
        if base_name in mcap_name or mcap_name.startswith(base_name):
            return school_mcap[mcap_name]
    
    return None

# Function to generate MCAP HTML
def generate_mcap_section(scores):
    """Generate MCAP HTML from score data"""
    # Organize by grade and subject
    by_grade = {}
    for score in scores:
        if score.get('proficient_pct') is None:
            continue
        grade = score['grade']
        if grade not in by_grade:
            by_grade[grade] = {}
        by_grade[grade][score['subject']] = score['proficient_pct']
    
    if not by_grade:
        return ""
    
    html = '\n                                <h5>📈 MCAP Performance (2024-25)</h5>'
    
    for grade in sorted(by_grade.keys()):
        subjects = by_grade[grade]
        html += f'\n                                <p style="margin: 0.5rem 0; font-weight: 600;">Grade {grade}:</p>'
        html += '\n                                <div class="detail-stats">'
        
        for subject in ['ELA', 'Math', 'Science']:
            if subject in subjects:
                pct = subjects[subject]
                html += f'\n                                    <div class="detail-stat">'
                html += f'\n                                        <span class="detail-label">{subject}</span>'
                html += f'\n                                        <span class="detail-value">{pct}% Proficient</span>'
                html += f'\n                                    </div>'
        
        html += '\n                                </div>'
    
    return html

# Pattern to find school details sections
# Find: <h4>SchoolName</h4>...lots of content...<h5>🎯 Student Groups</h5>...closing divs
pattern = r'(<div class="school-card[^>]+>.*?<h4>([^<]+)</h4>.*?<h5>🎯 Student Groups</h5>.*?</div>\s*</div>)\s*(</div>\s*</div>)'

updates_made = 0

def add_mcap(match):
    global updates_made
    full_card = match.group(1)
    school_name = match.group(2).strip()
    closing_divs = match.group(3)
    
    # Check if MCAP already exists
    if '📈 MCAP Performance' in full_card:
        return match.group(0)  # Already has MCAP
    
    scores = find_mcap_data(school_name)
    if scores:
        mcap_html = generate_mcap_section(scores)
        if mcap_html:
            updates_made += 1
            print(f"  ✓ {school_name}")
            # Insert MCAP before the closing divs
            return full_card + mcap_html + '\n                            ' + closing_divs
    
    return match.group(0)

# Apply the transformation
html_updated = re.sub(pattern, add_mcap, html_content, flags=re.DOTALL)

# Save
if updates_made > 0:
    with open(dashboard_file, 'w') as f:
        f.write(html_updated)
    print(f"\n✓ Updated {updates_made} schools with MCAP data")
    print(f"✓ Saved to: {dashboard_file}")
else:
    print("\n⚠ No updates made")

