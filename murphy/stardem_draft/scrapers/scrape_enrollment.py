#!/usr/bin/env python3
"""
Scrape enrollment data from Maryland Report Card Demographics tab.
For each school, extract total enrollment from the Demographics section.
"""

import json
import asyncio
from playwright.async_api import async_playwright
import time

async def scrape_enrollment(page, school_url, school_name):
    """
    Navigate to a school's page and extract enrollment from Demographics tab.
    Returns enrollment number as integer or None if not found.
    """
    try:
        print(f"\nProcessing: {school_name}")
        print(f"URL: {school_url}")
        
        # Navigate to school page
        await page.goto(school_url, wait_until='networkidle', timeout=30000)
        await asyncio.sleep(2)
        
        # Click Demographics tab
        try:
            demographics_tab = page.locator('text="Demographics"').first
            await demographics_tab.click()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"  Could not click Demographics tab: {e}")
            return None
        
        # Look for enrollment data - it should be visible on the Demographics page
        # The page structure shows "Enrollment Data (2025)" section
        page_content = await page.content()
        
        # Try to find enrollment number in the page content
        # Look for patterns like "Total: 123" or similar enrollment indicators
        try:
            # Get all text content from the page
            text_content = await page.locator('body').inner_text()
            
            # Look for enrollment patterns
            lines = text_content.split('\n')
            enrollment = None
            
            for i, line in enumerate(lines):
                if 'Enrollment Data' in line or 'Total' in line:
                    # Look in nearby lines for numbers
                    for j in range(max(0, i-2), min(len(lines), i+5)):
                        # Try to extract a number that could be enrollment
                        words = lines[j].strip().split()
                        for word in words:
                            # Clean and check if it's a valid enrollment number
                            cleaned = word.replace(',', '').strip()
                            if cleaned.isdigit():
                                num = int(cleaned)
                                # Reasonable enrollment range: 50-2000
                                if 50 <= num <= 2000:
                                    enrollment = num
                                    print(f"  Found enrollment: {enrollment}")
                                    return enrollment
            
            # If not found, try a different approach - look for table with enrollment
            # Try to click "Show Table" button if it exists
            try:
                show_table_btn = page.locator('text="Show Table"').first
                if await show_table_btn.is_visible(timeout=2000):
                    await show_table_btn.click()
                    await asyncio.sleep(1)
                    
                    # Re-get text content
                    text_content = await page.locator('body').inner_text()
                    lines = text_content.split('\n')
                    
                    # Look again for enrollment
                    for i, line in enumerate(lines):
                        if 'Total' in line or 'Enrollment' in line:
                            for j in range(max(0, i-2), min(len(lines), i+5)):
                                words = lines[j].strip().split()
                                for word in words:
                                    cleaned = word.replace(',', '').strip()
                                    if cleaned.isdigit():
                                        num = int(cleaned)
                                        if 50 <= num <= 2000:
                                            enrollment = num
                                            print(f"  Found enrollment (after Show Table): {enrollment}")
                                            return enrollment
            except:
                pass
            
            if enrollment:
                return enrollment
            else:
                print(f"  Could not extract enrollment number")
                return None
                
        except Exception as e:
            print(f"  Error extracting enrollment: {e}")
            return None
            
    except Exception as e:
        print(f"  Error processing {school_name}: {e}")
        return None

async def main():
    # Load schools list
    with open('schools_list.json', 'r') as f:
        schools = json.load(f)
    
    print(f"Loaded {len(schools)} schools")
    
    results = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for i, school in enumerate(schools, 1):
            print(f"\n[{i}/{len(schools)}]")
            
            enrollment = await scrape_enrollment(
                page, 
                school['url'], 
                school['name']
            )
            
            results.append({
                'school_name': school['name'],
                'county': school['county'],
                'url': school['url'],
                'enrollment': enrollment
            })
            
            # Small delay between requests
            await asyncio.sleep(1)
        
        await browser.close()
    
    # Save results
    with open('enrollment_data.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "="*50)
    print("ENROLLMENT DATA COLLECTION COMPLETE")
    print("="*50)
    
    successful = [r for r in results if r['enrollment'] is not None]
    failed = [r for r in results if r['enrollment'] is None]
    
    print(f"\nTotal schools: {len(results)}")
    print(f"Successfully collected: {len(successful)}")
    print(f"Failed to collect: {len(failed)}")
    
    if successful:
        total_enrollment = sum(r['enrollment'] for r in successful)
        avg_enrollment = total_enrollment / len(successful)
        print(f"\nTotal enrollment (collected schools): {total_enrollment:,}")
        print(f"Average enrollment: {avg_enrollment:.1f}")
    
    if failed:
        print("\nSchools with missing enrollment:")
        for r in failed:
            print(f"  - {r['school_name']} ({r['county']})")
    
    # Save to CSV as well
    import csv
    with open('enrollment_data.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['school_name', 'county', 'enrollment'])
        writer.writeheader()
        for r in results:
            writer.writerow({
                'school_name': r['school_name'],
                'county': r['county'],
                'enrollment': r['enrollment']
            })
    
    print("\nData saved to:")
    print("  - enrollment_data.json")
    print("  - enrollment_data.csv")

if __name__ == "__main__":
    asyncio.run(main())
