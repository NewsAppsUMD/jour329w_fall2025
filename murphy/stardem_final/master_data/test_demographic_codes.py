from playwright.sync_api import sync_playwright
import time
import re

def extract_proficiency_rate(page_content):
    """Extract the 2025 PL 3/4 proficiency percentage from page content"""
    pattern = r'2025.*?PL\s*3/4[^\d]*(\d+\.?\d*)'
    match = re.search(pattern, page_content, re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None

# Test different demographic code patterns
test_patterns = {
    'All Students': 'A',
    'White (code 1)': '1',
    'White (code 2)': '2', 
    'White (code 3)': '3',
    'White (code 4)': '4',
    'White (code 5)': '5',
    'White (code 6)': '6',
    'White (code 7)': '7',
    'Black (code 1)': '1',
    'Hispanic (code 2)': '2',
    'Econ Disadv (ED)': 'ED',
    'Econ Disadv (E)': 'E',
    'Econ Disadv (D)': 'D',
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Test with Caroline County ELA
    print("Testing different demographic codes in URL pattern...")
    print("=" * 70)
    
    # First, get the "All Students" baseline
    base_url = 'https://reportcard.msde.maryland.gov/Graphs/#/Assessments/ElaPerformance/AELAA/A/6/3/1/05/XXXX/2025'
    print(f"\nBaseline (All Students):")
    print(f"URL: {base_url}")
    page.goto(base_url, wait_until='networkidle', timeout=20000)
    time.sleep(3)
    content = page.locator('body').inner_text()
    rate = extract_proficiency_rate(content)
    print(f"Rate found: {rate}%")
    
    # Now test replacing the demographic parameter (4th position after AELAA)
    # Try different positions in the URL path
    
    # Pattern 1: Replace the "A" with demographic code
    print("\n\nTesting Pattern 1: Replacing 'A' position")
    print("-" * 70)
    for demo_name in ['1', '2', '3', '4', '5', '6', '7']:
        url = f'https://reportcard.msde.maryland.gov/Graphs/#/Assessments/ElaPerformance/AELAA/{demo_name}/6/3/1/05/XXXX/2025'
        print(f"\nTrying code '{demo_name}': {url}")
        try:
            page.goto(url, wait_until='networkidle', timeout=15000)
            time.sleep(2)
            content = page.locator('body').inner_text()
            rate = extract_proficiency_rate(content)
            
            # Look for demographic identifier in page
            if 'White' in content[:1000]:
                print(f"  -> Found 'White' in content, Rate: {rate}%")
            elif 'Black' in content[:1000] or 'African' in content[:1000]:
                print(f"  -> Found 'Black/African' in content, Rate: {rate}%")
            elif 'Hispanic' in content[:1000] or 'Latino' in content[:1000]:
                print(f"  -> Found 'Hispanic/Latino' in content, Rate: {rate}%")
            elif 'Economically' in content[:1000] or 'Disadvantaged' in content[:1000]:
                print(f"  -> Found 'Economically Disadvantaged' in content, Rate: {rate}%")
            elif rate:
                print(f"  -> Rate found: {rate}% (demographic unclear)")
            else:
                print(f"  -> No rate found")
                
        except Exception as e:
            print(f"  -> Error: {str(e)[:50]}")
        
        time.sleep(1)
    
    browser.close()

print("\n" + "=" * 70)
print("Test complete. Check output above for working patterns.")
