#!/usr/bin/env python3
"""
Generate a five-county local government beatbook using LLM (VERSION 3).

VERSION 3 GOALS:
- Reduce hallucinations and keep the model grounded strictly in your data.
- Provide explicit "facts blocks" per county that the model must stick to.
- Pre-generate "Key Sources – VERIFIED FROM DATA" tables for each county
  from county_officials and municipal_officials JSON, so the model copies
  them instead of inventing names/titles.
- Tighten instructions for Section 1 (Narrative) and Section 7 (Key Issues).
- Preserve your V2 structure, TOC, and overall 10-part county layout.
"""

import subprocess
import json
import sys
import re
import time
from pathlib import Path
from collections import Counter

# Model to use
MODEL = "groq/openai/gpt-oss-120b"

# Base directory
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "scraped_county_data"

# Counties to process (order matters)
COUNTIES = ["caroline", "dorchester", "kent", "queen_annes", "talbot"]

# County name mapping for display
COUNTY_NAMES = {
    "caroline": "Caroline County",
    "dorchester": "Dorchester County",
    "kent": "Kent County",
    "queen_annes": "Queen Anne's County",
    "talbot": "Talbot County"
}


def load_file_content(filepath: Path) -> str:
    """Load content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not load {filepath}: {e}", file=sys.stderr)
        return ""


def load_json_file(filepath: Path):
    """Load JSON content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load {filepath}: {e}", file=sys.stderr)
        return {}


def run_llm(prompt: str, max_retries: int = 3) -> str:
    """Runs the LLM through subprocess and strips <think> tags."""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ["llm", "-m", MODEL],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=300  # 5 minute timeout
            )

            if result.returncode != 0:
                error_msg = result.stderr.decode("utf-8")
                print(f"  Attempt {attempt + 1} failed: {error_msg}", file=sys.stderr)
                if "Connection error" in error_msg and attempt < max_retries - 1:
                    print("  Retrying in 5 seconds...", file=sys.stderr)
                    time.sleep(5)
                    continue
                raise RuntimeError(error_msg)

            output = result.stdout.decode("utf-8")
            # Strip out <think>...</think> content, if present
            output = re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL)
            return output.strip()

        except subprocess.TimeoutExpired:
            if attempt < max_retries - 1:
                print(f"  Timeout, retrying... (attempt {attempt + 1}/{max_retries})", file=sys.stderr)
                time.sleep(5)
                continue
            raise RuntimeError("LLM request timed out after multiple attempts")
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Error: {e}, retrying... (attempt {attempt + 1}/{max_retries})", file=sys.stderr)
                time.sleep(5)
                continue
            raise

    raise RuntimeError("Failed after maximum retries")


def extract_story_insights(stories: list, county_filter: str = None) -> dict:
    """
    Extract key insights from stories for a specific county or all counties.
    Uses beatbook_tag and counties fields in the standardized story JSON.
    """
    filtered_stories = stories
    if county_filter:
        county_name = COUNTY_NAMES[county_filter]
        filtered_stories = [s for s in stories if county_name in s.get("counties", [])]

    # Extract dates
    dates = [s.get("date") for s in filtered_stories if s.get("date")]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "unknown"

    # Count stories by topic tags
    topic_counter = Counter()
    for story in filtered_stories:
        topic = story.get("beatbook_tag", "Other")
        topic_counter[topic] += 1

    return {
        "total_stories": len(filtered_stories),
        "date_range": date_range,
        "top_topics": topic_counter.most_common(10),
        "sample_stories": filtered_stories[:15]  # Include sample for context
    }


def _normalize_official_list(data):
    """
    Best-effort helper: given JSON that might be a list of officials or a dict
    wrapping such a list, try to return a list of official dicts.

    NOTE: You may want to customize this to match your actual schema.
    """
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        # Common patterns: {"officials": [...]} or {"data": [...]}
        for key in ("officials", "data", "rows", "items"):
            if key in data and isinstance(data[key], list):
                return data[key]
    return []


def build_key_sources_tables(officials_data, muni_officials_data) -> str:
    """
    Build pre-verified Key Sources tables from county_officials and municipal_officials JSON.
    The LLM will be instructed to copy these tables EXACTLY for each county's
    "Key Sources" section so it does not invent names or titles.

    NOTE: This assumes each item in the normalized list has at least a "name"
    and "title" (or similar). You may want to customize the key names.
    """
    county_officials = _normalize_official_list(officials_data)
    muni_officials = _normalize_official_list(muni_officials_data)

    def extract_name_title(rec):
        # Customize these keys to match your JSON
        name = (
            rec.get("name")
            or rec.get("full_name")
            or rec.get("official_name")
            or rec.get("person")
            or "UNKNOWN"
        )
        title = (
            rec.get("title")
            or rec.get("office")
            or rec.get("position")
            or "UNKNOWN"
        )
        return name, title

    lines = []

    lines.append("### County Commissioners / Council / Constitutional Offices\n")
    lines.append("| Name | Position | Area of Influence | Notes |")
    lines.append("|------|----------|-------------------|-------|")

    if county_officials:
        for rec in county_officials:
            name, title = extract_name_title(rec)
            # Leave Area of Influence & Notes blank for model to optionally fill
            lines.append(f"| {name} | {title} |  |  |")
    else:
        lines.append("| (no officials data provided) |  |  |  |")

    lines.append("\n### Municipal Leadership\n")
    lines.append("| Name | Position | Area of Influence | Notes |")
    lines.append("|------|----------|-------------------|-------|")

    if muni_officials:
        for rec in muni_officials:
            name, title = extract_name_title(rec)
            lines.append(f"| {name} | {title} |  |  |")
    else:
        lines.append("| (no municipal officials data provided) |  |  |  |")

    return "\n".join(lines)


def format_county_data_section(
    county: str,
    stories_data: list,
    county_issues: dict,
    county_summary: str
) -> str:
    """
    Format the comprehensive data section for a specific county.

    This section is NOT the beatbook itself. It is the "data package"
    that the LLM will read.

    We now:
    - Attach the education / county summary
    - Include structured JSON blocks
    - Attach a best-effort, verified Key Sources table built from officials JSON
    """

    county_name = COUNTY_NAMES[county]
    county_dir = DATA_DIR / county

    section = f"""

{'='*80}
# DATA PACKAGE FOR {county_name.upper()}
{'='*80}

"""

    # County summary (from county_summary_book_v2.md)
    section += f"""
## COUNTY EDUCATION / CONTEXT SUMMARY (from county_summary_book_v2.md)

{county_summary}

"""

    # 1. CENSUS AND DEMOGRAPHIC DATA
    census_file = county_dir / f"{county}_census.json"
    census_data = load_json_file(census_file)
    section += f"""
## 1. CENSUS AND DEMOGRAPHIC DATA (RAW JSON)

```json
{json.dumps(census_data, indent=2)}
```

"""

    # 2. COUNTY OFFICIALS
    officials_file = county_dir / f"{county}_county_officials.json"
    officials_data = load_json_file(officials_file)
    section += f"""
## 2. COUNTY OFFICIALS AND LEADERSHIP (RAW JSON)

```json
{json.dumps(officials_data, indent=2)}
```

"""

    # 3. MUNICIPAL OFFICIALS
    muni_officials_file = county_dir / f"{county}_municipal_officials.json"
    muni_officials_data = load_json_file(muni_officials_file)
    section += f"""
## 3. MUNICIPAL OFFICIALS (RAW JSON)

```json
{json.dumps(muni_officials_data, indent=2)}
```

"""

    # 4. MUNICIPALITIES CENSUS
    muni_census_file = county_dir / f"{county}_municipalities_census.json"
    muni_census_data = load_json_file(muni_census_file)
    section += f"""
## 4. MUNICIPALITIES DEMOGRAPHIC DATA (RAW JSON)

```json
{json.dumps(muni_census_data, indent=2)}
```

"""

    # 5. ELECTIONS DATA
    elections_file = county_dir / f"{county}_elections.json"
    elections_data = load_json_file(elections_file)
    section += f"""
## 5. ELECTIONS DATA AND POLITICAL LANDSCAPE (RAW JSON)

```json
{json.dumps(elections_data, indent=2)}
```

"""

    # 6. SCHOOLS DATA
    schools_file = county_dir / f"{county}_schools.json"
    schools_data = load_json_file(schools_file)
    section += f"""
## 6. SCHOOLS AND EDUCATION DATA (RAW JSON)

```json
{json.dumps(schools_data, indent=2)}
```

"""

    # 7. BUDGET ANALYSIS (markdown analysis, not JSON)
    budget_file = county_dir / f"{county}_budget_analysis.md"
    budget_content = load_file_content(budget_file)
    section += f"""
## 7. BUDGET AND FISCAL ANALYSIS (MARKDOWN FROM DATA)

{budget_content}

"""

    # 8. RECENT MEETING MINUTES ANALYSIS
    minutes_file = county_dir / f"{county}_recent_minutes_analysis.md"
    minutes_content = load_file_content(minutes_file)
    section += f"""
## 8. RECENT MEETING MINUTES AND GOVERNANCE ANALYSIS (MARKDOWN FROM DATA)

{minutes_content}

"""

    # 9. RELEVANT NEWS STORIES
    story_insights = extract_story_insights(stories_data, county)
    section += f"""
## 9. RELEVANT NEWS STORIES FOR {county_name} (FROM STANDARDIZED STORY CORPUS)

**Total Stories Analyzed:** {story_insights['total_stories']}  
**Date Range:** {story_insights['date_range']}

**Story Coverage by Topic (beatbook_tag):**
"""
    for topic, count in story_insights["top_topics"]:
        section += f"- {topic}: {count} stories\n"

    section += """

**Sample Stories (titles, dates, tags, and summaries):**
"""

    for i, story in enumerate(story_insights["sample_stories"], 1):
        section += f"""
### Story {i}: {story.get('title', 'Untitled')}
- **Date:** {story.get('date', 'Unknown')}
- **Author:** {story.get('author', 'Unknown')}
- **Tag (beatbook_tag):** {story.get('beatbook_tag', 'Other')}
- **Counties (parsed):** {', '.join(story.get('counties', [])) if isinstance(story.get('counties'), list) else story.get('counties', '')}
- **Summary (if provided):** {story.get('summary', 'No summary available')}

"""

    # 10. COUNTY-SPECIFIC ISSUES
    if isinstance(county_issues, dict) and COUNTY_NAMES[county] in county_issues:
        issues = county_issues[COUNTY_NAMES[county]]
        section += f"""
## 10. TOP ISSUES SPECIFIC TO {county_name} (RAW JSON)

```json
{json.dumps(issues, indent=2)}
```

"""

    # 11. VERIFIED KEY SOURCES TABLE (TO BE COPIED VERBATIM BY THE MODEL)
    key_sources_md = build_key_sources_tables(officials_data, muni_officials_data)
    section += f"""
## 11. KEY SOURCES – VERIFIED FROM OFFICIALS DATA

You MUST use the tables below EXACTLY as written when you build the
"Key Sources" section for this county.  
You MAY fill in the "Area of Influence" and "Notes" cells, but you MUST
NOT change any names or positions or invent additional officials.

{key_sources_md}

"""

    return section


def extract_county_summary(county_summary_content: str, county: str) -> str:
    """
    Extract the relevant section for a specific county from county_summary_book_v2.md.

    We assume headings of the form:
    # Caroline County
    # Dorchester County
    ...
    """
    county_name = COUNTY_NAMES[county]
    pattern = rf"# {re.escape(county_name)}(.*?)(?=\n# [A-Z]|\Z)"
    match = re.search(pattern, county_summary_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return f"County summary for {county_name} not found in county_summary_book_v2.md"


def build_prompt() -> str:
    """Build the complete prompt with all data files in a structured format (VERSION 3)."""

    print("Loading base prompt...", file=sys.stderr)
    base_prompt = load_file_content(BASE_DIR / "prompt.md")

    print("Loading county summary book...", file=sys.stderr)
    county_summary_content = load_file_content(BASE_DIR / "county_summary_book_v2.md")

    print("Loading story corpus...", file=sys.stderr)
    stories_data = load_json_file(BASE_DIR / "beatbook_standardized_stories.json")
    if not isinstance(stories_data, list):
        stories_data = []

    print("Loading issue analysis...", file=sys.stderr)
    recurring_issues = load_json_file(BASE_DIR / "top_recurring_issues.json")
    county_issues = load_json_file(BASE_DIR / "top_issues_by_county.json")

    # === GLOBAL INSTRUCTIONS & GUARDRAILS (VERSION 3) ===
    guardrails = f"""
{('='*80)}
GLOBAL INSTRUCTIONS AND GUARDRAILS (VERSION 3)
{('='*80)}

You are generating a FIVE-COUNTY LOCAL GOVERNMENT BEATBOOK for:
Caroline, Dorchester, Kent, Queen Anne's, and Talbot Counties in Maryland.

This beatbook is for PROFESSIONAL NEWSROOM USE. It must be:
- Factual
- Grounded ONLY in the data provided in this prompt
- Structured and internally consistent

ABSOLUTE RULES – NO HALLUCINATIONS:
1. You MAY ONLY use facts (names, titles, vote counts, dollar amounts, dates,
   project names, municipalities, enrollment figures, etc.) that appear in:
   - The census JSON
   - The elections JSON
   - The schools JSON
   - The county_officials and municipal_officials JSON
   - The municipalities_census JSON
   - The budget_analysis markdown
   - The recent_minutes_analysis markdown
   - The standardized stories JSON (beatbook_standardized_stories.json)
   - The recurring-issues and county-issues JSON

2. You MUST NOT:
   - Invent officials, job titles, agencies, committees, projects, or towns.
   - Invent dollar amounts, vote counts, or dates.
   - Import outside knowledge (e.g., statewide results not in the data).
   - Use municipalities or counties that do not appear in the data.

3. If a specific detail is NOT present in the data, you MUST:
   - Either omit it,
   - Or describe it as "not provided in the dataset."
   You must NOT guess or fabricate.

4. "KEY SOURCES – VERIFIED FROM OFFICIALS DATA" tables:
   - For EACH county, the data package includes a verified Key Sources table.
   - When you reach the county's "Key Sources" section at the end of the county,
     you MUST copy those tables EXACTLY for the Name and Position columns.
   - You MAY add content to the "Area of Influence" and "Notes" cells,
     but you MUST NOT change names or positions or add new people.

STRUCTURE YOU MUST FOLLOW:

For EACH COUNTY, you MUST produce exactly these 10 sections, in this order,
with these headings (use the county name in the H2):

1. Narrative Summary – "The State of the County"
2. Current Power Structure – Who Runs the County?
3. Civic Infrastructure & Demographics (Data Summary)
4. Elections & Political Landscape
5. Schools & Education Landscape
6. Budget & Fiscal Priorities
7. Key Local Government Issues to Watch
8. Municipal Profiles (Reference)
9. Stakeholder Map – Informal Power Centers
10. Red Flags & Accountability Priorities

After all five counties, you MUST produce:

11. Key Documents, Records & Public Resources
    - This is a cross-county, regional section.
    - Use the datasets and records referenced in the data packages.

TONE AND STYLE:
- Professional investigative newsroom tone.
- No casual language, no emojis, no conversational asides.
- Clear, analytic sentences. Think: "deep briefing memo."

NARRATIVE DEPTH REQUIREMENTS (REINFORCED):

Section 1: Narrative Summary – "The State of the County"
- 3–5 substantial paragraphs (≈150–200 words each).
- Identify and explain the top 5–8 issues shaping the county.
- Synthesize trends from:
  * meeting-minutes analysis
  * budget-analysis
  * standardized news stories
  * recurring-issues and county-issues JSON
- Explain local vs state/federal context.
- NO invented events, numbers, or actors.

Section 7: Key Local Government Issues to Watch
- Present 3–5 major issues as H3 headings under Section 7.
- For EACH issue, you MUST write EXACTLY three full paragraphs
  (minimum ≈120 words each):
  1) What is happening – who, what, where, when.
  2) Why it matters – fiscal, quality-of-life, political significance.
  3) Tensions & stakeholders – conflicts, alliances, accountability questions.
- You MUST anchor each issue in specific:
  - meeting-minutes analysis,
  - budget lines,
  - or stories from the standardized corpus.

KEY SOURCES SECTION (PER COUNTY):
- Near the end of EACH COUNTY (after Section 9 or 10), create a short
  "Key Sources" subsection that uses the VERIFIED table for that county.
- You MUST copy the tables from "KEY SOURCES – VERIFIED FROM OFFICIALS DATA"
  in that county's data package.
- Do NOT add new people who are not in the table.
- You MAY enrich "Area of Influence" and "Notes" columns.

MUNICIPAL PROFILES:
- You MUST only list municipalities that appear in the municipalities_census
  JSON for that county (or obviously from the official data).
- Do NOT import municipalities from other counties.

CROSS-COUNTY COMPARISONS:
- You MAY compare counties (e.g., relative poverty, population) BUT only using
  numbers that appear in the provided JSON or county summary data.

If at any point you are unsure whether a fact is in the data, treat it as
"not provided in the dataset" rather than guessing.

{('='*80)}
END GLOBAL INSTRUCTIONS
{('='*80)}

"""

    # === CROSS-COUNTY RECURRING ISSUES SECTION ===
    cross_county_block = f"""
{('='*80)}
{('='*80)}
# PART 1: REGIONAL CONTEXT AND CROSS-COUNTY ISSUES
{('='*80)}
{('='*80)}

The following JSON describes issues that recur across multiple counties:

```json
{json.dumps(recurring_issues, indent=2)}
```

You MUST use only the issues listed here and in the county-specific issues
JSON when you describe cross-county themes. Do NOT invent new issue labels.
"""

    full_prompt = f"""{base_prompt}

{guardrails}

{cross_county_block}

"""

    # Add county-specific data packages
    print("Building county data packages...", file=sys.stderr)
    for county in COUNTIES:
        print(f"  - Processing {COUNTY_NAMES[county]}...", file=sys.stderr)
        county_summary = extract_county_summary(county_summary_content, county)
        county_section = format_county_data_section(
            county=county,
            stories_data=stories_data,
            county_issues=county_issues,
            county_summary=county_summary
        )
        full_prompt += county_section

    # FINAL TASK INSTRUCTIONS
    full_prompt += f"""

{('='*80)}
{('='*80)}
# YOUR TASK: GENERATE THE COMPLETE BEATBOOK (VERSION 3)
{('='*80)}
{('='*80)}

Using ONLY the data and guardrails provided above, produce a comprehensive
five-county government beatbook with the following specifications:

1. COVERAGE:
   - Caroline County
   - Dorchester County
   - Kent County
   - Queen Anne's County
   - Talbot County

2. STRUCTURE:
   - For EACH county, follow the 10-part structure IN ORDER as specified in
     the GLOBAL INSTRUCTIONS section.
   - AFTER all five counties, write a final cross-county section called:
     "Key Documents, Records & Public Resources."

3. DATA FIDELITY:
   - You MUST NOT invent facts.
   - You MUST use only the people, numbers, projects, vote counts, and issues
     contained in the data packages.
   - If a plausible detail is not in the data, omit it or mark it as
     "not provided in the dataset."

4. KEY SOURCES:
   - For each county, include a short "Key Sources" subsection near the end.
   - Copy the "KEY SOURCES – VERIFIED FROM OFFICIALS DATA" table for that
     county EXACTLY for Name and Position columns.
   - You may add content only in the Area of Influence and Notes columns.

5. ANALYTICAL DEPTH:
   - Make extensive use of:
     * budget_analysis.md
     * recent_minutes_analysis.md
     * standardized stories (titles, summaries, tags)
     * recurring_issues and county_issues
   - Explain WHY issues matter and WHO holds power.
   - Highlight red flags and accountability angles.

6. ORDER:
   - Present counties in this order:
     1) Caroline County
     2) Dorchester County
     3) Kent County
     4) Queen Anne's County
     5) Talbot County

7. OUTPUT FORMAT:
   - Use Markdown headings (##, ###, etc.).
   - Mirror the heading and section naming described above so the output is
     easy to navigate.

Begin now with Caroline County, Section 1:
"## Caroline County – Beat Book" followed by
"### 1. Narrative Summary – \"The State of the County\"".

"""

    return full_prompt


def generate_beatbook() -> int:
    """Generate the beatbook using LLM via subprocess (VERSION 3)."""

    print("\n" + "="*80, file=sys.stderr)
    print("FIVE-COUNTY LOCAL GOVERNMENT BEATBOOK GENERATOR (VERSION 3)", file=sys.stderr)
    print("="*80 + "\n", file=sys.stderr)

    print("Step 1: Building comprehensive prompt...", file=sys.stderr)
    prompt = build_prompt()

    print("\nStep 2: Prompt prepared", file=sys.stderr)
    print(f"  - Prompt size: {len(prompt):,} characters", file=sys.stderr)
    print(f"  - Model: {MODEL}", file=sys.stderr)

    # Save prompt for debugging
    prompt_debug_file = BASE_DIR / "beatbook_prompt_debug_v3.txt"
    with open(prompt_debug_file, "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"  - Debug prompt saved to: {prompt_debug_file}", file=sys.stderr)

    print("\nStep 3: Calling LLM...", file=sys.stderr)
    print("  - Processing five counties with strict data guardrails", file=sys.stderr)
    print("  - Using pre-verified Key Sources tables", file=sys.stderr)
    print("  - Enforcing non-hallucination rules in prompt\n", file=sys.stderr)

    try:
        output = run_llm(prompt)

        # Build final beatbook with header and TOC
        final_output = """# Five-County Local Government Beatbook (Version 3)

## Caroline, Dorchester, Kent, Queen Anne's, and Talbot Counties

*A comprehensive reference guide for local government reporters*

*Generated: November 2025*

*Model: groq/openai/gpt-oss-120b*

---

## Table of Contents

- [Caroline County](#caroline-county--beat-book)
- [Dorchester County](#dorchester-county--beat-book)
- [Kent County](#kent-county--beat-book)
- [Queen Anne's County](#queen-annes-county--beat-book)
- [Talbot County](#talbot-county--beat-book)
- [Key Documents, Records & Public Resources](#key-documents-records--public-resources)

---

"""
        final_output += output

        output_file = BASE_DIR / "beatbook_v3.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_output)

        print("\n" + "="*80, file=sys.stderr)
        print("✓ BEATBOOK V3 GENERATED SUCCESSFULLY!", file=sys.stderr)
        print("="*80, file=sys.stderr)
        print(f"\nOutput saved to: {output_file}", file=sys.stderr)
        print(f"Output size: {len(final_output):,} characters", file=sys.stderr)
        print("\nYou can now review the beatbook at:", file=sys.stderr)
        print(f"  {output_file}\n", file=sys.stderr)

        return 0

    except Exception as e:
        print("\n" + "="*80, file=sys.stderr)
        print("✗ ERROR GENERATING BEATBOOK (VERSION 3)", file=sys.stderr)
        print("="*80, file=sys.stderr)
        print(f"\nError: {e}", file=sys.stderr)
        print("\nCheck the debug prompt file at:", file=sys.stderr)
        print(f"  {prompt_debug_file}\n", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(generate_beatbook())