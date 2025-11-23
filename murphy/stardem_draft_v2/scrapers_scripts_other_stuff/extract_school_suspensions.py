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

def extract_school_suspensions(pdf_path, suspension_type):
    """Extract school-level suspension data"""
    school_records = []
    
    with pdfplumber.open(pdf_path) as pdf:
        current_county = None
        pages_processed = 0
        
        for page_num, page in enumerate(pdf.pages):
            # Progress indicator every 50 pages
            if page_num % 50 == 0:
                print(f"  Processing page {page_num + 1}/{len(pdf.pages)}...")
            
            text = page.extract_text()
            
            if not text:
                continue
            
            # Check for ANY county header to properly reset
            found_county = None
            lines = text.split('\n')[:10]  # Check first 10 lines for county header
            for line in lines:
                if ' County' in line:
                    # Extract county name from the line
                    for county in target_counties:
                        if county in line and 'County' in line:
                            found_county = county
                            current_county = county
                            print(f"  Page {page_num + 1}: Found {county} County")
                            break
                    # If we found a different county, reset
                    if found_county is None and 'County' in line:
                        current_county = None
                    break
            
            if not current_county:
                continue
            
            pages_processed += 1
            
            tables = page.extract_tables()
            
            for table in tables:
                if not table or len(table) < 2:
                    continue
                
                # Check if this is a school-level table (has "School Name" column)
                header = table[0] if table else []
                has_school_column = any('School Name' in str(cell) for cell in header if cell)
                
                if not has_school_column:
                    # Skip county-level tables
                    continue
                
                # Process school-level data
                current_school_data = None
                
                for row in table[1:]:  # Skip header
                    if not row or len(row) < 4:
                        continue
                    
                    school_name = str(row[0]).strip().replace('\n', ' ') if row[0] else ""
                    school_num = str(row[1]).strip() if row[1] else ""
                    desc = str(row[2]).strip().lower() if row[2] else ""
                    total = clean_number(row[3])
                    
                    # Check if this row has a school number (new school)
                    if school_num and len(school_num) == 4 and school_num.isdigit():
                        # Create new school record
                        current_school_data = {
                            'county': current_county,
                            'school_name': school_name,
                            'school_number': school_num,
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
                        school_records.append(current_school_data)
                        
                        # This row also contains demographic data (the "All" row)
                        if desc == 'all' and total > 0:
                            current_school_data['total_suspensions'] = total
                            # Also capture offense categories (columns 4-11)
                            current_school_data['offense_attendance'] = clean_number(row[4]) if len(row) > 4 else 0
                            current_school_data['offense_dangerous_substances'] = clean_number(row[5]) if len(row) > 5 else 0
                            current_school_data['offense_weapons'] = clean_number(row[6]) if len(row) > 6 else 0
                            current_school_data['offense_attacks_threats_fighting'] = clean_number(row[7]) if len(row) > 7 else 0
                            current_school_data['offense_arson_fire_explosives'] = clean_number(row[8]) if len(row) > 8 else 0
                            current_school_data['offense_sex_offenses'] = clean_number(row[9]) if len(row) > 9 else 0
                            current_school_data['offense_disrespect_disruption'] = clean_number(row[10]) if len(row) > 10 else 0
                            current_school_data['offense_other'] = clean_number(row[11]) if len(row) > 11 else 0
                    
                    # Process other demographic rows
                    elif current_school_data and desc and total > 0:
                        if desc == 'male':
                            current_school_data['male'] = total
                        elif desc == 'female':
                            current_school_data['female'] = total
                        elif 'asian' in desc:
                            current_school_data['asian'] = total
                        elif 'black' in desc or 'african american' in desc:
                            current_school_data['black'] = total
                        elif 'hispanic' in desc:
                            current_school_data['hispanic'] = total
                        elif desc == 'white':
                            current_school_data['white'] = total
                        elif 'two or more' in desc:
                            current_school_data['two_or_more'] = total
                        elif 'disabilities' in desc:
                            current_school_data['students_with_disabilities'] = total
        
        print(f"  Processed {pages_processed} relevant pages")
    
    return school_records

print("=" * 60)
print("EXTRACTING SCHOOL-LEVEL SUSPENSION DATA")
print("=" * 60)

print("\nExtracting in-school suspensions by school...")
in_school_data = extract_school_suspensions('suspension_pdfs/in_school_suspensions.pdf', 'in_school')
print(f"✓ Found {len(in_school_data)} school records\n")

print("Extracting out-of-school suspensions by school...")
out_of_school_data = extract_school_suspensions('suspension_pdfs/out_of_school_by_school.pdf', 'out_of_school')
print(f"✓ Found {len(out_of_school_data)} school records\n")

# Combine all data
all_data = in_school_data + out_of_school_data

# Filter out records with 0 total suspensions
all_data = [r for r in all_data if r['total_suspensions'] > 0]

# Sort
all_data.sort(key=lambda x: (x['county'], x['school_number'], x['suspension_type']))

# Save to JSON
with open('school_level_suspensions_2023_2024.json', 'w') as f:
    json.dump(all_data, f, indent=2)

print(f"✓ Saved {len(all_data)} school records to school_level_suspensions_2023_2024.json\n")

# Show summary
print("=" * 60)
print("SCHOOL-LEVEL SUMMARY")
print("=" * 60)
for county in target_counties:
    records = [r for r in all_data if r['county'] == county]
    schools = len(set(r['school_number'] for r in records))
    in_school_total = sum(r['total_suspensions'] for r in records if r['suspension_type'] == 'in_school')
    out_school_total = sum(r['total_suspensions'] for r in records if r['suspension_type'] == 'out_of_school')
    
    print(f"\n{county} County:")
    print(f"  Schools with data: {schools}")
    print(f"  Total in-school suspensions: {in_school_total}")
    print(f"  Total out-of-school suspensions: {out_school_total}")

# Show sample records
print("\n" + "=" * 60)
print("SAMPLE RECORDS")
print("=" * 60)
for county in target_counties[:2]:
    county_records = [r for r in all_data if r['county'] == county]
    if county_records:
        record = county_records[0]
        print(f"\n{record['school_name']} ({record['school_number']}) - {record['suspension_type']}:")
        print(f"  Total: {record['total_suspensions']}")
        print(f"  Demographics: Male: {record['male']}, Female: {record['female']}")
        print(f"  Race: Black: {record['black']}, White: {record['white']}, Hispanic: {record['hispanic']}, Two+: {record['two_or_more']}")
        print(f"  SWD: {record['students_with_disabilities']}")
        print(f"  Top Offenses: Disrespect/Disruption: {record['offense_disrespect_disruption']}, Attacks: {record['offense_attacks_threats_fighting']}, Attendance: {record['offense_attendance']}")
