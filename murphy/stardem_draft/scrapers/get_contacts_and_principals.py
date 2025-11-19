"""Get superintendent contact info and all school principals"""

from playwright.sync_api import sync_playwright
import json
import re

# Load schools list
with open('schools_list.json', 'r') as f:
    schools = json.load(f)

# District websites
DISTRICTS = {
    'Talbot': 'https://www.tcps.k12.md.us/',
    'Kent': 'https://www.kent.k12.md.us/',
    'Dorchester': 'https://www.dcpsmd.org/',
    'Caroline': 'https://www.carolineschools.org/',
    "Queen Anne's": 'https://www.qacps.org/'
}

# Superintendent contact and principals
results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    
    for county, base_url in DISTRICTS.items():
        print(f"\n{'='*70}")
        print(f"{county} County - Getting Superintendent Contact & Principals")
        print('='*70)
        
        county_data = {
            'superintendent_contact': {},
            'principals': []
        }
        
        page = context.new_page()
        
        # Try to find superintendent contact info
        super_urls = [
            base_url + 'page/leadership',
            base_url + 'leadership',
            base_url + 'about',
            base_url + 'staff',
            base_url + 'contact',
            base_url
        ]
        
        for url in super_urls:
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=15000)
                page.wait_for_timeout(2000)
                
                content = page.locator('body').inner_text()
                
                # Look for superintendent email/phone
                if 'superintendent' in content.lower():
                    # Find email
                    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                    emails = re.findall(email_pattern, content)
                    
                    # Find phone
                    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
                    phones = re.findall(phone_pattern, content)
                    
                    if emails or phones:
                        county_data['superintendent_contact'] = {
                            'url': url,
                            'emails': list(set(emails))[:3],
                            'phones': list(set(phones))[:3]
                        }
                        print(f"  ✓ Found superintendent contact at {url}")
                        break
            except:
                continue
        
        # Get principals for each school in this county
        county_schools = [s for s in schools if s['county'] == county]
        print(f"\n  Getting principals for {len(county_schools)} schools...")
        
        for i, school in enumerate(county_schools, 1):
            print(f"    [{i}/{len(county_schools)}] {school['name']}")
            
            school_data = {
                'school_name': school['name'],
                'school_url': school['url'],
                'principal': None,
                'principal_email': None,
                'school_phone': None
            }
            
            try:
                page.goto(school['url'], wait_until='domcontentloaded', timeout=15000)
                page.wait_for_timeout(2000)
                
                content = page.locator('body').inner_text()
                
                # Look for principal name
                principal_patterns = [
                    r'Principal[:\s]+(?:Dr\.\s+)?([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)',
                    r'(?:Dr\.\s+)?([A-Z][a-z]+\s+[A-Z][a-z]+),?\s+Principal',
                ]
                
                for pattern in principal_patterns:
                    match = re.search(pattern, content)
                    if match:
                        school_data['principal'] = match.group(1)
                        break
                
                # Get email and phone
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
                phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', content)
                
                if emails:
                    school_data['principal_email'] = emails[0]
                if phones:
                    school_data['school_phone'] = phones[0]
                
                if school_data['principal']:
                    print(f"        Principal: {school_data['principal']}")
                
            except Exception as e:
                print(f"        Error: {str(e)[:50]}")
            
            county_data['principals'].append(school_data)
        
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
    if data['superintendent_contact']:
        print(f"  Superintendent Contact: {len(data['superintendent_contact'].get('emails', []))} emails, {len(data['superintendent_contact'].get('phones', []))} phones")
    principals_found = sum(1 for p in data['principals'] if p['principal'])
    print(f"  Principals: {principals_found}/{len(data['principals'])} found")
