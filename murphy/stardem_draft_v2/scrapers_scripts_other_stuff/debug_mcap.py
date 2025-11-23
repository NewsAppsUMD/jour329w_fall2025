#!/usr/bin/env python3
"""
Debug script to understand the MSDE page structure
"""

import asyncio
from playwright.async_api import async_playwright


async def debug_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        url = "https://reportcard.msde.maryland.gov/Graphs/#/Assessments/ElaPerformance/3ELA/3/5/3/1/99/XXXX/2025"
        print(f"Loading: {url}")
        
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(5)
        
        # Take screenshot
        await page.screenshot(path='debug_page.png')
        print("Screenshot saved: debug_page.png")
        
        # Find all select elements
        print("\n=== Finding all select/dropdown elements ===")
        selects = await page.locator("select").all()
        print(f"Found {len(selects)} select elements")
        
        for i, select in enumerate(selects):
            print(f"\nSelect {i}:")
            # Get all options
            options = await select.locator("option").all()
            print(f"  Has {len(options)} options:")
            for opt in options[:10]:  # Show first 10
                text = await opt.text_content()
                value = await opt.get_attribute("value")
                print(f"    - {text} (value: {value})")
        
        # Look for buttons
        print("\n=== Finding buttons ===")
        buttons = await page.locator("button").all()
        print(f"Found {len(buttons)} buttons")
        for i, btn in enumerate(buttons[:10]):
            text = await btn.text_content()
            print(f"  Button {i}: {text}")
        
        # Save page HTML for inspection
        content = await page.content()
        with open('debug_page.html', 'w') as f:
            f.write(content)
        print("\nPage HTML saved: debug_page.html")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_page())
