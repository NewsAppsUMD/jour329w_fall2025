import json
import subprocess
import re
import argparse
import sys

# --- County and municipality mapping setup ---
maryland_county_list = [
    {
        "county": "Dorchester County",
        "municipalities": "Brookview, Cambridge, Church Creek, Crapo, Crocheron, East New Market, Eldorado, Fishing Creek, Galestown, Hurlock, Linkwood, Madison, Rhodesdale, Secretary, Taylors Island, Toddville, Vienna, Wingate, Woolford"
    },
    {
        "county": "Caroline County",
        "municipalities": "Denton, Federalsburg, Goldsboro, Greensboro, Henderson, Hillsboro, Marydel, Preston, Ridgely, Templeville, Choptank, West Denton, Williston, American Corner, Andersontown, Baltimore Corner, Bethlehem, Brick Wall Landing, Burrsville, Gilpin Point, Harmony, Hickman, Hobbs, Jumptown, Linchester, Oakland, Oil City, Tanyard, Two Johns, Reliance, Whiteleysburg"
    },
    {
        "county": "Kent County",
        "municipalities": "Betterton, Chestertown, Galena, Millington, Rock Hall, Butlertown, Chesapeake Landing, Edesville, Fairlee, Georgetown, Kennedyville, Still Pond, Tolchester, Worton, Chesterville, Golts, Hassengers Corner, Langford, Lynch, Massey, Pomona, Sassafras, Sharpstown, Tolchester Beach"
    },
    {
        "county": "Queen Anne's County",
        "municipalities": "Barclay, Centreville, Church Hill, Millington, Queen Anne, Queenstown, Sudlersville, Templeville, Chester, Grasonville, Kent Narrows, Kingstown, Romancoke, Stevensville, Crumpton, Dominion, Ingleside, Love Point, Matapeake, Price, Ruthsburg"
    },
    {
        "county": "Talbot County",
        "municipalities": "Easton, Oxford, Queen Anne, Saint Michaels, Trappe, Cordova, Tilghman Island, Anchorage, Bellevue, Bozman, Claiborne, Copperville, Doncaster, Fairbanks, Lewistown, Lloyd Landing, Matthews, McDaniel, Neavitt, Newcomb, Royal Oak, Sherwood, Tunis Mills, Unionville, Wittman, Windy Hill, Woodland, Wye Mills, Dover, York, Wyetown"
    }
]

municipality_to_county = {}
all_municipalities = set()
all_counties = set()
for entry in maryland_county_list:
    county = entry["county"]
    all_counties.add(county)
    for muni in entry["municipalities"].split(","):
        muni = muni.strip()
        municipality_to_county[muni] = county
        all_municipalities.add(muni)

county_names = list(all_counties)

def fix_county_field(story):
    counties = set()
    # From municipalities
    municipalities = [m.strip() for m in str(story.get("municipalities", "")).split(";") if m.strip() and m.strip() != "N/A"]
    for muni in municipalities:
        county = municipality_to_county.get(muni)
        if county:
            counties.add(county)
    # From events and institutions (if county name appears in string)
    for field in ["events", "institutions"]:
        field_val = story.get(field, "")
        if isinstance(field_val, list):
            # Handle list items that might be strings or dicts
            joined_val = " ".join(str(item) for item in field_val)
        else:
            joined_val = str(field_val)
        for county_name in county_names:
            if county_name in joined_val:
                counties.add(county_name)
    # From locations (if county name appears in string)
    locations_val = story.get("locations", "")
    if isinstance(locations_val, list):
        # Handle list items that might be strings or dicts
        joined_loc = " ".join(str(item) for item in locations_val)
    else:
        joined_loc = str(locations_val)
    for county_name in county_names:
        if county_name in joined_loc:
            counties.add(county_name)
    if counties:
        story["county"] = "; ".join(sorted(counties))
    else:
        story["county"] = "N/A"
    return story

def clean_fields(story):
    # Only allow real municipalities in municipalities field
    municipalities = [m.strip() for m in str(story.get("municipalities", "")).split(";") if m.strip()]
    municipalities = [m for m in municipalities if m in all_municipalities]
    story["municipalities"] = "; ".join(sorted(set(municipalities))) if municipalities else "N/A"

    # Only allow real counties in county field
    counties = [c.strip() for c in str(story.get("county", "")).split(";") if c.strip()]
    counties = [c for c in counties if c in all_counties]
    story["county"] = "; ".join(sorted(set(counties))) if counties else "N/A"

    # Remove municipalities and counties from locations field
    locations = [l.strip() for l in str(story.get("locations", "")).split(";") if l.strip()]
    locations = [l for l in locations if l not in all_municipalities and l not in all_counties]
    story["locations"] = "; ".join(locations) if locations else "N/A"

    return story

def extract_first_json(text):
    # Find the first { and then match braces to find the complete JSON object
    start = text.find('{')
    if start == -1:
        raise ValueError("No JSON object found in LLM output.")
    
    brace_count = 0
    in_string = False
    escape_next = False
    
    for i in range(start, len(text)):
        char = text[i]
        
        if escape_next:
            escape_next = False
            continue
            
        if char == '\\':
            escape_next = True
            continue
            
        if char == '"' and not escape_next:
            in_string = not in_string
            continue
            
        if not in_string:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    return text[start:i+1]
    
    raise ValueError("No complete JSON object found in LLM output.")

INSTRUCTIONS = """
You are extracting structured metadata from news articles. Extract and return ONLY a JSON object with these fields: content_type, people, events, locations, municipalities, county, institutions.

CONTENT_TYPE: Choose the single best-fitting type:
- "News": Full articles about politics, elections, government, agriculture, education, housing, economy, transportation, infrastructure, public safety, crime, environment, arts, society and community. Excludes calendars, obituaries, legal notices, opinion pieces.
- "Sports": Full articles about local sports topics and teams (excludes professional teams, calendars, listings).
- "Calendars": Event calendars and listings.
- "Obituaries": Obituaries only.
- "Legal Notices": Legal notices only.
- "Opinion": Columns, editorials, letters to the editor meant to persuade.
- "Miscellaneous": TV listings, Today in History, and other non-news/non-opinion content.

PEOPLE: List all people mentioned or quoted, separated by ";". Standardize names across stories. Exclude the article author.

EVENTS: List ONLY specific named events with proper names (conferences, festivals, races, competitions, ceremonies, fundraisers, etc.), separated by ";". Examples: "Maryland Ironman", "Bayside Conference championship", "Martin Luther King Jr. Day march". DO NOT include generic activities like "listening sessions", "meetings", "feedback submission", "briefings". If no named events, use "N/A".

LOCATIONS: List ONLY physical geographic places WITHIN municipalities, separated by ";". Include: rivers, creeks, bays, parks, wildlife refuges, neighborhoods, street names, bridges, specific buildings/landmarks. Spell out abbreviated street suffixes (St. → Street, Ave. → Avenue, Rd. → Road). Do NOT include street numbers. Include municipality in parentheses when known, e.g., "Market Street (Denton)". DO NOT include: websites, URLs, email addresses, municipality names, county names, or institution names. If no physical locations, use "N/A".

MUNICIPALITIES: List municipalities mentioned or central to the story, separated by ";". Use only these valid municipalities from the five Maryland counties:
- Dorchester County: Brookview, Cambridge, Church Creek, Crapo, Crocheron, East New Market, Eldorado, Fishing Creek, Galestown, Hurlock, Linkwood, Madison, Rhodesdale, Secretary, Taylors Island, Toddville, Vienna, Wingate, Woolford
- Caroline County: Denton, Federalsburg, Goldsboro, Greensboro, Henderson, Hillsboro, Marydel, Preston, Ridgely, Templeville, Choptank, West Denton, Williston, American Corner, Andersontown, Baltimore Corner, Bethlehem, Brick Wall Landing, Burrsville, Gilpin Point, Harmony, Hickman, Hobbs, Jumptown, Linchester, Oakland, Oil City, Tanyard, Two Johns, Reliance, Whiteleysburg
- Kent County: Betterton, Chestertown, Galena, Millington, Rock Hall, Butlertown, Chesapeake Landing, Edesville, Fairlee, Georgetown, Kennedyville, Still Pond, Tolchester, Worton, Chesterville, Golts, Hassengers Corner, Langford, Lynch, Massey, Pomona, Sassafras, Sharpstown, Tolchester Beach
- Queen Anne's County: Barclay, Centreville, Church Hill, Millington, Queen Anne, Queenstown, Sudlersville, Templeville, Chester, Grasonville, Kent Narrows, Kingstown, Romancoke, Stevensville, Crumpton, Dominion, Ingleside, Love Point, Matapeake, Price, Ruthsburg
- Talbot County: Easton, Oxford, Queen Anne, Saint Michaels, Trappe, Cordova, Tilghman Island, Anchorage, Bellevue, Bozman, Claiborne, Copperville, Doncaster, Fairbanks, Lewistown, Lloyd Landing, Matthews, McDaniel, Neavitt, Newcomb, Royal Oak, Sherwood, Tunis Mills, Unionville, Wittman, Windy Hill, Woodland, Wye Mills, Dover, York, Wyetown

EXCLUDE "Easton" if only mentioned in dateline as Star-Democrat location. If no valid municipality, use "N/A".

COUNTY: List counties where mentioned municipalities are located, separated by ";". Match municipalities to these counties:
- Dorchester County, Caroline County, Kent County, Queen Anne's County, Talbot County
Use title case. If no relation to listed counties, use "N/A".

INSTITUTIONS: List organizations, businesses, government agencies, councils, boards, teams, and institutions, separated by ";". Standardize names across stories. EXCLUDE "Star Democrat", "Chesapeake Publishing Group", and "Adams Publishing/APGMedia". INCLUDE other news organizations if article written by them. Libraries, schools, businesses hosting events are institutions (NOT locations). If institution name matches event name, include in BOTH fields.

SPORTS ARTICLES: Teams have multiple names (e.g., "Stephen Decatur High School Seahawks" = "Stephen Decatur" = "Decatur" = "Seahawks"). These are institutions, NOT people.

Return ONLY valid JSON with these exact field names. Use semicolon separators for lists.
"""

def process_stories(input_file, output_file, model="groq/meta-llama/llama-4-scout-17b-16e-instruct"):
    print(f"Script started. Input: {input_file} | Output: {output_file} | Model: {model}")
    try:
        with open(input_file, 'r') as f:
            stories = json.load(f)
    except Exception as e:
        print(f"ERROR: Could not open input file '{input_file}': {e}")
        sys.exit(1)

    updated_stories = []
    total_stories = len(stories)

    for index, story in enumerate(stories):
        print(f"Processing story {index + 1} of {total_stories}...")

        prompt = (
            INSTRUCTIONS
            + "\n\nSTORY:\n"
            + json.dumps(story, ensure_ascii=False)
            + "\n\nReturn only the updated JSON object."
        )

        try:
            result = subprocess.run(
                ["llm", "-m", model],
                input=prompt,
                capture_output=True,
                text=True
            )
        except Exception as e:
            print(f"ERROR: LLM subprocess failed for story {index+1}: {e}")
            story = fix_county_field(story)
            story = clean_fields(story)
            updated_stories.append(story)
            continue

        if result.returncode == 0 and result.stdout.strip():
            output = result.stdout.strip()
            try:
                json_str = extract_first_json(output)
                llm_output = json.loads(json_str)
                # Merge LLM output with original story to preserve metadata
                story_out = story.copy()
                story_out.update(llm_output)
                story_out = fix_county_field(story_out)
                story_out = clean_fields(story_out)
                updated_stories.append(story_out)
            except Exception as e:
                print(f"Failed to parse JSON for story {index+1}: {e}")
                story = fix_county_field(story)
                story = clean_fields(story)
                updated_stories.append(story)
        else:
            print(f"Error processing story {index+1}: {result.stderr}")
            story = fix_county_field(story)
            story = clean_fields(story)
            updated_stories.append(story)

        # Save after every 10 stories
        if (index + 1) % 10 == 0:
            try:
                with open(output_file, 'w') as f:
                    json.dump(updated_stories, f, indent=2, ensure_ascii=False)
                print(f"Progress saved after {index + 1} stories.")
            except Exception as e:
                print(f"ERROR: Could not write output file after {index+1} stories: {e}")

    # Final save
    try:
        with open(output_file, 'w') as f:
            json.dump(updated_stories, f, indent=2, ensure_ascii=False)
        print(f"Done. Saved {len(updated_stories)} stories to {output_file}")
    except Exception as e:
        print(f"ERROR: Could not write final output file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='stardem_sample.json', help='Input JSON file')
    parser.add_argument('--output', default='stories_with_entities_1.json', help='Output JSON file')
    parser.add_argument('--model', default='groq/meta-llama/llama-4-scout-17b-16e-instruct', help='LLM model name')
    args = parser.parse_args()
    process_stories(args.input, args.output, args.model)
