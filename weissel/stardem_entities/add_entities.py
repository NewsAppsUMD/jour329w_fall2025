import json
import re
import subprocess
import time
import argparse
import sys
from pathlib import Path

def extract_metadata(story_title, story_content, schema_prompt, model):
    """Use LLM to extract structured metadata from story title and summary."""
    prompt = f"""
Extract metadata from this news story in JSON format using only the title and summary provided.

Schema to follow:
{schema_prompt}

Story Title: {story_title}
Story Summary: {story_content}

Return only valid JSON with the metadata. If information is not available, use an empty array:
"""
    
    try:
        result = subprocess.run([
            'llm', '-m', model, prompt
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Parse and validate the JSON response
            response_text = result.stdout.strip()
            # Remove any markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('\n', 1)[1]
                response_text = response_text.rsplit('\n', 1)[0]
            
            metadata = json.loads(response_text)
            return metadata
        else:
            return {"error": "LLM failed", "stderr": result.stderr}
    except Exception as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description='Add metadata to CNS beat stories using LLM')
    parser.add_argument('--model', required=True, help='LLM model to use (e.g., gpt-4o-mini, claude-3.5-haiku)')
    parser.add_argument('--input', default='story_summaries_elections.json', help='Input JSON file with stories')
    parser.add_argument('--sports-json', help='Optional path to a sports JSON file whose metadata should be merged into matching stories')

    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    # If a sports json is supplied, try to load it and build an index for quick lookup
    sports_index = {}
    if args.sports_json:
        sports_path = Path(args.sports_json)
        if sports_path.exists():
            try:
                with open(sports_path) as sf:
                    sports_data = json.load(sf)
                # sports_data likely a list of objects; create simple lookup by id or title
                if isinstance(sports_data, list):
                    for item in sports_data:
                        # prefer explicit id keys
                        sid = None
                        for candidate in ('id', 'story_id', 'article_id'):
                            if isinstance(item, dict) and candidate in item:
                                sid = str(item[candidate])
                                break
                        if sid:
                            sports_index[('id', sid)] = item
                        # also index by title if present
                        title = item.get('title') if isinstance(item, dict) else None
                        if title:
                            sports_index[('title', str(title).strip().lower())] = item
                elif isinstance(sports_data, dict):
                    # If the file is an object keyed by id or title, just store it
                    for k, v in sports_data.items():
                        sports_index[('id', str(k))] = v
            except Exception as e:
                print(f"Warning: failed to load sports json '{args.sports_json}': {e}")
        else:
            print(f"Warning: sports json path '{args.sports_json}' does not exist; continuing without sports metadata")

    # Define your schema prompt based on your beat - CUSTOMIZE THIS!
    # Make keys lowercase, use underscores and provide example values so the LLM
    # returns consistent field names (this helps avoid duplicate/variant columns).
    # We want the LLM to extract three arrays: people, places, organizations.
    # Provide an explicit example in the schema so the model returns consistent keys
    # and short name tokens. The LLM should return JSON like the example.
    schema_prompt = """
        {
            "sport": "football",                       # single-word sport name (string)
            "story_type": "game recap",                # e.g., "game recap", "feature", "preview" (string)
            "location": "Easton, Maryland",            # city, state or short location string (string)
            "teams": ["Patriots", "Red Sox"],        # list of team names mentioned (array)
            "schools": ["Newton South High School"],  # list of school names when relevant (array)
            "people": ["Tom Brady"],                  # list of important people (array)
            "quoted_people": ["Coach John Smith"],    # list of all people who are quoted directly or paraphrased in the story (array)
            "level_of_play": "high school",           # e.g., "high school", "college", "professional" (string)
            "competition_type": "regular season",    # e.g., "regular season", "playoffs", "tournament" (string)
            "venue": "War Memorial Stadium",          # stadium/venue name (string)
            "outcome": "Easton 28, Cambridge 14",    # game score or outcome; if not a game, short outcome like "win","loss","tie" (string)
            "importance": 7,                            # numeric importance on a 1-10 scale (integer)
            "audience_blurb": "A brief 1-2 sentence blurb describing the most likely target audience for this story." # short textual blurb
        }

        IMPORTANT: Use the exact lowercase keys shown above with underscores (e.g., `level_of_play`).
        - Return JSON using these keys. For list fields (teams, schools, people, quoted_people) return an array; for single-valued fields return a string or integer as appropriate.
        - `importance` should be an integer between 1 and 10 (1 = minor/preseason, 10 = championship/major).
        - `quoted_people` must include all named people who are quoted in the story, whether a direct quote ("...") or a paraphrase attributed to a named source. Include role/title if available (e.g., "Coach John Smith").
        - `audience_blurb` should be a concise 1-2 sentence description of the story's most likely target audience (e.g., "Local high-school sports fans and families; readers interested in Easton High athletics").
        - If a value is not available, return an empty array for list fields, an empty string for textual fields, and 0 for numeric fields if unknown.
        - For `people`, include only the most important named individuals (primary sources, coaches, star players). Do NOT include the author/byline.
        - Keep arrays short (top 3-5 most relevant people/teams) and use consistent naming across stories.
        Example desired output for a short sports story:
        {
            "sport": "football",
            "story_type": "game recap",
            "location": "Easton, Maryland",
            "teams": ["Easton High School", "Cambridge High School"],
            "schools": ["Easton High School", "Cambridge High School"],
            "people": ["Coach John Smith", "Quarterback Joe Jones"],
            "quoted_people": ["Coach John Smith", "Quarterback Joe Jones"],
            "level_of_play": "high school",
            "competition_type": "regular season",
            "venue": "War Memorial Stadium",
            "outcome": "Easton 28, Cambridge 14",
            "importance": 8,
            "audience_blurb": "Local high-school sports fans and families; readers interested in Easton High athletics."
        }
        """

    # Load your beat stories
    try:
        with open(args.input) as f:
            stories = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find input file '{args.input}'")
        print("Make sure to update the --input parameter to match your topic file!")
        return

    # Process each story
    enhanced_stories = []
    for i, story in enumerate(stories):
        print(f"Processing {i+1}/{len(stories)}: {story.get('title', '<no title>')}")

        # prefer full article content when available
        story_content = story.get('content') or story.get('summary') or ''
        metadata = extract_metadata(story.get('title', ''), story_content, schema_prompt, args.model)

        # Add metadata fields as separate columns instead of nested object
        enhanced_story = story.copy()

        # If metadata extraction was successful, add people/places/organizations as JSON arrays
        if isinstance(metadata, dict) and 'error' not in metadata:
            # expected entity keys
            for key in ('people', 'places', 'organizations'):
                val = metadata.get(key, [])
                # ensure it's a list
                if not isinstance(val, list):
                    # if the model returned a single string, wrap it
                    if isinstance(val, str) and val.strip():
                        val = [v.strip() for v in re.split(r'[;,]\s*', val) if v.strip()]
                    else:
                        val = []

                # Post-process to enforce policy: prioritize important people,
                # limit places to 3, and keep organizations as returned.
                if key == 'people':
                    # Remove the author/byline if present
                    author = story.get('author') or story.get('byline') or ''
                    def normalize_name(n):
                        return n.strip()

                    # dedupe while preserving order
                    seen = set(); deduped = []
                    for x in val:
                        k = normalize_name(x)
                        if not k: continue
                        if author and k.lower() == author.strip().lower():
                            continue
                        if k not in seen:
                            seen.add(k); deduped.append(k)

                    # simple prioritization: prefer entries containing role/title
                    role_words = ('Mayor', 'Senator', 'Representative', 'Judge', 'Dr', 'Mr', 'Mrs', 'Ms', 'Chief', 'Sheriff', 'Officer', 'Coach', 'President', 'Principal')
                    story_text = (story.get('title') or '') + '\n' + (story_content or '')

                    def person_score(name, idx):
                        score = 0
                        lname = name.lower()
                        st = story_text.lower()
                        # role/title presence is a strong signal
                        for rw in role_words:
                            if rw.lower() in name.lower():
                                score += 4
                        # frequency of mentions is important
                        freq = st.count(lname)
                        score += min(freq, 5) * 1.5
                        # earlier appearance is better
                        pos = st.find(lname)
                        if pos != -1:
                            # earlier -> higher score
                            score += max(0, 3 - (pos / 200.0))
                        # shorter names slightly preferred
                        score += max(0, 1 - (len(name.split()) - 2) * 0.1)
                        return (-score, idx)

                    scored = sorted([(person_score(p, i), p) for i, p in enumerate(deduped)], key=lambda x: x[0])
                    prioritized = [p for _, p in scored]
                    # Keep only likely human first+last names (two tokens, capitalized)
                    def is_human_name(n):
                        # Allow letters, hyphens and apostrophes in names
                        m = re.match(r"^[A-Z][A-Za-z'\-]+\s+[A-Z][A-Za-z'\-]+$", n)
                        if not m:
                            return False
                        # exclude organization-like tokens
                        org_tokens = ('County','School','District','Commission','Commissioners','Board','Department','Inc','Company','Association','Committee','Publishing','Press','Times','Record','Observer','News','Document')
                        for t in org_tokens:
                            if t in n:
                                return False
                        # filter out likely team/place fragments that look like two words
                        block_words = ('High','School','Conference','Athletic','Saints','Royals','Bucs','Sabres','Kings','Lady','Saint','Team','Delmarva','Star','Democrat','Christian','Eastern','Shore','Independent','Publishing','Press','Times','Record','Observer','News','Document')
                        for part in n.split():
                            if part in block_words:
                                return False
                        return True

                    human_only = [p for p in prioritized if is_human_name(p)]
                    # Keep ONLY human-looking first+last names; if none found, leave empty
                    val = human_only[:4]

                if key == 'places':
                    # dedupe and keep only the top 3 places (most relevant)
                    seen = set(); places_ordered = []
                    for p in val:
                        k = p.strip()
                        if not k: continue
                        if k not in seen:
                            seen.add(k); places_ordered.append(k)
                    val = places_ordered[:3]

                # write out as JSON string in the story record, but skip empty lists
                if val:
                    enhanced_story[f'entities_{key}'] = json.dumps(val)
            # keep any additional fields (optional) as metadata_ prefixed columns
            for key, value in metadata.items():
                if key in ('people', 'places', 'organizations'):
                    continue
                # Special handling for quoted_people (store as entities_quoted_people)
                if key == 'quoted_people':
                    q = value if isinstance(value, list) else ([v.strip() for v in re.split(r'[;,]\s*', value)] if isinstance(value, str) and value.strip() else [])
                    # dedupe and keep order
                    seen_q = set(); q_ordered = []
                    for name in q:
                        n = name.strip()
                        if not n: continue
                        if n not in seen_q:
                            seen_q.add(n); q_ordered.append(n)
                    enhanced_story['entities_quoted_people'] = json.dumps(q_ordered)
                    continue

                # Special handling for importance (ensure integer 1-10)
                if key == 'importance':
                    imp = None
                    try:
                        imp = int(value)
                    except Exception:
                        # try to parse from string like "7" or "7/10"
                        if isinstance(value, str):
                            m = re.search(r"(\d+)", value)
                            if m:
                                imp = int(m.group(1))
                    if imp is None:
                        imp = 0
                    # clamp to 1-10 if in range, else leave as 0
                    if imp < 1 or imp > 10:
                        # allow 0 as unknown
                        pass
                    enhanced_story['metadata_importance'] = imp
                    continue

                # Special handling for audience blurb: store and also append to content preview
                if key in ('audience_blurb', 'target_audience'):
                    blurb = value if isinstance(value, str) else ''
                    enhanced_story['metadata_audience_blurb'] = blurb
                    # also add a content copy with the audience blurb appended for quick viewing
                    try:
                        base = story.get('content') or story.get('summary') or ''
                        if blurb and base:
                            enhanced_story['content_with_audience_blurb'] = base + "\n\nAudience: " + blurb
                        else:
                            enhanced_story['content_with_audience_blurb'] = base
                    except Exception:
                        enhanced_story['content_with_audience_blurb'] = story.get('content') or story.get('summary') or ''
                    continue

                norm_key = key.strip().lower().replace(' ', '_').replace('-', '_')
                col_name = f'metadata_{norm_key}'
                enhanced_story[col_name] = json.dumps(value) if isinstance(value, list) else value
        else:
            # If there was an error, add error information
            enhanced_story['metadata_error'] = (metadata.get('error') if isinstance(metadata, dict) else str(metadata)) or 'Unknown error'

        # If we have sports metadata loaded, try to match and merge it into the story
        if sports_index:
            matched = None
            # match by id if present
            sid = story.get('id') or story.get('story_id') or story.get('article_id')
            if sid and ('id', str(sid)) in sports_index:
                matched = sports_index[('id', str(sid))]
            # match by title (case-insensitive exact)
            if not matched:
                title_key = (story.get('title') or '').strip().lower()
                if title_key and ('title', title_key) in sports_index:
                    matched = sports_index[('title', title_key)]
            # fallback: substring match on titles
            if not matched:
                stitle = (story.get('title') or '').strip().lower()
                if stitle:
                    for (kind, key), item in sports_index.items():
                        if kind == 'title' and key in stitle:
                            matched = item
                            break

            if matched:
                # merge sports metadata into story with sports_ prefix
                for k, v in (matched.items() if isinstance(matched, dict) else []):
                    col = f'sports_{str(k).strip().lower().replace(" ", "_")}'
                    enhanced_story[col] = json.dumps(v) if isinstance(v, (list, dict)) else v

        enhanced_stories.append(enhanced_story)

        # Be respectful to the API
        time.sleep(1)

    # Save the enhanced collection (stories_with_entities.json per assignment)
    with open('stories_with_entities3.json', 'w') as f:
        json.dump(enhanced_stories, f, indent=2)

    print(f"Processed {len(enhanced_stories)} stories with metadata")

if __name__ == "__main__":
    main()
