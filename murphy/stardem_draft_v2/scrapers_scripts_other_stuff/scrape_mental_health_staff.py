#!/usr/bin/env python3
"""
Scrape mental health professional staffing data from MSDE Report Card
for all Eastern Shore schools.
"""

import json
import time
import re
import asyncio
from playwright.async_api import async_playwright

# Load schools
with open('all_eastern_shore_schools.json', 'r') as f:
    schools = json.load(f)

print(f"Starting to scrape mental health staffing data for {len(schools)} schools...")
print("This may take 10-15 minutes...\n")

# Setup Chrome driver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 20)

results = []
errors = []

for i, school in enumerate(schools, 1):
    county = school['county']
    code = school['full_code']
    name = school['name']
    
    print(f"[{i}/{len(schools)}] {name} ({code})...", end=" ", flush=True)
    
    try:
        # Navigate to school staffing page
        # Format: https://reportcard.msde.maryland.gov/Graphs/#/Staffing/School/99/20/0401/2024
        county_code = code[:2]
        school_code = code[2:]
        url = f"https://reportcard.msde.maryland.gov/Graphs/#/Staffing/School/99/{county_code}/{school_code}/2024"
        
        driver.get(url)
        time.sleep(3)  # Wait for JavaScript to load
        
        # Look for mental health staff data
        # The page structure may vary, so we'll look for common patterns
        
        staff_data = {
            'county': county,
            'school_code': code,
            'school_name': name,
            'counselors': None,
            'psychologists': None,
            'social_workers': None,
            'other_mental_health': None,
            'total_staff': None
        }
        
        # Try to find specific staffing categories
        try:
            # Wait for data to load
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Get page source to search for keywords
            page_source = driver.page_source.lower()
            
            # Look for counselor data
            if 'counselor' in page_source or 'guidance' in page_source:
                # Try to extract the number
                elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Counselor') or contains(text(), 'counselor')]")
                for elem in elements:
                    text = elem.text
                    # Look for numbers near "counselor"
                    import re
                    numbers = re.findall(r'\d+\.?\d*', text)
                    if numbers:
                        staff_data['counselors'] = float(numbers[0])
                        break
            
            # Look for psychologist data
            if 'psychologist' in page_source:
                elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Psychologist') or contains(text(), 'psychologist')]")
                for elem in elements:
                    text = elem.text
                    import re
                    numbers = re.findall(r'\d+\.?\d*', text)
                    if numbers:
                        staff_data['psychologists'] = float(numbers[0])
                        break
            
            # Look for social worker data
            if 'social worker' in page_source or 'social' in page_source:
                elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Social Worker') or contains(text(), 'social worker')]")
                for elem in elements:
                    text = elem.text
                    import re
                    numbers = re.findall(r'\d+\.?\d*', text)
                    if numbers:
                        staff_data['social_workers'] = float(numbers[0])
                        break
            
        except Exception as e:
            print(f"Error extracting data: {e}")
        
        results.append(staff_data)
        print("✓")
        
    except Exception as e:
        error_msg = f"Error for {name} ({code}): {str(e)}"
        errors.append(error_msg)
        print(f"✗ {str(e)[:50]}")
    
    # Be nice to the server
    time.sleep(2)

driver.quit()

# Save results
with open('mental_health_staffing.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n{'='*80}")
print(f"Scraping complete!")
print(f"Schools processed: {len(results)}")
print(f"Errors: {len(errors)}")
print(f"{'='*80}")

if errors:
    print("\nErrors encountered:")
    for error in errors[:10]:
        print(f"  - {error}")

print("\n✓ Saved: mental_health_staffing.json")

# Create summary
summary = {}
for result in results:
    county = result['county']
    if county not in summary:
        summary[county] = {
            'schools': 0,
            'total_counselors': 0,
            'total_psychologists': 0,
            'total_social_workers': 0
        }
    
    summary[county]['schools'] += 1
    if result['counselors']:
        summary[county]['total_counselors'] += result['counselors']
    if result['psychologists']:
        summary[county]['total_psychologists'] += result['psychologists']
    if result['social_workers']:
        summary[county]['total_social_workers'] += result['social_workers']

print("\nSummary by County:")
for county, data in sorted(summary.items()):
    print(f"\n{county}:")
    print(f"  Schools: {data['schools']}")
    print(f"  Counselors: {data['total_counselors']}")
    print(f"  Psychologists: {data['total_psychologists']}")
    print(f"  Social Workers: {data['total_social_workers']}")
