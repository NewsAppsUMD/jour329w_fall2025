import pdfplumber
import json

target_counties = ['Talbot', 'Kent', 'Dorchester', 'Caroline', "Queen Anne's"]

def clean_number(value):
    if value is None or value == '' or value == '*':
        return 0
    try:
        return int(str(value).replace(',', '').strip())
    except:
        return 0

def extract_county_totals(pdf_path, suspension_type):
    """Extract county-level suspension totals"""
    county_records = []
    
    with pdfplumber.open(pdf_path) as pdf:
        current_county = None
        
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            
            if not text:
                continue
            
            # Check for county header
            for county in target_counties:
                if f'{county} County' in text:
                    current_county = county
                    print(f"Page {page_num + 1}: Found {county} County")
                    break
            
            if not current_county:
                continue
            
            tables = page.extract_tables()
            
            for table in tables:
                if not table or len(table) < 2:
                    continue
                
                # Check if this is a county-level table (no "School Name" column header)
                header = table[0] if table else []
                has_school_column = any('School Name' in str(cell) for cell in header if cell)
                
                if has_school_column:
                    # Skip school-level tables
                    continue
                
                # This is county-level data
                county_record = {
                    'county': current_county,
                    'school_name': f'{current_county} County (All Schools)',
                    'school_number': 'COUNTY',
                    'suspension_type': suspension_type,
                    'total_suspensions': 0,
                    'male': 0,
                    'female': 0,
                    'asian': 0,
                    'black': 0,
                    'hispanic': 0,
                    'white': 0,
                    'two_or_more': 0,
                    'students_with_disabilities': 0,
                    'offense_attendance': 0,
                    'offense_dangerous_substances': 0,
                    'offense_weapons': 0,
                    'offense_attacks_threats_fighting': 0,
                    'offense_arson_fire_explosives': 0,
                    'offense_sex_offenses': 0,
                    'offense_disrespect_disruption': 0,
                    'offense_other': 0
                }
                
                # Process rows
                for row in table[1:]:  # Skip header
                    if not row or len(row) < 2:
                        continue
                    
                    desc = str(row[0]).strip().lower() if row[0] else ""
                    # Total is usually in column 1 for county tables
                    total = clean_number(row[1]) if len(row) > 1 else 0
                    
                    if total == 0 or not desc:
                        continue
                    
                    if desc == 'all':
                        county_record['total_suspensions'] = total
                        # Also capture offense categories (columns 2-9)
                        county_record['offense_attendance'] = clean_number(row[2]) if len(row) > 2 else 0
                        county_record['offense_dangerous_substances'] = clean_number(row[3]) if len(row) > 3 else 0
                        county_record['offense_weapons'] = clean_number(row[4]) if len(row) > 4 else 0
                        county_record['offense_attacks_threats_fighting'] = clean_number(row[5]) if len(row) > 5 else 0
                        county_record['offense_arson_fire_explosives'] = clean_number(row[6]) if len(row) > 6 else 0
                        county_record['offense_sex_offenses'] = clean_number(row[7]) if len(row) > 7 else 0
                        county_record['offense_disrespect_disruption'] = clean_number(row[8]) if len(row) > 8 else 0
                        county_record['offense_other'] = clean_number(row[9]) if len(row) > 9 else 0
                    elif desc == 'male':
                        county_record['male'] = total
                    elif desc == 'female':
                        county_record['female'] = total
                    elif 'asian' in desc:
                        county_record['asian'] = total
                    elif 'black' in desc or 'african american' in desc:
                        county_record['black'] = total
                    elif 'hispanic' in desc:
                        county_record['hispanic'] = total
                    elif desc == 'white':
                        county_record['white'] = total
                    elif 'two or more' in desc:
                        county_record['two_or_more'] = total
                    elif 'disabilities' in desc:
                        county_record['students_with_disabilities'] = total
                
                # Only add if we found data
                if county_record['total_suspensions'] > 0:
                    county_records.append(county_record)
                    current_county = None  # Reset so we don't duplicate
                    break
    
    return county_records

print("=" * 60)
print("EXTRACTING COUNTY-LEVEL SUSPENSION DATA")
print("=" * 60)

print("\nExtracting in-school suspension county totals...")
in_school_data = extract_county_totals('suspension_pdfs/in_school_suspensions.pdf', 'in_school')
print(f"✓ Found {len(in_school_data)} county records\n")

print("Extracting out-of-school suspension county totals...")
out_of_school_data = extract_county_totals('suspension_pdfs/out_of_school_by_school.pdf', 'out_of_school')
print(f"✓ Found {len(out_of_school_data)} county records\n")

# Combine all data
all_data = in_school_data + out_of_school_data

# Sort
all_data.sort(key=lambda x: (x['county'], x['suspension_type']))

# Save to JSON
with open('county_level_suspensions_2023_2024.json', 'w') as f:
    json.dump(all_data, f, indent=2)

print(f"✓ Saved {len(all_data)} county records to county_level_suspensions_2023_2024.json\n")

# Show summary
print("=" * 60)
print("COUNTY-LEVEL SUMMARY")
print("=" * 60)
for county in target_counties:
    records = [r for r in all_data if r['county'] == county]
    
    in_school_rec = next((r for r in records if r['suspension_type'] == 'in_school'), None)
    out_school_rec = next((r for r in records if r['suspension_type'] == 'out_of_school'), None)
    
    print(f"\n{county} County:")
    if in_school_rec:
        print(f"  In-School: {in_school_rec['total_suspensions']} total")
        print(f"    Demographics: Male: {in_school_rec['male']}, Female: {in_school_rec['female']}")
        print(f"    Race: Black: {in_school_rec['black']}, White: {in_school_rec['white']}, Hispanic: {in_school_rec['hispanic']}")
        print(f"    Top Offenses: Disrespect/Disruption: {in_school_rec['offense_disrespect_disruption']}, Attacks: {in_school_rec['offense_attacks_threats_fighting']}, Attendance: {in_school_rec['offense_attendance']}")
    if out_school_rec:
        print(f"  Out-of-School: {out_school_rec['total_suspensions']} total")
        print(f"    Demographics: Male: {out_school_rec['male']}, Female: {out_school_rec['female']}")
        print(f"    Race: Black: {out_school_rec['black']}, White: {out_school_rec['white']}, Hispanic: {out_school_rec['hispanic']}")
        print(f"    Top Offenses: Disrespect/Disruption: {out_school_rec['offense_disrespect_disruption']}, Attacks: {out_school_rec['offense_attacks_threats_fighting']}, Attendance: {out_school_rec['offense_attendance']}")
