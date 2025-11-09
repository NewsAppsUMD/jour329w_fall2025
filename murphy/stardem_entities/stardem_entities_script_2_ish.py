import json
import subprocess
import re
import argparse
import sys

# --- County and municipality mapping setup ---
maryland_county_list = [
    {"county": "Dorchester County", "municipalities": "Brookview, Cambridge, Church Creek, Crapo, Crocheron, East New Market, Eldorado, Fishing Creek, Galestown, Hurlock, Linkwood, Madison, Rhodesdale, Secretary, Taylors Island, Toddville, Vienna, Wingate, Woolford"},
    {"county": "Caroline County", "municipalities": "Denton, Federalsburg, Goldsboro, Greensboro, Henderson, Hillsboro, Marydel, Preston, Ridgely, Templeville, Choptank, West Denton, Williston, American Corner, Andersontown, Baltimore Corner, Bethlehem, Brick Wall Landing, Burrsville, Gilpin Point, Harmony, Hickman, Hobbs, Jumptown, Linchester, Oakland, Oil City, Tanyard, Two Johns, Reliance, Whiteleysburg"},
    {"county": "Kent County", "municipalities": "Betterton, Chestertown, Galena, Millington, Rock Hall, Butlertown, Chesapeake Landing, Edesville, Fairlee, Georgetown, Kennedyville, Still Pond, Tolchester, Worton, Chesterville, Golts, Hassengers Corner, Langford, Lynch, Massey, Pomona, Sassafras, Sharpstown, Tolchester Beach"},
    {"county": "Queen Anne's County", "municipalities": "Barclay, Centreville, Church Hill, Millington, Queen Anne, Queenstown, Sudlersville, Templeville, Chester, Grasonville, Kent Narrows, Kingstown, Romancoke, Stevensville, Crumpton, Dominion, Ingleside, Love Point, Matapeake, Price, Ruthsburg"},
    {"county": "Talbot County", "municipalities": "Easton, Oxford, Queen Anne, Saint Michaels, Trappe, Cordova, Tilghman Island, Anchorage, Bellevue, Bozman, Claiborne, Copperville, Doncaster, Fairbanks, Lewistown, Lloyd Landing, Matthews, McDaniel, Neavitt, Newcomb, Royal Oak, Sherwood, Tunis Mills, Unionville, Wittman, Windy Hill, Woodland, Wye Mills, Dover, York, Wyetown"},
    {"county": "Prince George's County", "municipalities": "Bowie, College Park, District Heights, Glenarden, Greenbelt, Hyattsville, Laurel, Mount Rainier, New Carrollton, Seat Pleasant, Berwyn Heights, Bladensburg, Brentwood, Capitol Heights, Cheverly, Colmar Manor, Cottage City, Eagle Harbor, Edmonston, Fairmount Heights, Forest Heights, Landover Hills, Morningside, North Brentwood, Riverdale Park, University Park, Upper Marlboro"},
    {"county": "Calvert County", "municipalities": "Adelina, Barstow, Bowens, Chaneyville, Dares Beach, Dowell, Johnstown, Lower Marlboro, Mutual, Parran, Pleasant Valley, Port Republic, Scientists Cliffs, Stoakley, Sunderland, Wallville, Wilson, Chesapeake Beach, North Beach, Broomes Island, Calvert Beach, Chesapeake Ranch Estates, Drum Point, Dunkirk, Huntingtown, Long Beach, Lusby, Owings, Prince Frederick, St. Leonard, Solomons"},
    {"county": "Anne Arundel County", "municipalities": "Annapolis, Highland Beach, Annapolis Neck, Arden on the Severn, Arnold, Brooklyn Park, Cape Saint Claire, Crofton, Crownsville, Deale, Edgewater, Ferndale, Fort Meade, Friendship, Galesville, Gambrills, Glen Burnie, Herald Harbor, Jessup, Lake Shore, Linthicum, Maryland City, Mayo, Naval Academy, Odenton, Parole, Pasadena, Riva, Riviera Beach, Selby-on-the-Bay, Severn, Severna Park, Shady Side, Beverly Beach, Bristol, Chestnut Hill Cove, Churchton, Davidsonville, Fairhaven, Germantown, Gibson Island, Green Haven, Hanover, Harmans, Harundale, Harwood, Hillsmere Shores, Jacobsville, Londontowne, Lothian, Millersville, Orchard Beach, Owensville, Pumphrey, Riverdale, Rose Haven, Russett, Sherwood Forest, South Gate, Sudley, Tracys Landing, Waysons Corner, West River, Winchester-on-the-Severn, Woodland Beach"},
    {"county": "Baltimore County", "municipalities": "Arbutus, Baltimore Highlands, Bowleys Quarters, Carney, Catonsville, Cockeysville, Dundalk, Edgemere, Essex, Garrison, Hampton, Honeygo, Kingsville, Lansdowne, Lochearn, Lutherville, Mays Chapel, Middle River, Milford Mill, Overlea, Owings Mills, Parkville, Perry Hall, Pikesville, Randallstown, Reisterstown, Rosedale, Rossville, Timonium, Towson, White Marsh, Woodlawn, Baldwin, Boring, Bradshaw, Brooklandville, Butler, Chase, Fork, Fort Howard, Germantown, Glen Arm, Glencoe, Glyndon, Halethorpe, Hereford, Hunt Valley, Hydes, Jacksonville, Long Green, Maryland Line, Monkton, Nottingham, Oella, Parkton, Phoenix, Ruxton, Sparks, Sparrows Point, Stevenson, Trump, Turners Station, Upper Falls, Upperco, White Hall"},
    {"county": "Baltimore City", "municipalities": "Baltimore City"},
    {"county": "Howard County", "municipalities": "Columbia, Elkridge, Ellicott City, Fulton, Highland, Ilchester, Jessup, Lisbon, North Laurel, Savage, Scaggsville, Clarksville, Cooksville, Daniels, Dayton, Dorsey, Glenelg, Glenwood, Granite, Guilford, Hanover, Isaacsville, Marriottsville, Simpsonville, West Friendship, Woodbine, Woodstock"},
    {"county": "Carroll County", "municipalities": "Westminster, Taneytown, Manchester, Mount Airy, New Windsor, Union Bridge, Hampstead, Sykesville, Eldersburg, Alesia, Carrollton, Carrolltowne, Detour, Finksburg, Frizzelburg, Gamber, Gaither, Greenmount, Harney, Henryton, Jasontown, Keymar, Lineboro, Linwood, Marriottsville, Mayberry, Middleburg, Millers, Patapsco, Pleasant Valley, Silver Run, Union Mills, Uniontown, Woodbine, Woodstock"},
    {"county": "Montgomery County", "municipalities": "Gaithersburg, Rockville, Takoma Park, Barnesville, Brookeville, Chevy Chase, Chevy Chase View, Chevy Chase Village, Garrett Park, Glen Echo, Kensington, Laytonsville, Poolesville, Somerset, Washington Grove, Martin's Additions, North Chevy Chase, Drummond, Oakmont"},
    {"county": "Frederick County", "municipalities": "Brunswick, Frederick, Burkittsville, Emmitsburg, Middletown, Mount Airy, Myersville, New Market, Thurmont, Walkersville, Woodsboro, Rosemont, Adamstown, Ballenger Creek, Bartonsville, Braddock Heights, Buckeystown, Graceham, Green Valley, Jefferson, Lewistown, Libertytown, Linganore, Monrovia, Point of Rocks, Sabillasville, Spring Ridge, Urbana, Charlesville, Clover Hill, Creagerstown, Discovery, Garfield, Ijamsville, Knoxville, Ladiesburg, Lake Linganore, Linganore, Mountaindale, Mount Pleasant, New Midway, Petersville, Rocky Ridge, Spring Garden, Sunny Side, Tuscarora, Unionville, Utica, Wolfsville"},
    {"county": "St. Mary's County", "municipalities": "Leonardtown, California, Callaway, Charlotte Hall, Golden Beach, Lexington Park, Mechanicsville, Piney Point, St. George Island, Tall Timbers, Wildewood, Abell, Avenue, Beachville-St. Inigoes, Beauvue, Bushwood, Chaptico, Clements, Coltons Point, Compton, Dameron, Drayden, Great Mills, Helen, Hollywood, Hopewell, Huntersville, Hurry, Loveville, Maddox, Morganza, Oakley, Oakville, Oraville, Park Hall, Ridge, St. Inigoes, St. Mary's City, Scotland, Spencers Wharf, Valley Lee"},
    {"county": "Charles County", "municipalities": "Indian Head, La Plata, Port Tobacco Village, Benedict, Bensville, Bryans Road, Bryantown, Charlotte Hall, Cobb Island, Hughesville, Pomfret, Potomac Heights, Rock Point, Waldorf, Bel Alton, Dentsville, Faulkner, Glymont, Grayton, Ironsides, Issue, Malcolm, Marbury, Morgantown, Mount Victoria, Nanjemoy, Newburg, Pisgah, Popes Creek, Port Tobacco, Pomonkey, Ripley, Rison, Saint Charles, Swan Point, Welcome, White Plains"},
    {"county": "Washington County", "municipalities": "Hagerstown, Boonsboro, Clear Spring, Funkstown, Hancock, Keedysville, Sharpsburg, Smithsburg, Williamsport, Antietam, Bagtown, Bakersville, Beaver Creek, Big Pool, Big Spring, Breathedsville, Brownsville, Cavetown, Cearfoss, Charlton, Chewsville, Dargan, Downsville, Eakles Mill, Edgemont, Ernstville, Fairplay, Fairview, Fort Ritchie, Fountainhead-Orchard Hills, Gapland, Garretts Mill, Greensburg, Halfway, Highfield-Cascade, Indian Springs, Jugtown, Kemps Mill, Leitersburg, Mapleville, Maugansville, Mercersville, Middleburg, Mount Aetna, Mount Briar, Mount Lena, Paramount-Long Meadow, Pecktonville, Pinesburg, Pondsville, Reid, Ringgold, Robinwood, Rohrersville, Saint James, San Mar, Sandy Hook, Tilghmanton, Trego-Rohrersville Station, Wilson-Conococheague, Yarrowsburg, Appletown, Benevola, Broadfording, Burtner, Huyett, Pen Mar, Samples Manor, Spielman, Trego, Van Lear, Weverton, Woodmont, Zittlestown"},
    {"county": "Somerset County", "municipalities": "Crisfield, Princess Anne, Chance, Dames Quarter, Deal Island, Eden, Fairmount, Frenchtown-Rumbly, Mount Vernon, Smith Island, West Pocomoke, Ewell, Kingston, Manokin, Marion Station, Oriole, Rehobeth, Rhodes Point, Shelltown, Tylerton, Upper Fairmount, Upper Falls, Wenona, Westover"},
    {"county": "Allegany County", "municipalities": "Cumberland, Frostburg, Barton, Lonaconing, Luke, Midland, Westernport, Bel Air, Bowling Green, Cresaptown, Ellerslie, LaVale, McCoole, Mount Savage, Potomac Park, Barrelville, Bier, Borden Shaft, Bowmans Addition, Carlos, Clarysville, Corriganville, Danville, Dawson, Detmold, Eckhart Mines, Flintstone, Franklin, Gilmore, Grahamtown, Klondike, Little Orleans, Midlothian, Moscow, National, Nikep, Ocean, Oldtown, Pleasant Grove, Rawlings, Shaft, Spring Gap, Vale Summit, Woodland, Zihlman, Amcelle, Dickens, Evitts Creek, George's Creek, Loartown, McKenzie, Narrows Park, Pinto, Town Creek"},
    {"county": "Cecil County", "municipalities": "Cecilton, Charlestown, Chesapeake City, Elkton, North East, Perryville, Port Deposit, Rising Sun, Appleton, Bay View, Blue Ball Village, Calvert, Carpenter Point, Cherry Hill, Childs, Colora, Conowingo, Crystal Beach, Earleville, Elk Mills, Elk Neck, Fair Hill, Fredericktown, Frenchtown, Hack's Point, Harrisville, Hopewell Manor, Liberty Grove, Oakwood, Perry Point, Providence, Red Point, St. Augustine, Warwick, Westminister, White Crystal Beach, White Hall, Zion"},
    {"county": "Worcester County", "municipalities": "Pocomoke City, Berlin, Ocean City, Snow Hill, Bishopville, Girdletree, Newark, Ocean Pines, Stockton, West Ocean City, Whaleyville, Boxiron, Cedartown, Friendship, Germantown, Goodwill, Ironshire, Klej Grange, Nassawango Hills, Public Landing, Showell, Sinepuxent, South Point, Taylorville, Whiton"},
    {"county": "Wicomico County", "municipalities": "Fruitland, Salisbury, Delmar, Hebron, Mardela Springs, Pittsville, Sharptown, Willards, Allen, Bivalve, Jesterville, Nanticoke, Nanticoke Acres, Parsonsburg, Powellville, Quantico, Tyaskin, Waterview, Whitehaven, Doe Run, Silver Run, Wetipquin, Whiton"},
    {"county": "Garrett County", "municipalities": "Accident, Deer Park, Friendsville, Grantsville, Kitzmiller, Loch Lynn Heights, Mountain Lake Park, Oakland, Bloomington, Crellin, Finzel, Gorman, Hutton, Jennings, Swanton, Altamont, Asher Glade, Avilton, Bethel, Bevansville, Bittinger, Blooming Rose, Casselman, Cove, East Vindex, Elder Hill, Engle Mill, Fairview, Floyd, Fort Pendleton, Foxtown, Fricks Crossing, Gortner, Gravel Hill, Green Glade, Hazelhurst, Herrington Manor, Hi-Point, High Point, Hoyes, Hoyes Run, Kaese Mill, Kearney, Keeler Glade, Kempton, Kendall, Keysers Ridge, Lake Ford, Locust Grove, McComas Beach, McHenry, Merrill, Mineral Spring, Mitchell Manor, New Germany, North Glade, Piney Grove, Redhouse, Ryan's Glade, Sand Spring, Sang Run, Schell, Selbysport, Shallmar, Standard, Stanton Mill, Steyer, Strawn, Strecker, Sunnyside, Table Rock, Tasker Corners, Thayerville, Wallman, West Vindex, Wilson, Winding Ridge"},
    {"county": "Harford County", "municipalities": "Aberdeen, Havre de Grace, Bel Air, Aldino, Benson, Berkley, Cardiff, Castleton, Churchville, Clayton, Constant Friendship, Creswell, Dublin, Darlington, Emmorton, Fairview, Forest Hill, Fountain Green, Glenwood, Hess, Hickory, Hopewell Village, Joppa, Kalmia, Level, Madonna, Norrisville, Shawsville, Street, Taylor, Whiteford, Aberdeen Proving Ground, Abingdon, Bel Air North, Bel Air South, Darlington, Edgewood, Fallston, Jarrettsville, Joppatowne, Perryman, Pleasant Hills, Pylesville, Riverside, Glenville"}
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
You are extracting structured metadata from news articles. Extract and return ONLY a JSON object with these fields: content_type, topic, people, sources, events, locations, municipalities, county, institutions.

CONTENT_TYPE: Choose the single best-fitting type:
- "News": Full articles, excluding calendars, obituaries, legal notices, opinion pieces and other listings, meant to inform, not persuade, readers on news topics such as politics, elections, government, agriculture, education, housing, economy and budget, transportation, infrastructure, public works, public safety, crime, environment, arts, society and community.
- "Sports": Full articles, excluding calendars, obituaries, legal notices, opinion pieces and other listings, about local sports topics and teams. Excludes listings and articles about professional teams.
- "Calendars": Calendars.
- "Obituaries": Obituaries.
- "Legal Notices": Legal notices.
- "Opinion": Columns, editorials, letters to the editor and any other opinion-based pieces for which the primary purpose is to persuade, not necessarily inform, readers.
- "Miscellaneous": TV listings, Today in History articles and other non-news and non-opinion content.

TOPIC: Choose the single best-fitting topic:
- "Local Government & Politics": Articles that center around and primarily discuss local government entities, including but not limited to local boards, councils and agencies, as well as coverage of their actions, meetings and any relevant legislation or resolutions they have sponsored. Also includes articles covering individual political figures, such as mayors and mayoral candidates, board members, and council members, as well as elections and political disputes.
- "Economy & Budget": Articles that center around and primarily discuss the finances and economy of a municipality, including local economic issues for both communities and businesses, notably the local impact of inflation, unemployment, debt, healthcare costs and housing costs.
- "Planning & Development": Articles that center around and primarily discuss planning, zoning, municipal development or housing, including local programs, policies and initiatives related to growth, economic development, housing, workforce development, job creation, community investment and tourism.
- "Transportation, Infrastructure & Public Works": Articles that center around and primarily discuss public transportation systems, local infrastructure and municipal services provided and funded by the government, including public transit, roads and bridges, and public sewer, water and electricity services.
- "Public Safety & Crime": Articles that center around and primarily discuss issues concerning police, crime, violence, public health, emergency management and other community-specific public safety concerns.
- "Arts & Culture": Articles that center around and primarily discuss local community and culture. This includes features on culturally relevant people, places and events, including notable community organizations, leaders and events related to art, music, food, heritage, local history and culture, as well as news articles about municipal social programs, such as community food drives, free mental health screenings and other public benefit initiatives.
- "Education": Articles that center around and primarily discuss local school systems and any prominent political, financial or other issues they face related to staffing, resources, curricula, school violence, attendance and mental health, as well as any programs, policies or initiatives designed to address those issues.
- "Agriculture & Environment": Articles that center around and primarily discuss environmental topics, including pollution, ecosystems, conservation and the Chesapeake Bay, as well as stories specific to local agricultural and aquacultural issues, including those related to commercial farming and fishing, food supply, economic viability, climate change and labor.
- "Sports & Recreation": Articles that center around and primarily discuss local sports and recreation at every level, including youth sports, high school athletics, local organized sports teams and leagues and community recreation.
- "Other": Last-resort classification for content that does not fall under another clearly defined topic.

PEOPLE: List important people mentioned or quoted in the story, separated by ";". Important people include politicians, political candidates, coaches, community leaders, public officials, board members and council members. If none, use "".

SOURCES: List categories of sources cited or quoted in the story, separated by ";". Use these categories: government officials, politicians, residents, advocates, organizers, community leaders, coaches. If none, use "".

EVENTS: List the names of relevant events mentioned in the text, separated by ";". This includes named, organized events, like a county fair or a march, and not generalized events like a fire. Use title case when an event is capitalized in the text. If none, use "".

LOCATIONS: List all specific places within municipalities that are mentioned in the story, such as rivers, parks, neighborhoods, and street names, separated by ";". Unabbreviate abbreviated street suffixes, do not include the number of the address, and, when possible, include in parentheses the name of the municipality where the place is located. If none, use "".

MUNICIPALITIES: List all municipalities mentioned in or central to the story, separated by ";". Exclude "Easton" if it is only mentioned in the dateline in the context of the location of the Star-Democrat, but not the main body of the story. If there is no municipality mentioned, put "N/A".

COUNTY: List the counties where the municipalities mentioned in the story are located, separated by ";". When localities are mentioned across multiple stories, ensure their names are standardized. If there is no relation to one of the listed counties, put "N/A". Use title case when a county, municipality or location is capitalized in the text.

INSTITUTIONS: List relevant organizations, businesses, government agencies, councils, boards, churches, teams and other entities mentioned in the story, separated by ";". When organizations are mentioned across multiple stories, ensure their names are standardized. Exclude the name of the main paper, the "Star-Democrat", and the names of the publishers, "Chesapeake Publishing Group" and "Adams Publishing/APGMedia", but when the article was written by someone other than the Star-Democrat, include the name of the organization. If none, use "".

SPORTS ARTICLES SPECIAL NOTE: Be careful when content_type is "Sports" — many of the teams will be referred to by multiple names, and they may appear to be people when they are not. For example, the "Stephen Decatur High School Seahawks" will be referred to as "Stephen Decatur", "Decatur" and "Seahawks." List high school names as locations and team names as institutions, and include the full title, like "Stephen Decatur High School Seahawks".

Return ONLY valid JSON with these exact field names. Use semicolon separators for lists. Use "" for empty string fields or "N/A" where specified.
"""

def process_stories(input_file, output_file, model="groq/meta-llama/llama-4-maverick-17b-128e-instruct"):
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
    parser.add_argument('--output', default='stories_with_entities_2.json', help='Output JSON file')
    parser.add_argument('--model', default='groq/meta-llama/llama-4-maverick-17b-128e-instruct', help='LLM model name')
    args = parser.parse_args()
    process_stories(args.input, args.output, args.model)
