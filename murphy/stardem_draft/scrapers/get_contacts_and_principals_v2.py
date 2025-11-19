"""Get superintendent contact info and principals from district websites"""

from playwright.sync_api import sync_playwright
import json
import re

# Load schools list
with open('schools_list.json', 'r') as f:
    schools = json.load(f)

# District info
DISTRICTS = {
    'Talbot': {
        'base_url': 'https://www.tcps.k12.md.us/',
        'schools_page': 'https://www.tcps.k12.md.us/our-schools',
        'leadership_page': 'https://www.tcps.k12.md.us/page/leadership'
    },
    'Kent': {
        'base_url': 'https://www.kent.k12.md.us/',
        'schools_page': 'https://www.kent.k12.md.us/schools',
        'leadership_page': 'https://www.kent.k12.md.us/leadership'
    },
    'Dorchester': {
        'base_url': 'https://www.dcpsmd.org/',
        'schools_page': 'https://www.dcpsmd.org/schools',
        'leadership_page': 'https://www.dcpsmd.org/o/dcps/page/district-leadership'
    },
    'Caroline': {
        'base_url': 'https://www.carolineschools.org/',
        'schools_page': 'https://www.carolineschools.org/schools',
        'leadership_page': 'https://www.carolineschools.org/o/ccps/page/leadership'
    },
    "Queen Anne's": {
        'base_url': 'https://www.qacps.org/',
        'schools_page': 'https://www.qacps.org/schools',
        'leadership_page': 'https://www.qacps.org/about'
    }
}

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    
    for county, urls in DISTRICTS.items():
        print(f"\n{'='*70}")
        print(f"{county} County")
        print('='*70)
        
        county_data = {
            'superintendent_contact': {},
            'principals': []
        }
        
        page = context.new_page()
        
        # Get superintendent contact info
        print(f"\n📞 Getting superintendent contact...")
        try:
            page.goto(urls['leadership_page'], wait_until='domcontentloaded', timeout=15000)
            page.wait_for_timeout(2000)
            
            content = page.locator('body').inner_text()
            
            # Find emails and phones
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
            phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', content)
            
            # Look for superintendent specific contact
            super_email = None
            super_phone = None
            
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'superintendent' in line.lower():
                    # Check nearby lines for contact info
                    nearby = '\n'.join(lines[max(0,i-2):min(len(lines),i+5)])
                    super_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', nearby)
                    super_phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', nearby)
                    if super_emails:
                        super_email = super_emails[0]
                    if super_phones:
                        super_phone = super_phones[0]
                    break
            
            county_data['superintendent_contact'] = {
                'url': urls['leadership_page'],
                'email': super_email or (emails[0] if emails else None),
                'phone': super_phone or (phones[0] if phones else None),
                'all_emails': emails[:3],
                'all_phones': phones[:3]
            }
            
            print(f"  Email: {super_email or (emails[0] if emails else 'Not found')}")
            print(f"  Phone: {super_phone or (phones[0] if phones else 'Not found')}")
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:100]}")
        
        # Get school pages and principals
        print(f"\n🏫 Finding school pages...")
        
        try:
            page.goto(urls['schools_page'], wait_until='domcontentloaded', timeout=15000)
            page.wait_for_timeout(2000)
            
            # Get all links on the schools page
            school_links = page.locator('a').all()
            school_urls = []
            
            for link in school_links:
                try:
                    href = link.get_attribute('href')
                    text = link.inner_text().strip()
                    
                    if href and text:
                        # Check if this looks like a school link
                        if any(keyword in text.lower() for keyword in ['elementary', 'middle', 'high', 'school', 'center']):
                            if href.startswith('/'):
                                href = urls['base_url'].rstrip('/') + href
                            elif not href.startswith('http'):
                                href = urls['base_url'].rstrip('/') + '/' + href
                            
                            school_urls.append({
                                'name': text,
                                'url': href
                            })
                except:
                    continue
            
            print(f"  Found {len(school_urls)} school pages")
            
            # Match schools from our list with district school pages
            county_schools = [s for s in schools if s['county'] == county]
            
            for school in county_schools:
                print(f"\n  {school['name']}")
                
                school_data = {
                    'school_name': school['name'],
                    'report_card_url': school['url'],
                    'district_url': None,
                    'principal': None,
                    'principal_email': None,
                    'school_phone': None
                }
                
                # Try to find matching district page
                school_name_clean = school['name'].lower().replace(' (', '').replace(')', '')
                
                matching_url = None
                for district_school in school_urls:
                    if any(word in district_school['name'].lower() for word in school_name_clean.split()[:2]):
                        matching_url = district_school['url']
                        break
                
                if matching_url:
                    school_data['district_url'] = matching_url
                    print(f"    District page: {matching_url}")
                    
                    try:
                        page.goto(matching_url, wait_until='domcontentloaded', timeout=15000)
                        page.wait_for_timeout(2000)
                        
                        content = page.locator('body').inner_text()
                        
                        # Look for principal
                        principal_patterns = [
                            r'Principal[:\s]+(?:Dr\.\s+)?([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)',
                            r'(?:Dr\.\s+)?([A-Z][a-z]+\s+[A-Z][a-z]+),?\s+Principal',
                            r'Principal:\s*([A-Z][^\n]+)',
                        ]
                        
                        for pattern in principal_patterns:
                            match = re.search(pattern, content)
                            if match:
                                school_data['principal'] = match.group(1).strip()
                                print(f"    Principal: {school_data['principal']}")
                                break
                        
                        # Get contact info
                        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
                        phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', content)
                        
                        if emails:
                            school_data['principal_email'] = emails[0]
                            print(f"    Email: {emails[0]}")
                        if phones:
                            school_data['school_phone'] = phones[0]
                            print(f"    Phone: {phones[0]}")
                        
                    except Exception as e:
                        print(f"    ❌ Error loading page: {str(e)[:50]}")
                else:
                    print(f"    ❌ No matching district page found")
                
                county_data['principals'].append(school_data)
        
        except Exception as e:
            print(f"  ❌ Error finding schools: {str(e)[:100]}")
        
        results[county] = county_data
        page.close()
    
    browser.close()

# Save results
with open('superintendent_contacts_and_principals.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n" + "="*70)
print("✅ COMPLETE")
print("="*70)
print("\nSaved to: superintendent_contacts_and_principals.json")

# Print summary
print("\nSUMMARY:")
for county, data in results.items():
    print(f"\n{county} County:")
    contact = data['superintendent_contact']
    if contact.get('email') or contact.get('phone'):
        print(f"  Superintendent: Email={bool(contact.get('email'))}, Phone={bool(contact.get('phone'))}")
    principals_found = sum(1 for p in data['principals'] if p['principal'])
    print(f"  Principals: {principals_found}/{len(data['principals'])} found")
    schools_matched = sum(1 for p in data['principals'] if p['district_url'])
    print(f"  District pages: {schools_matched}/{len(data['principals'])} matched")
