"""
Parse MSDE Suspension PDFs to extract student counts for Eastern Shore counties
"""

import PyPDF2
import re
import pandas as pd
from pathlib import Path
import json

def extract_county_schools(text, county_name):
    """Extract school-level suspension data for a county"""
    
    # Find the county section - look for county name followed by school data
    # The format is: "School Name \nSchool Number All <numbers>"
    schools = []
    
    # Find all instances of school_number + "All" + numbers pattern
    # Example: "0801 All 58 14 6 0 6 0 0 30 2"
    pattern = r'(\d{4})\s+All\s+([\d\s]+)'
    
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        # Check if this line is in the county section
        if county_name in line:
            # Start looking for schools after finding county name
            for j in range(i, min(i + 500, len(lines))):  # Look ahead up to 500 lines
                current_line = lines[j]
                
                # Stop if we hit another county
                if 'County' in current_line and county_name not in current_line and j > i + 5:
                    break
                
                # Look for school number + "All" pattern
                school_match = re.search(r'(\d{4})\s+All\s+([\d\s]+)', current_line)
                if school_match:
                    school_number = school_match.group(1)
                    numbers_str = school_match.group(2)
                    numbers = [int(n) for n in numbers_str.split()]
                    
                    # Extract school name - could be on same line or split across 2 lines
                    school_name = "Unknown"
                    
                    # Check if line starts with "School" + number (name is on previous line)
                    if j > 0 and current_line.strip().startswith('School ' + school_number):
                        # Name is split: "Colonel Richardson High\nSchool 0801 All..."
                        prev_line = lines[j-1].strip()
                        if prev_line and not prev_line.startswith(('Male', 'Female', 'Black', 'Hispanic', 'White', 'Asian', 'Two', 'Students', 'All ')):
                            school_name = prev_line + ' School'
                    else:
                        # Check if school name is before the number on the same line
                        parts_before = current_line.split(school_number)[0].strip()
                        if parts_before and not parts_before.startswith(('Male', 'Female', 'Black', 'Hispanic', 'White', 'Asian', 'Two', 'Students', 'All ', 'School ')):
                            school_name = parts_before
                        elif j > 0:
                            # Try previous line
                            prev_line = lines[j-1].strip()
                            if prev_line and not prev_line.startswith(('Male', 'Female', 'Black', 'Hispanic', 'White', 'Asian', 'Two', 'Students', 'All ')):
                                school_name = prev_line
                    
                    # Final cleanup
                    school_name = school_name.strip()
                    
                    if numbers and school_name != "Unknown":
                        current_school = {
                            'county': county_name,
                            'school_name': school_name.strip(),
                            'school_number': school_number,
                            'total_suspensions': numbers[0] if len(numbers) > 0 else 0,
                        }
                        
                        # Parse demographics from following lines
                        for k in range(j+1, min(j+20, len(lines))):
                            demo_line = lines[k].strip()
                            
                            # Stop at next school
                            if re.search(r'\d{4}\s+All', demo_line):
                                break
                            
                            # Extract demographic data
                            if demo_line.startswith('Male ') and 'Female' not in demo_line:
                                nums = re.findall(r'\d+', demo_line)
                                if nums:
                                    current_school['male'] = int(nums[0])
                            elif demo_line.startswith('Female '):
                                nums = re.findall(r'\d+', demo_line)
                                if nums:
                                    current_school['female'] = int(nums[0])
                            elif 'Black or African American' in demo_line:
                                nums = re.findall(r'\d+', demo_line)
                                if nums:
                                    current_school['black'] = int(nums[0])
                            elif demo_line.startswith('Hispanic '):
                                nums = re.findall(r'\d+', demo_line)
                                if nums:
                                    current_school['hispanic'] = int(nums[0])
                            elif demo_line.startswith('White '):
                                nums = re.findall(r'\d+', demo_line)
                                if nums:
                                    current_school['white'] = int(nums[0])
                            elif demo_line.startswith('Asian '):
                                nums = re.findall(r'\d+', demo_line)
                                if nums:
                                    current_school['asian'] = int(nums[0])
                            elif 'Two or more races' in demo_line:
                                nums = re.findall(r'\d+', demo_line)
                                if nums:
                                    current_school['two_or_more'] = int(nums[0])
                            elif 'Students with Disabilities' in demo_line:
                                nums = re.findall(r'\d+', demo_line)
                                if nums:
                                    current_school['students_with_disabilities'] = int(nums[0])
                            elif 'Economically Disadvantaged' in demo_line:
                                nums = re.findall(r'\d+', demo_line)
                                if nums:
                                    current_school['economically_disadvantaged'] = int(nums[0])
                        
                        schools.append(current_school)
            
            break  # Found county, done searching
    
    return schools

def parse_pdf(pdf_path, suspension_type):
    """Parse suspension PDF and extract data"""
    print(f"\nParsing: {pdf_path}")
    print(f"Suspension type: {suspension_type}")
    
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        
        # Eastern Shore counties
        counties = ['Talbot', 'Kent', 'Dorchester', 'Caroline', "Queen Anne's"]
        
        all_schools = []
        
        # Search through all pages
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            
            # Check if this page has data for any of our counties
            for county in counties:
                if f'{county} County' in text and 'School Name' in text:
                    print(f"\n✓ Processing {county} County (page {page_num + 1})...")
                    schools = extract_county_schools(text, county)
                    
                    if schools:
                        print(f"  ✓ Found {len(schools)} schools on this page")
                        for school in schools:
                            school['suspension_type'] = suspension_type
                            school['county'] = county if county != "Queen Anne" else "Queen Anne's"
                        all_schools.extend(schools)
    
    return all_schools

def main():
    print("="*80)
    print("MSDE SUSPENSION DATA PARSER")
    print("="*80)
    
    # Parse both PDFs
    inschool_data = parse_pdf('suspension_data_inschool_2024.pdf', 'in_school')
    outschool_data = parse_pdf('suspension_data_outofschool_2024.pdf', 'out_of_school')
    
    # Combine data
    all_data = inschool_data + outschool_data
    
    print(f"\n{'='*80}")
    print(f"RESULTS")
    print(f"{'='*80}")
    print(f"Total schools extracted: {len(all_data)}")
    print(f"  - In-school suspensions: {len(inschool_data)}")
    print(f"  - Out-of-school suspensions: {len(outschool_data)}")
    
    # Save to CSV and JSON
    if all_data:
        df = pd.DataFrame(all_data)
        
        output_csv = 'eastern_shore_suspensions_2023_2024.csv'
        output_json = 'eastern_shore_suspensions_2023_2024.json'
        
        df.to_csv(output_csv, index=False)
        
        with open(output_json, 'w') as f:
            json.dump(all_data, f, indent=2)
        
        print(f"\n✓ Saved to: {output_csv}")
        print(f"✓ Saved to: {output_json}")
        
        # Show summary by county
        print(f"\n{'='*80}")
        print("SUMMARY BY COUNTY")
        print(f"{'='*80}")
        for county in df['county'].unique():
            county_data = df[df['county'] == county]
            print(f"\n{county} County:")
            print(f"  Schools: {len(county_data)}")
            print(f"  Total suspensions: {county_data['total_suspensions'].sum()}")

if __name__ == "__main__":
    main()
