from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    url = 'https://reportcard.msde.maryland.gov/Graphs/#/Assessments/ElaPerformance/AELAA/A/12/3/1/05/XXXX/2025'
    page.goto(url, wait_until='networkidle', timeout=20000)
    time.sleep(5)
    
    # Try clicking "Show Table" button
    try:
        page.click('button:has-text("Show Table")', timeout=5000)
        print("Clicked Show Table button")
        time.sleep(3)
        
        # Now get the text again
        content = page.locator('body').inner_text()
        
        # Look for table data
        if '2025' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if '2025' in line or 'PL 3/4' in line or 'White' in line:
                    print(f"{i}: {line}")
                    
    except Exception as e:
        print(f"Error clicking Show Table: {e}")
    
    browser.close()
