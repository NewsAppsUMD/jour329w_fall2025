#!/usr/bin/env python3
"""
Extract only the highest grade level MCAP scores for each school.
Elementary: Grade 5, Middle: Grade 8, High: Grade 10
"""

import json
import csv

# Load the grade-level MCAP scores
with open('mcap_grade_level_scores.json', 'r') as f:
    all_scores = json.load(f)

# Load school list to get school types
with open('schools_list.json', 'r') as f:
    schools = json.load(f)

# Create a mapping of school names to types
school_types = {}
for school in schools:
    name = school['name']
    # Determine type from name or URL
    if 'Elementary' in name:
        school_types[name] = 'Elementary'
    elif 'Middle' in name:
        school_types[name] = 'Middle'
    elif 'High' in name or 'Academy' in name:
        school_types[name] = 'High'
    else:
        # Default based on common patterns
        school_types[name] = 'Unknown'

# Define highest grades for each type
HIGHEST_GRADES = {
    'Elementary': 5,
    'Middle': 8,
    'High': 10
}

# Filter to only highest grade scores
highest_grade_scores = []

for school_data in all_scores:
    school_name = school_data['school_name']
    county = school_data['county']
    
    # Determine school type
    school_type = school_types.get(school_name, 'Unknown')
    
    # Check if this school type has a highest grade defined
    if school_type in HIGHEST_GRADES:
        highest_grade = HIGHEST_GRADES[school_type]
        
        # Extract scores for the highest grade only
        for score in school_data.get('scores', []):
            if score['grade'] == highest_grade:
                highest_grade_scores.append({
                    'school_name': school_name,
                    'county': county,
                    'grade': score['grade'],
                    'subject': score['subject'],
                    'proficiency_rate': score['proficient_pct']
                })

# Sort by county and school name
highest_grade_scores.sort(key=lambda x: (x['county'], x['school_name'], x['subject']))

# Save to JSON
with open('mcap_highest_grades.json', 'w') as f:
    json.dump(highest_grade_scores, f, indent=2)

# Save to CSV
with open('mcap_highest_grades.csv', 'w', newline='') as f:
    fieldnames = ['school_name', 'county', 'grade', 'subject', 'proficiency_rate']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(highest_grade_scores)

# Print summary
print("="*70)
print("HIGHEST GRADE MCAP SCORES EXTRACTED")
print("="*70)

# Group by school
schools_dict = {}
for score in highest_grade_scores:
    name = score['school_name']
    if name not in schools_dict:
        schools_dict[name] = {
            'county': score['county'],
            'grade': score['grade'],
            'scores': {}
        }
    schools_dict[name]['scores'][score['subject']] = score['proficiency_rate']

print(f"\nTotal schools with highest grade data: {len(schools_dict)}")
print(f"Total score entries: {len(highest_grade_scores)}")

# Count by grade
grade_counts = {}
for score in highest_grade_scores:
    grade = score['grade']
    grade_counts[grade] = grade_counts.get(grade, 0) + 1

print(f"\nScores by grade:")
for grade in sorted(grade_counts.keys()):
    print(f"  Grade {grade}: {grade_counts[grade]} scores")

# Show sample data
print(f"\nSample schools with highest grade scores:")
for school_name, data in sorted(schools_dict.items())[:10]:
    print(f"\n{school_name} ({data['county']})")
    print(f"  Grade {data['grade']}:")
    for subject, rate in sorted(data['scores'].items()):
        print(f"    {subject}: {rate}%")

# Calculate averages by subject
subject_totals = {}
subject_counts = {}

for score in highest_grade_scores:
    subject = score['subject']
    rate = score['proficiency_rate']
    
    if rate is not None:
        subject_totals[subject] = subject_totals.get(subject, 0) + rate
        subject_counts[subject] = subject_counts.get(subject, 0) + 1

print(f"\nAverage proficiency rates (highest grades only):")
for subject in sorted(subject_totals.keys()):
    avg = subject_totals[subject] / subject_counts[subject]
    print(f"  {subject}: {avg:.1f}% (n={subject_counts[subject]})")

print(f"\n{'='*70}")
print("Data saved to:")
print("  - mcap_highest_grades.json")
print("  - mcap_highest_grades.csv")
print("="*70)
