#!/usr/bin/env python3
"""
Create a readable markdown summary book from the JSON data.
"""

import json

with open('county_summary_book.json', 'r') as f:
    data = json.load(f)

markdown = """# Maryland Eastern Shore Education Data Summary
**Five County Analysis: Talbot, Kent, Dorchester, Caroline, and Queen Anne's**

*Data collected: November 2025*

---

"""

counties = ['Talbot', 'Kent', 'Dorchester', 'Caroline', "Queen Anne's"]

for county in counties:
    county_data = data[county]
    
    markdown += f"## {county} County\n\n"
    
    # Census Overview
    census = county_data['census']
    markdown += "### Demographics & Economics\n\n"
    if census.get('total_population'):
        markdown += f"- **Total Population:** {census['total_population']:,}\n"
    if census.get('median_household_income'):
        markdown += f"- **Median Household Income:** ${census['median_household_income']:,}\n"
    if census.get('poverty_rate'):
        markdown += f"- **Poverty Rate:** {census['poverty_rate']}%\n"
    if census.get('school_age_population_5_17'):
        markdown += f"- **School-Age Population (5-17):** {census['school_age_population_5_17']:,}\n"
    if census.get('broadband_access_rate'):
        markdown += f"- **Broadband Access:** {census['broadband_access_rate']}%\n"
    
    # School enrollment
    enrollment = census.get('school_enrollment', {})
    if enrollment.get('total_enrolled'):
        markdown += f"\n**School Enrollment:**\n"
        markdown += f"- Total enrolled: {enrollment['total_enrolled']:,}\n"
        if enrollment.get('grades_1_4'):
            markdown += f"- Grades 1-4: {enrollment['grades_1_4']:,}\n"
        if enrollment.get('grades_5_8'):
            markdown += f"- Grades 5-8: {enrollment['grades_5_8']:,}\n"
        if enrollment.get('grades_9_12'):
            markdown += f"- Grades 9-12: {enrollment['grades_9_12']:,}\n"
    
    # District Leadership
    markdown += "\n### District Leadership\n\n"
    leadership = county_data['district_leadership']
    
    if leadership.get('superintendent'):
        supt = leadership['superintendent']
        markdown += f"**Superintendent:** {supt.get('name', 'N/A')}\n"
        if supt.get('email'):
            markdown += f"- Email: {supt['email']}\n"
        if supt.get('title'):
            markdown += f"- Title: {supt['title']}\n"
    
    if leadership.get('board_members'):
        markdown += f"\n**Board of Education:** {leadership['total_board_members']} members\n\n"
        for member in leadership['board_members']:
            name = member.get('name', 'N/A')
            markdown += f"- **{name}**"
            if member.get('district'):
                markdown += f" (District {member['district']})"
            if member.get('position'):
                markdown += f" - {member['position']}"
            markdown += "\n"
            if member.get('term_end'):
                markdown += f"  - Term ends: {member['term_end']}\n"
    
    # Board Meetings
    meetings = county_data['board_meetings']
    if meetings:
        markdown += "\n### Board Meeting Schedule\n\n"
        if meetings.get('regular_schedule'):
            markdown += f"- **Schedule:** {meetings['regular_schedule']}\n"
        if meetings.get('time'):
            markdown += f"- **Time:** {meetings['time']}\n"
        if meetings.get('location'):
            markdown += f"- **Location:** {meetings['location']}\n"
        if meetings.get('phone'):
            markdown += f"- **Phone:** {meetings['phone']}\n"
        
        if meetings.get('upcoming_meetings'):
            markdown += "\n**Upcoming Meetings:**\n"
            for meeting in meetings['upcoming_meetings'][:3]:
                markdown += f"- {meeting.get('date', 'N/A')}"
                if meeting.get('type'):
                    markdown += f" - {meeting['type']}"
                if meeting.get('time'):
                    markdown += f" at {meeting['time']}"
                markdown += "\n"
    
    # Academic Performance - by school level
    markdown += "\n### Academic Performance\n\n"
    performance = county_data['performance_summary']
    markdown += f"- **Total Schools:** {performance['total_schools']}\n\n"
    
    if 'proficiency_by_level' in performance:
        markdown += "**Average Proficiency by School Level:**\n\n"
        
        for level in ['elementary', 'middle', 'high']:
            if level in performance['proficiency_by_level']:
                scores = performance['proficiency_by_level'][level]
                level_name = level.title()
                if level == 'elementary':
                    level_name += " (Grade 5)"
                elif level == 'middle':
                    level_name += " (Grade 8)"
                elif level == 'high':
                    level_name += " (Grade 10)"
                
                markdown += f"*{level_name}:* {scores['count']} schools\n"
                if scores.get('ELA'):
                    markdown += f"- ELA: {scores['ELA']}%\n"
                if scores.get('Math'):
                    markdown += f"- Math: {scores['Math']}%\n"
                if scores.get('Science'):
                    markdown += f"- Science: {scores['Science']}%\n"
                markdown += "\n"
    
    # Top performing schools
    perf = county_data['performance_summary']
    if perf.get('top_performing_schools'):
        markdown += f"**Top Performing Schools:**\n"
        for school in perf['top_performing_schools']:
            markdown += f"- {school['name']}: {school['average_proficiency']}% average proficiency\n"
    
    # Individual Schools
    markdown += "\n### Schools\n\n"
    for school in county_data['schools']:
        markdown += f"#### {school['name']}\n\n"
        
        if school.get('star_rating'):
            markdown += f"- **Star Rating:** {school['star_rating']}/5\n"
        if school.get('percentile_rank'):
            markdown += f"- **Percentile Rank:** {school['percentile_rank']}\n"
        
        mcap = school.get('highest_grade_mcap', {})
        if mcap and mcap.get('scores'):
            grade = mcap.get('grade_tested')
            markdown += f"- **MCAP Scores (Grade {grade}):**\n"
            for subject, score in sorted(mcap['scores'].items()):
                if score is not None:
                    markdown += f"  - {subject}: {score}%\n"
                else:
                    markdown += f"  - {subject}: Data not available\n"
        
        markdown += "\n"
    
    markdown += "\n---\n\n"

# Add footer
markdown += """## Data Sources

- **School Performance Data:** Maryland State Department of Education Report Card (reportcard.msde.maryland.gov)
- **Census Data:** U.S. Census Bureau American Community Survey
- **District Officials:** County school district websites and BoardDocs
- **MCAP Scores:** Maryland Comprehensive Assessment Program (2024-2025 school year)

## Notes

- MCAP scores represent proficiency rates (Performance Levels 3 and 4 combined)
- Highest grade tested: Grade 5 for elementary schools, Grade 8 for middle schools, Grade 10 for high schools
- Star ratings and percentile ranks are from the Maryland School Report Card
- Some schools (career/technical centers) may not have complete MCAP data

## Summary Statistics Across All Five Counties

"""

# Overall summary
all_mcap = []
for county in counties:
    perf = data[county]['performance_summary']
    if perf.get('average_proficiency'):
        avg = perf['average_proficiency']
        if avg.get('ELA'):
            all_mcap.append({
                'county': county,
                'ela': avg['ELA'],
                'math': avg['Math'],
                'science': avg['Science']
            })

if all_mcap:
    overall_ela = sum(c['ela'] for c in all_mcap) / len(all_mcap)
    overall_math = sum(c['math'] for c in all_mcap) / len(all_mcap)
    overall_science = sum(c['science'] for c in all_mcap) / len(all_mcap)
    
    markdown += f"**Regional Average Proficiency:**\n"
    markdown += f"- ELA: {overall_ela:.1f}%\n"
    markdown += f"- Math: {overall_math:.1f}%\n"
    markdown += f"- Science: {overall_science:.1f}%\n\n"
    
    # Rank counties
    markdown += "**County Rankings by Average Proficiency:**\n\n"
    sorted_counties = sorted(all_mcap, key=lambda x: (x['ela'] + x['math'] + x['science']) / 3, reverse=True)
    for i, county_stats in enumerate(sorted_counties, 1):
        avg_all = (county_stats['ela'] + county_stats['math'] + county_stats['science']) / 3
        markdown += f"{i}. **{county_stats['county']} County** - {avg_all:.1f}% average\n"

total_pop = sum(data[c]['census'].get('total_population', 0) for c in counties)
total_schools = sum(data[c]['performance_summary'].get('total_schools', 0) for c in counties)

markdown += f"\n**Total Population (5 counties):** {total_pop:,}\n"
markdown += f"**Total Schools:** {total_schools}\n"

# Save markdown
with open('COUNTY_SUMMARY_BOOK.md', 'w') as f:
    f.write(markdown)

print("✓ Created COUNTY_SUMMARY_BOOK.md")
print(f"  - {len(markdown.split('##'))} sections")
print(f"  - {len(markdown.splitlines())} lines")
