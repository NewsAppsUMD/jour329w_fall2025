from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Not headless so we can see
    page = browser.new_page()
    
    url = 'https://reportcard.msde.maryland.gov/Graphs/#/Assessments/ElaPerformance/AELAA/A/12/3/1/05/XXXX/2025'
    page.goto(url, wait_until='networkidle', timeout=20000)
    
    print("Waiting 10 seconds for page to fully load...")
    time.sleep(10)
    
    # Save the full HTML
    html = page.content()
    with open('/workspaces/jour329w_fall2025/murphy/stardem_final/master_data/page_source.html', 'w') as f:
        f.write(html)
    print("HTML saved to page_source.html")
    
    # Get all text
    text = page.locator('body').inner_text()
    with open('/workspaces/jour329w_fall2025/murphy/stardem_final/master_data/page_text.txt', 'w') as f:
        f.write(text)
    print("Text saved to page_text.txt")
    
    # Keep browser open for manual inspection
    print("\nBrowser staying open for 30 seconds...")
    print("Please check if you can see 'PERCENT PROFICIENT' and '58.3%' on the page")
    time.sleep(30)
    
    browser.close()
