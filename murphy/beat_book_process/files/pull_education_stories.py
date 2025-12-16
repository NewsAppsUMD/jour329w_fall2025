import json
from pathlib import Path

# Define the source files to search
SOURCE_FILES = [
    "agriculture_stories.json",
    "aquaculture_stories.json",
    "arts_culture_stories.json",
    "business_economy_stories.json",
    "environment_stories.json",
    "health_stories.json",
    "local_government_stories.json",
    "public_notices_stories.json",
    "public_safety_stories.json",
    "race_diversity_stories.json"
]

OUTPUT_FILE = "education_secondary_stories.json"
CONFIDENCE_THRESHOLD = 0.5

def has_education_secondary_topic(story):
    """Check if story has Education as a secondary topic with confidence > 0.5"""
    if "llm_classification" not in story:
        return False
    
    llm_classification = story["llm_classification"]
    
    if "candidates" not in llm_classification:
        return False
    
    candidates = llm_classification["candidates"]
    
    # Look for Education in the candidates
    for candidate in candidates:
        if candidate.get("topic") == "Education":
            score = candidate.get("score", 0)
            if score > CONFIDENCE_THRESHOLD:
                return True
    
    return False

def main():
    education_stories = []
    stories_by_source = {}
    
    print(f"Searching for Education stories with confidence > {CONFIDENCE_THRESHOLD}")
    print("=" * 70)
    
    for source_file in SOURCE_FILES:
        file_path = Path(source_file)
        
        if not file_path.exists():
            print(f"⚠️  Skipping {source_file} (not found)")
            continue
        
        print(f"\n📂 Processing {source_file}...")
        
        try:
            with open(file_path, "r") as f:
                stories = json.load(f)
            
            # Filter stories with Education as secondary topic
            matching_stories = [
                story for story in stories 
                if has_education_secondary_topic(story)
            ]
            
            if matching_stories:
                education_stories.extend(matching_stories)
                stories_by_source[source_file] = len(matching_stories)
                print(f"   ✓ Found {len(matching_stories)} Education stories")
            else:
                print(f"   - No Education stories found")
                
        except json.JSONDecodeError as e:
            print(f"   ✗ Error reading {source_file}: {e}")
        except Exception as e:
            print(f"   ✗ Unexpected error with {source_file}: {e}")
    
    # Save combined results
    print("\n" + "=" * 70)
    print(f"\n📊 SUMMARY:")
    print(f"   Total Education stories found: {len(education_stories)}")
    print(f"\n   Breakdown by source:")
    for source, count in sorted(stories_by_source.items(), key=lambda x: x[1], reverse=True):
        print(f"      {source:40} {count:4} stories")
    
    if education_stories:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(education_stories, f, indent=2)
        print(f"\n✅ Saved {len(education_stories)} stories to {OUTPUT_FILE}")
    else:
        print(f"\n⚠️  No stories found. {OUTPUT_FILE} not created.")

if __name__ == "__main__":
    main()
