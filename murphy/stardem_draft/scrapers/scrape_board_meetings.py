#!/usr/bin/env python3
"""
Find board of education meeting schedules for the 5 counties.
Scrape from BoardDocs and district websites.
"""

import json
import asyncio
from playwright.async_api import async_playwright
import re

# District information
DISTRICTS = {
    'Talbot': {
        'name': 'Talbot County Public Schools',
        'boarddocs': 'https://go.boarddocs.com/mabe/tcps/Board.nsf/Public',
        'website': 'https://tcps.k12.md.us',
    },
    'Kent': {
        'name': 'Kent County Public Schools',
        'boarddocs': 'https://go.boarddocs.com/mabe/kcps/Board.nsf/Public',
        'website': 'https://kent.k12.md.us',
    },
    'Dorchester': {
        'name': 'Dorchester County Public Schools',
        'boarddocs': 'https://go.boarddocs.com/mabe/dcps/Board.nsf/Public',
        'website': 'https://dcpsmd.org',
    },
    'Caroline': {
        'name': 'Caroline County Public Schools',
        'boarddocs': 'https://go.boarddocs.com/mabe/ccps/Board.nsf/Public',
        'website': 'https://carolineschools.org',
    },
    'Queen Anne\'s': {
        'name': 'Queen Anne\'s County Public Schools',
        'boarddocs': 'https://go.boarddocs.com/mabe/qacps/Board.nsf/Public',
        'website': 'https://qacps.org',
    }
}

async def scrape_boarddocs_meetings(page, county, boarddocs_url):
    """
    Scrape meeting schedule from BoardDocs.
    """
    print(f"\nScraping BoardDocs for {county}...")
    print(f"URL: {boarddocs_url}")
    
    try:
        await page.goto(boarddocs_url, wait_until='networkidle', timeout=30000)
        await asyncio.sleep(3)
        
        # Get page content
        text_content = await page.locator('body').inner_text()
        
        # Look for meeting schedule information
        meetings_info = {
            'schedule_text': '',
            'upcoming_meetings': [],
            'regular_schedule': ''
        }
        
        # Try to find links or text about meetings
        lines = text_content.split('\n')
        
        # Look for patterns like "2nd Tuesday", "3rd Monday", dates, etc.
        schedule_patterns = []
        date_patterns = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for schedule patterns
            if any(word in line.lower() for word in ['monday', 'tuesday', 'wednesday', 'thursday', 'meeting', 'schedule']):
                if any(ord in line.lower() for ord in ['1st', '2nd', '3rd', '4th', 'first', 'second', 'third', 'fourth']):
                    schedule_patterns.append(line)
            
            # Look for specific dates (format: Month DD, YYYY or MM/DD/YYYY)
            if re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}', line):
                date_patterns.append(line)
            elif re.search(r'\d{1,2}/\d{1,2}/\d{2,4}', line):
                date_patterns.append(line)
        
        meetings_info['schedule_text'] = '\n'.join(schedule_patterns[:5]) if schedule_patterns else 'Not found'
        meetings_info['upcoming_meetings'] = date_patterns[:10]
        
        # Try to click on calendar or meetings link
        try:
            # Look for "Meetings" link
            meetings_link = page.locator('text=/meetings/i').first
            if await meetings_link.is_visible(timeout=2000):
                await meetings_link.click()
                await asyncio.sleep(2)
                
                # Get updated content
                text_content = await page.locator('body').inner_text()
                
                # Save full meetings page content
                meetings_info['meetings_page'] = text_content[:2000]  # First 2000 chars
        except:
            pass
        
        return meetings_info
        
    except Exception as e:
        print(f"  Error scraping BoardDocs: {e}")
        return None

async def scrape_district_website(page, county, website_url):
    """
    Scrape meeting schedule from district website.
    Look for board page, calendar, or meetings section.
    """
    print(f"\nScraping district website for {county}...")
    print(f"URL: {website_url}")
    
    try:
        await page.goto(website_url, wait_until='networkidle', timeout=30000)
        await asyncio.sleep(2)
        
        # Look for board or calendar links
        page_content = await page.content()
        text_content = await page.locator('body').inner_text()
        
        # Try to find board meeting page
        board_links = [
            'board of education',
            'school board',
            'board meetings',
            'calendar',
            'meeting schedule'
        ]
        
        for link_text in board_links:
            try:
                link = page.locator(f'text=/{link_text}/i').first
                if await link.is_visible(timeout=2000):
                    print(f"  Found link: {link_text}")
                    await link.click()
                    await asyncio.sleep(2)
                    
                    # Get content from this page
                    text_content = await page.locator('body').inner_text()
                    
                    # Look for meeting schedule
                    lines = text_content.split('\n')
                    schedule_info = []
                    
                    for line in lines:
                        line = line.strip()
                        if any(word in line.lower() for word in ['meeting', 'schedule', 'calendar', 'monday', 'tuesday']):
                            schedule_info.append(line)
                    
                    return {
                        'source': f'District website - {link_text}',
                        'schedule_text': '\n'.join(schedule_info[:20])
                    }
            except:
                continue
        
        return {
            'source': 'District website homepage',
            'schedule_text': 'Meeting schedule not found on main page'
        }
        
    except Exception as e:
        print(f"  Error scraping district website: {e}")
        return None

async def main():
    results = {}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for county, info in DISTRICTS.items():
            print(f"\n{'='*60}")
            print(f"Processing: {county} County")
            print(f"{'='*60}")
            
            county_data = {
                'county': county,
                'district_name': info['name'],
                'boarddocs_data': None,
                'website_data': None
            }
            
            # Try BoardDocs first
            boarddocs_data = await scrape_boarddocs_meetings(page, county, info['boarddocs'])
            county_data['boarddocs_data'] = boarddocs_data
            
            await asyncio.sleep(2)
            
            # Try district website
            website_data = await scrape_district_website(page, county, info['website'])
            county_data['website_data'] = website_data
            
            results[county] = county_data
            
            await asyncio.sleep(2)
        
        await browser.close()
    
    # Save results
    with open('board_meeting_schedules.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("BOARD MEETING SCHEDULES - SUMMARY")
    print("="*60)
    
    for county, data in results.items():
        print(f"\n{county} County:")
        
        if data['boarddocs_data']:
            bd = data['boarddocs_data']
            if bd.get('schedule_text'):
                print(f"  Schedule: {bd['schedule_text'][:100]}...")
            if bd.get('upcoming_meetings'):
                print(f"  Upcoming meetings found: {len(bd['upcoming_meetings'])}")
                for meeting in bd['upcoming_meetings'][:3]:
                    print(f"    - {meeting}")
        
        if data['website_data']:
            wd = data['website_data']
            print(f"  Website source: {wd.get('source', 'Unknown')}")
    
    print("\nData saved to: board_meeting_schedules.json")

if __name__ == "__main__":
    asyncio.run(main())
