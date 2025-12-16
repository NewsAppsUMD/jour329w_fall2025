from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    url = 'https://reportcard.msde.maryland.gov/Graphs/#/Assessments/ElaPerformance/AELAA/A/12/3/1/05/XXXX/2025'
    page.goto(url, wait_until='networkidle', timeout=20000)
    time.sleep(4)
    
    # Click Show Table button
    try:
        page.click('text=Show Table')
        time.sleep(2)
        print("Clicked Show Table")
    except:
        print("Could not click Show Table")
    
    content = page.locator('body').inner_text()
    
    # Look for 2025 in the content
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '2025' in line:
            # Print this line and next 10 lines
            print(f"\nFound 2025 at line {i}:")
            for j in range(i, min(i+15, len(lines))):
                print(f"{j}: {lines[j]}")
            break
    
    browser.close()
