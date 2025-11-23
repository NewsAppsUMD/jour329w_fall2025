#!/usr/bin/env python3
"""
Scrape district demographic enrollment data from Maryland Report Card.
This version uses a simpler approach - just loads the page and extracts visible data.
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
    
    # Direct URL to Demographics/Enrollment page
    url = f"https://reportcard.msde.maryland.gov/Graphs/#/Demographics/DemoEnrollment/2/17/1/{lss_code}/XXXX"
    
    try:
        print(f"Loading: {url}")
        await page.goto(url, wait_until='domcontentloaded', timeout=60000)
        
        # Wait for page to fully load
        print("Waiting for content to load...")
        await asyncio.sleep(5)
        
        # Try to find and click "Show Table" if it exists
        print("Looking for table data...")
        
        # Check if there's already a chart/graph with data
        page_content = await page.content()
        
        # Try to extract any visible enrollment numbers
        print("Extracting page content...")
        
        # Look for specific demographic data elements
        demographic_data = {
            "county": county,
            "lss_code": lss_code,
            "url": url,
            "page_title": await page.title(),
            "raw_data": {}
        }
        
        # Try to find demographic breakdown
        try:
            # Look for any text that might contain enrollment data
            all_text = await page.locator('body').inner_text()
            demographic_data["page_text_sample"] = all_text[:500]  # First 500 chars
            
            # Look for specific elements
            charts = await page.locator('[class*="chart"], [class*="graph"], [id*="chart"], [id*="graph"]').count()
            tables = await page.locator('table').count()
            
            print(f"  Found {charts} chart elements, {tables} table elements")
            demographic_data["elements_found"] = {"charts": charts, "tables": tables}
            
            # If tables exist, try to extract them
            if tables > 0:
                print("  Extracting table data...")
                for i in range(min(tables, 3)):  # Max 3 tables
                    table = page.locator('table').nth(i)
                    table_text = await table.inner_text()
                    demographic_data["raw_data"][f"table_{i}"] = table_text
                    print(f"    Table {i}: {len(table_text)} chars")
            
        except Exception as e:
            print(f"  Error extracting elements: {e}")
            demographic_data["extraction_error"] = str(e)
        
        # Take a screenshot for debugging
        screenshot_path = f"debug_{county.replace(' ', '_').lower()}.png"
        await page.screenshot(path=screenshot_path)
        print(f"  Screenshot saved: {screenshot_path}")
        
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
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()
        
        # Test with just one county first
        test_county = 'Talbot'
        test_lss = DISTRICTS[test_county]
        
        print(f"\n🔍 Testing with {test_county} County first...")
        data = await scrape_district_demographics(page, test_county, test_lss)
        results.append(data)
        
        await browser.close()
    
    # Save results
    output_file = 'district_demographics_debug.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✅ Debug scraping complete!")
    print(f"{'='*70}")
    print(f"Results saved to: {output_file}")
    print("\nPlease check the debug screenshot and JSON to see what's on the page.")

if __name__ == "__main__":
    asyncio.run(main())
