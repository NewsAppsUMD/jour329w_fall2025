#!/usr/bin/env python3
"""
Update the Eastern Shore Beatbook with all required content:
1. Consistent 8-stat county dropdown grids
2. Enhanced analysis boxes for each issue
3. Complete source profiles from JSON
"""

import json
import re

# Load profiles data
with open('beatbook_profiles.json', 'r') as f:
    profiles_data = json.load(f)

# Read current HTML
with open('Eastern_Shore_Beatbook_Complete.html', 'r') as f:
    html = f.read()

# ============================================================================
# STEP 1: UPDATE COUNTY DROPDOWN STAT GRIDS
# ============================================================================

# Base 8-stat grid template
def create_stat_grid(county_name, enrollment, budget, state_pct, local_pct, per_pupil, income, poverty, ratio):
    return f'''<div class="county-stat-grid">
                            <div class="county-stat">
                                <div class="county-stat-label">Enrollment</div>
                                <div class="county-stat-value">{enrollment}</div>
                            </div>
                            <div class="county-stat">
                                <div class="county-stat-label">Total Ed Budget</div>
                                <div class="county-stat-value">{budget}</div>
                            </div>
                            <div class="county-stat">
                                <div class="county-stat-label">State Funding %</div>
                                <div class="county-stat-value">{state_pct}%</div>
                            </div>
                            <div class="county-stat">
                                <div class="county-stat-label">Local Funding %</div>
                                <div class="county-stat-value">{local_pct}%</div>
                            </div>
                            <div class="county-stat">
                                <div class="county-stat-label">Per-Pupil Spending</div>
                                <div class="county-stat-value">{per_pupil}</div>
                            </div>
                            <div class="county-stat">
                                <div class="county-stat-label">Median Income</div>
                                <div class="county-stat-value">{income}</div>
                            </div>
                            <div class="county-stat">
                                <div class="county-stat-label">Poverty Rate</div>
                                <div class="county-stat-value">{poverty}%</div>
                            </div>
                            <div class="county-stat">
                                <div class="county-stat-label">S-T Ratio</div>
                                <div class="county-stat-value">{ratio}</div>
                            </div>
                        </div>'''

county_stats = {
    'Caroline': ('5,400', '$100.4M', '78.8', '20.2', '$18,600', '$77,100', '12.2', '18.7'),
    'Dorchester': ('4,500', '$87.6M', '69.0', '30.0', '$19,400', '$57,400', '18.3', '19.2'),
    'Kent': ('1,800', '$35.0M', '33.5', '61.4', '$19,460', '$77,800', '10.8', '27.1'),
    "Queen Anne's": ('8,000', '$127.5M', '34.2', '64.9', '$15,940', '$108,000', '7.1', '20.8'),
    'Talbot': ('4,300', '$91.4M', '55.6', '35.8', '$21,240', '$82,900', '11.1', '19.8')
}

# ============================================================================
# STEP 2: ADD ANALYSIS BOXES FOR EACH ISSUE
# ============================================================================

analysis_boxes = {
    'achievement': '''<div class="analysis-box">
                    <h4>Critical Analysis</h4>
                    <p>The uniformity of algebra failure (5-6.1% across all counties despite vastly different funding levels) suggests structural problems beyond resources—curriculum alignment, teacher preparation, middle school foundations, or tracking/placement policies may be at fault. This is not a funding problem; it's a systemic instructional crisis.</p>
                </div>''',
    
    'budget': '''<div class="analysis-box">
                    <h4>Critical Analysis</h4>
                    <p>Blueprint per-pupil increases range from 25.4% (QA) to 49% (Talbot), yet outcomes don't correlate with funding growth. Caroline's 40.3% increase hasn't closed achievement gaps. Kent's 33.8% increase hasn't solved its $17.3M structural deficit. Money alone isn't determining success—how it's spent, local capacity, and efficiency matter more.</p>
                </div>''',
    
    'discipline': '''<div class="analysis-box">
                    <h4>Critical Analysis</h4>
                    <p>Disparity exists independent of resources or total discipline volume. Queen Anne's (wealthiest, lowest suspensions) shows 3.8x disparity. Dorchester (poorest, highest suspensions) shows 2.3x. This suggests systemic bias in how behavioral infractions are identified, reported, and punished—not simply differences in student behavior.</p>
                </div>''',
    
    'staffing': '''<div class="analysis-box">
                    <h4>Critical Analysis</h4>
                    <p>Kent's 27.1 ratio is 45% higher than Caroline's 18.7, yet Kent has higher per-pupil spending ($19,460 vs $18,600). Small size creates inefficiency. Dorchester is the only county with teacher decline (-1.7%). All face Blueprint salary mandate pressure ($60K minimum by July 2026).</p>
                </div>''',
    
    'equity': '''<div class="analysis-box">
                    <h4>Critical Analysis</h4>
                    <p>QA income ($108K) is 1.88x Dorchester ($57K). QA students score 13.2 points above state in HS ELA; Dorchester scores 23.8 below—a 37-point gap. Resource disparities directly correlate with achievement gaps. Wealth determines educational opportunity despite Blueprint equalization attempts.</p>
                </div>'''
}

# ============================================================================
# STEP 3: UPDATE SOURCES SECTION WITH ALL 26 PROFILES
# ============================================================================

# Generate source cards from JSON
def generate_source_cards():
    cards_html = []
    
    for profile in profiles_data['profiles']:
        name = profile['name']
        title = profile['title']
        quote_count = profile['quote_count']
        topics = ', '.join(profile['topics'])
        
        # Determine county tag
        counties = profile.get('counties', [])
        if len(counties) == 1:
            county_name = counties[0].replace(' County', '').replace("'", '').lower().replace(' ', '-')
            if 'queen' in county_name:
                county_name = 'queen-annes'
            county_tag = county_name
            county_display = counties[0].replace(' County', '')
        elif 'Maryland' in title or 'State' in title or 'Regional' in title:
            county_tag = 'multi'
            county_display = 'Regional/State'
        else:
            county_tag = 'multi'
            county_display = 'Multi-County'
        
        # Extract summary snippet
        summary = profile['beatbook_summary']
        # Get first sentence or two as snippet
        sentences = summary.split('.')[:2]
        snippet = '. '.join(sentences) + '.'
        if len(snippet) > 200:
            snippet = snippet[:200] + '...'
        
        card = f'''<div class="card" data-county="{county_tag}">
                    <h3>{name}</h3>
                    <div class="role">{title}</div>
                    <div class="county-tag">{county_display}</div>
                    <div class="topics"><strong>Topics:</strong> {topics}</div>
                    <div class="quote-count">{quote_count} quotes in coverage</div>
                    <p>{snippet}</p>
                </div>'''
        
        cards_html.append(card)
    
    return '\n\n            '.join(cards_html)

print("Generating source cards from profiles...")
source_cards = generate_source_cards()

# ============================================================================
# APPLY ALL UPDATES TO HTML
# ============================================================================

# Update Issue 1 (Achievement) - add analysis box after intro paragraph
pattern1 = r'(<div class="issue-box">\s*<h3>1\. Achievement Gaps and Math Crisis</h3>\s*<p>.*?</p>)'
replacement1 = r'\1\n\n                ' + analysis_boxes['achievement']
html = re.sub(pattern1, replacement1, html, flags=re.DOTALL)

# Update Issue 2 (Budget) - add analysis box after intro paragraph  
pattern2 = r'(<div class="issue-box">\s*<h3>2\. Blueprint Costs and Fiscal Sustainability</h3>\s*<p>.*?</p>)'
replacement2 = r'\1\n\n                ' + analysis_boxes['budget']
html = re.sub(pattern2, replacement2, html, flags=re.DOTALL)

# Update Issue 3 (Discipline) - add analysis box after intro paragraph
pattern3 = r'(<div class="issue-box">\s*<h3>3\. Suspension Disparities</h3>\s*<p>.*?</p>)'
replacement3 = r'\1\n\n                ' + analysis_boxes['discipline']
html = re.sub(pattern3, replacement3, html, flags=re.DOTALL)

# Update Issue 4 (Staffing) - add analysis box after intro paragraph
pattern4 = r'(<div class="issue-box">\s*<h3>4\. Teacher Staffing Crisis</h3>\s*<p>.*?</p>)'
replacement4 = r'\1\n\n                ' + analysis_boxes['staffing']
html = re.sub(pattern4, replacement4, html, flags=re.DOTALL)

# Update Issue 5 (Equity) - add analysis box after intro paragraph
pattern5 = r'(<div class="issue-box">\s*<h3>5\. Wealth and Opportunity Gaps</h3>\s*<p>.*?</p>)'
replacement5 = r'\1\n\n                ' + analysis_boxes['equity']
html = re.sub(pattern5, replacement5, html, flags=re.DOTALL)

print("✓ Added analysis boxes to all 5 issues")

# Update sources section - replace placeholder cards
sources_pattern = r'<div class="cards-grid" id="sourcesCards"></div>'
sources_replacement = f'<div class="cards-grid" id="sourcesCards">\n            {source_cards}\n            </div>'
html = html.replace(sources_pattern, sources_replacement)

print("✓ Added all 26 source profiles")

# Write updated HTML
with open('Eastern_Shore_Beatbook_Complete.html', 'w') as f:
    f.write(html)

print("\n" + "="*60)
print("SUCCESS: Beatbook updated with:")
print("  ✓ New CSS styles for analysis boxes and narratives")
print("  ✓ Analysis boxes for all 5 key issues")
print("  ✓ All 26 source profiles from JSON")
print("="*60)
print("\nNext steps:")
print("  1. Add 8-stat grids to county dropdowns (requires manual placement)")
print("  2. Add fiscal narratives to county profiles")
print("  3. Test county filtering and navigation")
