"""
Maryland School Report Card Data Scraper using Selenium
Handles JavaScript-rendered content

Scrapes school data from https://reportcard.msde.maryland.gov/SchoolsList/
for the five counties: Talbot, Kent, Dorchester, Caroline, Queen Anne's
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
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


class MDSchoolDataSeleniumScraper:
    """Scraper for Maryland School Report Card data using Selenium"""
    
    def __init__(self, headless=True):
        self.base_url = "https://reportcard.msde.maryland.gov"
        self.schools_list_url = f"{self.base_url}/SchoolsList/Index"
        
        # Setup Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # Use webdriver-manager to automatically handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def get_county_schools(self, county_name: str, county_code: str) -> List[Dict]:
        """Get all schools for a specific county"""
        print(f"\n{'='*60}")
        print(f"Fetching schools for {county_name} County (code: {county_code})")
        print(f"{'='*60}")
        
        url = f"{self.schools_list_url}?l={county_code}"
        self.driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        schools = []
        
        try:
            # Look for school links or listings
            # Common patterns: links with school names, table rows, list items
            
            # Try to find all links that might be schools
            links = self.driver.find_elements(By.TAG_NAME, "a")
            
            print(f"Found {len(links)} links on page")
            
            for link in links:
                try:
                    href = link.get_attribute("href")
                    text = link.text.strip()
                    
                    # Filter for school-related links
                    if href and "SchoolPerformance" in href and text:
                        schools.append({
                            "name": text,
                            "url": href,
                            "county": county_name
                        })
                        print(f"  ✓ Found school: {text}")
                except:
                    continue
            
            # Also try to find divs or other elements with school data
            school_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-school], .school-item, .school-card")
            print(f"Found {len(school_elements)} school elements by CSS selector")
            
        except Exception as e:
            print(f"Error getting schools: {e}")
        
        print(f"Total schools found for {county_name}: {len(schools)}")
        return schools
    
    def get_school_details(self, school: Dict) -> Dict:
        """Get detailed information for a specific school"""
        print(f"\n  Fetching details for: {school['name']}")
        
        try:
            self.driver.get(school['url'])
            time.sleep(2)
            
            details = {
                "school_name": school['name'],
                "county": school['county'],
                "url": school['url'],
            }
            
            # Extract enrollment data
            try:
                enrollment_elem = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Enrollment')]")
                details['enrollment_section'] = enrollment_elem.text
            except NoSuchElementException:
                print("    No enrollment data found")
            
            # Extract demographics
            try:
                demo_elems = self.driver.find_elements(By.CSS_SELECTOR, "[class*='demographic'], [class*='race']")
                if demo_elems:
                    details['demographics'] = [elem.text for elem in demo_elems[:10]]
            except:
                pass
            
            # Extract test scores/performance data
            try:
                score_elems = self.driver.find_elements(By.CSS_SELECTOR, "[class*='score'], [class*='performance']")
                if score_elems:
                    details['performance_data'] = [elem.text for elem in score_elems[:10]]
            except:
                pass
            
            # Get all text content from the page
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            details['page_text_sample'] = page_text[:500]  # First 500 chars
            
            # Take a screenshot for reference
            screenshot_path = f"/workspaces/jour329w_fall2025/murphy/stardem_draft/screenshots/{school['county']}_{school['name'].replace(' ', '_')[:30]}.png"
            try:
                self.driver.save_screenshot(screenshot_path)
                details['screenshot'] = screenshot_path
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
        self.driver.get(url)
        time.sleep(3)
        
        # Save page source
        page_source_file = f"/workspaces/jour329w_fall2025/murphy/stardem_draft/page_source_{county_name}.html"
        with open(page_source_file, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        print(f"✓ Saved page source to: {page_source_file}")
        
        # Take screenshot
        screenshot_file = f"/workspaces/jour329w_fall2025/murphy/stardem_draft/screenshot_{county_name}.png"
        self.driver.save_screenshot(screenshot_file)
        print(f"✓ Saved screenshot to: {screenshot_file}")
        
        # Print page text
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        print(f"\nPage text (first 1000 chars):")
        print("=" * 60)
        print(body_text[:1000])
        print("=" * 60)
        
        # Find all clickable elements
        clickable = self.driver.find_elements(By.CSS_SELECTOR, "a, button, [onclick]")
        print(f"\nClickable elements found: {len(clickable)}")
        for elem in clickable[:20]:  # First 20
            try:
                text = elem.text.strip()
                tag = elem.tag_name
                href = elem.get_attribute("href") or ""
                if text:
                    print(f"  {tag}: {text[:50]} | {href[:60]}")
            except:
                pass
    
    def scrape_all_counties(self, detailed=False):
        """Main method to scrape data for all target counties"""
        print("Starting Maryland School Data Scraper (Selenium)")
        print(f"Target counties: {', '.join(COUNTIES.keys())}\n")
        
        # Create screenshots directory
        import os
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
                for school in schools[:3]:  # Limit to first 3 per county for testing
                    details = self.get_school_details(school)
                    all_details.append(details)
                    time.sleep(1)
        
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
    scraper = MDSchoolDataSeleniumScraper(headless=True)
    
    try:
        schools, details = scraper.scrape_all_counties(detailed=False)
    finally:
        scraper.driver.quit()


if __name__ == "__main__":
    main()
