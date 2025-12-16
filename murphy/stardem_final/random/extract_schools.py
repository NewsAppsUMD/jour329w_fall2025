#!/usr/bin/env python3
"""
Extract school data from the dashboard HTML and output as JSON for rebuilding
"""
import re
import json
from bs4 import BeautifulSoup

with open('dashboard.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

schools = []

# Find all school cards
school_cards = soup.find_all('div', class_='school-card')

for card in school_cards:
    school = {}
    
    # Get county from class
    classes = card.get('class', [])
    county = [c for c in classes if c in ['caroline', 'dorchester', 'kent', 'queen-annes', 'talbot']]
    school['county'] = county[0] if county else 'unknown'
    
    # Get school name and type
    header = card.find('div', class_='school-card-header')
    if header:
        h4 = header.find('h4')
        school['name'] = h4.text.strip() if h4 else 'Unknown'
        school_type = header.find('span', class_='school-type')
        school['type'] = school_type.text.strip() if school_type else 'Unknown'
    
    # Get enrollment data
    details = card.find('div', class_='school-details')
    if details:
        # Total students
        total_stat = details.find('span', class_='detail-label', string='Total Students')
        if total_stat:
            school['enrollment'] = total_stat.find_next('span', class_='detail-value').text.strip()
        
        # Gender
        male_stat = details.find('span', class_='detail-label', string='Male')
        if male_stat:
            school['male_pct'] = male_stat.find_next('span', class_='detail-value').text.strip()
        female_stat = details.find('span', class_='detail-label', string='Female')
        if female_stat:
            school['female_pct'] = female_stat.find_next('span', class_='detail-value').text.strip()
        
        # Race/Ethnicity
        race_data = {}
        for race in ['White', 'African Am.', 'Hispanic', 'Asian', '2+', 'Am. Indian']:
            race_stat = details.find('span', class_='detail-label', string=race)
            if race_stat:
                value = race_stat.find_next('span', class_='detail-value').text.strip()
                race_data[race] = value
        school['race'] = race_data
        
        # Student Groups
        groups = {}
        for group_label in ['Free and Reduced Meals Students', 'Economically Disadvantaged', 
                           'Students with Disabilities', 'Multilingual Learner']:
            group_stat = details.find('span', class_='detail-label', string=group_label)
            if group_stat:
                value = group_stat.find_next('span', class_='detail-value').text.strip()
                groups[group_label] = value
        school['student_groups'] = groups
        
        # MCAP Performance
        mcap = {}
        for subject in ['ELA', 'Math', 'Science', 'Algebra I']:
            subj_stat = details.find('span', class_='detail-label', string=subject)
            if subj_stat:
                value = subj_stat.find_next('span', class_='detail-value').text.strip()
                mcap[subject] = value
        school['mcap'] = mcap
    
    schools.append(school)

# Save to JSON
with open('schools_data.json', 'w') as f:
    json.dump(schools, f, indent=2)

print(f"Extracted {len(schools)} schools")
print(f"Counties: {set(s['county'] for s in schools)}")
print(f"Types: {set(s['type'] for s in schools)}")
