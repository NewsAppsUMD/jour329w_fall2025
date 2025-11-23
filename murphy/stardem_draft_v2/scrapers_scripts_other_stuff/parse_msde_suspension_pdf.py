"""
Parse MSDE Suspension PDF files to extract actual student counts
"""

import PyPDF2
import re
import pandas as pd
from pathlib import Path
import json

def extract_pdf_tables(pdf_path):
    """Extract text from PDF and parse suspension data"""
    print(f"Reading: {pdf_path}")
    
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        all_text = ""
        
        print(f"Total pages: {len(pdf_reader.pages)}")
        
        for i, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            all_text += text + "\n"
            
            if i < 3:  # Show first few pages to understand format
                print(f"\n--- Page {i+1} Preview ---")
                print(text[:500])
    
    return all_text

def parse_suspension_data(text):
    """Parse suspension data from extracted text"""
    lines = text.split('\n')
    
    eastern_shore = ['Talbot', 'Kent', 'Dorchester', 'Caroline', "Queen Anne's", 'Queen Anne']
    
    records = []
    current_county = None
    
    for i, line in enumerate(lines):
        # Check if line contains county name
        for county in eastern_shore:
            if county.lower() in line.lower():
                current_county = county if county != "Queen Anne" else "Queen Anne's"
                print(f"\nFound county: {current_county}")
                print(f"Line: {line}")
                
                # Try to extract numbers from this line and nearby lines
                context = ' '.join(lines[max(0, i-2):min(len(lines), i+5)])
                print(f"Context: {context[:200]}")
                break
    
    return records

def main():
    pdf_file = "suspension_data_inschool_2024.pdf"
    
    if not Path(pdf_file).exists():
        print(f"Error: {pdf_file} not found")
        return
    
    text = extract_pdf_tables(pdf_file)
    
    # Save extracted text for inspection
    with open('suspension_pdf_text.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    
    print("\n" + "="*80)
    print("Text extracted and saved to: suspension_pdf_text.txt")
    print("="*80)
    
    # Parse the data
    records = parse_suspension_data(text)

if __name__ == "__main__":
    main()
