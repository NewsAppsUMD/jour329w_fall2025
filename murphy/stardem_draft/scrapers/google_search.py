"""Google-style search for Dorchester superintendent and board members"""

from playwright.sync_api import sync_playwright

query = "Dorchester County Public Schools Maryland superintendent 2025"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Search Google
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    page.goto(search_url, wait_until='domcontentloaded', timeout=15000)
    page.wait_for_timeout(3000)
    
    content = page.locator('body').inner_text()
    
    with open('dorchester_google_search.txt', 'w', encoding='utf-8') as f:
        f.write(content[:5000])
    
    print("Dorchester Google search results:")
    print(content[:1500])
    
    # Try Caroline board members too
    query2 = "Caroline County Public Schools Maryland board of education members 2025"
    search_url2 = f"https://www.google.com/search?q={query2.replace(' ', '+')}"
    page.goto(search_url2, wait_until='domcontentloaded', timeout=15000)
    page.wait_for_timeout(3000)
    
    content2 = page.locator('body').inner_text()
    
    with open('caroline_board_google_search.txt', 'w', encoding='utf-8') as f:
        f.write(content2[:5000])
    
    print("\n" + "="*60)
    print("Caroline Board Google search results:")
    print(content2[:1500])
    
    browser.close()
