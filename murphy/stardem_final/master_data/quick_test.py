from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    url = 'https://reportcard.msde.maryland.gov/Graphs/#/Assessments/ElaPerformance/AELAA/A/12/3/1/05/XXXX/2025'
    page.goto(url, wait_until='networkidle', timeout=20000)
    time.sleep(5)  # Wait longer
    
    content = page.locator('body').inner_text()
    
    # Search for various keywords
    keywords = ['PERCENT', 'PROFICIENT', 'DISTRICT', '58', '%']
    
    for keyword in keywords:
        if keyword in content:
            idx = content.find(keyword)
            print(f"\nFound '{keyword}' at position {idx}")
            print(f"Context: {content[max(0, idx-50):idx+100]}")
    
    # Save first 2000 characters
    print("\n\nFirst 2000 characters of page:")
    print(content[:2000])
    
    browser.close()
