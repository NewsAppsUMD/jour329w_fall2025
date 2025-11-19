"""Try BoardDocs and other document sources for official names"""

from playwright.sync_api import sync_playwright
import json
import re

# Try BoardDocs and direct document links
DOCUMENT_URLS = {
    'Kent': [
        'https://www.kent.k12.md.us/departments',
        'https://go.boarddocs.com/mabe/kcps/Board.nsf/Public',
    ],
    'Dorchester': [
        'https://www.dcpsmd.org/page/leadership',
        'https://go.boarddocs.com/mabe/dcps/Board.nsf/Public',
    ],
    'Caroline': [
        'https://www.carolineschools.org/leadership',
        'https://go.boarddocs.com/mabe/ccps/Board.nsf/Public',
    ]
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    
    for county, urls in DOCUMENT_URLS.items():
        print(f"\n{county} County:")
        
        for url in urls:
            try:
                print(f"  Trying: {url}")
                page.goto(url, wait_until='domcontentloaded', timeout=20000)
                page.wait_for_timeout(3000)
                
                content = page.locator('body').inner_text()
                
                # Save what we find
                filename = f"{county.lower()}_{url.split('/')[-2]}_content.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"URL: {url}\n\n")
                    f.write(content[:5000])  # First 5000 chars
                
                print(f"    Saved to {filename}")
                print(f"    Preview: {content[:200]}")
                
            except Exception as e:
                print(f"    Error: {str(e)[:100]}")
    
    browser.close()

print("\n✅ Check the saved files for superintendent names")
