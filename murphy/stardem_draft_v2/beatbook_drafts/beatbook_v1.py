#!/usr/bin/env python3
"""
Eastern Shore Education Beatbook Generator

Uses Groq's gpt-oss-120b model via the `llm` CLI tool to generate
a comprehensive education beatbook for Eastern Shore counties.

Inputs (expected in the working directory by default):

  - County budget writeups (Markdown):
      caroline_education_budget.md
      dorchester_education_budget.md
      kent_education_budget.md
      queen_annes_education_budget.md
      talbot_education_budget.md

  - County profile / data summaries (JSON):
      caroline_summary.json
      dorchester_summary.json
      kent_summary.json
      queen_annes_summary.json
      talbot_summary.json

    Each JSON file should have a top-level object keyed by the
    county name (e.g. "Caroline", "Dorchester", etc.) with
    demographics, district, outcomes, discipline data, etc.
    (matching the structure of your existing summary JSONs).

  - Education news stories (JSON; one file for all five counties):
      education_stories.json

    Expected structure:
      [
        {
          "title": "...",
          "date": "YYYY-MM-DD",
          "author": "...",
          "content": "...",
          "source": "Star Democrat",
          "url": "https://...",
          "counties": ["Caroline", "Talbot"],
          "topics": ["budget", "blueprint", "discipline"],
          ...
        },
        ...
      ]

    Only `title`, `date`, `content`, `source`, and some way of
    associating a story with a county are strictly required.
    The script will try "counties" first, then fall back to
    text search on county name in the content or title.

Requirements:

  - `llm` CLI tool must be installed and configured with Groq access
  - Model: groq/openai/gpt-oss-120b

You can override file paths and model name with CLI flags.

Example usage:

  python3 beatbook_v1.py \
      --stories-file refined_beatbook_stories.json \
      --output-file education_beatbook.md

"""

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ----------------------------
# Configuration
# ----------------------------

BASE_DIR = Path(__file__).parent

# Updated to match actual directory structure: things_to_use/[county]/
DEFAULT_BUDGET_FILES = {
    "Caroline": BASE_DIR / "things_to_use" / "caroline" / "caroline_budget_analysis.md",
    "Dorchester": BASE_DIR / "things_to_use" / "dorchester" / "dorchester_budget_analysis.md",
    "Kent": BASE_DIR / "things_to_use" / "kent" / "kent_budget_analysis.md",
    "Queen Anne's": BASE_DIR / "things_to_use" / "queen_annes" / "queen_annes_budget_analysis.md",
    "Talbot": BASE_DIR / "things_to_use" / "talbot" / "talbot_budget_analysis.md",
}

# Blueprint analysis files from things_to_use/[county]/
DEFAULT_BLUEPRINT_FILES = {
    "Caroline": BASE_DIR / "things_to_use" / "caroline" / "caroline_blueprint_summary.md",
    "Dorchester": BASE_DIR / "things_to_use" / "dorchester" / "dorchester_blueprint_summary.md",
    "Kent": BASE_DIR / "things_to_use" / "kent" / "kent_blueprint_summary.md",
    "Queen Anne's": BASE_DIR / "things_to_use" / "queen_annes" / "queen_annes_blueprint_summary.md",
    "Talbot": BASE_DIR / "things_to_use" / "talbot" / "talbot_blueprint_summary.md",
}

# County data files from county_files/[county]/
DEFAULT_SUMMARY_FILES = {
    "Caroline": BASE_DIR / "county_files" / "caroline" / "caroline_county_summary.json",
    "Dorchester": BASE_DIR / "county_files" / "dorchester" / "dorchester_county_summary.json",
    "Kent": BASE_DIR / "county_files" / "kent" / "kent_county_summary.json",
    "Queen Anne's": BASE_DIR / "county_files" / "queen_annes" / "queen_annes_county_summary.json",
    "Talbot": BASE_DIR / "county_files" / "talbot" / "talbot_county_summary.json",
}

DEFAULT_STORIES_FILE = BASE_DIR / "refined_beatbook_stories.json"
DEFAULT_OUTPUT_FILE = BASE_DIR / "education_beatbook.md"

# Groq model string (you can tweak this if your deployment uses a different name)
LLM_MODEL = "groq/openai/gpt-oss-120b"

# How many stories to include per county to avoid blowing token limits
MAX_STORIES_PER_COUNTY = 30

# Major education topics for analysis
MAJOR_TOPICS = {
    'School Board/Policy': ['board', 'policy', 'meeting', 'vote', 'decision', 'superintendent', 'board of education', 'governance'],
    'Curriculum/Programs': ['curriculum', 'program', 'course', 'instruction', 'literacy', 'math', 'stem', 'science', 'reading'],
    'Staffing': ['teacher', 'staff', 'hiring', 'retention', 'recruitment', 'shortage', 'personnel', 'educator', 'vacancy'],
    'Budget/Funding': ['budget', 'funding', 'million', 'cost', 'expense', 'financial', 'money', 'appropriation', 'blueprint'],
    'Achievement/Scores': ['mcap', 'test score', 'proficiency', 'assessment', 'testing', 'achievement', 'performance', 'state test'],
    'Equity': ['equity', 'diversity', 'race', 'disparity', 'gap', 'minority', 'demographic', 'underserved'],
    'Construction/Facilities': ['construction', 'renovation', 'building', 'facility', 'infrastructure', 'repair', 'auditorium', 'hvac', 'maintenance'],
    'Behavior/Discipline': ['discipline', 'suspension', 'behavior', 'conduct', 'fighting', 'cellphone', 'expulsion', 'bullying'],
    'Safety': ['safety', 'security', 'lockdown', 'threat', 'violence', 'drill', 'window glazing', 'emergency'],
}


# ----------------------------
# File loading helpers
# ----------------------------

def load_text_file(path: Path) -> Optional[str]:
    """Return file contents as text or None if missing."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"[WARN] Missing text file: {path}")
        return None


def load_json_file(path: Path) -> Optional[Any]:
    """Return parsed JSON or None if missing/bad."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[WARN] Missing JSON file: {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"[WARN] Failed to parse JSON {path}: {e}")
        return None


def load_stories(path: Path) -> List[Dict[str, Any]]:
    """Load the stories JSON; returns a list of story dicts (or empty list)."""
    data = load_json_file(path)
    if isinstance(data, list):
        # Filter for Education topic only
        edu_stories = [s for s in data if s.get('llm_classification', {}).get('topic') == 'Education']
        print(f"[INFO] Loaded {len(edu_stories)} education stories out of {len(data)} total stories")
        return edu_stories
    print(f"[WARN] Stories file {path} is not a JSON list; got {type(data)}")
    return []


# ----------------------------
# Story selection / grouping
# ----------------------------

def story_matches_county(story: Dict[str, Any], county_name: str) -> bool:
    """
    Heuristics to decide if a story belongs to a county.

    - If story has a 'counties' list, check for case-insensitive match.
    - Otherwise, search for the county name in title or content.
    """
    counties = story.get("counties") or story.get("counties_mentioned")
    if isinstance(counties, list):
        for c in counties:
            if isinstance(c, str) and county_name.lower() in c.lower():
                return True

    title = (story.get("title") or "").lower()
    content = (story.get("content") or "").lower()
    if county_name.lower() in title or county_name.lower() in content:
        return True

    # Edge case: Queen Anne's might appear as "Queen Annes" or "Queen Anne"
    if county_name == "Queen Anne's":
        variants = ["queen anne", "queen annes", "queen anne's"]
        if any(v in title or v in content for v in variants):
            return True

    return False


def group_stories_by_county(
    stories: List[Dict[str, Any]],
    counties: List[str],
    max_per_county: int = MAX_STORIES_PER_COUNTY,
) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {c: [] for c in counties}
    for story in stories:
        for county in counties:
            if story_matches_county(story, county):
                if len(grouped[county]) < max_per_county:
                    grouped[county].append(story)
                break  # don't double-assign
    return grouped


def categorize_story_topics(story: Dict[str, Any]) -> List[str]:
    """
    Categorize a story by the major education topics it addresses.
    Returns a list of matching topic names.
    """
    title = (story.get("title") or "").lower()
    content = (story.get("content") or "").lower()
    summary = (story.get("summary") or "").lower()
    combined = f"{title} {content} {summary}"
    
    matched_topics = []
    for topic, keywords in MAJOR_TOPICS.items():
        if any(keyword in combined for keyword in keywords):
            matched_topics.append(topic)
    
    return matched_topics


def format_story_brief(story: Dict[str, Any]) -> str:
    """
    Turn a story into a compact text block the LLM can digest easily.
    Includes topic categorization and key metadata from refined_beatbook_stories.json.
    """
    title = story.get("title") or "Untitled story"
    date = story.get("date") or "Unknown date"
    author = story.get("author") or "Unknown author"
    source = story.get("source") or story.get("content_source") or "Star Democrat"
    url = story.get("url") or story.get("docref") or ""
    
    # Get LLM-generated summary if available, otherwise use content
    summary = story.get("summary") or ""
    content = (story.get("content") or "").strip()
    
    # Use summary preferentially, fall back to content
    main_text = summary if summary else content
    if len(main_text) > 2400:
        main_text = main_text[:2400] + " [...]"
    
    # Get key metadata
    key_people = story.get("key_people", [])
    key_orgs = story.get("key_organizations", [])
    key_establishments = story.get("key_establishments", [])
    
    # Categorize by major topics
    topics = categorize_story_topics(story)
    
    parts = [
        f"Title: {title}",
        f"Date: {date}",
        f"Author: {author}",
        f"Source: {source}",
    ]
    if url:
        parts.append(f"Reference: {url}")
    
    if topics:
        parts.append(f"Topics: {', '.join(topics)}")
    
    if key_people:
        parts.append(f"Key people: {'; '.join(key_people[:3])}")
    
    if key_orgs:
        parts.append(f"Organizations: {'; '.join(key_orgs[:3])}")
    
    if key_establishments:
        parts.append(f"Schools/Establishments: {'; '.join(key_establishments[:3])}")
    
    parts.append("\nStory summary/excerpt:")
    parts.append(main_text)
    
    return "\n".join(parts)


# ----------------------------
# Prompt construction
# ----------------------------

def analyze_stories_by_topic(stories: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group stories by the major education topics they address.
    """
    topic_stories: Dict[str, List[Dict[str, Any]]] = {topic: [] for topic in MAJOR_TOPICS.keys()}
    
    for story in stories:
        topics = categorize_story_topics(story)
        for topic in topics:
            if topic in topic_stories:
                topic_stories[topic].append(story)
    
    return topic_stories


def build_county_context(
    county_name: str,
    budget_md: Optional[str],
    blueprint_md: Optional[str],
    summary_json: Optional[Dict[str, Any]],
    stories: List[Dict[str, Any]],
) -> str:
    """
    Build a county-specific context block for the LLM.
    """
    lines: List[str] = []
    lines.append(f"=== COUNTY: {county_name.upper()} ===")

    if budget_md:
        lines.append("\n[BUDGET ANALYSIS / CONTEXT]")
        lines.append(budget_md.strip())
    
    if blueprint_md:
        lines.append("\n[BLUEPRINT FOR MARYLAND'S FUTURE ANALYSIS]")
        lines.append(blueprint_md.strip())

    if summary_json:
        lines.append("\n[PROFILE DATA JSON]")
        # The JSON may have multiple counties; prefer the key matching the county
        if county_name in summary_json:
            lines.append(json.dumps(summary_json[county_name], indent=2))
        else:
            lines.append(json.dumps(summary_json, indent=2))

    if stories:
        # Analyze stories by topic
        topic_analysis = analyze_stories_by_topic(stories)
        
        lines.append("\n[EDUCATION STORY ANALYSIS BY MAJOR TOPIC]")
        lines.append("\nTopic breakdown:")
        for topic, topic_stories in topic_analysis.items():
            if topic_stories:
                lines.append(f"  - {topic}: {len(topic_stories)} stories")
        
        lines.append("\n[RECENT EDUCATION NEWS STORIES]")
        for idx, story in enumerate(stories, 1):
            lines.append(f"\n--- Story {idx} ---")
            lines.append(format_story_brief(story))

    return "\n".join(lines)


SYSTEM_PROMPT = """
You are an education-beat editor creating a deeply reported beat book
for a new reporter covering K-12 education in five Eastern Shore
Maryland counties: Caroline, Dorchester, Kent, Queen Anne's, and Talbot.

You will be given, for each county:
- Budget analysis text highlighting how much of the county budget goes to
  education, capital vs. operating, and fiscal sustainability concerns.
- Blueprint for Maryland's Future analysis showing implementation progress
  and challenges.
- Structured profile data (demographics, district leadership, test scores,
  suspensions/discipline, etc.).
- A curated set of recent local education news stories tagged to that county,
  pre-analyzed and categorized by 9 major education topics:
  
  1. **School Board/Policy** - governance, decisions, board meetings, superintendent
  2. **Curriculum/Programs** - instruction, literacy, STEM, course offerings
  3. **Staffing** - teacher hiring, retention, shortages, personnel
  4. **Budget/Funding** - fiscal matters, Blueprint funding, appropriations
  5. **Achievement/Scores** - MCAP, test results, proficiency, performance
  6. **Equity** - racial/demographic gaps, diversity, underserved populations
  7. **Construction/Facilities** - buildings, renovations, infrastructure
  8. **Behavior/Discipline** - suspensions, conduct, bullying
  9. **Safety** - security, threats, emergency preparedness

Your job is to synthesize these into a single MARKDOWN document that a
reporter could read cover-to-cover and walk into the beat ready to work.

ABSOLUTE REQUIREMENTS FOR THE OUTPUT:

1. The entire document must be valid Markdown.
2. Organize by county, with a short regional overview at the top.
3. Within each county section, write primarily in NARRATIVE PARAGRAPHS,
   not bullet lists, **except** for one short "Sources, documents & links"
   subsection which may be a bulleted list.
4. Focus on CURRENT AND EMERGING ISSUES using the 9 MAJOR TOPIC FRAMEWORK:
   - For each county, analyze the news coverage across the 9 major topics:
     School Board/Policy, Curriculum/Programs, Staffing, Budget/Funding,
     Achievement/Scores, Equity, Construction/Facilities, Behavior/Discipline,
     and Safety.
   - Identify which topics dominate the news (high story count) and which are
     underreported (low story count but important based on data).
   - Synthesize patterns: How do budget pressures connect to staffing issues?
     Do discipline trends correlate with equity gaps? Are construction projects
     driven by safety concerns or enrollment shifts?
   - Flag any obvious accountability questions or contradictions that a
     reporter should pursue.
5. Include concrete details from the inputs (numbers, names, dates) but DO
   NOT invent data. If something is unclear or missing, say what you would
   want to find out, not a made-up fact.

MANDATORY STRUCTURE:

# Eastern Shore Education Beatbook

## How to use this beatbook
(Brief paragraph explaining how a new reporter should use this document:
what to read first, how to prepare for meetings, how to develop sources.)

## Regional overview: Five-county picture
- 2–4 paragraphs narratively comparing the five counties:
  - How much of each county budget goes to education
  - Shared pressures (Blueprint mandates, reserve drawdowns, staffing,
    capital needs, discipline trends)
  - Key differences (richer vs poorer counties, small vs large districts,
    college access, broadband, etc.)

Then, for EACH COUNTY (Caroline, Dorchester, Kent, Queen Anne's, Talbot),
include a section using this rough pattern. You may adapt the subheadings,
but keep the content:

## [County Name] County

### Big picture: What this beat feels like on the ground
Narrative description of the county’s schools, communities, and politics.
What does it feel like to cover this system day-to-day? Who is in charge?
What is the relationship between the school system, county commissioners,
and the public?

### Budget, Blueprint & fiscal stress
Narrative explanation of:
- How much of the county budget goes to education.
- Whether the county is relying on reserves, tax increases, or cuts.
- How Blueprint for Education mandates show up in this county
  (or what questions the reporter should ask).

### Student outcomes, equity & discipline
Narrative synthesis of:
- Test score patterns by level (elementary, middle, high school)
- Any obvious equity gaps by race, poverty, disability
- Discipline/suspension patterns and what they might signal

### Top current issues & storylines (organized by major topics)
2–5 paragraphs analyzing the county's education landscape through the
9 major topic areas. Focus on:

- **School Board/Policy**: Board dynamics, governance issues, major decisions
- **Curriculum/Programs**: Instructional initiatives, program changes
- **Staffing**: Teacher recruitment/retention, vacancies, workforce challenges
- **Budget/Funding**: Fiscal pressures, Blueprint mandates, funding gaps
- **Achievement/Scores**: MCAP performance, proficiency trends, achievement gaps
- **Equity**: Demographic disparities, diversity issues, underserved populations
- **Construction/Facilities**: Building projects, infrastructure needs, capital plans
- **Behavior/Discipline**: Discipline trends, suspension patterns, student conduct
- **Safety**: Security measures, threat responses, emergency preparedness

Highlight which topics dominate recent coverage and which deserve more
reporting attention. Connect dots between topics (e.g., how budget cuts
affect staffing, how discipline policies impact equity).

### Power map: Who matters and how to cover them
Narrative description of:
- Key decision-makers (superintendent, board members, union leaders,
  frequent public commenters, key community organizations).
- How and when the board meets; what a reporter should pay attention to.
- Any underlying political or racial tensions that shape education debates.

### Sources, documents & links (bulleted list allowed)
- 5–12 bullet points listing:
  - Websites (district, state, budget portals, board agendas, data dashboards)
  - Key recurring sources (advocacy groups, parent coalitions, teachers union)
  - Data sources (MCAP dashboards, MSDE data, discipline reports, ESSA plans)
  - Any particularly useful recurring documents (line-item budgets,
    capital improvement plans, enrollment projections, etc.)

### Questions to walk in with
Close each county section with 1–2 paragraphs of “starter questions” the
new reporter should be asking officials, parents, and students, based on
gaps or tensions you see in the inputs.

IMPORTANT:
- Keep the tone grounded, skeptical, and practical for a working reporter.
- Do NOT write like a press release. Surface contradictions, missing data,
  and places where officials’ claims might not match the numbers.
"""

def build_master_prompt(
    county_contexts: Dict[str, str],
) -> str:
    """
    Flatten all county context into a single user prompt for the LLM.
    """
    lines: List[str] = []
    lines.append(
        "You are given budget analysis, profile data, and recent stories "
        "for several Eastern Shore counties. Use them to build the beatbook."
    )
    lines.append("\n===== INPUT MATERIALS BY COUNTY =====\n")
    for county, ctx in county_contexts.items():
        lines.append(ctx)
        lines.append("\n\n")
    return "\n".join(lines)


# ----------------------------
# LLM call via llm CLI tool
# ----------------------------

def call_llm(
    system_prompt: str,
    user_prompt: str,
    model: str = LLM_MODEL,
) -> str:
    """
    Call LLM using the `llm` CLI tool with system and user prompts.
    Returns the generated text response.
    """
    # Combine system and user prompts
    full_prompt = f"{system_prompt.strip()}\n\n{user_prompt.strip()}"
    
    try:
        result = subprocess.run(
            ["llm", "-m", model],
            input=full_prompt.encode(),
            capture_output=True,
            check=True,
            timeout=300  # 5 minute timeout for long generation
        )
        
        response_text = result.stdout.decode()
        return response_text.strip()
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else "No error message"
        raise RuntimeError(f"LLM call failed: {error_msg}")
    except subprocess.TimeoutExpired:
        raise RuntimeError("LLM call timed out after 300 seconds")
    except Exception as e:
        raise RuntimeError(f"Unexpected error calling LLM: {e}")


# ----------------------------
# Main pipeline
# ----------------------------

def generate_beatbook(
    stories_file: Path,
    output_file: Path,
    model: str = LLM_MODEL,
) -> None:
    # 1. Load all stories and group by county
    counties = list(DEFAULT_BUDGET_FILES.keys())
    all_stories = load_stories(stories_file)
    grouped_stories = group_stories_by_county(all_stories, counties)
    
    # Print topic analysis summary
    print("\n[INFO] Story analysis by major topics:")
    all_topic_counts = {topic: 0 for topic in MAJOR_TOPICS.keys()}
    for county, stories in grouped_stories.items():
        topic_analysis = analyze_stories_by_topic(stories)
        print(f"\n  {county}:")
        for topic, topic_stories in topic_analysis.items():
            count = len(topic_stories)
            all_topic_counts[topic] += count
            if count > 0:
                print(f"    - {topic}: {count} stories")
    
    print("\n  Overall topic distribution:")
    for topic, count in sorted(all_topic_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"    - {topic}: {count} stories")

    # 2. Build per-county context
    county_contexts: Dict[str, str] = {}
    for county in counties:
        budget_path = DEFAULT_BUDGET_FILES[county]
        blueprint_path = DEFAULT_BLUEPRINT_FILES[county]
        summary_path = DEFAULT_SUMMARY_FILES[county]

        budget_md = load_text_file(budget_path)
        blueprint_md = load_text_file(blueprint_path)
        summary_json = load_json_file(summary_path)

        ctx = build_county_context(
            county_name=county,
            budget_md=budget_md,
            blueprint_md=blueprint_md,
            summary_json=summary_json if isinstance(summary_json, dict) else None,
            stories=grouped_stories.get(county, []),
        )
        county_contexts[county] = ctx

    # 3. Build master user prompt
    user_prompt = build_master_prompt(county_contexts)

    # 4. Call LLM
    print("[INFO] Calling LLM to generate beatbook...")
    print(f"[INFO] Using model: {model}")
    beatbook_md = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        model=model,
    )

    # 5. Save output
    output_file.write_text(beatbook_md, encoding="utf-8")
    print(f"[INFO] Beatbook written to: {output_file}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an Eastern Shore education beatbook using Groq gpt-oss-120b."
    )
    parser.add_argument(
        "--stories-file",
        type=Path,
        default=DEFAULT_STORIES_FILE,
        help=f"Path to education stories JSON (default: {DEFAULT_STORIES_FILE})",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output Markdown file (default: {DEFAULT_OUTPUT_FILE})",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=LLM_MODEL,
        help=f"Model name (default: {LLM_MODEL})",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    generate_beatbook(
        stories_file=args.stories_file,
        output_file=args.output_file,
        model=args.model,
    )
