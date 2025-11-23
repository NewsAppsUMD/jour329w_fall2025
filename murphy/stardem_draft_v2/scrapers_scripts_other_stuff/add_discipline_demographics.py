import json
from collections import OrderedDict, defaultdict

# Load the suspension data
with open('eastern_shore_suspensions_2023_2024.json', 'r') as f:
    suspension_records = json.load(f)

# Load the county summary book
with open('county_summary_book.json', 'r') as f:
    county_book = json.load(f, object_pairs_hook=OrderedDict)

# Aggregate county-level discipline data with all demographic breakdowns
county_discipline = {}

for county_name in ["Caroline", "Dorchester", "Kent", "Queen Anne's", "Talbot"]:
    county_records = [r for r in suspension_records if r['county'] == county_name]
    
    # Initialize aggregation structures
    in_school = defaultdict(int)
    out_of_school = defaultdict(int)
    
    for record in county_records:
        suspension_type = record['suspension_type']
        target = in_school if suspension_type == 'in_school' else out_of_school
        
        # Aggregate all fields
        target['total'] += record.get('total_suspensions', 0)
        target['male'] += record.get('male', 0)
        target['female'] += record.get('female', 0)
        target['black'] += record.get('black', 0)
        target['hispanic'] += record.get('hispanic', 0)
        target['white'] += record.get('white', 0)
        target['asian'] += record.get('asian', 0)
        target['american_indian'] += record.get('american_indian', 0)
        target['two_or_more'] += record.get('two_or_more', 0)
        target['students_with_disabilities'] += record.get('students_with_disabilities', 0)
        target['economically_disadvantaged'] += record.get('economically_disadvantaged', 0)
    
    # Create structured discipline data
    total_in = in_school['total']
    total_out = out_of_school['total']
    total_all = total_in + total_out
    
    county_discipline[county_name] = {
        'total_suspensions': total_all,
        'in_school_suspensions': {
            'total': total_in,
            'by_gender': {
                'male': in_school['male'],
                'female': in_school['female']
            },
            'by_race': {
                'black': in_school['black'],
                'hispanic': in_school['hispanic'],
                'white': in_school['white'],
                'asian': in_school['asian'],
                'american_indian': in_school['american_indian'],
                'two_or_more': in_school['two_or_more']
            },
            'students_with_disabilities': in_school['students_with_disabilities'],
            'economically_disadvantaged': in_school['economically_disadvantaged']
        },
        'out_of_school_suspensions': {
            'total': total_out,
            'by_gender': {
                'male': out_of_school['male'],
                'female': out_of_school['female']
            },
            'by_race': {
                'black': out_of_school['black'],
                'hispanic': out_of_school['hispanic'],
                'white': out_of_school['white'],
                'asian': out_of_school['asian'],
                'american_indian': out_of_school['american_indian'],
                'two_or_more': out_of_school['two_or_more']
            },
            'students_with_disabilities': out_of_school['students_with_disabilities'],
            'economically_disadvantaged': out_of_school['economically_disadvantaged']
        }
    }

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

# Update county_summary_book with county-level discipline and school-level demographics
for county_name in ["Caroline", "Dorchester", "Kent", "Queen Anne's", "Talbot"]:
    if county_name in county_book:
        county_data = county_book[county_name]
        
        # Add county-level discipline summary after staffing
        if county_name in county_discipline:
            # Find where to insert (after staffing, before schools_and_performance)
            new_county = OrderedDict()
            for key, value in county_data.items():
                new_county[key] = value
                if key == 'staffing':
                    new_county['student_discipline'] = county_discipline[county_name]
            county_book[county_name] = new_county
        
        # Add demographics to school-level discipline data
        if 'schools_and_performance' in county_data:
            schools = county_data['schools_and_performance'].get('schools', [])
            for school in schools:
                import re
                match = re.search(r'\((\d{4})\)', school.get('school_name', ''))
                if match:
                    school_num = match.group(1)
                    key = (county_name, school_num)
                    if key in school_discipline and 'discipline' in school:
                        # Replace simple discipline data with full demographic breakdown
                        school['discipline'] = school_discipline[key]

# Save updated county_summary_book
with open('county_summary_book.json', 'w') as f:
    json.dump(county_book, f, indent=2)

print("✓ Added county-level discipline summaries with demographic breakdowns")
print("✓ Enhanced school-level discipline data with demographic details")

# Show sample for Caroline
print("\nSample County Discipline Data (Caroline):")
import json
print(json.dumps(county_discipline['Caroline'], indent=2))
