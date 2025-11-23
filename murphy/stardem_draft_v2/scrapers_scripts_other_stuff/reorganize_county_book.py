#!/usr/bin/env python3
"""Reorganize county_summary_book.md to separate county data from school data."""

def extract_sections(content):
    """Extract header, county summaries, school details, and footer."""
    lines = content.split('\n')
    
    # Find main section boundaries
    header_end = 0
    for i, line in enumerate(lines):
        if line.strip() == '## Talbot County':
            header_end = i
            break
    
    # Extract header (everything before first county)
    header = '\n'.join(lines[:header_end])
    
    # Find where Data Sources section starts
    footer_start = len(lines)
    for i, line in enumerate(lines):
        if line.strip() == '## Data Sources':
            footer_start = i
            break
    
    # Extract footer
    footer = '\n'.join(lines[footer_start:])
    
    # Process middle section (counties)
    middle_lines = lines[header_end:footer_start]
    
    counties = []
    current_county = None
    current_county_summary = []
    current_schools = []
    in_schools_section = False
    
    for line in middle_lines:
        if line.startswith('## ') and 'County' in line:
            # Save previous county if exists
            if current_county:
                counties.append({
                    'name': current_county,
                    'summary': '\n'.join(current_county_summary),
                    'schools': '\n'.join(current_schools)
                })
            
            # Start new county
            current_county = line.strip()
            current_county_summary = [line]
            current_schools = []
            in_schools_section = False
            
        elif line.strip() == '### Schools':
            in_schools_section = True
            current_schools.append(line)
            
        elif in_schools_section:
            current_schools.append(line)
            
        else:
            current_county_summary.append(line)
    
    # Save last county
    if current_county:
        counties.append({
            'name': current_county,
            'summary': '\n'.join(current_county_summary),
            'schools': '\n'.join(current_schools)
        })
    
    return header, counties, footer

def reorganize_content(header, counties, footer):
    """Reorganize content with all county data first, then all school data."""
    result = []
    
    # Add header
    result.append(header)
    result.append('')
    
    # Section 1: All County-Level Data
    result.append('# PART I: COUNTY-LEVEL DATA')
    result.append('')
    
    for county in counties:
        result.append(county['summary'])
        result.append('')
        result.append('---')
        result.append('')
    
    # Section 2: All School-Level Data
    result.append('# PART II: SCHOOL-LEVEL DATA')
    result.append('')
    
    for county in counties:
        if county['schools'].strip():
            result.append(county['name'])
            result.append('')
            result.append(county['schools'])
            result.append('')
            result.append('---')
            result.append('')
    
    # Add footer
    result.append(footer)
    
    return '\n'.join(result)

def main():
    # Read original file
    with open('county_summary_book.md', 'r') as f:
        content = f.read()
    
    # Extract sections
    header, counties, footer = extract_sections(content)
    
    # Reorganize
    reorganized = reorganize_content(header, counties, footer)
    
    # Write to new file
    with open('county_summary_book.md', 'w') as f:
        f.write(reorganized)
    
    print(f"✓ Reorganized {len(counties)} counties")
    print("  County data grouped in Part I")
    print("  School data grouped in Part II")

if __name__ == '__main__':
    main()
