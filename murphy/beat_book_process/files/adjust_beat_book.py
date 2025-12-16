#!/usr/bin/env python3
"""
Adjust beat book based on specific criteria:
1. Remove stories about individual student fights or crimes
2. Restore stories about cell phone policies (they ARE policy-relevant)
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

def is_individual_crime_or_fight(story: dict) -> bool:
    """Check if story is about individual student crime or fight."""
    title = story.get('title', '').lower()
    content = story.get('content', '').lower()
    
    # Keywords indicating individual incidents
    crime_keywords = [
        'student arrested',
        'student charged',
        'student accused',
        'assault on student',
        'student assault',
        'student attack',
        'fight at school',
        'student fight',
        'student injured in',
        'student hurt in',
        'stabbing',
        'shooting',
        'battery'
    ]
    
    # Check if it's about an individual incident
    for keyword in crime_keywords:
        if keyword in title or keyword in content[:500]:
            return True
    
    return False

def is_cell_phone_policy(story: dict) -> bool:
    """Check if story is about cell phone policy (should be kept)."""
    title = story.get('title', '').lower()
    content = story.get('content', '').lower()
    
    # Keywords for cell phone policy stories
    policy_keywords = [
        'cell phone',
        'cellphone',
        'mobile phone',
        'phone policy',
        'phone ban',
        'phone pouch',
        'phone restriction',
        'smartphone'
    ]
    
    for keyword in policy_keywords:
        if keyword in title or keyword in content[:1000]:
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
    
    # Find stories to restore (cell phone policies)
    to_restore = []
    for entry in removed_stories:
        story = entry['story']
        if is_cell_phone_policy(story):
            to_restore.append(entry)
            print(f"  📱 Restoring cell phone policy story: {story.get('title', 'Untitled')[:70]}")
    
    # Find stories to permanently remove (individual crimes/fights)
    permanently_removed = []
    for entry in removed_stories:
        story = entry['story']
        if is_individual_crime_or_fight(story):
            permanently_removed.append(entry)
            print(f"  🚫 Permanently removing crime/fight story: {story.get('title', 'Untitled')[:70]}")
    
    # Update removed list (remove both cell phone and crime stories)
    filtered_removed = [
        entry for entry in removed_stories
        if not is_cell_phone_policy(entry['story']) 
        and not is_individual_crime_or_fight(entry['story'])
    ]
    
    # Add restored stories back to kept
    for entry in to_restore:
        kept_stories.append(entry['story'])
    
    # Sort kept stories by date
    kept_stories.sort(key=lambda x: x.get('date', ''), reverse=True)
    
    print(f"\n📊 Summary:")
    print(f"   Cell phone stories restored: {len(to_restore)}")
    print(f"   Crime/fight stories removed: {len(permanently_removed)}")
    print(f"   Updated kept stories: {len(kept_stories)}")
    print(f"   Updated removed log: {len(filtered_removed)}")
    
    # Save updated files
    save_json(filtered_removed, removed_path)
    save_json(kept_stories, refined_path)
    
    print(f"\n💾 Updated files:")
    print(f"   {REMOVED_LOG}")
    print(f"   {REFINED_BEATBOOK}")
    
    # Show which cell phone stories were restored
    if to_restore:
        print(f"\n📱 Cell phone policy stories restored:")
        for entry in to_restore:
            story = entry['story']
            print(f"   • {story.get('title', 'Untitled')}")
            print(f"     Date: {story.get('date', 'Unknown')}")
            print(f"     Previous removal reason: {entry.get('reason', 'N/A')}")
    
    # Show which crime/fight stories were removed
    if permanently_removed:
        print(f"\n🚫 Individual crime/fight stories permanently removed:")
        for entry in permanently_removed:
            story = entry['story']
            print(f"   • {story.get('title', 'Untitled')}")
            print(f"     Date: {story.get('date', 'Unknown')}")

if __name__ == '__main__':
    main()
