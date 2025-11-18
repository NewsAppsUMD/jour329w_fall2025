"""
Enhanced Maryland School Data Parser

This script demonstrates how to extract more detailed information from
the Maryland School Report Card pages that were already scraped.

Run this AFTER running get_school_data_playwright.py
"""

import json
import re
from playwright.sync_api import sync_playwright
import pandas as pd
import time


def extract_detailed_school_data(page, school_url, school_name):
    """
    Extract detailed information from a school's report card page
    """
    print(f"Extracting detailed data for: {school_name}")
    
    page.goto(school_url, wait_until='networkidle')
    page.wait_for_timeout(2000)
    
    data = {
        'school_name': school_name,
        'url': school_url
    }
    
    # Get all text content
    full_text = page.locator('body').inner_text()
    
    # Extract star rating
    star_match = re.search(r'(\d+)\s+OUT OF\s+(\d+)\s+STARS', full_text)
    if star_match:
        data['stars'] = f"{star_match.group(1)}/{star_match.group(2)}"
        data['star_rating'] = int(star_match.group(1))
    
    # Extract percentile rank
    percentile_match = re.search(r'Percentile Rank:\s+(\d+)', full_text)
    if percentile_match:
        data['percentile_rank'] = int(percentile_match.group(1))
    
    # Extract enrollment information
    enrollment_match = re.search(r'Total Enrollment:\s+([\d,]+)', full_text)
    if enrollment_match:
        data['total_enrollment'] = enrollment_match.group(1).replace(',', '')
    
    # Look for demographic data
    demographics = {}
    
    # Race/ethnicity patterns
    race_patterns = {
        'african_american': r'African American.*?([\d.]+)%',
        'asian': r'Asian.*?([\d.]+)%',
        'hispanic': r'Hispanic.*?([\d.]+)%',
        'white': r'White.*?([\d.]+)%',
        'two_or_more': r'Two or More Races.*?([\d.]+)%'
    }
    
    for key, pattern in race_patterns.items():
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            demographics[key] = match.group(1)
    
    # Economic disadvantage
    econ_match = re.search(r'Economically Disadvantaged.*?([\d.]+)%', full_text, re.IGNORECASE)
    if econ_match:
        demographics['economically_disadvantaged'] = econ_match.group(1)
    
    # Special education
    sped_match = re.search(r'Special Education.*?([\d.]+)%', full_text, re.IGNORECASE)
    if sped_match:
        demographics['special_education'] = sped_match.group(1)
    
    # English learners
    ell_match = re.search(r'English Learner.*?([\d.]+)%', full_text, re.IGNORECASE)
    if ell_match:
        demographics['english_learners'] = ell_match.group(1)
    
    if demographics:
        data['demographics'] = demographics
    
    # Try to click on tabs to get more data
    try:
        # Look for Demographics tab
        demo_tab = page.locator('text="Demographics"').first
        if demo_tab:
            demo_tab.click()
            page.wait_for_timeout(1000)
            demo_text = page.locator('body').inner_text()
            data['demographics_full'] = demo_text[:500]
    except:
        pass
    
    try:
        # Look for MCAP (test scores) tab
        mcap_tab = page.locator('text="MCAP"').first
        if mcap_tab:
            mcap_tab.click()
            page.wait_for_timeout(1000)
            mcap_text = page.locator('body').inner_text()
            data['mcap_data'] = mcap_text[:500]
    except:
        pass
    
    return data


def enhance_school_data(limit=None):
    """
    Re-scrape schools with enhanced data extraction
    
    Args:
        limit: Number of schools to process (None for all)
    """
    # Load the basic school list
    with open('schools_list.json', 'r') as f:
        schools = json.load(f)
    
    if limit:
        schools = schools[:limit]
        print(f"Processing first {limit} schools...")
    else:
        print(f"Processing all {len(schools)} schools...")
    
    enhanced_data = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for i, school in enumerate(schools, 1):
            print(f"\n[{i}/{len(schools)}] ", end="")
            try:
                data = extract_detailed_school_data(
                    page, 
                    school['url'], 
                    school['name']
                )
                data['county'] = school['county']
                enhanced_data.append(data)
                time.sleep(0.5)  # Be polite
            except Exception as e:
                print(f"  ⚠️  Error: {e}")
                enhanced_data.append({
                    'school_name': school['name'],
                    'county': school['county'],
                    'url': school['url'],
                    'error': str(e)
                })
        
        browser.close()
    
    # Save enhanced data
    output_file = 'schools_enhanced_data.json'
    with open(output_file, 'w') as f:
        json.dump(enhanced_data, f, indent=2)
    print(f"\n\n✓ Saved enhanced data to: {output_file}")
    
    # Create a summary dataframe
    try:
        df = pd.DataFrame(enhanced_data)
        csv_file = 'schools_enhanced_data.csv'
        df.to_csv(csv_file, index=False)
        print(f"✓ Saved CSV to: {csv_file}")
        
        # Print summary statistics
        print(f"\n{'='*70}")
        print("ENHANCED DATA SUMMARY")
        print(f"{'='*70}")
        if 'star_rating' in df.columns:
            print(f"\nStar Ratings:")
            print(df.groupby('star_rating').size().sort_index(ascending=False))
        
        if 'percentile_rank' in df.columns:
            print(f"\nPercentile Rank Statistics:")
            print(f"  Mean: {df['percentile_rank'].mean():.1f}")
            print(f"  Median: {df['percentile_rank'].median():.1f}")
            print(f"  Min: {df['percentile_rank'].min()}")
            print(f"  Max: {df['percentile_rank'].max()}")
        
        if 'total_enrollment' in df.columns:
            df['total_enrollment'] = pd.to_numeric(df['total_enrollment'], errors='coerce')
            print(f"\nEnrollment Statistics:")
            print(f"  Total: {df['total_enrollment'].sum():.0f}")
            print(f"  Mean: {df['total_enrollment'].mean():.0f}")
            print(f"  Median: {df['total_enrollment'].median():.0f}")
    except Exception as e:
        print(f"Could not create summary: {e}")
    
    return enhanced_data


if __name__ == "__main__":
    import sys
    
    # Allow limiting number of schools for testing
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    
    if limit:
        print(f"Running in TEST MODE - processing {limit} schools only")
        print("To process all schools, run: python extract_detailed_data.py")
    
    enhance_school_data(limit=limit)
