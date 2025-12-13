#!/usr/bin/env python3
"""
Modified demographics scraper to support multiple years
Usage: python demographics_multi_year.py --years 2025 2024 2023 2022
"""

from playwright.sync_api import sync_playwright
import pandas as pd
import json
import time
import re
import os
import argparse

CHECKPOINT_FILE = 'scraper_checkpoint_multi_year.json'
ENROLLMENT_DATA_DIR = 'enrollment_data'

def load_checkpoint():
    """Load checkpoint data"""
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    return {'completed': {}}

def save_checkpoint(checkpoint_data):
    """Save checkpoint data"""
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint_data, f, indent=2)
    print(f"✓ Checkpoint saved")

def get_all_schools(page, county_code):
    """
    Get list of all schools from the schools list page for a specific county
    County codes: 05=Caroline, 09=Dorchester, 14=Kent, 17=Queen Anne's, 20=Talbot
    """
    print(f"Fetching school list for county {county_code}...")
    
    try:
        url = f"https://reportcard.msde.maryland.gov/SchoolsList/Index?l={county_code}"
        page.goto(url, wait_until='networkidle', timeout=60000)
        print("Waiting for schools to load...")
        time.sleep(8)
        
        schools = []
        links = page.locator('a').all()
        
        print(f"Scanning {len(links)} links...")
        
        for link in links:
            text = link.text_content().strip()
            match = re.match(r'(.+?)\s*\((\d{4})\)', text)
            if match:
                school_name = match.group(1).strip()
                school_code = match.group(2)
                schools.append({
                    'name': school_name,
                    'code': school_code
                })
                print(f"  Found: {school_name} ({school_code})")
        
        print(f"\nTotal schools found: {len(schools)}")
        return schools
        
    except Exception as e:
        print(f"Error fetching schools: {e}")
        import traceback
        traceback.print_exc()
        return []

def extract_from_table(page, year):
    """Extract enrollment number from the data table for a specific year"""
    try:
        time.sleep(2)
        table = page.locator('table').first
        
        if table.is_visible(timeout=3000):
            rows = table.locator('tr').all()
            
            for row in rows:
                cells = row.locator('td').all()
                if len(cells) >= 3:
                    row_year = cells[0].text_content().strip()
                    group = cells[1].text_content().strip()
                    number = cells[2].text_content().strip()
                    
                    # Check if suppressed data (*)
                    if number.strip() == '*':
                        if row_year == str(year):
                            return '*'
                    
                    # Make sure it's the right year
                    if row_year == str(year) and number.replace(',', '').isdigit():
                        return int(number.replace(',', ''))
        
        # If table not visible, look in the chart text
        body_text = page.locator('body').text_content()
        match = re.search(r'Number of Students[^0-9*]+([0-9*]+|[\*])', body_text)
        if match:
            val = match.group(1).strip()
            if val == '*':
                return '*'
            if val.isdigit():
                return int(val)
                
    except Exception as e:
        print(f"    Error in extract_from_table: {e}")
    
    return None

def scrape_enrollment(page, school_code, school_name, county_code, year):
    """Scrape enrollment data for all demographic breakdowns for a specific year"""
    base_url = f"https://reportcard.msde.maryland.gov/Graphs/#/Demographics/Enrollment/3/17/6/{county_code}/{school_code}/{year}"
    
    enrollment_data = []
    
    demographics = {
        'Race/Ethnicity': [
            'All Students', 'Asian', 'African Am.', 'Hispanic', 'White',
            'Am.Ind/AK', 'HI/Pac.Isl.', '2+'
        ]
    }
    
    print(f"\nNavigating to: {base_url}")
    try:
        page.goto(base_url, wait_until='networkidle', timeout=90000)
        time.sleep(10)
    except Exception as e:
        print(f"⚠ Navigation timeout or error: {e}")
        time.sleep(5)
    
    for category, options in demographics.items():
        print(f"\n--- {category.upper()} ---")
        
        for display_name in options:
            try:
                print(f"Processing: {display_name}")
                
                page.goto(base_url, wait_until='networkidle', timeout=60000)
                time.sleep(5)
                
                script = f"""
                (async function() {{
                    const links = Array.from(document.querySelectorAll('a.cbox__link'));
                    const option = links.find(l => l.textContent.trim() === '{display_name}');
                    
                    if (option) {{
                        const button = option.closest('.cbox').querySelector('button');
                        if (button) {{
                            button.click();
                            await new Promise(r => setTimeout(r, 1000));
                        }}
                        option.click();
                        await new Promise(r => setTimeout(r, 2000));
                        return true;
                    }}
                    return false;
                }})()
                """
                
                result = page.evaluate(script)
                
                if result:
                    time.sleep(3)
                    
                    try:
                        show_table = page.locator('text="Show Table"').first
                        if show_table.is_visible(timeout=2000):
                            show_table.click()
                            time.sleep(2)
                    except:
                        pass
                    
                    enrollment = extract_from_table(page, year)
                    
                    if enrollment:
                        enrollment_data.append({
                            'category': category,
                            'group': display_name,
                            'enrollment': enrollment,
                            'year': str(year)
                        })
                        print(f"  ✓ {display_name}: {enrollment} students")
                    else:
                        print(f"  ✗ Could not extract enrollment")
                else:
                    print(f"  ✗ Could not select option")
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
    
    return enrollment_data

def main():
    parser = argparse.ArgumentParser(description='Scrape MSDE enrollment data for multiple years')
    parser.add_argument('--years', nargs='+', type=int, default=[2025], 
                        help='Years to scrape (e.g., 2025 2024 2023)')
    parser.add_argument('--counties', nargs='+', 
                        choices=['05', '09', '14', '17', '20'],
                        default=['05', '09', '14', '17', '20'],
                        help='County codes to scrape (05=Caroline, 09=Dorchester, 14=Kent, 17=Queen Annes, 20=Talbot)')
    parser.add_argument('--schools', nargs='+',
                        help='Specific school codes to scrape (optional)')
    
    args = parser.parse_args()
    
    os.makedirs(ENROLLMENT_DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(ENROLLMENT_DATA_DIR, 'pngs'), exist_ok=True)
    
    checkpoint = load_checkpoint()
    
    county_names = {
        '05': 'caroline',
        '09': 'dorchester',
        '14': 'kent',
        '17': 'queen_annes',
        '20': 'talbot'
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            for county_code in args.counties:
                county_name = county_names[county_code]
                print(f"\n{'='*60}")
                print(f"COUNTY: {county_name.upper()} ({county_code})")
                print(f"{'='*60}")
                
                # Get schools for this county
                if args.schools:
                    schools = [{'name': f'School {code}', 'code': code} for code in args.schools 
                              if code.startswith(county_code[1])]  # Match second digit
                else:
                    schools = get_all_schools(page, county_code)
                
                if not schools:
                    print(f"⚠ No schools found for county {county_code}")
                    continue
                
                for year in args.years:
                    print(f"\n{'-'*60}")
                    print(f"YEAR: {year}")
                    print(f"{'-'*60}")
                    
                    for school in schools:
                        school_code = school['code']
                        school_name = school['name']
                        
                        checkpoint_key = f"{county_code}_{school_code}_{year}"
                        
                        if checkpoint_key in checkpoint.get('completed', {}):
                            print(f"\n⏭ Skipping {school_name} ({school_code}) - already completed")
                            continue
                        
                        print(f"\n{'*'*60}")
                        print(f"SCHOOL: {school_name} ({school_code})")
                        print(f"YEAR: {year}")
                        print(f"{'*'*60}")
                        
                        try:
                            enrollment_data = scrape_enrollment(page, school_code, school_name, county_code, year)
                            
                            if enrollment_data:
                                # Save individual school file
                                county_dir = os.path.join(ENROLLMENT_DATA_DIR, county_name)
                                os.makedirs(county_dir, exist_ok=True)
                                
                                output_file = os.path.join(county_dir, f'enrollment_{county_code}_{school_code}_{year}.json')
                                
                                school_data = {
                                    'school_name': school_name,
                                    'school_code': school_code,
                                    'county_code': county_code,
                                    'year': str(year),
                                    'enrollment_data': enrollment_data
                                }
                                
                                with open(output_file, 'w') as f:
                                    json.dump(school_data, f, indent=2)
                                
                                print(f"\n✓ Saved to: {output_file}")
                                print(f"  Collected {len(enrollment_data)} data points")
                                
                                # Update checkpoint
                                checkpoint['completed'][checkpoint_key] = True
                                save_checkpoint(checkpoint)
                            else:
                                print(f"\n⚠ No enrollment data collected for {school_name}")
                            
                        except Exception as e:
                            print(f"\n❌ Error processing {school_name}: {e}")
                            import traceback
                            traceback.print_exc()
                
                print(f"\n{'='*60}")
                print(f"Completed county: {county_name.upper()}")
                print(f"{'='*60}")
        
        finally:
            browser.close()
    
    print(f"\n✅ All done!")
    print(f"Data saved to: {ENROLLMENT_DATA_DIR}")

if __name__ == "__main__":
    main()
