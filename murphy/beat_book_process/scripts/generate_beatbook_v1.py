#!/usr/bin/env python3
import json
import subprocess
from collections import Counter, defaultdict
import textwrap

MODEL_NAME = "groq/openai/gpt-oss-120b"

COUNTIES = [
    "Talbot County",
    "Kent County",
    "Dorchester County",
    "Caroline County",
    "Queen Anne's County"
]

INPUT_FILE = "selected_processed_education_stories.json"
OUTPUT_FILE = "education_beatbook_draft_v1.md"


# ---------------------------------------------------------
# LLM utility
# ---------------------------------------------------------
def run_llm(prompt: str) -> str:
    """Runs the LLM through the command-line interface."""
    result = subprocess.run(
        ["llm", "-m", MODEL_NAME],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8"))
    return result.stdout.decode("utf-8")


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
# Prompt: TOP THREE ISSUES (NO BULLETS, narrative under H3 headings)
# ---------------------------------------------------------
def build_top_issues_prompt(county, entities, titles, full_content, date_range):
    return f"""
You are writing the "Top Three Issues on the Education Beat" section for {county}, Maryland.

You will determine the three biggest issues by analyzing the *full story text*, not just metadata.

Dataset date range: {date_range}

Metadata available (context only):
- Key People: {entities['top_people']}
- Key Organizations: {entities['top_organizations']}
- Key Initiatives: {entities['top_initiatives']}
- Key Events: {entities['top_events']}
- Key Establishments: {entities['top_establishments']}
- Municipalities: {entities['top_municipalities']}
- Regions: {entities['top_regions']}

Sample Story Titles:
{titles}

FULL STORY CONTENT (this is your MAIN evidence):
\"\"\"TEXT_START
{full_content}
TEXT_END\"\"\"


Write a section titled "Top Three Issues on the Education Beat".

Requirements:
- Produce **exactly three issues**, each as an **H3 heading (###)**.
- Under each heading, write **3–4 paragraphs of narrative prose** that lay out and contextualizes what an education reporter needs know.
- **Do NOT use bullets or lists** in this section.
- Base your assessment primarily on the full story content.
- The writing must feel like a newsroom beat memo for a reporter.
"""


# ---------------------------------------------------------
# Prompt: Key Sources (HEADINGS + BULLETS ALLOWED)
# ---------------------------------------------------------
def build_sources_prompt(county, entities, titles, full_content):
    return f"""
You are writing the "Key Sources to Know" section of a beat book for {county}, Maryland.

Stories may include metadata from:
- key_people
- key_organizations
- key_initiatives
- key_events
- key_establishments
- municipalities
- regions

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

FULL STORY CONTENT:
\"\"\"TEXT_START
{full_content}
TEXT_END\"\"\"


Write a “Key Sources to Know” section for {county}.

Requirements:
- Use **H3 headings** to label different source categories (e.g., “### Superintendent and Central Office Leadership”).
- Under each heading, use **bulleted lists**.
- Each bullet should identify:
  - A specific person, position, or office (e.g., superintendent, board chair, principal, union rep)
  - Why they matter and what decisions they influence
  - Why a reporter might contact them
- Keep bullets concise and journalist-friendly.
"""


# ---------------------------------------------------------
# Prompt: Documents & Websites (HEADINGS + BULLETS)
# ---------------------------------------------------------
def build_documents_prompt(county, entities, titles, full_content):
    return f"""
You are writing the "Key Documents, Records & Websites to Track" section of a beat book for {county}, Maryland.

Metadata available includes:
- Key People: {entities['top_people']}
- Key Organizations: {entities['top_organizations']}
- Key Initiatives: {entities['top_initiatives']}
- Key Events: {entities['top_events']}
- Key Establishments: {entities['top_establishments']}
- Municipalities: {entities['top_municipalities']}
- Regions: {entities['top_regions']}

Story Titles:
{titles}

FULL STORY CONTENT:
\"\"\"TEXT_START
{full_content}
TEXT_END\"\"\"


Write a “Key Documents, Records & Websites to Track” section for {county}.

Requirements:
- Use **H3 headings** for document categories (e.g., “### Budget & Finance Records”).
- Under each heading, use **bulleted lists**.
- Bullets should:
  - Identify a document type (e.g., CIP, budget book, staffing report, discipline dataset)
  - Explain what information it provides
  - Explain why it matters for reporting
- Include county-level and MSDE/Blueprint-related materials.
"""


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
        out.write("Generated from selected_processed_education_stories.json\n\n")

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

            # Full content (primary evidence)
            full_content = "\n\n".join(
                s.get("content", "") for s in stories if s.get("content")
            )
            if len(full_content) > 28000:
                full_content = full_content[:28000]

            # Date range
            dates = [s.get("date") for s in stories if s.get("date")]
            date_range = f"{min(dates)} to {max(dates)}" if dates else "unknown"

            # Header
            out.write(f"## {county}\n\n")

            # --- TOP THREE ISSUES ---
            issue_prompt = build_top_issues_prompt(
                county, entities, titles, full_content, date_range
            )
            issues_text = run_llm(issue_prompt)
            out.write("### Top Three Issues on the Education Beat\n\n")
            out.write(issues_text.strip() + "\n\n")

            # --- SOURCES ---
            source_prompt = build_sources_prompt(
                county, entities, titles, full_content
            )
            sources_text = run_llm(source_prompt)
            out.write("### Key Sources to Know\n\n")
            out.write(sources_text.strip() + "\n\n")

            # --- DOCUMENTS ---
            docs_prompt = build_documents_prompt(
                county, entities, titles, full_content
            )
            docs_text = run_llm(docs_prompt)
            out.write("### Key Documents, Records & Websites to Track\n\n")
            out.write(docs_text.strip() + "\n\n")

    print(f"Beat book generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
