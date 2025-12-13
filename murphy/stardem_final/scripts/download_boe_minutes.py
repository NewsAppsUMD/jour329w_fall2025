#!/usr/bin/env python3
"""
Download actual Board of Education meeting minutes content (PDFs and text)
Reads the meeting links from boe_meetings_2025.json and downloads the minutes
"""

from playwright.sync_api import sync_playwright
import json
import time
import re
from pathlib import Path
from datetime import datetime
import argparse

def parse_date(date_str):
    """Parse date string to datetime object"""
    # Try common formats
    formats = [
        '%m/%d/%Y',
        '%m/%d/%y',
        '%B %d, %Y',
        '%b %d, %Y',
        '%Y-%m-%d'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except:
            continue
    
    # Try to extract date with regex
    match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', date_str)
    if match:
        return datetime(int(match.group(3)), int(match.group(1)), int(match.group(2)))
    
    return None

def is_2025_or_later(date_str):
    """Check if date is January 2025 or later"""
    parsed = parse_date(date_str)
    if parsed:
        return parsed >= datetime(2025, 1, 1)
    return False

def download_boarddocs_minutes(page, meeting, county_key, output_dir):
    """Download minutes from a BoardDocs meeting page"""
    print(f"\n  Opening: {meeting['title']}")
    
    try:
        page.goto(meeting['url'], wait_until='networkidle', timeout=60000)
        time.sleep(5)
        
        # Look for minutes document
        # BoardDocs typically has "Minutes" link or PDF
        minutes_found = False
        minutes_content = {
            'date': meeting['date'],
            'title': meeting['title'],
            'url': meeting['url'],
            'documents': []
        }
        
        # Look for links containing "minutes"
        links = page.locator('a').all()
        for link in links:
            try:
                link_text = link.text_content().strip().lower()
                href = link.get_attribute('href')
                
                if 'minute' in link_text:
                    print(f"    Found minutes link: {link_text}")
                    
                    doc_info = {
                        'title': link.text_content().strip(),
                        'url': href if href and href.startswith('http') else meeting['url'] + href if href else None
                    }
                    
                    # If it's a PDF, download it
                    if href and '.pdf' in href.lower():
                        doc_info['type'] = 'pdf'
                        pdf_url = href if href.startswith('http') else f"https://go.boarddocs.com{href}"
                        
                        # Create download directory
                        download_dir = output_dir / county_key / 'pdfs'
                        download_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Clean filename
                        safe_date = meeting['date'].replace('/', '-')
                        pdf_filename = f"minutes_{safe_date}.pdf"
                        pdf_path = download_dir / pdf_filename
                        
                        doc_info['local_path'] = str(pdf_path)
                        doc_info['download_url'] = pdf_url
                        
                        print(f"    PDF: {pdf_url}")
                        print(f"    Save to: {pdf_path}")
                    else:
                        doc_info['type'] = 'link'
                    
                    minutes_content['documents'].append(doc_info)
                    minutes_found = True
                    
            except Exception as e:
                continue
        
        # Also try to extract text content from the page itself
        try:
            # Look for minutes text in the page
            body_text = page.locator('body').text_content()
            if 'minutes' in body_text.lower():
                # Try to find a content area
                content_divs = page.locator('div.content, div.minutes, div.details, .BoardDoc').all()
                for div in content_divs:
                    text = div.text_content().strip()
                    if len(text) > 200 and 'minute' in text.lower():
                        minutes_content['text_content'] = text
                        print(f"    Extracted text content: {len(text)} chars")
                        minutes_found = True
                        break
        except Exception as e:
            pass
        
        return minutes_content if minutes_found else None
        
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return None

def download_diligent_minutes(page, meeting, county_key, output_dir):
    """Download minutes from a Diligent meeting page"""
    print(f"\n  Opening: {meeting['title']}")
    
    try:
        page.goto(meeting['url'], wait_until='networkidle', timeout=60000)
        time.sleep(5)
        
        minutes_found = False
        minutes_content = {
            'date': meeting['date'],
            'title': meeting['title'],
            'url': meeting['url'],
            'documents': []
        }
        
        # Look for minutes documents in Diligent interface
        links = page.locator('a').all()
        for link in links:
            try:
                link_text = link.text_content().strip().lower()
                href = link.get_attribute('href')
                
                if 'minute' in link_text or 'approved' in link_text:
                    print(f"    Found: {link_text}")
                    
                    doc_info = {
                        'title': link.text_content().strip(),
                        'url': href if href and href.startswith('http') else f"https://tcpsk12.diligent.community{href}" if href else None
                    }
                    
                    if href and '.pdf' in href.lower():
                        doc_info['type'] = 'pdf'
                        pdf_url = doc_info['url']
                        
                        download_dir = output_dir / county_key / 'pdfs'
                        download_dir.mkdir(parents=True, exist_ok=True)
                        
                        safe_date = meeting['date'].replace('/', '-')
                        pdf_filename = f"minutes_{safe_date}.pdf"
                        pdf_path = download_dir / pdf_filename
                        
                        doc_info['local_path'] = str(pdf_path)
                        doc_info['download_url'] = pdf_url
                        
                        print(f"    PDF: {pdf_url}")
                    else:
                        doc_info['type'] = 'link'
                    
                    minutes_content['documents'].append(doc_info)
                    minutes_found = True
                    
            except Exception as e:
                continue
        
        return minutes_content if minutes_found else None
        
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return None

def download_pdfs(page, minutes_with_pdfs, output_dir):
    """Actually download the PDF files"""
    print(f"\n{'='*60}")
    print("DOWNLOADING PDFs")
    print(f"{'='*60}")
    
    downloaded = 0
    failed = 0
    
    for county_data in minutes_with_pdfs.values():
        for meeting in county_data:
            for doc in meeting.get('documents', []):
                if doc.get('type') == 'pdf' and doc.get('download_url'):
                    try:
                        print(f"\nDownloading: {doc['download_url']}")
                        
                        # Navigate and download
                        with page.expect_download() as download_info:
                            page.goto(doc['download_url'])
                            time.sleep(2)
                        
                        download = download_info.value
                        download.save_as(doc['local_path'])
                        
                        print(f"  ✓ Saved: {doc['local_path']}")
                        downloaded += 1
                        
                    except Exception as e:
                        print(f"  ✗ Failed: {e}")
                        failed += 1
                        # Try alternative download method
                        try:
                            import requests
                            response = requests.get(doc['download_url'], timeout=30)
                            if response.status_code == 200:
                                Path(doc['local_path']).write_bytes(response.content)
                                print(f"  ✓ Downloaded via requests: {doc['local_path']}")
                                downloaded += 1
                                failed -= 1
                        except Exception as e2:
                            print(f"  ✗ Requests also failed: {e2}")
    
    print(f"\n{'='*60}")
    print(f"Downloaded: {downloaded} PDFs")
    print(f"Failed: {failed} PDFs")
    print(f"{'='*60}")

def main():
    parser = argparse.ArgumentParser(description='Download BOE meeting minutes content')
    parser.add_argument('--input-dir', type=str, default='boe_minutes',
                        help='Directory with boe_meetings_2025.json files')
    parser.add_argument('--output-dir', type=str, default='boe_minutes',
                        help='Output directory for downloaded content')
    parser.add_argument('--year', type=int, default=2025,
                        help='Year (default: 2025)')
    parser.add_argument('--download-pdfs', action='store_true',
                        help='Actually download PDF files (slower)')
    
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    # County platform mapping
    platforms = {
        'queen_annes': 'boarddocs',
        'talbot': 'diligent',
        'dorchester': 'boarddocs',
        'kent': 'boarddocs',
        'caroline': 'boarddocs'
    }
    
    all_minutes = {}
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            for county in ['queen_annes', 'talbot', 'dorchester', 'kent', 'caroline']:
                print(f"\n{'='*60}")
                print(f"COUNTY: {county.upper()}")
                print(f"{'='*60}")
                
                # Load meeting links
                meetings_file = input_dir / county / f'boe_meetings_{args.year}.json'
                
                if not meetings_file.exists():
                    print(f"⚠ No meetings file found: {meetings_file}")
                    continue
                
                with open(meetings_file) as f:
                    all_meetings = json.load(f)
                
                # Filter to only January 2025 or later
                meetings = [m for m in all_meetings if is_2025_or_later(m.get('date', ''))]
                
                print(f"Found {len(all_meetings)} total meetings")
                print(f"Filtered to {len(meetings)} meetings from Jan 2025 onwards")
                
                county_minutes = []
                platform = platforms[county]
                
                for i, meeting in enumerate(meetings, 1):
                    print(f"\n[{i}/{len(meetings)}] {meeting['date']}")
                    
                    if platform == 'boarddocs':
                        minutes = download_boarddocs_minutes(page, meeting, county, output_dir)
                    else:
                        minutes = download_diligent_minutes(page, meeting, county, output_dir)
                    
                    if minutes:
                        county_minutes.append(minutes)
                        print(f"  ✓ Found minutes content")
                    else:
                        print(f"  ⚠ No minutes found")
                    
                    time.sleep(2)  # Be nice to servers
                
                all_minutes[county] = county_minutes
                
                # Save county minutes metadata
                county_output_dir = output_dir / county
                county_output_dir.mkdir(parents=True, exist_ok=True)
                
                metadata_file = county_output_dir / f'minutes_metadata_{args.year}.json'
                with open(metadata_file, 'w') as f:
                    json.dump(county_minutes, f, indent=2)
                
                print(f"\n✓ Saved metadata: {metadata_file}")
                print(f"  Total minutes found: {len(county_minutes)}")
            
            # Download PDFs if requested
            if args.download_pdfs:
                download_pdfs(page, all_minutes, output_dir)
            
        finally:
            browser.close()
    
    # Create summary
    summary = {
        'year': args.year,
        'download_date': datetime.now().isoformat(),
        'counties': {}
    }
    
    for county, minutes in all_minutes.items():
        pdf_count = sum(1 for m in minutes for d in m.get('documents', []) if d.get('type') == 'pdf')
        summary['counties'][county] = {
            'meetings_with_minutes': len(minutes),
            'pdf_documents': pdf_count,
            'has_text_content': sum(1 for m in minutes if 'text_content' in m)
        }
    
    summary_file = output_dir / f'minutes_summary_{args.year}.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*60}")
    print("COMPLETE")
    print(f"{'='*60}")
    print(f"\nSummary saved to: {summary_file}")
    print(f"\nResults by county:")
    for county, stats in summary['counties'].items():
        print(f"  {county}:")
        print(f"    Meetings with minutes: {stats['meetings_with_minutes']}")
        print(f"    PDF documents: {stats['pdf_documents']}")
    
    if not args.download_pdfs:
        print(f"\n💡 To download PDFs, run with --download-pdfs flag")

if __name__ == "__main__":
    main()
