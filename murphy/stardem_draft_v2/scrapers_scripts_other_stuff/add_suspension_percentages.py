import json
from collections import OrderedDict

def add_percentages(suspension_data, total):
    """Add percentage calculations to suspension data"""
    if total == 0:
        return suspension_data
    
    result = OrderedDict()
    result['total'] = suspension_data['total']
    
    # Gender percentages
    if 'by_gender' in suspension_data:
        result['by_gender'] = OrderedDict()
        for gender, count in suspension_data['by_gender'].items():
            pct = round((count / total * 100), 1) if total > 0 else 0
            result['by_gender'][gender] = OrderedDict([
                ('count', count),
                ('percent', pct)
            ])
    
    # Race percentages
    if 'by_race' in suspension_data:
        result['by_race'] = OrderedDict()
        for race, count in suspension_data['by_race'].items():
            pct = round((count / total * 100), 1) if total > 0 else 0
            result['by_race'][race] = OrderedDict([
                ('count', count),
                ('percent', pct)
            ])
    
    # Students with disabilities
    if 'students_with_disabilities' in suspension_data:
        count = suspension_data['students_with_disabilities']
        pct = round((count / total * 100), 1) if total > 0 else 0
        result['students_with_disabilities'] = OrderedDict([
            ('count', count),
            ('percent', pct)
        ])
    
    # Economically disadvantaged
    if 'economically_disadvantaged' in suspension_data:
        count = suspension_data['economically_disadvantaged']
        pct = round((count / total * 100), 1) if total > 0 else 0
        result['economically_disadvantaged'] = OrderedDict([
            ('count', count),
            ('percent', pct)
        ])
    
    return result

# Load the county summary book
with open('county_summary_book.json', 'r') as f:
    county_book = json.load(f, object_pairs_hook=OrderedDict)

# Update county-level discipline data with percentages
for county_name in ["Caroline", "Dorchester", "Kent", "Queen Anne's", "Talbot"]:
    if county_name in county_book and 'student_discipline' in county_book[county_name]:
        disc = county_book[county_name]['student_discipline']
        total = disc['total_suspensions']
        
        # Update in-school suspensions
        in_school_total = disc['in_school_suspensions']['total']
        disc['in_school_suspensions'] = add_percentages(disc['in_school_suspensions'], in_school_total)
        
        # Update out-of-school suspensions
        out_school_total = disc['out_of_school_suspensions']['total']
        disc['out_of_school_suspensions'] = add_percentages(disc['out_of_school_suspensions'], out_school_total)

# Update school-level discipline data with percentages
for county_name in ["Caroline", "Dorchester", "Kent", "Queen Anne's", "Talbot"]:
    if county_name in county_book and 'schools_and_performance' in county_book[county_name]:
        schools = county_book[county_name]['schools_and_performance'].get('schools', [])
        for school in schools:
            if 'discipline' in school:
                disc = school['discipline']
                total = disc['total_suspensions']
                
                # Update in-school suspensions
                in_school_total = disc['in_school_suspensions']['total']
                disc['in_school_suspensions'] = add_percentages(disc['in_school_suspensions'], in_school_total)
                
                # Update out-of-school suspensions
                out_school_total = disc['out_of_school_suspensions']['total']
                disc['out_of_school_suspensions'] = add_percentages(disc['out_of_school_suspensions'], out_school_total)

# Save updated county_summary_book
with open('county_summary_book.json', 'w') as f:
    json.dump(county_book, f, indent=2)

print("✓ Added percentage calculations to all suspension data")

# Show sample
print("\nSample - Caroline County In-School Suspensions:")
caroline = county_book['Caroline']['student_discipline']['in_school_suspensions']
print(f"Total: {caroline['total']}")
print(f"Students with Disabilities: {caroline['students_with_disabilities']['count']} ({caroline['students_with_disabilities']['percent']}%)")
print(f"Black: {caroline['by_race']['black']['count']} ({caroline['by_race']['black']['percent']}%)")
print(f"White: {caroline['by_race']['white']['count']} ({caroline['by_race']['white']['percent']}%)")
