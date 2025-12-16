#!/usr/bin/env python3
"""Test graduation rate scraping"""

from playwright.sync_api import sync_playwright
import time

def test_grad_rate():
    url = "https://reportcard.msde.maryland.gov/Graphs/#/GraduationRates/GraduationRate/6/3/1/05/XXXX/2024"
    
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
                print("Found 'Show Table' button, clicking...")
                show_table.click(timeout=5000)
                time.sleep(2)
        except Exception as e:
            print(f"Could not click Show Table: {e}")
        
        # Get content
        content = page.locator('body').inner_text()
        
        # Print relevant section
        print("\nPage content (first 2000 chars):")
        print(content[:2000])
        
        # Look for graduation rate patterns
        if "2024" in content:
            idx = content.find("2024")
            print(f"\nContent around '2024':")
            print(content[max(0, idx-100):idx+200])
        
        browser.close()

if __name__ == "__main__":
    test_grad_rate()
