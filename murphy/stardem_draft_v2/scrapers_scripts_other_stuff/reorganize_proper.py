#!/usr/bin/env python3
"""Reorganize county_summary_book.md with county data followed by school data, add discipline/teacher stats."""

import json

def load_discipline_data():
    """Load suspension data."""
    with open('eastern_shore_suspensions_2023_2024.json', 'r') as f:
        data = json.load(f)
    
    # Organize by county and school
    by_county = {}
    for record in data:
        county = record['county']
        school = record['school_number']
        susp_type = record['suspension_type']
        
        if county not in by_county:
            by_county[county] = {}
        if school not in by_county[county]:
            by_county[county][school] = {'in_school': 0, 'out_of_school': 0}
        
        by_county[county][school][susp_type] = record['total_suspensions']
    
    return by_county

def load_teacher_data():
    """Load teacher data."""
    with open('teacher_data.json', 'r') as f:
        data = json.load(f)
    return {item['county']: item for item in data}

def extract_county_sections(content):
    """Extract individual county sections with their schools."""
    lines = content.split('\n')
    
    # Find header end
    header_end = 0
    for i, line in enumerate(lines):
        if '# PART I: COUNTY-LEVEL DATA' in line:
            header_end = i
            break
    
    header = '\n'.join(lines[:header_end])
    
    # Find footer start
    footer_start = len(lines)
    for i, line in enumerate(lines):
        if line.strip() == '## Data Sources':
            footer_start = i
            break
    
    footer = '\n'.join(lines[footer_start:])
    
    # Extract Part I and Part II sections
    part1_start = header_end
    part2_start = len(lines)
    for i in range(header_end, footer_start):
        if '# PART II: SCHOOL-LEVEL DATA' in lines[i]:
            part2_start = i
            break
    
    part1_lines = lines[part1_start:part2_start]
    part2_lines = lines[part2_start:footer_start]
    
    # Parse counties from Part I
    counties = {}
    current_county = None
    current_lines = []
    
    for line in part1_lines:
        if line.startswith('## ') and 'County' in line:
            if current_county:
                counties[current_county] = {'summary': '\n'.join(current_lines), 'schools': ''}
            current_county = line.strip().replace('## ', '').strip()
            current_lines = [line]
        elif line == '---':
            if current_county:
                counties[current_county] = {'summary': '\n'.join(current_lines), 'schools': ''}
            current_county = None
            current_lines = []
        elif current_county:
            current_lines.append(line)
    
    # Parse schools from Part II
    current_county = None
    current_lines = []
    in_schools = False
    
    for line in part2_lines:
        if line.startswith('## ') and 'County' in line:
            if current_county and in_schools:
                counties[current_county]['schools'] = '\n'.join(current_lines)
            current_county = line.strip().replace('## ', '').strip()
            current_lines = []
            in_schools = False
        elif line.strip() == '### Schools':
            in_schools = True
            current_lines.append(line)
        elif in_schools and line == '---':
            if current_county:
                counties[current_county]['schools'] = '\n'.join(current_lines)
            current_county = None
            current_lines = []
            in_schools = False
        elif in_schools:
            current_lines.append(line)
    
    if current_county and in_schools:
        counties[current_county]['schools'] = '\n'.join(current_lines)
    
    return header, counties, footer

def add_teacher_section(county_name, teacher_data):
    """Generate teacher data section."""
    data = teacher_data.get(county_name)
    if not data:
        return ""
    
    return f"""
### Teacher Workforce

- **Total Teachers:** {data['teachers']:,}
- **Year-over-Year Change:** {data['teacher_change_pct']:+.1f}%
- **New Hires:** {data['new_hires']} ({data['new_hires_pct']:.1f}% of workforce)
- **Student-Teacher Ratio:** {data['student_teacher_ratio']:.1f}:1
"""

def add_discipline_section(county_name, discipline_data):
    """Generate discipline overview section."""
    county_data = discipline_data.get(county_name, {})
    if not county_data:
        return ""
    
    total_in = sum(school.get('in_school', 0) for school in county_data.values())
    total_out = sum(school.get('out_of_school', 0) for school in county_data.values())
    total = total_in + total_out
    
    return f"""
### Discipline Data (2023-2024)

**County-Wide Suspensions:**
- In-School Suspensions: {total_in:,}
- Out-of-School Suspensions: {total_out:,}
- **Total Suspensions:** {total:,}
"""

def add_school_discipline(school_num, county_name, discipline_data):
    """Generate discipline data for a specific school."""
    county_data = discipline_data.get(county_name, {})
    school_data = county_data.get(school_num, {})
    
    if not school_data or (school_data.get('in_school', 0) == 0 and school_data.get('out_of_school', 0) == 0):
        return ""
    
    in_school = school_data.get('in_school', 0)
    out_school = school_data.get('out_of_school', 0)
    
    lines = ["- **Suspensions (2023-2024):**"]
    if in_school > 0:
        lines.append(f"  - In-School: {in_school}")
    if out_school > 0:
        lines.append(f"  - Out-of-School: {out_school}")
    
    return '\n'.join(lines)

def reorganize_content(header, counties, footer, teacher_data, discipline_data):
    """Reorganize with each county's summary + schools together."""
    result = []
    
    result.append(header)
    result.append('')
    
    for county_name, county_info in counties.items():
        # County summary
        summary_lines = county_info['summary'].split('\n')
        
        # Find where to insert teacher and discipline sections
        # Insert after Academic Performance section, before schools
        academic_perf_end = -1
        for i, line in enumerate(summary_lines):
            if line.strip().startswith('**Top Performing Schools:**'):
                # Find the end of this list
                for j in range(i+1, len(summary_lines)):
                    if summary_lines[j].strip() and not summary_lines[j].strip().startswith('-'):
                        academic_perf_end = j
                        break
                if academic_perf_end == -1:
                    academic_perf_end = len(summary_lines)
                break
        
        if academic_perf_end > 0:
            # Insert teacher and discipline sections
            before = summary_lines[:academic_perf_end]
            after = summary_lines[academic_perf_end:]
            
            teacher_section = add_teacher_section(county_name, teacher_data)
            discipline_section = add_discipline_section(county_name, discipline_data)
            
            result.extend(before)
            if teacher_section:
                result.append(teacher_section)
            if discipline_section:
                result.append(discipline_section)
            result.extend(after)
        else:
            result.extend(summary_lines)
        
        result.append('')
        
        # Schools for this county
        if county_info['schools'].strip():
            school_lines = county_info['schools'].split('\n')
            
            # Add discipline data to each school
            i = 0
            while i < len(school_lines):
                line = school_lines[i]
                
                # Check if this is a school header
                if line.startswith('#### ') and '(' in line and ')' in line:
                    # Extract school number
                    school_num = line.split('(')[-1].split(')')[0]
                    
                    # Find end of this school's section (next #### or end)
                    school_end = i + 1
                    for j in range(i + 1, len(school_lines)):
                        if school_lines[j].startswith('####'):
                            school_end = j
                            break
                    else:
                        school_end = len(school_lines)
                    
                    # Add school header and data
                    result.append(line)
                    
                    # Add existing school data
                    for k in range(i + 1, school_end):
                        result.append(school_lines[k])
                    
                    # Add discipline data if available
                    disc_text = add_school_discipline(school_num, county_name, discipline_data)
                    if disc_text:
                        result.append(disc_text)
                        result.append('')
                    
                    i = school_end
                else:
                    result.append(line)
                    i += 1
        
        result.append('')
        result.append('---')
        result.append('')
    
    result.append(footer)
    
    return '\n'.join(result)

def main():
    # Load data
    teacher_data = load_teacher_data()
    discipline_data = load_discipline_data()
    
    # Read current file
    with open('county_summary_book.md', 'r') as f:
        content = f.read()
    
    # Extract sections
    header, counties, footer = extract_county_sections(content)
    
    # Reorganize
    reorganized = reorganize_content(header, counties, footer, teacher_data, discipline_data)
    
    # Write
    with open('county_summary_book.md', 'w') as f:
        f.write(reorganized)
    
    print(f"✓ Reorganized {len(counties)} counties")
    print("  • Each county: summary → schools together")
    print("  • Added teacher workforce data")
    print("  • Added discipline statistics")

if __name__ == '__main__':
    main()
