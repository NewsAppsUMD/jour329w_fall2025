#!/usr/bin/env python3
"""
Generate a comprehensive education beat book (VERSION 3) by combining:
1. Selected education stories (refined_beatbook_stories.json)
2. County demographic and performance data (county_summary_book_v2.json)
3. School-level data (school_summary_book_v2.json)
4. Blueprint summaries (blueprint_summaries.md)

VERSION 3 IMPROVEMENTS:
- Excludes candidates and Star Democrat writers from sources
- Removes Regional Education Partners and Media sections
- Uses footnotes instead of title references
- Corrects data years (discipline: 2023-2024, census/scores: 2024)
- Includes science in MCAP proficiency data
- State-level figures in separate list
- Excludes governor except for bill signings
- Explains legislative connections to education
- Removes neighboring district superintendents
- Removes community/service organizations and law enforcement
- Consolidates state orgs (Maryland Reads, etc.)
- Consistent source formatting, no duplicates
- Cleaner document references
"""

import json
import subprocess
import re
from collections import Counter, defaultdict
from pathlib import Path

MODEL_NAME = "groq/openai/gpt-oss-120b"
COUNTIES = [
    "Talbot County",
    "Kent County",
    "Dorchester County",
    "Caroline County",
    "Queen Anne's County"
]

INPUT_STORIES = "refined_beatbook_stories.json"
INPUT_COUNTY_DATA = "county_summary_book_v2.json"
INPUT_SCHOOL_DATA = "school_summary_book_v2.json"
INPUT_BLUEPRINT = "blueprint_summaries.md"
OUTPUT_FILE = "comprehensive_education_beatbook_v3.md"


# ---------------------------------------------------------
# LLM utility with <think> tag stripping and retry logic
# ---------------------------------------------------------
def run_llm(prompt: str, max_retries: int = 3) -> str:
    """Runs the LLM through the command-line interface and strips <think> tags."""
    import time
    
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ["llm", "-m", MODEL_NAME],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.decode("utf-8")
                if "Connection error" in error_msg and attempt < max_retries - 1:
                    print(f"    Connection error, retrying in 5 seconds... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(5)
                    continue
                raise RuntimeError(error_msg)
            
            output = result.stdout.decode("utf-8")
            
            # Strip out <think>...</think> content
            output = re.sub(r'<think>.*?</think>', '', output, flags=re.DOTALL)
            
            return output.strip()
            
        except subprocess.TimeoutExpired:
            if attempt < max_retries - 1:
                print(f"    Timeout, retrying... (attempt {attempt + 1}/{max_retries})")
                time.sleep(5)
                continue
            raise RuntimeError("LLM request timed out after multiple attempts")
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"    Error: {e}, retrying... (attempt {attempt + 1}/{max_retries})")
                time.sleep(5)
                continue
            raise
    
    raise RuntimeError("Failed after maximum retries")


# ---------------------------------------------------------
# Parse County Summary Data (JSON format for v2)
# ---------------------------------------------------------
def parse_county_data(json_file: str) -> dict:
    """
    Parse the county_summary_book_v2.json file to extract county-specific data.
    Returns a dict mapping county name to its data.
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    county_data = {}
    
    # The JSON structure has county names as top-level keys
    for county_name in COUNTIES:
        if county_name in data:
            county_data[county_name] = data[county_name]
    
    return county_data


# ---------------------------------------------------------
# Parse School Summary Data (JSON format for v2)
# ---------------------------------------------------------
def parse_school_data(json_file: str) -> dict:
    """
    Parse the school_summary_book_v2.json file to extract school-level data.
    Returns a dict mapping county name to list of schools.
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    schools_by_county = defaultdict(list)
    
    # The JSON structure has county names as top-level keys, with arrays of schools
    for county_name in COUNTIES:
        if county_name in data:
            # Each county maps directly to an array of school objects
            schools = data[county_name]
            if isinstance(schools, list):
                schools_by_county[county_name] = schools
    
    return schools_by_county


# ---------------------------------------------------------
# Parse Blueprint Summaries (Markdown format)
# ---------------------------------------------------------
def parse_blueprint_data(md_file: str) -> str:
    """
    Parse the blueprint_summaries.md file.
    Returns the full markdown content.
    """
    with open(md_file, 'r') as f:
        content = f.read()
    
    return content


# ---------------------------------------------------------
# Entity Extraction (metadata that exists in JSON)
# ---------------------------------------------------------
def extract_entities(stories):
    """
    Extracts metadata only from stories where llm_failed == False.
    """
    counters = {
        "people": Counter(),
        "organizations": Counter(),
        "initiatives": Counter(),
        "events": Counter(),
        "establishments": Counter(),
        "municipalities": Counter(),
        "regions": Counter(),
    }

    for s in stories:
        # Skip metadata if llm_failed == True
        if s.get("llm_failed", False) is True:
            continue

        for p in s.get("key_people", []):
            counters["people"][p] += 1
        for o in s.get("key_organizations", []):
            counters["organizations"][o] += 1
        for i in s.get("key_initiatives", []):
            counters["initiatives"][i] += 1
        for e in s.get("key_events", []):
            counters["events"][e] += 1
        for est in s.get("key_establishments", []):
            counters["establishments"][est] += 1
        for m in s.get("municipalities", []):
            counters["municipalities"][m] += 1
        for r in s.get("regions", []):
            counters["regions"][r] += 1

    def top(counter):
        return [x for x, _ in counter.most_common(15)] or ["None found"]

    return {
        "top_people": top(counters["people"]),
        "top_organizations": top(counters["organizations"]),
        "top_initiatives": top(counters["initiatives"]),
        "top_events": top(counters["events"]),
        "top_establishments": top(counters["establishments"]),
        "top_municipalities": top(counters["municipalities"]),
        "top_regions": top(counters["regions"]),
    }


# ---------------------------------------------------------
# Format County Data for Prompts
# ---------------------------------------------------------
def format_county_data(county_name: str, county_entry: dict) -> str:
    """Convert county JSON data to readable text for prompts."""
    if not county_entry:
        return "No data available"
    
    text = f"County: {county_name}\n\n"
    
    if "demographics" in county_entry:
        demo = county_entry["demographics"]
        text += "Demographics (2024 Census Data):\n"
        text += f"  Total K-12 Enrollment: {demo.get('total_k12_enrollment', 'N/A')}\n"
        text += f"  Total Population: {demo.get('total_population', 'N/A')}\n"
        text += f"  School Age Population (5-17): {demo.get('school_age_population_5_17', 'N/A')}\n"
        text += f"  Poverty Rate: {demo.get('poverty_rate_percent', 'N/A')}%\n"
        text += f"  Median Household Income: ${demo.get('median_household_income', 'N/A')}\n"
        text += f"  Broadband Access: {demo.get('broadband_access_rate_percent', 'N/A')}%\n"
        
        if "enrollment_by_race" in demo:
            text += "\n  Enrollment by Race:\n"
            for race, data in demo["enrollment_by_race"].items():
                text += f"    {race}: {data.get('count', 'N/A')} ({data.get('percentage', 'N/A')}%)\n"
        text += "\n"
    
    if "district" in county_entry and "leadership" in county_entry["district"]:
        lead = county_entry["district"]["leadership"]
        text += "District Leadership:\n"
        text += f"  Superintendent: {lead.get('superintendent', 'Unknown')}\n"
        text += f"  Website: {lead.get('website', 'N/A')}\n"
        
        if "board_members" in lead and lead["board_members"]:
            text += "\n  Board Members:\n"
            for member in lead["board_members"][:5]:  # Limit to first 5
                text += f"    {member.get('name', 'Unknown')} - {member.get('position', 'Board Member')}\n"
        text += "\n"
    
    if "performance" in county_entry:
        perf = county_entry["performance"]
        text += "Academic Performance (2024 MCAP Scores):\n"
        if "mcap_scores" in perf:
            for grade, subjects in perf["mcap_scores"].items():
                text += f"  Grade {grade}:\n"
                for subject, data in subjects.items():
                    text += f"    {subject}: {data.get('rate', 'N/A')}% (State avg: {data.get('state_average', 'N/A')}%)\n"
        text += "\n"
    
    return text


# ---------------------------------------------------------
# Format School Data for Prompts
# ---------------------------------------------------------
def format_school_data(schools: list) -> str:
    """Convert school JSON data to readable text for prompts."""
    if not schools:
        return "No school data available"
    
    text = f"Total Schools: {len(schools)}\n\n"
    
    for school in schools[:10]:  # Limit to top 10 for brevity
        text += f"**{school.get('school_name', 'Unknown School')}** ({school.get('school_number', 'N/A')})\n"
        text += f"  Category: {school.get('category', 'N/A')}\n"
        
        if "mcap_performance" in school:
            text += "  MCAP Performance (2024):\n"
            perf = school["mcap_performance"]
            for grade, subjects in perf.items():
                if isinstance(subjects, dict):
                    for subject, data in subjects.items():
                        if isinstance(data, dict):
                            rate = data.get('rate', 'N/A')
                            comparison = data.get('comparison', '')
                            text += f"    Grade {grade} {subject}: {rate}% ({comparison})\n"
        
        if "suspension_data" in school and school["suspension_data"]:
            susp = school["suspension_data"][0]  # First suspension record
            total = susp.get('total_suspensions', 0)
            text += f"  Total Suspensions (2023-2024): {total}\n"
        
        text += "\n"
    
    return text


# ---------------------------------------------------------
# Generate County Overview
# ---------------------------------------------------------
def build_county_overview_prompt(county, county_data_text, school_data_text, blueprint_excerpt, entities, story_count, recent_stories_text):
    return f"""
You are writing a "County Overview & Context" section for {county} in an education beat book for a new reporter.

County Data:
{county_data_text}

School-Level Data:
{school_data_text}

Blueprint Implementation Context:
{blueprint_excerpt[:1000]}

Story Coverage Insights:
- Total stories analyzed: {story_count}
- Key People mentioned: {entities['top_people'][:10]}
- Key Organizations: {entities['top_organizations'][:8]}
- Key Establishments: {entities['top_establishments'][:8]}
- Municipalities covered: {entities['top_municipalities'][:8]}

Recent Stories (Title, Summary, and Key Details):
{recent_stories_text}

Write a comprehensive overview section that helps a new reporter understand {county}'s education landscape.

Requirements:
- Start with 2-3 paragraphs of narrative that synthesizes the demographic data, academic performance, and governance structure
- Highlight notable patterns (e.g., achievement gaps, resource challenges, leadership transitions)
- Use data from the county section to ground your observations
- Reference stories using numbered footnotes [1], [2], etc. DO NOT use title references
- Write in a direct, newsroom style - no fluff
- After the narrative, include a "Quick Facts" subsection with key numbers in bullet form
- CRITICAL DATA YEARS: Census/demographic data is from 2024. MCAP scores are from 2024. Discipline data is from 2023-2024 school year.
- Include ALL subjects in MCAP data: ELA, Math, AND Science proficiency rates
- CRITICAL: When mentioning any dates or events, ALWAYS include the full year (e.g., "November 2025", "2024-2025 school year"). Focus on developments from 2025.
"""


# ---------------------------------------------------------
# Generate Top Issues
# ---------------------------------------------------------
def build_top_issues_prompt(county, county_data_text, school_data_text, entities, stories_content, date_range):
    return f"""
You are writing the "Top Three Issues on the Education Beat" section for {county}, Maryland.

County Performance Data:
{county_data_text}

School-Level Context:
{school_data_text[:800]}

Recent Stories (with full content, summaries, and metadata):
{stories_content}

Metadata from Coverage:
- Key Initiatives: {entities['top_initiatives']}
- Key Events: {entities['top_events']}
- Key Organizations: {entities['top_organizations'][:8]}

Dataset date range: {date_range}

Write a "Top Three Issues on the Education Beat" section.

Requirements:
- Produce **exactly three issues**, each as an **H3 heading (###)**
- Under each heading, write **2-4 paragraphs** of narrative prose
- **Do NOT use bullets or lists**
- Ground each issue in both the story coverage and the performance data
- Reference stories using numbered footnotes [1], [2], etc. DO NOT use title references
- Issues should be ongoing challenges or policy debates, not one-time events
- Focus on systemic problems: funding, achievement gaps, infrastructure, staffing, policy conflicts
- Write like a beat reporter briefing a colleague
- CRITICAL DATA YEARS: Census data from 2024. MCAP scores from 2024. Discipline data from 2023-2024.
- CRITICAL: When mentioning any dates or events, ALWAYS include the full year (e.g., "September 2025", "2024-2025 school year"). Focus primarily on developments from 2025.
"""


# ---------------------------------------------------------
# Generate Key Sources
# ---------------------------------------------------------
def build_sources_prompt(county, county_data_text, entities, stories_with_context):
    return f"""
You are writing the "Key Sources to Know" section for {county}, Maryland.

County Leadership Data:
{county_data_text[:600]}

Coverage Insights:
- Key People: {entities['top_people']}
- Key Organizations: {entities['top_organizations']}
- Key Establishments: {entities['top_establishments']}

Recent Stories with Context:
{stories_with_context}

Write a "Key Sources to Know" section.

CRITICAL EXCLUSIONS - DO NOT INCLUDE:
- Political candidates for office
- Star Democrat writers or journalists
- Neighboring district superintendents from other counties
- Community & Service Organizations
- Law Enforcement & Public Safety personnel
- State Education Agency officials
- Education Policy & Advocacy Groups (unless directly tied to county operations)
- Duplicate names

CATEGORIES TO INCLUDE:
- District Leadership (superintendent, board members)
- School Principals
- State Legislators (ONLY if directly connected to education - explain their education role/committee assignments)

Requirements:
- Use **H4 headings (####)** to label source categories
- Under each heading, use **bulleted lists**
- Each bullet should identify:
  - A specific person and their position
  - What decisions/areas they influence
  - Use consistent name formatting and spelling
- For state legislators: explain their specific connection to education (e.g., "serves on Senate Education Committee")
- DO NOT include the governor unless specifically about bill signings
- Keep bullets concise and factual
- CRITICAL: When referencing events or appointments, ALWAYS include the full year (e.g., "appointed in 2025", "as of 2025").
"""


# ---------------------------------------------------------
# Generate Story Themes
# ---------------------------------------------------------
def build_story_themes_prompt(county, full_stories_text):
    return f"""
You are analyzing education coverage in {county}, Maryland to identify recurring story themes and patterns.

Stories with Full Content and Metadata:
{full_stories_text}

Write a "Recent Coverage Themes" section that identifies 3-5 recurring story patterns.

Requirements:
- Use **H4 headings (####)** for each theme
- Under each heading, write 1-2 paragraphs explaining:
  - What stories fell into this theme (use numbered footnotes [1], [2], etc.)
  - What angle or perspective dominated
  - Key findings or quotes from the stories
  - What questions remain unresolved
- Themes might include: test scores/achievement, budget battles, facility projects, Blueprint implementation, discipline/safety, personnel changes, etc.
- Write in a newsroom analysis style
- CRITICAL: When mentioning any dates or events, ALWAYS include the full year (e.g., "March 2025", "the 2024-2025 school year"). Focus on coverage from 2025.
"""


# ---------------------------------------------------------
# Generate Documents Section
# ---------------------------------------------------------
def build_documents_prompt(all_entities, blueprint_excerpt, sample_stories_with_content):
    return f"""
You are creating a "Key Documents, Records & Websites" section for an education beat book covering five Maryland Eastern Shore counties: Talbot, Kent, Dorchester, Caroline, and Queen Anne's.

Blueprint Implementation Context:
{blueprint_excerpt[:1000]}

Metadata from Coverage:
- Key Initiatives: {all_entities['top_initiatives']}
- Key Organizations: {all_entities['top_organizations'][:10]}

Sample Stories (with summaries showing document references):
{sample_stories_with_content}

Write a consolidated "Key Documents, Records & Websites to Track" section.

Requirements:
- Use **H3 headings (###)** for document categories (e.g., "### Budget & Finance Records", "### Assessment & Accountability Data")
- Under each heading, use **bulleted lists**
- Each bullet should identify:
  - A specific document type or website
  - What information it provides (1 sentence)
  - Whether it's county-level or state-level
- Include: budgets, CIPs, board minutes, MCAP data, enrollment reports, staffing data, Blueprint plans
- Reference documents mentioned in the stories
- Organize logically by topic area
- Keep explanations concise
- DO NOT include format indicators like (PDF), (web portal), etc. - just the document name
- CRITICAL: When referring to reports or data years, ALWAYS include the full year (e.g., "2024-2025 budget", "2024 MCAP results").
"""


# ---------------------------------------------------------
# Generate State-Level Resources Section
# ---------------------------------------------------------
def build_state_resources_prompt(all_entities):
    return f"""
You are creating a "State-Level Resources & Organizations" section for an education beat book.

Key Organizations from Coverage:
{all_entities['top_organizations'][:15]}

Key Initiatives:
{all_entities['top_initiatives'][:15]}

Write a consolidated section listing state-level education resources.

Requirements:
- Use **H4 headings (####)** for categories:
  - #### State Legislators with Education Roles
  - #### State Education Organizations
  - #### Key State Figures & Data

- For State Legislators: ONLY include those with direct education committee assignments or education-focused roles. Explain their specific connection to education.

- For State Education Organizations: Group similar organizations together (e.g., Maryland Reads, Maryland Rural Development Cooperative, Giving the Edge Foundation in one list). DO NOT include individual public school employees or local advocacy groups.

- For Key State Figures & Data: Include state-level MCAP averages and other statewide benchmarks for comparison. DO NOT include the governor except to note education bills signed.

- Use bulleted lists under each heading
- Keep entries concise
- Avoid duplicates
- Focus on resources relevant to Eastern Shore education reporting
"""


# ---------------------------------------------------------
# MAIN SCRIPT
# ---------------------------------------------------------
def main():
    print("Loading data files...")
    
    # Load stories
    with open(INPUT_STORIES, "r") as f:
        stories = json.load(f)
    
    # Load county data (v2 JSON format)
    county_data = parse_county_data(INPUT_COUNTY_DATA)
    
    # Load school data (v2 JSON format)
    school_data = parse_school_data(INPUT_SCHOOL_DATA)
    
    # Load blueprint summaries
    blueprint_text = parse_blueprint_data(INPUT_BLUEPRINT)
    
    # Group stories by county
    stories_by_county = defaultdict(list)
    for story in stories:
        for county in story.get("counties", []):
            if county in COUNTIES:
                stories_by_county[county].append(story)
    
    print(f"Loaded {len(stories)} stories across {len(stories_by_county)} counties")
    
    # Create beatbook
    with open(OUTPUT_FILE, "w") as out:
        out.write("# Comprehensive Education Beat Book (Version 3)\n")
        out.write("## Five Maryland Eastern Shore Counties\n\n")
        out.write("*A complete reference guide for education reporters covering Talbot, Kent, Dorchester, Caroline, and Queen Anne's Counties*\n\n")
        out.write(f"*Generated November 2025 from {INPUT_STORIES} with enhanced county/school data*\n\n")
        out.write("*Focuses on 2025 developments and the 2024-2025 school year*\n\n")
        out.write("**Data Sources:** Census data (2024), MCAP scores (2024), Discipline data (2023-2024 school year)\n\n")
        out.write("---\n\n")
        
        # Table of Contents
        out.write("## Table of Contents\n\n")
        for county in COUNTIES:
            county_short = county.replace(" County", "")
            out.write(f"- [{county_short}](#{county_short.lower().replace(' ', '-')})\n")
        out.write("- [State-Level Resources](#state-level-resources--organizations)\n")
        out.write("- [Key Documents & Resources](#key-documents--resources)\n\n")
        out.write("---\n\n")
        
        # Process each county
        for county in COUNTIES:
            print(f"\n{'='*60}")
            print(f"Processing {county}...")
            print(f"{'='*60}")
            
            county_stories = stories_by_county.get(county, [])
            if not county_stories:
                print(f"  No stories found for {county}, skipping...")
                continue
            
            county_entry = county_data.get(county, {})
            county_data_text = format_county_data(county, county_entry)
            
            schools = school_data.get(county, [])
            school_data_text = format_school_data(schools)
            
            # Extract relevant blueprint section for this county
            blueprint_excerpt = blueprint_text  # Could be filtered by county if needed
            
            # Extract metadata
            entities = extract_entities(county_stories)
            
            # Date range
            dates = [s.get("date") for s in county_stories if s.get("date")]
            date_range = f"{min(dates)} to {max(dates)}" if dates else "unknown"
            
            # Build comprehensive story text for different uses
            # For overview: Recent stories with title, summary, key metadata
            recent_stories_text = ""
            for i, s in enumerate(county_stories[:8], 1):
                recent_stories_text += f"\n{i}. **{s.get('title', 'Untitled')}** ({s.get('date', 'No date')})\n"
                if s.get('summary'):
                    recent_stories_text += f"   Summary: {s.get('summary')}\n"
                if s.get('key_people'):
                    recent_stories_text += f"   Key People: {', '.join(s.get('key_people', [])[:5])}\n"
                if s.get('key_initiatives'):
                    recent_stories_text += f"   Initiatives: {', '.join(s.get('key_initiatives', [])[:3])}\n"
                recent_stories_text += "\n"
            
            # For issues: More detailed story content
            stories_content = ""
            for i, s in enumerate(county_stories[:15], 1):
                stories_content += f"\n**Story {i}: {s.get('title', 'Untitled')}** ({s.get('date', 'No date')})\n"
                if s.get('summary'):
                    stories_content += f"Summary: {s.get('summary')}\n"
                if s.get('content'):
                    # Include first 500 chars of content for context
                    content_excerpt = s.get('content', '')[:500].strip()
                    stories_content += f"Content excerpt: {content_excerpt}...\n"
                stories_content += "\n"
            
            # For sources: Stories with people/organization context
            stories_with_context = ""
            for i, s in enumerate(county_stories[:12], 1):
                stories_with_context += f"\n{i}. **{s.get('title', 'Untitled')}**\n"
                if s.get('key_people'):
                    stories_with_context += f"   People: {', '.join(s.get('key_people', []))}\n"
                if s.get('key_organizations'):
                    stories_with_context += f"   Organizations: {', '.join(s.get('key_organizations', []))}\n"
                if s.get('summary'):
                    stories_with_context += f"   Context: {s.get('summary')[:200]}...\n"
                stories_with_context += "\n"
            
            # For themes: Full story details
            full_stories_text = ""
            for i, s in enumerate(county_stories[:10], 1):
                full_stories_text += f"\n**Story {i}: {s.get('title', 'Untitled')}** ({s.get('date', 'No date')})\n"
                full_stories_text += f"Author: {s.get('author', 'Unknown')}\n"
                if s.get('summary'):
                    full_stories_text += f"Summary: {s.get('summary')}\n"
                if s.get('key_initiatives'):
                    full_stories_text += f"Initiatives: {', '.join(s.get('key_initiatives', []))}\n"
                if s.get('key_events'):
                    full_stories_text += f"Events: {', '.join(s.get('key_events', []))}\n"
                if s.get('content'):
                    content_excerpt = s.get('content', '')[:600].strip()
                    full_stories_text += f"Content: {content_excerpt}...\n"
                full_stories_text += "\n"
            
            # Write county header
            county_short = county.replace(" County", "")
            out.write(f"# {county_short}\n\n")
            out.write(f"**Stories analyzed:** {len(county_stories)} | **Date range:** {date_range}\n\n")
            out.write("---\n\n")
            
            # 1. COUNTY OVERVIEW & CONTEXT
            print(f"  Generating county overview...")
            overview_prompt = build_county_overview_prompt(
                county, county_data_text, school_data_text, blueprint_excerpt, 
                entities, len(county_stories), recent_stories_text
            )
            overview_text = run_llm(overview_prompt)
            out.write("## County Overview & Context\n\n")
            out.write(overview_text.strip() + "\n\n")
            out.write("---\n\n")
            
            # 2. TOP THREE ISSUES
            print(f"  Generating top three issues...")
            issues_prompt = build_top_issues_prompt(
                county, county_data_text, school_data_text, entities, stories_content, date_range
            )
            issues_text = run_llm(issues_prompt)
            out.write("## Top Three Issues on the Education Beat\n\n")
            out.write(issues_text.strip() + "\n\n")
            out.write("---\n\n")
            
            # 3. KEY SOURCES
            print(f"  Generating key sources...")
            sources_prompt = build_sources_prompt(
                county, county_data_text, entities, stories_with_context
            )
            sources_text = run_llm(sources_prompt)
            out.write("## Key Sources to Know\n\n")
            out.write(sources_text.strip() + "\n\n")
            out.write("---\n\n")
            
            # 4. RECENT COVERAGE THEMES
            print(f"  Analyzing coverage themes...")
            themes_prompt = build_story_themes_prompt(
                county, full_stories_text
            )
            themes_text = run_llm(themes_prompt)
            out.write("## Recent Coverage Themes\n\n")
            out.write(themes_text.strip() + "\n\n")
            out.write("---\n\n")
        
        # 5. STATE-LEVEL RESOURCES
        print(f"\n{'='*60}")
        print("Generating state-level resources section...")
        print(f"{'='*60}")
        
        all_stories = []
        for county_stories in stories_by_county.values():
            all_stories.extend(county_stories)
        
        all_entities = extract_entities(all_stories)
        
        state_prompt = build_state_resources_prompt(all_entities)
        state_text = run_llm(state_prompt)
        
        out.write("# State-Level Resources & Organizations\n\n")
        out.write(state_text.strip() + "\n\n")
        out.write("---\n\n")
        
        # 6. CONSOLIDATED DOCUMENTS SECTION
        print(f"\n{'='*60}")
        print("Generating consolidated documents section...")
        print(f"{'='*60}")
        
        # Build sample stories with content for documents section
        sample_stories_with_content = ""
        for i, s in enumerate(all_stories[:20], 1):
            sample_stories_with_content += f"\n{i}. **{s.get('title', 'Untitled')}**\n"
            if s.get('summary'):
                sample_stories_with_content += f"   Summary: {s.get('summary')[:250]}...\n"
            if s.get('key_initiatives'):
                sample_stories_with_content += f"   Initiatives: {', '.join(s.get('key_initiatives', []))}\n"
            sample_stories_with_content += "\n"
        
        docs_prompt = build_documents_prompt(all_entities, blueprint_text, sample_stories_with_content)
        docs_text = run_llm(docs_prompt)
        
        out.write("# Key Documents & Resources\n\n")
        out.write("*Applies across all five counties unless noted*\n\n")
        out.write(docs_text.strip() + "\n\n")
    
    print(f"\n{'='*60}")
    print(f"✓ Beat book generated: {OUTPUT_FILE}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
