#!/usr/bin/env python3
"""
Scrape mental health professional staffing data from MSDE Report Card
for all Eastern Shore schools using Playwright.
"""

import json
import time
import re
import asyncio
from playwright.async_api import async_playwright

async def scrape_school_staffing(page, school):
    """Scrape staffing data for a single school."""
    county = school['county']
    code = school['full_code']
    name = school['name']
    
    try:
        # Navigate to school staffing page
        county_code = code[:2]
        school_code = code[2:]
        url = f"https://reportcard.msde.maryland.gov/Graphs/#/Staffing/School/99/{county_code}/{school_code}/2024"
        
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(3)  # Wait for JavaScript to fully load
        
        staff_data = {
            'county': county,
            'school_code': code,
            'school_name': name,
            'counselors': None,
            'psychologists': None,
            'social_workers': None,
            'nurses': None,
            'total_staff': None
        }
        
        # Get page content
        content = await page.content()
        content_lower = content.lower()
        
        # Try to find staffing data in the page
        # Look for patterns like "Counselor" followed by a number
        
        # Method 1: Search for text containing staffing categories
        if 'counselor' in content_lower or 'guidance' in content_lower:
            counselor_elements = await page.locator("text=/counselor/i").all()
            for elem in counselor_elements:
                text = await elem.text_content()
                numbers = re.findall(r'\b\d+\.?\d*\b', text)
                if numbers:
                    try:
                        staff_data['counselors'] = float(numbers[0])
                        break
                    except:
                        pass
        
        if 'psychologist' in content_lower:
            psych_elements = await page.locator("text=/psychologist/i").all()
            for elem in psych_elements:
                text = await elem.text_content()
                numbers = re.findall(r'\b\d+\.?\d*\b', text)
                if numbers:
                    try:
                        staff_data['psychologists'] = float(numbers[0])
                        break
                    except:
                        pass
        
        if 'social worker' in content_lower or 'social' in content_lower:
            social_elements = await page.locator("text=/social.*worker/i").all()
            for elem in social_elements:
                text = await elem.text_content()
                numbers = re.findall(r'\b\d+\.?\d*\b', text)
                if numbers:
                    try:
                        staff_data['social_workers'] = float(numbers[0])
                        break
                    except:
                        pass
        
        if 'nurse' in content_lower:
            nurse_elements = await page.locator("text=/nurse/i").all()
            for elem in nurse_elements:
                text = await elem.text_content()
                numbers = re.findall(r'\b\d+\.?\d*\b', text)
                if numbers:
                    try:
                        staff_data['nurses'] = float(numbers[0])
                        break
                    except:
                        pass
        
        return staff_data, None
        
    except Exception as e:
        return None, f"Error: {str(e)}"

async def main():
    # Load schools
    with open('all_eastern_shore_schools.json', 'r') as f:
        schools = json.load(f)
    
    print(f"Starting to scrape mental health staffing data for {len(schools)} schools...")
    print("This may take 10-15 minutes...\n")
    
    results = []
    errors = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for i, school in enumerate(schools, 1):
            print(f"[{i}/{len(schools)}] {school['name']} ({school['full_code']})...", end=" ", flush=True)
            
            staff_data, error = await scrape_school_staffing(page, school)
            
            if error:
                errors.append(f"{school['name']} ({school['full_code']}): {error}")
                print(f"✗ {error[:30]}")
            else:
                results.append(staff_data)
                print("✓")
            
            # Be nice to the server
            await asyncio.sleep(1)
        
        await browser.close()
    
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
                'total_social_workers': 0,
                'total_nurses': 0
            }
        
        summary[county]['schools'] += 1
        if result['counselors']:
            summary[county]['total_counselors'] += result['counselors']
        if result['psychologists']:
            summary[county]['total_psychologists'] += result['psychologists']
        if result['social_workers']:
            summary[county]['total_social_workers'] += result['social_workers']
        if result['nurses']:
            summary[county]['total_nurses'] += result['nurses']
    
    print("\nSummary by County:")
    for county, data in sorted(summary.items()):
        print(f"\n{county}:")
        print(f"  Schools: {data['schools']}")
        print(f"  Counselors: {data['total_counselors']}")
        print(f"  Psychologists: {data['total_psychologists']}")
        print(f"  Social Workers: {data['total_social_workers']}")
        print(f"  Nurses: {data['total_nurses']}")

if __name__ == "__main__":
    asyncio.run(main())
