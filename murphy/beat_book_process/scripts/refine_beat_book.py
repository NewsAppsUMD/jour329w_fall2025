#!/usr/bin/env python3
"""Two-pass beat book refinement script.

Phase 1 - PRUNE: Review selected stories and remove those that are too niche, too old, or not essential
Phase 2 - DISCOVER: Review original stories to find important ones that were missed

This ensures the beat book contains only the most essential stories for understanding
the education landscape in the five target counties.
"""

import json
import subprocess
import sys
from pathlib import Path
from time import perf_counter

# Configuration
SELECTED_FILE = "selected_processed_education_stories.json"
ORIGINAL_FILE = "education_stories_with_entities_v3.json"
OUTPUT_FILE = "refined_beat_book_stories.json"
REMOVED_FILE = "removed_stories_log.json"
ADDED_FILE = "added_stories_log.json"
LLM_MODEL = "groq/meta-llama/llama-4-maverick-17b-128e-instruct"
BATCH_SIZE = 10

# Pruning criteria prompt
PRUNING_PROMPT = """You are reviewing stories already selected for an education beat book covering five Maryland counties: Talbot, Kent, Dorchester, Caroline, and Queen Anne's.

BEAT BOOK PURPOSE:
Help a new education reporter quickly understand:
- Major policy issues and initiatives affecting these counties
- Key decision-makers (board members, superintendents, legislators)
- Systemic challenges (funding, staffing, achievement gaps)
- Critical programs and facilities decisions

PRUNE STORIES THAT ARE:

TOO NICHE OR MINOR:
- Individual school events (single-school plays, concerts, field trips)
- Minor grant announcements (< $50k or affecting single school)
- Routine personnel moves (individual teacher hires, retirements)
- One-time awards or recognitions for individuals
- Small-scale program launches affecting single classrooms
- Routine procedural updates without policy implications

TOO OLD TO MATTER:
- Stories from 2023 about short-term events/issues already resolved
- Time-sensitive announcements (back-to-school dates, specific event schedules)
- Stories about temporary pandemic measures (unless showing lasting policy changes)
- Personnel announcements about people no longer in those roles
- Budget discussions from fiscal years that have closed

NOT SUBSTANTIVE ENOUGH:
- Brief announcements without context or implications
- Stories that merely describe without revealing decisions or issues
- Feature stories about "day in the life" without policy content
- Stories that duplicate information better covered in other articles
- Announcements of future meetings without outcomes

KEEP STORIES THAT ARE:
- About ongoing systemic issues (staffing crisis, achievement gaps, Blueprint implementation)
- Major funding decisions that set precedent or affect multiple schools
- School board policy changes with lasting impact
- Significant facility decisions (construction, consolidation, closures)
- Major state/federal policy with local impact
- Stories revealing key power dynamics or conflicts
- Anything essential to understanding current education landscape

EXAMPLES OF STORIES TO PRUNE:
❌ "Elementary School Holds Fall Festival" - one-time event
❌ "Teacher Retires After 30 Years" - individual personnel, no policy impact
❌ "School Board Approves Routine Budget Transfers" - procedural, no controversy
❌ "Back-to-School Shopping Tips" - feature content, not news
❌ "Student Wins Art Contest" - individual achievement

EXAMPLES OF STORIES TO KEEP:
✅ "Board Votes to Close Elementary School" - major facility decision
✅ "Superintendent Resigns Amid Controversy" - leadership crisis
✅ "District Faces $5M Budget Shortfall" - systemic funding issue
✅ "Blueprint Implementation Stalls Over Staffing" - ongoing policy challenge
✅ "Counties Debate Chesapeake College Funding" - multi-county decision with lasting impact

Evaluate each story for ESSENTIAL vs. NICE-TO-HAVE. When in doubt, prune it - the beat book should be focused on what a reporter MUST know, not everything they COULD know.

Story to evaluate:
Title: {title}
Date: {date}
Counties: {counties}
Key People: {key_people}
Key Organizations: {key_organizations}
Key Initiatives: {key_initiatives}

Respond with JSON only:
{{"keep": true/false, "reason": "brief explanation", "confidence": 0.0-1.0}}
"""

DISCOVERY_PROMPT = """You are searching for stories that SHOULD be in an education beat book but were MISSED in initial filtering.

BEAT BOOK COVERS: Five Maryland counties (Talbot, Kent, Dorchester, Caroline, Queen Anne's)

LOOK FOR STORIES ABOUT:

MAJOR DECISIONS & POLICY:
- School board votes on significant issues (budgets, closures, redistricting)
- Superintendent hiring, firing, major contract decisions
- Policy changes affecting multiple schools or districts
- County commissioner votes on education funding
- State legislation with direct impact on these counties

SYSTEMIC ISSUES:
- Teacher/staff shortages and retention problems
- Blueprint for Maryland's Future implementation
- Achievement gaps, test scores, graduation rates
- School safety incidents and policy responses
- Curriculum controversies or major changes
- Equity issues and civil rights matters

MAJOR PROGRAMS & FACILITIES:
- School construction, renovation, closure decisions
- New district-wide programs or initiatives
- Chesapeake College governance, funding, major decisions
- Regional education partnerships
- Career and technical education expansion

KEY PLAYERS & POWER DYNAMICS:
- School board elections or controversies
- Superintendent performance reviews or conflicts
- Legislative battles over education funding
- Community organizing around education issues
- Major investigations or audits

EXCLUDE (NOT BEAT BOOK MATERIAL):
- Individual student achievements or awards
- Single-school events (concerts, plays, field trips)
- Feature stories about teachers/students (human interest)
- Minor grants or small programs
- Routine procedural updates
- Stories primarily about other counties

CRITICAL TEST:
Would a NEW education reporter covering these five counties need to read this story to understand:
- Current major issues?
- Key decision-makers?
- Policy landscape?
- Systemic challenges?

If YES to any of these → Story should probably be in beat book
If NO to all → Can safely exclude

Story to evaluate:
Title: {title}
Date: {date}
Counties: {counties}
Key People: {key_people}
Key Organizations: {key_organizations}
Key Initiatives: {key_initiatives}

Respond with JSON only:
{{"should_include": true/false, "reason": "brief explanation", "confidence": 0.0-1.0}}
"""


def load_json(filepath: Path) -> list:
    """Load stories from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: list, filepath: Path):
    """Save data to JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def format_story_metadata(story: dict) -> dict:
    """Extract key metadata from story for LLM evaluation."""
    return {
        'title': story.get('title', 'Untitled'),
        'date': story.get('date', 'Unknown'),
        'counties': ', '.join(story.get('counties', [])) or 'None',
        'key_people': ', '.join(story.get('key_people', [])[:3]) or 'None',
        'key_organizations': ', '.join(story.get('key_organizations', [])[:3]) or 'None',
        'key_initiatives': ', '.join(story.get('key_initiatives', [])[:3]) or 'None'
    }


def evaluate_story_pruning(story: dict) -> dict:
    """Evaluate whether a selected story should be kept or pruned."""
    metadata = format_story_metadata(story)
    
    prompt = PRUNING_PROMPT.format(**metadata)
    
    try:
        result = subprocess.run(
            ['llm', '-m', LLM_MODEL],
            input=prompt,
            capture_output=True,
            text=True,
            check=True
        )
        
        response = result.stdout.strip()
        
        # Extract JSON
        if '```json' in response:
            response = response.split('```json')[1].split('```')[0].strip()
        elif '```' in response:
            response = response.split('```')[1].split('```')[0].strip()
        
        evaluation = json.loads(response)
        return evaluation
        
    except Exception as e:
        print(f"  ⚠️  Error evaluating story: {e}", file=sys.stderr)
        return {"keep": True, "reason": "Error in evaluation", "confidence": 0.5}


def evaluate_story_discovery(story: dict) -> dict:
    """Evaluate whether an unselected story should be added."""
    metadata = format_story_metadata(story)
    
    prompt = DISCOVERY_PROMPT.format(**metadata)
    
    try:
        result = subprocess.run(
            ['llm', '-m', LLM_MODEL],
            input=prompt,
            capture_output=True,
            text=True,
            check=True
        )
        
        response = result.stdout.strip()
        
        # Extract JSON
        if '```json' in response:
            response = response.split('```json')[1].split('```')[0].strip()
        elif '```' in response:
            response = response.split('```')[1].split('```')[0].strip()
        
        evaluation = json.loads(response)
        return evaluation
        
    except Exception as e:
        print(f"  ⚠️  Error evaluating story: {e}", file=sys.stderr)
        return {"should_include": False, "reason": "Error in evaluation", "confidence": 0.5}


def prune_selected_stories(selected_stories: list) -> tuple[list, list]:
    """
    Phase 1: Review selected stories and remove those that aren't essential.
    Returns: (kept_stories, removed_stories_with_reasons)
    """
    print("\n" + "="*80)
    print("PHASE 1: PRUNING SELECTED STORIES")
    print("="*80)
    print(f"\nReviewing {len(selected_stories)} selected stories...")
    print("Removing stories that are too niche, too old, or not essential.\n")
    
    kept_stories = []
    removed_stories = []
    
    # Load existing progress if available
    removed_path = Path(REMOVED_FILE)
    kept_path = Path("kept_stories_progress.json")
    
    if removed_path.exists() and kept_path.exists():
        print("📂 Found existing progress, resuming...")
        removed_stories = load_json(removed_path)
        kept_stories = load_json(kept_path)
        processed_titles = {s['story']['title'] for s in removed_stories} | {s['title'] for s in kept_stories}
        selected_stories = [s for s in selected_stories if s.get('title') not in processed_titles]
        print(f"   Resuming from story {len(kept_stories) + len(removed_stories) + 1}\n")
    
    total = len(kept_stories) + len(removed_stories) + len(selected_stories)
    
    for i, story in enumerate(selected_stories, len(kept_stories) + len(removed_stories) + 1):
        title = story.get('title', 'Untitled')
        print(f"[{i}/{total}] Evaluating: {title[:70]}...")
        
        evaluation = evaluate_story_pruning(story)
        
        if evaluation.get('keep', True):
            kept_stories.append(story)
            print(f"  ✅ KEEP (confidence: {evaluation.get('confidence', 0):.2f})")
        else:
            removed_stories.append({
                'story': story,
                'reason': evaluation.get('reason', 'No reason provided'),
                'confidence': evaluation.get('confidence', 0)
            })
            print(f"  ❌ PRUNE: {evaluation.get('reason', 'No reason')}")
            print(f"     (confidence: {evaluation.get('confidence', 0):.2f})")
        
        # Save progress every story
        save_json(removed_stories, removed_path)
        save_json(kept_stories, kept_path)
    
    # Clean up progress file
    if kept_path.exists():
        kept_path.unlink()
    
    print(f"\n📊 Pruning Results:")
    print(f"   Kept: {len(kept_stories)}")
    print(f"   Removed: {len(removed_stories)}")
    
    return kept_stories, removed_stories


def discover_missing_stories(original_stories: list, selected_titles: set) -> tuple[list, list]:
    """
    Phase 2: Find important stories that were missed in initial filtering.
    Returns: (stories_to_add, discovery_log)
    """
    print("\n" + "="*80)
    print("PHASE 2: DISCOVERING MISSING STORIES")
    print("="*80)
    
    # Filter to stories not already selected and only News content type
    unselected = [
        s for s in original_stories 
        if s.get('title') not in selected_titles 
        and s.get('content_type') == 'News'
    ]
    
    print(f"\nSearching {len(unselected)} unselected stories for important ones that were missed...")
    print("Looking for major decisions, systemic issues, and key players.\n")
    
    stories_to_add = []
    discovery_log = []
    
    # Load existing progress if available
    added_path = Path(ADDED_FILE)
    added_stories_path = Path("added_stories_progress.json")
    
    if added_path.exists() and added_stories_path.exists():
        print("📂 Found existing progress, resuming...")
        discovery_log = load_json(added_path)
        stories_to_add = load_json(added_stories_path)
        processed_titles = {entry['title'] for entry in discovery_log}
        unselected = [s for s in unselected if s.get('title') not in processed_titles]
        print(f"   Resuming from story {len(discovery_log) + 1}\n")
    
    for i, story in enumerate(unselected, len(discovery_log) + 1):
        title = story.get('title', 'Untitled')
        
        # Only evaluate stories with some education relevance
        education_score = get_education_score(story)
        if education_score < 0.3:
            continue
        
        print(f"[{i}/{len(unselected) + len(discovery_log)}] Checking: {title[:70]}...")
        
        evaluation = evaluate_story_discovery(story)
        
        log_entry = {
            'title': title,
            'should_include': evaluation.get('should_include', False),
            'reason': evaluation.get('reason', 'No reason'),
            'confidence': evaluation.get('confidence', 0)
        }
        discovery_log.append(log_entry)
        
        if evaluation.get('should_include', False) and evaluation.get('confidence', 0) > 0.7:
            stories_to_add.append(story)
            print(f"  ✨ ADD THIS: {evaluation.get('reason', 'No reason')}")
            print(f"     (confidence: {evaluation.get('confidence', 0):.2f})")
        else:
            print(f"  ⏭️  Skip (confidence: {evaluation.get('confidence', 0):.2f})")
        
        # Save progress every story
        save_json(discovery_log, added_path)
        save_json(stories_to_add, added_stories_path)
    
    # Clean up progress file
    if added_stories_path.exists():
        added_stories_path.unlink()
    
    print(f"\n📊 Discovery Results:")
    print(f"   Stories to add: {len(stories_to_add)}")
    
    return stories_to_add, discovery_log


def get_education_score(story: dict) -> float:
    """Extract education topic score from story classification."""
    classification = story.get('llm_classification', {})
    
    if classification.get('topic') == 'Education':
        return classification.get('score', 0.0)
    
    candidates = classification.get('candidates', [])
    for candidate in candidates:
        if candidate.get('topic') == 'Education':
            return candidate.get('score', 0.0)
    
    return 0.0


def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Refine beat book through pruning and discovery')
    parser.add_argument('--prune-only', action='store_true', help='Only run pruning phase')
    parser.add_argument('--discover-only', action='store_true', help='Only run discovery phase')
    parser.add_argument('--limit', type=int, help='Limit number of stories to process in discovery phase')
    args = parser.parse_args()
    
    start_time = perf_counter()
    
    # Load files
    print("Loading data files...")
    selected_path = Path(SELECTED_FILE)
    original_path = Path(ORIGINAL_FILE)
    
    if not selected_path.exists():
        print(f"❌ Error: {SELECTED_FILE} not found", file=sys.stderr)
        sys.exit(1)
    
    if not original_path.exists():
        print(f"❌ Error: {ORIGINAL_FILE} not found", file=sys.stderr)
        sys.exit(1)
    
    selected_stories = load_json(selected_path)
    print(f"✅ Loaded {len(selected_stories)} selected stories")
    
    original_stories = load_json(original_path)
    print(f"✅ Loaded {len(original_stories)} original stories")
    
    # Phase 1: Prune selected stories
    kept_stories = selected_stories
    removed_stories = []
    
    if not args.discover_only:
        kept_stories, removed_stories = prune_selected_stories(selected_stories)
        print(f"\n💾 Pruning progress saved to {REMOVED_FILE}")
    
    # Phase 2: Discover missing stories
    added_stories = []
    discovery_log = []
    
    if not args.prune_only:
        selected_titles = {s.get('title') for s in kept_stories}
        
        # Apply limit if specified
        stories_to_check = original_stories
        if args.limit:
            stories_to_check = stories_to_check[:args.limit]
        
        added_stories, discovery_log = discover_missing_stories(stories_to_check, selected_titles)
        print(f"\n💾 Discovery progress saved to {ADDED_FILE}")
    
    # Combine kept + added stories
    final_stories = kept_stories + added_stories
    
    # Sort by date (newest first)
    final_stories.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    # Save refined beat book
    save_json(final_stories, Path(OUTPUT_FILE))
    
    # Final summary
    elapsed = perf_counter() - start_time
    
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"\n📊 Beat Book Refinement Complete:")
    print(f"   Original selected: {len(selected_stories)}")
    print(f"   After pruning: {len(kept_stories)} (removed {len(removed_stories)})")
    print(f"   Added from discovery: {len(added_stories)}")
    print(f"   Final beat book: {len(final_stories)} stories")
    print(f"\n⏱️  Total time: {elapsed:.1f} seconds")
    print(f"\n💾 Output files:")
    print(f"   {OUTPUT_FILE} - Refined beat book")
    print(f"   {REMOVED_FILE} - Pruning log")
    print(f"   {ADDED_FILE} - Discovery log")


if __name__ == '__main__':
    main()
