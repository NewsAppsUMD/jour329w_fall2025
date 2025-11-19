#!/usr/bin/env python3
"""
Generate a comprehensive education beat book by combining:
1. Selected education stories (selected_processed_education_stories.json)
2. County demographic and performance data (COUNTY_SUMMARY_BOOK.md)

This creates a complete reference guide for a new education reporter.
"""

import json
import subprocess
import re
from collections import Counter, defaultdict
from pathlib import Path

MODEL_NAME = "groq/qwen/qwen3-32b"

COUNTIES = [
    "Talbot County",
    "Kent County",
    "Dorchester County",
    "Caroline County",
    "Queen Anne's County"
]

INPUT_STORIES = "refined_beat_book_stories.json"
INPUT_COUNTY_DATA = "COUNTY_SUMMARY_BOOK.md"
OUTPUT_FILE = "comprehensive_education_beatbook.md"


# ---------------------------------------------------------
# LLM utility with <think> tag stripping
# ---------------------------------------------------------
def run_llm(prompt: str) -> str:
    """Runs the LLM through the command-line interface and strips <think> tags."""
    result = subprocess.run(
        ["llm", "-m", MODEL_NAME],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8"))
    
    output = result.stdout.decode("utf-8")
    
    # Strip out <think>...</think> content
    output = re.sub(r'<think>.*?</think>', '', output, flags=re.DOTALL)
    
    return output.strip()


# ---------------------------------------------------------
# Parse County Summary Data
# ---------------------------------------------------------
def parse_county_data(md_file: str) -> dict:
    """
    Parse the COUNTY_SUMMARY_BOOK.md file to extract county-specific data.
    Returns a dict mapping county name to its full markdown section.
    """
    with open(md_file, 'r') as f:
        content = f.read()
    
    county_data = {}
    
    # Split by ## headers (county sections)
    sections = re.split(r'\n## ', content)
    
    for section in sections[1:]:  # Skip the intro
        lines = section.split('\n', 1)
        if len(lines) >= 2:
            county_name = lines[0].strip()
            county_content = lines[1].strip()
            
            # Match full county name
            for county in COUNTIES:
                if county_name in county or county.replace(' County', '') in county_name:
                    county_data[county] = county_content
                    break
    
    return county_data


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
# Generate County Overview (combines data + context from stories)
# ---------------------------------------------------------
def build_county_overview_prompt(county, county_data_section, entities, story_count, recent_stories_text):
    return f"""
You are writing a "County Overview & Context" section for {county} in an education beat book for a new reporter.

County Data:
{county_data_section}

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
- Reference specific stories and their content to illustrate key issues
- Write in a direct, newsroom style - no fluff
- After the narrative, include a "Quick Facts" subsection with key numbers in bullet form
"""


# ---------------------------------------------------------
# Generate Top Issues (informed by both stories and data)
# ---------------------------------------------------------
def build_top_issues_prompt(county, county_data_section, entities, stories_content, date_range):
    return f"""
You are writing the "Top Three Issues on the Education Beat" section for {county}, Maryland.

County Performance Data:
{county_data_section[:800]}

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
- Cite specific stories by title to support your points
- Issues should be ongoing challenges or policy debates, not one-time events
- Focus on systemic problems: funding, achievement gaps, infrastructure, staffing, policy conflicts
- Write like a beat reporter briefing a colleague
"""


# ---------------------------------------------------------
# Generate Key Sources
# ---------------------------------------------------------
def build_sources_prompt(county, county_data_section, entities, stories_with_context):
    return f"""
You are writing the "Key Sources to Know" section for {county}, Maryland.

County Leadership Data:
{county_data_section[:600]}

Coverage Insights:
- Key People: {entities['top_people']}
- Key Organizations: {entities['top_organizations']}
- Key Establishments: {entities['top_establishments']}

Recent Stories with Context:
{stories_with_context}

Write a "Key Sources to Know" section.

Requirements:
- Use **H4 headings (####)** to label source categories (e.g., "#### District Leadership", "#### School Principals")
- Under each heading, use **bulleted lists**
- Each bullet should identify:
  - A specific person, position, or office
  - What decisions/areas they influence
  - Which stories they appeared in (cite by title)
- Include roles from the county data (superintendent, board members) plus key figures from stories
- Keep bullets concise and factual
"""


# ---------------------------------------------------------
# Generate Story Themes (narrative synthesis)
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
  - What stories fell into this theme (cite by title)
  - What angle or perspective dominated
  - Key findings or quotes from the stories
  - What questions remain unresolved
- Themes might include: test scores/achievement, budget battles, facility projects, Blueprint implementation, discipline/safety, personnel changes, etc.
- Write in a newsroom analysis style
"""


# ---------------------------------------------------------
# Generate Documents Section (consolidated across counties)
# ---------------------------------------------------------
def build_documents_prompt(all_entities, sample_stories_with_content):
    return f"""
You are creating a "Key Documents, Records & Websites" section for an education beat book covering five Maryland Eastern Shore counties: Talbot, Kent, Dorchester, Caroline, and Queen Anne's.

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
"""


# ---------------------------------------------------------
# MAIN SCRIPT
# ---------------------------------------------------------
def main():
    print("Loading data files...")
    
    # Load stories
    with open(INPUT_STORIES, "r") as f:
        stories = json.load(f)
    
    # Load county data
    county_data = parse_county_data(INPUT_COUNTY_DATA)
    
    # Group stories by county
    stories_by_county = defaultdict(list)
    for story in stories:
        for county in story.get("counties", []):
            if county in COUNTIES:
                stories_by_county[county].append(story)
    
    print(f"Loaded {len(stories)} stories across {len(stories_by_county)} counties")
    
    # Create beatbook
    with open(OUTPUT_FILE, "w") as out:
        out.write("# Comprehensive Education Beat Book\n")
        out.write("## Five Maryland Eastern Shore Counties\n\n")
        out.write("*A complete reference guide for education reporters covering Talbot, Kent, Dorchester, Caroline, and Queen Anne's Counties*\n\n")
        out.write(f"*Generated from {INPUT_STORIES} - refined and curated education coverage*\n\n")
        out.write("---\n\n")
        
        # Table of Contents
        out.write("## Table of Contents\n\n")
        for county in COUNTIES:
            county_short = county.replace(" County", "")
            out.write(f"- [{county_short}](#{county_short.lower().replace(' ', '-')})\n")
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
            
            county_data_section = county_data.get(county, "No data available")
            
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
                county, county_data_section, entities, len(county_stories), recent_stories_text
            )
            overview_text = run_llm(overview_prompt)
            out.write("## County Overview & Context\n\n")
            out.write(overview_text.strip() + "\n\n")
            out.write("---\n\n")
            
            # 2. TOP THREE ISSUES
            print(f"  Generating top three issues...")
            issues_prompt = build_top_issues_prompt(
                county, county_data_section, entities, stories_content, date_range
            )
            issues_text = run_llm(issues_prompt)
            out.write("## Top Three Issues on the Education Beat\n\n")
            out.write(issues_text.strip() + "\n\n")
            out.write("---\n\n")
            
            # 3. KEY SOURCES
            print(f"  Generating key sources...")
            sources_prompt = build_sources_prompt(
                county, county_data_section, entities, stories_with_context
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
        
        # 5. CONSOLIDATED DOCUMENTS SECTION
        print(f"\n{'='*60}")
        print("Generating consolidated documents section...")
        print(f"{'='*60}")
        
        all_stories = []
        for county_stories in stories_by_county.values():
            all_stories.extend(county_stories)
        
        all_entities = extract_entities(all_stories)
        
        # Build sample stories with content for documents section
        sample_stories_with_content = ""
        for i, s in enumerate(all_stories[:20], 1):
            sample_stories_with_content += f"\n{i}. **{s.get('title', 'Untitled')}**\n"
            if s.get('summary'):
                sample_stories_with_content += f"   Summary: {s.get('summary')[:250]}...\n"
            if s.get('key_initiatives'):
                sample_stories_with_content += f"   Initiatives: {', '.join(s.get('key_initiatives', []))}\n"
            sample_stories_with_content += "\n"
        
        docs_prompt = build_documents_prompt(all_entities, sample_stories_with_content)
        docs_text = run_llm(docs_prompt)
        
        out.write("# Key Documents & Resources\n\n")
        out.write("*Applies across all five counties unless noted*\n\n")
        out.write(docs_text.strip() + "\n\n")
    
    print(f"\n{'='*60}")
    print(f"✓ Beat book generated: {OUTPUT_FILE}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
