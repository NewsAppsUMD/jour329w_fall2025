#!/usr/bin/env python3
"""
Scrape district-level MCAP data from MSDE Report Card website.
Gets 2025 PL 3/4 proficiency rates for ELA, Math, and Science for Eastern Shore counties.
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
            # Table might already be showing
            pass
        
        content = page.locator('body').inner_text()
        
        # For graduation rate, look for different pattern
        if "Graduation Rate" in content or "Four-Year" in content:
            # Look for graduation rate percentage
            match = re.search(r'2024.*?(\d+\.?\d*)\s*%', content)
            if match:
                return float(match.group(1))
            # Alternative pattern
            match = re.search(r'All Students.*?(\d+\.?\d*)\s*%', content)
            if match:
                return float(match.group(1))
        
        # Look for 2025 PL 3/4 data specifically (for MCAP)
        # Pattern: "2025" followed by PL 3/4 value
        match = re.search(r'2025.*?PL\s*3/4[^\d]*(\d+\.?\d*)', content)
        
        if match:
            return float(match.group(1))
            
    except Exception as e:
        print(f"      Error extracting: {e}")
    
    return None


def scrape_district_mcap():
    """Scrape district-level MCAP proficiency data for Eastern Shore counties"""
    
    base_url = "https://reportcard.msde.maryland.gov"
    
    # Districts to scrape
    districts = {
        "Caroline": "05",
        "Dorchester": "09",
        "Kent": "14",
        "Queen Anne's": "17",
        "Talbot": "20"
    }
    
    # Data structure
    all_data = {}
    
    for district_name, district_code in districts.items():
        all_data[district_name] = {
            "ELA": None,
            "Math": None,
            "Graduation_Rate": None,
            "metadata": {
                "district_code": district_code,
                "source": "Maryland Report Card",
                "date_scraped": datetime.now().strftime("%Y-%m-%d"),
                "url": f"https://reportcard.msde.maryland.gov/",
                "note": "District MCAP proficiency rates (PL 3/4) for All Students, 2025"
            }
        }
    
    # Define what to scrape: (key, subject_type, display_name)
    # For "All" students across all grades
    scrape_list = [
        ("ELA", "ElaPerformance", "ELA - All Students"),
        ("Math", "MathPerformance", "Math - All Students"),
        ("Graduation_Rate", "GraduationRate", "Graduation Rate"),
    ]
    
    print("Starting district-level MCAP data scraping...")
    print("=" * 80)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for district_name, district_code in districts.items():
            print(f"\n{'='*80}")
            print(f"SCRAPING: {district_name} County (Code: {district_code})")
            print(f"{'='*80}")
            
            for key, subject_type, display_name in scrape_list:
                print(f"\n  Scraping {display_name}...")
                
                try:
                    # Build URL for district data - All students across all grades
                    # ELA: AELAA/A, Math: AMATA/A, Graduation: different URL pattern
                    if subject_type == "GraduationRate":
                        # Graduation rate URL pattern
                        url = f"{base_url}/Graphs/#/GraduationRates/GraduationRate/6/3/1/{district_code}/XXXX/2024"
                    else:
                        if subject_type == "ElaPerformance":
                            grade_code = "AELAA"
                        elif subject_type == "MathPerformance":
                            grade_code = "AMATA"
                        
                        url = f"{base_url}/Graphs/#/Assessments/{subject_type}/{grade_code}/A/6/3/1/{district_code}/XXXX/2025"
                    print(f"    URL: {url}")
                    
                    # Navigate to page
                    page.goto(url, wait_until='networkidle', timeout=15000)
                    
                    # Extract proficiency
                    proficiency = extract_proficiency_from_page(page)
                    
                    if proficiency is not None:
                        all_data[district_name][key] = proficiency
                        print(f"    ✓ Proficiency: {proficiency}%")
                    else:
                        print(f"    ✗ No data found")
                    
                    time.sleep(1)  # Be polite
                    
                except Exception as e:
                    print(f"    ✗ Error: {str(e)[:100]}")
        
        browser.close()
    
    # Save results
    output_file = "district_mcap_data.json"
    with open(output_file, 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print("\n" + "=" * 80)
    print("DISTRICT MCAP SCRAPING COMPLETE")
    print("=" * 80)
    print(f"\n✓ Saved to: {output_file}")
    
    print("\nResults Summary:")
    for district_name, data in all_data.items():
        print(f"\n{district_name}:")
        for key, value in data.items():
            if key != "metadata" and value is not None:
                print(f"  {key}: {value}%")
    
    return all_data


if __name__ == "__main__":
    scrape_district_mcap()
