"""Scrape board of education pages for each district"""

from playwright.sync_api import sync_playwright
import json

# URLs for board pages
BOARD_PAGES = {
    'Talbot': 'https://www.tcps.k12.md.us/page/board-of-education',
    'Kent': 'https://www.kent.k12.md.us/page/board-of-education',
    'Dorchester': 'https://www.dcpsmd.org/page/board-of-education',
    'Caroline': 'https://www.carolineschools.org/page/board-of-education',
    "Queen Anne's": 'https://www.qacps.org/board-of-education/'
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    
    board_content = {}
    
    for county, url in BOARD_PAGES.items():
        print(f"\nScraping {county} Board of Education...")
        page = context.new_page()
        
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=20000)
            page.wait_for_timeout(3000)
            
            content = page.locator('body').inner_text()
            board_content[county] = content
            
            # Save screenshot
            page.screenshot(path=f'{county.lower().replace(" ", "_")}_board.png', full_page=True)
            print(f"  ✓ Saved ({len(content)} chars)")
            
        except Exception as e:
            print(f"  ERROR: {e}")
            board_content[county] = None
        
        page.close()
    
    browser.close()
    
    # Save all content
    with open('board_pages_content.json', 'w', encoding='utf-8') as f:
        json.dump(board_content, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Saved to board_pages_content.json")
    
    # Print first 500 chars of each
    for county, content in board_content.items():
        if content:
            print(f"\n{county}:")
            print(content[:800])
