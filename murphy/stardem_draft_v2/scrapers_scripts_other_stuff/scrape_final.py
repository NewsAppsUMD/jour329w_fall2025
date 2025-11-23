#!/usr/bin/env python3
"""
Final working version - waits for the hide class to be removed from tableData.
"""

import asyncio
import json
from playwright.async_api import async_playwright

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
        await asyncio.sleep(5)
        
        demographic_data = {
            "county": county,
            "lss_code": lss_code,
            "enrollment_data": {}
        }
        
        # Click on the tableHeader div
        print("Clicking 'Show Table'...")
        table_header = page.locator('div.tableHeader')
        await table_header.click()
        
        # Wait for the 'hide' class to be removed from tableData
        print("Waiting for table to appear...")
        await asyncio.sleep(3)
        
        # The tableData div should now not have 'hide' class
        table_data_div = page.locator('div.tableData').first
        
        # Get the class attribute
        class_attr = await table_data_div.get_attribute('class')
        print(f"  tableData classes: {class_attr}")
        
        # Extract content regardless
        table_area = page.locator('div.tableArea').first
        table_text = await table_area.inner_text()
        
        if table_text.strip():
            print(f"  ✓ Got table text ({len(table_text)} chars)")
            demographic_data["enrollment_data"]["raw_text"] = table_text
            
            # Try to parse as table
            tables = await table_area.locator('table').all()
            
            if tables:
                print(f"  Found {len(tables)} table(s)")
                
                for idx, table in enumerate(tables):
                    rows = await table.locator('tr').all()
                    parsed_data = []
                    headers = []
                    
                    for row_idx, row in enumerate(rows):
                        cells = await row.locator('td, th').all()
                        cell_values = []
                        
                        for cell in cells:
                            text = (await cell.inner_text()).strip()
                            cell_values.append(text)
                        
                        if row_idx == 0:
                            headers = cell_values
                            print(f"    Headers: {headers}")
                        elif cell_values and any(cell_values):
                            row_dict = dict(zip(headers, cell_values))
                            parsed_data.append(row_dict)
                    
                    demographic_data["enrollment_data"][f"table_{idx}"] = parsed_data
                    print(f"    ✓ Extracted {len(parsed_data)} rows")
            else:
                # Parse raw text
                lines = [l.strip() for l in table_text.split('\n') if l.strip()]
                demographic_data["enrollment_data"]["lines"] = lines
                print(f"  Parsed {len(lines)} lines of text")
        else:
            print("  ✗ No table text found")
        
        return demographic_data
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
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
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        for county, lss_code in DISTRICTS.items():
            data = await scrape_district_demographics(page, county, lss_code)
            results.append(data)
            await asyncio.sleep(1)
        
        await browser.close()
    
    output_file = 'district_demographics_enrollment.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✅ Complete! Saved to {output_file}")
    print(f"{'='*70}")
    
    for result in results:
        if result.get('enrollment_data'):
            tables = sum(1 for k in result['enrollment_data'] if 'table_' in k)
            has_data = bool(result['enrollment_data'].get('raw_text') or tables > 0)
            print(f"  {result['county']}: {'✓' if has_data else '✗'} data")

if __name__ == "__main__":
    asyncio.run(main())
