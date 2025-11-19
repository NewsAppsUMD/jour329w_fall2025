"""Search Dorchester site more thoroughly for superintendent"""

from playwright.sync_api import sync_playwright
import re

urls_to_try = [
    "https://www.dcpsmd.org/page/leadership",
    "https://www.dcpsmd.org/staff",
    "https://www.dcpsmd.org/about",
    "https://go.boarddocs.com/mabe/dcps/Board.nsf/Public",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    
    for url in urls_to_try:
        print(f"\n{'='*60}")
        print(f"Trying: {url}")
        
        page = context.new_page()
        
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=20000)
            page.wait_for_timeout(3000)
            
            # Try clicking any links that might lead to leadership
            try:
                links = page.locator('a').all()
                for link in links[:50]:  # Check first 50 links
                    text = link.inner_text().lower()
                    if any(word in text for word in ['superintendent', 'leadership', 'staff', 'administration', 'about']):
                        href = link.get_attribute('href')
                        if href:
                            print(f"  Found relevant link: {text[:50]} -> {href}")
            except:
                pass
            
            content = page.locator('body').inner_text()
            
            # Search for superintendent
            if 'superintendent' in content.lower():
                # Extract context around superintendent mentions
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'superintendent' in line.lower():
                        context = '\n'.join(lines[max(0, i-2):min(len(lines), i+3)])
                        print(f"\n  Context around 'superintendent':")
                        print(f"  {context}\n")
            
            # Save if this is leadership page
            if 'leadership' in url or 'staff' in url:
                with open(f'dorchester_{url.split("/")[-1]}_content.txt', 'w', encoding='utf-8') as f:
                    f.write(f"URL: {url}\n\n")
                    f.write(content)
                print(f"  ✓ Saved content")
            
        except Exception as e:
            print(f"  Error: {str(e)[:100]}")
        
        page.close()
    
    browser.close()

print("\n" + "="*60)
print("✅ Search complete")
