#!/usr/bin/env python3
"""
Scrape Maryland Report Card using requests - simpler approach.
The site appears to be Angular-based, so we'll try accessing the API directly.
"""

import requests
import json
import time

DISTRICTS = {
    'Talbot': '20',
    'Kent': '14',
    'Dorchester': '10',
    'Caroline': '07',
    "Queen Anne's": '18'
}

def scrape_district_enrollment(county, lss_code):
    """Try to get enrollment data directly from the Maryland Report Card API."""
    
    print(f"\n{'='*70}")
    print(f"Scraping {county} County (LSS: {lss_code})")
    print('='*70)
    
    # Try different possible API endpoints
    base_urls = [
        f"https://reportcard.msde.maryland.gov/Graphs/api/ReportCardSearch/GetGraphData",
        f"https://reportcard.msde.maryland.gov/api/Demographics/Enrollment",
        f"https://reportcard.msde.maryland.gov/Graphs/api/GetData"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': f'https://reportcard.msde.maryland.gov/Graphs/#/Demographics/DemoEnrollment/2/17/1/{lss_code}/XXXX'
    }
    
    # Try to find the actual API call by examining network traffic patterns
    # Most Angular apps use /api/ endpoints
    api_params = {
        'reportLevel': '1',  # District level
        'lss': lss_code,
        'schoolNumber': 'XXXX',
        'reportYear': '17',  # 2023-2024 school year
        'topic': '2',  # Demographics
        'subtopic': 'DemoEnrollment'
    }
    
    for base_url in base_urls:
        try:
            print(f"  Trying: {base_url}")
            response = requests.get(base_url, params=api_params, headers=headers, timeout=10)
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  ✓ Got JSON response!")
                    return {
                        'county': county,
                        'lss_code': lss_code,
                        'data': data,
                        'source_url': base_url
                    }
                except json.JSONDecodeError:
                    print(f"  Response not JSON: {response.text[:200]}")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    # If API doesn't work, try direct page scraping with requests
    print("\n  Trying direct page scraping...")
    page_url = f"https://reportcard.msde.maryland.gov/Graphs/#/Demographics/DemoEnrollment/2/17/1/{lss_code}/XXXX"
    
    try:
        response = requests.get(page_url, headers=headers, timeout=10)
        print(f"  Page status: {response.status_code}")
        
        # Look for JSON data embedded in the page
        html = response.text
        if 'enrollment' in html.lower() or 'demographic' in html.lower():
            print(f"  Found relevant keywords in page ({len(html)} chars)")
            return {
                'county': county,
                'lss_code': lss_code,
                'html_sample': html[:1000],
                'note': 'Page loaded but may need JavaScript execution'
            }
    except Exception as e:
        print(f"  ✗ Page scrape error: {e}")
    
    return {
        'county': county,
        'lss_code': lss_code,
        'error': 'Could not fetch data from any endpoint'
    }

def main():
    results = []
    
    print("="*70)
    print("Maryland Report Card - Demographics Scraper (Requests)")
    print("="*70)
    
    for county, lss_code in DISTRICTS.items():
        data = scrape_district_enrollment(county, lss_code)
        results.append(data)
        time.sleep(1)  # Be nice to the server
    
    # Save results
    output_file = 'district_demographics_requests.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✅ Complete!")
    print(f"{'='*70}")
    print(f"Results saved to: {output_file}")
    
    # Summary
    for result in results:
        county = result['county']
        if 'data' in result:
            print(f"  {county}: ✓ Got data")
        elif 'html_sample' in result:
            print(f"  {county}: ⚠ Got HTML (needs JS)")
        else:
            print(f"  {county}: ✗ Failed")

if __name__ == "__main__":
    main()
