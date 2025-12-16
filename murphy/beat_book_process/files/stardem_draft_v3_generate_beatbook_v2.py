#!/usr/bin/env python3
"""
Generate a five-county local government beatbook using LLM (VERSION 2).
Based on prompt.md and all scraped county data.

VERSION 2 CHANGES:
- Incorporates county_summary_book_v2.md for richer county context
- Simplified structure: eliminates Story Playbook and Contact Points sections
- Streamlined Table of Contents with clickable county links
- Reformatted Key Datasets & Sources to match beatbook_v2_enhanced.md style
- Reformatted Key Sources section with table format while matching v2_enhanced style
"""

import subprocess
import json
import sys
import re
import time
from pathlib import Path
from collections import Counter, defaultdict

# Model to use
MODEL = "groq/openai/gpt-oss-120b"

# Base directory
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "scraped_county_data"

# Counties to process
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


def load_json_file(filepath: Path) -> dict | list:
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
                timeout=300  # 5 minute timeout for large prompts
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.decode("utf-8")
                print(f"  Attempt {attempt + 1} failed: {error_msg}", file=sys.stderr)
                if "Connection error" in error_msg and attempt < max_retries - 1:
                    print(f"  Retrying in 5 seconds...", file=sys.stderr)
                    time.sleep(5)
                    continue
                raise RuntimeError(error_msg)
            
            output = result.stdout.decode("utf-8")
            
            # Strip out <think>...</think> content
            output = re.sub(r'<think>.*?</think>', '', output, flags=re.DOTALL)
            
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
    """Extract key insights from stories for a specific county or all counties."""
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


def format_county_data_section(county: str, stories_data: list, recurring_issues: list, county_issues: dict, county_summary: str) -> str:
    """Format a comprehensive data section for a specific county."""
    county_name = COUNTY_NAMES[county]
    county_dir = DATA_DIR / county
    
    section = f"""

{'='*80}
# DATA PACKAGE FOR {county_name.upper()}
{'='*80}

"""
    
    # Add county summary from county_summary_book_v2.md
    section += f"""
## COUNTY EDUCATION CONTEXT (from County Summary Book)

{county_summary}

"""
    
    # 1. CENSUS AND DEMOGRAPHIC DATA
    census_file = county_dir / f"{county}_census.json"
    census_data = load_json_file(census_file)
    section += f"""
## 1. CENSUS AND DEMOGRAPHIC DATA (2024)

```json
{json.dumps(census_data, indent=2)}
```

"""
    
    # 2. COUNTY OFFICIALS
    officials_file = county_dir / f"{county}_county_officials.json"
    officials_data = load_json_file(officials_file)
    section += f"""
## 2. COUNTY OFFICIALS AND LEADERSHIP

```json
{json.dumps(officials_data, indent=2)}
```

"""
    
    # 3. MUNICIPAL OFFICIALS
    muni_officials_file = county_dir / f"{county}_municipal_officials.json"
    muni_officials_data = load_json_file(muni_officials_file)
    section += f"""
## 3. MUNICIPAL OFFICIALS

```json
{json.dumps(muni_officials_data, indent=2)}
```

"""
    
    # 4. MUNICIPALITIES CENSUS
    muni_census_file = county_dir / f"{county}_municipalities_census.json"
    muni_census_data = load_json_file(muni_census_file)
    section += f"""
## 4. MUNICIPALITIES DEMOGRAPHIC DATA

```json
{json.dumps(muni_census_data, indent=2)}
```

"""
    
    # 5. ELECTIONS DATA
    elections_file = county_dir / f"{county}_elections.json"
    elections_data = load_json_file(elections_file)
    section += f"""
## 5. ELECTIONS DATA AND POLITICAL LANDSCAPE

```json
{json.dumps(elections_data, indent=2)}
```

"""
    
    # 6. SCHOOLS DATA
    schools_file = county_dir / f"{county}_schools.json"
    schools_data = load_json_file(schools_file)
    section += f"""
## 6. SCHOOLS AND EDUCATION DATA

```json
{json.dumps(schools_data, indent=2)}
```

"""
    
    # 7. BUDGET ANALYSIS
    budget_file = county_dir / f"{county}_budget_analysis.md"
    budget_content = load_file_content(budget_file)
    section += f"""
## 7. BUDGET AND FISCAL ANALYSIS

{budget_content}

"""
    
    # 8. RECENT MEETING MINUTES ANALYSIS
    minutes_file = county_dir / f"{county}_recent_minutes_analysis.md"
    minutes_content = load_file_content(minutes_file)
    section += f"""
## 8. RECENT MEETING MINUTES AND GOVERNANCE ANALYSIS

{minutes_content}

"""
    
    # 9. RELEVANT NEWS STORIES
    story_insights = extract_story_insights(stories_data, county)
    section += f"""
## 9. RELEVANT NEWS STORIES FOR {county_name}

**Total Stories Analyzed:** {story_insights['total_stories']}
**Date Range:** {story_insights['date_range']}

**Story Coverage by Topic:**
"""
    for topic, count in story_insights['top_topics']:
        section += f"- {topic}: {count} stories\n"
    
    section += f"""

**Sample Stories (showing titles, summaries, and key metadata):**

"""
    for i, story in enumerate(story_insights['sample_stories'], 1):
        section += f"""
### Story {i}: {story.get('title', 'Untitled')}
- **Date:** {story.get('date', 'Unknown')}
- **Author:** {story.get('author', 'Unknown')}
- **Tag:** {story.get('beatbook_tag', 'Other')}
- **Summary:** {story.get('summary', 'No summary available')}

"""
    
    # 10. COUNTY-SPECIFIC ISSUES
    if county_name in county_issues:
        issues = county_issues[county_name]
        section += f"""
## 10. TOP ISSUES SPECIFIC TO {county_name}

```json
{json.dumps(issues, indent=2)}
```

"""
    
    return section


def extract_county_summary(county_summary_content: str, county: str) -> str:
    """Extract the relevant section for a specific county from county_summary_book_v2.md."""
    county_name = COUNTY_NAMES[county]
    
    # Try to find the county section
    # Look for "# County Name" heading
    pattern = rf"# {county_name}(.*?)(?=\n# [A-Z]|\Z)"
    match = re.search(pattern, county_summary_content, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    else:
        return f"County summary for {county_name} not found in county_summary_book_v2.md"


def build_prompt() -> str:
    """Build the complete prompt with all data files in a structured format."""
    
    print("Loading base prompt...", file=sys.stderr)
    # Load the base prompt
    prompt_file = BASE_DIR / "prompt.md"
    base_prompt = load_file_content(prompt_file)
    
    print("Loading county summary book...", file=sys.stderr)
    # Load county summary book
    county_summary_file = BASE_DIR / "county_summary_book_v2.md"
    county_summary_content = load_file_content(county_summary_file)
    
    print("Loading story corpus...", file=sys.stderr)
    # Load story data
    stories_file = BASE_DIR / "beatbook_standardized_stories.json"
    stories_data = load_json_file(stories_file)
    
    print("Loading issue analysis...", file=sys.stderr)
    # Load issue summaries
    recurring_issues_file = BASE_DIR / "top_recurring_issues.json"
    recurring_issues = load_json_file(recurring_issues_file)
    
    county_issues_file = BASE_DIR / "top_issues_by_county.json"
    county_issues = load_json_file(county_issues_file)
    
    # Build the complete prompt
    full_prompt = f"""{base_prompt}

{'='*80}
{'='*80}
# COMPREHENSIVE DATA PACKAGE
{'='*80}
{'='*80}

You have been provided with an extensive dataset covering five Maryland counties on the Eastern Shore: Caroline, Dorchester, Kent, Queen Anne's, and Talbot.

The data includes:
- County education summaries with demographic, performance, and leadership data
- Census and demographic information (2024)
- County and municipal officials
- Elections results and political data
- School performance and enrollment data
- Budget and fiscal analysis
- Recent meeting minutes analysis
- A corpus of {len(stories_data) if isinstance(stories_data, list) else 0} local news stories
- Identified recurring issues across all counties
- County-specific issue analysis

---

# PART 1: REGIONAL CONTEXT AND CROSS-COUNTY ISSUES

## Cross-County Issue Analysis

The following issues recur across multiple counties in the region:

```json
{json.dumps(recurring_issues, indent=2)}
```

---

"""
    
    # Add county-specific data packages
    print("Building county data packages...", file=sys.stderr)
    for county in COUNTIES:
        print(f"  - Processing {COUNTY_NAMES[county]}...", file=sys.stderr)
        county_summary = extract_county_summary(county_summary_content, county)
        county_section = format_county_data_section(county, stories_data, recurring_issues, county_issues, county_summary)
        full_prompt += county_section
    
    full_prompt += f"""

{'='*80}
{'='*80}
# YOUR TASK: GENERATE THE COMPLETE BEATBOOK (VERSION 2)
{'='*80}
{'='*80}

Using ALL the data provided above, produce a comprehensive five-county government beatbook with the following VERSION 2 specifications:

**STRUCTURE CHANGES FOR VERSION 2:**

1. **Simplified Section Structure** for each county (10 parts instead of 12):
   - Narrative Summary: "The State of the County"
   - Current Power Structure: Who Runs the County?
   - Civic Infrastructure & Demographics (Data Summary)
   - Elections & Political Landscape
   - Schools & Education Landscape
   - Budget & Fiscal Priorities
   - Key Local Government Issues to Watch
   - Municipal Profiles (Reference Section)
   - Stakeholder Map: Informal Power Centers
   - Red Flags & Accountability Priorities
   
   **ELIMINATED SECTIONS:**
   - Story Playbook for a New Reporter (removed)
   - Appendices with contact points (removed)

2. **Key Sources Section - TABLE FORMAT:**
   - Create a section called "Key Sources" near the end of each county
   - Use markdown tables with columns: Name | Position | Area of Influence | Notes
   - Group sources by category with H3 headings: County Commissioners/Council, Municipal Leadership, Judicial & Constitutional Offices, Department Heads
   - Include actual names, titles, and brief descriptions from the data
   - Style should be similar to beatbook_v2_enhanced.md's Key Sources section but in table format
   - Example format:
   
   ```markdown
   ### County Commissioners
   
   | Name | Position | Area of Influence | Notes |
   |------|----------|-------------------|-------|
   | John Smith | Commissioner (D) | Budget, Planning | Chair of Budget Committee |
   ```

3. **Key Datasets & Sources Section - ENHANCED FORMAT:**
   - Create a final section after all counties called "Key Documents, Records & Public Resources"
   - Use H3 headings for categories (Budget & Finance Records, Meeting Minutes & Governance, Elections Data, etc.)
   - Under each heading, use bulleted lists with document names and descriptions
   - Match the style from beatbook_v2_enhanced.md's "Key Documents & Resources" section
   - Include both county-level and state-level resources
   - Example format:
   
   ```markdown
   ### Budget & Finance Records
   - **Caroline County FY2026 Budget** – Details revenue sources, expenditure allocations, and capital projects; county-level.
   - **Maryland State Budget Portal** – Central repository for statewide funding formulas and allocations; state-level.
   ```

**TONE AND STYLE - PROFESSIONAL JOURNALISM:**
   - Write in a professional, analytical newsroom style
   - Use formal, clear prose appropriate for a beat reference guide
   - Be narrative-driven but authoritative
   - Avoid casual language, contractions, or conversational tone
   - Think "deep briefing memo" not "friendly chat"
   - Every assertion should be grounded in the provided data

**NARRATIVE DEPTH REQUIREMENTS:**
   
   **For Section 1 (Narrative Summary):**
   - Write 3-5 substantial paragraphs (150-200 words each)
   - Identify and explain the top 5-8 issues shaping the county
   - Synthesize trends from meeting minutes AND news stories
   - Explain the political and policy context behind each issue
   - Connect local dynamics to state/federal pressures
   - Identify emerging patterns and power struggles

   **For Section 7 (Key Local Government Issues to Watch):**
   - Present 3-5 major issues as H3 headings
   - For EACH issue, write **3 full paragraphs** (minimum 120 words per paragraph):
     * **Paragraph 1:** Describe the issue in detail - what is happening, who is involved, what decisions are pending
     * **Paragraph 2:** Explain why it matters - fiscal implications, quality of life impacts, political significance, precedent-setting nature
     * **Paragraph 3:** Analyze the tensions and stakeholders - who supports/opposes, what's at stake, what accountability questions arise, what story angles exist
   - Ground each issue in specific meeting minutes, budget items, or news stories
   - Use concrete examples, dates, dollar amounts, vote counts, official names

**Use REAL DATA Throughout:**
   - Quote actual numbers from census data (population, income, poverty rates)
   - Name actual officials with their exact titles and party affiliations
   - Reference actual election results with vote percentages and turnout
   - Cite actual school performance metrics (STAR ratings, enrollment, test scores)
   - Reference actual budget figures (revenues, expenditures, debt, reserves)
   - Quote from actual meeting minutes (decisions, discussions, votes)
   - Reference actual news stories by describing their content and significance

**Analytical Requirements:**
   - Connect patterns across multiple data sources
   - Explain WHY issues matter (not just what is happening)
   - Identify power dynamics, alliances, and tensions
   - Highlight governance red flags and accountability gaps
   - Provide context for political and policy conflicts

**Process Counties in This Order:**
   - Caroline County
   - Dorchester County
   - Kent County
   - Queen Anne's County
   - Talbot County

**REMEMBER:** This beatbook is a professional reference tool for a reporter covering local government. Every section should be deeply reported, analytically rich, and grounded in the extensive data provided. Write with authority and precision.

Begin now with Caroline County, Section 1: Narrative Summary - "The State of the County".
"""
    
    return full_prompt


def generate_beatbook():
    """Generate the beatbook using LLM via subprocess."""
    
    print("\n" + "="*80, file=sys.stderr)
    print("FIVE-COUNTY LOCAL GOVERNMENT BEATBOOK GENERATOR (VERSION 2)", file=sys.stderr)
    print("="*80 + "\n", file=sys.stderr)
    
    print("Step 1: Building comprehensive prompt...", file=sys.stderr)
    prompt = build_prompt()
    
    print(f"\nStep 2: Prompt prepared", file=sys.stderr)
    print(f"  - Prompt size: {len(prompt):,} characters", file=sys.stderr)
    print(f"  - Model: {MODEL}", file=sys.stderr)
    
    # Save prompt for debugging
    prompt_debug_file = BASE_DIR / "beatbook_prompt_debug_v2.txt"
    with open(prompt_debug_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    print(f"  - Debug prompt saved to: {prompt_debug_file}", file=sys.stderr)
    
    print(f"\nStep 3: Calling LLM... (this may take several minutes)", file=sys.stderr)
    print("  - Processing five counties with 10-part structure each", file=sys.stderr)
    print("  - Simplified format with table-based sources", file=sys.stderr)
    print("  - Enhanced documents section", file=sys.stderr)
    print("  - This is a large task, please be patient...\n", file=sys.stderr)
    
    try:
        output = run_llm(prompt)
        
        # Build the final output with proper header and TOC
        final_output = """# Five-County Local Government Beatbook

## Caroline, Dorchester, Kent, Queen Anne's, and Talbot Counties

*A comprehensive reference guide for local government reporters*

*Generated: November 2025*

*Model: groq/openai/gpt-oss-120b*

---

## Table of Contents

- [Caroline County](#caroline-county)
- [Dorchester County](#dorchester-county)
- [Kent County](#kent-county)
- [Queen Anne's County](#queen-annes-county)
- [Talbot County](#talbot-county)
- [Key Documents, Records & Public Resources](#key-documents-records--public-resources)

---

"""
        final_output += output
        
        # Save the output
        output_file = BASE_DIR / "beatbook_v2.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_output)
        
        print(f"\n" + "="*80, file=sys.stderr)
        print(f"✓ BEATBOOK V2 GENERATED SUCCESSFULLY!", file=sys.stderr)
        print(f"="*80, file=sys.stderr)
        print(f"\nOutput saved to: {output_file}", file=sys.stderr)
        print(f"Output size: {len(final_output):,} characters", file=sys.stderr)
        print(f"\nYou can now review the beatbook at:", file=sys.stderr)
        print(f"  {output_file}\n", file=sys.stderr)
        
        return 0
        
    except Exception as e:
        print(f"\n" + "="*80, file=sys.stderr)
        print(f"✗ ERROR GENERATING BEATBOOK", file=sys.stderr)
        print(f"="*80, file=sys.stderr)
        print(f"\nError: {e}", file=sys.stderr)
        print(f"\nCheck the debug prompt file at:", file=sys.stderr)
        print(f"  {prompt_debug_file}\n", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(generate_beatbook())
