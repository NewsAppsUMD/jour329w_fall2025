"""
Manual scraper to extract district officials - saves full page content
for manual review and targeted extraction
"""

from playwright.sync_api import sync_playwright
import json

DISTRICTS = {
    'Talbot': 'https://www.tcps.k12.md.us/',
    'Kent': 'https://www.kent.k12.md.us/',
    'Dorchester': 'https://www.dcpsmd.org/',
    'Caroline': 'https://www.carolineschools.org/',
    "Queen Anne's": 'https://www.qacps.org/'
}

# Common pages to check
COMMON_PATHS = [
    '',  # Homepage
    'about',
    'about-us',
    'leadership',
    'administration',
    'board-of-education',
    'board',
    'contact',
    'staff',
    'directory'
]

def scrape_all_pages():
    """Save full content from all district pages"""
    
    print("Scraping District Websites - Saving Full Content")
    print("=" * 80)
    
    results = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)  # Ignore SSL errors
        
        for county, base_url in DISTRICTS.items():
            print(f"\n[{county} County]")
            print(f"  Base URL: {base_url}")
            
            county_data = {
                'base_url': base_url,
                'pages': {}
            }
            
            page = context.new_page()
            
            # Try homepage
            try:
                print(f"  Loading homepage...")
                page.goto(base_url, wait_until='domcontentloaded', timeout=15000)
                page.wait_for_timeout(3000)
                
                content = page.locator('body').inner_text()
                county_data['pages']['homepage'] = content
                
                # Save screenshot
                page.screenshot(path=f'district_{county.lower().replace(" ", "_")}_home.png', full_page=True)
                print(f"    ✓ Saved homepage ({len(content)} chars)")
                
                # Try to find and click leadership/board links
                keywords = ['board of education', 'leadership', 'administration', 'about us', 'superintendent']
                
                for keyword in keywords:
                    try:
                        link = page.locator(f'a:has-text("{keyword}")').first
                        if link.is_visible(timeout=2000):
                            href = link.get_attribute('href')
                            print(f"  Found link: {keyword} → {href}")
                            
                            # Visit the page
                            if href:
                                if not href.startswith('http'):
                                    href = base_url.rstrip('/') + '/' + href.lstrip('/')
                                
                                try:
                                    page.goto(href, wait_until='domcontentloaded', timeout=15000)
                                    page.wait_for_timeout(3000)
                                    content = page.locator('body').inner_text()
                                    county_data['pages'][keyword.replace(' ', '_')] = content
                                    page.screenshot(path=f'district_{county.lower().replace(" ", "_")}_{keyword.replace(" ", "_")}.png', full_page=True)
                                    print(f"    ✓ Saved {keyword} page ({len(content)} chars)")
                                    break  # Got one good page
                                except:
                                    pass
                    except:
                        continue
                
            except Exception as e:
                print(f"  ERROR: {e}")
                county_data['error'] = str(e)
            
            results[county] = county_data
            page.close()
        
        browser.close()
    
    # Save all content to JSON
    with open('district_pages_content.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("✅ CONTENT SAVED")
    print("=" * 80)
    print("\nSaved to: district_pages_content.json")
    print("\nNow extracting officials...")
    
    # Extract officials from saved content
    extract_officials(results)

def extract_officials(results):
    """Extract officials from page content"""
    import re
    
    officials = []
    
    for county, data in results.items():
        if 'error' in data:
            continue
        
        county_info = {
            'county': county,
            'superintendent': None,
            'board_members': [],
            'other_officials': []
        }
        
        # Combine all page content
        all_text = ' '.join(data['pages'].values())
        
        # Find superintendent
        super_patterns = [
            r'Superintendent[:\s]+(?:Dr\.\s+)?([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z]\.?\s*[A-Z][a-z]+)?)',
            r'(?:Dr\.\s+)?([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z]\.?\s*[A-Z][a-z]+)?)[,\s]+Superintendent',
        ]
        
        for pattern in super_patterns:
            match = re.search(pattern, all_text)
            if match:
                name = match.group(1).strip()
                if len(name.split()) >= 2:  # At least first and last name
                    county_info['superintendent'] = name
                    break
        
        # Find board members - look for patterns like "Name, President" or "Name - Member"
        board_patterns = [
            r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)[,\s]*[-–]\s*(?:President|Vice President|Member|Chair|Board Member)',
            r'(?:President|Vice President|Member|Chair)[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        ]
        
        for pattern in board_patterns:
            matches = re.findall(pattern, all_text)
            for match in matches:
                name = match.strip() if isinstance(match, str) else match[0].strip()
                if len(name.split()) >= 2 and name not in county_info['board_members']:
                    county_info['board_members'].append(name)
        
        officials.append(county_info)
        
        print(f"\n{county}:")
        print(f"  Superintendent: {county_info['superintendent']}")
        print(f"  Board Members: {county_info['board_members']}")
    
    # Save officials
    with open('district_officials.json', 'w', encoding='utf-8') as f:
        json.dump(officials, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("✅ Officials extracted and saved to: district_officials.json")

if __name__ == '__main__':
    scrape_all_pages()
