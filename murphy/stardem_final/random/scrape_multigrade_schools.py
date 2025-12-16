#!/usr/bin/env python3
"""
Scrape MCAP data for multi-grade schools:
- South Dorchester School (PreK-8): needs Grade 5 and Grade 8 scores
- St. Michaels Middle/High School (6-12): needs Grade 8 and Grade 10 scores
"""

from playwright.sync_api import sync_playwright
import json
import time
import re
from datetime import datetime


def extract_proficiency_from_page(page) -> float:
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
        
        # Fallback: look for Level 3 + Level 4
        level_3_match = re.search(r'Level\s*3[^\d]*(\d+\.?\d*)\s*%?', content, re.IGNORECASE)
        level_4_match = re.search(r'Level\s*4[^\d]*(\d+\.?\d*)\s*%?', content, re.IGNORECASE)
        
        if level_3_match and level_4_match:
            level_3 = float(level_3_match.group(1))
            level_4 = float(level_4_match.group(1))
            return level_3 + level_4
            
    except Exception as e:
        print(f"      Error extracting: {e}")
    
    return None


def scrape_school_mcap(school_name, county_code, school_code, assessments):
    """
    Scrape MCAP data for a specific school
    
    Args:
        school_name: Display name
        county_code: County LSS code (17=Dorchester, 19=Talbot)
        school_code: School code
        assessments: List of (key, subject_type, grade_code, grade_num, display_name)
    """
    
    base_url = "https://reportcard.msde.maryland.gov"
    results = {}
    
    print(f"\n{'=' * 80}")
    print(f"Scraping {school_name}")
    print(f"County: {county_code}, School: {school_code}")
    print(f"{'=' * 80}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for key, subject_type, grade_code, grade_num, display_name in assessments:
            print(f"\n{display_name}...")
            
            try:
                # Build URL
                if subject_type == "SciencePerformance":
                    url = f"{base_url}/Graphs/#/Assessments/{subject_type}/{grade_num}/6/3/1/{county_code}/{school_code}/2025"
                else:
                    url = f"{base_url}/Graphs/#/Assessments/{subject_type}/{grade_code}/{grade_num}/6/3/1/{county_code}/{school_code}/2025"
                
                print(f"  URL: {url}")
                
                # Navigate
                page.goto(url, wait_until='networkidle', timeout=15000)
                
                # Extract proficiency
                proficiency = extract_proficiency_from_page(page)
                
                if proficiency is not None:
                    results[key] = proficiency
                    print(f"  ✓ Proficiency: {proficiency}%")
                else:
                    print(f"  ✗ No data found")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"  ✗ Error: {str(e)[:100]}")
        
        browser.close()
    
    return results


def main():
    """Main scraping function"""
    
    all_results = {}
    
    # South Dorchester School (PreK-8)
    # Dorchester County code: 17, School code: 0231
    south_dorchester_assessments = [
        # Grade 5
        ("ELA_G5", "ElaPerformance", "5ELA", "5", "Grade 5 ELA"),
        ("Math_G5", "MathPerformance", "5MAT", "5", "Grade 5 Math"),
        ("Science_G5", "SciencePerformance", "5", "5", "Grade 5 Science"),
        # Grade 8
        ("ELA_G8", "ElaPerformance", "8ELA", "8", "Grade 8 ELA"),
        ("Math_G8", "MathPerformance", "8MAT", "8", "Grade 8 Math"),
        ("Science_G8", "SciencePerformance", "8", "8", "Grade 8 Science"),
    ]
    
    all_results["South Dorchester School"] = scrape_school_mcap(
        "South Dorchester School",
        "17",  # Dorchester County
        "0231",  # South Dorchester School code
        south_dorchester_assessments
    )
    
    # St. Michaels Middle/High School (6-12)
    # Talbot County code: 19, School code: 0501
    st_michaels_assessments = [
        # Grade 8 (Middle School)
        ("ELA_G8", "ElaPerformance", "8ELA", "8", "Grade 8 ELA"),
        ("Math_G8", "MathPerformance", "8MAT", "8", "Grade 8 Math"),
        ("Science_G8", "SciencePerformance", "8", "8", "Grade 8 Science"),
        # Grade 10 / High School
        ("ELA_G10", "ElaPerformance", "10ELA", "10", "Grade 10 ELA"),
        ("Math_Algebra1", "MathPerformance", "UALG01", "99", "Algebra I"),
        ("Science_HS", "SciencePerformance", "A", "A", "High School Science"),
    ]
    
    all_results["St. Michaels Middle/High School"] = scrape_school_mcap(
        "St. Michaels Middle/High School",
        "19",  # Talbot County
        "0501",  # St. Michaels Middle/High code
        st_michaels_assessments
    )
    
    # Save results
    output_file = "multigrade_schools_mcap.json"
    with open(output_file, 'w') as f:
        json.dump({
            "schools": all_results,
            "metadata": {
                "source": "Maryland Report Card",
                "date_scraped": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "url": "https://reportcard.msde.maryland.gov/",
                "note": "MCAP proficiency rates for multi-grade schools"
            }
        }, f, indent=2)
    
    print(f"\n{'=' * 80}")
    print("SCRAPING COMPLETE")
    print(f"{'=' * 80}")
    print(f"\n✓ Saved to: {output_file}")
    
    print("\n\nRESULTS SUMMARY:")
    for school_name, data in all_results.items():
        print(f"\n{school_name}:")
        for key, value in data.items():
            print(f"  {key}: {value}%")


if __name__ == "__main__":
    main()
