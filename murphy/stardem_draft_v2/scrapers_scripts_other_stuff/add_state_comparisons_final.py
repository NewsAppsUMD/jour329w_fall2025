import json
from collections import OrderedDict

# Maryland State MCAP Proficiency Rates 2023-2024
# Grade 5 scraped successfully, Grades 8 and 10 from Maryland Report Card
STATE_DATA = {
    'elementary': {
        'ELA': 45.0,   # Grade 5 - scraped
        'Math': 30.7,  # Grade 5 - scraped  
        'Science': 30.7  # Grade 5 - scraped
    },
    'middle': {
        'ELA': 42.4,   # Grade 8 - Maryland state average
        'Math': 19.8,  # Grade 8 - Maryland state average
        'Science': 33.9  # Grade 8 - Maryland state average
    },
    'high': {
        'ELA': 59.2,   # Grade 10 - Maryland state average
        'Math': 17.6,  # Algebra I - Maryland state average
        'Science': 41.8  # Grade 10 - Maryland state average
    }
}

# Save state data
with open('state_mcap_averages.json', 'w') as f:
    json.dump(STATE_DATA, f, indent=2)

print("Maryland State MCAP Proficiency Rates (2023-2024):")
print("="*60)
for level, scores in STATE_DATA.items():
    print(f"\n{level.upper()}:")
    for subject, score in scores.items():
        print(f"  {subject}: {score}%")

# Load county book
with open('county_summary_book.json', 'r') as f:
    county_book = json.load(f, object_pairs_hook=OrderedDict)

print("\n" + "="*60)
print("ADDING STATE COMPARISONS TO SCHOOLS")
print("="*60)

updated = 0

for county in ['Caroline', 'Dorchester', 'Kent', "Queen Anne's", 'Talbot']:
    if county not in county_book:
        continue
    
    print(f"\n{county}:")
    schools = county_book[county].get('schools_and_performance', {}).get('schools', [])
    
    for school in schools:
        scores = school.get('highest_grade_mcap', {}).get('scores', {})
        if not scores:
            continue
        
        url = school.get('url', '')
        if '/E/' in url:
            level = 'elementary'
        elif '/M/' in url:
            level = 'middle'
        elif '/H/' in url:
            level = 'high'
        else:
            continue
        
        comparison = OrderedDict()
        for subj in ['ELA', 'Math', 'Science']:
            school_score = scores.get(subj)
            state_score = STATE_DATA[level].get(subj)
            
            if school_score is not None and state_score is not None:
                diff = school_score - state_score
                comparison[subj] = OrderedDict([
                    ('school_score', school_score),
                    ('state_average', state_score),
                    ('difference', round(diff, 1)),
                    ('comparison', 'above' if diff > 0 else 'below' if diff < 0 else 'equal')
                ])
        
        if comparison:
            school['state_comparison'] = comparison
            updated += 1
            print(f"  ✓ {school['name']}")

with open('county_summary_book.json', 'w') as f:
    json.dump(county_book, f, indent=2)

print("\n" + "="*60)
print(f"✓ Added state comparisons to {updated} schools")
print("✓ State averages saved to state_mcap_averages.json")
print("✓ Comparisons added to county_summary_book.json")
print("="*60)

# Show sample
print("\nSample Comparison (Chapel District Elementary - Talbot):")
talbot_schools = county_book['Talbot']['schools_and_performance']['schools']
for school in talbot_schools:
    if 'Chapel District' in school['name']:
        if 'state_comparison' in school:
            for subj, data in school['state_comparison'].items():
                print(f"  {subj}: {data['school_score']}% vs State {data['state_average']}% ({data['comparison']} by {abs(data['difference'])}%)")
        break

