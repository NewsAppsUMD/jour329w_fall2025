#!/usr/bin/env python3
import json
import subprocess
from typing import Dict, Any

MODEL_NAME = "groq/openai/gpt-oss-120b"
INPUT_FILE = "selected_processed_education_stories.json"
OUTPUT_FILE = "selected_processed_education_stories.json"

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
    """Generate a brief summary (max 50 words) for a story."""
    
    title = story.get("title", "")
    date = story.get("date", "")
    
    # Build metadata string
    metadata_parts = []
    
    if story.get("key_people"):
        metadata_parts.append(f"People: {', '.join(story['key_people'][:3])}")
    
    if story.get("key_organizations"):
        metadata_parts.append(f"Organizations: {', '.join(story['key_organizations'][:3])}")
    
    if story.get("key_initiatives"):
        metadata_parts.append(f"Initiatives: {', '.join(story['key_initiatives'][:2])}")
    
    metadata = "\n".join(metadata_parts) if metadata_parts else "No metadata available"
    
    prompt = f"""Generate a brief summary of this news story in MAXIMUM 50 words.

Title: {title}
Date: {date}

Metadata:
{metadata}

Requirements:
- MAXIMUM 50 words total
- Capture the key facts, actions, and context
- Be specific and concrete
- Use active voice
- Focus on who, what, when, where, why

Examples of good 50-word summaries:
- "Talbot County Board of Education approved a $2 million budget increase for special education programs starting in fall 2024. The funding will hire 15 new teachers and expand services for students with disabilities, addressing staffing shortages reported throughout the 2023-24 school year."
- "Maryland's teacher shortage worsened in 2024, with 28 subject areas lacking qualified instructors, up from 17 five years ago. The Blueprint for Maryland's Future aims to address this through higher pay, better training, and recruitment efforts, though experts debate effectiveness."

Return ONLY the summary text, nothing else."""

    summary = run_llm(prompt)
    
    # Count words and truncate if necessary
    words = summary.split()
    if len(words) > 50:
        summary = ' '.join(words[:50]) + "..."
    
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
            print(f"    ✓ Summary ({word_count} words): {summary}")
            
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
