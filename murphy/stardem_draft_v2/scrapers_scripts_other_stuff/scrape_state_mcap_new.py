#!/usr/bin/env python3
"""
Scrape statewide MCAP average data from MSDE Report Card website.
Scrapes ELA 5, ELA 8, ELA 10, Math 5, Math 8, Math Algebra I, Science 5, Science 8, Science Biology.
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
        # Pattern: "2025   PL 3/4  26.5" or "PL 3/4  26.5"
        pl34_matches = re.findall(r'PL\s*3/4[^\d]*(\d+\.?\d*)', content)
        
        if pl34_matches:
            # Return the last match (most recent year)
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


def scrape_statewide_mcap():
    """Scrape statewide MCAP proficiency data"""
    
    base_url = "https://reportcard.msde.maryland.gov"
    
    # Data structure
    mcap_data = {
        "ELA_5": None,
        "ELA_8": None,
        "ELA_10": None,
        "Math_5": None,
        "Math_8": None,
        "Math_Algebra_1": None,
        "Science_5": None,
        "Science_8": None,
        "Science_All_High": None,
        "metadata": {
            "source": "Maryland Report Card",
            "date_scraped": datetime.now().strftime("%Y-%m-%d"),
            "url": "https://reportcard.msde.maryland.gov/",
            "note": "Statewide MCAP proficiency rates (PL 3/4)"
        }
    }
    
    # Define what to scrape: (key, subject_type, grade_code, grade_num, display_name)
    # State level: county_code=99, school_code=XXXX
    scrape_list = [
        ("ELA_5", "ElaPerformance", "5ELA", "5", "ELA Grade 5"),
        ("ELA_8", "ElaPerformance", "8ELA", "8", "ELA Grade 8"),
        ("ELA_10", "ElaPerformance", "10ELA", "10", "ELA Grade 10"),
        ("Math_5", "MathPerformance", "5MAT", "5", "Math Grade 5"),
        ("Math_8", "MathPerformance", "8MAT", "8", "Math Grade 8"),
        ("Math_Algebra_1", "MathPerformance", "UALG01", "99", "Math - Algebra 1"),
        ("Science_5", "SciencePerformance", "5", "5", "Science Grade 5"),
        ("Science_8", "SciencePerformance", "8", "8", "Science Grade 8"),
        ("Science_All_High", "SciencePerformance", "A", "A", "All High"),
    ]
    
    print("Starting statewide MCAP data scraping...")
    print("=" * 80)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for key, subject_type, grade_code, grade_num, display_name in scrape_list:
            print(f"\nScraping {display_name}...")
            
            try:
                # Build URL for statewide data
                # Science has a different URL pattern - no grade code in the path
                if subject_type == "SciencePerformance":
                    url = f"{base_url}/Graphs/#/Assessments/{subject_type}/{grade_num}/6/3/1/99/XXXX/2025"
                else:
                    url = f"{base_url}/Graphs/#/Assessments/{subject_type}/{grade_code}/{grade_num}/6/3/1/99/XXXX/2025"
                print(f"  URL: {url}")
                
                # Navigate to page
                page.goto(url, wait_until='networkidle', timeout=15000)
                
                # Extract proficiency
                proficiency = extract_proficiency_from_page(page)
                
                if proficiency is not None:
                    mcap_data[key] = proficiency
                    print(f"  ✓ Proficiency: {proficiency}%")
                else:
                    print(f"  ✗ No data found")
                
                time.sleep(1)  # Be polite
                
            except Exception as e:
                print(f"  ✗ Error: {str(e)[:100]}")
        
        browser.close()
    
    # Save results
    output_file = "state_mcap_averages.json"
    with open(output_file, 'w') as f:
        json.dump(mcap_data, f, indent=2)
    
    print("\n" + "=" * 80)
    print("STATEWIDE MCAP SCRAPING COMPLETE")
    print("=" * 80)
    print(f"\n✓ Saved to: {output_file}")
    
    print("\nResults:")
    for key, value in mcap_data.items():
        if key != "metadata" and value is not None:
            print(f"  {key}: {value}%")
    
    return mcap_data


if __name__ == "__main__":
    scrape_statewide_mcap()
