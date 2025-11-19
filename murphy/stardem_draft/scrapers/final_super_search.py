"""Final search for Dorchester and Caroline superintendents via recent news/meetings"""

from playwright.sync_api import sync_playwright
import re

TARGETS = {
    'Dorchester': [
        'https://www.dcpsmd.org/',
        'https://www.dcpsmd.org/news',  
    ],
    'Caroline': [
        'https://www.carolineschools.org/',
        'https://www.carolineschools.org/news',
    ]
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    
    for county, urls in TARGETS.items():
        print(f"\n{county} County - Searching homepage and news")
        print("="*60)
        
        for url in urls:
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=15000)
                page.wait_for_timeout(3000)
                
                html = page.content()
                text = page.locator('body').inner_text()
                
                # Look for superintendent mentions in different patterns
                patterns = [
                    r'Superintendent\s+(?:Dr\.\s+)?([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)',
                    r'(?:Dr\.\s+)?([A-Z][a-z]+\s+[A-Z]\.\s+[A-Z][a-z]+),?\s+(?:Ed\.D\.|Ph\.D\.)?,?\s+Superintendent',
                    r'(?:Dr\.\s+)?([A-Z][a-z]+\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?),?\s+Superintendent',
                    r'Superintendent\s+of\s+Schools[:\s]+(?:Dr\.\s+)?([A-Z][a-z]+\s+[A-Z][a-z]+)'
                ]
                
                found = []
                for pattern in patterns:
                    matches = re.findall(pattern, text)
                    found.extend(matches)
                
                if found:
                    print(f"  URL: {url}")
                    print(f"  Found potential names: {set(found)}")
                    
                    # Save for review
                    with open(f'{county.lower()}_final_search.txt', 'w', encoding='utf-8') as f:
                        f.write(f"URL: {url}\n\n")
                        f.write(text[:3000])
                    
            except Exception as e:
                print(f"  Error on {url}: {str(e)[:80]}")
    
    browser.close()

print("\n" + "="*60)
print("✅ Search complete")
