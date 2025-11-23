#!/usr/bin/env python3
"""
Scrape Blueprint funding data from CNS Maryland county pages
"""

import json
import re
from playwright.sync_api import sync_playwright
import pandas as pd

# Eastern Shore counties with their Blueprint page URLs
COUNTIES = {
    'Caroline': 'https://cnsmaryland.org/2023/10/31/behind-the-blueprint-caroline-county',
    'Dorchester': 'https://cnsmaryland.org/2023/10/23/behind-the-blueprint-dorchester-county',
    'Kent': 'https://cnsmaryland.org/2023/11/13/behind-the-blueprint-kent-county',
    'Queen Anne\'s': 'https://cnsmaryland.org/2023/11/14/behind-the-blueprint-queen-annes-county',
    'Talbot': 'https://cnsmaryland.org/2023/11/14/behind-the-blueprint-talbot-county',
}

def extract_funding_data(page_text, county_name):
    """Extract Blueprint funding information from page text."""
    
    data = {
        'county': county_name,
        'per_pupil_increase_percent': None,
        'per_pupil_increase_rank': None,
        'base_year': None,
        'comparison_year': None,
        'strengths': [],
        'needs_improvement': [],
    }
    
    # Look for per-pupil funding increase percentage
    # Patterns: "increased X% between" or "would increase X% between" or "increased by X% between"
    increase_pattern = r'(?:would\s+)?increase[ds]?\s+(?:by\s+)?([\d.]+)%\s+between\s+fiscal\s+(\d{4})\s+and\s+fiscal\s+(\d{4})'
    increase_match = re.search(increase_pattern, page_text, re.IGNORECASE)
    
    if increase_match:
        data['per_pupil_increase_percent'] = float(increase_match.group(1))
        data['base_year'] = int(increase_match.group(2))
        data['comparison_year'] = int(increase_match.group(3))
    
    # Look for ranking among districts
    # Pattern: "the Xth largest increase" or "the Xth smallest increase"
    rank_pattern = r'the\s+(\d+)(?:st|nd|rd|th)[-\s]*(largest|smallest)\s+increase\s+among\s+all\s+(\d+)\s+Maryland'
    rank_match = re.search(rank_pattern, page_text, re.IGNORECASE)
    
    if rank_match:
        data['per_pupil_increase_rank'] = int(rank_match.group(1))
        data['rank_type'] = rank_match.group(2).lower()  # 'largest' or 'smallest'
        data['total_districts'] = int(rank_match.group(3))
    
    # Extract strengths
    strengths_section = re.search(r'Strengths:(.*?)(?:Needs improvement:|$)', page_text, re.DOTALL | re.IGNORECASE)
    if strengths_section:
        strengths_text = strengths_section.group(1)
        # Split by lines and clean
        strengths = [s.strip() for s in strengths_text.split('\n') if s.strip() and not s.strip().startswith('The district')]
        # Filter out very short lines
        data['strengths'] = [s for s in strengths if len(s) > 20][:10]
    
    # Extract needs improvement
    needs_section = re.search(r'Needs improvement:(.*?)(?:-\s*[A-Z]|$)', page_text, re.DOTALL | re.IGNORECASE)
    if needs_section:
        needs_text = needs_section.group(1)
        needs = [n.strip() for n in needs_text.split('\n') if n.strip()]
        data['needs_improvement'] = [n for n in needs if len(n) > 20][:10]
    
    return data

def scrape_county_page(page, county_name, url):
    """Scrape a single county's Blueprint page."""
    
    print(f"\nScraping {county_name} County...")
    print(f"URL: {url}")
    
    try:
        page.goto(url, wait_until='networkidle', timeout=30000)
        
        # Get the main content
        content = page.content()
        
        # Try to get article text specifically
        article_text = ""
        try:
            article = page.locator('article, .entry-content, .post-content, main').first
            article_text = article.inner_text()
        except:
            article_text = page.inner_text()
        
        # Extract data
        data = extract_funding_data(article_text, county_name)
        
        # Try to find specific Blueprint funding tables or sections
        try:
            # Look for tables
            tables = page.locator('table').all()
            if tables:
                print(f"  Found {len(tables)} table(s)")
                data['has_tables'] = True
                data['table_count'] = len(tables)
        except:
            pass
        
        # Look for key statistics in bold or headings
        try:
            headings = page.locator('h2, h3, h4, strong').all()
            key_stats = []
            for heading in headings[:20]:  # First 20 headings
                text = heading.inner_text().strip()
                if any(word in text.lower() for word in ['million', 'funding', 'budget', 'fiscal']):
                    key_stats.append(text)
            data['key_statistics'] = key_stats
        except:
            pass
        
        if data['per_pupil_increase_percent']:
            print(f"  ✓ Per-pupil increase: {data['per_pupil_increase_percent']}%")
        if data['per_pupil_increase_rank']:
            print(f"  ✓ Rank: #{data['per_pupil_increase_rank']}")
        print(f"  ✓ Found {len(data['strengths'])} strengths")
        print(f"  ✓ Found {len(data['needs_improvement'])} areas needing improvement")
        
        return data
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None

def main():
    print("="*80)
    print("BLUEPRINT FUNDING DATA SCRAPER")
    print("="*80)
    
    all_data = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for county, url in COUNTIES.items():
            data = scrape_county_page(page, county, url)
            if data:
                all_data.append(data)
        
        browser.close()
    
    # Save results
    if all_data:
        output_json = 'blueprint_funding_data.json'
        with open(output_json, 'w') as f:
            json.dump(all_data, f, indent=2)
        
        print(f"\n{'='*80}")
        print("RESULTS")
        print(f"{'='*80}")
        print(f"Scraped {len(all_data)} counties")
        print(f"✓ Saved to: {output_json}")
        
        # Summary
        print(f"\n{'='*80}")
        print("SUMMARY")
        print(f"{'='*80}")
        
        for data in all_data:
            print(f"\n{data['county']} County:")
            if data['per_pupil_increase_percent']:
                print(f"  Per-pupil increase: {data['per_pupil_increase_percent']}% (FY{data['base_year']} to FY{data['comparison_year']})")
            if data['per_pupil_increase_rank']:
                print(f"  Ranking: #{data['per_pupil_increase_rank']} of {data.get('total_districts', '24')} districts")
            print(f"  Strengths: {len(data['strengths'])}")
            print(f"  Needs improvement: {len(data['needs_improvement'])}")

if __name__ == '__main__':
    main()
