#!/usr/bin/env python3
"""
Manually search Talbot and Caroline websites for board meeting schedules.
"""

import asyncio
from playwright.async_api import async_playwright

async def search_talbot(page):
    """Search Talbot County website for board meeting info."""
    print("\n" + "="*60)
    print("Searching Talbot County website...")
    print("="*60)
    
    # Try main website
    urls_to_try = [
        'https://www.tcps.k12.md.us',
        'https://www.tcps.k12.md.us/about',
        'https://www.tcps.k12.md.us/boe',
    ]
    
    for url in urls_to_try:
        try:
            print(f"\nTrying: {url}")
            await page.goto(url, timeout=15000)
            await asyncio.sleep(2)
            
            # Search for board or meeting links
            text = await page.locator('body').inner_text()
            
            if 'board' in text.lower() or 'meeting' in text.lower():
                print("Found board/meeting content")
                
                # Try to find links
                links = await page.locator('a').all()
                for link in links[:50]:  # Check first 50 links
                    link_text = await link.inner_text()
                    if any(word in link_text.lower() for word in ['board', 'meeting', 'schedule']):
                        href = await link.get_attribute('href')
                        print(f"  Link: {link_text} -> {href}")
                
                # Save content snippet
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if 'board' in line.lower() or 'meeting' in line.lower():
                        print(f"  Content: {line.strip()[:80]}")
                        if i < len(lines) - 1:
                            print(f"           {lines[i+1].strip()[:80]}")
                
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    # Try searching BoardDocs directly with different year
    print("\nTrying Talbot BoardDocs with year selection...")
    try:
        await page.goto('https://go.boarddocs.com/mabe/tcps/Board.nsf/Public', timeout=15000)
        await asyncio.sleep(2)
        
        # Get all year links
        text = await page.locator('body').inner_text()
        print("Available years:", [y for y in text.split('\n') if y.strip().isdigit()])
        
    except Exception as e:
        print(f"  Error: {e}")

async def search_caroline(page):
    """Search Caroline County website for board meeting info."""
    print("\n" + "="*60)
    print("Searching Caroline County website...")
    print("="*60)
    
    urls_to_try = [
        'https://www.carolineschools.org/o/ccps/page/board',
        'https://www.carolineschools.org/calendar',
    ]
    
    for url in urls_to_try:
        try:
            print(f"\nTrying: {url}")
            await page.goto(url, timeout=15000)
            await asyncio.sleep(2)
            
            text = await page.locator('body').inner_text()
            
            # Look for meeting schedule info
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if any(word in line.lower() for word in ['meeting', 'schedule', 'monday', 'tuesday', 'wednesday', 'thursday']):
                    if any(ord in line.lower() for ord in ['1st', '2nd', '3rd', '4th', 'first', 'second', 'third']):
                        print(f"  Found: {line.strip()}")
                        if i < len(lines) - 1:
                            print(f"         {lines[i+1].strip()}")
            
        except Exception as e:
            print(f"  Error: {e}")
            continue

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await search_talbot(page)
        await search_caroline(page)
        
        await browser.close()
    
    print("\n" + "="*60)
    print("Manual search complete")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
