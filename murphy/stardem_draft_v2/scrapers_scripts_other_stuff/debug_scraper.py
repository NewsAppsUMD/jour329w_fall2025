#!/usr/bin/env python3
"""
Debug scraper - test one school and save screenshot
"""

import asyncio
from playwright.async_api import async_playwright

async def test_single_school():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Test with Preston Elementary
        url = "https://reportcard.msde.maryland.gov/Graphs/#/Staffing/School/99/05/0401/2024"
        print(f"Navigating to: {url}")
        
        await page.goto(url, wait_until="networkidle", timeout=60000)
        print("Page loaded, waiting 10 seconds for data...")
        await asyncio.sleep(10)
        
        # Take screenshot
        await page.screenshot(path="staffing_page_screenshot.png", full_page=True)
        print("Screenshot saved: staffing_page_screenshot.png")
        
        # Get all text content
        content = await page.content()
        print(f"\nPage content length: {len(content)} characters")
        
        # Save full HTML
        with open("staffing_page_full.html", "w") as f:
            f.write(content)
        print("Full HTML saved: staffing_page_full.html")
        
        # Try to find specific elements
        print("\nLooking for data tables or charts...")
        
        # Check for various possible selectors
        tables = await page.locator("table").all()
        print(f"Found {len(tables)} tables")
        
        charts = await page.locator("[class*='chart']").all()
        print(f"Found {len(charts)} chart elements")
        
        # Look for any text containing numbers
        all_text = await page.locator("body").text_content()
        print(f"\nBody text preview (first 500 chars):\n{all_text[:500]}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_single_school())
