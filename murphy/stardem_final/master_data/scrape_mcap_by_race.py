from playwright.sync_api import sync_playwright
import json
import time
import re
import os
import csv

# District codes
districts = {
    'Caroline': '05',
    'Dorchester': '09',
    'Kent': '14',
    'Queen Anne\'s': '17',
    'Talbot': '20'
}

# Race codes for Maryland Report Card (position 5 in URL)
race_codes = {
    'White': '12',
    'Black': '10', 
    'Hispanic': '7'
}

# Subject codes
subjects = {
    'ELA': 'AELAA',  # ELA All Grades
    'Math': 'AMATA'   # Math All Grades
}

# Create downloads directory
download_dir = '/workspaces/jour329w_fall2025/murphy/stardem_final/master_data/downloads'
os.makedirs(download_dir, exist_ok=True)

def extract_pl34_from_csv(csv_path):
    """Extract PL 3/4 value from downloaded CSV"""
    try:
        with open(csv_path, 'r') as f:
            lines = f.readlines()
            
            # Find the header line (contains "Year,Performance Level")
            for i, line in enumerate(lines):
                if line.startswith('Year,Performance Level'):
                    # Parse from this line forward
                    reader = csv.DictReader(lines[i:])
                    for row in reader:
                        perf_level = row.get('Performance Level', '').strip()
                        if perf_level == 'PL 3/4':
                            # Get the result column - look for any column with "Result (%)"
                            for key, value in row.items():
                                if 'Result (%)' in key:
                                    return float(value.strip())
                    break
    except Exception as e:
        print(f"      Error parsing CSV: {e}")
    return None

def scrape_mcap_by_race():
    results = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        
        for county, district_code in districts.items():
            print(f"\nProcessing {county} County...")
            results[county] = {}
            
            for race_name, race_code in race_codes.items():
                print(f"  Scraping {race_name} students...")
                results[county][race_name] = {}
                
                for subject_name, subject_code in subjects.items():
                    # URL format with race parameter in position 5
                    # Pattern: /Graphs/#/Assessments/{subject}/{assessment_type}/A/{race_code}/3/1/{district}/XXXX/2025
                    url = f'https://reportcard.msde.maryland.gov/Graphs/#/Assessments/{"ElaPerformance" if subject_name == "ELA" else "MathPerformance"}/{subject_code}/A/{race_code}/3/1/{district_code}/XXXX/2025'
                    
                    try:
                        print(f"    {subject_name}: {url}")
                        page.goto(url, wait_until='networkidle', timeout=20000)
                        time.sleep(3)  # Wait for page to fully load
                        
                        # Download CSV
                        csv_filename = f'{county}_{race_name}_{subject_name}.csv'
                        csv_path = os.path.join(download_dir, csv_filename)
                        
                        with page.expect_download() as download_info:
                            page.click('text=Download CSV', timeout=10000)
                        
                        download = download_info.value
                        download.save_as(csv_path)
                        
                        # Extract PL 3/4 value from CSV
                        rate = extract_pl34_from_csv(csv_path)
                        
                        if rate is not None:
                            results[county][race_name][subject_name] = rate
                            print(f"      Found: {rate}%")
                            # Clean up CSV file
                            os.remove(csv_path)
                        else:
                            results[county][race_name][subject_name] = "Not found"
                            print(f"      Not found in CSV - keeping file for inspection")
                            # Keep the first failed file for debugging
                            if not os.path.exists(os.path.join(download_dir, 'debug.csv')):
                                os.rename(csv_path, os.path.join(download_dir, 'debug.csv'))
                    
                    except Exception as e:
                        print(f"      Error: {str(e)}")
                        results[county][race_name][subject_name] = f"Error: {str(e)}"
                    
                    time.sleep(1)  # Rate limiting
        
        browser.close()
    
    return results

if __name__ == "__main__":
    print("Scraping MCAP data by race (White, Black, Hispanic)...")
    print("=" * 70)
    
    data = scrape_mcap_by_race()
    
    # Save to JSON
    output_file = '/workspaces/jour329w_fall2025/murphy/stardem_final/master_data/mcap_by_race.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("\n" + "=" * 70)
    print(f"\nResults saved to {output_file}")
    print("\nSummary:")
    for county, races in data.items():
        print(f"\n{county}:")
        for race, subjects in races.items():
            print(f"  {race}: ELA={subjects.get('ELA', 'N/A')}%, Math={subjects.get('Math', 'N/A')}%")
