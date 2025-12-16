#!/usr/bin/env python3
"""
Scrape missing Grade 6-8 MCAP data for St. Michaels Middle/High School
Uses the same pattern as the successful scrape_detailed_mcap.py
"""

from playwright.sync_api import sync_playwright
import json
import time
import re

def extract_proficiency_from_page(page):
    """Extract proficiency percentage from assessment page"""
    try:
        # Wait for page to load
        page.wait_for_timeout(3000)
        
        # Click "Show Table" to reveal actual data
        try:
            show_table = page.locator('text=/Show Table/i')
            show_table.click(timeout=5000)
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"      Warning: Could not click Show Table: {e}")
        
        content = page.locator('body').inner_text()
        
        # Look for PL 3/4 (Performance Levels 3/4 = Proficient)
        pl34_matches = re.findall(r'PL\s*3/4[^\d]*(\d+\.?\d*)', content)
        
        if pl34_matches:
            return float(pl34_matches[-1])
        
        # Fallback: look for any proficiency pattern
        prof_matches = re.findall(r'(?:Proficient|Met)[:\s]*(\d+\.?\d*)%?', content, re.IGNORECASE)
        if prof_matches:
            return float(prof_matches[0])
            
    except Exception as e:
        print(f"      Error extracting: {e}")
    
    return None

def scrape_grade_subject(page, base_url, county_code, school_code, grade, subject):
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
            url = f"{base_url}/Graphs/#/Assessments/ElaPerformance/{grade}ELA/{grade}/6/3/1/{county_code}/{school_code}/2025"
        elif subject == 'Math':
            url = f"{base_url}/Graphs/#/Assessments/MathPerformance/{grade}MAT/{grade}/6/3/1/{county_code}/{school_code}/2025"
        elif subject == 'Science':
            url = f"{base_url}/Graphs/#/Assessments/SciencePerformance/{grade}/6/3/1/{county_code}/{school_code}/2025"
        else:
            result['error'] = f"Unknown subject: {subject}"
            return result
        
        print(f"      Navigating to: {url}")
        
        # Navigate and extract
        page.goto(url, wait_until='networkidle', timeout=15000)
        proficiency = extract_proficiency_from_page(page)
        
        if proficiency is not None:
            result['proficient_pct'] = proficiency
            print(f"      ✓ {subject} Grade {grade}: {proficiency}%")
        else:
            result['error'] = "No data found"
            print(f"      ✗ {subject} Grade {grade}: No data")
            
    except Exception as e:
        result['error'] = str(e)
        print(f"      ✗ {subject} Grade {grade}: Error - {str(e)[:50]}")
    
    return result

def main():
    """Scrape missing middle school grades"""
    
    base_url = "https://reportcard.msde.maryland.gov"
    
    schools_to_scrape = [
        {
            'name': 'St. Michaels Middle/High School',
            'county_code': '20',  # Talbot
            'school_code': '0202',
            'grades': [6, 7, 8]
        },
        {
            'name': 'South Dorchester School', 
            'county_code': '09',  # Dorchester
            'school_code': '0508',
            'grades': [6, 7, 8]
        }
    ]
    
    subjects = ['ELA', 'Math', 'Science']
    all_results = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for school in schools_to_scrape:
            print(f"\n{'='*80}")
            print(f"Scraping: {school['name']}")
            print(f"County: {school['county_code']}, School: {school['school_code']}")
            print(f"{'='*80}")
            
            school_scores = []
            
            for grade in school['grades']:
                print(f"\n  Grade {grade}:")
                for subject in subjects:
                    score_data = scrape_grade_subject(
                        page, base_url, 
                        school['county_code'], 
                        school['school_code'],
                        grade, subject
                    )
                    school_scores.append(score_data)
                    time.sleep(0.5)
            
            all_results[school['name']] = {
                'county_code': school['county_code'],
                'school_code': school['school_code'],
                'scores': school_scores
            }
        
        browser.close()
    
    # Save results
    output_file = 'missing_middle_grades.json'
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n{'='*80}")
    print("SCRAPING COMPLETE")
    print(f"{'='*80}")
    print(f"\n✓ Results saved to: {output_file}")
    
    # Display summary
    print("\n\nSUMMARY:")
    for school_name, data in all_results.items():
        print(f"\n{school_name}:")
        for score in data['scores']:
            if score['proficient_pct'] is not None:
                print(f"  Grade {score['grade']} {score['subject']}: {score['proficient_pct']}%")
            else:
                print(f"  Grade {score['grade']} {score['subject']}: No data ({score['error']})")

if __name__ == "__main__":
    main()
