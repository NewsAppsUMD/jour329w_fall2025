#!/usr/bin/env python3
"""
Get detailed board meeting schedules by analyzing BoardDocs calendars.
Look at all meetings for 2025 to determine regular schedule pattern.
"""

import json
import asyncio
from playwright.async_api import async_playwright
from collections import Counter
import re

BOARDDOCS_URLS = {
    'Talbot': 'https://go.boarddocs.com/mabe/tcps/Board.nsf/Public',
    'Kent': 'https://go.boarddocs.com/mabe/kcps/Board.nsf/Public',
    'Dorchester': 'https://go.boarddocs.com/mabe/dcps/Board.nsf/Public',
    'Caroline': 'https://go.boarddocs.com/mabe/ccps/Board.nsf/Public',
    'Queen Anne\'s': 'https://go.boarddocs.com/mabe/qacps/Board.nsf/Public',
}

async def get_all_2025_meetings(page, county, url):
    """
    Get all meetings scheduled for 2025 to determine pattern.
    """
    print(f"\n{'='*60}")
    print(f"Analyzing {county} County Board Meetings")
    print(f"{'='*60}")
    
    try:
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await asyncio.sleep(3)
        
        # Click on "Meetings" tab if available
        try:
            meetings_tab = page.locator('text="MEETINGS"').first
            await meetings_tab.click()
            await asyncio.sleep(2)
        except:
            pass
        
        # Get all text content
        text = await page.locator('body').inner_text()
        
        # Extract all dates and times
        lines = text.split('\n')
        
        meetings = []
        current_date = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Look for date pattern: "Nov 20, 2025 (Thu)"
            date_match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),\s+2025\s+\((\w+)\)', line)
            if date_match:
                month = date_match.group(1)
                day = date_match.group(2)
                weekday = date_match.group(3)
                current_date = f"{month} {day}, 2025 ({weekday})"
                
                # Look at next few lines for time/description
                description = []
                for j in range(i+1, min(i+3, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and not re.search(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', next_line):
                        description.append(next_line)
                
                meetings.append({
                    'date': current_date,
                    'month': month,
                    'day': int(day),
                    'weekday': weekday,
                    'description': ' '.join(description)
                })
        
        # Analyze pattern
        if meetings:
            print(f"\nFound {len(meetings)} meetings in 2025:")
            for meeting in sorted(meetings, key=lambda x: (
                ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'].index(x['month']),
                x['day']
            )):
                print(f"  {meeting['date']}: {meeting['description']}")
            
            # Determine pattern
            weekday_counts = Counter([m['weekday'] for m in meetings])
            most_common_day = weekday_counts.most_common(1)[0] if weekday_counts else None
            
            # Calculate which week of month (1st, 2nd, 3rd, 4th)
            week_positions = []
            for m in meetings:
                day = m['day']
                if 1 <= day <= 7:
                    week_positions.append('1st')
                elif 8 <= day <= 14:
                    week_positions.append('2nd')
                elif 15 <= day <= 21:
                    week_positions.append('3rd')
                elif 22 <= day <= 28:
                    week_positions.append('4th')
            
            week_counts = Counter(week_positions)
            most_common_week = week_counts.most_common(1)[0] if week_counts else None
            
            pattern = "No clear pattern"
            if most_common_day and most_common_week:
                pattern = f"{most_common_week[0]} {most_common_day[0]} of the month"
            
            return {
                'meetings': meetings,
                'pattern': pattern,
                'weekday_counts': dict(weekday_counts),
                'week_counts': dict(week_counts),
                'total_meetings': len(meetings)
            }
        else:
            print("  No meetings found")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

async def main():
    results = {}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for county, url in BOARDDOCS_URLS.items():
            data = await get_all_2025_meetings(page, county, url)
            results[county] = data
            await asyncio.sleep(2)
        
        await browser.close()
    
    # Save results
    with open('board_meeting_patterns.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "="*70)
    print("BOARD MEETING SCHEDULE SUMMARY")
    print("="*70)
    
    for county, data in results.items():
        print(f"\n{county} County:")
        if data:
            print(f"  Regular Schedule: {data['pattern']}")
            print(f"  Total Meetings (2025): {data['total_meetings']}")
            if data['meetings']:
                next_meetings = [m for m in data['meetings'] if m['month'] in ['Nov', 'Dec']][:3]
                if next_meetings:
                    print(f"  Upcoming meetings:")
                    for m in next_meetings:
                        print(f"    - {m['date']}: {m['description'][:50]}")
        else:
            print("  No meeting data found")
    
    print("\nData saved to: board_meeting_patterns.json")

if __name__ == "__main__":
    asyncio.run(main())
