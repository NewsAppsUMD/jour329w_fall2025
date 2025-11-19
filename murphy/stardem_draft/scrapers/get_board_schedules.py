#!/usr/bin/env python3
"""
Get full 2025 meeting schedule from BoardDocs by clicking on year links.
"""

import json
import asyncio
from playwright.async_api import async_playwright
from collections import Counter

COUNTIES = {
    'Talbot': 'https://go.boarddocs.com/mabe/tcps/Board.nsf/Public',
    'Kent': 'https://go.boarddocs.com/mabe/kcps/Board.nsf/Public',
    'Dorchester': 'https://go.boarddocs.com/mabe/dcps/Board.nsf/Public',
    'Caroline': 'https://go.boarddocs.com/mabe/ccps/Board.nsf/Public',
    'Queen Anne\'s': 'https://go.boarddocs.com/mabe/qacps/Board.nsf/Public',
}

MONTH_ORDER = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def parse_meetings(text):
    """Parse meeting dates from BoardDocs text."""
    import re
    meetings = []
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        # Match "Nov 17, 2025 (Mon)"
        match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),\s+2025\s+\((\w+)\)', line)
        if match:
            month = match.group(1)
            day = int(match.group(2))
            weekday = match.group(3)
            
            # Get description from next line
            desc = lines[i+1].strip() if i+1 < len(lines) else ''
            
            meetings.append({
                'month': month,
                'day': day,
                'weekday': weekday,
                'description': desc,
                'full_date': f"{month} {day}, 2025 ({weekday})"
            })
    
    return meetings

def analyze_pattern(meetings):
    """Determine meeting schedule pattern."""
    if not meetings:
        return "No meetings found"
    
    weekdays = [m['weekday'] for m in meetings]
    weekday_counts = Counter(weekdays)
    
    # Find most common weekday
    if not weekday_counts:
        return "Unknown schedule"
    
    most_common_weekday, count = weekday_counts.most_common(1)[0]
    
    # Determine which week of month
    week_positions = []
    for m in meetings:
        day = m['day']
        if 1 <= day <= 7:
            week_positions.append('1st')
        elif 8 <= day <= 14:
            week_positions.append('2nd')
        elif 15 <= day <= 21:
            week_positions.append('3rd')
        else:
            week_positions.append('4th')
    
    week_counts = Counter(week_positions)
    most_common_week = week_counts.most_common(1)[0][0] if week_counts else None
    
    # Build pattern description
    if most_common_week:
        pattern = f"{most_common_week} {most_common_weekday} of each month"
    else:
        pattern = f"{most_common_weekday}s"
    
    return pattern

async def scrape_county(page, county, url):
    """Scrape meeting schedule for one county."""
    print(f"\n{'='*60}")
    print(f"{county} County")
    print(f"{'='*60}")
    
    try:
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await asyncio.sleep(2)
        
        # Try clicking "MEETINGS" tab
        try:
            meetings_tab = page.locator('a:has-text("MEETINGS")').first
            await meetings_tab.click(timeout=5000)
            await asyncio.sleep(2)
        except:
            pass
        
        # Try clicking on "2025" link to see all meetings for the year
        try:
            year_2025 = page.locator('a:has-text("2025")').first
            await year_2025.click(timeout=5000)
            await asyncio.sleep(2)
        except:
            pass
        
        # Get page content
        text = await page.locator('body').inner_text()
        
        # Parse meetings
        meetings = parse_meetings(text)
        
        # Sort meetings chronologically
        meetings_sorted = sorted(meetings, key=lambda x: (MONTH_ORDER.index(x['month']), x['day']))
        
        # Print findings
        print(f"Found {len(meetings_sorted)} meetings")
        for m in meetings_sorted:
            print(f"  {m['full_date']}: {m['description'][:60]}")
        
        # Analyze pattern
        pattern = analyze_pattern(meetings_sorted)
        print(f"\nPattern: {pattern}")
        
        return {
            'county': county,
            'url': url,
            'meetings': meetings_sorted,
            'pattern': pattern,
            'total_meetings': len(meetings_sorted)
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {
            'county': county,
            'url': url,
            'error': str(e)
        }

async def main():
    results = {}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for county, url in COUNTIES.items():
            data = await scrape_county(page, county, url)
            results[county] = data
            await asyncio.sleep(1)
        
        await browser.close()
    
    # Save results
    with open('board_meeting_schedules_final.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print final summary
    print("\n" + "="*70)
    print("BOARD OF EDUCATION MEETING SCHEDULES - SUMMARY")
    print("="*70)
    
    for county, data in results.items():
        print(f"\n{county} County:")
        if 'error' in data:
            print(f"  Error: {data['error']}")
        else:
            print(f"  Regular Schedule: {data['pattern']}")
            print(f"  Total 2025 Meetings: {data['total_meetings']}")
            
            # Show next 3 upcoming meetings
            upcoming = [m for m in data.get('meetings', []) if m['month'] in ['Nov', 'Dec']][:3]
            if upcoming:
                print(f"  Upcoming meetings:")
                for m in upcoming:
                    print(f"    - {m['full_date']}: {m['description'][:50]}")
    
    print("\n" + "="*70)
    print("Data saved to: board_meeting_schedules_final.json")

if __name__ == "__main__":
    asyncio.run(main())
