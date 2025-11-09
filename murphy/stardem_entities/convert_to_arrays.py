#!/usr/bin/env python3
"""
Convert semicolon-separated fields in stories JSON files to proper JSON arrays.
"""

import json
import sys
from pathlib import Path

def convert_semicolon_fields_to_arrays(story):
    """Convert semicolon-separated string fields to arrays."""
    fields_to_convert = ['people', 'sources', 'events', 'locations', 'municipalities', 'county', 'institutions']
    
    for field in fields_to_convert:
        if field in story and isinstance(story[field], str):
            value = story[field]
            # Split by semicolon and clean up
            if value and value != "N/A" and value != "":
                items = [item.strip() for item in value.split(';') if item.strip()]
                story[field] = items if items else []
            else:
                story[field] = []
    
    return story


def process_file(input_file):
    """Process a single file."""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"Warning: File {input_file} does not exist, skipping...")
        return
    
    print(f"\nLoading stories from {input_file}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        stories = json.load(f)
    
    print(f"Converting {len(stories)} stories...")
    converted_stories = []
    for i, story in enumerate(stories, 1):
        if i % 10 == 0:
            print(f"  Processed {i}/{len(stories)} stories...")
        converted_story = convert_semicolon_fields_to_arrays(story)
        converted_stories.append(converted_story)
    
    print(f"Saving converted stories to {input_file}...")
    with open(input_path, 'w', encoding='utf-8') as f:
        json.dump(converted_stories, f, indent=2, ensure_ascii=False)
    
    print(f"Done with {input_file}!")


def main():
    # Process multiple files
    files_to_process = [
        'stories_with_entities_1.json',
        'stories_with_entities_2.json',
        'stories_with_entities_2_ish.json'
    ]
    
    # If arguments provided, use those instead
    if len(sys.argv) > 1:
        files_to_process = sys.argv[1:]
    
    for file in files_to_process:
        process_file(file)
    
    print("\nAll files processed!")


if __name__ == '__main__':
    main()
