import json
import subprocess

def generate_beatbook_section(entities, stories_sample, prompt_type, model):
    """Generate a beat book section based on entities and stories."""
    
    if prompt_type == "source_profiles":
        prompt = f"""Based on these news stories about [TOPIC], create profiles of the 5 most important sources a reporter should know.

Key people mentioned: {entities['top_people']}
Key organizations: {entities['top_organizations']}
Sample story titles: {stories_sample}

For each source, provide:
- Name and title
- Why they matter to this beat
- What topics they can speak to
- Contact approach recommendations

Write in a concise, professional style suitable for a reporter's reference guide.
"""
    
    elif prompt_type == "story_opportunities":
        prompt = f"""Based on this beat's coverage patterns, suggest 10 story ideas a reporter should pursue.

Coverage analysis:
- Key people: {entities['top_people']}
- Key places: {entities['top_places']}
- Key organizations: {entities['top_organizations']}
- Recent story themes: {stories_sample}

For each story idea, provide:
- Story angle/headline
- Why it matters
- Who to interview
- What data/documents to get

Focus on enterprise stories, not breaking news.
"""
    
    # Add more prompt types as you experiment
    
    result = subprocess.run(
        ['llm', '-m', model, prompt],
        capture_output=True,
        text=True,
        check=True
    )
    
    return result.stdout.strip()

def main():
    # Load entity-enriched stories
    with open('stories_with_entities.json') as f:
        stories = json.load(f)
    
    # Aggregate entity information
    entities = aggregate_entities(stories)
    
    # Generate different sections
    sections = {
        'source_profiles': generate_beatbook_section(entities, stories[:10], 'source_profiles', model),
        'story_opportunities': generate_beatbook_section(entities, stories[:10], 'story_opportunities', model),
        # Add more sections
    }
    
    # Save to markdown
    save_beatbook(sections, 'beatbook_draft_v1.md')

# Implement helper functions