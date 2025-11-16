#!/usr/bin/env python3
import json
import subprocess
import re
from collections import Counter, defaultdict

MODEL_NAME = "groq/qwen/qwen3-32b"

COUNTIES = [
    "Talbot County",
    "Kent County",
    "Dorchester County",
    "Caroline County",
    "Queen Anne's County"
]

INPUT_FILE = "selected_processed_education_stories.json"
OUTPUT_FILE = "education_beatbook_draft_v2.md"


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
# Prompt: TOP THREE ISSUES (SIMPLIFIED - MAX 3 PARAGRAPHS)
# ---------------------------------------------------------
def build_top_issues_prompt(county, entities, titles, date_range):
    return f"""
You are writing the "Top Three Issues on the Education Beat" section for {county}, Maryland.

You will determine the three biggest issues by analyzing the story titles and metadata.

Dataset date range: {date_range}

Metadata:
- Key People: {entities['top_people']}
- Key Organizations: {entities['top_organizations']}
- Key Initiatives: {entities['top_initiatives']}
- Key Events: {entities['top_events']}
- Key Establishments: {entities['top_establishments']}
- Municipalities: {entities['top_municipalities']}
- Regions: {entities['top_regions']}

Story Titles:
{titles}


Write a section titled "Top Three Issues on the Education Beat".

Requirements:
- Produce **exactly three issues**, each as an **H3 heading (###)**.
- Under each heading, write **MAXIMUM THREE PARAGRAPHS** of narrative prose.
- **Do NOT use bullets or lists** in this section.
- Be concise and focused - get to the point quickly.
- Base your assessment on the story titles and metadata provided.
- The writing must feel like a newsroom beat memo for a reporter.
"""


# ---------------------------------------------------------
# Prompt: Key Sources (SIMPLIFIED - NO "WHY THIS MATTERS")
# ---------------------------------------------------------
def build_sources_prompt(county, entities, titles):
    return f"""
You are writing the "Key Sources to Know" section of a beat book for {county}, Maryland.

Metadata:
- Key People: {entities['top_people']}
- Key Organizations: {entities['top_organizations']}
- Key Initiatives: {entities['top_initiatives']}
- Key Events: {entities['top_events']}
- Key Establishments: {entities['top_establishments']}
- Municipalities: {entities['top_municipalities']}
- Regions: {entities['top_regions']}

Story Titles:
{titles}


Write a "Key Sources to Know" section for {county}.

Requirements:
- Use **H3 headings** to label different source categories (e.g., "### Superintendent and Central Office Leadership").
- Under each heading, use **bulleted lists**.
- Each bullet should identify:
  - A specific person, position, or office (e.g., superintendent, board chair, principal, union rep)
  - What decisions they influence
- Keep bullets concise - NO "why this matters" explanations.
"""


# ---------------------------------------------------------
# Collect all documents across all counties for consolidated list
# ---------------------------------------------------------
def collect_all_documents(stories_by_county):
    """
    Collects documents from all counties to create a consolidated list.
    Returns a dictionary with document categories and their descriptions.
    """
    all_stories = []
    for county_stories in stories_by_county.values():
        all_stories.extend(county_stories)
    
    entities = extract_entities(all_stories)
    
    titles = "\n".join(
        f"- {s.get('title','').strip()}" for s in all_stories[:30] if s.get("title")
    )
    
    prompt = f"""
You are creating a consolidated "Key Documents, Records & Websites to Track" section for an education beat book covering five Maryland counties: Talbot County, Kent County, Dorchester County, Caroline County, and Queen Anne's County.

Metadata:
- Key People: {entities['top_people']}
- Key Organizations: {entities['top_organizations']}
- Key Initiatives: {entities['top_initiatives']}
- Key Events: {entities['top_events']}
- Key Establishments: {entities['top_establishments']}
- Municipalities: {entities['top_municipalities']}
- Regions: {entities['top_regions']}

Story Titles:
{titles}


Write a consolidated "Key Documents, Records & Websites to Track" section that applies across all five counties.

Requirements:
- Use **H3 headings** for document categories (e.g., "### Budget & Finance Records", "### Assessment Data").
- Under each heading, use **bulleted lists**.
- Bullets should:
  - Identify a document type (e.g., CIP, budget book, staffing report, discipline dataset)
  - Briefly explain what information it provides
  - Keep explanations concise - one sentence maximum
- Include county-level and MSDE/Blueprint-related materials that apply across counties.
- Do NOT create separate sections for each county - this should be ONE consolidated list.
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
        out.write("Generated from selected_processed_education_stories.json (v2 - Simplified)\n\n")

        for county in COUNTIES:
            stories = stories_by_county.get(county, [])
            if not stories:
                continue

            # Metadata extraction
            entities = extract_entities(stories)

            # Titles for context
            titles = "\n".join(
                f"- {s.get('title','').strip()}" for s in stories[:20] if s.get("title")
            )

            # Date range
            dates = [s.get("date") for s in stories if s.get("date")]
            date_range = f"{min(dates)} to {max(dates)}" if dates else "unknown"

            # Header
            out.write(f"## {county}\n\n")

            # --- TOP THREE ISSUES ---
            print(f"Generating top issues for {county}...")
            issue_prompt = build_top_issues_prompt(
                county, entities, titles, date_range
            )
            issues_text = run_llm(issue_prompt)
            out.write("### Top Three Issues on the Education Beat\n\n")
            out.write(issues_text.strip() + "\n\n")

            # --- SOURCES ---
            print(f"Generating key sources for {county}...")
            source_prompt = build_sources_prompt(
                county, entities, titles
            )
            sources_text = run_llm(source_prompt)
            out.write("### Key Sources to Know\n\n")
            out.write(sources_text.strip() + "\n\n")

        # --- CONSOLIDATED DOCUMENTS (ONCE, FOR ALL COUNTIES) ---
        print("Generating consolidated documents list...")
        docs_text = collect_all_documents(stories_by_county)
        out.write("## Key Documents, Records & Websites to Track (All Counties)\n\n")
        out.write(docs_text.strip() + "\n\n")

    print(f"Beat book generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
