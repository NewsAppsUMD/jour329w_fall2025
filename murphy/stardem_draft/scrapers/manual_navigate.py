"""Manual navigation through site menus to find officials"""

from playwright.sync_api import sync_playwright
import json

DISTRICTS = {
    'Kent': 'https://www.kent.k12.md.us/',
    'Dorchester': 'https://www.dcpsmd.org/',
    'Caroline': 'https://www.carolineschools.org/'
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    
    results = {}
    
    for county, url in DISTRICTS.items():
        print(f"\n{'='*60}")
        print(f"{county} County - Manual Navigation")
        print('='*60)
        
        page = context.new_page()
        page.goto(url, wait_until='domcontentloaded', timeout=15000)
        page.wait_for_timeout(3000)
        
        # Try clicking "About" menu
        try:
            about_link = page.locator('a:has-text("About"), a:has-text("Leadership"), a:has-text("Administration")').first
            if about_link.is_visible(timeout=2000):
                href = about_link.get_attribute('href')
                print(f"  Found 'About' link: {href}")
                
                if href:
                    if not href.startswith('http'):
                        href = url.rstrip('/') + '/' + href.lstrip('/')
                    
                    page.goto(href, wait_until='domcontentloaded', timeout=15000)
                    page.wait_for_timeout(3000)
                    
                    content = page.locator('body').inner_text()
                    
                    # Save screenshot
                    page.screenshot(path=f'{county.lower()}_about_page.png', full_page=True)
                    
                    # Save content
                    with open(f'{county.lower()}_about_content.txt', 'w', encoding='utf-8') as f:
                        f.write(f"URL: {href}\n\n")
                        f.write(content)
                    
                    print(f"  ✓ Saved content ({len(content)} chars)")
                    print(f"\n  First 800 chars:")
                    print(f"  {content[:800]}")
                    
        except Exception as e:
            print(f"  Error navigating: {e}")
        
        page.close()
    
    browser.close()
    
    print("\n" + "="*60)
    print("✅ Manual navigation complete")
    print("="*60)
    print("\nCheck the saved *_about_content.txt files for superintendent names")
