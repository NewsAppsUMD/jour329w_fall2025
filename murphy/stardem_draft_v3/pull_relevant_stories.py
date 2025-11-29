#!/usr/bin/env python3
"""
Filter local government stories for beat book relevance.

This script uses an LLM to evaluate each story in local_government_stories_with_entities_v2_cleaned_final.json
and determines whether it would be relevant for a local government beat book covering
Talbot County, Kent County, Dorchester County, Caroline County, and Queen Anne's County.
"""

import json
import subprocess
import sys
from pathlib import Path
from time import perf_counter

# Configuration
INPUT_FILE = "local_government_all_stories_combined.json"
OUTPUT_FILE = "selected_local_government_stories.json"
EXCLUDED_FILE = "excluded_local_government_stories.json"
LLM_MODEL = "groq/meta-llama/llama-4-maverick-17b-128e-instruct"

# Target counties for the beat book
TARGET_COUNTIES = [
    "Talbot County",
    "Kent County",
    "Dorchester County",
    "Caroline County",
    "Queen Anne's County"
]

RELEVANCE_PROMPT = """You are helping to create a beat book for a reporter covering the local government beat across five Maryland counties: Talbot County, Kent County, Dorchester County, Caroline County, and Queen Anne's County.

A beat book should help a reporter understand the TOP LOCAL GOVERNMENT ISSUES, KEY DECISION-MAKERS, and CRITICAL POLICIES in their coverage area. It is NOT a comprehensive archive of all local government stories.

Evaluate whether this story is ESSENTIAL for a beat book that helps a reporter cover major local government issues in these five counties.

BEAT BOOK FOCUS - INCLUDE STORIES ABOUT:

LOCAL GOVERNMENT MEETINGS & ACTIONS:
- Town/city council meetings, votes, appointments, controversies
- County commissioner meetings, decisions, discussions
- Planning and zoning commission meetings and decisions
- Board of education meetings and decisions
- Any other local government board or commission meetings

GOVERNMENT LEADERSHIP & PERSONNEL:
- Mayor, city manager, county administrator actions or changes
- Department head appointments, resignations, or controversies
- Elected official actions, statements, or controversies
- Government staff changes affecting operations

LEGISLATION, POLICY & REGULATIONS:
- Local ordinances, resolutions, laws proposed or passed
- Zoning changes, comprehensive plans, land use decisions
- Environmental regulations and policies
- Business regulations and licensing
- State or federal legislation affecting the five counties

BUDGETS & FUNDING:
- Local government budgets, tax rates, fiscal decisions
- Grant funding received by counties or municipalities (INCLUDE ALL)
- State or federal funding for local projects
- Bond issues, debt, financial planning
- Budget cuts or expansions

ELECTIONS & REPRESENTATION:
- Local elections, candidates, results
- Voter registration, polling places
- Redistricting, ward changes
- Referendums, ballot questions

SCHOOLS & EDUCATION (LOCAL GOVERNMENT ANGLE):
- School board decisions and funding
- School construction, facilities, capital projects
- School budget votes and tax implications
- School-related referendums

INFRASTRUCTURE & DEVELOPMENT:
- Roads, bridges, transportation projects
- Water, sewer, utilities infrastructure
- Broadband, telecommunications infrastructure
- DATA CENTER projects (ALWAYS INCLUDE)
- Major development projects requiring government approval
- Housing developments, affordable housing initiatives

ECONOMIC DEVELOPMENT:
- Business attraction and retention programs
- Economic development authority actions
- Tax incentives, enterprise zones
- Downtown revitalization, Main Street programs

PUBLIC SERVICES & FACILITIES:
- Parks, recreation facilities, libraries
- Public safety facilities (fire, police, EMS)
- Government buildings, courthouses
- Waste management, recycling programs

LAND USE & ENVIRONMENT:
- Annexations, municipal boundaries
- Critical area regulations
- Historic preservation decisions
- Environmental permits and reviews
- Waterfront access, marina issues

ACCOUNTABILITY & TRANSPARENCY:
- Ethics investigations, violations
- Open meetings law, public records disputes
- Government audits, investigations
- Lawsuits involving local government
- Regional cooperation or conflicts

EXCLUDE:
- Stories ONLY about state/federal issues with no local angle
- Pure opinion pieces without reporting on government action
- Individual citizen complaints not involving government response
- Routine announcements with no policy implications

GEOGRAPHIC REQUIREMENT:
Story MUST directly involve Talbot, Kent, Dorchester, Caroline, or Queen Anne's County local governments (towns, cities, or county governments). State-level stories are only relevant if they have clear, specific impact on these counties.

BEAT BOOK TEST:
Ask yourself: "Would a new local government reporter covering these five counties need to know this story to understand the major issues, key players, and policy landscape?" If not, exclude it.

Story to evaluate (TITLE AND METADATA ONLY - make your decision based on these fields):
Title: {title}
Date: {date}
Content Type: {content_type}
Local Government Score: {local_gov_score}
Topics: {topics}
Counties: {counties}
Key People: {key_people}
Key Organizations: {key_organizations}
Key Initiatives: {key_initiatives}

Respond with a JSON object containing ONLY:
- "relevant": true or false
- "confidence": a number from 0.0 to 1.0
- "reason": (if relevant=false) brief explanation categorized as one of: "too_niche", "wrong_jurisdiction", "opinion_only", "routine_announcement", "no_policy_impact", "other"

Examples:
{{"relevant": true, "confidence": 0.95}}
{{"relevant": false, "confidence": 0.90, "reason": "too_niche"}}
{{"relevant": false, "confidence": 0.85, "reason": "wrong_jurisdiction"}}

Your response (JSON only):"""


def load_stories(input_path: Path) -> list:
    """Load stories from JSON file."""
    with open(input_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_stories(stories: list, output_path: Path):
    """Save stories to JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)


def get_local_gov_score(story: dict) -> float:
    """Extract local government topic score from story classification."""
    classification = story.get('llm_classification', {})
    
    # Check primary topic
    if classification.get('topic') == 'Local Government':
        return classification.get('score', 0.0)
    
    # Check candidates
    candidates = classification.get('candidates', [])
    for candidate in candidates:
        if candidate.get('topic') == 'Local Government':
            return candidate.get('score', 0.0)
    
    return 0.0


def format_story_for_batch(story: dict, index: int) -> str:
    """Format a single story's metadata for batch evaluation."""
    title = story.get('title', 'Untitled')
    date = story.get('date', 'Unknown')
    content_type = story.get('content_type', 'Unknown')
    local_gov_score = get_local_gov_score(story)
    
    # Get topics
    classification = story.get('llm_classification', {})
    topics = []
    if classification.get('topic'):
        topics.append(f"{classification['topic']} ({classification.get('score', 0.0):.2f})")
    for candidate in classification.get('candidates', [])[:3]:
        if candidate.get('topic') != classification.get('topic'):
            topics.append(f"{candidate['topic']} ({candidate.get('score', 0.0):.2f})")
    
    counties = story.get('counties', [])
    key_people = story.get('key_people', [])[:3]
    key_organizations = story.get('key_organizations', [])[:3]
    key_initiatives = story.get('key_initiatives', [])[:3]
    
    return f"""
Story {index}:
- Title: {title}
- Date: {date}
- Content Type: {content_type}
- Local Government Score: {local_gov_score:.2f}
- Topics: {', '.join(topics) if topics else 'None'}
- Counties: {', '.join(counties) if counties else 'None'}
- Key People: {', '.join(key_people) if key_people else 'None'}
- Key Organizations: {', '.join(key_organizations) if key_organizations else 'None'}
- Key Initiatives: {', '.join(key_initiatives) if key_initiatives else 'None'}
"""


def evaluate_stories_batch(stories: list) -> list:
    """Evaluate a batch of stories at once using LLM."""
    
    batch_prompt = RELEVANCE_PROMPT + "\n\n"
    batch_prompt += "Evaluate the following stories. Respond with a JSON array containing one evaluation object for each story (in order), with ONLY these fields:\n"
    batch_prompt += '- "relevant": true/false\n'
    batch_prompt += '- "confidence": 0.0-1.0\n'
    batch_prompt += '- "reason": (if relevant=false) categorize as: "too_niche", "wrong_jurisdiction", "opinion_only", "routine_announcement", "no_policy_impact", or "other"\n\n'
    
    for i, story in enumerate(stories, 1):
        batch_prompt += format_story_for_batch(story, i)
    
    batch_prompt += '\nYour response (JSON array only, no explanations):\n'
    
    # Call LLM
    try:
        result = subprocess.run(
            ['llm', '-m', LLM_MODEL],
            input=batch_prompt,
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse JSON response
        response_text = result.stdout.strip()
        
        # Try to extract JSON if wrapped in markdown
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        evaluations = json.loads(response_text)
        
        # Ensure it's a list and has the right length
        if not isinstance(evaluations, list):
            raise ValueError("Response is not a list")
        if len(evaluations) != len(stories):
            raise ValueError(f"Expected {len(stories)} evaluations, got {len(evaluations)}")
        
        return evaluations
        
    except (subprocess.CalledProcessError, json.JSONDecodeError, ValueError) as e:
        print(f"  ⚠️  Batch evaluation failed: {e}", file=sys.stderr)
        # Return all False as fallback
        return [{"relevant": False, "confidence": 0.0, "error": True} for _ in stories]


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Filter local government stories for beat book relevance')
    parser.add_argument('--limit', type=int, help='Limit number of stories to process')
    parser.add_argument('--skip', type=int, default=0, help='Skip first N stories')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without saving')
    args = parser.parse_args()
    
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_FILE)
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Loading stories from {input_path}...")
    stories = load_stories(input_path)
    print(f"Loaded {len(stories)} stories")
    
    # Apply skip and limit
    if args.skip > 0:
        stories = stories[args.skip:]
        print(f"Skipped first {args.skip} stories, {len(stories)} remaining")
    
    if args.limit:
        stories = stories[:args.limit]
        print(f"Limited to {len(stories)} stories")
    
    relevant_stories = []
    excluded_stories = []
    excluded_by_reason = {}
    stats = {
        'total': len(stories),
        'relevant': 0,
        'not_relevant': 0,
        'errors': 0,
        'non_news': 0
    }
    
    # Filter to only News stories upfront
    news_stories = [s for s in stories if s.get('content_type') == 'News']
    stats['non_news'] = len(stories) - len(news_stories)
    
    print(f"\nFiltered to {len(news_stories)} News stories (skipped {stats['non_news']} non-news)")
    print("Processing in batches of 10...")
    start_time = perf_counter()
    
    BATCH_SIZE = 10
    processed = 0
    
    for batch_start in range(0, len(news_stories), BATCH_SIZE):
        batch = news_stories[batch_start:batch_start + BATCH_SIZE]
        batch_num = (batch_start // BATCH_SIZE) + 1
        total_batches = (len(news_stories) + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"\n{'='*80}")
        print(f"Batch {batch_num}/{total_batches} (stories {batch_start+1}-{batch_start+len(batch)})")
        print(f"{'='*80}")
        
        batch_start_time = perf_counter()
        evaluations = evaluate_stories_batch(batch)
        batch_time = perf_counter() - batch_start_time
        
        # Process results
        for story, evaluation in zip(batch, evaluations):
            processed += 1
            title = story.get('title', 'Untitled')
            
            # Add evaluation to story
            story['beatbook_evaluation'] = evaluation
            
            if evaluation.get('error'):
                print(f"  [{processed}] ⚠️  {title[:70]}")
                stats['errors'] += 1
                excluded_stories.append(story)
                reason = 'error'
                excluded_by_reason[reason] = excluded_by_reason.get(reason, 0) + 1
            elif evaluation.get('relevant'):
                print(f"  [{processed}] ✅ {title[:70]} (conf: {evaluation.get('confidence', 0):.2f})")
                relevant_stories.append(story)
                stats['relevant'] += 1
            else:
                reason = evaluation.get('reason', 'other')
                print(f"  [{processed}] ❌ {title[:70]} ({reason})")
                stats['not_relevant'] += 1
                excluded_stories.append(story)
                excluded_by_reason[reason] = excluded_by_reason.get(reason, 0) + 1
        
        print(f"\nBatch completed in {batch_time:.1f}s ({batch_time/len(batch):.1f}s per story)")
        print(f"Running total: {stats['relevant']} relevant, {stats['not_relevant']} not relevant, {stats['errors']} errors")
        
        # Save every 10 relevant stories (check after each batch)
        if not args.dry_run and stats['relevant'] > 0 and stats['relevant'] % 10 <= len(batch):
            print(f"💾 Saving progress ({stats['relevant']} relevant stories so far)...")
            save_stories(relevant_stories, output_path)
    
    total_time = perf_counter() - start_time
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total stories processed: {stats['total']}")
    print(f"Non-news stories skipped: {stats['non_news']}")
    print(f"Relevant stories: {stats['relevant']}")
    print(f"Not relevant stories: {stats['not_relevant']}")
    print(f"Errors: {stats['errors']}")
    print(f"Total time: {total_time:.1f}s ({total_time/stats['total']:.1f}s per story)")
    
    # Print exclusion breakdown
    if excluded_by_reason:
        print("\nEXCLUSION BREAKDOWN:")
        for reason, count in sorted(excluded_by_reason.items(), key=lambda x: x[1], reverse=True):
            print(f"  {reason}: {count}")
    
    if args.dry_run:
        print("\n🔍 DRY RUN - No files saved")
    else:
        print(f"\nSaving {len(relevant_stories)} relevant stories to {output_path}...")
        save_stories(relevant_stories, output_path)
        
        # Group excluded stories by reason
        excluded_grouped = {}
        for story in excluded_stories:
            reason = story.get('beatbook_evaluation', {}).get('reason', 'other')
            if reason not in excluded_grouped:
                excluded_grouped[reason] = []
            excluded_grouped[reason].append(story)
        
        # Save excluded stories
        excluded_path = Path(EXCLUDED_FILE)
        print(f"Saving {len(excluded_stories)} excluded stories to {excluded_path}...")
        save_stories(excluded_grouped, excluded_path)
        print("✅ Done!")


if __name__ == '__main__':
    main()
