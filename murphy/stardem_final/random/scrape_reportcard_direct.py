#!/usr/bin/env python3
"""
Scrape MCAP data directly from school report card pages
"""

from playwright.sync_api import sync_playwright
import json
import time
import re

def scrape_report_card(url, school_name):
    """Scrape MCAP data from a school report card page"""
    
    print(f"\n{'=' * 80}")
    print(f"Scraping: {school_name}")
    print(f"URL: {url}")
    print(f"{'=' * 80}\n")
    
    results = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print("Loading page...")
            page.goto(url, wait_until='networkidle', timeout=30000)
            page.wait_for_timeout(5000)
            
            # Get all text content
            content = page.locator('body').inner_text()
            
            print("\nSearching for MCAP data...")
            
            # Look for assessment data patterns
            # Pattern 1: "Grade 5 ELA   45.0% Proficient"
            # Pattern 2: "ELA Grade 8   48.4%"
            
            # Try to find grade-specific data
            grade_patterns = [
                (r'Grade\s*5\s*ELA[^\d]*(\d+\.?\d*)\s*%', 'Grade 5 ELA'),
                (r'Grade\s*5\s*Math[^\d]*(\d+\.?\d*)\s*%', 'Grade 5 Math'),
                (r'Grade\s*5\s*Science[^\d]*(\d+\.?\d*)\s*%', 'Grade 5 Science'),
                (r'Grade\s*8\s*ELA[^\d]*(\d+\.?\d*)\s*%', 'Grade 8 ELA'),
                (r'Grade\s*8\s*Math[^\d]*(\d+\.?\d*)\s*%', 'Grade 8 Math'),
                (r'Grade\s*8\s*Science[^\d]*(\d+\.?\d*)\s*%', 'Grade 8 Science'),
                (r'Grade\s*10\s*ELA[^\d]*(\d+\.?\d*)\s*%', 'Grade 10 ELA'),
                (r'Algebra\s*I[^\d]*(\d+\.?\d*)\s*%', 'Algebra I'),
                (r'Biology[^\d]*(\d+\.?\d*)\s*%', 'Biology'),
            ]
            
            for pattern, name in grade_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    value = float(match.group(1))
                    results[name] = value
                    print(f"  ✓ Found {name}: {value}%")
            
            # Save a screenshot for debugging
            screenshot_path = f"{school_name.replace(' ', '_').replace('/', '_')}_screenshot.png"
            page.screenshot(path=screenshot_path)
            print(f"\n  Screenshot saved to: {screenshot_path}")
            
            # Also save the page content for manual inspection
            content_path = f"{school_name.replace(' ', '_').replace('/', '_')}_content.txt"
            with open(content_path, 'w') as f:
                f.write(content)
            print(f"  Page content saved to: {content_path}")
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
        finally:
            browser.close()
    
    return results


def main():
    """Main function"""
    
    schools = [
        {
            "name": "St. Michaels Middle/High School",
            "url": "https://reportcard.msde.maryland.gov/Graphs/#/ReportCards/ReportCardSchool/1/MH/1/20/0202/0"
        },
        {
            "name": "South Dorchester School", 
            "url": "https://reportcard.msde.maryland.gov/Graphs/#/ReportCards/ReportCardSchool/1/EM/1/09/0508/0"
        }
    ]
    
    all_results = {}
    
    for school in schools:
        results = scrape_report_card(school["url"], school["name"])
        all_results[school["name"]] = results
        time.sleep(2)
    
    # Save results
    output_file = "reportcard_mcap_data.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n{'=' * 80}")
    print("SCRAPING COMPLETE")
    print(f"{'=' * 80}")
    print(f"\n✓ Results saved to: {output_file}")
    
    print("\n\nSUMMARY:")
    for school_name, data in all_results.items():
        print(f"\n{school_name}:")
        if data:
            for key, value in data.items():
                print(f"  {key}: {value}%")
        else:
            print("  No data found")


if __name__ == "__main__":
    main()
