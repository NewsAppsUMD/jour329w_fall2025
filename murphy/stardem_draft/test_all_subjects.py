"""Test all three subjects for Federalsburg Elementary Grade 5"""

from playwright.sync_api import sync_playwright
import json
import re

school_url = "https://reportcard.msde.maryland.gov/Graphs/#/ReportCards/ReportCardSchool/1/E/1/05/0501/0"
county_code = "05"
school_code = "0501"
grade = 5

base_url = "https://reportcard.msde.maryland.gov"

print("Testing Federalsburg Elementary Grade 5 - All Subjects")
print("="*70)

def extract_proficiency(page):
    """Extract PL 3/4 proficiency from page"""
    try:
        # Click Show Table
        show_table = page.locator('text=/Show Table/i')
        show_table.click(timeout=5000)
        page.wait_for_timeout(2000)
    except:
        pass
    
    content = page.locator('body').inner_text()
    pl34_matches = re.findall(r'PL\s*3/4[^\d]*(\d+\.?\d*)', content)
    return float(pl34_matches[-1]) if pl34_matches else None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    subjects = {
        'ELA': f"{base_url}/Graphs/#/Assessments/ElaPerformance/{grade}ELA/{grade}/6/3/1/{county_code}/{school_code}/2025",
        'Math': f"{base_url}/Graphs/#/Assessments/MathPerformance/{grade}MAT/{grade}/6/3/1/{county_code}/{school_code}/2025",
        'Science': f"{base_url}/Graphs/#/Assessments/SciencePerformance/{grade}/6/3/1/{county_code}/{school_code}/2025"
    }
    
    results = {}
    
    for subject, url in subjects.items():
        print(f"\n{subject}:")
        print(f"  URL: {url}")
        page.goto(url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(3000)
        
        proficiency = extract_proficiency(page)
        results[subject] = proficiency
        print(f"  Proficiency: {proficiency}%")
    
    browser.close()
    
    print("\n" + "="*70)
    print("SUMMARY:")
    for subject, prof in results.items():
        print(f"  {subject}: {prof}%")
    
    print("\n✓ Test complete")
