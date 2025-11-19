"""Scrape all board pages again to get election/appointment dates"""

from playwright.sync_api import sync_playwright
import json

BOARD_URLS = {
    'Talbot': 'https://www.tcps.k12.md.us/page/board-of-education',
    'Kent': 'https://go.boarddocs.com/mabe/kcps/Board.nsf/Public',
    'Dorchester': 'https://go.boarddocs.com/mabe/dcps/Board.nsf/Public',
    'Caroline': 'https://www.carolineschools.org/o/ccps/page/board#members',
    "Queen Anne's": 'https://www.qacps.org/board-of-education/'
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    
    all_info = {}
    
    for county, url in BOARD_URLS.items():
        print(f"\n{'='*60}")
        print(f"{county} County")
        print('='*60)
        
        page = context.new_page()
        
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=20000)
            page.wait_for_timeout(3000)
            
            content = page.locator('body').inner_text()
            
            # Save full content for review
            filename = f'{county.lower().replace(" ", "_")}_board_full.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ Saved to {filename}")
            
            # Look for term/election info
            import re
            term_info = re.findall(r'(term|elected|appointed).*?20[0-9]{2}', content, re.IGNORECASE)
            if term_info:
                print(f"\nFound term info:")
                for info in term_info[:10]:
                    print(f"  - {info}")
            
            all_info[county] = content
            
        except Exception as e:
            print(f"Error: {e}")
        
        page.close()
    
    browser.close()

print("\n" + "="*60)
print("✅ All board pages saved")
print("Check the *_board_full.txt files for detailed term information")
