"""Debug script to see how principals are displayed on school pages"""

from playwright.sync_api import sync_playwright
import json

# Load schools
with open('schools_list.json', 'r') as f:
    schools = json.load(f)

# Test with one school from each county
test_schools = [
    ('Chapel District Elementary (0401)', 'Talbot'),
    ('Galena Elementary School (0105)', 'Kent'),
    ('Choptank Elementary School (0716)', 'Dorchester'),
    ('Denton Elementary School (0301)', 'Caroline'),
    ('Bayside Elementary School (0403)', "Queen Anne's")
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for school_name, county in test_schools:
        school = next(s for s in schools if s['name'] == school_name)
        print(f"\n{'='*70}")
        print(f"{county}: {school['name']}")
        print(f"URL: {school['url']}")
        print('='*70)
        
        try:
            page.goto(school['url'], wait_until='domcontentloaded', timeout=15000)
            page.wait_for_timeout(2000)
            
            # Get the HTML
            html = page.content()
            
            # Look for sections with "principal" or "staff" or "contact"
            lines = html.split('\n')
            principal_section = []
            found_principal_keyword = False
            
            for i, line in enumerate(lines):
                if 'principal' in line.lower():
                    # Get surrounding lines
                    start = max(0, i-5)
                    end = min(len(lines), i+10)
                    principal_section = lines[start:end]
                    found_principal_keyword = True
                    break
            
            if found_principal_keyword:
                print("\nHTML around 'principal':")
                print('\n'.join(principal_section[:15]))
            else:
                print("\n❌ No 'principal' keyword found in HTML")
                
                # Try to find any staff/contact section
                for keyword in ['staff', 'contact', 'about', 'administration']:
                    for i, line in enumerate(lines):
                        if keyword in line.lower():
                            start = max(0, i-3)
                            end = min(len(lines), i+8)
                            print(f"\nHTML around '{keyword}':")
                            print('\n'.join(lines[start:end]))
                            break
                    else:
                        continue
                    break
                    
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    browser.close()
