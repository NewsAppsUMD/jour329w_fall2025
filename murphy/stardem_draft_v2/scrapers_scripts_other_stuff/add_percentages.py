import json

def add_percentages(record):
    """Add percentage calculations to a suspension record"""
    total = record['total_suspensions']
    
    if total == 0:
        return record
    
    # Calculate demographic percentages
    record['male_pct'] = round((record['male'] / total) * 100, 1)
    record['female_pct'] = round((record['female'] / total) * 100, 1)
    record['asian_pct'] = round((record['asian'] / total) * 100, 1) if record['asian'] > 0 else 0
    record['black_pct'] = round((record['black'] / total) * 100, 1)
    record['hispanic_pct'] = round((record['hispanic'] / total) * 100, 1)
    record['white_pct'] = round((record['white'] / total) * 100, 1)
    record['two_or_more_pct'] = round((record['two_or_more'] / total) * 100, 1)
    record['students_with_disabilities_pct'] = round((record['students_with_disabilities'] / total) * 100, 1)
    
    # Calculate offense percentages
    record['offense_attendance_pct'] = round((record['offense_attendance'] / total) * 100, 1)
    record['offense_dangerous_substances_pct'] = round((record['offense_dangerous_substances'] / total) * 100, 1)
    record['offense_weapons_pct'] = round((record['offense_weapons'] / total) * 100, 1)
    record['offense_attacks_threats_fighting_pct'] = round((record['offense_attacks_threats_fighting'] / total) * 100, 1)
    record['offense_arson_fire_explosives_pct'] = round((record['offense_arson_fire_explosives'] / total) * 100, 1)
    record['offense_sex_offenses_pct'] = round((record['offense_sex_offenses'] / total) * 100, 1)
    record['offense_disrespect_disruption_pct'] = round((record['offense_disrespect_disruption'] / total) * 100, 1)
    record['offense_other_pct'] = round((record['offense_other'] / total) * 100, 1)
    
    return record

print("=" * 70)
print("ADDING PERCENTAGES TO SUSPENSION DATA")
print("=" * 70)

# Process county-level data
print("\nProcessing county-level data...")
with open('county_level_suspensions_2023_2024.json', 'r') as f:
    county_data = json.load(f)

for record in county_data:
    add_percentages(record)

with open('county_level_suspensions_2023_2024.json', 'w') as f:
    json.dump(county_data, f, indent=2)

print(f"✓ Updated {len(county_data)} county records")

# Process school-level data
print("\nProcessing school-level data...")
with open('school_level_suspensions_2023_2024.json', 'r') as f:
    school_data = json.load(f)

for record in school_data:
    add_percentages(record)

with open('school_level_suspensions_2023_2024.json', 'w') as f:
    json.dump(school_data, f, indent=2)

print(f"✓ Updated {len(school_data)} school records")

print("\n" + "=" * 70)
print("SAMPLE OUTPUT WITH PERCENTAGES")
print("=" * 70)

# Show sample county record
county_sample = county_data[0]
print(f"\n{county_sample['county']} County - {county_sample['suspension_type']}:")
print(f"  Total: {county_sample['total_suspensions']}")
print(f"\n  Demographics:")
print(f"    Male: {county_sample['male']} ({county_sample['male_pct']}%)")
print(f"    Female: {county_sample['female']} ({county_sample['female_pct']}%)")
print(f"    Black: {county_sample['black']} ({county_sample['black_pct']}%)")
print(f"    White: {county_sample['white']} ({county_sample['white_pct']}%)")
print(f"    Hispanic: {county_sample['hispanic']} ({county_sample['hispanic_pct']}%)")
print(f"    SWD: {county_sample['students_with_disabilities']} ({county_sample['students_with_disabilities_pct']}%)")
print(f"\n  Offense Categories:")
print(f"    Disrespect/Disruption: {county_sample['offense_disrespect_disruption']} ({county_sample['offense_disrespect_disruption_pct']}%)")
print(f"    Attacks/Threats/Fighting: {county_sample['offense_attacks_threats_fighting']} ({county_sample['offense_attacks_threats_fighting_pct']}%)")
print(f"    Attendance: {county_sample['offense_attendance']} ({county_sample['offense_attendance_pct']}%)")
print(f"    Dangerous Substances: {county_sample['offense_dangerous_substances']} ({county_sample['offense_dangerous_substances_pct']}%)")

# Show sample school record
school_sample = next((s for s in school_data if s['total_suspensions'] > 50), school_data[0])
print(f"\n{school_sample['school_name']} ({school_sample['school_number']}) - {school_sample['suspension_type']}:")
print(f"  Total: {school_sample['total_suspensions']}")
print(f"\n  Demographics:")
print(f"    Male: {school_sample['male']} ({school_sample['male_pct']}%)")
print(f"    Female: {school_sample['female']} ({school_sample['female_pct']}%)")
print(f"    Black: {school_sample['black']} ({school_sample['black_pct']}%)")
print(f"    White: {school_sample['white']} ({school_sample['white_pct']}%)")
print(f"    Hispanic: {school_sample['hispanic']} ({school_sample['hispanic_pct']}%)")
print(f"    SWD: {school_sample['students_with_disabilities']} ({school_sample['students_with_disabilities_pct']}%)")
print(f"\n  Offense Categories:")
print(f"    Disrespect/Disruption: {school_sample['offense_disrespect_disruption']} ({school_sample['offense_disrespect_disruption_pct']}%)")
print(f"    Attacks/Threats/Fighting: {school_sample['offense_attacks_threats_fighting']} ({school_sample['offense_attacks_threats_fighting_pct']}%)")
print(f"    Attendance: {school_sample['offense_attendance']} ({school_sample['offense_attendance_pct']}%)")

print("\n✓ All percentages added successfully!")
