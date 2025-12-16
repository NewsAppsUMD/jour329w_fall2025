#!/usr/bin/env python3
"""Test extracting the actual PL 3/4 percentage value"""

from playwright.sync_api import sync_playwright
import time
import re

def test_extraction():
    url = "https://reportcard.msde.maryland.gov/Graphs/#/Assessments/ElaPerformance/AllGrades/99/6/3/1/05/XXXX/2025"
    
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
            else:
                print("No 'Show Table' button found")
        except Exception as e:
            print(f"Could not click Show Table: {e}")
        
        # Get the page content
        content = page.locator('body').inner_text()
        
        # Print relevant section around PL 3/4
        if "PL 3/4" in content:
            idx = content.find("PL 3/4")
            print(f"\nContent around 'PL 3/4':")
            print(content[max(0, idx-200):idx+300])
            print("\n" + "="*80)
        
        # Try different regex patterns
        print("\nTrying regex patterns:")
        
        patterns = [
            r'2025.*?PL\s*3/4[^\d]*(\d+\.?\d*)',
            r'PL\s*3/4[^\d]*(\d+\.?\d*)',
            r'(?:^|\n)2025\s+(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)\s+(\d+\.?\d*)',
        ]
        
        for i, pattern in enumerate(patterns, 1):
            matches = re.findall(pattern, content, re.MULTILINE)
            print(f"{i}. Pattern: {pattern}")
            print(f"   Matches: {matches[:5] if matches else 'None'}")
        
        browser.close()

if __name__ == "__main__":
    test_extraction()
