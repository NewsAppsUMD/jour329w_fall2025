#!/usr/bin/env python3
"""Test different URL patterns for MCAP data"""

from playwright.sync_api import sync_playwright
import time

def test_urls():
    base_url = "https://reportcard.msde.maryland.gov"
    district_code = "05"  # Caroline
    
    # Try different URL patterns
    url_patterns = [
        f"{base_url}/Graphs/#/Assessments/ElaPerformance/AllGrades/99/6/3/1/{district_code}/XXXX/2025",
        f"{base_url}/Graphs/#/Assessments/ElaPerformance/A/99/6/3/1/{district_code}/XXXX/2025",
        f"{base_url}/Graphs/#/Assessments/ElaPerformance/99/6/3/1/{district_code}/XXXX/2025",
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for i, url in enumerate(url_patterns, 1):
            print(f"\nTest {i}: {url}")
            try:
                page.goto(url, wait_until='networkidle', timeout=15000)
                time.sleep(3)
                
                # Get page content
                content = page.locator('body').inner_text()
                
                # Look for PL 3/4 data
                if "PL 3/4" in content:
                    print("  ✓ Found PL 3/4 data")
                    # Extract surrounding text
                    idx = content.find("PL 3/4")
                    print(f"  Context: {content[max(0, idx-50):idx+100]}")
                else:
                    print("  ✗ No PL 3/4 data found")
                    
                # Check if we see "2025"
                if "2025" in content:
                    print("  ✓ Found 2025 data")
                else:
                    print("  ✗ No 2025 data")
                    
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        browser.close()

if __name__ == "__main__":
    test_urls()
