#!/usr/bin/env python3
"""
Generate County Summary Books from organized data files.

This script creates comprehensive county education summary books in both JSON and Markdown
formats, similar to county_summary_book_v2.json and county_summary_book_v2.md.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


def load_json(filepath: Path) -> Any:
    """Load JSON file and return data."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def load_markdown(filepath: Path) -> str:
    """Load markdown file and return content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return ""


def extract_county_data(county_folder: Path, county_name: str) -> Dict[str, Any]:
    """Extract all data for a county from its folder."""
    
    county_key = county_name.replace('_', ' ').title()
    if county_key == "Queen Annes":
        county_key = "Queen Anne's"
    
    data = {
        "county_name": county_key,
        "demographics": {},
        "district": {},
        "schools": {},
        "mcap_averages_by_school_level": {},
        "suspension_data": {},
        "blueprint_summary": "",
        "education_budget": ""
    }
    
    # Load census/demographic data
    census_file = county_folder / f"{county_name}_census_education_data.json"
    if census_file.exists():
        census_data = load_json(census_file)
        # Try with " County" suffix if base name doesn't work
        county_census_key = f"{county_key} County"
        if census_data:
            if county_census_key in census_data:
                county_census = census_data[county_census_key]
            elif county_key in census_data:
                county_census = census_data[county_key]
            else:
                county_census = None
                
            if county_census:
                data["demographics"] = {
                    "total_population": county_census.get("Total Population"),
                    "school_age_population_5_17": county_census.get("School-Age Population (5-17)"),
                    "total_k12_enrollment": county_census.get("total_k12_enrollment"),
                    "enrollment_by_race": county_census.get("enrollment_by_race", {}),
                    "poverty_rate_percent": county_census.get("Poverty Rate (%)"),
                    "median_household_income": county_census.get("Median household income"),
                    "broadband_access_rate_percent": county_census.get("Broadband Access Rate (%)"),
                    "education_metrics": {
                        "school_enrollment_rate_percent": county_census.get("School Enrollment Rate (%)"),
                        "adult_education_25_and_over": {
                            "total_population": county_census.get("Total population 25 years and over"),
                            "high_school_graduate": county_census.get("High school graduate"),
                            "bachelors_degree": county_census.get("Bachelor's degree"),
                            "masters_degree": county_census.get("Master's degree"),
                            "professional_degree": county_census.get("Professional school degree"),
                            "doctorate": county_census.get("Doctorate degree")
                        }
                    }
                }
    
    # Load district officials
    officials_file = county_folder / f"{county_name}_district_officials.json"
    if officials_file.exists():
        officials_data = load_json(officials_file)
        if officials_data and len(officials_data) > 0:
            official = officials_data[0]
            data["district"]["leadership"] = {
                "superintendent": official.get("superintendent"),
                "website": official.get("website"),
                "board_members": official.get("board_members", [])
            }
    
    # Load board meeting schedules
    meetings_file = county_folder / f"{county_name}_board_meeting_schedules_complete.json"
    if meetings_file.exists():
        meetings_data = load_json(meetings_file)
        if meetings_data:
            data["district"]["board_meetings"] = meetings_data
    
    # Load teacher data
    teacher_file = county_folder / f"{county_name}_teacher_data.json"
    if teacher_file.exists():
        teacher_data = load_json(teacher_file)
        if teacher_data and len(teacher_data) > 0:
            teacher = teacher_data[0]
            data["district"]["teacher_data"] = {
                "total_teachers": teacher.get("teachers"),
                "year_over_year_change_pct": teacher.get("teacher_change_pct"),
                "new_hires": teacher.get("new_hires"),
                "new_hires_pct": teacher.get("new_hires_pct"),
                "student_teacher_ratio": teacher.get("student_teacher_ratio")
            }
    
    # Load schools data
    schools_file = county_folder / f"{county_name}_schools_enhanced_data.json"
    if schools_file.exists():
        schools_data = load_json(schools_file)
        if schools_data:
            data["schools"] = {
                "elementary": [],
                "middle": [],
                "high": [],
                "other": []
            }
            for school in schools_data:
                school_name = school.get("school_name", "")
                # Categorize by school level
                if "Elementary" in school_name:
                    data["schools"]["elementary"].append(school_name)
                elif "Middle" in school_name:
                    data["schools"]["middle"].append(school_name)
                elif "High" in school_name and "Middle/High" not in school_name:
                    data["schools"]["high"].append(school_name)
                elif "Middle/High" in school_name:
                    # Add to both middle and high
                    data["schools"]["middle"].append(school_name)
                    data["schools"]["high"].append(school_name)
                else:
                    data["schools"]["other"].append(school_name)
    
    # Load MCAP data
    mcap_file = county_folder / f"{county_name}_mcap_highest_grades.json"
    state_mcap_file = county_folder / f"{county_name}_state_mcap_averages.json"
    
    if mcap_file.exists() and state_mcap_file.exists():
        mcap_data = load_json(mcap_file)
        state_averages = load_json(state_mcap_file)
        
        if mcap_data and state_averages:
            # Organize MCAP data by school level
            elementary_scores = {"5": {"ELA": [], "Math": [], "Science": []}}
            middle_scores = {"8": {"ELA": [], "Math": [], "Science": []}}
            high_scores = {"High School": {"ELA": [], "Math (Algebra 1)": [], "Science": []}}
            
            # Process list format
            for item in mcap_data:
                school_name = item.get("school_name", "")
                grade = item.get("grade")
                subject = item.get("subject")
                rate = item.get("proficiency_rate")
                
                is_elementary = "Elementary" in school_name
                is_middle = "Middle" in school_name and "High" not in school_name
                is_high = "High" in school_name
                
                if rate is not None and rate != "N/A":
                    if grade == 5 and is_elementary:
                        if subject in elementary_scores["5"]:
                            elementary_scores["5"][subject].append(float(rate))
                    elif grade == 8 and is_middle:
                        if subject in middle_scores["8"]:
                            middle_scores["8"][subject].append(float(rate))
                    elif grade == "High School" and is_high:
                        if subject == "ELA":
                            high_scores["High School"]["ELA"].append(float(rate))
                        elif subject == "Math (Algebra 1)":
                            high_scores["High School"]["Math (Algebra 1)"].append(float(rate))
                        elif subject == "Science":
                            high_scores["High School"]["Science"].append(float(rate))
            
            # Calculate averages and comparisons
            def calc_avg_comparison(scores: List[float], state_avg: float) -> Dict[str, Any]:
                if not scores:
                    return None
                avg = round(sum(scores) / len(scores), 1)
                diff = round(avg - state_avg, 1)
                comparison = f"{'+' if diff > 0 else ''}{diff} {'above' if diff > 0 else 'below'} state"
                return {
                    "average_rate": avg,
                    "state_average": state_avg,
                    "comparison": comparison,
                    "schools_counted": len(scores)
                }
            
            data["mcap_averages_by_school_level"] = {
                "elementary": {
                    "5": {
                        "ELA": calc_avg_comparison(elementary_scores["5"]["ELA"], state_averages.get("ELA_5", 45.0)),
                        "Math": calc_avg_comparison(elementary_scores["5"]["Math"], state_averages.get("Math_5", 30.7)),
                        "Science": calc_avg_comparison(elementary_scores["5"]["Science"], state_averages.get("Science_5", 25.6))
                    }
                },
                "middle": {
                    "8": {
                        "ELA": calc_avg_comparison(middle_scores["8"]["ELA"], state_averages.get("ELA_8", 48.4)),
                        "Math": calc_avg_comparison(middle_scores["8"]["Math"], state_averages.get("Math_8", 8.7)),
                        "Science": calc_avg_comparison(middle_scores["8"]["Science"], state_averages.get("Science_8", 31.4))
                    }
                },
                "high": {
                    "High School": {
                        "ELA": calc_avg_comparison(high_scores["High School"]["ELA"], state_averages.get("ELA_10", 59.5)),
                        "Math (Algebra 1)": calc_avg_comparison(high_scores["High School"]["Math (Algebra 1)"], state_averages.get("Math_Algebra_1", 21.4)),
                        "Science": calc_avg_comparison(high_scores["High School"]["Science"], state_averages.get("Science_All_High", 44.2))
                    }
                }
            }
    
    # Load suspension data
    suspension_file = county_folder / f"{county_name}_county_level_suspensions_2023_2024.json"
    if suspension_file.exists():
        suspension_data = load_json(suspension_file)
        if suspension_data and len(suspension_data) > 0:
            data["suspension_data"] = suspension_data[0]
    
    # Load blueprint summary
    blueprint_file = county_folder / f"{county_name}_blueprint_summary.md"
    if blueprint_file.exists():
        data["blueprint_summary"] = load_markdown(blueprint_file)
    
    # Load education budget
    budget_file = county_folder / f"{county_name}_education_budget.md"
    if budget_file.exists():
        data["education_budget"] = load_markdown(budget_file)
    
    return data


def generate_json_summary(counties_data: Dict[str, Dict]) -> Dict[str, Any]:
    """Generate the JSON summary structure."""
    
    # Get state averages from first county
    first_county = list(counties_data.values())[0]
    state_mcap = {}
    if first_county["mcap_averages_by_school_level"]:
        elem = first_county["mcap_averages_by_school_level"].get("elementary", {}).get("5", {})
        middle = first_county["mcap_averages_by_school_level"].get("middle", {}).get("8", {})
        high = first_county["mcap_averages_by_school_level"].get("high", {}).get("High School", {})
        
        for subject, data in elem.items():
            if data:
                state_mcap[f"{subject}_5"] = data["state_average"]
        for subject, data in middle.items():
            if data:
                state_mcap[f"{subject}_8"] = data["state_average"]
        for subject, data in high.items():
            if data:
                key = subject.replace(" ", "_").replace("(", "").replace(")", "")
                if subject == "ELA":
                    state_mcap["ELA_10"] = data["state_average"]
                elif "Algebra" in subject:
                    state_mcap["Math_Algebra_1"] = data["state_average"]
                else:
                    state_mcap["Science_All_High"] = data["state_average"]
    
    summary = {
        "metadata": {
            "generated_date": datetime.now().strftime("%B %Y"),
            "data_sources_summary": {
                "demographic_data": {
                    "source": "U.S. Census Bureau American Community Survey",
                    "year": "2022 (5-Year Estimates)",
                    "notes": "Population, income, poverty, education, broadband access, K-12 enrollment by race"
                },
                "school_performance": {
                    "source": "Maryland Comprehensive Assessment Program (MCAP)",
                    "year": "2023-2024 school year",
                    "notes": "Test scores in ELA, Math, and Science with comparisons to state averages"
                },
                "district_leadership": {
                    "source": "County School Board websites",
                    "year": "2024-2025 school year",
                    "notes": "Superintendent and board member information"
                },
                "teacher_staffing": {
                    "source": "MSDE Educator Dashboard",
                    "year": "2024",
                    "notes": "Teacher counts, student-teacher ratios, year-over-year changes, new hires"
                },
                "discipline_data": {
                    "source": "Maryland Department of Education Suspension Reports",
                    "year": "2023-2024 school year",
                    "notes": "Suspension counts by type, demographics, and offense categories"
                }
            },
            "counties_included": list(counties_data.keys()),
            "total_schools": sum(
                len(data["schools"].get("elementary", [])) +
                len(data["schools"].get("middle", [])) +
                len(data["schools"].get("high", [])) +
                len(data["schools"].get("other", []))
                for data in counties_data.values()
            ),
            "state_mcap_averages": state_mcap
        }
    }
    
    # Add each county's data
    for county_name, data in counties_data.items():
        summary[county_name] = {
            "demographics": data["demographics"],
            "district": data["district"],
            "schools": data["schools"],
            "mcap_averages_by_school_level": data["mcap_averages_by_school_level"],
            "suspension_data": data["suspension_data"]
        }
    
    return summary


def generate_markdown_summary(counties_data: Dict[str, Dict]) -> str:
    """Generate the Markdown summary document."""
    
    md = f"""# Maryland Eastern Shore County Education Summary Book

**Generated:** {datetime.now().strftime("%B %Y")}

---

"""
    
    for county_name, data in counties_data.items():
        # Helper to format numbers with commas
        def fmt(val, prefix='', suffix=''):
            if val is None or val == 'N/A':
                return 'N/A'
            return f"{prefix}{val:,}{suffix}" if isinstance(val, (int, float)) else str(val)
        
        md += f"""# {county_name}

## Demographics

- **Total Population:** {fmt(data['demographics'].get('total_population'))}
- **School-Age Population (5-17):** {fmt(data['demographics'].get('school_age_population_5_17'))}
- **Total K-12 Enrollment:** {fmt(data['demographics'].get('total_k12_enrollment'))}
- **Poverty Rate:** {data['demographics'].get('poverty_rate_percent', 'N/A')}%
- **Median Household Income:** {fmt(data['demographics'].get('median_household_income'), '$')}
- **Broadband Access Rate:** {data['demographics'].get('broadband_access_rate_percent', 'N/A')}%

### K-12 Enrollment by Race

"""
        enrollment = data['demographics'].get('enrollment_by_race', {})
        for race, info in enrollment.items():
            race_display = race.replace('_', ' ')
            md += f"- **{race_display}:** {fmt(info.get('count', 0))} ({info.get('percentage', 0)}%)\n"
        
        md += "\n### Adult Education (25 and Over)\n\n"
        adult_ed = data['demographics'].get('education_metrics', {}).get('adult_education_25_and_over', {})
        if adult_ed:
            md += f"- **Total Population:** {fmt(adult_ed.get('total_population'))}\n"
            md += f"- **High School Graduate:** {fmt(adult_ed.get('high_school_graduate'))}\n"
            md += f"- **Bachelor's Degree:** {fmt(adult_ed.get('bachelors_degree'))}\n"
            md += f"- **Master's Degree:** {fmt(adult_ed.get('masters_degree'))}\n"
            md += f"- **Professional Degree:** {fmt(adult_ed.get('professional_degree'))}\n"
            md += f"- **Doctorate:** {fmt(adult_ed.get('doctorate'))}\n"
        
        md += "\n## District Leadership\n\n"
        leadership = data['district'].get('leadership', {})
        md += f"### Superintendent\n**{leadership.get('superintendent', 'N/A')}**\n\n"
        
        board_members = leadership.get('board_members', [])
        if board_members:
            md += "### Board Members\n\n"
            for member in board_members:
                position = member.get('position', 'Board Member')
                md += f"- **{member.get('name', 'N/A')}** ({position})\n"
        
        meetings = data['district'].get('board_meetings', {})
        if meetings:
            md += "\n### Board Meetings\n\n"
            md += f"- **Schedule:** {meetings.get('schedule', 'N/A')}\n"
            if meetings.get('location'):
                md += f"- **Location:** {meetings.get('location')}\n"
            if meetings.get('time'):
                md += f"- **Time:** {meetings.get('time')}\n"
        
        teacher_data = data['district'].get('teacher_data', {})
        if teacher_data:
            md += f"\n## Teacher Staffing (2024)\n\n"
            md += f"- **Total Teachers:** {teacher_data.get('total_teachers', 'N/A')}\n"
            md += f"- **Student-Teacher Ratio:** {teacher_data.get('student_teacher_ratio', 'N/A')}\n"
            md += f"- **Year-over-Year Change:** {teacher_data.get('year_over_year_change_pct', 'N/A'):+.1f}%\n"
            if teacher_data.get('new_hires'):
                md += f"- **New Hires:** {teacher_data.get('new_hires')} ({teacher_data.get('new_hires_pct', 0):.1f}% of total)\n"
        
        schools = data['schools']
        md += "\n## Schools\n\n"
        
        if schools.get('elementary'):
            md += f"### Elementary Schools ({len(schools['elementary'])})\n\n"
            for school in schools['elementary']:
                md += f"- {school}\n"
            md += "\n"
        
        if schools.get('middle'):
            md += f"### Middle Schools ({len(schools['middle'])})\n\n"
            for school in schools['middle']:
                md += f"- {school}\n"
            md += "\n"
        
        if schools.get('high'):
            md += f"### High Schools ({len(schools['high'])})\n\n"
            for school in schools['high']:
                md += f"- {school}\n"
            md += "\n"
        
        if schools.get('other'):
            md += f"### Other Schools ({len(schools['other'])})\n\n"
            for school in schools['other']:
                md += f"- {school}\n"
            md += "\n"
        
        # MCAP Performance
        mcap = data['mcap_averages_by_school_level']
        if mcap:
            md += "## MCAP Performance Averages by School Level (2023-2024)\n\n"
            
            if mcap.get('elementary', {}).get('5'):
                md += "**Grade 5:**\n\n"
                for subject, scores in mcap['elementary']['5'].items():
                    if scores:
                        diff = scores['average_rate'] - scores['state_average']
                        direction = "above" if diff > 0 else "below"
                        md += f"- **{subject}:** {scores['average_rate']}% ({abs(diff):.1f} points {direction} state average of {scores['state_average']}%)\n"
                md += "\n"
            
            if mcap.get('middle', {}).get('8'):
                md += "**Grade 8:**\n\n"
                for subject, scores in mcap['middle']['8'].items():
                    if scores:
                        diff = scores['average_rate'] - scores['state_average']
                        direction = "above" if diff > 0 else "below"
                        md += f"- **{subject}:** {scores['average_rate']}% ({abs(diff):.1f} points {direction} state average of {scores['state_average']}%)\n"
                md += "\n"
            
            if mcap.get('high', {}).get('High School'):
                md += "**High School:**\n\n"
                for subject, scores in mcap['high']['High School'].items():
                    if scores:
                        diff = scores['average_rate'] - scores['state_average']
                        direction = "above" if diff > 0 else "below"
                        md += f"- **{subject}:** {scores['average_rate']}% ({abs(diff):.1f} points {direction} state average of {scores['state_average']}%)\n"
                md += "\n"
        
        # Suspension Data
        suspension = data.get('suspension_data', {})
        if suspension and suspension.get('total_suspensions'):
            md += f"## Discipline Data (2023-2024)\n\n"
            md += f"- **Total Suspensions:** {suspension.get('total_suspensions')}\n"
        
        md += "\n---\n\n"
    
    return md


def main():
    """Main function to generate county summary books."""
    
    base_dir = Path(__file__).parent / "things_to_use"
    output_dir = Path(__file__).parent / "county_summary_books"
    output_dir.mkdir(exist_ok=True)
    
    counties = ["caroline", "dorchester", "kent", "queen_annes", "talbot"]
    
    print("Generating county summary books...")
    
    counties_data = {}
    
    for county in counties:
        print(f"  Processing {county.replace('_', ' ').title()}...")
        county_folder = base_dir / county
        
        if not county_folder.exists():
            print(f"    Warning: {county_folder} does not exist, skipping")
            continue
        
        data = extract_county_data(county_folder, county)
        
        # Format county name for output
        county_display = county.replace('_', ' ').title()
        if county_display == "Queen Annes":
            county_display = "Queen Anne's"
        
        counties_data[county_display] = data
    
    # Generate JSON summary
    print("\nGenerating JSON summary...")
    json_summary = generate_json_summary(counties_data)
    json_output = output_dir / "county_summary_book.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(json_summary, f, indent=2, ensure_ascii=False)
    print(f"  ✓ {json_output}")
    
    # Generate Markdown summary
    print("\nGenerating Markdown summary...")
    md_summary = generate_markdown_summary(counties_data)
    md_output = output_dir / "county_summary_book.md"
    with open(md_output, 'w', encoding='utf-8') as f:
        f.write(md_summary)
    print(f"  ✓ {md_output}")
    
    # Generate individual county JSON files
    print("\nGenerating individual county JSON files...")
    for county_name, data in counties_data.items():
        county_slug = county_name.lower().replace("'", "").replace(" ", "_")
        county_json = output_dir / f"{county_slug}_summary.json"
        
        county_output = {
            county_name: {
                "demographics": data["demographics"],
                "district": data["district"],
                "schools": data["schools"],
                "mcap_averages_by_school_level": data["mcap_averages_by_school_level"],
                "suspension_data": data["suspension_data"]
            }
        }
        
        with open(county_json, 'w', encoding='utf-8') as f:
            json.dump(county_output, f, indent=2, ensure_ascii=False)
        print(f"  ✓ {county_json}")
    
    # Generate individual county Markdown files
    print("\nGenerating individual county Markdown files...")
    for county_name, data in counties_data.items():
        county_slug = county_name.lower().replace("'", "").replace(" ", "_")
        county_md = output_dir / f"{county_slug}_summary.md"
        
        # Generate markdown for single county
        single_county_data = {county_name: data}
        md_content = generate_markdown_summary(single_county_data)
        
        with open(county_md, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"  ✓ {county_md}")
    
    print("\n✅ Done! Summary books generated in:", output_dir)


if __name__ == "__main__":
    main()
