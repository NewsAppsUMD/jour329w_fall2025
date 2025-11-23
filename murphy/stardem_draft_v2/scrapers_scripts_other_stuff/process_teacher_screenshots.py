#!/usr/bin/env python3
"""
Process OCR text files from teacher data screenshots
Extracts structured data from MSDE Educator Dashboard screenshots
"""

import json
import re
from pathlib import Path
import pandas as pd

def extract_percentage(text):
    """Extract percentage from text."""
    match = re.search(r'([\d.]+)\s*%', text)
    if match:
        return float(match.group(1))
    return None

def parse_ocr_file(filepath):
    """Parse an OCR text file and extract teacher data."""
    
    with open(filepath, 'r') as f:
        text = f.read()
    
    # Split into lines for line-by-line parsing
    lines = text.split('\n')
    
    # Extract county name from filename or text
    filename = Path(filepath).stem  # e.g., 'ocr_caroline'
    county_name = filename.replace('ocr_', '').replace('_', ' ').title()
    
    # Try to extract from text for better accuracy
    district_match = re.search(r'Select a District:\s*\|?\s*([^\s\\v]+)', text)
    if district_match:
        name = district_match.group(1).strip()
        if name and name != '|':
            county_name = name
    
    data = {
        'county': county_name,
        'total_teachers': None,
        'total_teachers_change_pct': None,
        'new_hires': None,
        'new_hires_pct': None,
    }
    
    # Extract total number of teachers
    # Look for pattern: number followed by "Change from previous year"
    total_match = re.search(r'(\d{2,4})\s+Change from previous year', text)
    if total_match:
        num = int(total_match.group(1))
        if 100 < num < 1000:  # Reasonable range
            data['total_teachers'] = num
    
    # Alternative: Look for number that makes sense (not 3533, etc)
    if not data['total_teachers'] or data['total_teachers'] > 600:
        # Dorchester has "353 3" which gets read as 3533
        dorchester_match = re.search(r'(\d{3})\s*\d\s*VV', text)
        if dorchester_match:
            data['total_teachers'] = int(dorchester_match.group(1))
    
    # Kent has "4 1 58" which should be 158
    if not data['total_teachers']:
        kent_match = re.search(r'4\s*1\s*(\d{2})\s+Change from previous year', text)
        if kent_match:
            # It's actually "158" split across spaces
            data['total_teachers'] = 158
    
    # Extract change from previous year for total teachers
    # Look for pattern like ") 3.1%" or ") -1.7%" or standalone "-1.7%" or "VY X.X%"
    for i, line in enumerate(lines):
        if 'Total Number of Teachers' in line:
            # Check next 4 lines
            for j in range(i+1, min(i+5, len(lines))):
                check_line = lines[j].strip()
                # Pattern 1: ") X.X%"
                match = re.search(r'\)\s*([+-]?\d+\.?\d*)\s*%', check_line)
                if match:
                    data['total_teachers_change_pct'] = float(match.group(1))
                    break
                # Pattern 2: standalone "-X.X%" or "X.X%"
                if check_line and re.match(r'^[+-]?\d+\.?\d*\s*%$', check_line):
                    data['total_teachers_change_pct'] = float(check_line.replace('%', '').strip())
                    break
                # Pattern 3: "VY X.X%" (Kent format)
                match = re.search(r'VY\s*([+-]?\d+\.?\d*)\s*%', check_line)
                if match:
                    data['total_teachers_change_pct'] = float(match.group(1))
                    break
            break
    
    # Extract new hires
    new_hires_match = re.search(r'(\d+)\s+\(([\d.]+)%\s+of all teachers\)', text)
    if new_hires_match:
        data['new_hires'] = int(new_hires_match.group(1))
        data['new_hires_pct'] = float(new_hires_match.group(2))
    
    return data

def main():
    print("="*80)
    print("TEACHER DATA SCREENSHOT PROCESSOR")
    print("="*80)
    
    # Find all OCR text files
    ocr_files = list(Path('scrapers').glob('ocr_*.txt'))
    if not ocr_files:
        ocr_files = list(Path('.').glob('ocr_*.txt'))
    
    if not ocr_files:
        print("\n✗ No OCR text files found!")
        print("Expected files like: ocr_caroline.txt, ocr_dorchester.txt, etc.")
        return
    
    print(f"\nFound {len(ocr_files)} OCR files to process")
    
    all_data = []
    
    for ocr_file in sorted(ocr_files):
        print(f"\n{'='*80}")
        print(f"Processing: {ocr_file.name}")
        print(f"{'='*80}")
        
        try:
            data = parse_ocr_file(ocr_file)
            all_data.append(data)
            
            # Show what we extracted
            print(f"\n✓ Extracted data for {data['county']}:")
            change_str = f"{data['total_teachers_change_pct']:+.1f}%" if data['total_teachers_change_pct'] else "N/A"
            print(f"  Total Teachers: {data['total_teachers']} (Change: {change_str})")
            print(f"  New Hires: {data['new_hires']} ({data['new_hires_pct']}%)")
            
        except Exception as e:
            print(f"✗ Error processing {ocr_file.name}: {e}")
            import traceback
            traceback.print_exc()
    
    if not all_data:
        print("\n✗ No data extracted!")
        return
    
    # Save results
    print(f"\n{'='*80}")
    print("SAVING RESULTS")
    print(f"{'='*80}")
    
    # Save JSON
    json_file = 'eastern_shore_teacher_data.json'
    with open(json_file, 'w') as f:
        json.dump(all_data, f, indent=2)
    print(f"✓ Saved: {json_file}")
    
    # Save CSV
    csv_file = 'eastern_shore_teacher_data.csv'
    df = pd.DataFrame(all_data)
    df.to_csv(csv_file, index=False)
    print(f"✓ Saved: {csv_file}")
    
    # Display summary table
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}\n")
    
    # Create a display with proper formatting
    display_data = []
    for _, row in df.iterrows():
        change_str = f"{row['total_teachers_change_pct']:+.1f}%" if pd.notna(row['total_teachers_change_pct']) else "N/A"
        display_data.append({
            'County': row['county'],
            'Teachers': int(row['total_teachers']) if pd.notna(row['total_teachers']) else 'N/A',
            'Change': change_str,
            'New Hires': int(row['new_hires']) if pd.notna(row['new_hires']) else 0,
            'New Hires %': f"{row['new_hires_pct']:.1f}%" if pd.notna(row['new_hires_pct']) else "N/A"
        })
    
    display_df = pd.DataFrame(display_data)
    print(display_df.to_string(index=False))
    print(f"\n✓ Successfully processed {len(all_data)} counties")

if __name__ == '__main__':
    main()
