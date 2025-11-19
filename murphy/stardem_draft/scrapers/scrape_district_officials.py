"""
Scrape district websites to find top officials and board of education members
for the 5 counties: Talbot, Kent, Dorchester, Caroline, Queen Anne's
"""

from playwright.sync_api import sync_playwright
import json
import re
from bs4 import BeautifulSoup

# District websites for the 5 counties
DISTRICTS = {
    'Talbot': 'https://www.tcps.k12.md.us/',
    'Kent': 'https://www.kent.k12.md.us/',
    'Dorchester': 'https://www.dcpsmd.org/',
    'Caroline': 'https://www.carolineschools.org/',
    "Queen Anne's": 'https://www.qacps.org/'
}

def extract_officials_from_page(html_content, county_name):
    """Extract names of officials from HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    results = {
        'county': county_name,
        'superintendent': None,
        'board_members': [],
        'other_officials': []
    }
    
    # Look for superintendent
    superintendent_patterns = [
        r'Superintendent[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'Dr\.\s+([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),?\s+Superintendent',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)[,\s]+Superintendent'
    ]
    
    text = soup.get_text()
    for pattern in superintendent_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            results['superintendent'] = match.group(1)
            break
    
    # Look for board of education members
    board_keywords = ['board of education', 'board members', 'school board']
    for keyword in board_keywords:
        if keyword.lower() in text.lower():
            # Find section with board members
            # This is a simplified approach - may need adjustment per site
            board_section = re.search(
                rf'{keyword}.*?(?=Contact|Footer|©|\Z)',
                text,
                re.IGNORECASE | re.DOTALL
            )
            if board_section:
                # Extract names (capitalized words that look like names)
                names = re.findall(
                    r'\b([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b',
                    board_section.group(0)
                )
                results['board_members'] = list(set(names))[:10]  # Limit to 10
                break
    
    return results

def scrape_district_officials():
    """Main scraper function"""
    print("Scraping District Officials for 5 Counties")
    print("=" * 80)
    
    all_results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for county, url in DISTRICTS.items():
            print(f"\n[{county} County]")
            print(f"  URL: {url}")
            
            try:
                page = browser.new_page()
                page.goto(url, wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(3000)
                
                # Get HTML content
                html = page.content()
                
                # Extract officials
                results = extract_officials_from_page(html, county)
                
                # Also try to find leadership/administration page
                try:
                    # Look for links to leadership pages
                    leadership_links = page.locator('a:has-text("Leadership"), a:has-text("Administration"), a:has-text("Board"), a:has-text("About Us")').all()
                    
                    if leadership_links:
                        print(f"  Found {len(leadership_links)} potential leadership links")
                        # Try first link
                        first_link = leadership_links[0]
                        href = first_link.get_attribute('href')
                        if href:
                            print(f"  Checking: {href}")
                            if not href.startswith('http'):
                                href = url.rstrip('/') + '/' + href.lstrip('/')
                            page.goto(href, wait_until='networkidle', timeout=30000)
                            page.wait_for_timeout(3000)
                            html = page.content()
                            results = extract_officials_from_page(html, county)
                except Exception as e:
                    print(f"  Could not check leadership page: {e}")
                
                print(f"  Superintendent: {results['superintendent']}")
                print(f"  Board Members: {len(results['board_members'])} found")
                
                # Save screenshot
                page.screenshot(path=f'district_{county.lower().replace(" ", "_")}_screenshot.png', full_page=True)
                
                all_results.append(results)
                page.close()
                
            except Exception as e:
                print(f"  ERROR: {e}")
                all_results.append({
                    'county': county,
                    'error': str(e)
                })
        
        browser.close()
    
    # Save results
    with open('district_officials.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("✅ SCRAPING COMPLETE")
    print("=" * 80)
    print(f"\nResults saved to: district_officials.json")
    
    # Print summary
    print("\nSUMMARY:")
    for result in all_results:
        if 'error' not in result:
            print(f"\n{result['county']} County:")
            print(f"  Superintendent: {result['superintendent']}")
            print(f"  Board Members ({len(result['board_members'])}): {', '.join(result['board_members'][:3])}...")

if __name__ == '__main__':
    scrape_district_officials()
