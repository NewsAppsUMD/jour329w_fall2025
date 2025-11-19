"""Scrape Dorchester superintendent from chamber of commerce listing"""

from playwright.sync_api import sync_playwright
import re

url = "https://www.dorchesterchamber.org/list/member/dorchester-county-public-schools-101"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    
    print(f"Scraping Dorchester info from Chamber of Commerce...")
    print(f"URL: {url}")
    
    page.goto(url, wait_until='domcontentloaded', timeout=20000)
    page.wait_for_timeout(3000)
    
    content = page.locator('body').inner_text()
    
    # Save content
    with open('dorchester_chamber.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Save screenshot
    page.screenshot(path='dorchester_chamber.png', full_page=True)
    
    print(f"\n✓ Content saved ({len(content)} chars)")
    print(f"\nFull content:")
    print(content)
    
    # Search for superintendent
    super_patterns = [
        r'Superintendent[:\s]+(?:Dr\.\s+)?([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)',
        r'(?:Dr\.\s+)?([A-Z][a-z]+\s+[A-Z][a-z]+),?\s+Superintendent',
        r'Contact[:\s]+(?:Dr\.\s+)?([A-Z][a-z]+\s+[A-Z][a-z]+)'
    ]
    
    for pattern in super_patterns:
        matches = re.findall(pattern, content)
        if matches:
            print(f"\n\nPotential superintendent names:")
            for name in matches:
                print(f"  - {name}")
    
    browser.close()
