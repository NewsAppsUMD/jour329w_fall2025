import pdfplumber
import json
import re

# Counties we care about
target_counties = ['Talbot', 'Kent', 'Dorchester', 'Caroline', "Queen Anne's"]

# Map county names to codes
county_codes = {
    '14': 'Talbot',
    '12': 'Kent',
    '10': 'Dorchester',
    '06': 'Caroline',
    '15': "Queen Anne's"
}

def clean_number(value):
    """Convert string numbers to integers, handle * for suppressed data"""
    if value is None or value == '' or value == '*':
        return 0
    try:
        return int(str(value).replace(',', '').strip())
    except:
        return 0

def extract_school_suspensions(pdf_path, suspension_type):
    """Extract school-level suspension data from PDF by aggregating across offense categories"""
    school_data = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        current_school = None
        current_school_num = None
        current_school_county = None
        
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            
            for table in tables:
                if not table:
                    continue
                
                for row_idx, row in enumerate(table):
                    if not row or len(row) < 3:
                        continue
                    
                    # Check if this is a school header row
                    school_name = str(row[0]).strip() if row[0] else ""
                    school_num = str(row[1]).strip() if row[1] else ""
                    
                    # If we have a valid school number (4 digits), this is a new school
                    if school_num and len(school_num) == 4 and school_num.isdigit():
                        county_code = school_num[:2]
                        county = county_codes.get(county_code)
                        
                        if county in target_counties:
                            current_school = school_name
                            current_school_num = school_num
                            current_school_county = county
                            
                            # Initialize school data
                            if school_num not in school_data:
                                school_data[school_num] = {
                                    'county': county,
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
                                    'students_with_disabilities': 0
                                }
                        else:
                            current_school = None
                            current_school_num = None
                            current_school_county = None
                        continue
                    
                    # If we're tracking a school, process demographic rows
                    if current_school_num and current_school_county:
                        desc = str(row[2] if len(row) > 2 else row[0]).strip().lower() if len(row) > 0 else ""
                        
                        # Get the total column (usually column 3)
                        total_col_idx = 3 if len(row) > 3 else 1
                        total = clean_number(row[total_col_idx] if len(row) > total_col_idx else 0)
                        
                        if total == 0:
                            continue
                        
                        # Map demographic descriptions to fields
                        if desc == 'all':
                            school_data[current_school_num]['total_suspensions'] += total
                        elif desc == 'male':
                            school_data[current_school_num]['male'] += total
                        elif desc == 'female':
                            school_data[current_school_num]['female'] += total
                        elif 'asian' in desc:
                            school_data[current_school_num]['asian'] += total
                        elif 'black' in desc or 'african american' in desc:
                            school_data[current_school_num]['black'] += total
                        elif 'hispanic' in desc:
                            school_data[current_school_num]['hispanic'] += total
                        elif desc == 'white':
                            school_data[current_school_num]['white'] += total
                        elif 'two or more' in desc:
                            school_data[current_school_num]['two_or_more'] += total
                        elif 'disabilities' in desc:
                            school_data[current_school_num]['students_with_disabilities'] += total
    
    return list(school_data.values())

print("Extracting in-school suspension data...")
in_school_data = extract_school_suspensions('suspension_pdfs/in_school_suspensions.pdf', 'in_school')
print(f"Found {len(in_school_data)} schools with in-school suspensions")

print("\nExtracting out-of-school suspension data...")
out_of_school_data = extract_school_suspensions('suspension_pdfs/out_of_school_suspensions.pdf', 'out_of_school')
print(f"Found {len(out_of_school_data)} schools with out-of-school suspensions")

# Combine all data
all_data = in_school_data + out_of_school_data

# Filter out records with 0 suspensions
all_data = [record for record in all_data if record['total_suspensions'] > 0]

# Sort by county and school
all_data.sort(key=lambda x: (x['county'], x['school_number'], x['suspension_type']))

# Save to JSON
with open('eastern_shore_suspensions_2023_2024.json', 'w') as f:
    json.dump(all_data, f, indent=2)

print(f"\n✓ Total records: {len(all_data)}")
print(f"✓ Saved to eastern_shore_suspensions_2023_2024.json")

# Show summary by county
print("\nRecords by county:")
for county in target_counties:
    county_records = [r for r in all_data if r['county'] == county]
    schools = len(set(r['school_number'] for r in county_records))
    in_school = sum(r['total_suspensions'] for r in county_records if r['suspension_type'] == 'in_school')
    out_school = sum(r['total_suspensions'] for r in county_records if r['suspension_type'] == 'out_of_school')
    print(f"  {county}: {schools} schools, {in_school} in-school, {out_school} out-of-school")

# Show sample records
if all_data:
    print("\nSample records:")
    for i in range(min(3, len(all_data))):
        print(f"\n{all_data[i]['school_name']} ({all_data[i]['school_number']}) - {all_data[i]['suspension_type']}:")
        print(f"  Total: {all_data[i]['total_suspensions']}")
        print(f"  Male: {all_data[i]['male']}, Female: {all_data[i]['female']}")
        print(f"  Black: {all_data[i]['black']}, White: {all_data[i]['white']}, Hispanic: {all_data[i]['hispanic']}")
