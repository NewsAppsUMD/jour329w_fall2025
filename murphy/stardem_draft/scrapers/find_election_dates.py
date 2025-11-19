"""Search for Talbot, Kent, and Dorchester board member election/appointment dates"""

from playwright.sync_api import sync_playwright
import re

# Try searching recent news, board meeting minutes, and "about" pages
SEARCH_URLS = {
    'Talbot': [
        'https://www.tcps.k12.md.us/page/board-of-education',
        'https://www.tcps.k12.md.us/news'
    ],
    'Kent': [
        'https://www.kent.k12.md.us/',
        'https://go.boarddocs.com/mabe/kcps/Board.nsf/Public'
    ],
    'Dorchester': [
        'https://www.dcpsmd.org/page/board-of-education',
        'https://www.dcpsmd.org/'
    ]
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    
    for county, urls in SEARCH_URLS.items():
        print(f"\n{'='*60}")
        print(f"{county} County - Searching for election dates")
        print('='*60)
        
        page = context.new_page()
        
        for url in urls:
            try:
                print(f"\n  URL: {url}")
                page.goto(url, wait_until='domcontentloaded', timeout=20000)
                page.wait_for_timeout(2000)
                
                content = page.locator('body').inner_text()
                
                # Search for board election mentions
                elections = re.findall(r'board.*?election.*?20[0-9]{2}', content, re.IGNORECASE)
                if elections:
                    print(f"  Found election mentions:")
                    for e in elections[:5]:
                        print(f"    - {e[:100]}")
                
                # Search for specific board member names with dates
                if county == 'Talbot':
                    names = ['Jackson', 'Dodson', 'Strawberry', "O'Connor", 'Wieland', 'Jurrius', 'Bridges']
                elif county == 'Kent':
                    names = ['McKenzie', 'Queen', 'Dorsey', 'Rhodes', 'McGee']
                else:  # Dorchester
                    names = ['board member', 'elected', 'appointed']
                
                for name in names:
                    pattern = rf'{name}.*?20[0-9]{{2}}'
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        print(f"  {name}: {matches[0][:80]}")
                
            except Exception as e:
                print(f"  Error: {str(e)[:60]}")
        
        page.close()
    
    browser.close()

print("\n" + "="*60)
print("✅ Search complete")
print("\nNote: Some counties may not publicly list specific election dates")
print("for individual board members. Contact county board offices directly")
print("for detailed election history.")
