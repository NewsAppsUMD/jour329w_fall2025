"""Scrape Caroline board members from the correct URL"""

from playwright.sync_api import sync_playwright
import json
import re

url = "https://www.carolineschools.org/o/ccps/page/board#members"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    
    print(f"Scraping Caroline Board Members...")
    print(f"URL: {url}")
    
    page.goto(url, wait_until='domcontentloaded', timeout=20000)
    page.wait_for_timeout(3000)
    
    content = page.locator('body').inner_text()
    
    # Save content
    with open('caroline_board_members.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Save screenshot
    page.screenshot(path='caroline_board_members.png', full_page=True)
    
    print(f"\n✓ Content saved ({len(content)} chars)")
    print(f"\nFirst 2000 characters:")
    print(content[:2000])
    
    # Try to extract board member names
    # Look for patterns like "Name - Position" or "Name, Position"
    board_patterns = [
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*[-–]\s*(?:President|Vice President|Member)',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),?\s+(?:President|Vice President|Member)',
    ]
    
    members = []
    for pattern in board_patterns:
        matches = re.findall(pattern, content)
        for name in matches:
            if isinstance(name, tuple):
                name = name[0]
            name = name.strip()
            if len(name.split()) >= 2 and name not in members:
                members.append(name)
    
    print(f"\n\nExtracted {len(members)} board members:")
    for member in members:
        print(f"  - {member}")
    
    browser.close()
