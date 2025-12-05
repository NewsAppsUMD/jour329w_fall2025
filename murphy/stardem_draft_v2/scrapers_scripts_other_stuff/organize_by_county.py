#!/usr/bin/env python3
import json
from pathlib import Path

def organize_files():
    base_dir = Path('.')
    
    # Files to split by county
    files_to_split = [
        'district_officials.json',
        'schools_list.json',
        'board_meeting_schedules_complete.json',
        'schools_enhanced_data.json',
        'teacher_data.json',
        'enrollment_by_race_percentages.json',
        'mcap_highest_grades.json',
        'county_level_suspensions_2023_2024.json',
        'school_level_suspensions_2023_2024.json',
        'census_education_data.json'
    ]
    
    counties = ['caroline', 'dorchester', 'kent', 'queen_annes', 'talbot']
    
    for filename in files_to_split:
        filepath = base_dir / filename
        if not filepath.exists():
            print(f"Skipping {filename} - not found")
            continue
            
        print(f"Processing {filename}...")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Handle different data structures
        if filename == 'board_meeting_schedules_complete.json':
            # Has 'meeting_schedules' key
            schedules = data.get('meeting_schedules', [])
            for county in counties:
                county_data = [item for item in schedules if item.get('county', '').lower().replace("'", '').replace(' ', '_') == county]
                if county_data:
                    output_file = base_dir / county / filename
                    with open(output_file, 'w') as f:
                        json.dump({'meeting_schedules': county_data}, f, indent=2)
                    print(f"  Created {county}/{filename}")
        
        elif isinstance(data, list):
            # List of items with county field
            for county in counties:
                county_name_variants = [
                    county.replace('_', ' ').title(),
                    county.replace('_', "'").title(),
                    'Queen Anne\'s' if county == 'queen_annes' else county.title()
                ]
                
                county_data = []
                for item in data:
                    item_county = item.get('county', '')
                    # Normalize for comparison
                    if any(variant.lower() == item_county.lower() for variant in county_name_variants):
                        county_data.append(item)
                
                if county_data:
                    output_file = base_dir / county / filename
                    with open(output_file, 'w') as f:
                        json.dump(county_data, f, indent=2)
                    print(f"  Created {county}/{filename}")
        
        elif isinstance(data, dict):
            # Dictionary with county as top-level keys
            for county in counties:
                county_key_variants = [
                    county.replace('_', ' ').title(),
                    county.replace('_', "'").title(),
                    'Queen Anne\'s County' if county == 'queen_annes' else f'{county.title()} County',
                    'Queen Annes' if county == 'queen_annes' else county.title(),
                    county.title()
                ]
                
                # Find matching key
                county_data = None
                for variant in county_key_variants:
                    if variant in data:
                        county_data = {variant: data[variant]}
                        break
                
                if county_data:
                    output_file = base_dir / county / filename
                    with open(output_file, 'w') as f:
                        json.dump(county_data, f, indent=2)
                    print(f"  Created {county}/{filename}")
    
    # Copy state_mcap_averages to each county (it's reference data)
    state_mcap_file = base_dir / 'state_mcap_averages.json'
    if state_mcap_file.exists():
        print("Copying state_mcap_averages.json to all county folders...")
        for county in counties:
            output_file = base_dir / county / 'state_mcap_averages.json'
            with open(state_mcap_file, 'r') as src:
                with open(output_file, 'w') as dst:
                    dst.write(src.read())
            print(f"  Copied to {county}/")

if __name__ == '__main__':
    organize_files()
    print("\nDone! Files organized by county.")
