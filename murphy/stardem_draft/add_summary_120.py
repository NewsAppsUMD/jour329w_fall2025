#!/usr/bin/env python3
import json
import subprocess
from typing import Dict, Any

MODEL_NAME = "groq/openai/gpt-oss-120b"
INPUT_FILE = "education_stories_with_entities_v2.json"
OUTPUT_FILE = "education_stories_with_entities_v3.json"

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
    return result.stdout.decode("utf-8").strip()


def generate_summary(story: Dict[str, Any]) -> str:
    """Generate a 120-word summary for a story."""
    
    title = story.get("title", "")
    date = story.get("date", "")
    
    # Build metadata string
    metadata_parts = []
    
    if story.get("key_people"):
        metadata_parts.append(f"People: {', '.join(story['key_people'][:5])}")
    
    if story.get("key_organizations"):
        metadata_parts.append(f"Organizations: {', '.join(story['key_organizations'][:5])}")
    
    if story.get("key_initiatives"):
        metadata_parts.append(f"Initiatives: {', '.join(story['key_initiatives'][:3])}")
    
    if story.get("counties"):
        metadata_parts.append(f"Counties: {', '.join(story['counties'])}")
    
    metadata = "\n".join(metadata_parts) if metadata_parts else "No metadata available"
    
    prompt = f"""Generate a summary of this news story in MAXIMUM 120 words. You must stay under 120 words - do not exceed this limit.

Title: {title}
Date: {date}

Metadata:
{metadata}

Requirements:
- MAXIMUM 120 words - you MUST stay under this limit
- Count your words carefully and stop before reaching 120
- Capture the key facts, actions, context, and significance
- Be specific and concrete - include names, numbers, dates when relevant
- Use active voice
- Focus on who, what, when, where, why, and how
- Provide enough detail to understand the story without reading the full article
- If you're approaching 120 words, conclude your summary concisely

Example of a good summary (119 words):
"Talbot County Board of Education approved a $2 million budget increase for special education programs starting in fall 2024. The funding will hire 15 new teachers, expand services for students with disabilities, and address staffing shortages reported throughout the 2023-24 school year. Board President Emily Jackson said the investment reflects the county's commitment to inclusive education and compliance with state mandates. The decision comes after months of advocacy from parents and special education teachers who testified about overcrowded classrooms and inadequate resources. The expansion will include new classroom aides, specialized instructional materials, and professional development for existing staff. Implementation begins July 1, with new hires expected to start by August 15."

Return ONLY the summary text, nothing else. Stay under 120 words."""

    summary = run_llm(prompt)
    
    return summary


def main():
    # Load input data
    print(f"Loading {INPUT_FILE}...")
    with open(INPUT_FILE, "r") as f:
        stories = json.load(f)
    
    # Check if output file already exists (resume from previous run)
    start_index = 0
    try:
        with open(OUTPUT_FILE, "r") as f:
            existing_stories = json.load(f)
            # Count how many already have summaries
            start_index = sum(1 for s in existing_stories if "summary" in s)
            if start_index > 0:
                print(f"Found existing file with {start_index} summaries. Resuming from story {start_index + 1}...")
                stories = existing_stories
    except FileNotFoundError:
        print(f"Starting fresh - no existing output file found.")
    
    print(f"Processing {len(stories)} stories (starting from #{start_index + 1})...")
    
    # Process each story
    for i in range(start_index, len(stories)):
        story = stories[i]
        print(f"  [{i+1}/{len(stories)}] Processing: {story.get('title', 'Untitled')[:60]}...")
        
        try:
            summary = generate_summary(story)
            story["summary"] = summary
            word_count = len(summary.split())
            print(f"    ✓ Summary ({word_count} words): {summary[:100]}...")
            
            # Save after each story to preserve progress
            with open(OUTPUT_FILE, "w") as f:
                json.dump(stories, f, indent=2, ensure_ascii=False)
                
        except KeyboardInterrupt:
            print(f"\n\n⚠️  Interrupted by user. Saving progress...")
            with open(OUTPUT_FILE, "w") as f:
                json.dump(stories, f, indent=2, ensure_ascii=False)
            print(f"✓ Saved {i+1} stories with summaries to {OUTPUT_FILE}")
            print(f"Run the script again to resume from story #{i+2}")
            return
        except Exception as e:
            print(f"    ✗ Error generating summary: {e}")
            story["summary"] = "Error generating summary"
            # Still save progress even on error
            with open(OUTPUT_FILE, "w") as f:
                json.dump(stories, f, indent=2, ensure_ascii=False)
    
    # Final save
    print(f"\nSaving final output to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w") as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Complete! {len(stories)} stories saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
