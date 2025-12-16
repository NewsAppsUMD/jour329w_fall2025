from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    url = 'https://reportcard.msde.maryland.gov/Graphs/#/Assessments/ElaPerformance/AELAA/A/12/3/1/05/XXXX/2025'
    page.goto(url, wait_until='networkidle', timeout=20000)
    time.sleep(6)  
    
    # Try to get all text including from specific elements
    all_text = page.locator('body').all_inner_texts()
    full_content = '\n'.join(all_text)
    
    # Look for proficient
    if 'PROFICIENT' in full_content.upper():
        print("Found PROFICIENT!")
        idx = full_content.upper().find('PROFICIENT')
        print(full_content[idx-50:idx+200])
    else:
        print("PROFICIENT not found")
        
    # Try to find any div or span that might contain percentage data
    # Look for elements with specific text patterns
    elements_with_percent = page.locator('text=/\\d+\\.\\d+%/').all()
    print(f"\nFound {len(elements_with_percent)} elements with percentage pattern")
    for i, elem in enumerate(elements_with_percent[:10]):
        try:
            text = elem.inner_text()
            print(f"{i}: {text}")
        except:
            pass
    
    browser.close()
