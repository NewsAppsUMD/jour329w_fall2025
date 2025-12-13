#!/usr/bin/env python3
"""
Scrape Board of Education meeting minutes for 2025 from multiple county websites
Handles both BoardDocs and Diligent platforms
"""

from playwright.sync_api import sync_playwright
import json
import time
import re
from pathlib import Path
from datetime import datetime
import argparse

# County websites
COUNTIES = {
    'queen_annes': {
        'name': 'Queen Anne\'s County Public Schools',
        'url': 'https://go.boarddocs.com/mabe/qacps/Board.nsf/Public',
        'platform': 'boarddocs'
    },
    'talbot': {
        'name': 'Talbot County Public Schools',
        'url': 'https://tcpsk12.diligent.community/Portal/MeetingTypeList.aspx',
        'platform': 'diligent'
    },
    'dorchester': {
        'name': 'Dorchester County Public Schools',
        'url': 'https://go.boarddocs.com/mabe/dcps/Board.nsf/Public',
        'platform': 'boarddocs'
    },
    'kent': {
        'name': 'Kent County Public Schools',
        'url': 'https://go.boarddocs.com/mabe/kcps/Board.nsf/Public',
        'platform': 'boarddocs'
    },
    'caroline': {
        'name': 'Caroline County Public Schools',
        'url': 'https://go.boarddocs.com/mabe/carps/Board.nsf/Public',
        'platform': 'boarddocs'
    }
}

def scrape_boarddocs(page, county_key, county_info, output_dir, year=2025):
    """Scrape meeting minutes from BoardDocs platform - clicks into each meeting"""
    print(f"\n{'='*60}")
    print(f"Scraping BoardDocs: {county_info['name']}")
    print(f"{'='*60}")
    
    url = county_info['url']
    print(f"URL: {url}")
    
    try:
        page.goto(url, wait_until='networkidle', timeout=60000)
        time.sleep(8)
        
        meetings = []
        
        print("\nSearching for 2025 meetings...")
        
        # Take screenshot for debugging
        screenshot_dir = output_dir / 'screenshots'
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(screenshot_dir / f'{county_key}_main.png'))
        print(f"  Screenshot saved: screenshots/{county_key}_main.png")
        
        # Try different selectors for meeting rows
        # BoardDocs uses different table structures
        selectors_to_try = [
            'table tr',  # Generic table rows
            '.BoardMeetings tr',  # Meeting table
            'tr[class*="meeting"]',  # Meeting rows
            'a[href*="Public.nsf"]'  # Meeting links
        ]
        
        all_elements = []
        for selector in selectors_to_try:
            try:
                elements = page.locator(selector).all()
                if elements:
                    print(f"  Found {len(elements)} elements with selector: {selector}")
                    all_elements.extend(elements)
            except:
                continue
        
        # Get all text on page to find meetings
        page_text = page.locator('body').text_content()
        
        # Find all dates in 2025
        date_pattern = r'(\d{1,2}/\d{1,2}/2025)'
        found_dates = re.findall(date_pattern, page_text)
        print(f"  Found {len(set(found_dates))} unique 2025 dates on page")
        
        # For each date, try to find and click the meeting
        meeting_data = []
        for date_str in set(found_dates):
            try:
                month, day, yr = map(int, date_str.split('/'))
                if month >= 1:  # January or later
                    print(f"\n  Looking for meeting on {date_str}...")
                    
                    # Find clickable elements containing this date
                    date_elements = page.locator(f'a:has-text("{date_str}")').all()
                    
                    if not date_elements:
                        # Try table cells
                        date_elements = page.locator(f'td:has-text("{date_str}")').all()
                    
                    for elem in date_elements:
                        try:
                            elem_text = elem.text_content().strip()
                            if date_str in elem_text:
                                meeting_data.append({
                                    'date': date_str,
                                    'text': elem_text,
                                    'element_type': elem.evaluate('el => el.tagName')
                                })
                                print(f"    Found: {elem_text[:80]}")
                                break
                        except:
                            continue
            except:
                continue
        
        print(f"\nFound {len(meeting_data)} potential meetings from Jan 2025+")
        
        # Now navigate to each meeting
        for i, meeting in enumerate(meeting_data, 1):
            try:
                print(f"\n[{i}/{len(meeting_data)}] Processing {meeting['date']}")
                
                # Go back to main page
                page.goto(url, wait_until='networkidle', timeout=60000)
                time.sleep(4)
                
                # Click on the meeting - try finding by date text
                clicked = False
                
                # Try clicking link with date
                try:
                    link = page.locator(f'a:has-text("{meeting["date"]}")').first
                    if link.is_visible(timeout=2000):
                        link.click()
                        time.sleep(6)
                        clicked = True
                        print(f"  Clicked meeting link")
                except:
                    pass
                
                # If not clicked, try finding row and clicking anywhere in it
                if not clicked:
                    try:
                        row = page.locator(f'tr:has-text("{meeting["date"]}")').first
                        if row.is_visible(timeout=2000):
                            # Try to find a link in the row
                            row_link = row.locator('a').first
                            if row_link:
                                row_link.click()
                                time.sleep(6)
                                clicked = True
                                print(f"  Clicked row link")
                    except:
                        pass
                
                if not clicked:
                    print(f"  ⚠ Could not click meeting")
                    continue
                
                # Now we should be on the meeting page
                current_url = page.url
                print(f"  Meeting URL: {current_url}")
                
                # Look for Minutes documents
                minutes_found = []
                
                # Try multiple ways to find minutes
                minutes_selectors = [
                    'a:has-text("Minutes")',
                    'a:has-text("MINUTES")',
                    'a:has-text("Approved Minutes")',
                    'a[href*="minutes"]',
                    'a[href*=".pdf"]'
                ]
                
                for selector in minutes_selectors:
                    try:
                        links = page.locator(selector).all()
                        for link in links:
                            link_text = link.text_content().strip()
                            if 'minute' in link_text.lower():
                                href = link.get_attribute('href')
                                if href:
                                    full_url = href if href.startswith('http') else f"https://go.boarddocs.com{href}"
                                    minutes_found.append({
                                        'title': link_text,
                                        'url': full_url,
                                        'type': 'pdf' if '.pdf' in href.lower() else 'link'
                                    })
                                    print(f"  ✓ Found: {link_text}")
                    except:
                        continue
                
                if minutes_found:
                    meeting_info = {
                        'date': meeting['date'],
                        'title': meeting['text'],
                        'meeting_url': current_url,
                        'minutes': minutes_found,
                        'platform': 'boarddocs'
                    }
                    meetings.append(meeting_info)
                else:
                    print(f"  ⚠ No minutes found for this meeting")
                    
            except Exception as e:
                print(f"  ✗ Error: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        # Save meetings data
        if meetings:
            county_output_dir = output_dir / county_key
            county_output_dir.mkdir(parents=True, exist_ok=True)
            
            output_file = county_output_dir / f'boe_meetings_{year}.json'
            with open(output_file, 'w') as f:
                json.dump(meetings, f, indent=2)
            
            print(f"\n✓ Saved {len(meetings)} meetings to: {output_file}")
        else:
            print(f"\n⚠ No meetings found for {year}")
        
        return meetings
        
    except Exception as e:
        print(f"❌ Error scraping {county_info['name']}: {e}")
        import traceback
        traceback.print_exc()
        return []

def scrape_diligent(page, county_key, county_info, output_dir, year=2025):
    """Scrape meeting minutes from Diligent platform"""
    print(f"\n{'='*60}")
    print(f"Scraping Diligent: {county_info['name']}")
    print(f"{'='*60}")
    
    url = county_info['url']
    print(f"URL: {url}")
    
    try:
        page.goto(url, wait_until='networkidle', timeout=60000)
        time.sleep(5)
        
        meetings = []
        
        print("\nSearching for 2025 meetings...")
        
        # Diligent uses a different structure - look for meeting type links first
        meeting_type_links = page.locator('a').all()
        
        for mt_link in meeting_type_links:
            try:
                mt_text = mt_link.text_content().strip()
                if 'board' in mt_text.lower() and 'meeting' in mt_text.lower():
                    print(f"\nChecking meeting type: {mt_text}")
                    mt_link.click()
                    time.sleep(3)
                    
                    # Now look for individual meetings
                    meeting_links = page.locator('a').all()
                    
                    for link in meeting_links:
                        try:
                            link_text = link.text_content().strip()
                            href = link.get_attribute('href')
                            
                            # Check for 2025 date patterns
                            if str(year) in link_text:
                                date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', link_text)
                                meeting_date = date_match.group(1) if date_match else link_text
                                
                                meeting_info = {
                                    'date': meeting_date,
                                    'title': link_text,
                                    'url': href if href and href.startswith('http') else f"https://tcpsk12.diligent.community{href}" if href else None,
                                    'platform': 'diligent',
                                    'meeting_type': mt_text
                                }
                                
                                if meeting_info['url'] and meeting_info not in meetings:
                                    meetings.append(meeting_info)
                                    print(f"  Found: {meeting_date} - {link_text[:60]}")
                        except Exception as e:
                            continue
                    
                    # Go back
                    page.go_back()
                    time.sleep(2)
            except Exception as e:
                continue
        
        # Alternative approach - look directly for date patterns
        if not meetings:
            print("\nTrying alternative search...")
            links = page.locator('a').all()
            for link in links:
                try:
                    link_text = link.text_content().strip()
                    href = link.get_attribute('href')
                    
                    if str(year) in link_text:
                        date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', link_text)
                        meeting_date = date_match.group(1) if date_match else link_text
                        
                        meeting_info = {
                            'date': meeting_date,
                            'title': link_text,
                            'url': href if href and href.startswith('http') else f"https://tcpsk12.diligent.community{href}" if href else None,
                            'platform': 'diligent'
                        }
                        
                        if meeting_info['url']:
                            meetings.append(meeting_info)
                            print(f"  Found: {meeting_date} - {link_text[:60]}")
                except Exception as e:
                    continue
        
        # Save meetings data
        if meetings:
            county_output_dir = output_dir / county_key
            county_output_dir.mkdir(parents=True, exist_ok=True)
            
            output_file = county_output_dir / f'boe_meetings_{year}.json'
            with open(output_file, 'w') as f:
                json.dump(meetings, f, indent=2)
            
            print(f"\n✓ Saved {len(meetings)} meetings to: {output_file}")
        else:
            print(f"\n⚠ No meetings found for {year}")
        
        return meetings
        
    except Exception as e:
        print(f"❌ Error scraping {county_info['name']}: {e}")
        import traceback
        traceback.print_exc()
        return []

def main():
    parser = argparse.ArgumentParser(description='Scrape Board of Education meeting minutes for 2025')
    parser.add_argument('--counties', nargs='+', 
                        choices=list(COUNTIES.keys()),
                        default=list(COUNTIES.keys()),
                        help='Counties to scrape')
    parser.add_argument('--year', type=int, default=2025,
                        help='Year to scrape (default: 2025)')
    parser.add_argument('--output-dir', type=str, default='boe_minutes',
                        help='Output directory (default: boe_minutes)')
    parser.add_argument('--headless', action='store_true', default=True,
                        help='Run browser in headless mode')
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_meetings = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        page = browser.new_page()
        
        try:
            for county_key in args.counties:
                county_info = COUNTIES[county_key]
                
                if county_info['platform'] == 'boarddocs':
                    meetings = scrape_boarddocs(page, county_key, county_info, output_dir, args.year)
                elif county_info['platform'] == 'diligent':
                    meetings = scrape_diligent(page, county_key, county_info, output_dir, args.year)
                else:
                    print(f"⚠ Unknown platform: {county_info['platform']}")
                    meetings = []
                
                all_meetings[county_key] = meetings
                
                # Brief pause between counties
                time.sleep(2)
        
        finally:
            browser.close()
    
    # Create summary
    summary_file = output_dir / f'summary_{args.year}.json'
    summary = {
        'year': args.year,
        'scrape_date': datetime.now().isoformat(),
        'counties': {
            county: {
                'name': COUNTIES[county]['name'],
                'platform': COUNTIES[county]['platform'],
                'meetings_found': len(meetings),
                'meetings': meetings
            }
            for county, meetings in all_meetings.items()
        },
        'total_meetings': sum(len(m) for m in all_meetings.values())
    }
    
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*60}")
    print("SCRAPING COMPLETE")
    print(f"{'='*60}")
    print(f"\nTotal meetings found: {summary['total_meetings']}")
    for county, info in summary['counties'].items():
        print(f"  {county}: {info['meetings_found']} meetings")
    print(f"\nSummary saved to: {summary_file}")
    print(f"Individual county files in: {output_dir}")

if __name__ == "__main__":
    main()
