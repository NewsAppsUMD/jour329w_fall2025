"""Get 2024 and 2022 election results for Board of Education races"""

from playwright.sync_api import sync_playwright

# Try direct URLs to recent election results
RESULT_URLS = [
    'https://elections.maryland.gov/elections/2024/index.html',
    'https://elections.maryland.gov/elections/2022/index.html',
    'https://elections.maryland.gov/voting/municipal_results.html',
    'https://elections.maryland.gov/about/county_boards.html'
]

COUNTIES = ['Talbot', 'Kent', 'Dorchester', 'Caroline', 'Queen Anne']

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for url in RESULT_URLS:
        print(f"\n{'='*60}")
        print(f"Checking: {url}")
        print('='*60)
        
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=20000)
            page.wait_for_timeout(3000)
            
            content = page.locator('body').inner_text()
            
            # Save content
            filename = url.split('/')[-2] + '_' + url.split('/')[-1].replace('.html', '.txt')
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ Saved to {filename}")
            
            # Look for Board of Education
            if 'board of education' in content.lower() or 'school board' in content.lower():
                print("✓ Contains Board of Education/School Board references")
                
                for county in COUNTIES:
                    if county.lower() in content.lower():
                        print(f"  • Found {county} County")
            
            # Look for any of our counties
            found_counties = [c for c in COUNTIES if c.lower() in content.lower()]
            if found_counties:
                print(f"\nCounties mentioned: {', '.join(found_counties)}")
            
            # Print first 1000 chars
            print(f"\nPreview:")
            print(content[:1000])
            
        except Exception as e:
            print(f"Error: {str(e)[:100]}")
    
    browser.close()

print("\n" + "="*60)
print("✅ Complete")
