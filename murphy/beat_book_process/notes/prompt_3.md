```python
content_type_list = [
    {
        "content_type": "News",
        "definition": "Full articles, excluding calendars, obituaries, legal notices, opinion pieces and other listings, meant to inform, not persuade, readers on news topics such as politics, elections, government, agriculture, education, housing, economy and budget, transportation, infrastructure, public works, public safety, crime, environment, arts, society, community and sports.",
        "examples": "Police investigating Easton homicide"; "Robbins YMCA opening reading hub to tackle childhood illiteracy"
    },
    {
        "content_type": "Calendars",
        "definition": "Calendars.",
        "examples": "Mid-Shore Calendar"; "RELIGION CALENDAR"
    },
    {
        "content_type": "Obituaries",
        "definition": "Obituaries.",
        "examples": "Rhonda Lynn Fearins Thomas"; "Mary Beth Adams"
    },
    {
        "content_type": "Legal Notices",
        "definition": "Legal notices.",
        "examples": "Legal Notices"
    },
    {
        "content_type": "Opinion",
        "definition": "Columns, editorials, letters to the editor and any other opinion-based pieces for which the primary purpose is to persuade, not necessarily inform, readers.",
        "examples": "Biden must go"; "EDITORIAL: 10-cent paper bag fee should be optional"
    },
    {
        "content_type": "Miscellaneous",
        "definition": "TV listings, Today in History articles and other non-news and non-opinion content.",
        "examples": "SPRING TRAINING GLANCE 3-10-24"; "TV LISTINGS 1-11-24"; "TODAY IN HISTORY/Aug. 4"; "Web links"; "Tonight's top picks"
    }
]

topic_list = [
    {
        "topic": "Local Government & Politics",
        "definition": "Articles that center around and primarily discuss local government entities, including but not limited to local boards, councils and agencies, as well as coverage of their actions, meetings and any relevant legislation or resolutions they have sponsored. Also includes articles covering individual political figures, such as mayors and mayoral candidates, board members, and council members, as well as elections and political disputes."
    }
    {
        "topic": "Economy & Budget",
        "definition": "Articles that center around and primarily discuss the finances and economy of a municipality, including local economic issues for both communities and businesses, notably the local impact of inflation, unemployment, debt, healthcare costs and housing costs."
    },
    {
        "topic": "Planning & Development",
        "definition": "Articles that center around and primarily discuss planning, zoning, municipal development or housing, including local programs, policies and initiatives related to growth, economic development, housing, workforce development, job creation, community investment and tourism"
    },
    {
        "topic": "Transportation, Infrastructure & Public Works",
        "definition": "Articles that center around and primarily discuss public transportation systems, local infrastructure and municipal services provided and funded by the government, including public transit, roads and bridges, and public sewer, water and electricity services."
    },
    {
        "topic": "Public Safety & Crime",
        "definition": "Articles that center around and primarily discuss issues concerning police, crime, violence, public health, emergency management and other community-specific public safety concerns."
    },
    {
        "topic": "Arts & Culture",
        "definition": "Articles that center around and primarily discuss local community and culture. This includes features on culturally relevant people, places and events, including notable community organizations, leaders and events related to art, music, food, heritage, local history and culture, as well as news articles about municipal social programs, such as community food drives, free mental health screenings and other public benefit initiatives."
    },
    {
        "topic": "Education",
        "definition": "Articles that center around and primarily discuss local school systems and any prominent political, financial or other issues they face related to staffing, resources, curricula, school violence, attendance and mental health, as well as any programs, policies or initiatives designed to address those issues"
    },
    {
        "topic": "Agriculture & Environment",
        "definition": "Articles that center around and primarily discuss environmental topics, including pollution, ecosystems, conservation and the Chesapeake Bay, as well as stories specific to local agricultural and aquacultural issues, including those related to commercial farming and fishing, food supply, economic viability, climate change and labor."
    },
    {
        "topic": "Sports & Recreation",
        "definition": "Articles that center around and primarily discuss local sports and recreation at every level, including youth sports, high school athletics, local organized sports teams and leagues and community recreation"
    }, 
    {
        "topic": "Other",
        "definition": "Last-resort classification for content that does not fall under another clearly defined topic."
    }
]

maryland_counties_list = [
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

I need to make a python script called `starmdem_entities_script_3.py`.

Here are the script requirements:
- Use the `llm` command-line tool with the model `groq/moonshotai/kimi-k2-instruct-0905`
- Use subprocess to call the `llm` command
- Have the LLM process each story from `stardem_sample.json`
- Have the LLM add the following fields to each story: `content_type`, `primary_topic`, `secondary_topic`, `regions`, `municipalities`, `counties`, `key_people`, `key_locations`, `key_events_and_initiatives`, `key_establishments`, `key_organizations`, `key_bodies`.
- Have the LLM save the updated stories to `stories_with_entities_3.json`
- Print progress as it processes stories

Here are the guidelines:
- The `content_type` field should contain the single best-fitting content type from list provided in `content_type_list`.
- The `primary_topic` field should contain the single best-fitting topic from the list provided in `topic_list`.
- The `secondary_topic` field should contain, when applicable, a second topic from the list provided in `topic_list`. 
- The `regions` field should contain the general region of the story: Maryland, Virginia, D.C., or other specific country, state or region. Use "U.S." for national stories.
- The `municipalities` field should contain a json array of all Maryland municipalities mentioned in or central to the story, using `maryland_county_list` as a guide. Always exclude "Easton" if it not mentioned in the main body of the story.
- The `counties` field should contain a json array of the counties where the municipalities mentioned in the the story are located, based on `maryland_county_list`. When localities are mentioned across multiple stories, ensure their names are standardized. 
- The `key_people` field should contain a json array of important people mentioned or quoted in the story, along with their title in parentheses. Important people would include people who are relevant beyond a single story — like politicians, political candidates, coaches, community leaders, public officials, board members and council members. names of people listed in obituaries unless they were important figures during their lives. No more than four people. Never include the name of the author of the article.
- The `key_locations` field should contain a json array of all specific locations within municipalities that are mentioned in the story, such as rivers, parks, neighborhoods, and street names. This does not include physical places like schools, community centers or town halls. Unabbreviate abbreviated street suffixes like "St." or "Ave.". Do not include the number associated with the address, and, when possible, include in parentheses the name of the municipality where the location is. When a state or city outside of Maryland is mentioned, include it here.
- The `key_events_and_initiatives` field should contain a json array of the names of relevant organized events or initiatives central to the story. This includes named, planned events, like a county fair or a march, and initiatives like legislation, policies or a town plan. It does not include generalized events like a fire or funeral.
- The `key_establishments` field should contain a json array of any relevant businesses, restaurants and other private establishments central to the story.
- The `key_organizations` field should contain a json array of the relevant organizations central to the story, such as nonprofits, advocacy organizations, community centers, museums, fundraising organizations, political organizations. When organizations are mentioned across multiple stories, ensure their names are standardized.
- The `key_bodies` field should contain a json array of the relevant government bodies and other public institutions central to the story, such as agencies, school districts, councils, boards and similar entities. When organizations are mentioned across multiple stories, ensure their names are standardized.

Remember:
- Use title case when the original text is capitalized
- Never include the name of the main paper, the "Star-Democrat", or the names of the publishers, "Chesapeake Publishing Group" and "Adams Publishing/APGMedia"
- Leave fields blank where there are no applicable data
- The state legislature should always be written as "Maryland General Assembly"

example_output = [
    {
        "title": "Attorney general visits Easton to honor first responders at annual celebration",
        "date": "2025-06-13",
        "author": "Konner Metz",
        "content": "Attorney general visits Easton to honor first responders at annual celebration\n\n June 13, 2025 | Star Democrat, The (Easton, MD)\n\n Author/Byline: Konner Metz | Section: Local News \n \n 433\n Words \n\n Read News Document\n\n EASTON — First responders across different Talbot County agencies were honored Thursday in Easton by local residents, business leaders and Maryland Attorney General Anthony Brown.Bluepoint Hospitality Group hosted the fifth annual First Responders Celebration, closing down North Washington Street temporarily on Thursday afternoon to pay thanks to the county's police officers, firefighters, EMTs and other first responders.\n\"These people put their lives on the line so that we can live in a civil and safe community,\" said Bluepoint Hospitality owner Paul Prager.\nThe event was headlined by Maryland Attorney General Anthony Brown, who called the Talbot County first responders — paid or volunteers — \"heroes.\"\n\"When others run away from danger, you run toward it,\" Brown said. \"From volunteers who respond to dangerous house fires in the middle of the night, to police officers who take drugs, and guns and bad people off our streets, to emergency medical service personnel who rush people to the hospital for life-saving care, our first responders are the backbone of public safety and the cornerstone of our communities.\"\nDuring the brief ceremonies, Ed Forte, vice president of the Friends of Easton Volunteer Fire Department, revealed a new rendering of an in-construction training campus to Easton Fire Chief J.R. Dobson.\nThe A. James Clark Emergency Services Training Campus, located on Mistletoe Drive, will be 7,200 square feet and provide state-of-the-art training opportunities for all first responders.\nAs the rendering showed, a building on the training campus will be named after Paul Prager and his wife, Joanne. The Pragers donated $500,000 to the project.\nForte said Thursday that $4.5 million has been raised in the last two-and-a-half years, nearly all of the project's $5 million goal. Project leaders hope for the campus to open by the end of this year.\n\"(It's) taken many, many years; many, many people; many hours; many ideas,\" Forte said. \" … Raising the money was the hardest thing.\"\nAfter the event, Brown said in an interview he's impressed with the coordination between the different first responder agencies in Talbot County.\n\"Often people think small, rural community on the Eastern Shore, 'how busy does it get?'\" Brown said. \"But clearly the numbers show that they're busy. It's important to stand ready. The facility that is going to be built is going to help them do that.\"\nWhen asked afterward if the First Responders Celebration is becoming a tradition, Prager had no hesitation.\n\"It's gotta be, absolutely,\" Prager said. \"These people do thankless jobs. And there's not a whole lot you can do to enable them to make their lives better. So I think if you at least just say thank you, that goes a long way.\" \n\n © Copyright © 2025 Star Democrat, Chesapeake Publishing Group (Adams Publishing/APGMedia). All rights reserved.",
        "docref": "news/1A1356326A94CD78",
        "article_id": "search-hits__hit--421",
        "content_source": "full_document",
        "year": 2025,
        "month": 6,
        "day": 13
        "content_type": "News",
        "primary_topic": "Public Safety & Crime",
        "secondary_topic": "",
        "regions": [
            "Maryland"
        ]
        "municipalities": [
            "Easton"
        ],
        "counties": [
            "Talbot County"
        ]
        "key_people": [
            "Anthony Brown (Maryland Attorney General)",
            "J.R. Dobson (Easton Fire Chief)"
        ],
        "key_locations": [
            "North Washington Street (Easton)",
            "Mistletoe Drive"
        ],
        "key_events_and_initiatives": [
            "First Responders Celebration"
        ],
        "key_establishments": [
            "A. James Clark Emergency Services Training Campus"
        ],
        "key_organizations": [
            "Bluepoint Hospitality Group"
        ],
        "key_bodies": [
            "Easton Volunteer Fire Department"
        ]
    },
    {
        "title": "Chesapeake Bay cleanup at a crossroads: new path or stay the course?",
        "date": "2024-10-03",
        "author": "JEREMY COX Bay Journal",
        "content": "Chesapeake Bay cleanup at a crossroads: new path or stay the course?\n\n October 3, 2024 | Star Democrat, The (Easton, MD)\n\n Author/Byline: JEREMY COX Bay Journal | Section: State News \n \n 1014\n Words \n\n Read News Document\n\n As the Chesapeake Bay cleanup's leaders close in on a revised working agreement, many of the effort's most influential supporters are endorsing a major thematic shift: putting less emphasis on improving the estuary's seldom-seen deep waters and more on helping people and living resources in the Bay watershed.\"This is an opportunity for our movement to understand our successes and failures, and adjust accordingly,\" said Kate Fritz, CEO of the Alliance for the Chesapeake Bay, in a letter to the Chesapeake Bay Program, the multi-state and federal partnership in charge of reviving the Bay. \"This means … intentionally including people and living resources at the center of the partnership's work.\"\nThat closely aligns with the recommendations of the Bay Program team that was tasked with drafting an update of the 2014 Chesapeake Bay Agreement. A draft was released for public feedback on July 1.\nThe team urged the program to \"better incentivize practices that maximize benefits to living resources and people.\" This, they argued, could be accomplished largely through actions that target water quality improvements — long the effort's central focus — but only if local community concerns take precedent.\nMore than 80 people and organizations submitted comments on the draft agreement by the Aug. 30 deadline. The Chesapeake Executive Council — the governors of the six watershed states, mayor of the District of Columbia, chair of the Chesapeake Bay Commission and administrator of the Environmental Protection Agency — is set to vote on a final draft during its annual meeting in December.\nThe revised agreement is intended to serve as a top-line strategy for cleaning up the Bay and its 64,000-square-mile drainage basin beyond 2025, when the deadline for goals in the current agreement expires.\nFor decades, the partnership has centered its work on reducing nutrient and sediment pollution flowing into the Bay. The main goal has been to shrink the annual \"dead zones,\" pockets of oxygen-starved water in the estuary's deepest waters where aquatic creatures struggle to survive.\nDespite billions of dollars invested in the effort, pollution reductions have been modest and slow in coming, according to the Bay Program's own calculations. Some advocates and scientists fear that the cleanup risks falling out of favor with the public if it doesn't shift toward more visible quests, such as restoring shallow waters along the edge of the Bay and its tributaries.\n\"Without renewed attention to those things that matter the most to people, we run the risk of leaving potential living resource benefits unaddressed and potentially losing public support for our efforts,\" wrote Larry Sanford, chair of the Bay Program's Scientific and Technical Advisory Committee (STAC), on behalf of the panel.\nBut in remarks to STAC on Sept. 12, Sanford, a professor at the University of Maryland Center for Environmental Science, described the new draft agreement as a \"compromise\" between two factions: those seeking a pronounced change in direction and those who want to stay the course.\nFor his part, Sanford said the program needs to maintain much of its existing work but also \"go back to the original reason for the Bay Program, and that was what was happening to the living resources.\"\nIf that recalibration is to move forward, it will have to survive a big test later this fall when the agreement goes before the Principals' Staff Committee — senior officials from the Bay states and DC, who sounded a note of caution about that approach when they met in March.\nMeeting water quality goals is a legal requirement, enforced by the EPA. The committee appeared concerned that de-stressing that goal could lead to potential lawsuits. Several members at the time also said they believed that those authoring the revised agreement had gone beyond what they had been authorized to do.\nA group of agricultural industry groups in Virginia, including the Virginia Farm Bureau, signed on to a letter that said they \"appreciate\" the draft's call to better address climate change and public engagement. But they are concerned that such measures would \"change the original intent and shared goals\" of the 2014 agreement. The state in its current two-year budget has set aside a record $207 million to reduce farm-based pollution.\nMeanwhile, several environmental groups touted how reorienting the program toward people and living creatures would support other important goals. Much could be achieved, for example, through tougher enforcement of state and federal water pollution control laws, according to a letter signed by Waterkeepers Chesapeake and several local waterkeepers.\n\"While the status quo elevates considerations of nutrient pollutants and the dissolved oxygen levels in the mainstem of the Bay, the path forward must elevate the role that enforcement of illegal pollution from point sources has on protecting humans and wildlife from toxic and carcinogenic substances,\" the waterkeepers said.\nThe needs of people and wildlife will be difficult to meet without more land conservation, said the Chesapeake Conservation Partnership, an alliance of land trusts and related organizations. Bay leaders, they added, should elevate land conservation to stand as a \"key guiding pillar\" along those already on that top tier: science, restoration and partnership.\nThe document being readied for the Executive Council's approval this December isn't the final revised agreement but rather a framework for a more detailed compact to be worked out in the future. The current draft doesn't call for a full revision of the agreement until the council meets in 2026.\nSeveral commenters urged leadership to put the finalized agreement on a faster schedule. To wait until late 2026 could lead to a pause or slowdown in oyster restoration activities in key Bay tributaries, said Oyster Recovery Partnership Executive Director H. Ward Slacum. It should be ready by the end of 2025 instead, he said.\nA group of about 40 retired Bay scientists and former public officials also weighed in. The coalition, calling itself \"Chesapeake Bay Program Veterans,\" echoed the push to have the revisions in place in 2025.\nAnd the program should look at the problems and benefits that arise from local, state and federal greenhouse gas reduction goals, they said. They suggested that the transition from fossil fuels to renewable energy, for example, is likely to reduce nitrogen pollution that enters Bay waters from the atmosphere. \n\n © Copyright © 2024 Star Democrat, Chesapeake Publishing Group (Adams Publishing/APGMedia). All rights reserved.",
        "docref": "news/19BFA26DA1B954D0",
        "article_id": "search-hits__hit--3174",
        "content_source": "full_document",
        "year": 2024,
        "month": 10,
        "day": 3,
        "content_type": "News",
        "primary_topic": "Agriculture & Environment",
        "secondary_topic": "Local Government & Politics",
        "regions": [
            "Maryland",
            "D.C.",
            "Virginia",
            "Bay States"
        ]
        "municipalities": [
            ""
        ],
        "counties": [
            ""
        ]
        "key_people": [
            ""
        ],
        "key_locations": [
            "Chesapeake Bay"
        ],
        "key_events_and_initiatives": [
            "2014 Chesapeake Bay Agreement"
        ],
        "key_establishments": [
            ""
        ]
        "key_organizations": [
            "Alliance for the Chesapeake Bay",
            "University of Maryland Center for Environmental Science",
            "Chesapeake Conservation Partnership",
            "Chesapeake Bay Program Veterans",
            "Oyster Recovery Partnership"
        ],
        "key_bodies": [
            "Chesapeake Bay Program",
            "Chesapeake Executive Council",
            "Chesapeake Bay Commission",
            "Environmental Protection Agency",
            "Scientific and Technical Advisory Committee",
            "Principals' Staff Committee",
            "Virginia Farm Bureau"
        ]
    }
]
```
uv run python stardem_entities_script_3.py --model groq/moonshotai/kimi-k2-instruct-0905  --input stardem_sample.json --output stories_with_entities_3.json