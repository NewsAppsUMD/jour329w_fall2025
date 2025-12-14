#!/usr/bin/env python3
"""
Add MCAP data to all school cards in the dashboard
"""

import json
import re
from pathlib import Path

# Load MCAP data
mcap_file = Path("/workspaces/jour329w_fall2025/murphy/stardem_final/dashboard/mcap_grade_level_scores.json")
with open(mcap_file) as f:
    mcap_raw = json.load(f)

# Organize by school - the JSON has a nested structure with 'scores' array
mcap_by_school = {}
for school_entry in mcap_raw:
    name = school_entry['school_name']
    mcap_by_school[name] = school_entry.get('scores', [])

print(f"Loaded MCAP data for {len(mcap_by_school)} schools\n")

# Load dashboard HTML
dashboard_file = Path("/workspaces/jour329w_fall2025/murphy/stardem_final/dashboard/dashboard.html")
html = dashboard_file.read_text()

# Check for existing MCAP sections
existing = html.count('📈 MCAP Performance')
print(f"Existing MCAP sections: {existing}\n")

# Process each school
updates = 0
for school_name, scores in mcap_by_school.items():
    # Build MCAP HTML section
    by_grade = {}
    for s in scores:
        if s.get('proficient_pct'):
            grade = s['grade']
            if grade not in by_grade:
                by_grade[grade] = {}
            by_grade[grade][s['subject']] = s['proficient_pct']
    
    if not by_grade:
        print(f"  ✗ {school_name[:40]} - no grade data")
        continue
    
    # Build HTML
    mcap_html = '\n                                <h5>📈 MCAP Performance (2024-25)</h5>'
    for grade in sorted(by_grade.keys()):
        mcap_html += f'\n                                <p style="margin: 0.5rem 0; font-weight: 600;">Grade {grade}:</p>'
        mcap_html += '\n                                <div class="detail-stats">'
        for subj in ['ELA', 'Math', 'Science']:
            if subj in by_grade[grade]:
                pct = by_grade[grade][subj]
                mcap_html += f'\n                                    <div class="detail-stat">'
                mcap_html += f'\n                                        <span class="detail-label">{subj}</span>'
                mcap_html += f'\n                                        <span class="detail-value">{pct}% Proficient</span>'
                mcap_html += f'\n                                    </div>'
        mcap_html += '\n                                </div>'
    
    # Try to find this school in HTML
    # Remove code suffix to get base name
    base_name = re.sub(r'\s*\([^)]*\)', '', school_name).strip()
    
    # Look for <h4>base_name</h4> in the HTML (don't escape, it's literal text)
    h4_pattern = f'<h4>{base_name}</h4>'
    
    if h4_pattern not in html:
        continue
    
    # Find this school's position
    h4_pos = html.find(h4_pattern)
    
    # Find Student Groups section after this h4
    student_groups_pos = html.find('<h5>🎯 Student Groups</h5>', h4_pos)
    if student_groups_pos == -1 or student_groups_pos > h4_pos + 5000:
        continue
    
    # Find the end of the Student Groups detail-stats div
    # Look for the pattern: </div>\n</div>\n</div> (end of detail-stats, end of school-details, end of school-card)
    search_start = student_groups_pos + 200
    
    # Find next occurrence of triple closing divs
    triple_div_pattern = r'(</div>\s+</div>\s+</div>)'
    remaining = html[search_start:search_start + 1500]
    match = re.search(triple_div_pattern, remaining)
    
    if not match:
        continue
    
    # Check if MCAP already exists in this section
    section = html[student_groups_pos:search_start + match.start()]
    if '📈 MCAP' in section:
        continue  # Already has MCAP
    
    # Insert position is right before the triple closing divs
    insert_pos = search_start + match.start()
    
    # Insert MCAP HTML
    html = html[:insert_pos] + mcap_html + '\n                            ' + html[insert_pos:]
    
    updates += 1
    print(f"  ✓ {base_name}")

print(f"\n{'='*60}")
print(f"Added MCAP data to {updates} schools")
print(f"{'='*60}")

# Save updated HTML
dashboard_file.write_text(html)
print(f"\n✓ Saved to: {dashboard_file}")
