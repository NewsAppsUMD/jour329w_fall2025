#!/usr/bin/env python3
"""
Generate a comprehensive narrative education beat book by analyzing:
1. Selected education stories (refined_beatbook_stories.json)
2. County demographic and performance data (master_data files)
3. Master quotes and profiles

This version focuses on 5 OVERARCHING ISSUES affecting the Eastern Shore,
with each county's role and impact described within each issue section.
"""

import json
import subprocess
import time
import re
from collections import Counter, defaultdict
from pathlib import Path

MODEL_NAME = "groq/openai/gpt-oss-120b"
# Increase timeout for longer narrative generation
TIMEOUT_SECONDS = 300  # 5 minutes

COUNTIES = [
    "Talbot County",
    "Kent County",
    "Dorchester County",
    "Caroline County",
    "Queen Anne's County"
]

# Input files
INPUT_STORIES = "master_data/refined_beatbook_stories.json"
INPUT_BUDGET = "master_data/budget.json"
INPUT_PROFILES = "master_data/beatbook_profiles.json"
INPUT_QUOTES = "master_data/master_quotes.json"
INPUT_COUNTY_DATA_TEMPLATE = "master_data/{}_master_student_data.json"

OUTPUT_FILE = "beatbook_output/narrative_beatbook.md"


# ---------------------------------------------------------
# LLM utility with retry logic
# ---------------------------------------------------------
def run_llm(prompt: str, max_retries: int = 3) -> str:
    """Runs the LLM through the command-line interface with retry logic."""
    for attempt in range(max_retries):
        try:
            result = subprocess.run(
                ["llm", "-m", MODEL_NAME],
                input=prompt.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=TIMEOUT_SECONDS
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.decode("utf-8")
                if "Connection error" in error_msg and attempt < max_retries - 1:
                    print(f"    Connection error, retrying in 5 seconds... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(5)
                    continue
                raise RuntimeError(error_msg)
            
            output = result.stdout.decode("utf-8")
            
            # Strip out <think>...</think> content if present
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
# Load and process data
# ---------------------------------------------------------
def load_stories(filepath):
    """Load stories from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def load_budget_data(filepath):
    """Load budget data from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def load_profiles(filepath):
    """Load source profiles from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
        # Extract the profiles array from the structure
        if isinstance(data, dict) and 'profiles' in data:
            return data['profiles']
        return data


def load_quotes(filepath):
    """Load master quotes from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def load_county_student_data(county_name):
    """Load student data for a specific county."""
    # Convert "Talbot County" to "talbot"
    county_slug = county_name.replace(" County", "").lower()
    filepath = INPUT_COUNTY_DATA_TEMPLATE.format(county_slug)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"    Warning: No student data found for {county_name}")
        return {}


def group_stories_by_county(stories):
    """Group stories by county."""
    stories_by_county = defaultdict(list)
    for story in stories:
        for county in story.get("counties", []):
            if county in COUNTIES:
                stories_by_county[county].append(story)
    return stories_by_county


def extract_county_quotes(quotes_data, county_name):
    """Extract quotes relevant to a specific county."""
    county_quotes = []
    
    # The quotes structure is: quotes_by_topic -> topic -> speaker -> quotes array
    if isinstance(quotes_data, dict) and 'quotes_by_topic' in quotes_data:
        for topic, speakers in quotes_data['quotes_by_topic'].items():
            for speaker, speaker_data in speakers.items():
                if isinstance(speaker_data, dict) and 'quotes' in speaker_data:
                    for quote in speaker_data['quotes']:
                        if isinstance(quote, dict) and county_name in quote.get("counties", []):
                            county_quotes.append({
                                'speaker': speaker,
                                'quote': quote.get('quote', ''),
                                'topic': topic,
                                'story_title': quote.get('story_title', ''),
                                'date': quote.get('story_date', '')
                            })
    
    return county_quotes


def format_county_data_summary(county_name, budget_data, student_data, stories, quotes):
    """Create a text summary of county data for LLM prompts with enhanced detail."""
    summary = f"### {county_name} Data Summary\n\n"
    
    # Enhanced Budget info from budget.json
    county_slug = county_name.replace(" County", "").lower()
    if county_slug in budget_data:
        b = budget_data[county_slug]
        
        core = b.get('core_fiscal', {})
        per_pupil = b.get('enrollment_per_pupil', {})
        
        summary += f"**Budget & Fiscal Data (FY2026):**\n"
        
        # Operating budget details
        if 'ccps_total_operating_budget' in core:
            summary += f"- Total Operating Budget: ${core['ccps_total_operating_budget']:,.0f}\n"
        elif 'dcps_total_operating_budget' in core:
            summary += f"- Total Operating Budget: ${core['dcps_total_operating_budget']:,.0f}\n"
        elif 'kcps_total_operating_budget' in core:
            summary += f"- Total Operating Budget: ${core['kcps_total_operating_budget']:,.0f}\n"
        
        # Per-pupil breakdown
        if per_pupil:
            summary += f"- Enrollment: {per_pupil.get('enrollment', 0):,} students\n"
            summary += f"- Total per pupil: ${per_pupil.get('total_per_pupil', 0):,.0f}\n"
            summary += f"- Local per pupil: ${per_pupil.get('local_per_pupil', 0):,.0f}\n"
            summary += f"- State per pupil: ${per_pupil.get('state_per_pupil', 0):,.0f}\n"
        
        # Funding shares
        if core.get('local_share_pct'):
            summary += f"- Local share: {core['local_share_pct']:.1f}%\n"
            summary += f"- State share: {core['state_share_pct']:.1f}%\n"
        
        if core.get('county_local_appropriation'):
            summary += f"- County appropriation: ${core['county_local_appropriation']:,.0f}\n"
        if core.get('state_aid'):
            summary += f"- State aid: ${core['state_aid']:,.0f}\n"
        
        # Blueprint context
        blueprint = b.get('blueprint_drivers', {})
        if blueprint:
            summary += f"\n**Blueprint Drivers:**\n"
            for key, val in blueprint.items():
                summary += f"- {key.replace('_', ' ').title()}: {val}\n"
        
        # Narrative context
        if b.get('narrative'):
            summary += f"\n**Fiscal Context:** {b['narrative']}\n"
        
        summary += "\n"
    
    # Enhanced Student demographics from master_student_data files
    if student_data:
        summary += f"**Student Data & Demographics:**\n"
        
        # Count schools by level
        elem_schools = student_data.get('elementary_schools', [])
        middle_schools = student_data.get('middle_schools', [])
        high_schools = student_data.get('high_schools', [])
        
        if elem_schools or middle_schools or high_schools:
            summary += f"- Schools: {len(elem_schools)} elementary, {len(middle_schools)} middle, {len(high_schools)} high\n"
        
        # Sample a few schools with enrollment details
        all_schools = elem_schools + middle_schools + high_schools
        if all_schools:
            summary += f"\n**Sample School Demographics:**\n"
            for school in all_schools[:3]:  # First 3 schools
                name = school.get('school_name', 'Unknown')
                enrollment_data = school.get('enrollment', [])
                
                # Find total enrollment
                total_enroll = next((e for e in enrollment_data if e.get('group') == 'All Students'), {})
                if total_enroll.get('enrollment'):
                    summary += f"- {name}: {total_enroll['enrollment']} students\n"
                    
                    # Add racial breakdown
                    for e in enrollment_data:
                        if e.get('category') == 'Race/Ethnicity' and e.get('group') not in ['All Students']:
                            if e.get('enrollment') != '*' and e.get('percentage') != '*':
                                summary += f"  • {e['group']}: {e['percentage']:.1f}%\n"
        
        summary += "\n"
    
    # Story count and date range
    if stories:
        dates = [s.get('date') for s in stories if s.get('date')]
        date_range = f"{min(dates)} to {max(dates)}" if dates else "unknown"
        summary += f"**Coverage:** {len(stories)} stories ({date_range})\n\n"
    
    # Sample quotes
    if quotes:
        summary += f"**Sample Quotes ({len(quotes)} total):**\n"
        for i, q in enumerate(quotes[:3], 1):
            speaker = q.get('speaker', 'Unknown')
            text = q.get('quote', '')[:150]
            summary += f"{i}. {speaker}: \"{text}...\"\n"
        summary += "\n"
    
    return summary


# ---------------------------------------------------------
# Generate sections
# ---------------------------------------------------------
def build_county_overview_prompt(county, county_summary, stories_sample):
    """Build prompt for county overview section."""
    stories_text = ""
    for i, s in enumerate(stories_sample[:8], 1):
        stories_text += f"{i}. **{s.get('title', 'Untitled')}** ({s.get('date', 'No date')})\n"
        if s.get('summary'):
            stories_text += f"   {s.get('summary')[:200]}...\n"
        stories_text += "\n"
    
    return f"""You are writing a "County Overview & Context" section for {county} in an education beat book.

{county_summary}

Recent Stories:
{stories_text}

Write a comprehensive 2-3 paragraph overview that:
- Synthesizes demographic, budget, and academic performance data
- Highlights notable patterns (achievement gaps, resource challenges, leadership dynamics)
- Uses a direct, newsroom style
- Focuses on 2024-2025 developments
- References stories using numbered footnotes [1], [2], etc.

After the narrative, include a "Quick Facts" subsection with key data points in bullet form.

Write in a clear, fact-based style appropriate for a beat reporter.
"""


def build_key_sources_prompt(county, profiles, stories):
    """Build prompt for key sources section."""
    # Extract people from stories
    people_counter = Counter()
    for story in stories:
        for person in story.get('key_people', []):
            people_counter[person] += 1
    
    top_people = [p for p, _ in people_counter.most_common(15)]
    
    # Filter profiles for this county
    county_profiles = [p for p in profiles if county in p.get('counties', [])]
    
    profiles_text = ""
    for p in county_profiles[:10]:
        name = p.get('name', 'Unknown')
        title = p.get('current_title', 'Unknown position')
        profiles_text += f"- {name}: {title}\n"
    
    return f"""You are writing a "Key Sources to Know" section for {county} in an education beat book.

Top people mentioned in coverage: {', '.join(top_people[:10])}

Profiles available:
{profiles_text}

Write a "Key Sources to Know" section that lists key people organized by category:
- District Leadership (superintendent, board members, CFO, etc.)
- School Principals
- State Legislators (ONLY if directly connected to education)

Use **H4 headings (####)** for categories and bulleted lists for names.
For each person, include:
- Name and current position
- What decisions/areas they influence
- Current as of 2025

EXCLUDE:
- Political candidates
- Journalists/media
- Neighboring district leaders
- Community organizations
- Law enforcement

Keep entries concise and factual.
"""


def build_overarching_issues_prompt(all_county_summaries, all_stories_summary, budget_data, all_stories):
    """Build prompt for the 5 overarching issues section."""
    # Build budget context
    budget_context = "Budget Data by County:\n"
    for county, data in budget_data.items():
        if isinstance(data, dict) and county not in ['cross_county', 'metadata']:
            enroll = data.get('enrollment_per_pupil', {}).get('enrollment', 0)
            per_pupil = data.get('enrollment_per_pupil', {}).get('total_per_pupil', 0)
            local_per_pupil = data.get('enrollment_per_pupil', {}).get('local_per_pupil', 0)
            state_per_pupil = data.get('enrollment_per_pupil', {}).get('state_per_pupil', 0)
            county_budget = data.get('core_fiscal', {}).get('ccps_total_operating_budget', 0) or data.get('core_fiscal', {}).get('dcps_total_operating_budget', 0)
            local_share = data.get('core_fiscal', {}).get('local_share_pct', 0)
            
            budget_context += f"  - {county.title()}: {enroll:,} students, ${county_budget:,.0f} total budget, ${per_pupil:,.0f} per pupil (${local_per_pupil:,.0f} local + ${state_per_pupil:,.0f} state), {local_share:.1f}% local share\n"
    
    # Build detailed story excerpts for narrative richness
    story_excerpts = "Sample Story Details for Narrative Context:\n\n"
    for i, story in enumerate(all_stories[:30], 1):
        story_excerpts += f"[{i}] **{story.get('title', 'Untitled')}** ({story.get('date', 'No date')}) by {story.get('author', 'Unknown')}\n"
        if story.get('summary'):
            story_excerpts += f"Summary: {story.get('summary')}\n"
        if story.get('content'):
            excerpt = story.get('content', '')[:400].strip()
            story_excerpts += f"Excerpt: {excerpt}...\n"
        if story.get('key_people'):
            story_excerpts += f"People: {', '.join(story.get('key_people', [])[:5])}\n"
        if story.get('key_initiatives'):
            story_excerpts += f"Initiatives: {', '.join(story.get('key_initiatives', [])[:3])}\n"
        story_excerpts += "\n"
    
    return f"""You are writing a NARRATIVE education beat book covering five Maryland Eastern Shore counties: Talbot, Kent, Dorchester, Caroline, and Queen Anne's.

{budget_context}

County Data Summaries (demographics, test scores, student counts):
{all_county_summaries}

{story_excerpts}

Write about these **5 SPECIFIC OVERARCHING EDUCATION ISSUES** (YOU MUST WRITE ALL FIVE):
1. Achievement Gaps and Stagnant Test Scores
2. Funding Strains and Blueprint Implementation
3. Aging Infrastructure and Safety Investments
4. Discipline Equity and Student Support Services
5. Teacher Recruitment and Retention Crisis

For EACH OF THE 5 ISSUES (COMPLETE ALL FIVE):
1. Use an **H2 heading (##)** with the issue title above
2. Write a **REGIONAL SUMMARY** (1 paragraph) that:
   - States what happened across the region in 2023-2025
   - Cites 2-3 specific data points or decisions from the stories
3. Then create **5 county subsections** (one per county) using **H3 headings (###)**
4. In each county subsection, write **2-3 paragraphs** of ANALYTICAL NARRATIVE that:
   - Opens with what THIS county did/decided regarding this issue in 2023-2025
   - Cites specific data: enrollment numbers, budget amounts, test scores, project costs
   - Names specific schools, programs, board members involved
   - Analyzes the local factors: Why did this county take this approach? What constraints or priorities shaped decisions?
   - Shows cause and effect: Connect board decisions to outcomes, budget pressures to policy choices
   - Uses direct quotes from officials to illustrate positions or reasoning
   - References 3-5 specific stories for context and verification
   - NO SPECULATION: Don't say "remains to be seen" or "will likely" - analyze what actually happened and why

CRITICAL REQUIREMENTS:
- WRITE ALL FIVE ISSUES - do not stop after one issue
- STICK TO FACTS: Only report and analyze what actually happened in 2023-2025
- NO SPECULATION: Never say "remains to be seen," "will likely," "aims to," "seeks to"
- USE PAST TENSE: "The board approved," "Test scores dropped," "The district allocated"
- NEVER quote reporters (Konner Metz, Lily Tierney, Andrea Grabenstein, Ahmad Garnett, etc.)
- ONLY quote: superintendents, board members, state legislators, education officials
- Use REAL DATA: "$100,373,108 budget," "5,400 students," "$18,600 per pupil," "math scores dropped 3 points"
- Name REAL FACILITIES: "Easton High School," "Chapel District Elementary," "Lockerman Middle School"
- Reference REAL VOTES: "The board voted 5-0 to approve..."
- Show REAL PROJECTS with costs: "$1.2 million auditorium renovation," "$12 million Lockerman Middle construction"
- Use data from budget.json: enrollment, per-pupil spending, total budget, local vs state share
- ANALYTICAL DEPTH: Explain WHY decisions were made, WHAT constraints existed, HOW outcomes connected to choices
- Show competing priorities: budget vs services, local control vs state mandates, equity vs efficiency
- Connect the dots: "With enrollment declining and per-pupil funding flat, the board faced..."
- Each county section should be 2-3 substantive paragraphs with journalistic analysis
- Regional summary should be 1 paragraph stating what happened regionally

FORMAT: Each issue should have:
- H2 heading with issue name
- 1 paragraph regional summary
- 5 H3 county headings with 2-3 paragraph analytical narratives
"""


def build_state_resources_prompt(all_stories, budget_data):
    """Build prompt for state-level resources section."""
    # Extract state-level organizations and initiatives
    orgs = Counter()
    initiatives = Counter()
    legislators = Counter()
    
    for story in all_stories:
        for org in story.get('key_organizations', []):
            orgs[org] += 1
        for init in story.get('key_initiatives', []):
            initiatives[init] += 1
        for person in story.get('key_people', []):
            # Check if they're a legislator
            if any(title in person.lower() for title in ['senator', 'delegate', 'governor']):
                legislators[person] += 1
    
    top_orgs = [o for o, _ in orgs.most_common(20)]
    top_initiatives = [i for i, _ in initiatives.most_common(20)]
    top_legislators = [l for l, _ in legislators.most_common(15)]
    
    # Calculate regional averages from budget data
    regional_stats = ""
    total_enrollment = 0
    total_budget = 0
    
    county_breakdown = []
    for county, data in budget_data.items():
        if isinstance(data, dict) and county not in ['cross_county', 'metadata']:
            enroll = data.get('enrollment_per_pupil', {}).get('enrollment', 0)
            per_pupil = data.get('enrollment_per_pupil', {}).get('total_per_pupil', 0)
            county_budget = data.get('core_fiscal', {}).get('ccps_total_operating_budget', 0) or data.get('core_fiscal', {}).get('dcps_total_operating_budget', 0)
            
            if enroll > 0:
                total_enrollment += enroll
                total_budget += county_budget
                county_breakdown.append({
                    'name': county.title(),
                    'enrollment': enroll,
                    'per_pupil': per_pupil,
                    'budget': county_budget
                })
    
    avg_per_pupil = total_budget / total_enrollment if total_enrollment > 0 else 0
    
    regional_stats = f"""
Regional Data Summary:
- Total enrollment across 5 counties: {total_enrollment:,}
- Combined budget: ${total_budget:,.0f}
- Average per-pupil spending: ${avg_per_pupil:,.0f}

County breakdown:
"""
    for county_info in county_breakdown:
        regional_stats += f"  - {county_info['name']}: {county_info['enrollment']:,} students, ${county_info['per_pupil']:,.0f} per pupil (${county_info['budget']:,.0f} total budget)\n"
    
    return f"""You are creating a "State-Level Resources & Organizations" section for an education beat book covering Maryland's Eastern Shore.

{regional_stats}

Top organizations from coverage: {', '.join(top_orgs)}
Top initiatives from coverage: {', '.join(top_initiatives)}
Legislators mentioned: {', '.join(top_legislators)}

Write a comprehensive section with these categories (use H4 headings ####):

#### State Legislators with Education Roles
- Use the ACTUAL NAMES from the legislators list above
- Include their specific role (Senator/Delegate) and which committees they serve on
- Explain their connection to education policy or funding
- ONLY include those who have actual education-related roles

#### State Education Organizations
- Maryland State Department of Education and its key functions
- Maryland State Board of Education
- Other state organizations mentioned in coverage (from the list above)
- Keep descriptions brief but specific

#### Regional Data & Benchmarks
- Use the ACTUAL NUMBERS from the regional data summary above
- Include county-by-county enrollment and per-pupil spending comparisons
- Note any significant disparities between counties
- Reference state MCAP averages if mentioned in stories

Be specific and factual. Use the actual data provided - do NOT use placeholders like [Name] or [percentage].
"""


# ---------------------------------------------------------
# MAIN SCRIPT
# ---------------------------------------------------------
def main():
    print("Loading data files...")
    
    # Load all data
    stories = load_stories(INPUT_STORIES)
    budget = load_budget_data(INPUT_BUDGET)
    profiles = load_profiles(INPUT_PROFILES)
    quotes = load_quotes(INPUT_QUOTES)
    
    print(f"Loaded {len(stories)} stories, {len(profiles)} profiles, {len(quotes)} quotes")
    
    # Group by county
    stories_by_county = group_stories_by_county(stories)
    
    # Prepare county summaries with full budget data
    county_data = {}
    for county in COUNTIES:
        student_data = load_county_student_data(county)
        county_stories = stories_by_county.get(county, [])
        county_quotes = extract_county_quotes(quotes, county)
        
        county_data[county] = {
            'student_data': student_data,
            'stories': county_stories,
            'quotes': county_quotes,
            'summary': format_county_data_summary(county, budget, student_data, county_stories, county_quotes)
        }
    
    # Generate beatbook
    print("\nGenerating narrative beatbook...")
    
    with open(OUTPUT_FILE, 'w') as out:
        # Header
        out.write("# Eastern Shore Education Beat Book\n")
        out.write("## Five Maryland Counties: Comprehensive Regional Analysis\n\n")
        out.write("*A narrative guide for education reporters covering Talbot, Kent, Dorchester, Caroline, and Queen Anne's Counties*\n\n")
        out.write("*Generated December 2025 from 211 stories, county data, and source profiles*\n\n")
        out.write("*Focus: 2024-2025 school year developments*\n\n")
        out.write("---\n\n")
        
        # No table of contents - pure narrative
        out.write("\n")
        
        # PART 1: Five Overarching Issues
        print("\n" + "="*60)
        print("Generating regional analysis: Five Overarching Issues")
        print("="*60)
        
        out.write("# Five Overarching Education Issues\n\n")
        
        # Prepare comprehensive summaries
        all_county_summaries = "\n\n".join([
            data['summary'] for data in county_data.values()
        ])
        
        # Create story summary
        all_stories_summary = f"Total stories: {len(stories)}\n\n"
        all_stories_summary += "Story distribution by county:\n"
        for county in COUNTIES:
            count = len(stories_by_county.get(county, []))
            all_stories_summary += f"- {county}: {count} stories\n"
        
        # Sample key stories
        all_stories_summary += "\n\nSample stories across all counties:\n"
        for i, story in enumerate(stories[:20], 1):
            all_stories_summary += f"{i}. {story.get('title', 'Untitled')} ({story.get('date', 'No date')})\n"
            if story.get('summary'):
                all_stories_summary += f"   {story.get('summary')[:150]}...\n"
        
        # Generate the narrative analysis
        issues_prompt = build_overarching_issues_prompt(
            all_county_summaries,
            all_stories_summary,
            budget,
            stories
        )
        issues_text = run_llm(issues_prompt)
        out.write(issues_text.strip() + "\n\n")
    
    print(f"\n{'='*60}")
    print(f"✓ Narrative beatbook generated: {OUTPUT_FILE}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
