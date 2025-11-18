"""
Maryland School MCAP Test Scores Scraper

Directly scrapes MCAP test score data from Maryland Report Card website
for all 50 schools across 5 counties.
"""

from playwright.sync_api import sync_playwright
import json
import time
import re
from typing import Dict, List

def extract_mcap_from_page(page) -> Dict:
    """Extract MCAP test scores from the current page"""
    scores = {}
    
    try:
        # Wait for MCAP content to load
        page.wait_for_timeout(2000)
        
        # Get all text content
        content = page.locator('body').inner_text()
        
        # Look for proficiency percentages
        # Pattern: "XX% Proficient" or "XX.X% Proficient"
        proficient_matches = re.findall(r'(\d+\.?\d*)%?\s*Proficient', content, re.IGNORECASE)
        
        # Look for subject areas and their scores
        # ELA scores
        ela_section = re.search(r'English Language Arts.*?(\d+\.?\d*)%', content, re.IGNORECASE | re.DOTALL)
        if ela_section:
            scores['ela_proficient'] = float(ela_section.group(1))
        
        # Math scores  
        math_section = re.search(r'Mathematics.*?(\d+\.?\d*)%', content, re.IGNORECASE | re.DOTALL)
        if math_section:
            scores['math_proficient'] = float(math_section.group(1))
            
        # Science scores
        science_section = re.search(r'Science.*?(\d+\.?\d*)%', content, re.IGNORECASE | re.DOTALL)
        if science_section:
            scores['science_proficient'] = float(science_section.group(1))
        
        # If no specific subjects found, try to get any proficiency numbers
        if not scores and proficient_matches:
            # Take first few proficiency numbers found
            for i, match in enumerate(proficient_matches[:3]):
                scores[f'proficient_{i+1}'] = float(match)
                
    except Exception as e:
        print(f"      Error extracting scores: {e}")
    
    return scores


class MCAPScoresScraper:
    """Scraper for MCAP test scores"""
    
    def __init__(self):
        self.base_url = "https://reportcard.msde.maryland.gov"
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
    
    def get_mcap_scores(self, school: Dict) -> Dict:
        """Navigate to school's MCAP page and extract scores"""
        print(f"  Fetching MCAP data for: {school['name']}")
        
        result = {
            'school_name': school['name'],
            'county': school['county'],
            'url': school['url']
        }
        
        try:
            # Navigate to school page
            self.page.goto(school['url'], wait_until='networkidle')
            self.page.wait_for_timeout(2000)
            
            # Click on MCAP tab
            try:
                mcap_tab = self.page.locator('text=/MCAP/i').first
                mcap_tab.click()
                self.page.wait_for_timeout(3000)
                
                # Extract scores
                scores = extract_mcap_from_page(self.page)
                result.update(scores)
                
                if scores:
                    score_str = ', '.join([f"{k}: {v}%" for k, v in scores.items()])
                    print(f"    ✓ Scores: {score_str}")
                else:
                    print(f"    ○ No scores found")
                    
            except Exception as e:
                print(f"    ○ MCAP tab not found or error: {e}")
                result['error'] = str(e)
            
        except Exception as e:
            print(f"    ✗ Error loading page: {e}")
            result['error'] = str(e)
        
        return result
    
    def scrape_all_schools(self):
        """Scrape MCAP scores for all schools"""
        
        # Load schools list
        with open('schools_list.json', 'r') as f:
            schools = json.load(f)
        
        print(f"Scraping MCAP Scores for {len(schools)} schools")
        print("="*80)
        
        all_results = []
        
        for i, school in enumerate(schools, 1):
            print(f"\n[{i}/{len(schools)}] {school['county']} County")
            result = self.get_mcap_scores(school)
            all_results.append(result)
            time.sleep(0.5)  # Be polite
        
        # Save results
        output_json = 'mcap_test_scores.json'
        output_csv = 'mcap_test_scores.csv'
        
        with open(output_json, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        # Convert to CSV
        import pandas as pd
        df = pd.DataFrame(all_results)
        df.to_csv(output_csv, index=False)
        
        print("\n" + "="*80)
        print("MCAP SCORES EXTRACTION COMPLETE")
        print("="*80)
        
        # Count schools with scores
        schools_with_ela = sum(1 for r in all_results if 'ela_proficient' in r)
        schools_with_math = sum(1 for r in all_results if 'math_proficient' in r)
        schools_with_science = sum(1 for r in all_results if 'science_proficient' in r)
        schools_with_any = sum(1 for r in all_results if any(k.startswith(('ela', 'math', 'science', 'proficient')) for k in r.keys() if k not in ['school_name', 'county', 'url', 'error']))
        
        print(f"\nSchools with ELA scores: {schools_with_ela}")
        print(f"Schools with Math scores: {schools_with_math}")
        print(f"Schools with Science scores: {schools_with_science}")
        print(f"Schools with any test scores: {schools_with_any}")
        
        print(f"\n✓ Saved to: {output_json}")
        print(f"✓ Saved to: {output_csv}")
        
        return all_results


def main():
    """Run the MCAP scores scraper"""
    with MCAPScoresScraper() as scraper:
        results = scraper.scrape_all_schools()


if __name__ == "__main__":
    main()
