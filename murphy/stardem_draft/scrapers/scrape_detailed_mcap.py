"""
Maryland Schools - Grade-Level MCAP Scores Scraper

Scrapes detailed grade-level performance data for ELA, Math, and Science
for all 50 schools across 5 counties.

URL Pattern:
ELA:     /Assessments/ElaPerformance/{grade}ELA/{grade}/6/3/1/{county_code}/{school_code}/2025
Math:    /Assessments/MathPerformance/{grade}MAT/{grade}/6/3/1/{county_code}/{school_code}/2025
Science: /Assessments/SciencePerformance/{grade}/6/3/1/{county_code}/{school_code}/2025
"""

from playwright.sync_api import sync_playwright
import json
import time
import re
from typing import Dict, List

# Extract county code and school code from school URL
def parse_school_url(url: str) -> tuple:
    """Extract county and school codes from report card URL"""
    # URL format: .../ReportCardSchool/1/{level}/1/{county_code}/{school_code}/0
    match = re.search(r'/(\d+)/(\d+)/0$', url)
    if match:
        return match.group(1), match.group(2)
    return None, None


# Determine which grades to test based on school name
def get_grades_for_school(school_name: str) -> List[int]:
    """Determine which grade levels to scrape based on school type"""
    name_lower = school_name.lower()
    
    if 'high' in name_lower:
        return [10]  # High schools - test grade 10
    elif 'middle' in name_lower:
        return [6, 7, 8]  # Middle schools
    elif 'elementary' in name_lower:
        return [3, 4, 5]  # Elementary schools
    elif 'career' in name_lower or 'technology' in name_lower:
        return []  # No standard MCAP
    elif 'early childhood' in name_lower:
        return []  # No MCAP
    else:
        # Default to elementary grades if unclear
        return [3, 4, 5]


class DetailedMCAPScraper:
    """Scraper for detailed grade-level MCAP scores"""
    
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
    
    def extract_proficiency_from_page(self) -> float:
        """Extract proficiency percentage from assessment page"""
        try:
            # Wait for page to load
            self.page.wait_for_timeout(3000)
            
            # Click "Show Table" to reveal actual data
            try:
                show_table = self.page.locator('text=/Show Table/i')
                show_table.click(timeout=5000)
                self.page.wait_for_timeout(2000)
            except Exception as e:
                print(f"      Warning: Could not click Show Table: {e}")
            
            content = self.page.locator('body').inner_text()
            
            # Look for PL 3/4 (Performance Levels 3/4 = Proficient)
            # Pattern: "2025   PL 3/4  26.5" or "PL 3/4  26.5"
            pl34_matches = re.findall(r'PL\s*3/4[^\d]*(\d+\.?\d*)', content)
            
            if pl34_matches:
                # Return the last match (most recent year)
                return float(pl34_matches[-1])
            
            # Fallback: look for any proficiency pattern
            prof_matches = re.findall(r'(?:Proficient|Met)[:\s]*(\d+\.?\d*)%?', content, re.IGNORECASE)
            if prof_matches:
                return float(prof_matches[0])
                
        except Exception as e:
            print(f"      Error extracting: {e}")
        
        return None
    
    def scrape_grade_subject(self, county_code: str, school_code: str, 
                            grade: int, subject: str) -> Dict:
        """Scrape a specific grade/subject combination"""
        
        result = {
            'grade': grade,
            'subject': subject,
            'proficient_pct': None,
            'error': None
        }
        
        try:
            # Build URL based on subject
            if subject == 'ELA':
                url = f"{self.base_url}/Graphs/#/Assessments/ElaPerformance/{grade}ELA/{grade}/6/3/1/{county_code}/{school_code}/2025"
            elif subject == 'Math':
                url = f"{self.base_url}/Graphs/#/Assessments/MathPerformance/{grade}MAT/{grade}/6/3/1/{county_code}/{school_code}/2025"
            elif subject == 'Science':
                url = f"{self.base_url}/Graphs/#/Assessments/SciencePerformance/{grade}/6/3/1/{county_code}/{school_code}/2025"
            else:
                result['error'] = f"Unknown subject: {subject}"
                return result
            
            # Navigate and extract
            self.page.goto(url, wait_until='networkidle', timeout=15000)
            proficiency = self.extract_proficiency_from_page()
            
            if proficiency is not None:
                result['proficient_pct'] = proficiency
                print(f"      {subject} Grade {grade}: {proficiency}%")
            else:
                result['error'] = "No data found"
                print(f"      {subject} Grade {grade}: No data")
                
        except Exception as e:
            result['error'] = str(e)
            print(f"      {subject} Grade {grade}: Error - {str(e)[:50]}")
        
        return result
    
    def scrape_school(self, school: Dict) -> Dict:
        """Scrape all grade-level data for a school"""
        
        print(f"\n  Scraping: {school['name']}")
        
        # Parse school codes from URL
        county_code, school_code = parse_school_url(school['url'])
        
        if not county_code or not school_code:
            print(f"    ✗ Could not parse codes from URL")
            return {
                'school_name': school['name'],
                'county': school['county'],
                'error': 'Could not parse URL codes',
                'scores': []
            }
        
        print(f"    Codes: County={county_code}, School={school_code}")
        
        # Determine grades to test
        grades = get_grades_for_school(school['name'])
        
        if not grades:
            print(f"    ○ No MCAP grades for this school type")
            return {
                'school_name': school['name'],
                'county': school['county'],
                'school_type': 'no_mcap',
                'scores': []
            }
        
        print(f"    Testing grades: {grades}")
        
        # Scrape each grade and subject
        all_scores = []
        subjects = ['ELA', 'Math', 'Science']
        
        for grade in grades:
            for subject in subjects:
                score_data = self.scrape_grade_subject(county_code, school_code, grade, subject)
                score_data['county_code'] = county_code
                score_data['school_code'] = school_code
                all_scores.append(score_data)
                time.sleep(0.5)  # Be polite
        
        result = {
            'school_name': school['name'],
            'county': school['county'],
            'county_code': county_code,
            'school_code': school_code,
            'grades_tested': grades,
            'scores': all_scores
        }
        
        return result
    
    def scrape_all_schools(self):
        """Scrape detailed MCAP scores for all schools"""
        
        # Load schools list
        with open('schools_list.json', 'r') as f:
            schools = json.load(f)
        
        print(f"Scraping Grade-Level MCAP Scores for {len(schools)} schools")
        print("="*80)
        
        all_results = []
        
        for i, school in enumerate(schools, 1):
            print(f"\n[{i}/{len(schools)}] {school['county']} County")
            result = self.scrape_school(school)
            all_results.append(result)
        
        # Save results
        output_json = 'mcap_grade_level_scores.json'
        output_csv = 'mcap_grade_level_scores.csv'
        
        with open(output_json, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        # Flatten for CSV
        self.create_csv(all_results, output_csv)
        
        print("\n" + "="*80)
        print("GRADE-LEVEL MCAP SCRAPING COMPLETE")
        print("="*80)
        
        # Summary statistics
        total_scores = sum(len(r['scores']) for r in all_results)
        successful_scores = sum(1 for r in all_results for s in r['scores'] if s.get('proficient_pct') is not None)
        
        print(f"\nTotal grade/subject combinations attempted: {total_scores}")
        print(f"Successful extractions: {successful_scores}")
        print(f"Success rate: {successful_scores/total_scores*100:.1f}%")
        
        print(f"\n✓ Saved detailed data to: {output_json}")
        print(f"✓ Saved CSV to: {output_csv}")
        
        return all_results
    
    def create_csv(self, results: List[Dict], output_file: str):
        """Create a flattened CSV from results"""
        import pandas as pd
        
        rows = []
        for school_result in results:
            school_name = school_result['school_name']
            county = school_result['county']
            
            for score in school_result.get('scores', []):
                rows.append({
                    'school_name': school_name,
                    'county': county,
                    'county_code': school_result.get('county_code', ''),
                    'school_code': school_result.get('school_code', ''),
                    'grade': score.get('grade', ''),
                    'subject': score.get('subject', ''),
                    'proficient_pct': score.get('proficient_pct', None),
                    'error': score.get('error', '')
                })
        
        df = pd.DataFrame(rows)
        df.to_csv(output_file, index=False)


def main():
    """Run the detailed MCAP scraper"""
    with DetailedMCAPScraper() as scraper:
        results = scraper.scrape_all_schools()
    
    print("\n" + "="*80)
    print("✅ ALL GRADE-LEVEL MCAP SCORES COLLECTED!")
    print("="*80)
    print("\nFiles created:")
    print("  • mcap_grade_level_scores.json - Detailed nested data")
    print("  • mcap_grade_level_scores.csv - Flat format for analysis")
    print("\nEach school now has:")
    print("  • ELA scores by grade")
    print("  • Math scores by grade")
    print("  • Science scores by grade")


if __name__ == "__main__":
    main()
