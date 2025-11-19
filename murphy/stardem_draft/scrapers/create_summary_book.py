#!/usr/bin/env python3
"""
Create a comprehensive summary book organized by county.
Combines census data, school information, test scores, and leadership data.
"""

import json
from collections import defaultdict

# Load all data files
with open('census_education_data.json', 'r') as f:
    census_data = json.load(f)

with open('schools_list.json', 'r') as f:
    schools_list = json.load(f)

with open('district_officials.json', 'r') as f:
    district_officials = json.load(f)

with open('board_meeting_schedules_complete.json', 'r') as f:
    board_meetings = json.load(f)

with open('mcap_highest_grades.json', 'r') as f:
    mcap_highest = json.load(f)

with open('schools_enhanced_data.json', 'r') as f:
    schools_enhanced = json.load(f)

# Organize data by county
counties = ['Talbot', 'Kent', 'Dorchester', 'Caroline', "Queen Anne's"]

summary_book = {}

for county in counties:
    print(f"Processing {county} County...")
    
    county_summary = {
        'county_name': county,
        'census': {},
        'district_leadership': {},
        'board_meetings': {},
        'schools': [],
        'performance_summary': {}
    }
    
    # Census data
    census_key = f"{county} County"
    if census_key in census_data:
        county_summary['census'] = {
            'total_population': census_data[census_key].get('Total Population'),
            'median_household_income': census_data[census_key].get('Median household income'),
            'poverty_rate': census_data[census_key].get('Poverty Rate (%)'),
            'school_age_population_5_17': census_data[census_key].get('School-Age Population (5-17)'),
            'school_enrollment': {
                'total_enrolled': census_data[census_key].get('Enrolled in school'),
                'grades_1_4': census_data[census_key].get('Enrolled in grade 1 to grade 4'),
                'grades_5_8': census_data[census_key].get('Enrolled in grade 5 to grade 8'),
                'grades_9_12': census_data[census_key].get('Enrolled in grade 9 to grade 12'),
            },
            'broadband_access_rate': census_data[census_key].get('Broadband Access Rate (%)'),
            'education_attainment_25_plus': {
                'high_school_graduate': census_data[census_key].get('High school graduate'),
                'bachelors_degree': census_data[census_key].get("Bachelor's degree"),
                'masters_degree': census_data[census_key].get("Master's degree"),
            },
            'demographics': {
                'white_alone': census_data[census_key].get('White alone'),
                'black_or_african_american': census_data[census_key].get('Black or African American alone'),
                'asian_alone': census_data[census_key].get('Asian alone'),
                'hispanic_or_latino': census_data[census_key].get('Hispanic or Latino'),
            }
        }
    
    # District leadership
    if county in district_officials:
        officials = district_officials[county]
        county_summary['district_leadership'] = {
            'superintendent': officials.get('superintendent', {}),
            'board_members': officials.get('board_members', []),
            'total_board_members': len(officials.get('board_members', []))
        }
    
    # Board meetings
    for meeting_data in board_meetings.get('meeting_schedules', []):
        if meeting_data['county'] == county:
            county_summary['board_meetings'] = {
                'regular_schedule': meeting_data['regular_meetings'].get('schedule'),
                'location': meeting_data['regular_meetings'].get('location'),
                'time': meeting_data['regular_meetings'].get('time'),
                'phone': meeting_data['regular_meetings'].get('phone'),
                'upcoming_meetings': meeting_data.get('upcoming_meetings', [])
            }
            break
    
    # Schools data
    county_schools = [s for s in schools_list if s['county'] == county]
    
    for school in county_schools:
        school_name = school['name']
        
        # Get enhanced data
        enhanced = next((s for s in schools_enhanced if s['school_name'] == school_name), None)
        
        # Get MCAP highest grade scores
        mcap_scores = [m for m in mcap_highest if m['school_name'] == school_name]
        
        school_summary = {
            'name': school_name,
            'url': school['url'],
            'star_rating': enhanced.get('star_rating') if enhanced else None,
            'percentile_rank': enhanced.get('percentile_rank') if enhanced else None,
            'highest_grade_mcap': {}
        }
        
        # Organize MCAP scores by subject
        if mcap_scores:
            grade = mcap_scores[0]['grade']
            school_summary['highest_grade_mcap']['grade_tested'] = grade
            school_summary['highest_grade_mcap']['scores'] = {}
            
            for score in mcap_scores:
                subject = score['subject']
                proficiency = score['proficiency_rate']
                school_summary['highest_grade_mcap']['scores'][subject] = proficiency
        
        county_summary['schools'].append(school_summary)
    
    # Performance summary
    county_mcap = [m for m in mcap_highest if m['county'] == county]
    
    if county_mcap:
        # Calculate averages
        ela_scores = [s['proficiency_rate'] for s in county_mcap if s['subject'] == 'ELA' and s['proficiency_rate'] is not None]
        math_scores = [s['proficiency_rate'] for s in county_mcap if s['subject'] == 'Math' and s['proficiency_rate'] is not None]
        science_scores = [s['proficiency_rate'] for s in county_mcap if s['subject'] == 'Science' and s['proficiency_rate'] is not None]
        
        county_summary['performance_summary'] = {
            'total_schools': len(county_schools),
            'schools_with_mcap_data': len(set(s['school_name'] for s in county_mcap)),
            'average_proficiency': {
                'ELA': round(sum(ela_scores) / len(ela_scores), 1) if ela_scores else None,
                'Math': round(sum(math_scores) / len(math_scores), 1) if math_scores else None,
                'Science': round(sum(science_scores) / len(science_scores), 1) if science_scores else None,
            },
            'top_performing_schools': []
        }
        
        # Find top 3 schools by average score
        school_averages = {}
        for school in county_summary['schools']:
            if school['highest_grade_mcap']:
                scores = school['highest_grade_mcap'].get('scores', {})
                valid_scores = [v for v in scores.values() if v is not None]
                if valid_scores:
                    school_averages[school['name']] = sum(valid_scores) / len(valid_scores)
        
        top_schools = sorted(school_averages.items(), key=lambda x: x[1], reverse=True)[:3]
        county_summary['performance_summary']['top_performing_schools'] = [
            {'name': name, 'average_proficiency': round(score, 1)} 
            for name, score in top_schools
        ]
    
    summary_book[county] = county_summary

# Save to JSON
with open('county_summary_book.json', 'w') as f:
    json.dump(summary_book, f, indent=2)

print("\n" + "="*70)
print("COUNTY SUMMARY BOOK CREATED")
print("="*70)

# Print summary stats
for county in counties:
    data = summary_book[county]
    print(f"\n{county} County:")
    print(f"  Population: {data['census'].get('total_population', 'N/A'):,}" if data['census'].get('total_population') else "  Population: N/A")
    print(f"  Schools: {data['performance_summary'].get('total_schools', 0)}")
    print(f"  Board Members: {data['district_leadership'].get('total_board_members', 0)}")
    
    if data['district_leadership'].get('superintendent'):
        supt = data['district_leadership']['superintendent']
        print(f"  Superintendent: {supt.get('name', 'N/A')}")
    
    if data['performance_summary'].get('average_proficiency'):
        avg = data['performance_summary']['average_proficiency']
        print(f"  Avg MCAP: ELA {avg.get('ELA', 'N/A')}%, Math {avg.get('Math', 'N/A')}%, Science {avg.get('Science', 'N/A')}%")

print("\n" + "="*70)
print("Saved to: county_summary_book.json")
print("="*70)
