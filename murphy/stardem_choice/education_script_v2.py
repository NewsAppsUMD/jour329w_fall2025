import json
import subprocess
import sys
from pathlib import Path
from subprocess import TimeoutExpired

# Load content_type_list and maryland_counties_list from this script (copy-paste or import as needed)
content_type_list = [
    {
        "content_type": "News",
        "definition": "Full articles, excluding calendars, obituaries, legal notices, opinion pieces and other listings, meant to inform, not persuade, readers on news topics such as politics, elections, government, agriculture, education, housing, economy and budget, transportation, infrastructure, public works, public safety, crime, environment, arts, society, community and sports.",
        "examples": "Police investigating Easton homicide; Robbins YMCA opening reading hub to tackle childhood illiteracy"
    },
    {
        "content_type": "Calendars",
        "definition": "Calendars.",
        "examples": "Mid-Shore Calendar; RELIGION CALENDAR"
    },
    {
        "content_type": "Obituaries",
        "definition": "Obituaries.",
        "examples": "Rhonda Lynn Fearins Thomas; Mary Beth Adams"
    },
    {
        "content_type": "Legal Notices",
        "definition": "Legal notices.",
        "examples": "Legal Notices"
    },
    {
        "content_type": "Opinion",
        "definition": "Columns, editorials, letters to the editor and any other opinion-based pieces for which the primary purpose is to persuade, not necessarily inform, readers.",
        "examples": "Biden must go; EDITORIAL: 10-cent paper bag fee should be optional"
    },
    {
        "content_type": "Miscellaneous",
        "definition": "TV listings, Today in History articles and other non-news and non-opinion content.",
        "examples": "SPRING TRAINING GLANCE 3-10-24; TV LISTINGS 1-11-24; TODAY IN HISTORY/Aug. 4; Web links; Tonight's top picks"
    }
]

# maryland_counties_list omitted for brevity, but should be included in the actual script

INPUT_FILE = "education_stories_merged.json"
OUTPUT_FILE = "education_stories_with_entities_v2.json"
LLM_MODEL = "groq/meta-llama/llama-4-maverick-17b-128e-instruct"

# Helper to call LLM

def call_llm(prompt, story_json):
    # Combine the prompt and story into a single prompt
    full_prompt = f"{prompt}\n\nStory to process:\n{json.dumps(story_json, indent=2)}"
    
    try:
        result = subprocess.run(
            ["llm", "-m", LLM_MODEL],
            input=full_prompt.encode(),
            capture_output=True,
            check=True,
            timeout=120
        )
        
        # Parse the JSON response
        response_text = result.stdout.decode()
        
        # Try to extract JSON from the response (in case there's extra text)
        # Look for JSON object starting with { and ending with }
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_str = response_text[start_idx:end_idx+1]
            return json.loads(json_str)
        else:
            print(f"No JSON found in response", file=sys.stderr)
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"LLM call failed: {e.stderr.decode()}", file=sys.stderr)
        return None
    except subprocess.TimeoutExpired:
        print(f"LLM call timed out", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}", file=sys.stderr)
        print(f"Response was: {response_text[:200]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return None

def save_progress(updated_stories, output_file):
    """Save progress to output file"""
    with open(output_file, "w") as f:
        json.dump(updated_stories, f, indent=2)
    print(f"💾 Saved progress: {len(updated_stories)} stories to {output_file}")



def main():
    import argparse
    parser = argparse.ArgumentParser(description='Process education stories to add entity fields (v2).')
    parser.add_argument('--limit', type=int, help='Limit the number of stories to process (testing)')
    parser.add_argument('--batch-size', type=int, default=10, help='Number of stories per batch (default: 10)')
    parser.add_argument('--single-batch', action='store_true', help='Only process one batch then exit')
    parser.add_argument('--dry-run', action='store_true', help='Skip LLM calls; just copy stories forward for testing')
    parser.add_argument('--continuous', action='store_true', help='Process all remaining stories in batches automatically')
    args = parser.parse_args()
    
    if not Path(INPUT_FILE).exists():
        print(f"Input file {INPUT_FILE} not found.", file=sys.stderr)
        sys.exit(1)
    
    # Load existing progress if output file exists
    if Path(OUTPUT_FILE).exists():
        print(f"Found existing output file {OUTPUT_FILE}, loading progress...")
        with open(OUTPUT_FILE, "r") as f:
            updated_stories = json.load(f)
        # Count how many stories actually have the new fields
        processed_count = sum(1 for s in updated_stories if "content_type" in s)
        print(f"Found {len(updated_stories)} stories in output file, {processed_count} have new fields")
        # Keep only the processed stories
        updated_stories = updated_stories[:processed_count]
        print(f"Resuming from story {len(updated_stories) + 1}")
    else:
        updated_stories = []
    
    with open(INPUT_FILE, "r") as f:
        stories = json.load(f)
    
    # Apply limit if specified (for testing)
    if args.limit:
        stories = stories[:args.limit]
        print(f"Limiting to {args.limit} stories")
    
    # Skip already processed stories / resume
    start_idx = len(updated_stories)
    remaining_total = len(stories) - start_idx
    if remaining_total <= 0:
        print("Nothing left to process.")
        save_progress(updated_stories, OUTPUT_FILE)
        print(f"✅ ALL DONE! Processed all {len(updated_stories)} stories")
        return

    batch_size = args.batch_size
    batch_num = 1
    from time import perf_counter
    
    if args.continuous:
        print(f"🚀 CONTINUOUS MODE: Processing all {remaining_total} remaining stories in batches of {batch_size}")
    else:
        print(f"🚀 Starting batch at story {start_idx+1}. Remaining: {remaining_total}. This batch size: {batch_size}")

    # Loop over batches
    while start_idx < len(stories):
        stories_to_process = stories[start_idx : start_idx + batch_size]
        if not stories_to_process:
            break
            
        print(f"\n🔄 Batch {batch_num}: Processing {len(stories_to_process)} stories (stories {start_idx + 1}-{start_idx + len(stories_to_process)})")
        
        for idx, story in enumerate(stories_to_process):
            actual_idx = start_idx + idx
            print(f"\n[{idx+1}/{len(stories_to_process)}] Processing story {actual_idx+1}/{len(stories)}: {story.get('title', '')[:60]}")
            story_start = perf_counter()
            
            prompt = f"""
You are an expert news data annotator specializing in EDUCATION stories. Analyze the story and return a JSON object with ALL the original story fields plus these NEW fields.

CRITICAL: ALL entities must be EXPLICITLY education-related. This is an education beat book.

NEW FIELDS TO ADD:
- content_type: single best from: {json.dumps([ct["content_type"] for ct in content_type_list])}
- regions: array of general regions (Maryland, Virginia, D.C., or other country/state/region; 'U.S.' for national)
- municipalities: array of Maryland municipalities mentioned or central to story
- counties: array of Maryland counties where those municipalities are located. ALWAYS include "County" in the name (e.g., "Talbot County", "Caroline County", not just "Talbot" or "Caroline")
- key_people: array of ALL public officials, politicians, board members, council members, superintendents, principals, teachers, education officials, etc. Format MUST be: "Name — Title, Organization/Body/Institution" (use em dash —, not hyphen). Examples: "John Smith — Superintendent, Talbot County Public Schools", "Jane Doe — President, Talbot County Board of Education", "Robert Johnson — Principal, Easton High School". STANDARDIZE all names (consistent capitalization), titles, and organizations. If a person appears in the known people list below, use their EXACT format.
- key_events: array of EDUCATION-RELATED events. ONLY include: named, recurring or significant education events. Examples: "Back to School Resource Fair", "Chrome City Ride", "Kent County Fair" (if it's a 4-H/education event). DO NOT include: generic ceremonies (ribbon-cuttings, grand openings, dedications), board meetings, or general community events unless they are major education-focused events with a specific name.
- key_initiatives: array of SPECIFIC NAMED education initiatives/legislation/policies with proper names. ONLY include actual named initiatives. Examples: "Blueprint for Maryland's Future", "No Child Left Behind Act". DO NOT include: general course types (e.g., "Career and Technical Education", "Advanced Placement"), general programs, curriculum types, or activities mentioned in passing. Must be an actual initiative with a specific name.
- key_establishments: array of EDUCATION-RELATED establishments in Maryland. ONLY include: Maryland schools, colleges, universities, education centers, tutoring centers that are central to the story. Examples: "Easton High School", "Talbot County Public Schools", "Chesapeake College". DO NOT include: out-of-state universities mentioned only in people's backgrounds, general businesses, restaurants, stores, or companies that provide services to schools.
- key_organizations: array of EDUCATION-RELATED organizations AND government bodies. ONLY include: education nonprofits, parent-teacher organizations, educational advocacy groups, school foundations, major 4-H organizations, school boards, boards of education, school districts, departments of education, education committees. Examples: "Talbot County Board of Education", "National 4-H Council", "Parent Teacher Association", "Maryland State Department of Education". Standardize "4-H" (not "4H" or variations). DO NOT include: individual local 4-H clubs mentioned only as historical background, general nonprofits or community organizations unless they have an explicit education mission central to the story. DO NOT include district numbers or subdivisions - only the main body name (e.g., "Talbot County Board of Education", not "Talbot County Board of Education District 5"). Avoid duplicates and variations of the same body.

KEY_PEOPLE EXTRACTION RULES:
1. Extract ALL public officials, politicians, board members, council members, superintendents, principals, teachers, education board members, school officials, college/university administrators, education program directors
2. Use the EXACT standardized format: "Name — Title, Organization/Body/Institution"
3. STANDARDIZE all elements: consistent name capitalization, standardized titles, standardized organization names
4. Use em dash (—) not hyphen (-) between name and title
5. CRITICAL: When a person is mentioned with incomplete information (e.g., "board member" without specifying which board, or "superintendent" without the district name), you MUST use context clues from the story to determine the full title and organization. Look at the story's location, topic, and surrounding context to infer the correct board/organization. For example, if the story is about Talbot County schools and mentions "board member John Smith", infer this refers to the "Talbot County Board of Education".

RULES:
- Use title case when original is capitalized
- NEVER include 'Star-Democrat', 'Chesapeake Publishing Group', or 'Adams Publishing/APGMedia'
- Leave arrays empty [] if no education-related items exist
- State legislature = 'Maryland General Assembly'
- When in doubt about non-people entities, EXCLUDE - only include if it's clearly education-related
- For key_people, be INCLUSIVE - extract all public officials and education-related people
- Return ONLY valid JSON with all original fields plus new fields"""
            
            if args.dry_run:
                updated_stories.append(story)
            else:
                print("  ⏳ Calling LLM...", end="", flush=True)
                llm_result = call_llm(prompt, story)
                elapsed = perf_counter() - story_start
                if llm_result:
                    print(f" ✓ Done in {elapsed:.1f}s")
                    updated_stories.append(llm_result)
                else:
                    print(f" ✗ Failed after {elapsed:.1f}s", file=sys.stderr)
                    updated_stories.append(story)

        # Save after each batch
        save_progress(updated_stories, OUTPUT_FILE)
        remaining = len(stories) - len(updated_stories)
        
        if remaining <= 0:
            print(f"\n✅ ALL DONE! Processed all {len(updated_stories)} stories")
            break
        else:
            est_batches = (remaining + batch_size - 1) // batch_size
            print(f"📊 Batch {batch_num} complete. Progress: {len(updated_stories)}/{len(stories)}. Remaining: {remaining} (~{est_batches} more batches)")
            
        if args.single_batch:
            print(f"⏹ Single batch mode: stopping. Run again to continue.")
            break
            
        # Move to next batch
        start_idx += len(stories_to_process)
        batch_num += 1

if __name__ == "__main__":
    main()
