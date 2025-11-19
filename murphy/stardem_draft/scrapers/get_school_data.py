"""
Maryland School Report Card Data Scraper

Scrapes school data from https://reportcard.msde.maryland.gov/SchoolsList/
for the five counties: Talbot, Kent, Dorchester, Caroline, Queen Anne's
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from typing import Dict, List
import pandas as pd

# Target counties
COUNTIES = [
    "Talbot",
    "Kent", 
    "Dorchester",
    "Caroline",
    "Queen Anne's"
]

class MDSchoolDataScraper:
    """Scraper for Maryland School Report Card data"""
    
    def __init__(self):
        self.base_url = "https://reportcard.msde.maryland.gov"
        self.schools_list_url = f"{self.base_url}/SchoolsList/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_schools_page(self):
        """Fetch the main schools list page"""
        print(f"Fetching schools list from {self.schools_list_url}")
        response = self.session.get(self.schools_list_url)
        response.raise_for_status()
        return response.text
    
    def parse_schools_list(self, html: str) -> List[Dict]:
        """Parse the schools list HTML to extract school information"""
        soup = BeautifulSoup(html, 'html.parser')
        schools = []
        
        # This will need to be adjusted based on actual page structure
        # Looking for tables, divs, or other elements containing school data
        print("Parsing HTML structure...")
        
        # Find all links or entries for schools
        # Common patterns: tables with school names, dropdown menus, etc.
        school_links = soup.find_all('a', href=True)
        
        for link in school_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Filter for school-related links
            if 'school' in href.lower() or 'SchoolPerformance' in href:
                schools.append({
                    'name': text,
                    'url': href if href.startswith('http') else f"{self.base_url}{href}"
                })
        
        return schools
    
    def filter_by_county(self, schools: List[Dict]) -> Dict[str, List[Dict]]:
        """Filter schools by target counties"""
        schools_by_county = {county: [] for county in COUNTIES}
        
        for school in schools:
            school_name = school.get('name', '')
            # Check if any county name appears in the school name or details
            for county in COUNTIES:
                if county.lower() in school_name.lower():
                    schools_by_county[county].append(school)
                    break
        
        return schools_by_county
    
    def get_school_details(self, school_url: str) -> Dict:
        """Fetch detailed information for a specific school"""
        print(f"  Fetching details from {school_url}")
        try:
            response = self.session.get(school_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            details = {
                'url': school_url,
                'raw_html': response.text[:1000]  # First 1000 chars for debugging
            }
            
            # Extract various data points - adjust selectors based on actual page structure
            # Common data points: enrollment, demographics, test scores, etc.
            
            # Look for tables with data
            tables = soup.find_all('table')
            if tables:
                details['tables_found'] = len(tables)
            
            # Look for key statistics
            stats_divs = soup.find_all('div', class_=lambda x: x and ('stat' in x.lower() or 'data' in x.lower()))
            if stats_divs:
                details['stats_sections'] = len(stats_divs)
            
            return details
            
        except Exception as e:
            print(f"    Error fetching school details: {e}")
            return {'url': school_url, 'error': str(e)}
    
    def explore_page_structure(self):
        """Explore the page structure to understand how to extract data"""
        html = self.get_schools_page()
        soup = BeautifulSoup(html, 'html.parser')
        
        print("\n=== Page Structure Analysis ===")
        
        # Check for forms
        forms = soup.find_all('form')
        print(f"\nForms found: {len(forms)}")
        for i, form in enumerate(forms[:3]):  # First 3 forms
            print(f"  Form {i+1}: action='{form.get('action')}', method='{form.get('method')}'")
            inputs = form.find_all('input')
            selects = form.find_all('select')
            print(f"    Inputs: {len(inputs)}, Selects: {len(selects)}")
        
        # Check for dropdowns/selects (common for county/school selection)
        selects = soup.find_all('select')
        print(f"\nSelect dropdowns found: {len(selects)}")
        for select in selects[:5]:  # First 5 selects
            select_id = select.get('id', 'no-id')
            select_name = select.get('name', 'no-name')
            options = select.find_all('option')
            print(f"  Select: id='{select_id}', name='{select_name}', options={len(options)}")
            
            # Check if county names appear in options
            for option in options:
                option_text = option.get_text(strip=True)
                if any(county.lower() in option_text.lower() for county in COUNTIES):
                    print(f"    ✓ Found county option: {option_text} (value={option.get('value')})")
        
        # Check for tables
        tables = soup.find_all('table')
        print(f"\nTables found: {len(tables)}")
        
        # Check for iframes (some sites load data in iframes)
        iframes = soup.find_all('iframe')
        print(f"\nIframes found: {len(iframes)}")
        for iframe in iframes:
            print(f"  Iframe src: {iframe.get('src')}")
        
        # Look for JavaScript that might load data dynamically
        scripts = soup.find_all('script', src=True)
        print(f"\nExternal scripts: {len(scripts)}")
        
        # Save the HTML for manual inspection
        output_file = '/workspaces/jour329w_fall2025/murphy/stardem_draft/schools_page_structure.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"\n✓ Saved full HTML to: {output_file}")
        
        return soup
    
    def scrape_all_counties(self):
        """Main method to scrape data for all target counties"""
        print("Starting Maryland School Data Scraper")
        print(f"Target counties: {', '.join(COUNTIES)}\n")
        
        # First, explore the page structure
        soup = self.explore_page_structure()
        
        # Get and parse schools list
        html = self.get_schools_page()
        schools = self.parse_schools_list(html)
        
        print(f"\nFound {len(schools)} potential school entries")
        
        # Filter by county
        schools_by_county = self.filter_by_county(schools)
        
        # Report findings
        print("\n=== Schools by County ===")
        for county, county_schools in schools_by_county.items():
            print(f"{county} County: {len(county_schools)} schools")
        
        # Get detailed data for each school (limit to avoid overwhelming)
        all_data = []
        for county, county_schools in schools_by_county.items():
            print(f"\nFetching details for {county} County schools...")
            for school in county_schools[:5]:  # Limit to first 5 per county for testing
                details = self.get_school_details(school['url'])
                details['county'] = county
                details['school_name'] = school['name']
                all_data.append(details)
                time.sleep(1)  # Be polite, wait between requests
        
        # Save results
        output_file = '/workspaces/jour329w_fall2025/murphy/stardem_draft/schools_data.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2)
        
        print(f"\n✓ Saved data to: {output_file}")
        print(f"Total schools scraped: {len(all_data)}")
        
        return all_data


def main():
    """Run the scraper"""
    scraper = MDSchoolDataScraper()
    data = scraper.scrape_all_counties()
    
    print("\n=== Summary ===")
    print(f"Total records collected: {len(data)}")
    
    # Group by county for summary
    by_county = {}
    for record in data:
        county = record.get('county', 'Unknown')
        by_county[county] = by_county.get(county, 0) + 1
    
    for county, count in sorted(by_county.items()):
        print(f"  {county}: {count} schools")


if __name__ == "__main__":
    main()
