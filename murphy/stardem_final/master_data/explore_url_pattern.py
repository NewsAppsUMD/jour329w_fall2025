from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Start with the basic district page for Caroline
    base_url = 'https://reportcard.msde.maryland.gov/Graphs/#/Assessments/ElaPerformance/AELAA/A/6/3/1/05/XXXX/2025'
    
    print("Opening base URL...")
    page.goto(base_url, wait_until='networkidle')
    time.sleep(5)
    
    print("\nCurrent URL after load:", page.url)
    
    # Try to find race/demographic filter elements
    print("\nLooking for filter elements...")
    
    # Check for dropdown or filter buttons
    content = page.content()
    
    # Save the page for inspection
    with open('/workspaces/jour329w_fall2025/murphy/stardem_final/master_data/test_page.html', 'w') as f:
        f.write(content)
    
    print("Page content saved to test_page.html")
    
    # Keep browser open for manual inspection
    print("\nBrowser will stay open for 60 seconds for manual inspection...")
    time.sleep(60)
    
    browser.close()
