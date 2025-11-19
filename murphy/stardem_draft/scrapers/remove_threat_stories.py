#!/usr/bin/env python3
"""
Remove individual threat/crime incident stories from beat book.
These are individual security incidents, not policy-relevant stories about systemic safety issues.
"""

import json

def is_individual_threat_or_crime(story):
    """
    Check if a story is about an individual threat or crime incident.
    These are not policy-relevant unless they lead to systemic changes.
    """
    title = story.get('title', '').lower()
    content = story.get('content', '').lower()
    
    # Threat/crime incident patterns
    threat_patterns = [
        'investigating another threat',
        'investigating threat',
        'bomb threat',
        'social media threat',
        'threat not specific',
        'students evacuated',
        'school bus crash',
        'student arrested',
        'student charged',
        'assault circulate',
        'videos of.*assault',
        'fight at school',
        'stabbing',
        'shooting at school'
    ]
    
    # Check if title matches threat/crime incident patterns
    for pattern in threat_patterns:
        if pattern in title:
            return True
    
    # Additional check: if it's primarily about a sheriff's office investigation of a specific incident
    if 'sheriff' in title and ('investigating' in title or 'threat' in title):
        # But NOT if it's about policy changes or systemic issues
        if 'policy' not in content and 'new protocol' not in content and 'changes to' not in content:
            return True
    
    return False

def main():
    # Load the current beat book
    with open('refined_beat_book_stories.json', 'r') as f:
        kept_stories = json.load(f)
    
    print(f"Loaded {len(kept_stories)} kept stories")
    print()
    
    # Find threat/crime stories to remove
    to_remove = []
    for story in kept_stories:
        if is_individual_threat_or_crime(story):
            to_remove.append(story)
            county = story.get('counties', ['Unknown'])[0] if story.get('counties') else 'Unknown'
            print(f"Found threat/crime story to remove:")
            print(f"  County: {county}")
            print(f"  Title: {story.get('title', 'No title')}")
            print(f"  Date: {story.get('date', 'No date')}")
            print()
    
    if not to_remove:
        print("No threat/crime incident stories found to remove.")
        return
    
    print(f"\nRemoving {len(to_remove)} threat/crime incident stories...")
    
    # Create removal log entries
    removal_entries = []
    for story in to_remove:
        removal_entries.append({
            "story": story,
            "reason": "Individual security/crime incident without policy implications",
            "confidence": 0.95
        })
        kept_stories.remove(story)
    
    # Load and update removed stories log
    try:
        with open('removed_stories_log.json', 'r') as f:
            removed_log = json.load(f)
    except FileNotFoundError:
        removed_log = []
    
    removed_log.extend(removal_entries)
    
    # Save updated files
    with open('refined_beat_book_stories.json', 'w') as f:
        json.dump(kept_stories, f, indent=2)
    
    with open('removed_stories_log.json', 'w') as f:
        json.dump(removed_log, f, indent=2)
    
    print(f"\n✓ Removed {len(to_remove)} threat/crime incident stories")
    print(f"✓ Updated beat book now has {len(kept_stories)} stories")
    print(f"✓ Removed log now has {len(removed_log)} stories")
    
    # Print titles of removed stories
    print(f"\nRemoved stories:")
    for story in to_remove:
        print(f"  - {story.get('title', 'No title')}")

if __name__ == '__main__':
    main()
