#!/usr/bin/env python3
"""
Restore county commissioners meeting summary stories.
These stories contain important policy discussions, budget decisions, and governance activities.
"""

import json
import re

def is_commissioners_meeting_summary(story):
    """
    Check if a story is a county commissioners meeting summary.
    These typically have titles like "County Commissioners/Month" or "County Commissioners Meeting"
    """
    title = story.get('title', '').lower()
    
    # Patterns for commissioners meeting summaries
    commissioners_patterns = [
        r'county commissioners\s*/\s*\w+',  # "County Commissioners/Month"
        r'commissioners\s*/\s*\w+',          # "Commissioners/Month"
        r'board of commissioners\s*/\s*\w+'  # "Board of Commissioners/Month"
    ]
    
    # Month names to look for
    months = ['january', 'february', 'march', 'april', 'may', 'june', 
              'july', 'august', 'september', 'october', 'november', 'december',
              'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'sept', 'oct', 'nov', 'dec']
    
    for pattern in commissioners_patterns:
        if re.search(pattern, title):
            # Check if it includes a month
            if any(month in title for month in months):
                return True
    
    return False

def main():
    # Load the removed stories log
    with open('removed_stories_log.json', 'r') as f:
        removed_log = json.load(f)
    
    # Load the current beat book
    with open('refined_beat_book_stories.json', 'r') as f:
        kept_stories = json.load(f)
    
    print(f"Loaded {len(removed_log)} removed stories")
    print(f"Loaded {len(kept_stories)} kept stories")
    print()
    
    # Find commissioners meeting summaries to restore
    to_restore = []
    for entry in removed_log:
        # Handle both nested and flat structures
        if 'story' in entry:
            story = entry['story']
        else:
            story = entry
        
        if is_commissioners_meeting_summary(story):
            to_restore.append(entry)
            county = story.get('counties', ['Unknown'])[0] if story.get('counties') else 'Unknown'
            print(f"Found commissioners meeting to restore:")
            print(f"  County: {county}")
            print(f"  Title: {story.get('title', 'No title')}")
            print(f"  Date: {story.get('date', 'No date')}")
            print()
    
    if not to_restore:
        print("No commissioners meeting summaries found to restore.")
        return
    
    print(f"\nRestoring {len(to_restore)} commissioners meeting summary stories...")
    
    # Restore the stories
    for entry in to_restore:
        # Handle both nested and flat structures
        if 'story' in entry:
            kept_stories.append(entry['story'])
        else:
            kept_stories.append(entry)
        removed_log.remove(entry)
    
    # Save updated files
    with open('refined_beat_book_stories.json', 'w') as f:
        json.dump(kept_stories, f, indent=2)
    
    with open('removed_stories_log.json', 'w') as f:
        json.dump(removed_log, f, indent=2)
    
    print(f"\n✓ Restored {len(to_restore)} commissioners meeting summaries")
    print(f"✓ Updated beat book now has {len(kept_stories)} stories")
    print(f"✓ Removed log now has {len(removed_log)} stories")

if __name__ == '__main__':
    main()
