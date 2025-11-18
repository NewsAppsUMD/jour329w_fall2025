"""
Maryland School Report Card Data Scraper using Playwright
Handles JavaScript-rendered content

Scrapes school data from https://reportcard.msde.maryland.gov/SchoolsList/
for the five counties: Talbot, Kent, Dorchester, Caroline, Queen Anne's
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import json
import time
import os
from typing import Dict, List
import pandas as pd

# Target counties with their URL parameters
COUNTIES = {
    "Talbot": "20",
    "Kent": "14",
    "Dorchester": "09",
    "Caroline": "05",
    "Queen Anne's": "17"
}


class MDSchoolDataPlaywrightScraper:
    """Scraper for Maryland School Report Card data using Playwright"""
    
    def __init__(self):
        self.base_url = "https://reportcard.msde.maryland.gov"
        self.schools_list_url = f"{self.base_url}/SchoolsList/Index"
        self.playwright = None
        self.browser = None
        self.page = None
        
    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def get_county_schools(self, county_name: str, county_code: str) -> List[Dict]:
        """Get all schools for a specific county"""
        print(f"\n{'='*60}")
        print(f"Fetching schools for {county_name} County (code: {county_code})")
        print(f"{'='*60}")
        
        url = f"{self.schools_list_url}?l={county_code}"
        self.page.goto(url, wait_until='networkidle')
        
        # Wait for content to load
        self.page.wait_for_timeout(3000)
        
        schools = []
        
        try:
            # Get all links on the page
            links = self.page.locator('a').all()
            
            print(f"Found {len(links)} links on page")
            
            for link in links:
                try:
                    href = link.get_attribute("href")
                    text = link.inner_text().strip()
                    
                    # Filter for school-related links
                    # Look for ReportCardSchool URLs which contain school data
                    if href and "ReportCardSchool" in href and text and len(text) > 2:
                        full_url = href if href.startswith('http') else f"{self.base_url}{href}"
                        schools.append({
                            "name": text,
                            "url": full_url,
                            "county": county_name
                        })
                        print(f"  ✓ Found school: {text}")
                except Exception as e:
                    continue
            
        except Exception as e:
            print(f"Error getting schools: {e}")
        
        print(f"Total schools found for {county_name}: {len(schools)}")
        return schools
    
    def get_school_details(self, school: Dict) -> Dict:
        """Get detailed information for a specific school"""
        print(f"\n  Fetching details for: {school['name']}")
        
        try:
            self.page.goto(school['url'], wait_until='networkidle')
            self.page.wait_for_timeout(2000)
            
            details = {
                "school_name": school['name'],
                "county": school['county'],
                "url": school['url'],
            }
            
            # Get all visible text from the page
            body_text = self.page.locator('body').inner_text()
            details['page_content'] = body_text[:1000]  # First 1000 chars
            
            # Look for specific data sections
            # Try to find enrollment
            try:
                enrollment = self.page.locator('text=/enrollment/i').first
                if enrollment:
                    details['has_enrollment'] = True
            except:
                pass
            
            # Try to find demographics
            try:
                demo = self.page.locator('text=/demographic|race|ethnicity/i').first
                if demo:
                    details['has_demographics'] = True
            except:
                pass
            
            # Take a screenshot
            screenshot_dir = "/workspaces/jour329w_fall2025/murphy/stardem_draft/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = f"{screenshot_dir}/{school['county']}_{school['name'].replace(' ', '_')[:30]}.png"
            try:
                self.page.screenshot(path=screenshot_path, full_page=True)
                details['screenshot'] = screenshot_path
                print(f"    ✓ Saved screenshot to {screenshot_path}")
            except:
                pass
            
            return details
            
        except Exception as e:
            print(f"    Error: {e}")
            return {
                **school,
                "error": str(e)
            }
    
    def explore_county_page(self, county_name: str, county_code: str):
        """Explore a county page structure in detail"""
        print(f"\n{'='*60}")
        print(f"EXPLORING PAGE STRUCTURE: {county_name} County")
        print(f"{'='*60}")
        
        url = f"{self.schools_list_url}?l={county_code}"
        self.page.goto(url, wait_until='networkidle')
        self.page.wait_for_timeout(3000)
        
        # Save page source
        page_source_file = f"/workspaces/jour329w_fall2025/murphy/stardem_draft/page_source_{county_name}.html"
        content = self.page.content()
        with open(page_source_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Saved page source to: {page_source_file}")
        
        # Take screenshot
        screenshot_file = f"/workspaces/jour329w_fall2025/murphy/stardem_draft/screenshot_{county_name}.png"
        self.page.screenshot(path=screenshot_file, full_page=True)
        print(f"✓ Saved screenshot to: {screenshot_file}")
        
        # Print page text
        body_text = self.page.locator('body').inner_text()
        print(f"\nPage text (first 1000 chars):")
        print("=" * 60)
        print(body_text[:1000])
        print("=" * 60)
        
        # Find all clickable elements
        buttons = self.page.locator('a, button, [onclick]').all()
        print(f"\nClickable elements found: {len(buttons)}")
        for elem in buttons[:20]:  # First 20
            try:
                text = elem.inner_text().strip()
                tag = elem.evaluate('el => el.tagName')
                href = elem.get_attribute("href") or ""
                if text:
                    print(f"  {tag}: {text[:50]} | {href[:60]}")
            except:
                pass
    
    def scrape_all_counties(self, detailed=True):
        """Main method to scrape data for all target counties"""
        print("Starting Maryland School Data Scraper (Playwright)")
        print(f"Target counties: {', '.join(COUNTIES.keys())}\n")
        
        # Create screenshots directory
        os.makedirs("/workspaces/jour329w_fall2025/murphy/stardem_draft/screenshots", exist_ok=True)
        
        all_schools = []
        all_details = []
        
        # First, explore one county page to understand structure
        first_county = list(COUNTIES.items())[0]
        self.explore_county_page(first_county[0], first_county[1])
        
        # Get schools for each county
        for county_name, county_code in COUNTIES.items():
            schools = self.get_county_schools(county_name, county_code)
            all_schools.extend(schools)
            
            # Get detailed data if requested
            if detailed and schools:
                print(f"\nFetching detailed data for {county_name} schools...")
                # Get all schools for this county (not just first 3)
                for school in schools:
                    details = self.get_school_details(school)
                    all_details.append(details)
                    time.sleep(0.5)  # Small delay between requests
        
        # Save schools list
        schools_file = "/workspaces/jour329w_fall2025/murphy/stardem_draft/schools_list.json"
        with open(schools_file, "w", encoding="utf-8") as f:
            json.dump(all_schools, f, indent=2)
        print(f"\n✓ Saved schools list to: {schools_file}")
        
        # Save detailed data if collected
        if all_details:
            details_file = "/workspaces/jour329w_fall2025/murphy/stardem_draft/schools_detailed.json"
            with open(details_file, "w", encoding="utf-8") as f:
                json.dump(all_details, f, indent=2)
            print(f"✓ Saved detailed data to: {details_file}")
            
            # Also save as CSV for easy viewing
            try:
                df = pd.DataFrame(all_details)
                csv_file = "/workspaces/jour329w_fall2025/murphy/stardem_draft/schools_data.csv"
                df.to_csv(csv_file, index=False)
                print(f"✓ Saved CSV to: {csv_file}")
            except Exception as e:
                print(f"Could not save CSV: {e}")
        
        # Summary
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        print(f"Total schools found: {len(all_schools)}")
        
        by_county = {}
        for school in all_schools:
            county = school['county']
            by_county[county] = by_county.get(county, 0) + 1
        
        for county, count in sorted(by_county.items()):
            print(f"  {county}: {count} schools")
        
        return all_schools, all_details


def main():
    """Run the scraper"""
    with MDSchoolDataPlaywrightScraper() as scraper:
        schools, details = scraper.scrape_all_counties(detailed=True)
    
    print(f"\n{'='*60}")
    print("✅ SCRAPING COMPLETE!")
    print(f"{'='*60}")
    print(f"Collected data for {len(schools)} schools across 5 counties")
    print("\nFiles created:")
    print("  - schools_list.json: List of all schools with URLs")
    print("  - schools_detailed.json: Detailed data for each school")
    print("  - schools_data.csv: Data in CSV format")
    print("  - screenshots/: Screenshots of each school's page")


if __name__ == "__main__":
    main()
