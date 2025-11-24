import json
import re
import subprocess
import time
import argparse
import sys
from pathlib import Path

# Maryland county/municipality list (used for local place detection)
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
    },
    {
        "county": "Prince George's County",
        "municipalities": "Bowie, College Park, District Heights, Glenarden, Greenbelt, Hyattsville, Laurel, Mount Rainier, New Carrollton, Seat Pleasant, Berwyn Heights, Bladensburg, Brentwood, Capitol Heights, Cheverly, Colmar Manor, Cottage City, Eagle Harbor, Edmonston, Fairmount Heights, Forest Heights, Landover Hills, Morningside, North Brentwood, Riverdale Park, University Park, Upper Marlboro"
    },
    {
        "county": "Calvert County",
        "municipalities": "Adelina, Barstow, Bowens, Chaneyville, Dares Beach, Dowell, Johnstown, Lower Marlboro, Mutual, Parran, Pleasant Valley, Port Republic, Scientists Cliffs, Stoakley, Sunderland, Wallville, Wilson, Chesapeake Beach, North Beach, Broomes Island, Calvert Beach, Chesapeake Ranch Estates, Drum Point, Dunkirk, Huntingtown, Long Beach, Lusby, Owings, Prince Frederick, St. Leonard, Solomons"
    },
    {
        "county": "Anne Arundel County",
        "municipalities": "Annapolis, Highland Beach, Annapolis Neck, Arden on the Severn, Arnold, Brooklyn Park, Cape Saint Claire, Crofton, Crownsville, Deale, Edgewater, Ferndale, Fort Meade, Friendship, Galesville, Gambrills, Glen Burnie, Herald Harbor, Jessup, Lake Shore, Linthicum, Maryland City, Mayo, Naval Academy, Odenton, Parole, Pasadena, Riva, Riviera Beach, Selby-on-the-Bay, Severn, Severna Park, Shady Side, Beverly Beach, Bristol, Chestnut Hill Cove, Churchton, Davidsonville, Fairhaven, Germantown, Gibson Island, Green Haven, Hanover, Harmans, Harundale, Harwood, Hillsmere Shores, Jacobsville, Londontowne, Lothian, Millersville, Orchard Beach, Owensville, Pumphrey, Riverdale, Rose Haven, Russett, Sherwood Forest, South Gate, Sudley, Tracys Landing, Waysons Corner, West River, Winchester-on-the-Severn, Woodland Beach"
    },
    {
        "county": "Baltimore County",
        "municipalities": "Arbutus, Baltimore Highlands, Bowleys Quarters, Carney, Catonsville, Cockeysville, Dundalk, Edgemere, Essex, Garrison, Hampton, Honeygo, Kingsville, Lansdowne, Lochearn, Lutherville, Mays Chapel, Middle River, Milford Mill, Overlea, Owings Mills, Parkville, Perry Hall, Pikesville, Randallstown, Reisterstown, Rosedale, Rossville, Timonium, Towson, White Marsh, Woodlawn, Baldwin, Boring, Bradshaw, Brooklandville, Butler, Chase, Fork, Fort Howard, Germantown, Glen Arm, Glencoe, Glyndon, Halethorpe, Hereford, Hunt Valley, Hydes, Jacksonville, Long Green, Maryland Line, Monkton, Nottingham, Oella, Parkton, Phoenix, Ruxton, Sparks, Sparrows Point, Stevenson, Trump, Turners Station, Upper Falls, Upperco, White Hall"
    },
    {
        "county": "Baltimore City",
        "municipalities": "Baltimore City"
    },
    {
        "county": "Howard County",
        "municipalities": "Columbia, Elkridge, Ellicott City, Fulton, Highland, Ilchester, Jessup, Lisbon, North Laurel, Savage, Scaggsville, Clarksville, Cooksville, Daniels, Dayton, Dorsey, Glenelg, Glenwood, Granite, Guilford, Hanover, Isaacsville, Marriottsville, Simpsonville, West Friendship, Woodbine, Woodstock"
    },
    {
        "county": "Carroll County",
        "municipalities": "Westminster, Taneytown, Manchester, Mount Airy, New Windsor, Union Bridge, Hampstead, Sykesville, Eldersburg, Alesia, Carrollton, Carrolltowne, Detour, Finksburg, Frizzelburg, Gamber, Gaither, Greenmount, Harney, Henryton, Jasontown, Keymar, Lineboro, Linwood, Marriottsville, Mayberry, Middleburg, Millers, Patapsco, Pleasant Valley, Silver Run, Union Mills, Uniontown, Woodbine, Woodstock"
    },
    {
        "county": "Montgomery County",
        "municipalities": "Gaithersburg, Rockville, Takoma Park, Barnesville, Brookeville, Chevy Chase, Chevy Chase View, Chevy Chase Village, Garrett Park, Glen Echo, Kensington, Laytonsville, Poolesville, Somerset, Washington Grove, Martin's Additions, North Chevy Chase, Drummond, Oakmont."
    },
    {
        "county": "Frederick County",
        "municipalities": "Brunswick, Frederick, Burkittsville, Emmitsburg, Middletown, Mount Airy, Myersville, New Market, Thurmont, Walkersville, Woodsboro, Rosemont, Adamstown, Ballenger Creek, Bartonsville, Braddock Heights, Buckeystown, Graceham, Green Valley, Jefferson, Lewistown, Libertytown, Linganore, Monrovia, Point of Rocks, Sabillasville, Spring Ridge, Urbana, Charlesville, Clover Hill, Creagerstown, Discovery, Garfield, Ijamsville, Knoxville, Ladiesburg, Lake Linganore, Linganore, Mountaindale, Mount Pleasant, New Midway, Petersville, Rocky Ridge, Spring Garden, Sunny Side, Tuscarora, Unionville, Utica, Wolfsville"
    },
    {
        "county": "St. Mary's County",
        "municipalities": "Leonardtown, California, Callaway, Charlotte Hall, Golden Beach, Lexington Park, Mechanicsville, Piney Point, St. George Island, Tall Timbers, Wildewood, Abell, Avenue, Beachville-St. Inigoes, Beauvue, Bushwood, Chaptico, Clements, Coltons Point, Compton, Dameron, Drayden, Great Mills, Helen, Hollywood, Hopewell, Huntersville, Hurry, Loveville, Maddox, Morganza, Oakley, Oakville, Oraville, Park Hall, Ridge, St. Inigoes, St. Mary’s City, Scotland, Spencers Wharf, Valley Lee"
    },
    {
        "county": "Charles County",
        "municipalities": "Indian Head, La Plata, Port Tobacco Village, Benedict, Bensville, Bryans Road, Bryantown, Charlotte Hall, Cobb Island, Hughesville, Pomfret, Potomac Heights, Rock Point, Waldorf, Bel Alton, Dentsville, Faulkner, Glymont, Grayton, Ironsides, Issue, Malcolm, Marbury, Morgantown, Mount Victoria, Nanjemoy, Newburg, Pisgah, Popes Creek, Port Tobacco, Pomonkey, Ripley, Rison, Saint Charles, Swan Point, Welcome, White Plains"
    },
    {
        "county": "Washington County",
        "municipalities": "Hagerstown, Boonsboro, Clear Spring, Funkstown, Hancock, Keedysville, Sharpsburg, Smithsburg, Williamsport, Antietam, Bagtown, Bakersville, Beaver Creek, Big Pool, Big Spring, Breathedsville, Brownsville, Cavetown, Cearfoss, Charlton, Chewsville, Dargan, Downsville, Eakles Mill, Edgemont, Ernstville, Fairplay, Fairview, Fort Ritchie, Fountainhead-Orchard Hills, Gapland, Garretts Mill, Greensburg, Halfway, Highfield-Cascade, Indian Springs, Jugtown, Kemps Mill, Leitersburg, Mapleville, Maugansville, Mercersville, Middleburg, Mount Aetna, Mount Briar, Mount Lena, Paramount-Long Meadow, Pecktonville, Pinesburg, Pondsville, Reid, Ringgold, Robinwood, Rohrersville, Saint James, San Mar, Sandy Hook, Tilghmanton, Trego-Rohrersville Station, Wilson-Conococheague, Yarrowsburg, Appletown, Benevola, Broadfording, Burtner, Huyett, Pen Mar, Samples Manor, Spielman, Trego, Van Lear, Weverton, Woodmont, Zittlestown"
    },
    {
        "county": "Somerset County",
        "municipalities": "Crisfield, Princess Anne, Chance, Dames Quarter, Deal Island, Eden, Fairmount, Frenchtown-Rumbly, Mount Vernon, Smith Island, West Pocomoke, Ewell, Kingston, Manokin, Marion Station, Oriole, Rehobeth, Rhodes Point, Shelltown, Tylerton, Upper Fairmount, Upper Falls, Wenona, Westover"
    },
    {
        "county": "Allegany County",
        "municipalities": "Cumberland, Frostburg, Barton, Lonaconing, Luke, Midland, Westernport, Bel Air, Bowling Green, Cresaptown, Ellerslie, LaVale, McCoole, Mount Savage, Potomac Park, Barrelville, Bier, Borden Shaft, Bowmans Addition, Carlos, Clarysville, Corriganville, Danville, Dawson, Detmold, Eckhart Mines, Flintstone, Franklin, Gilmore, Grahamtown, Klondike, Little Orleans, Midlothian, Moscow, National, Nikep, Ocean, Oldtown, Pleasant Grove, Rawlings, Shaft, Spring Gap, Vale Summit, Woodland, Zihlman, Amcelle, Dickens, Evitts Creek, George's Creek, Loartown, McKenzie, Narrows Park, Pinto, Town Creek"
    },
    {
        "county": "Cecil County",
        "municipalities": "Cecilton, Charlestown, Chesapeake City, Elkton, North East, Perryville, Port Deposit, Rising Sun, Appleton, Bay View, Blue Ball Village, Calvert, Carpenter Point, Cherry Hill, Childs, Colora, Conowingo, Crystal Beach, Earleville, Elk Mills, Elk Neck, Fair Hill, Fredericktown, Frenchtown, Hack's Point, Harrisville, Hopewell Manor, Liberty Grove, Oakwood, Perry Point, Providence, Red Point, St. Augustine, Warwick, Westminister, White Crystal Beach, White Hall, Zion"
    },
    {
        "county": "Worcester County",
        "municipalities": "Pocomoke City, Berlin, Ocean City, Snow Hill, Bishopville, Girdletree, Newark, Ocean Pines, Stockton, West Ocean City, Whaleyville, Boxiron, Cedartown, Friendship, Germantown, Goodwill, Ironshire, Klej Grange, Nassawango Hills, Public Landing, Showell, Sinepuxent, South Point, Taylorville, Whiton"
    },
    {
        "county": "Wicomico County",
        "municipalities": "Fruitland, Salisbury, Delmar, Hebron, Mardela Springs, Pittsville, Sharptown, Willards, Allen, Bivalve, Jesterville, Nanticoke, Nanticoke Acres, Parsonsburg, Powellville, Quantico, Tyaskin, Waterview, Whitehaven, Doe Run, Silver Run, Wetipquin, Whiton"
    },
    {
        "county": "Garrett",
        "municipalities": "Accident, Deer Park, Friendsville, Grantsville, Kitzmiller, Loch Lynn Heights, Mountain Lake Park, Oakland, Bloomington, Crellin, Finzel, Gorman, Hutton, Jennings, Swanton, Altamont, Asher Glade, Avilton, Bethel, Bevansville, Bittinger, Blooming Rose, Casselman, Cove, East Vindex, Elder Hill, Engle Mill, Fairview, Floyd, Fort Pendleton, Foxtown, Fricks Crossing, Gortner, Gravel Hill, Green Glade, Hazelhurst, Herrington Manor, Hi-Point, High Point, Hoyes, Hoyes Run, Kaese Mill, Kearney, Keeler Glade, Kempton, Kendall, Keysers Ridge, Lake Ford, Locust Grove, McComas Beach, McHenry, Merrill, Mineral Spring, Mitchell Manor, New Germany, North Glade, Piney Grove, Redhouse, Ryan’s Glade, Sand Spring, Sang Run, Schell, Selbysport, Shallmar, Standard, Stanton Mill, Steyer, Strawn, Strecker, Sunnyside, Table Rock, Tasker Corners, Thayerville, Wallman, West Vindex, Wilson, Winding Ridge"
    },
    {
        "county": "Harford County",
        "municipalities": "Aberdeen, Havre de Grace, Bel Air, Aldino, Benson, Berkley, Cardiff, Castleton, Churchville, Clayton, Constant Friendship, Creswell, Dublin, Darlington, Emmorton, Fairview, Forest Hill, Fountain Green, Glenwood, Hess, Hickory, Hopewell Village, Joppa, Kalmia, Level, Madonna, Norrisville, Shawsville, Street, Taylor, Whiteford, Aberdeen Proving Ground, Abingdon, Bel Air North, Bel Air South, Darlington, Edgewood, Fallston, Jarrettsville, Joppatowne, Perryman, Pleasant Hills, Pylesville, Riverside, Glenville"
    }
]

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
            "outcome": "Easton 28, Cambridge 14",    # game score or outcome; if not a game, short outcome like "win","loss","tie" (string)
            "importance": 7,                            # numeric importance on a 1-10 scale (integer)
            "audience_blurb": "Local high-school sports fans and families; readers interested in Easton High athletics" # 1-2 sentence target audience description (string)
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
            "outcome": "Easton 28, Cambridge 14",
            "importance": 8
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
                    # Remove the author/byline if present and prepare helpers for titles
                    author = story.get('author') or story.get('byline') or ''

                    ROLE_PREFIXES = (
                        'Coach', 'Head Coach', 'Assistant Coach', 'Assistant', 'Player', 'Parent',
                        'Athletic Director', 'Trainer', 'Captain', 'Referee', 'Umpire', 'Principal',
                        'Teacher', 'Director', 'Officer', 'Coach Emeritus'
                    )
                    HONORIFICS = ('Mr', 'Mrs', 'Ms', 'Miss')

                    role_prefix_pattern = '|'.join([re.escape(t) for t in ROLE_PREFIXES])
                    honorific_pattern = '|'.join([re.escape(t) for t in HONORIFICS])

                    def strip_honorific(name):
                        return re.sub(rf'^(?:{honorific_pattern})\.?\s+', '', name, flags=re.IGNORECASE).strip()

                    def strip_role_or_honorific(name):
                        s = re.sub(rf'^(?:{role_prefix_pattern})\.?\s+', '', name, flags=re.IGNORECASE).strip()
                        s = re.sub(rf'^(?:{honorific_pattern})\.?\s+', '', s, flags=re.IGNORECASE).strip()
                        return s

                    def normalize_name(n):
                        return n.strip()

                    # dedupe while preserving order; compare stripped names to the author
                    seen = set(); deduped = []
                    for x in val:
                        k = normalize_name(x)
                        if not k: continue
                        if author and strip_role_or_honorific(k).lower() == strip_role_or_honorific(author).strip().lower():
                            continue
                        if k not in seen:
                            seen.add(k); deduped.append(k)

                    # simple prioritization: prefer entries containing role/title
                    role_words = tuple(list(ROLE_PREFIXES) + ['Mayor', 'Senator', 'Representative', 'Judge', 'Dr', 'Chief', 'Sheriff'])
                    story_text = (story.get('title') or '') + '\n' + (story_content or '')

                    def person_score(name, idx):
                        score = 0
                        # role/title presence is a strong signal
                        for rw in role_words:
                            if rw.lower() in name.lower():
                                score += 4
                        lname = name.lower()
                        st = story_text.lower()
                        # frequency of mentions is important
                        freq = st.count(lname)
                        score += min(freq, 5) * 1.5
                        # earlier appearance is better
                        pos = st.find(lname)
                        if pos != -1:
                            score += max(0, 3 - (pos / 200.0))
                        # shorter names slightly preferred
                        score += max(0, 1 - (len(name.split()) - 2) * 0.1)
                        return (-score, idx)

                    scored = sorted([(person_score(p, i), p) for i, p in enumerate(deduped)], key=lambda x: x[0])
                    prioritized = [p for _, p in scored]

                    # Allow optional role prefixes before a human name; require at least two name tokens
                    prefixes_regex = '|'.join([re.escape(t) for t in ROLE_PREFIXES])
                    name_pattern = rf'^(?:(?:{prefixes_regex})\.?\s+)?[A-Z][A-Za-z\'\-]+(?:\s+[A-Z][A-Za-z\'\-]+)+$'

                    def is_human_name(n):
                        m = re.match(name_pattern, n)
                        if not m:
                            return False
                        # exclude organization-like tokens
                        org_tokens = ('County','School','District','Commission','Commissioners','Board','Department','Inc','Company','Association','Committee','Publishing','Press','Times','Record','Observer','News','Document')
                        for t in org_tokens:
                            if t in n:
                                return False
                        # filter out likely team/place fragments
                        block_words = ('High','School','Conference','Athletic','Saints','Royals','Bucs','Sabres','Kings','Lady','Saint','Team','Delmarva','Star','Democrat','Christian','Eastern','Shore','Independent','Publishing','Press','Times','Record','Observer','News','Document')
                        for part in n.split():
                            if part in block_words:
                                return False
                        return True

                    def augment_with_title(name):
                        try:
                            regex = rf"\b(?:{prefixes_regex})\.?\s+{re.escape(name)}\b"
                            m = re.search(regex, story_text, flags=re.IGNORECASE)
                            if m:
                                return m.group(0).strip()
                            # If no role prefix found but an honorific appears like 'Mr. Name', strip it
                            hregex = rf"\b(?:{honorific_pattern})\.?\s+{re.escape(name)}\b"
                            mh = re.search(hregex, story_text, flags=re.IGNORECASE)
                            if mh:
                                return strip_honorific(mh.group(0)).strip()
                        except Exception:
                            pass
                        return name

                    # augment prioritized names with titles when possible
                    augmented = [augment_with_title(p) for p in prioritized]
                    human_only = [p for p in augmented if is_human_name(p)]
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
                # Skip entity arrays handled above and skip 'venue' which was removed from the schema
                if key in ('people', 'places', 'organizations'):
                    continue
                if key == 'venue':
                    # explicitly ignore venue metadata (schema no longer includes this)
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
                        # Try to augment quoted names with title prefixes found in the story (e.g., 'Coach John Smith')
                        TITLE_PREFIXES_Q = ('Coach', 'Head Coach', 'Assistant Coach', 'Mr', 'Mrs', 'Ms', 'Dr', 'Captain', 'Officer', 'President', 'Mayor', 'Senator', 'Judge', 'Principal', 'Lt', 'Sr')
                        prefixes_q = '|'.join([re.escape(t) for t in TITLE_PREFIXES_Q])
                        augmented_q = []
                        for n in q_ordered:
                            try:
                                regex = rf"\b(?:{prefixes_q})\.?\s+{re.escape(n)}\b"
                                m = re.search(regex, story_text, flags=re.IGNORECASE)
                                if m:
                                    augmented_q.append(m.group(0).strip())
                                    continue
                            except Exception:
                                pass
                            augmented_q.append(n)

                        enhanced_story['entities_quoted_people'] = json.dumps(augmented_q)
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

                # audience_blurb: write a concise 1-2 sentence target-audience description
                if key == 'audience_blurb':
                    ab = ''
                    if isinstance(value, str):
                        ab = value.strip()
                    elif isinstance(value, (list, dict)):
                        try:
                            ab = json.dumps(value, ensure_ascii=False)
                        except Exception:
                            ab = str(value)
                    else:
                        ab = str(value or '')
                    # enforce concise length (truncate if necessary)
                    if ab and len(ab) > 400:
                        ab = ab[:397].rstrip() + '...'
                    enhanced_story['metadata_audience_blurb'] = ab
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
    with open('stories_with_entities.json', 'w') as f:
        json.dump(enhanced_stories, f, indent=2)

    print(f"Processed {len(enhanced_stories)} stories with metadata")

if __name__ == "__main__":
    main()
