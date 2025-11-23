import json

def add_percentages(record):
    """Add percentage fields for demographics and offenses while keeping raw counts"""
    total = record['total_suspensions']
    
    if total == 0:
        return record
    
    # Add demographic percentages
    record['male_pct'] = round((record['male'] / total * 100), 1) if total > 0 else 0
    record['female_pct'] = round((record['female'] / total * 100), 1) if total > 0 else 0
    record['asian_pct'] = round((record['asian'] / total * 100), 1) if total > 0 else 0
    record['black_pct'] = round((record['black'] / total * 100), 1) if total > 0 else 0
    record['hispanic_pct'] = round((record['hispanic'] / total * 100), 1) if total > 0 else 0
    record['white_pct'] = round((record['white'] / total * 100), 1) if total > 0 else 0
    record['two_or_more_pct'] = round((record['two_or_more'] / total * 100), 1) if total > 0 else 0
    record['students_with_disabilities_pct'] = round((record['students_with_disabilities'] / total * 100), 1) if total > 0 else 0
    
    # Add offense category percentages
    record['offense_attendance_pct'] = round((record['offense_attendance'] / total * 100), 1) if total > 0 else 0
    record['offense_dangerous_substances_pct'] = round((record['offense_dangerous_substances'] / total * 100), 1) if total > 0 else 0
    record['offense_weapons_pct'] = round((record['offense_weapons'] / total * 100), 1) if total > 0 else 0
    record['offense_attacks_threats_fighting_pct'] = round((record['offense_attacks_threats_fighting'] / total * 100), 1) if total > 0 else 0
    record['offense_arson_fire_explosives_pct'] = round((record['offense_arson_fire_explosives'] / total * 100), 1) if total > 0 else 0
    record['offense_sex_offenses_pct'] = round((record['offense_sex_offenses'] / total * 100), 1) if total > 0 else 0
    record['offense_disrespect_disruption_pct'] = round((record['offense_disrespect_disruption'] / total * 100), 1) if total > 0 else 0
    record['offense_other_pct'] = round((record['offense_other'] / total * 100), 1) if total > 0 else 0
    
    return record

# Process county-level data
print("Adding percentages to county-level data...")
with open('county_level_suspensions_2023_2024.json', 'r') as f:
    county_data = json.load(f)

county_data = [add_percentages(record) for record in county_data]

with open('county_level_suspensions_2023_2024.json', 'w') as f:
    json.dump(county_data, f, indent=2)

print(f"✓ Updated {len(county_data)} county records")

# Process school-level data
print("\nAdding percentages to school-level data...")
with open('school_level_suspensions_2023_2024.json', 'r') as f:
    school_data = json.load(f)

school_data = [add_percentages(record) for record in school_data]

with open('school_level_suspensions_2023_2024.json', 'w') as f:
    json.dump(school_data, f, indent=2)

print(f"✓ Updated {len(school_data)} school records")

# Show sample
print("\n" + "=" * 80)
print("SAMPLE RECORD WITH PERCENTAGES")
print("=" * 80)

sample = county_data[0]
print(f"\n{sample['school_name']} - {sample['suspension_type']}")
print(f"Total: {sample['total_suspensions']}")
print(f"\nDemographics (count / percentage):")
print(f"  Male: {sample['male']} / {sample['male_pct']}%")
print(f"  Female: {sample['female']} / {sample['female_pct']}%")
print(f"  Black: {sample['black']} / {sample['black_pct']}%")
print(f"  White: {sample['white']} / {sample['white_pct']}%")
print(f"  Hispanic: {sample['hispanic']} / {sample['hispanic_pct']}%")
print(f"  SWD: {sample['students_with_disabilities']} / {sample['students_with_disabilities_pct']}%")
print(f"\nTop Offenses (count / percentage):")
print(f"  Disrespect/Disruption: {sample['offense_disrespect_disruption']} / {sample['offense_disrespect_disruption_pct']}%")
print(f"  Attacks/Threats/Fighting: {sample['offense_attacks_threats_fighting']} / {sample['offense_attacks_threats_fighting_pct']}%")
print(f"  Attendance: {sample['offense_attendance']} / {sample['offense_attendance_pct']}%")

print("\n✓ All data updated with percentages!")
