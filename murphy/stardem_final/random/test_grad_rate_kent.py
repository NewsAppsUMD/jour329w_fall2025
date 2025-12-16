#!/usr/bin/env python3
"""Test graduation rate URL and extraction"""

from playwright.sync_api import sync_playwright
import time
import re

def test_grad_rate():
    # Test with Kent County (code 14)
    url = "https://reportcard.msde.maryland.gov/Graphs/#/GraduationRates/GraduationRate/6/3/1/14/XXXX/2024"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"Navigating to: {url}")
        page.goto(url, wait_until='networkidle', timeout=15000)
        time.sleep(3)
        
        # Try to click Show Table
        try:
            show_table = page.locator('text=/Show Table/i')
            if show_table.count() > 0:
                print("Clicking Show Table...")
                show_table.click(timeout=5000)
                time.sleep(2)
        except Exception as e:
            print(f"Show Table issue: {e}")
        
        # Get content
        content = page.locator('body').inner_text()
        
        # Look for graduation rate patterns
        print("\n=== Searching for graduation rate data ===")
        
        # Try different patterns
        patterns = [
            r'2024.*?(\d+\.?\d*)\s*%',
            r'All Students.*?(\d+\.?\d*)\s*%',
            r'Four[- ]Year.*?(\d+\.?\d*)',
            r'Graduation Rate.*?(\d+\.?\d*)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                print(f"Pattern '{pattern}' found: {matches[:5]}")
        
        # Print section around "2024"
        if "2024" in content:
            idx = content.find("2024")
            print(f"\n=== Content around '2024' ===")
            print(content[max(0, idx-200):idx+300])
        
        browser.close()

if __name__ == "__main__":
    test_grad_rate()
