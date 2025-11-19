#!/usr/bin/env python3
"""
Restore board meeting summary stories that were incorrectly removed.
These stories with titles like "Board of Education/Month" contain important policy discussions.
"""

import json
from pathlib import Path

# File paths
REMOVED_LOG = "removed_stories_log.json"
REFINED_BEATBOOK = "refined_beat_book_stories.json"

def load_json(filepath: Path) -> list:
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: list, filepath: Path):
    """Save JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def is_board_meeting_summary(story: dict) -> bool:
    """Check if story is a board meeting summary (should be kept)."""
    title = story.get('title', '')
    
    # Patterns for board meeting summaries
    patterns = [
        'Board of Education/',
        'Board of Ed/',
        'BOE/',
        'Policy Committee/'
    ]
    
    # Check if title matches board meeting pattern
    for pattern in patterns:
        if pattern in title and any(month in title for month in [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]):
            return True
    
    return False

def main():
    """Main execution."""
    print("Loading files...")
    
    removed_path = Path(REMOVED_LOG)
    refined_path = Path(REFINED_BEATBOOK)
    
    if not removed_path.exists():
        print(f"❌ Error: {REMOVED_LOG} not found")
        return
    
    if not refined_path.exists():
        print(f"❌ Error: {REFINED_BEATBOOK} not found")
        return
    
    removed_stories = load_json(removed_path)
    kept_stories = load_json(refined_path)
    
    print(f"✅ Loaded {len(removed_stories)} removed stories")
    print(f"✅ Loaded {len(kept_stories)} kept stories")
    
    # Find board meeting summaries to restore
    to_restore = []
    for entry in removed_stories:
        story = entry['story']
        if is_board_meeting_summary(story):
            to_restore.append(entry)
            title = story.get('title', 'Untitled')
            date = story.get('date', 'Unknown')
            print(f"  📋 Restoring board meeting: {title}")
            print(f"     Date: {date}")
            print(f"     Previous removal reason: {entry.get('reason', 'N/A')[:80]}...")
    
    # Update removed list (remove board meetings from it)
    filtered_removed = [
        entry for entry in removed_stories
        if not is_board_meeting_summary(entry['story'])
    ]
    
    # Add restored stories back to kept
    for entry in to_restore:
        kept_stories.append(entry['story'])
    
    # Sort kept stories by date
    kept_stories.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    print(f"\n📊 Summary:")
    print(f"   Board meeting stories restored: {len(to_restore)}")
    print(f"   Updated kept stories: {len(kept_stories)}")
    print(f"   Updated removed log: {len(filtered_removed)}")
    
    # Save updated files
    save_json(filtered_removed, removed_path)
    save_json(kept_stories, refined_path)
    
    print(f"\n💾 Updated files:")
    print(f"   {REMOVED_LOG}")
    print(f"   {REFINED_BEATBOOK}")
    
    if to_restore:
        print(f"\n📋 Board meeting summary stories restored:")
        counties = {}
        for entry in to_restore:
            story = entry['story']
            county_list = story.get('counties', ['Unknown'])
            county = county_list[0] if county_list else 'Unknown'
            if county not in counties:
                counties[county] = []
            counties[county].append(story.get('title', 'Untitled'))
        
        for county, titles in sorted(counties.items()):
            print(f"\n   {county}:")
            for title in titles:
                print(f"     • {title}")

if __name__ == '__main__':
    main()
