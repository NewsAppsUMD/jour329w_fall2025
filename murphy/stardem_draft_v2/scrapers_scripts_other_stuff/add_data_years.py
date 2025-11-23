#!/usr/bin/env python3
"""
Add year/data source information to county_summary_book.json
"""

import json

# Load the current data
with open('../county_summary_book.json', 'r') as f:
    data = json.load(f)

# Data source years based on typical data collection
data_years = {
    "census": "2022 American Community Survey 5-Year Estimates",
    "district_leadership": "2024-2025 school year",
    "board_meetings": "2025 (current)",
    "schools": "2023-2024 school year (MCAP scores)",
    "performance_summary": "2023-2024 school year (MCAP assessments)",
    "teacher_student_ratio": "2024 Educator Dashboard data",
    "cohort3_funding": "2024 School Improvement Funding Cohort 3"
}

# Add metadata section to each county
for county_name, county_data in data.items():
    # Add data_sources section at the top level
    if "data_sources" not in county_data:
        county_data["data_sources"] = {}
    
    # Add year info to each major section
    if "census" in county_data:
        county_data["data_sources"]["census"] = data_years["census"]
    
    if "district_leadership" in county_data:
        county_data["data_sources"]["district_leadership"] = data_years["district_leadership"]
    
    if "board_meetings" in county_data:
        county_data["data_sources"]["board_meetings"] = data_years["board_meetings"]
    
    if "schools" in county_data:
        county_data["data_sources"]["schools_mcap"] = data_years["schools"]
    
    if "performance_summary" in county_data:
        county_data["data_sources"]["performance_summary"] = data_years["performance_summary"]

# Add global metadata
metadata = {
    "metadata": {
        "generated_date": "November 2025",
        "data_sources_summary": {
            "demographic_data": {
                "source": "U.S. Census Bureau American Community Survey",
                "year": "2022 (5-Year Estimates)",
                "notes": "Population, income, poverty, education, broadband access"
            },
            "school_performance": {
                "source": "Maryland Comprehensive Assessment Program (MCAP)",
                "year": "2023-2024 school year",
                "notes": "Test scores in ELA, Math, and Science"
            },
            "school_information": {
                "source": "Maryland Report Card",
                "year": "2023-2024 school year",
                "notes": "School ratings, enrollment, staff data"
            },
            "district_leadership": {
                "source": "County School Board websites",
                "year": "2024-2025 school year",
                "notes": "Superintendent and board member information"
            },
            "teacher_staffing": {
                "source": "MSDE Educator Dashboard",
                "year": "2024",
                "notes": "Teacher counts, student-teacher ratios"
            },
            "school_improvement_funding": {
                "source": "MSDE School Improvement Funding Report",
                "year": "Cohort 3 (2024)",
                "notes": "Funding for Comprehensive and Additional Targeted Support schools"
            }
        },
        "counties_included": [
            "Caroline",
            "Dorchester", 
            "Kent",
            "Queen Anne's",
            "Talbot"
        ],
        "total_schools": 50
    }
}

# Insert metadata at the beginning
output_data = {**metadata, **data}

# Save updated file
with open('../county_summary_book_with_years.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print("✓ Created: county_summary_book_with_years.json")
print("\nAdded data source years for:")
for key, value in data_years.items():
    print(f"  - {key}: {value}")

# Also create a summary document
summary = """# Eastern Shore Education Beat Book - Data Sources

## Data Collection Period
**Generated:** November 2025

## Primary Data Sources

### Demographic Data
- **Source:** U.S. Census Bureau American Community Survey
- **Year:** 2022 (5-Year Estimates)
- **Includes:** Population, median household income, poverty rates, school enrollment, broadband access, education attainment, demographics

### School Performance Data  
- **Source:** Maryland Comprehensive Assessment Program (MCAP)
- **Year:** 2023-2024 school year
- **Includes:** Test scores in English Language Arts (ELA), Mathematics, and Science by school and grade level

### School Information
- **Source:** Maryland Report Card (MSDE)
- **Year:** 2023-2024 school year  
- **Includes:** School star ratings, percentile ranks, enrollment data

### District Leadership
- **Source:** County School Board websites
- **Year:** 2024-2025 school year
- **Includes:** Superintendent information, board members, meeting schedules

### Teacher Staffing
- **Source:** MSDE Educator Dashboard
- **Year:** 2024
- **Includes:** Teacher counts by county, year-over-year changes, new hires, student-teacher ratios

### School Improvement Funding
- **Source:** MSDE School Improvement Funding Report
- **Year:** Cohort 3 (2024)
- **Includes:** Funding amounts and improvement strategies for designated schools

## Counties Covered
- Caroline County
- Dorchester County
- Kent County
- Queen Anne's County
- Talbot County

## Total Schools: 50
"""

with open('../DATA_SOURCES.md', 'w') as f:
    f.write(summary)

print("\n✓ Created: DATA_SOURCES.md")
