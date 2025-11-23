#!/usr/bin/env python3
"""
Debug scraper to see the actual HTML structure of the Maryland Report Card page.
"""

import asyncio
from playwright.async_api import async_playwright

async def debug_page():
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        url = "https://reportcard.msde.maryland.gov/Graphs/#/Demographics/DemoEnrollment/2/17/1/20/XXXX"
        
        print(f"\nLoading: {url}")
        await page.goto(url, wait_until='networkidle', timeout=60000)
        
        print("\nWaiting 8 seconds for Angular to load...")
        await asyncio.sleep(8)
        
        # Get the full page HTML
        html = await page.content()
        
        with open('page_html.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ Saved full HTML to page_html.html")
        
        # Get all button text
        print("\n" + "="*70)
        print("All buttons on page:")
        print("="*70)
        buttons = await page.locator('button, a[role="button"], [ng-click]').all()
        for i, btn in enumerate(buttons[:20]):  # First 20 buttons
            try:
                text = await btn.inner_text()
                if text.strip():
                    print(f"{i+1}. {text.strip()[:50]}")
            except:
                pass
        
        # Look for "Show Table" specifically
        print("\n" + "="*70)
        print("Looking for 'Show Table' elements:")
        print("="*70)
        
        locators_to_try = [
            'text="Show Table"',
            'button:has-text("Show Table")',
            'a:has-text("Show Table")',
            '[ng-click*="table"]',
            '*:has-text("Show Table")'
        ]
        
        for locator_str in locators_to_try:
            try:
                elements = await page.locator(locator_str).all()
                print(f"\n{locator_str}: found {len(elements)} element(s)")
                for elem in elements[:3]:
                    html = await elem.evaluate('el => el.outerHTML')
                    print(f"  {html[:150]}")
            except Exception as e:
                print(f"\n{locator_str}: ERROR - {e}")
        
        # Check if data is already visible without clicking
        print("\n" + "="*70)
        print("Checking for existing data elements:")
        print("="*70)
        
        # Look for chart data
        all_text = await page.locator('body').inner_text()
        if 'Asian' in all_text or 'Hispanic' in all_text or 'African American' in all_text:
            print("✓ Demographic keywords found in page text")
            
            # Try to extract data from chart/graph
            print("\nSearching for data in various elements...")
            
            # SVG charts often contain data
            svg_elements = await page.locator('svg').all()
            print(f"Found {len(svg_elements)} SVG elements")
            
            # Check for Angular scope data
            try:
                data = await page.evaluate('''() => {
                    // Try to get Angular scope data
                    const el = document.querySelector('[ng-controller]');
                    if (el && angular) {
                        const scope = angular.element(el).scope();
                        return scope ? scope.$$childHead : null;
                    }
                    return null;
                }''')
                if data:
                    print("\n✓ Found Angular scope data")
                    print(str(data)[:200])
            except Exception as e:
                print(f"\nAngular data extraction failed: {e}")
        
        await browser.close()
        
        print("\n" + "="*70)
        print("✅ Debug complete - check page_html.html for full structure")
        print("="*70)

if __name__ == "__main__":
    asyncio.run(debug_page())
