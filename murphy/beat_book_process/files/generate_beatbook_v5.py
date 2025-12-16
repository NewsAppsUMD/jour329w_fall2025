#!/usr/bin/env python3
"""
Generate a five-county local government beatbook using LLM (VERSION 4).

VERSION 4 IMPROVEMENTS:
- Pre-digest all data into narrative fact blocks (no raw JSON in prompt)
- Generate iteratively: one county at a time, one section at a time
- Pre-build Key Sources tables before LLM sees them
- Dramatically reduced prompt size (~20K tokens vs 190K)
- Specific, measurable requirements for each section
- Immediate validation and error catching
"""

import subprocess
import json
import sys
import re
import time
from pathlib import Path
from collections import Counter
from typing import Dict, List, Any

# Model to use
MODEL = "groq/openai/gpt-oss-120b"

# Base directory
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "scraped_county_data"

# Counties to process (order matters)
COUNTIES = ["caroline", "dorchester", "kent", "queen_annes", "talbot"]

# County name mapping
COUNTY_NAMES = {
    "caroline": "Caroline County",
    "dorchester": "Dorchester County",
    "kent": "Kent County",
    "queen_annes": "Queen Anne's County",
    "talbot": "Talbot County"
}

# Output file
OUTPUT_FILE = BASE_DIR / "beatbook_v5.md"


def load_file_content(filepath: Path) -> str:
    """Load content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Warning: Could not load {filepath}: {e}", file=sys.stderr)
        return ""


def load_json_file(filepath: Path) -> Any:
    """Load JSON content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load {filepath}: {e}", file=sys.stderr)
        return {}


def run_llm(prompt: str, max_retries: int = 3) -> str:
    """Run LLM through subprocess with retry logic."""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ["llm", "-m", MODEL],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=300
            )

            if result.returncode != 0:
                error_msg = result.stderr.decode("utf-8")
                print(f"  Attempt {attempt + 1} failed: {error_msg}", file=sys.stderr)
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
                raise RuntimeError(error_msg)

            output = result.stdout.decode("utf-8")
            # Strip <think> tags if present
            output = re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL)
            return output.strip()

        except subprocess.TimeoutExpired:
            if attempt < max_retries - 1:
                print(f"  Timeout, retrying...", file=sys.stderr)
                time.sleep(5)
                continue
            raise RuntimeError("LLM request timed out")
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Error: {e}, retrying...", file=sys.stderr)
                time.sleep(5)
                continue
            raise

    raise RuntimeError("Failed after maximum retries")


def build_county_facts_block(county: str) -> str:
    """Build a clean facts block from county data."""
    
    county_name = COUNTY_NAMES[county]
    county_dir = DATA_DIR / county
    
    # Load data files
    census_data = load_json_file(county_dir / f"{county}_census.json")
    officials_data = load_json_file(county_dir / f"{county}_county_officials.json")
    elections_data = load_json_file(county_dir / f"{county}_elections.json")
    muni_data = load_json_file(county_dir / f"{county}_municipalities_census.json")
    
    # Extract census facts
    census_api = census_data.get("census_api_data", {})
    pop_data = census_api.get("population", {})
    econ_data = census_api.get("economics", {})
    race_data = census_api.get("race_ethnicity", {})
    housing_data = census_api.get("housing", {})
    enhanced = census_api.get("enhanced", {})
    poverty_data = enhanced.get("poverty", {})
    afford_data = enhanced.get("housing_affordability", {})
    broadband_data = enhanced.get("broadband_access", {})
    
    facts = f"""
## VERIFIED FACTS: {county_name.upper()}

### Demographics (U.S. Census Bureau, 2025)
- **Total Population**: {pop_data.get('total', 'N/A'):,}
- **Median Age**: {pop_data.get('median_age', 'N/A')}
- **Racial Composition**: 
  - White: {race_data.get('white_alone', 'N/A'):,} ({100*race_data.get('white_alone', 0)/max(pop_data.get('total', 1), 1):.1f}%)
  - Black: {race_data.get('black_alone', 'N/A'):,} ({100*race_data.get('black_alone', 0)/max(pop_data.get('total', 1), 1):.1f}%)
  - Hispanic/Latino: {race_data.get('hispanic_latino', 'N/A'):,} ({100*race_data.get('hispanic_latino', 0)/max(pop_data.get('total', 1), 1):.1f}%)

### Economics
- **Median Household Income**: ${econ_data.get('median_household_income', 'N/A'):,}
- **Median Home Value**: ${econ_data.get('median_home_value', 'N/A'):,}
- **Poverty Rate**: {poverty_data.get('poverty_rate', 'N/A')}% ({poverty_data.get('people_in_poverty', 'N/A'):,} people)
- **Unemployment**: {econ_data.get('unemployed', 'N/A'):,} (labor force: {econ_data.get('labor_force', 'N/A'):,})

### Housing
- **Total Housing Units**: {housing_data.get('total_units', 'N/A'):,}
- **Homeownership Rate**: {afford_data.get('homeownership_rate', 'N/A')}%
- **Renters Cost-Burdened (≥30%)**: {afford_data.get('renters_cost_burdened_30plus', 'N/A'):,} ({afford_data.get('renters_cost_burdened_30plus_pct', 'N/A')}%)
- **Broadband Access**: {broadband_data.get('with_broadband', 'N/A'):,} of {broadband_data.get('total_households', 'N/A'):,} households ({broadband_data.get('broadband_pct', 'N/A')}%)
"""

    # Add county officials
    facts += "\n### County Leadership\n"
    leg_branch = officials_data.get("county_officials", {}).get("legislative_branch", [])
    if leg_branch:
        for official in leg_branch:
            name = official.get("name", "")
            title = official.get("title", "")
            party = official.get("party", "")
            selection = official.get("selection_method", "")
            if name and title:
                party_str = f" ({party})" if party else ""
                selection_str = f" — {selection}" if selection else ""
                facts += f"- **{name}**: {title}{party_str}{selection_str}\n"
    else:
        facts += "- No county officials data available\n"
    
    # Add judicial
    jud_branch = officials_data.get("county_officials", {}).get("judicial_branch", [])
    if jud_branch:
        facts += "\n### Judicial Officials\n"
        for judge in jud_branch:
            name = judge.get("name", "")
            if name:
                facts += f"- **{name}**: Judge\n"
    
    # Add voter registration
    voter_reg = elections_data.get("voter_registration", {})
    facts += f"""
### Voter Registration
- **Total Registered**: {voter_reg.get('total_registered', 'N/A')}
- **Party Split**: Democrat {voter_reg.get('democrat', 'N/A')}, Republican {voter_reg.get('republican', 'N/A')}, Unaffiliated {voter_reg.get('unaffiliated', 'N/A')}
"""
    
    # Add recent elections
    recent = elections_data.get("recent_elections", [])
    if recent:
        facts += "\n### Recent Elections\n"
        for election in recent[:2]:  # Just top 2
            elec_name = election.get("election", "")
            results = election.get("results", {})
            turnout = election.get("turnout", "N/A")
            facts += f"- **{elec_name}**: "
            
            # Format results
            result_parts = []
            for key, val in results.items():
                if key not in ["total_votes", "other"] and val:
                    # Parse candidate name from key
                    parts = key.split("_")
                    if len(parts) >= 2:
                        candidate = parts[0].title()
                        result_parts.append(f"{candidate} {val}")
            
            facts += ", ".join(result_parts)
            facts += f" (turnout {turnout})\n"
    
    # Add municipalities
    munis = muni_data.get("municipalities", [])
    if munis:
        facts += f"\n### Municipalities ({len(munis)} incorporated towns)\n"
        # Sort by population
        munis_sorted = sorted(munis, key=lambda x: x.get("population", {}).get("total", 0), reverse=True)
        for muni in munis_sorted[:5]:  # Top 5 only
            place_name = muni.get("place_name", "")
            pop = muni.get("population", {}).get("total", "N/A")
            income = muni.get("economics", {}).get("median_household_income")
            if place_name:
                income_str = f", median income ${income:,}" if income else ""
                facts += f"- **{place_name}**: pop. {pop:,}{income_str}\n"
    
    facts += "\n**CRITICAL RULE**: You may ONLY cite facts that appear in this block. Do not invent names, numbers, or details.\n"
    
    return facts


def summarize_budget_analysis(county: str) -> str:
    """Extract key budget facts from the markdown analysis."""
    
    county_dir = DATA_DIR / county
    budget_md = load_file_content(county_dir / f"{county}_budget_analysis.md")
    
    if not budget_md:
        return "Budget analysis not available for this county."
    
    # Extract core numbers using regex
    operating = re.search(r'\*\*Operating Budget:\*\* \$?([\d,\.]+)', budget_md)
    capital = re.search(r'\*\*Capital Budget:\*\* \$?([\d,\.]+)', budget_md)
    total = re.search(r'\*\*Total Budget:\*\* \$?([\d,\.]+)', budget_md)
    
    summary = f"### Budget Summary (FY2026)\n"
    if operating:
        summary += f"- **Operating Budget**: ${operating.group(1)}\n"
    if capital:
        summary += f"- **Capital Budget**: ${capital.group(1)}\n"
    if total:
        summary += f"- **Total Budget**: ${total.group(1)}\n"
    
    # Extract "What This Means" section
    analysis_match = re.search(r'## What This Means: Analysis\n\n(.*?)(?=\n## |\Z)', budget_md, re.DOTALL)
    if analysis_match:
        analysis_text = analysis_match.group(1)
        # Get first 3 subsections
        subsections = re.findall(r'### \d+\. \*\*(.*?)\*\*\n(.*?)(?=\n### |\Z)', analysis_text, re.DOTALL)
        
        summary += "\n### Key Budget Insights\n"
        for title, content in subsections[:5]:  # Top 5 insights
            # Get first paragraph only
            first_para = content.strip().split('\n\n')[0]
            summary += f"\n**{title}**\n{first_para}\n"
    
    return summary


def summarize_minutes_analysis(county: str) -> str:
    """Extract key issues from meeting minutes analysis."""
    
    county_dir = DATA_DIR / county
    minutes_md = load_file_content(county_dir / f"{county}_recent_minutes_analysis.md")
    
    if not minutes_md:
        return "Meeting minutes analysis not available for this county."
    
    summary = "### Key Issues from Recent County Meetings\n\n"
    
    # Extract major issues section
    issues_match = re.search(r'## Major Issues & Developments\n(.*?)(?=\n## |\Z)', minutes_md, re.DOTALL)
    if issues_match:
        issues_text = issues_match.group(1)
        # Get each subsection
        subsections = re.findall(r'### \d+\. (.*?)\n(.*?)(?=\n### |\Z)', issues_text, re.DOTALL)
        
        for title, content in subsections[:5]:  # Top 5 issues
            # Get first 2 paragraphs
            paras = [p for p in content.strip().split('\n\n') if p and not p.startswith('**')]
            first_paras = '\n\n'.join(paras[:2])
            summary += f"**{title}**\n{first_paras}\n\n"
    
    # Extract public engagement summary
    engagement_match = re.search(r'## Public Engagement Analysis\n(.*?)(?=\n## |\Z)', minutes_md, re.DOTALL)
    if engagement_match:
        summary += f"\n**Public Engagement Pattern**\n{engagement_match.group(1).strip()[:500]}...\n"
    
    return summary


def build_sources_table(county: str) -> str:
    """Pre-build the Key Sources table."""
    
    county_dir = DATA_DIR / county
    county_name = COUNTY_NAMES[county]
    
    officials_data = load_json_file(county_dir / f"{county}_county_officials.json")
    muni_data = load_json_file(county_dir / f"{county}_municipal_officials.json")
    
    # Also load stories to see who's quoted
    stories_data = load_json_file(BASE_DIR / "beatbook_standardized_stories.json")
    if isinstance(stories_data, list):
        county_stories = [s for s in stories_data if county_name in s.get("counties", [])]
        people_in_stories = Counter()
        for story in county_stories:
            for person in story.get("key_people", []):
                if person and len(person) > 2:
                    people_in_stories[person] += 1
    else:
        people_in_stories = Counter()
    
    table = f"## Key Sources — {county_name}\n\n"
    
    # Start with commissioners
    table += "### County Commissioners/Council\n\n"
    table += "| Name | Position | Party | Stories Mentioning | Notes |\n"
    table += "|------|----------|-------|-------------------|-------|\n"
    
    leg_branch = officials_data.get("county_officials", {}).get("legislative_branch", [])
    if leg_branch:
        for official in leg_branch:
            name = official.get("name", "")
            title = official.get("title", "")
            party = official.get("party", "")
            story_count = people_in_stories.get(name, 0)
            story_note = f"Mentioned in {story_count} stories" if story_count > 0 else ""
            if name and title:
                table += f"| {name} | {title} | {party} | {story_count} | {story_note} |\n"
    else:
        table += "| No data available |  |  |  |  |\n"
    
    # Add contact info
    contact = officials_data.get("other_info", {})
    if contact:
        phone = contact.get("phone", "")
        website = contact.get("website", "")
        address = contact.get("address", "")
        if phone or website:
            table += f"\n**County Contact**: "
            if phone:
                table += f"Phone: {phone} | "
            if website:
                table += f"Website: {website}"
            table += "\n"
    
    # Add judicial
    jud_branch = officials_data.get("county_officials", {}).get("judicial_branch", [])
    if jud_branch:
        table += "\n### Judicial Officials\n\n"
        table += "| Name | Position |\n"
        table += "|------|----------|\n"
        for judge in jud_branch:
            name = judge.get("name", "")
            if name:
                table += f"| {name} | Judge |\n"
    
    # Add municipal officials with story mentions
    if isinstance(muni_data, list) and muni_data:
        table += "\n### Municipal Leadership\n\n"
        table += "| Municipality | Chief Executive | Council Members | Stories | Website |\n"
        table += "|--------------|-----------------|-----------------|---------|----------|\n"
        
        for town in muni_data:
            town_name = town.get("municipality_name", "")
            chief = town.get("chief_executive")
            
            # Handle None or missing chief_executive
            if chief is None or not isinstance(chief, dict):
                mayor_name = "No data"
                mayor_title = ""
                mayor_email = ""
            else:
                mayor_name = chief.get("name", "No data")
                mayor_title = chief.get("title", "")
                mayor_email = chief.get("email", "")
            
            website = town.get("website", "")
            
            # Count stories mentioning this municipality
            muni_story_count = sum(1 for s in county_stories 
                                  if town_name in s.get("municipalities", []))
            
            council = town.get("council_members", [])
            if isinstance(council, list):
                council_names = ", ".join([c.get("name", "") for c in council[:3] if isinstance(c, dict)])
                if len(council) > 3:
                    council_names += f" (+{len(council)-3} more)"
            else:
                council_names = ""
            
            if town_name:
                mayor_display = f"{mayor_name} ({mayor_title})" if mayor_title else mayor_name
                table += f"| {town_name} | {mayor_display} | {council_names} | {muni_story_count} | {website} |\n"
    
    # Add most-quoted people who aren't commissioners
    table += "\n### Other Key Figures (from story coverage)\n\n"
    table += "| Name | Story Mentions | Likely Role |\n"
    table += "|------|----------------|-------------|\n"
    
    # Get people not already in commissioners list
    commissioner_names = {o.get("name", "") for o in leg_branch}
    other_people = [(name, count) for name, count in people_in_stories.most_common(15) 
                   if name not in commissioner_names and count >= 3]
    
    for name, count in other_people[:10]:
        table += f"| {name} | {count} | (staff/advocate/stakeholder) |\n"
    
    table += "\n*Note: Story mention counts based on analysis of local news coverage. Roles for non-officials inferred from context.*\n"
    
    return table


def find_story_meeting_connections(county: str) -> str:
    """Find stories that correspond to meeting topics for better Section 7 integration."""
    
    county_name = COUNTY_NAMES[county]
    county_dir = DATA_DIR / county
    
    # Load minutes
    minutes_md = load_file_content(county_dir / f"{county}_recent_minutes_analysis.md")
    
    # Load stories
    stories_data = load_json_file(BASE_DIR / "beatbook_standardized_stories.json")
    if not isinstance(stories_data, list):
        return ""
    
    county_stories = [s for s in stories_data if county_name in s.get("counties", [])]
    
    # Extract meeting topics from minutes (look for ## Major Issues headings)
    meeting_topics = re.findall(r'### \d+\. (.*?)\n', minutes_md)
    
    connections = "### Story-to-Meeting Connections\n\n"
    connections += "*Use these to strengthen Section 7 by showing which issues got media coverage*\n\n"
    
    for topic in meeting_topics[:8]:  # Top 8 meeting topics
        topic_clean = topic.strip()
        
        # Find stories that mention keywords from this topic
        keywords = [word.lower() for word in topic_clean.split() 
                   if len(word) > 4 and word.lower() not in 
                   ['county', 'about', 'through', 'their', 'would', 'could']]
        
        related_stories = []
        for story in county_stories:
            title = story.get("title", "").lower()
            summary = story.get("summary", "").lower()
            content = story.get("content", "").lower()
            
            # Check if any keywords appear
            matches = sum(1 for kw in keywords if kw in title or kw in summary or kw in content[:500])
            if matches >= 2:  # At least 2 keyword matches
                related_stories.append({
                    'title': story.get("title", ""),
                    'date': story.get("date", ""),
                    'author': story.get("author", ""),
                    'matches': matches
                })
        
        if related_stories:
            related_stories.sort(key=lambda x: x['matches'], reverse=True)
            connections += f"**Meeting Topic**: {topic_clean}\n"
            connections += f"**Related Stories** ({len(related_stories)} found):\n"
            for story in related_stories[:3]:  # Top 3 matches
                connections += f"  - \"{story['title']}\" ({story['date']}) by {story['author']}\n"
            connections += "\n"
    
    return connections


def extract_story_insights(county: str) -> str:
    """Build comprehensive story analysis from standardized stories JSON."""
    
    stories_data = load_json_file(BASE_DIR / "beatbook_standardized_stories.json")
    if not isinstance(stories_data, list):
        return "Story data not available."
    
    county_name = COUNTY_NAMES[county]
    filtered = [s for s in stories_data if county_name in s.get("counties", [])]
    
    if not filtered:
        return f"No stories found for {county_name}."
    
    # Filter for relevant stories only
    relevant = [s for s in filtered 
                if s.get("beatbook_evaluation", {}).get("relevant", False)]
    
    summary = f"### Recent News Coverage for {county_name}\n\n"
    summary += f"- **Total stories**: {len(filtered)}\n"
    summary += f"- **Beatbook-relevant stories**: {len(relevant)}\n"
    
    # Date range
    dates = sorted([s.get("date", "") for s in filtered if s.get("date")])
    if dates:
        summary += f"- **Date range**: {dates[0]} to {dates[-1]}\n"
    
    # Topic analysis using llm_classification
    topic_counter = Counter()
    for story in relevant:
        topic = story.get("llm_classification", {}).get("topic", "Other")
        topic_counter[topic] += 1
    
    summary += "\n**Coverage by Topic**:\n"
    for topic, count in topic_counter.most_common(10):
        summary += f"- {topic}: {count} stories\n"
    
    # Key people mentioned across stories
    people_counter = Counter()
    for story in relevant:
        people = story.get("key_people", [])
        for person in people[:5]:  # Top 5 per story
            if person and len(person) > 2:  # Filter out initials
                people_counter[person] += 1
    
    if people_counter:
        summary += "\n**Most-Mentioned Officials/Figures** (across all stories):\n"
        for person, count in people_counter.most_common(10):
            summary += f"- {person}: mentioned in {count} stories\n"
    
    # Key organizations
    org_counter = Counter()
    for story in relevant:
        orgs = story.get("key_organizations", [])
        for org in orgs[:5]:
            if org and len(org) > 3:
                org_counter[org] += 1
    
    if org_counter:
        summary += "\n**Most-Mentioned Organizations**:\n"
        for org, count in org_counter.most_common(8):
            summary += f"- {org}: {count} stories\n"
    
    # Key events/initiatives
    events = []
    initiatives = []
    for story in relevant:
        events.extend(story.get("key_events", [])[:3])
        initiatives.extend(story.get("key_initiatives", [])[:3])
    
    event_counter = Counter(events)
    initiative_counter = Counter(initiatives)
    
    if event_counter:
        summary += "\n**Recurring Events/Issues**:\n"
        for event, count in event_counter.most_common(8):
            if event and len(event) > 5:
                summary += f"- {event}: {count} mentions\n"
    
    if initiative_counter:
        summary += "\n**Key Initiatives/Projects**:\n"
        for initiative, count in initiative_counter.most_common(8):
            if initiative and len(initiative) > 5:
                summary += f"- {initiative}: {count} mentions\n"
    
    # Sample high-relevance stories with full context
    summary += "\n**Sample High-Priority Stories** (for narrative context):\n\n"
    
    # Get stories with highest confidence scores
    scored_stories = [s for s in relevant 
                     if s.get("beatbook_evaluation", {}).get("confidence")]
    scored_stories.sort(
        key=lambda x: x.get("beatbook_evaluation", {}).get("confidence", 0), 
        reverse=True
    )
    
    for i, story in enumerate(scored_stories[:8], 1):
        title = story.get("title", "Untitled")
        date = story.get("date", "")
        author = story.get("author", "Unknown")
        topic = story.get("llm_classification", {}).get("topic", "")
        summary_text = story.get("summary", "")
        
        # Get top people/orgs for this story
        story_people = story.get("key_people", [])[:3]
        story_orgs = story.get("key_organizations", [])[:3]
        story_events = story.get("key_events", [])[:2]
        
        summary += f"**Story {i}**: \"{title}\"\n"
        summary += f"- Date: {date} | Author: {author} | Topic: {topic}\n"
        if story_people:
            summary += f"- Key people: {', '.join(story_people)}\n"
        if story_orgs:
            summary += f"- Key organizations: {', '.join(story_orgs)}\n"
        if story_events:
            summary += f"- Key events: {', '.join(story_events)}\n"
        if summary_text:
            summary += f"- Summary: {summary_text[:200]}...\n"
        summary += "\n"
    
    # Add municipalities covered
    muni_counter = Counter()
    for story in relevant:
        munis = story.get("municipalities", [])
        for muni in munis:
            if muni:
                muni_counter[muni] += 1
    
    if muni_counter:
        summary += "**Most-Covered Municipalities**:\n"
        for muni, count in muni_counter.most_common(10):
            summary += f"- {muni}: {count} stories\n"
    
    return summary


def build_section_prompt(section_num: int, county: str, facts: str, 
                         budget: str, minutes: str, sources: str, stories: str,
                         connections: str) -> str:
    """Build prompt for a specific section."""
    
    county_name = COUNTY_NAMES[county]
    
    # Section-specific instructions
    section_instructions = {
        1: """
## SECTION 1: Narrative Summary — "The State of the County"

Write EXACTLY 5 paragraphs. Each paragraph MUST be 180-220 words (900-1100 words total).

**Paragraph 1: Fiscal Overview**
- Lead with the FY2026 total budget number (from Budget Summary)
- Explain revenue sources (property/income tax percentages, any fund balance draw)
- Quote specific warnings from Budget Insights (use exact phrases like "revenue paradox," "unsustainable")
- Cite at least 3 specific dollar amounts from the budget
- Cross-reference with story coverage: if stories mention tax debates or budget battles, note this
- Use past tense (budget was adopted, commissioners voted, etc.)

**Paragraph 2: Major Capital/Infrastructure Challenge**  
- Identify the single biggest capital project or facility crisis from the minutes
- State the dollar amount and timeline from the budget or minutes
- Check story coverage: if this project was covered in multiple stories, cite story titles
- Explain what's driving it (state mandate, building failure, capacity limits, court order)
- Name specific officials who championed or opposed the project (from minutes and stories)
- Note any state cost-share uncertainty or funding gaps

**Paragraph 3: Policy Debates and Governance Decisions**
- Cite at least 2 specific policies from Meeting Minutes (give meeting dates and vote outcomes)
- Cross-reference Story Coverage: identify which policies got media attention
- Note whether votes were unanimous or contentious
- Name officials who took strong positions (use names from both minutes and story data)
- Explain what triggered each policy (state mandate, local crisis, advocacy pressure)
- Include any organized testimony or opposition mentioned in minutes

**Paragraph 4: Service Delivery and Community Impact**
- Focus on one major service expansion or crisis (EMS, seniors, housing, public safety, education)
- Cite a specific program or initiative from the minutes (with dollar amounts and dates)
- Check if stories covered this issue—cite relevant story titles if so
- Explain if this is expansion, contraction, or holding steady
- Note grant dependency and sustainability concerns
- Reference "Most-Mentioned Organizations" from story coverage if relevant

**Paragraph 5: Civic Engagement and Accountability Patterns**
- State explicitly whether public comments were recorded in the minutes (cite specific meetings)
- Describe the pattern you observe (zero comments on major items, stakeholder-only testimony, etc.)
- Cross-reference with story coverage: are reporters covering public input, or is it absent from stories too?
- Note which demographic groups are silent (homeowners, renters, young families, seniors)
- Identify any accountability gaps this creates
- End with a forward-looking question: What should reporters investigate in 2026?

**Integration Requirements**:
- Weave together minutes, budget data, and story coverage naturally
- When an issue appears in all three sources, emphasize this (e.g., "The detention center crisis, mentioned in 6 stories and debated in 3 meetings...")
- Use names consistently: if someone appears in both minutes and stories, note this
- Connect official actions to media coverage to show what got attention and what didn't

**Style Requirements**:
- Use past tense throughout (events already happened)
- Write in active voice with specific subjects (not "the county decided" but "Commissioners Breeding, Porter, and Bartz voted unanimously...")
- Every claim must cite a source (budget analysis, meeting date, story title/date)
- No speculation beyond documented evidence
- No phrases like "not provided in dataset"—focus only on what you know
""",
        2: """
## SECTION 2: Current Power Structure — Who Runs the County?

Create a table showing:
- Legislative branch (commissioners/council)
- Judicial officials (if listed)
- Key municipal leaders (mayors from largest towns)

For each official, include:
- Name and title (from Verified Facts)
- Party affiliation
- Selection method (elected, appointed, chosen by board)
- Notable voting patterns or policy focuses (from meeting minutes)

After the table, write 2 paragraphs (150 words each):
1. Describe informal alliances or rivalries among commissioners
2. Explain how municipal leaders interact with county government

Use only officials named in the Verified Facts block.
""",
        3: """
## SECTION 3: Civic Infrastructure & Demographics (Data Summary)

Create a clean reference table with these rows:
- Total Population
- Median Age
- Racial Composition (top 3 groups with percentages)
- Median Household Income
- Poverty Rate
- Homeownership Rate
- Median Home Value
- Renters Cost-Burdened
- Broadband Access
- Largest Towns (top 3-5 with populations)

Then write 1 paragraph (120 words) highlighting:
- The most significant demographic facts
- Any notable disparities or trends visible in the data
- What these numbers mean for service delivery

Use ONLY data from the Verified Facts block.
""",
        4: """
## SECTION 4: Elections & Political Landscape

Create a table with these rows:
- Registered Voters (approximate)
- Party Registration breakdown
- 2024 Presidential Vote
- 2022 Gubernatorial Vote
- Recent County Races (if available)
- Voter turnout patterns

Then write 2 paragraphs (150 words each):
1. Analyze the partisan balance and recent trends
2. Explain implications for reporters (what to watch, potential conflicts)

Use ONLY data from the Verified Facts block (Recent Elections section).
""",
        5: """
## SECTION 5: Schools & Education Landscape

Look for education spending in the Budget Summary.

If education spending is listed:
- State the dollar amount and percentage of total budget
- Note any year-over-year change
- Flag any mention of state Blueprint mandates

If no detailed school data is provided:
Write 1 paragraph: "Education accounts for [X]% of the county budget ($X million in FY2026). Detailed enrollment, performance, and facility data were not available for this analysis. The county's budget [does/does not] explicitly reference Maryland's Blueprint for Education mandates."

Do NOT invent enrollment numbers, test scores, or school names.
""",
        6: """
## SECTION 6: Budget & Fiscal Priorities

First, create a summary table:
- Operating Budget (FY2026)
- Capital Budget (FY2026)
- Total Budget
- Top 5 expenditure categories with dollar amounts and percentages

Then write 3 paragraphs (150 words each):

**Paragraph 1: Revenue Structure**
- Describe where the money comes from
- Note any reliance on fund balance draws or one-time sources
- Flag any tax rate changes

**Paragraph 2: Spending Priorities**
- Explain which departments/services got the most
- Note fastest-growing categories
- Connect to service mandates or community needs

**Paragraph 3: Fiscal Sustainability**
- Summarize warnings or concerns from the Budget Insights
- Explain structural deficits, reserve depletion, or debt capacity
- Note any deferred maintenance or capital needs

Use ONLY data from Budget Summary and Budget Insights sections.
""",
        7: """
## SECTION 7: Key Local Government Issues to Watch

Identify 4-6 major issues by synthesizing:
1. Issues from the Meeting Minutes summary
2. Recurring themes in the Story Coverage (check "Recurring Events/Issues" and "Key Initiatives/Projects")
3. Warnings from the Budget Insights

For EACH issue, write EXACTLY 3 paragraphs (130-160 words each):

**Paragraph 1: What's Happening**
- State the issue clearly with a strong topic sentence
- Cite specific meeting dates and votes from the minutes
- Reference story titles/dates that covered this issue
- Include key people involved (from both minutes and story data)
- Give concrete numbers: dollar amounts, vote counts, project timelines, affected populations

**Paragraph 2: Why It Matters**
- Explain fiscal implications (budget impact, tax consequences, debt)
- Describe service delivery impacts (who benefits, who's affected)
- Note quality-of-life or economic development effects
- Connect to broader county challenges (aging infrastructure, demographic shifts, etc.)
- Explain political significance (election implications, state mandate pressure)

**Paragraph 3: Stakeholder Tensions**
- Name specific officials and their positions (use names from minutes and stories)
- Identify advocacy groups, developers, or community organizations involved
- Describe the nature of the conflict (fiscal vs. service, growth vs. preservation, local vs. state)
- Note what's at stake for different groups
- End with an accountability question: What should reporters watch? What records should be requested?

**Issue Selection Priority**:
- Issues mentioned in BOTH minutes and multiple news stories (highest priority)
- Budget red flags that appear in multiple budget insights
- Topics with the most story coverage or mentions in "Key Initiatives/Projects"
- Issues involving named officials who appear frequently

**Format**:
- Use H3 headings for each issue: "### Issue Name"
- Lead each issue with a compelling, specific title (not "Budget Concerns" but "County Faces $17M Structural Deficit Despite Tax Increases")
- Connect stories to official actions whenever possible
- Use past tense for events that happened, present tense for ongoing situations

**Evidence Requirements**:
Every claim must be anchored in:
- A specific meeting date and vote from the minutes, OR
- A story title and date from the coverage summary, OR  
- A dollar amount or percentage from the budget analysis

Do NOT speculate or invent tensions that aren't documented.
""",
        8: """
## SECTION 8: Municipal Profiles (Reference)

Create a table with these columns:
- Municipality name
- Population (from Verified Facts - Municipalities)
- Government type / key officials (from Key Sources table)
- Notable issues (from meeting minutes or story headlines, if mentioned)

Include only municipalities listed in the Verified Facts block.

After the table, write 1 paragraph (100 words):
Briefly describe the relationship between municipalities and county government (cooperative, contentious, independent, etc.) based on patterns in the meeting minutes.

Do NOT invent town names or officials.
""",
        9: """
## SECTION 9: Reporting Gaps & Investigative Leads

**IMPORTANT CONTEXT**: The story data provided represents only a subset of total news coverage for this county. Many stories were not included in the analysis. Therefore, this section focuses on gaps in *official government records and transparency*, not gaps in news coverage.

Write 4 paragraphs (150-180 words each):

**Paragraph 1: Missing Data in Official Records**
Identify what's missing from the government's own documentation:
- Budget line items mentioned in stories but not detailed in budget documents
- Meeting agenda items that lack corresponding minutes or vote records
- Officials quoted in stories who never appear in formal meeting records
- Programs or initiatives mentioned in news coverage with no supporting county documents
- Use specific examples with dates (ALWAYS include the year)

**Paragraph 2: Public Engagement Deficits**
Analyze patterns in citizen participation:
- Which major decisions (with dollar amounts and dates including year) had zero recorded public comment?
- What demographic groups are consistently absent from official testimony?
- Are there procedural barriers (meeting times, notice requirements, comment periods)?
- Compare public turnout at controversial hearings vs. routine meetings
- Note: Do NOT criticize reporters for not covering something—focus only on government transparency gaps

**Paragraph 3: Key Investigative Leads for Reporters**
List 5-7 concrete reporting angles:
- Specific budget discrepancies to probe (with dollar amounts)
- Vote patterns that suggest conflicts of interest
- Officials who abstain repeatedly without explanation
- Programs that appear in both meeting minutes and stories but have no budget allocation
- State mandates mentioned but never acted upon
- Projects announced in stories that never reach the formal agenda
- Each lead should cite a specific meeting date (with year), story title (with date including year), or budget line item

**Paragraph 4: Records to Request**
Provide a practical FOIA roadmap:
- Specific documents to request (with enough detail that a reporter could file the request)
- Which officials to interview and what questions to ask
- Secondary records that might reveal hidden patterns (email threads, consultant reports, grant applications)
- Timeline-based requests (e.g., "all emails between X and Y from March-June 2025")

**Style Requirements**:
- Write as if advising a reporter new to the beat
- Be specific with names, dates (always with years), dollar amounts, and vote tallies
- Avoid generic advice like "reporters should investigate..." without concrete examples
- Acknowledge incomplete story data but don't speculate about what stories might exist
- Focus on *provable* gaps using the meeting minutes and budget data as the baseline
""",
        10: """
## SECTION 10: Red Flags & Accountability Priorities

Create a table with two columns:
- Red Flag
- Why It Matters

List 7-10 accountability concerns based on:
- Budget warnings (structural deficits, reserve depletion, unsustainable growth)
- Procedural issues (lack of public comment, unanimous votes on controversial items)
- Fiscal risks (grant dependency, deferred maintenance, debt capacity)
- Policy conflicts (state mandates vs. local control, development vs. preservation)
- Transparency gaps (decisions made without public debate)

**CRITICAL**: Every red flag must cite a specific source:
- Meeting date (with year) and vote count, OR
- Budget line item and dollar amount, OR
- Story title and publication date (with year)

Then write 1 paragraph (150 words):

**Top 3 Priorities**: Explain which red flags demand immediate investigation and why. For each priority, specify:
- The accountability question at stake
- Which officials are responsible
- What records would reveal the full picture
- Why this matters to residents (connect to demographics or budget impacts)

Use ONLY concerns documented in Budget Insights, Meeting Minutes, Story Coverage, or evident from cross-referencing these sources.
""",
        11: """
## SECTION 11: Media Coverage Analysis — What's Getting Attention?

Write 4 paragraphs (150 words each):

**Paragraph 1: Coverage Volume and Focus**
- How many stories total vs. how many beatbook-relevant?
- Which topics dominate coverage (from "Coverage by Topic")?
- Which topics are under-covered despite appearing in budgets/minutes?
- Are reporters covering process stories (votes, meetings) or outcome stories (impacts, people)?

**Paragraph 2: Geographic Focus**
- Which municipalities get the most story coverage (from "Most-Covered Municipalities")?
- Does coverage match population distribution or budget allocation?
- Are rural areas or smaller towns getting adequate coverage?
- What explains the imbalances?

**Paragraph 3: Source Patterns**
- Which officials appear most in stories (from "Most-Mentioned Officials/Figures")?
- Do story sources match the formal power structure (commissioners) or include staff, advocates, citizens?
- Are the same organizations quoted repeatedly?
- Who's NOT getting quoted but should be?

**Paragraph 4: Story Types and Timing**
- Looking at story dates, do stories follow board meetings or lead them?
- Are stories reactive (covering decisions) or proactive (investigating issues before votes)?
- What proportion of stories include public comment or citizen voices?
- What types of stories are missing (investigative deep-dives, accountability follow-ups, impact analyses)?

Use specific numbers from the Story Coverage data (story counts, mention counts, date ranges).
"""
    }
    
    base_prompt = f"""
You are a professional journalist creating a local government beat book for {county_name}.

You have been provided with:
1. Verified demographic and political facts
2. Budget summary and analysis
3. Recent meeting minutes summary
4. Story coverage patterns
5. Pre-built key sources table

{facts}

{budget}

{minutes}

{stories}

{connections}

{sources}

---

{section_instructions.get(section_num, "Section not defined")}

**CRITICAL RULES**:
1. Use ONLY facts from the data blocks above
2. Do NOT invent names, numbers, dates, or organizations
3. If something is not in the data, omit it (do NOT write "not provided in dataset")
4. Write in past tense (events already happened)
5. Be specific: use actual names, dollar amounts, and dates
6. Focus on what IS known, not what's missing

Begin writing Section {section_num} now.
"""
    
    return base_prompt


def generate_county_section(county: str, section_num: int, 
                           facts: str, budget: str, minutes: str, 
                           sources: str, stories: str, connections: str) -> str:
    """Generate a single section for a county."""
    
    county_name = COUNTY_NAMES[county]
    
    print(f"  Generating Section {section_num}...", file=sys.stderr)
    
    prompt = build_section_prompt(section_num, county, facts, budget, 
                                  minutes, sources, stories, connections)
    
    # Save prompt for debugging
    debug_file = BASE_DIR / f"debug_{county}_section_{section_num}.txt"
    with open(debug_file, "w", encoding="utf-8") as f:
        f.write(prompt)
    
    output = run_llm(prompt)
    
    return output


def generate_beatbook() -> int:
    """Generate the complete beatbook iteratively."""
    
    print("\n" + "="*80, file=sys.stderr)
    print("FIVE-COUNTY BEATBOOK GENERATOR (VERSION 4)", file=sys.stderr)
    print("="*80 + "\n", file=sys.stderr)
    
    # Initialize output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("""# Five-County Local Government Beatbook (Version 4)

## Caroline, Dorchester, Kent, Queen Anne's, and Talbot Counties

*A comprehensive reference guide for local government reporters*

*Generated: November 2025*

---

## About This Beatbook

This beatbook integrates three critical data sources:
1. **Official county records**: budgets, meeting minutes, census data, election results
2. **Structured news coverage**: Analysis of local reporting patterns, key figures, and coverage gaps
3. **Cross-referencing**: Connections between media coverage and official government actions

Each county section includes:
- Narrative summary grounding current challenges in data
- Power structure and key sources with story mention counts
- Detailed issue analysis connecting meeting decisions to news coverage
- Media coverage analysis identifying gaps and opportunities

---

## Table of Contents

- [Caroline County](#caroline-county--beat-book)
- [Dorchester County](#dorchester-county--beat-book)
- [Kent County](#kent-county--beat-book)
- [Queen Anne's County](#queen-annes-county--beat-book)
- [Talbot County](#talbot-county--beat-book)

---

""")
    
    # Process each county
    for county in COUNTIES:
        county_name = COUNTY_NAMES[county]
        print(f"\n{'='*80}", file=sys.stderr)
        print(f"PROCESSING {county_name.upper()}", file=sys.stderr)
        print(f"{'='*80}\n", file=sys.stderr)
        
        # Pre-build all data blocks
        print("Building data blocks...", file=sys.stderr)
        facts = build_county_facts_block(county)
        budget = summarize_budget_analysis(county)
        minutes = summarize_minutes_analysis(county)
        sources = build_sources_table(county)
        stories = extract_story_insights(county)
        connections = find_story_meeting_connections(county)
        
        # Write county header
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n## {county_name} — Beat Book\n\n")
        
        # Generate each section
        for section_num in range(1, 12):  # Now includes Section 11
            try:
                section_output = generate_county_section(
                    county, section_num, facts, budget, minutes, sources, stories, connections
                )
                
                # Append to file
                with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                    f.write(section_output + "\n\n")
                
                print(f"  ✓ Section {section_num} complete", file=sys.stderr)
                
            except Exception as e:
                print(f"  ✗ Section {section_num} failed: {e}", file=sys.stderr)
                with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                    f.write(f"### Section {section_num}: [Generation Failed]\n\n")
        
        print(f"\n✓ {county_name} complete\n", file=sys.stderr)
    
    # Add final cross-county section
    print("\nGenerating cross-county resources section...", file=sys.stderr)
    
    cross_county_prompt = """
Create a final section titled "Key Documents, Records & Public Resources"

List common record types available across all five counties:
- Meeting minutes and agendas
- Budget documents
- Election results
- Comprehensive plans
- FOIA request procedures
- County codes and ordinances

Format as a reference table with:
- Resource Type
- Description
- Typical Access Point

Keep this concise and practical - no more than 20 rows.
"""
    
    try:
        cross_output = run_llm(cross_county_prompt)
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write("\n## Key Documents, Records & Public Resources\n\n")
            f.write(cross_output + "\n")
    except Exception as e:
        print(f"Cross-county section failed: {e}", file=sys.stderr)
    
    print("\n" + "="*80, file=sys.stderr)
    print("✓ BEATBOOK V4 GENERATION COMPLETE", file=sys.stderr)
    print("="*80, file=sys.stderr)
    print(f"\nOutput saved to: {OUTPUT_FILE}", file=sys.stderr)
    
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        final_size = len(f.read())
    print(f"Final size: {final_size:,} characters\n", file=sys.stderr)
    
    return 0


if __name__ == "__main__":
    sys.exit(generate_beatbook())