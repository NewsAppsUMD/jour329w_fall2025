from playwright.sync_api import sync_playwright
import time
import re

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    url = 'https://reportcard.msde.maryland.gov/Graphs/#/Assessments/ElaPerformance/AELAA/A/12/3/1/05/XXXX/2025'
    page.goto(url, wait_until='networkidle', timeout=20000)
    time.sleep(3)
    
    content = page.locator('body').inner_text()
    
    # Look for any proficient-related text
    if 'PROFICIENT' in content.upper():
        print('Found PROFICIENT in content')
        idx = content.upper().find('PROFICIENT')
        print('Context:')
        print(content[max(0,idx-50):idx+250])
    
    if 'DISTRICT' in content.upper():
        print('\nFound DISTRICT in content')
        idx = content.upper().find('DISTRICT')
        print('Context:')
        print(content[max(0,idx-50):idx+150])
    
    # Save full content for inspection
    with open('/workspaces/jour329w_fall2025/murphy/stardem_final/master_data/page_content.txt', 'w') as f:
        f.write(content)
    print('\nFull content saved to page_content.txt')
    
    browser.close()
