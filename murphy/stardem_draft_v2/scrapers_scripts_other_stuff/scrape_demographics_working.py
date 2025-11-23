#!/usr/bin/env python3
"""
Working scraper for Maryland Report Card district demographics.
Clicks the correct div.tableHeader element to show the table.
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
        
        # Click on the tableHeader div to show the table
        print("Clicking 'Show Table'...")
        try:
            table_header = page.locator('div.tableHeader')
            await table_header.click(timeout=5000)
            await asyncio.sleep(2)
            print("  ✓ Table toggled")
        except Exception as e:
            print(f"  ✗ Could not click Show Table: {e}")
            return demographic_data
        
        # Extract data from the tableData div that becomes visible
        print("Extracting table data...")
        try:
            # Wait for tableData to become visible
            table_data_div = page.locator('div.tableData')
            
            # Check if it's now visible
            is_visible = await table_data_div.locator('div.tableArea').is_visible(timeout=5000)
            
            if is_visible:
                print("  ✓ Table is now visible")
                
                # Get the table area content
                table_area = table_data_div.locator('div.tableArea')
                table_html = await table_area.inner_html()
                table_text = await table_area.inner_text()
                
                demographic_data["enrollment_data"]["table_html"] = table_html[:500]  # First 500 chars
                demographic_data["enrollment_data"]["table_text"] = table_text
                
                # Try to parse as structured table if there's a <table> element
                tables = await table_area.locator('table').all()
                
                if tables:
                    print(f"  Found {len(tables)} table element(s)")
                    
                    for idx, table in enumerate(tables):
                        rows = await table.locator('tr').all()
                        table_data = []
                        headers = []
                        
                        for row_idx, row in enumerate(rows):
                            cells = await row.locator('td, th').all()
                            cell_values = []
                            
                            for cell in cells:
                                text = await cell.inner_text()
                                cell_values.append(text.strip())
                            
                            if row_idx == 0 and any(cell_values):
                                headers = cell_values
                            elif any(cell_values):
                                row_dict = {}
                                for i, val in enumerate(cell_values):
                                    header = headers[i] if i < len(headers) else f"col_{i}"
                                    row_dict[header] = val
                                table_data.append(row_dict)
                        
                        demographic_data["enrollment_data"][f"table_{idx}"] = {
                            "headers": headers,
                            "rows": table_data
                        }
                        print(f"    ✓ Table {idx}: {len(headers)} columns, {len(table_data)} rows")
                else:
                    print("  No <table> elements found, saved raw text")
            else:
                print("  ✗ Table not visible after click")
        
        except Exception as e:
            print(f"  ✗ Error extracting table: {e}")
            demographic_data["error"] = str(e)
        
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
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()
        
        # Scrape all counties
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
    
    # Print summary
    for result in results:
        county = result.get('county')
        if result.get('enrollment_data'):
            table_count = sum(1 for k in result['enrollment_data'] if k.startswith('table_'))
            print(f"  {county}: {table_count} table(s) extracted")
        else:
            print(f"  {county}: No data extracted")

if __name__ == "__main__":
    asyncio.run(main())
