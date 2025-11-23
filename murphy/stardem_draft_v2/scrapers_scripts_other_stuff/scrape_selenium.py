#!/usr/bin/env python3
"""
Selenium-based scraper for Maryland Report Card demographics.
Waits for JavaScript to load and extracts the actual table data.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time

DISTRICTS = {
    'Talbot': '20',
    'Kent': '14',
    'Dorchester': '10',
    'Caroline': '07',
    "Queen Anne's": '18'
}

def scrape_district(driver, county, lss_code):
    """Scrape enrollment demographics for one district."""
    
    print(f"\n{'='*70}")
    print(f"Scraping {county} County (LSS: {lss_code})")
    print('='*70)
    
    url = f"https://reportcard.msde.maryland.gov/Graphs/#/Demographics/DemoEnrollment/2/17/1/{lss_code}/XXXX"
    
    try:
        print(f"Loading: {url}")
        driver.get(url)
        
        # Wait for page to load
        print("Waiting for page to load...")
        time.sleep(8)  # Give Angular time to initialize
        
        # Click "Show Table"
        print("Looking for Show Table button...")
        try:
            # Find the tableHeader div
            table_header = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "tableHeader"))
            )
            print("  Clicking Show Table...")
            table_header.click()
            time.sleep(3)
        except Exception as e:
            print(f"  Could not click Show Table: {e}")
        
        # Now extract the data
        print("Extracting data...")
        
        # Try to find the table
        try:
            table_area = driver.find_element(By.CLASS_NAME, "tableArea")
            
            # Check if there's a table element
            tables = table_area.find_elements(By.TAG_NAME, "table")
            
            if tables:
                print(f"  Found {len(tables)} table(s)")
                
                result_data = {
                    'county': county,
                    'lss_code': lss_code,
                    'tables': []
                }
                
                for idx, table in enumerate(tables):
                    print(f"  Processing table {idx + 1}...")
                    
                    rows = table.find_elements(By.TAG_NAME, "tr")
                    table_data = []
                    headers = []
                    
                    for row_idx, row in enumerate(rows):
                        cells = row.find_elements(By.TAG_NAME, "td") + row.find_elements(By.TAG_NAME, "th")
                        cell_values = [cell.text.strip() for cell in cells]
                        
                        if row_idx == 0 and cell_values:
                            headers = cell_values
                            print(f"    Headers: {headers}")
                        elif cell_values and any(cell_values):
                            row_dict = dict(zip(headers if headers else [f"col_{i}" for i in range(len(cell_values))], cell_values))
                            table_data.append(row_dict)
                    
                    result_data['tables'].append({
                        'headers': headers,
                        'data': table_data
                    })
                    print(f"    ✓ {len(table_data)} rows extracted")
                
                return result_data
            else:
                # No table, try to get raw text
                text = table_area.text
                print(f"  No table elements, got {len(text)} chars of text")
                return {
                    'county': county,
                    'lss_code': lss_code,
                    'raw_text': text
                }
                
        except Exception as e:
            print(f"  Error extracting table: {e}")
            return {
                'county': county,
                'lss_code': lss_code,
                'error': str(e)
            }
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {
            'county': county,
            'lss_code': lss_code,
            'error': str(e)
        }

def main():
    print("="*70)
    print("Maryland Report Card - Selenium Scraper")
    print("="*70)
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    print("\nStarting Chrome...")
    driver = webdriver.Chrome(options=chrome_options)
    
    results = []
    
    try:
        for county, lss_code in DISTRICTS.items():
            data = scrape_district(driver, county, lss_code)
            results.append(data)
            time.sleep(2)
    
    finally:
        driver.quit()
        print("\n✓ Browser closed")
    
    # Save results
    output_file = 'district_demographics_enrollment.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✅ Scraping complete!")
    print(f"{'='*70}")
    print(f"Results saved to: {output_file}")
    
    # Summary
    for result in results:
        county = result['county']
        if 'tables' in result and result['tables']:
            total_rows = sum(len(t['data']) for t in result['tables'])
            print(f"  {county}: ✓ {len(result['tables'])} table(s), {total_rows} total rows")
        elif 'raw_text' in result:
            print(f"  {county}: ⚠ Got text ({len(result['raw_text'])} chars)")
        else:
            print(f"  {county}: ✗ No data")

if __name__ == "__main__":
    main()
