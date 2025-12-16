#!/usr/bin/env python3
import json
import subprocess
import re
from collections import Counter, defaultdict
from datetime import datetime

MODEL_NAME = "groq/openai/gpt-oss-120b"

COUNTIES = [
    "Talbot County",
    "Kent County",
    "Dorchester County",
    "Caroline County",
    "Queen Anne's County"
]

INPUT_FILE = "selected_processed_education_stories.json"
OUTPUT_FILE = "education_beatbook_draft_v3.md"

# Cutoff date for recent stories (Nov 2024)
RECENT_CUTOFF = "2024-11-01"


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
# Story Filtering by Date
# ---------------------------------------------------------
def partition_stories_by_date(stories):
    """Separate stories into recent (Nov 2024+) and historical."""
    recent = []
    historical = []
    
    for story in stories:
        date_str = story.get("date", "")
        if date_str >= RECENT_CUTOFF:
            recent.append(story)
        else:
            historical.append(story)
    
    return recent, historical


# ---------------------------------------------------------
# Entity Extraction (metadata that exists in JSON)
# ---------------------------------------------------------
def extract_entities(stories):
    """
    Extracts metadata *only from stories where llm_failed == False*.
    Stories with llm_failed == True contribute only content, not metadata.
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

    # Helper to return top 10 values or ["None found"]
    def top(counter):
        return [x for x, _ in counter.most_common(10)] or ["None found"]

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
# Format story titles with summaries
# ---------------------------------------------------------
def format_titles_with_summaries(stories, limit=20):
    """Format story titles with their summaries for LLM input."""
    formatted = []
    for s in stories[:limit]:
        title = s.get('title', '').strip()
        summary = s.get('summary', '')
        date = s.get('date', '')
        if title:
            if summary:
                formatted.append(f"- [{date}] {title}\n  Summary: {summary}")
            else:
                formatted.append(f"- [{date}] {title}")
    return "\n".join(formatted)


# ---------------------------------------------------------
# Prompt: TOP THREE ISSUES (PRIORITIZING RECENT COVERAGE)
# ---------------------------------------------------------
def build_top_issues_prompt(county, entities, recent_titles, historical_titles, date_range):
    return f"""
You are writing the "Top Three Issues on the Education Beat" section for {county}, Maryland.

You will determine the three biggest issues by analyzing story titles, summaries, and metadata.

**PRIORITIZE RECENT COVERAGE (Nov 2024 forward)** - These stories should drive your issue selection.
Use historical stories (before Nov 2024) only as context to understand how issues have developed.

Dataset date range: {date_range}

Metadata:
- Key People: {entities['top_people']}
- Key Organizations: {entities['top_organizations']}
- Key Initiatives: {entities['top_initiatives']}
- Key Events: {entities['top_events']}
- Key Establishments: {entities['top_establishments']}
- Municipalities: {entities['top_municipalities']}
- Regions: {entities['top_regions']}

RECENT STORIES (Nov 2024 forward) - **FOCUS HERE**:
{recent_titles}

HISTORICAL STORIES (Before Nov 2024) - Context only:
{historical_titles}


Write a section titled "Top Three Issues on the Education Beat".

Requirements:
- Produce **exactly three issues**, each as an **H3 heading (###)**.
- Under each heading, write **MAXIMUM THREE PARAGRAPHS** of narrative prose.
- **Do NOT use bullets or lists** in this section.
- **PRIORITIZE recent coverage** - focus on what's happening now or recently
- Use historical stories only to provide context for ongoing issues
- Be concise and focused - get to the point quickly.
- The writing must feel like a newsroom beat memo for a reporter.
"""


# ---------------------------------------------------------
# Prompt: Key Sources (PRIORITIZING RECENT COVERAGE)
# ---------------------------------------------------------
def build_sources_prompt(county, entities, recent_titles, historical_titles):
    return f"""
You are writing the "Key Sources to Know" section of a beat book for {county}, Maryland.

**PRIORITIZE people and organizations mentioned in recent coverage (Nov 2024 forward).**

Metadata:
- Key People: {entities['top_people']}
- Key Organizations: {entities['top_organizations']}
- Key Initiatives: {entities['top_initiatives']}
- Key Events: {entities['top_events']}
- Key Establishments: {entities['top_establishments']}
- Municipalities: {entities['top_municipalities']}
- Regions: {entities['top_regions']}

RECENT STORIES (Nov 2024 forward) - **FOCUS HERE**:
{recent_titles}

HISTORICAL STORIES (Before Nov 2024) - Context only:
{historical_titles}


Write a "Key Sources to Know" section for {county}.

Requirements:
- Use **H3 headings** to label different source categories (e.g., "### Superintendent and Central Office Leadership").
- Under each heading, use **bulleted lists**.
- Each bullet should identify:
  - A specific person, position, or office (e.g., superintendent, board chair, principal, union rep)
  - What decisions they influence
- **Prioritize sources from recent stories** - these are the active players
- Keep bullets concise - NO "why this matters" explanations.
"""


# ---------------------------------------------------------
# Comprehensive Documents Section (ALL COUNTIES)
# ---------------------------------------------------------
def build_comprehensive_documents_prompt(stories_by_county):
    """
    Creates a comprehensive data/documents section using all stories.
    """
    all_stories = []
    for county_stories in stories_by_county.values():
        all_stories.extend(county_stories)
    
    recent_stories, historical_stories = partition_stories_by_date(all_stories)
    
    entities = extract_entities(all_stories)
    
    recent_titles = format_titles_with_summaries(recent_stories, 30)
    historical_titles = format_titles_with_summaries(historical_stories, 20)
    
    prompt = f"""
You are creating a COMPREHENSIVE "Key Documents, Records & Data Sources to Track" section for an education beat book covering five Maryland counties: Talbot County, Kent County, Dorchester County, Caroline County, and Queen Anne's County.

This should be a thorough reference guide for reporters covering education across these counties.

Metadata:
- Key People: {entities['top_people']}
- Key Organizations: {entities['top_organizations']}
- Key Initiatives: {entities['top_initiatives']}
- Key Events: {entities['top_events']}
- Key Establishments: {entities['top_establishments']}
- Municipalities: {entities['top_municipalities']}
- Regions: {entities['top_regions']}

RECENT STORIES (Nov 2024 forward):
{recent_titles}

HISTORICAL STORIES (Before Nov 2024):
{historical_titles}


Write a comprehensive "Key Documents, Records & Data Sources to Track" section.

Requirements:
- Use **H3 headings** for document categories (e.g., "### Budget & Finance Records", "### Assessment & Academic Data", "### Personnel Records", "### Facilities & Capital Planning").
- Under each heading, use **bulleted lists**.
- Be COMPREHENSIVE - include all major document types a reporter would need
- For each bullet:
  - Identify the document type or data source
  - Briefly explain what information it provides (one sentence)
  - Include WHERE to find it when applicable (county websites, MSDE portal, etc.)
- Cover both county-level and state-level (MSDE/Blueprint) materials
- Include recurring reports (annual budgets, MCAP results, etc.)
- Include meeting records (board minutes, agendas, recordings)
- Include data dashboards and online portals
- This should be ONE consolidated list for all five counties - do NOT create separate sections per county.
"""
    
    return run_llm(prompt)


# ---------------------------------------------------------
# MAIN SCRIPT
# ---------------------------------------------------------
def main():

    # Load dataset
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    # Group stories by county
    stories_by_county = defaultdict(list)
    for story in data:
        for county in story.get("counties", []):
            if county in COUNTIES:
                stories_by_county[county].append(story)

    # Create beatbook file
    with open(OUTPUT_FILE, "w") as out:
        out.write("# Education Beat Book – Five Maryland Counties\n")
        out.write("Generated from selected_stories_with_summaries.json (v3 - Recent Coverage Priority)\n\n")

        for county in COUNTIES:
            stories = stories_by_county.get(county, [])
            if not stories:
                continue

            # Partition stories by date
            recent_stories, historical_stories = partition_stories_by_date(stories)
            
            print(f"\n{county}: {len(recent_stories)} recent stories, {len(historical_stories)} historical stories")

            # Metadata extraction (from all stories)
            entities = extract_entities(stories)

            # Format titles with summaries
            recent_titles = format_titles_with_summaries(recent_stories, 15)
            historical_titles = format_titles_with_summaries(historical_stories, 10)

            # Date range
            dates = [s.get("date") for s in stories if s.get("date")]
            date_range = f"{min(dates)} to {max(dates)}" if dates else "unknown"

            # Header
            out.write(f"## {county}\n\n")

            # --- TOP THREE ISSUES ---
            print(f"Generating top issues for {county}...")
            issue_prompt = build_top_issues_prompt(
                county, entities, recent_titles, historical_titles, date_range
            )
            issues_text = run_llm(issue_prompt)
            out.write("### Top Three Issues on the Education Beat\n\n")
            out.write(issues_text.strip() + "\n\n")

            # --- SOURCES ---
            print(f"Generating key sources for {county}...")
            source_prompt = build_sources_prompt(
                county, entities, recent_titles, historical_titles
            )
            sources_text = run_llm(source_prompt)
            out.write("### Key Sources to Know\n\n")
            out.write(sources_text.strip() + "\n\n")

        # --- COMPREHENSIVE DOCUMENTS SECTION (ONCE, FOR ALL COUNTIES) ---
        print("\nGenerating comprehensive documents section...")
        docs_text = build_comprehensive_documents_prompt(stories_by_county)
        out.write("## Key Documents, Records & Data Sources to Track (All Counties)\n\n")
        out.write(docs_text.strip() + "\n\n")

    print(f"\n✓ Beat book generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
