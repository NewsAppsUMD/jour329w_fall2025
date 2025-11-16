#!/usr/bin/env python3
"""
Filter education stories for beat book relevance.

This script uses an LLM to evaluate each story in education_stories_with_entities_v2.json
and determines whether it would be relevant for an education beat book covering
Talbot County, Kent County, Dorchester County, Caroline County, and Queen Anne's County.
"""

import json
import subprocess
import sys
from pathlib import Path
from time import perf_counter

# Configuration
INPUT_FILE = "education_stories_with_entities_v2.json"
OUTPUT_FILE = "selected_processed_education_stories.json"
LLM_MODEL = "groq/meta-llama/llama-4-maverick-17b-128e-instruct"

# Target counties for the beat book
TARGET_COUNTIES = [
    "Talbot County",
    "Kent County",
    "Dorchester County",
    "Caroline County",
    "Queen Anne's County"
]

RELEVANCE_PROMPT = """You are helping to create a beat book for a reporter covering the education beat across five Maryland counties: Talbot County, Kent County, Dorchester County, Caroline County, and Queen Anne's County.

A beat book should help a reporter understand the TOP EDUCATION ISSUES, KEY DECISION-MAKERS, and CRITICAL POLICIES in their coverage area. It is NOT a comprehensive archive of all education stories.

Evaluate whether this story is ESSENTIAL for a beat book that helps a reporter cover major education issues in these five counties.

BEAT BOOK FOCUS - ONLY INCLUDE STORIES ABOUT:

GOVERNANCE & POLICY (HIGH PRIORITY):
- Board of education meetings, votes, appointments, controversies
- Superintendent hiring, firing, contracts, major decisions
- Education policy changes and debates at board/county level
- Budget battles, funding decisions, tax issues affecting schools
- State legislation/policies with major impact on the five counties
- School consolidation, redistricting, facility planning decisions

SYSTEMIC ISSUES & ACCOUNTABILITY (HIGH PRIORITY):
- Teacher/staff shortages, hiring challenges, retention problems
- Blueprint for Maryland's Future implementation in the counties
- Student achievement gaps, test scores, graduation rates
- School safety incidents, security policy changes
- Major curriculum changes or controversies
- Equity issues, discrimination, civil rights matters
- Special education services, compliance issues

MAJOR INITIATIVES & PROGRAMS (MODERATE PRIORITY):
- New programs affecting multiple schools or whole districts
- Significant grants or funding for county-wide initiatives
- Regional partnerships involving the covered counties
- Career and technical education expansion

ABSOLUTELY EXCLUDE:
- Individual student achievements, awards, scholarships (NOT systemic issues)
- Feature stories about teachers or students (human interest, not policy)
- One-off school events (plays, concerts, fundraisers, field trips)
- School club activities, sports scores, student council elections
- Individual classroom activities or teaching methods
- College signing days, individual college acceptances
- Stories exclusively about other Maryland jurisdictions
- Stories about higher education unless directly tied to K-12 policy
- Opinion pieces, editorials, letters to editor
- Community events not directly related to education policy

GEOGRAPHIC REQUIREMENT:
Story MUST directly involve Talbot, Kent, Dorchester, Caroline, or Queen Anne's County. State-level stories are only relevant if they have clear, specific impact on these counties.

BEAT BOOK TEST:
Ask yourself: "Would a new education reporter covering these five counties need to know this story to understand the major issues, key players, and policy landscape?" If not, exclude it.

Story to evaluate (TITLE AND METADATA ONLY - make your decision based on these fields):
Title: {title}
Date: {date}
Content Type: {content_type}
Education Score: {education_score}
Topics: {topics}
Counties: {counties}
Key People: {key_people}
Key Organizations: {key_organizations}
Key Initiatives: {key_initiatives}

Respond with a JSON object containing ONLY:
- "relevant": true or false (be VERY selective - only include stories essential for understanding top education issues)
- "confidence": a number from 0.0 to 1.0

Examples:
{{"relevant": true, "confidence": 0.95}}
{{"relevant": false, "confidence": 0.90}}

Your response (JSON only):"""


def load_stories(input_path: Path) -> list:
    """Load stories from JSON file."""
    with open(input_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_stories(stories: list, output_path: Path):
    """Save stories to JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)


def get_education_score(story: dict) -> float:
    """Extract education topic score from story classification."""
    classification = story.get('llm_classification', {})
    
    # Check primary topic
    if classification.get('topic') == 'Education':
        return classification.get('score', 0.0)
    
    # Check candidates
    candidates = classification.get('candidates', [])
    for candidate in candidates:
        if candidate.get('topic') == 'Education':
            return candidate.get('score', 0.0)
    
    return 0.0


def format_story_for_batch(story: dict, index: int) -> str:
    """Format a single story's metadata for batch evaluation."""
    title = story.get('title', 'Untitled')
    date = story.get('date', 'Unknown')
    content_type = story.get('content_type', 'Unknown')
    education_score = get_education_score(story)
    
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
- Education Score: {education_score:.2f}
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
    batch_prompt += '- "confidence": 0.0-1.0\n\n'
    
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
    
    parser = argparse.ArgumentParser(description='Filter education stories for beat book relevance')
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
            elif evaluation.get('relevant'):
                print(f"  [{processed}] ✅ {title[:70]} (conf: {evaluation.get('confidence', 0):.2f})")
                relevant_stories.append(story)
                stats['relevant'] += 1
            else:
                print(f"  [{processed}] ❌ {title[:70]}")
                stats['not_relevant'] += 1
        
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
    
    if args.dry_run:
        print("\n🔍 DRY RUN - No files saved")
    else:
        print(f"\nSaving {len(relevant_stories)} relevant stories to {output_path}...")
        save_stories(relevant_stories, output_path)
        print("✅ Done!")


if __name__ == '__main__':
    main()
