#!/usr/bin/env python3
"""
Simple direct scraper for BoardDocs BOE minutes
Navigates directly to each county's meeting list and downloads PDFs
"""

from playwright.sync_api import sync_playwright
import json
import time
import re
from pathlib import Path
from datetime import datetime

# Simplified - just get the URLs directly
COUNTIES = {
    'queen_annes': 'https://go.boarddocs.com/mabe/qacps/Board.nsf/Public',
    'dorchester': 'https://go.boarddocs.com/mabe/dcps/Board.nsf/Public',
    'kent': 'https://go.boarddocs.com/mabe/kcps/Board.nsf/Public',
    'caroline': 'https://go.boarddocs.com/mabe/carps/Board.nsf/Public',
    'talbot': 'https://tcpsk12.diligent.community/Portal/MeetingTypeList.aspx'
}

def main():
    output_dir = Path('boe_minutes_simple')
    output_dir.mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser
        page = browser.new_page()
        
        for county, url in COUNTIES.items():
            print(f"\n{'='*60}")
            print(f"{county.upper()}: {url}")
            print(f"{'='*60}")
            print("\nOpening page... (browser will stay open)")
            print("MANUALLY:")
            print("1. Navigate to 2025 meetings")
            print("2. Click into each meeting from January 2025 onwards")  
            print("3. Download the 'Minutes' PDFs")
            print(f"4. Save them to: {output_dir}/{county}/")
            print("\nPress Enter when done with this county...")
            
            page.goto(url)
            
            county_dir = output_dir / county
            county_dir.mkdir(exist_ok=True)
            
            input()  # Wait for user
        
        browser.close()
    
    print("\n✅ Manual collection complete!")
    print(f"PDFs should be in: {output_dir}")

if __name__ == "__main__":
    main()
