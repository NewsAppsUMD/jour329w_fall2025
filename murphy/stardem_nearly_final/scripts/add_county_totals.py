import json
import os

# County information
counties = {
    '05': {'name': 'Caroline', 'folder': 'caroline'},
    '09': {'name': 'Dorchester', 'folder': 'dorchester'},
    '14': {'name': 'Kent', 'folder': 'kent'},
    '17': {'name': 'Queen Anne\'s', 'folder': 'queen_annes'},
    '20': {'name': 'Talbot', 'folder': 'talbot'}
}

def calculate_county_totals(county_code, folder_name):
    """Calculate county-wide enrollment and demographics"""
    
    # Load the county enrollment file
    county_file = f'../enrollment_data/{folder_name}/{folder_name}_county_enrollment.json'
    
    with open(county_file, 'r') as f:
        schools = json.load(f)
    
    # Aggregate by category and group
    totals = {}
    
    for school in schools:
        for enrollment_item in school['enrollment_data']:
            category = enrollment_item['category']
            group = enrollment_item['group']
            enrollment = enrollment_item['enrollment']
            
            # Skip asterisk values (suppressed data)
            if enrollment == '*':
                continue
            
            # Initialize category if needed
            if category not in totals:
                totals[category] = {}
            
            # Initialize group if needed
            if group not in totals[category]:
                totals[category][group] = 0
            
            # Add enrollment
            totals[category][group] += int(enrollment)
    
    # Build the county_totals structure
    county_totals = []
    
    # Get total enrollment from "All Students" in Race/Ethnicity
    total_enrollment = totals.get('Race/Ethnicity', {}).get('All Students', 0)
    
    # Add each category's data
    for category in ['Race/Ethnicity', 'Gender', 'Grade']:
        if category not in totals:
            continue
        
        for group, enrollment in totals[category].items():
            percentage = round((enrollment / total_enrollment * 100), 2) if total_enrollment > 0 else 0
            
            county_totals.append({
                'category': category,
                'group': group,
                'enrollment': enrollment,
                'year': '2025',
                'percentage': percentage
            })
    
    return {
        'total_enrollment': total_enrollment,
        'enrollment_breakdown': county_totals
    }

def update_master_file(county_code, county_name, folder_name):
    """Update a master data file with county totals"""
    
    master_file = f'../master_data/{folder_name}_master_student_data.json'
    
    print(f"\nProcessing {county_name} County...")
    
    # Load master data
    with open(master_file, 'r') as f:
        data = json.load(f)
    
    # Calculate county totals
    county_totals = calculate_county_totals(county_code, folder_name)
    
    # Add county totals at the beginning (after county_code)
    new_data = {
        'county_name': data['county_name'],
        'county_code': data['county_code'],
        'county_totals': county_totals
    }
    
    # Add the rest of the data
    for key, value in data.items():
        if key not in ['county_name', 'county_code']:
            new_data[key] = value
    
    # Save updated file
    with open(master_file, 'w') as f:
        json.dump(new_data, f, indent=2)
    
    print(f"✓ Added county totals - Total Enrollment: {county_totals['total_enrollment']:,}")
    
    # Print some demographics
    race_data = [item for item in county_totals['enrollment_breakdown'] 
                 if item['category'] == 'Race/Ethnicity' and item['group'] != 'All Students']
    print(f"  Demographics breakdown:")
    for item in sorted(race_data, key=lambda x: x['enrollment'], reverse=True):
        print(f"    {item['group']}: {item['enrollment']:,} ({item['percentage']}%)")

def main():
    print("Adding county-wide enrollment and demographics to master data files...")
    
    for county_code, info in counties.items():
        update_master_file(county_code, info['name'], info['folder'])
    
    print("\n" + "="*80)
    print("COMPLETE - All master data files updated with county totals")
    print("="*80)

if __name__ == '__main__':
    main()
