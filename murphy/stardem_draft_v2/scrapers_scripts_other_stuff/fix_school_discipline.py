import json
from collections import OrderedDict
import re

# Load the suspension data
with open('eastern_shore_suspensions_2023_2024.json', 'r') as f:
    suspension_records = json.load(f)

# Load the county summary book
with open('county_summary_book.json', 'r') as f:
    county_book = json.load(f, object_pairs_hook=OrderedDict)

# Create lookup for school-level discipline data with demographics
school_discipline = {}
for record in suspension_records:
    county = record['county']
    school_num = record['school_number']
    susp_type = record['suspension_type']
    
    key = (county, school_num)
    if key not in school_discipline:
        school_discipline[key] = {
            'total_suspensions': 0,
            'in_school_suspensions': {
                'total': 0,
                'by_gender': {'male': 0, 'female': 0},
                'by_race': {'black': 0, 'hispanic': 0, 'white': 0, 'asian': 0, 'american_indian': 0, 'two_or_more': 0},
                'students_with_disabilities': 0,
                'economically_disadvantaged': 0
            },
            'out_of_school_suspensions': {
                'total': 0,
                'by_gender': {'male': 0, 'female': 0},
                'by_race': {'black': 0, 'hispanic': 0, 'white': 0, 'asian': 0, 'american_indian': 0, 'two_or_more': 0},
                'students_with_disabilities': 0,
                'economically_disadvantaged': 0
            }
        }
    
    target = school_discipline[key]['in_school_suspensions'] if susp_type == 'in_school' else school_discipline[key]['out_of_school_suspensions']
    
    target['total'] += record.get('total_suspensions', 0)
    target['by_gender']['male'] += record.get('male', 0)
    target['by_gender']['female'] += record.get('female', 0)
    target['by_race']['black'] += record.get('black', 0)
    target['by_race']['hispanic'] += record.get('hispanic', 0)
    target['by_race']['white'] += record.get('white', 0)
    target['by_race']['asian'] += record.get('asian', 0)
    target['by_race']['american_indian'] += record.get('american_indian', 0)
    target['by_race']['two_or_more'] += record.get('two_or_more', 0)
    target['students_with_disabilities'] += record.get('students_with_disabilities', 0)
    target['economically_disadvantaged'] += record.get('economically_disadvantaged', 0)
    
    school_discipline[key]['total_suspensions'] = school_discipline[key]['in_school_suspensions']['total'] + school_discipline[key]['out_of_school_suspensions']['total']

# Update school-level discipline data with demographics
for county_name in ["Caroline", "Dorchester", "Kent", "Queen Anne's", "Talbot"]:
    if county_name in county_book:
        county_data = county_book[county_name]
        
        # Add demographics to school-level discipline data
        if 'schools_and_performance' in county_data:
            schools = county_data['schools_and_performance'].get('schools', [])
            for school in schools:
                # Extract school number from name field (e.g., "Chapel District Elementary (0401)")
                match = re.search(r'\((\d{4})\)', school.get('name', ''))
                if match:
                    school_num = match.group(1)
                    key = (county_name, school_num)
                    if key in school_discipline:
                        # Replace simple discipline data with full demographic breakdown
                        school['discipline'] = school_discipline[key]

# Save updated county_summary_book
with open('county_summary_book.json', 'w') as f:
    json.dump(county_book, f, indent=2)

print("✓ Enhanced school-level discipline data with demographic details")

# Show sample school
with open('county_summary_book.json', 'r') as f:
    data = json.load(f)

caroline_schools = data['Caroline']['schools_and_performance']['schools']
for school in caroline_schools:
    if 'Denton Elementary' in school['name']:
        print('\nSample School Discipline Data (Denton Elementary):')
        print(json.dumps(school['discipline'], indent=2))
        break
