"""Test scraper with one school (Federalsburg Elementary)"""

from playwright.sync_api import sync_playwright
import json
import re

school_url = "https://reportcard.msde.maryland.gov/Graphs/#/ReportCards/ReportCardSchool/1/E/1/05/0501/0"
county_code = "05"
school_code = "0501"
grade = 5

base_url = "https://reportcard.msde.maryland.gov"

print("Testing Federalsburg Elementary Grade 5 MCAP Scores")
print("="*70)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Test ELA
    print("\nTesting ELA Grade 5...")
    ela_url = f"{base_url}/Graphs/#/Assessments/ElaPerformance/5ELA/5/6/3/1/{county_code}/{school_code}/2025"
    print(f"URL: {ela_url}")
    page.goto(ela_url, wait_until='networkidle', timeout=30000)
    page.wait_for_timeout(5000)
    
    # Try to click "Show Table" button to get actual data
    try:
        show_table = page.locator('text=/Show Table/i')
        if show_table.is_visible():
            print("Clicking 'Show Table' button...")
            show_table.click()
            page.wait_for_timeout(2000)
    except:
        print("'Show Table' button not found or not clickable")
    
    content = page.locator('body').inner_text()
    print(f"\nPage content length: {len(content)}")
    
    # Save full content
    with open('test_ela_content.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Full content saved to test_ela_content.txt")
    
    # Look for PL 3/4 (proficiency = Performance Levels 3 and 4)
    pl34_matches = re.findall(r'PL\s*3/4[^\d]*(\d+\.?\d*)', content)
    print(f"\nPL 3/4 matches: {pl34_matches}")
    
    # Look for table data
    if 'PL 1' in content and 'PL 2' in content:
        print("\nLooking for table structure...")
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'PL 3/4' in line or 'PL 1' in line:
                print(f"Line {i}: {line}")
    
    # Take screenshot
    page.screenshot(path='/workspaces/jour329w_fall2025/murphy/stardem_draft/test_ela_screenshot.png', full_page=True)
    print("\nScreenshot saved to test_ela_screenshot.png")
    
    browser.close()

print("\n✓ Test complete")
