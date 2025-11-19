"""Search for missing superintendent and board member info via alternative methods"""

from playwright.sync_api import sync_playwright
import json
import re

# Try alternative URLs and search methods
SEARCH_URLS = {
    'Kent': [
        'https://www.kent.k12.md.us/about/leadership',
        'https://www.kent.k12.md.us/about/board',
        'https://www.kent.k12.md.us/leadership',
        'https://www.kent.k12.md.us/staff',
        'https://www.kent.k12.md.us/'
    ],
    'Dorchester': [
        'https://www.dcpsmd.org/page/leadership',
        'https://www.dcpsmd.org/page/administration',
        'https://www.dcpsmd.org/page/staff-directory',
        'https://www.dcpsmd.org/'
    ],
    'Caroline': [
        'https://www.carolineschools.org/page/leadership',
        'https://www.carolineschools.org/page/administration',
        'https://www.carolineschools.org/about',
        'https://www.carolineschools.org/'
    ]
}

def search_for_officials(county, urls, page):
    """Search multiple URLs for superintendent and board info"""
    found_data = {
        'superintendent': None,
        'board_members': [],
        'working_url': None
    }
    
    for url in urls:
        try:
            print(f"  Trying: {url}")
            page.goto(url, wait_until='domcontentloaded', timeout=15000)
            page.wait_for_timeout(2000)
            
            content = page.locator('body').inner_text()
            
            # Search for superintendent
            super_patterns = [
                r'Superintendent[:\s]+(?:Dr\.\s+)?([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?)',
                r'(?:Dr\.\s+)?([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?)[,\s]+(?:Ed\.D\.|Ph\.D\.)?,?\s+Superintendent',
                r'([A-Z][a-z]+\s+[A-Z]\.\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?)\s+Superintendent'
            ]
            
            for pattern in super_patterns:
                match = re.search(pattern, content)
                if match:
                    name = match.group(1).strip()
                    if len(name.split()) >= 2 and name not in ['The Kent', 'Maryland Public']:
                        found_data['superintendent'] = name
                        found_data['working_url'] = url
                        print(f"    ✓ Found superintendent: {name}")
                        break
            
            # Search for board members
            if 'board' in url.lower() or 'board of education' in content.lower():
                # Look for names with titles
                board_patterns = [
                    r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*[-–]\s*(?:President|Vice President|Member|Chair)',
                    r'(?:President|Vice President|Member|Chair)[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
                    r'([A-Z][a-z]+\s+[A-Z][a-z]+),\s*(?:President|Vice President|Member)'
                ]
                
                for pattern in board_patterns:
                    matches = re.findall(pattern, content)
                    for name in matches:
                        if isinstance(name, tuple):
                            name = name[0]
                        name = name.strip()
                        if len(name.split()) >= 2 and name not in found_data['board_members']:
                            found_data['board_members'].append(name)
                
                if found_data['board_members']:
                    print(f"    ✓ Found {len(found_data['board_members'])} board members")
                    found_data['working_url'] = url
            
            # If we found superintendent, save screenshot
            if found_data['superintendent']:
                page.screenshot(path=f'{county.lower()}_leadership_found.png', full_page=True)
                
                # Save content for manual review
                with open(f'{county.lower()}_leadership_content.txt', 'w', encoding='utf-8') as f:
                    f.write(f"URL: {url}\n\n")
                    f.write(content)
                
                return found_data
                
        except Exception as e:
            print(f"    Error: {e}")
            continue
    
    return found_data

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    
    all_results = {}
    
    for county, urls in SEARCH_URLS.items():
        print(f"\n{'='*60}")
        print(f"Searching {county} County")
        print('='*60)
        
        results = search_for_officials(county, urls, page)
        all_results[county] = results
        
        print(f"\nResults for {county}:")
        print(f"  Superintendent: {results['superintendent']}")
        print(f"  Board Members: {len(results['board_members'])}")
        print(f"  Working URL: {results['working_url']}")
    
    browser.close()
    
    # Save results
    with open('missing_officials_search_results.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*60)
    print("✅ Search complete - saved to missing_officials_search_results.json")
    print("="*60)
    
    # Summary
    print("\nSUMMARY:")
    for county, data in all_results.items():
        print(f"\n{county}:")
        if data['superintendent']:
            print(f"  ✓ Superintendent: {data['superintendent']}")
        else:
            print(f"  ✗ Superintendent: NOT FOUND")
        
        if data['board_members']:
            print(f"  ✓ Board Members: {', '.join(data['board_members'][:3])}...")
        else:
            print(f"  ✗ Board Members: NOT FOUND")
