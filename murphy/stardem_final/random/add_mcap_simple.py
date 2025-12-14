#!/usr/bin/env python3
"""
Simple approach: Add MCAP data right after each Student Groups section
"""

import json
import re
from pathlib import Path

# Read MCAP data  
mcap_file = Path("/workspaces/jour329w_fall2025/murphy/stardem_final/dashboard/mcap_grade_level_scores.json")
with open(mcap_file) as f:
    mcap_raw = json.load(f)

# Organize by school
mcap_by_school = {}
for item in mcap_raw:
    name = item['school_name']
    if name not in mcap_by_school:
        mcap_by_school[name] = []
    mcap_by_school[name].append(item)

# Read dashboard
dashboard_file = Path("/workspaces/jour329w_fall2025/murphy/stardem_final/dashboard/dashboard.html")
html = dashboard_file.read_text()

# Count existing MCAP sections
existing_mcap = html.count('📈 MCAP Performance')
print(f"Existing MCAP sections: {existing_mcap}")

# For each school in MCAP data, try to add the data
updates = 0

for school_name, scores in mcap_by_school.items():
    # Build MCAP section
    by_grade = {}
    for s in scores:
        if s.get('proficient_pct'):
            grade = s['grade']
            if grade not in by_grade:
                by_grade[grade] = {}
            by_grade[grade][s['subject']] = s['proficient_pct']
    
    if not by_grade:
        continue
        
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
    
    # Try to find this school in the HTML
    # Extract base name without code
    base_name = re.sub(r'\s*\([^)]*\)', '', school_name).strip()
    
    # Look for patterns: "<h4>School Name</h4>" or "<h4>School Name (code)</h4>"
    # And then find where its Student Groups section ends
    
    # Try exact match first
    for search_name in [school_name, base_name]:
        pattern = f'<h4>{search_name}</h4>'
        if pattern in html:
            print(f"  Found: {search_name}")
            # Find this school's Student Groups section
            pos = html.find(pattern)
            # Find the Student Groups heading after this
            groups_pos = html.find('<h5>🎯 Student Groups</h5>', pos)
            if groups_pos > pos:
                print(f"    Student Groups found")
                # Find the end of this detail-stats div
                # Look for closing </div> followed by another closing div for school-details
                search_start = groups_pos + 100
                # Find pattern: </div>\n                            </div>\n                        </div>
                # This is: end of detail-stats, end of school-details, end of school-card
                insert_pattern = r'(</div>\s*</div>\s*</div>)'
                
                # Find the first occurrence after Student Groups
                remaining = html[search_start:search_start+2000]
                match = re.search(insert_pattern, remaining)
                if match:
                    print(f"    Closing divs found, inserting MCAP")
                    insert_pos = search_start + match.start()
                    # Insert MCAP before the triple closing divs
                    html = html[:insert_pos] + mcap_html + '\n                            ' + html[insert_pos:]
                    updates += 1
                    print(f"  ✓ {search_name}")
                    break
                else:
                    print(f"    No closing divs match")
            else:
                print(f"    Student Groups not found after position {pos}")
        else:
            print(f"  Not found: {search_name}")

print(f"\n✓ Added MCAP data to {updates} schools")

# Save
dashboard_file.write_text(html)
print(f"✓ Saved to {dashboard_file}")
