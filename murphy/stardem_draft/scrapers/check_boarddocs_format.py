#!/usr/bin/env python3
"""
Manually navigate BoardDocs to see meeting listings.
"""

import asyncio
from playwright.async_api import async_playwright

async def check_boarddocs():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Non-headless to see
        page = await browser.new_page()
        
        # Check Queen Anne's since we know it has meetings
        url = 'https://go.boarddocs.com/mabe/qacps/Board.nsf/Public'
        print(f"Navigating to: {url}")
        
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await asyncio.sleep(3)
        
        # Get full text
        text = await page.locator('body').inner_text()
        
        print("\n" + "="*60)
        print("PAGE CONTENT:")
        print("="*60)
        print(text[:2000])
        
        # Save to file
        with open('boarddocs_sample.txt', 'w') as f:
            f.write(text)
        
        print("\nFull content saved to: boarddocs_sample.txt")
        print("\nPress Enter to continue...")
        
        # Keep browser open
        await asyncio.sleep(30)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_boarddocs())
