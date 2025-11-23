#!/usr/bin/env python3
"""
Scrape district demographic enrollment data from Maryland Report Card.
Goes to each county's Demographics > Enrollment page and extracts data
by Race/Ethnicity categories.
"""

import asyncio
import json
from playwright.async_api import async_playwright

# District LSS codes for our 5 counties
DISTRICTS = {
    'Talbot': '20',
    'Kent': '14',
    'Dorchester': '10',
    'Caroline': '07',
    "Queen Anne's": '18'
}

async def scrape_district_demographics(page, county, lss_code):
    """Scrape demographic enrollment data for one district."""
    
    print(f"\n{'='*70}")
    print(f"Scraping {county} County (LSS: {lss_code})")
    print('='*70)
    
    url = f"https://reportcard.msde.maryland.gov/Graphs/#/Demographics/DemoEnrollment/2/17/1/{lss_code}/XXXX"
    
    try:
        print(f"Loading: {url}")
        await page.goto(url, wait_until='networkidle', timeout=60000)
        await asyncio.sleep(3)
        
        # Look for the Demographics tab
        print("Navigating to Demographics...")
        try:
            demographics_tab = page.locator('text="Demographics"').first
            await demographics_tab.click(timeout=5000)
            await asyncio.sleep(2)
        except:
            print("Demographics tab not needed or already selected")
        
        # Race/Ethnicity options to collect
        race_categories = [
            "All Students",
            "Asian",
            "Black or African American",
            "Hispanic/Latino of any race",
            "White",
            "Two or more races"
        ]
        
        demographic_data = {
            "county": county,
            "lss_code": lss_code,
            "enrollment_by_race": {}
        }
        
        for race in race_categories:
            print(f"\n  Collecting data for: {race}")
            
            try:
                # Click on the Race/Ethnicity dropdown
                dropdown = page.locator('select[ng-model*="race"], select[name*="race"], label:has-text("Race") + select').first
                await dropdown.select_option(label=race, timeout=5000)
                await asyncio.sleep(2)
                
                # Click "Show Table" button
                show_table_btn = page.locator('button:has-text("Show Table"), a:has-text("Show Table")').first
                await show_table_btn.click(timeout=5000)
                await asyncio.sleep(2)
                
                # Extract table data
                table = page.locator('table').first
                
                # Get all rows
                rows = await table.locator('tr').all()
                
                race_data = []
                for row in rows[1:]:  # Skip header
                    cells = await row.locator('td, th').all()
                    if len(cells) >= 2:
                        cell_texts = []
                        for cell in cells:
                            text = await cell.inner_text()
                            cell_texts.append(text.strip())
                        race_data.append(cell_texts)
                
                demographic_data["enrollment_by_race"][race] = race_data
                print(f"    ✓ Collected {len(race_data)} rows")
                
                # Close table
                close_btn = page.locator('button:has-text("Close"), a:has-text("Hide")').first
                try:
                    await close_btn.click(timeout=3000)
                    await asyncio.sleep(1)
                except:
                    pass
                
            except Exception as e:
                print(f"    ✗ Error collecting {race}: {e}")
                demographic_data["enrollment_by_race"][race] = {"error": str(e)}
        
        return demographic_data
        
    except Exception as e:
        print(f"ERROR: {e}")
        return {
            "county": county,
            "lss_code": lss_code,
            "error": str(e)
        }

async def main():
    results = []
    
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for county, lss_code in DISTRICTS.items():
            data = await scrape_district_demographics(page, county, lss_code)
            results.append(data)
            await asyncio.sleep(2)
        
        await browser.close()
    
    # Save results
    output_file = 'district_demographics_enrollment.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✅ Scraping complete!")
    print(f"{'='*70}")
    print(f"Results saved to: {output_file}")
    print(f"Total districts: {len(results)}")

if __name__ == "__main__":
    asyncio.run(main())
