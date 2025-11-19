"""Search Maryland State Board of Elections for board member election info"""

from playwright.sync_api import sync_playwright
import re

# Counties to search
COUNTIES = ['Talbot', 'Kent', 'Dorchester', 'Caroline', 'Queen Anne\'s']

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    print("Searching Maryland State Board of Elections")
    print("="*60)
    
    # Start at main page
    page.goto('https://elections.maryland.gov/index.html', wait_until='domcontentloaded', timeout=20000)
    page.wait_for_timeout(3000)
    
    # Save homepage
    content = page.locator('body').inner_text()
    print(f"\nHomepage loaded ({len(content)} chars)")
    
    # Look for links to election results or local boards
    try:
        # Try to find election results or local boards link
        links = page.locator('a').all()
        relevant_links = []
        
        for link in links[:100]:
            text = link.inner_text().lower()
            if any(word in text for word in ['board', 'local', 'county', 'results', 'election', 'school']):
                href = link.get_attribute('href')
                if href:
                    relevant_links.append((text.strip()[:50], href))
        
        print(f"\nFound {len(relevant_links)} relevant links:")
        for text, href in relevant_links[:15]:
            print(f"  - {text}: {href[:80]}")
        
        # Try to navigate to election results
        if 'election-results' in content.lower() or 'results' in content.lower():
            # Look for 2024 or 2022 general election results
            for year in ['2024', '2022', '2020']:
                try:
                    year_link = page.locator(f'a:has-text("{year}")').first
                    if year_link.is_visible(timeout=2000):
                        print(f"\nFound {year} results link")
                        year_link.click(timeout=5000)
                        page.wait_for_timeout(3000)
                        
                        new_content = page.locator('body').inner_text()
                        
                        # Look for "Board of Education" results
                        if 'board of education' in new_content.lower():
                            print(f"\n{year} contains Board of Education results")
                            
                            # Save content
                            with open(f'md_elections_{year}.txt', 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            
                            # Look for our counties
                            for county in COUNTIES:
                                if county.lower() in new_content.lower():
                                    print(f"  ✓ Found {county} County")
                        
                        page.go_back(timeout=5000)
                        page.wait_for_timeout(2000)
                        break
                except:
                    continue
        
    except Exception as e:
        print(f"\nError navigating: {e}")
    
    # Take screenshot
    page.screenshot(path='md_elections_homepage.png', full_page=True)
    
    browser.close()

print("\n" + "="*60)
print("✅ Search complete")
print("\nNote: Detailed election results by candidate may require")
print("navigating to specific election year results pages.")
