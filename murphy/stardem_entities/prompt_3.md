```python
content_type_list = [
    {
        "content_type": "News",
        "definition": "Full articles, excluding calendars, obituaries, legal notices, opinion pieces and other listings, meant to inform, not persuade, readers on news topics such as politics, elections, government, agriculture, education, housing, economy and budget, transportation, infrastructure, public works, public safety, crime, environment, arts, society and community.",
        "examples": "Police investigating Easton homicide"; "Robbins YMCA opening reading hub to tackle childhood illiteracy"
    },
    {
        "content_type": "Sports"
        "definition": "Full articles, excluding calendars, obituaries, legal notices, opinion pieces and other listings, about local sports topics and teams. Excludes listings and articles about professional teams." 
        "examples": "Lions move closer to first North Bayside title in program history"; 
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
- Have the LLM process each story from `stardem_sample_2.json`
- Have the LLM add the following fields to each story: `content_type`, `primary_topic`, `secondary_topic`, `municipalities`, `counties`, `key_people`, `key_locations`, `key_events`, `key_organizations`, `key_bodies`.
- Have the LLM save the updated stories to `stories_with_entities_3.json`
- Print progress as it processes stories

Here are the guidelines:
- The `content_type` field should contain the single best-fitting content type from list provided in `content_type_list`.
- The `primary_topic` field should contain the single best-fitting topic from the list provided in `topic_list`.
- The `secondary_topic` field should contain, when applicable, a second topic from the list provided in `topic_list`. 
- The `municipalities` field should contain a json array of all Maryland municipalities mentioned in or central to the story, using `maryland_county_list` as a guide. Always exclude "Easton" if it not mentioned in the main body of the story.
- The `counties` field should contain a json array of the counties where the municipalities mentioned in the the story are located, based on `maryland_county_list`. When localities are mentioned across multiple stories, ensure their names are standardized. 
- The `key_people` field should contain a json array of important people mentioned or quoted in the story, along with their title in parentheses. Important people would include people like politicians, political candidates, coaches, community leaders, public officials, board members and council members. Do not include the names of people listed in obituaries unless they were important figures during their lives. No more than four people. Never include the name of the author of the article.
- The `key_locations` field should contain a json array of all specific locations within municipalities that are mentioned in the story, such as rivers, parks, neighborhoods, and street names. This does not include physical places like schools, community centers or town halls. Unabbreviate abbreviated street suffixes like "St." or "Ave.". Do not include the number associated with the address, and, when possible, include in parentheses the name of the municipality where the location is. When a state or city outside of Maryland is mentioned, include it here.
- The `key_events_and_initiatives` field should contain a json array of the names of relevant organized events or initiatives central to the story. This includes named, planned events, like a county fair or a march, and initiatives like a hazard mitigation plan. It does not include generalized events like a fire or funeral.
- The `key_organizations` field should contain a json array of the relevant private organizations central to the story, such as businesses, churches, nonprofits, advocacy organizations, community centers, food pantries, fundraising organizations or political organizations. When organizations are mentioned across multiple stories, ensure their names are standardized.
- The `key_bodies` field should contain a json array of the relevant government bodies and other public institutions central to the story, such as agencies, schools and school districts, councils, boards and similar entities. When organizations are mentioned across multiple stories, ensure their names are standardized.

Remember:
- Use title case when the original text is capitalized
- Never include the name of the main paper, the "Star-Democrat", or the names of the publishers, "Chesapeake Publishing Group" and "Adams Publishing/APGMedia"
- Leave fields blank where there are no applicable data
- The state legislature should always be written as "Maryland General Assembly"

example_output = [
    {
        "title": "Easton traffic dashboard gives residents detailed look at crash trends",
        "date": "2024-07-17",
        "author": "KONNER METZ kmetz@chespub.com",
        "content": "Easton traffic dashboard gives residents detailed look at crash trends\n\n July 17, 2024 | Star Democrat, The (Easton, MD)\n\n Author/Byline: KONNER METZ kmetz@chespub.com | Section: Local News \n \n 537\n Words \n\n Read News Document\n\n EASTON — Residents can now easily access traffic statistics online thanks to a new traffic dashboard released by the town last week.The Easton Interactive Traffic Dashboard allows users to view up-to-date vehicle, pedestrian and bicycle data from 2018 to the present.\nIt includes maps, charts and filters that allow users to see crash information based on time of day, where the crash took place and the weather circumstances. Residents can find specific information on categories such as drunk driving, Route 50 and distracted driving incidents.\nEaston Police Chief Alan Lowrey said it will be a valuable resource for the community to better understand where an alarming number of accidents or traffic citations may happen.\n\"We are focusing on making transportation safety in Easton better,\" Lowrey said. \"We're trying to take a methodical approach, a thoughtful approach to it. … Here is a resource, here's a transparent resource to see what is going on in the town where you live.\"\nRon Engle, a former town council member, helped spearhead the project, along with the Washington College Geographic Information Systems Program and the Maryland Highway Safety Office. Engle has a background in law enforcement and with the National Highway Traffic Safety Administration.\nSean Lynn, the GIS program manager at Washington College, presented the tool to the Easton Town Council on Monday.\n\"Hopefully it allows the folks here in the town to be able to get the information quickly,\" Lynn said.\nEver since the pandemic in 2020, Lowrey said it's been hard to recruit officers. With limited human resources but a need to improve traffic safety, Lowrey began to think about solutions from an \"engineering\" standpoint.\n\"An officer sitting at a location, the impact ends soon after the officer leaves,\" he said. \"Engineering (and) other means are more of a 24-hour solution.\"\nLowrey added that it'll help not just residents, but his team of officers as well. The department will be better-equipped to answer questions such as, \"How many of these are left turn-related? How many of these are red light-related?,\" Lowrey said.\nThe dashboard is a step in completing a Strategic Highway Safety Plan for the town. Engle, Lowrey and Mayor Megan Cook have been working to develop the plan.\nLowrey said a Strategic Highway Safety Plan will open up the ability for the town to acquire grant funding. He pointed to Salisbury as a local jurisdiction that has embraced the state's \"Vision Zero' initiative that was passed by the state legislature in 2019.\n\"Behind it is the notion that you try to reduce fatalities and serious injury accidents down to zero,\" Lowrey said. \"It's a pretty big goal, a really difficult one.\"\nAccording to Lowrey, a plan outline for Easton will be completed in about a month. Engle told council members on Monday that a lack of data was perhaps the \"biggest problem\" for the town in terms of developing a highway safety plan.\nEngle said the dashboard will be a \"strong compliment\" to developing the plan in line with the Vision Zero initiative.\n\"I would hope by fall that we're at a place where we can present a finalized plan before the council with a pretty good idea that they're going to approve it,\" Lowrey said.\nThe interactive traffic dashboard can be accessed by visiting https://eastonmd.gov/196/Police and clicking on the dashboard image. \n\n © Copyright © 2024 Star Democrat, Chesapeake Publishing Group (Adams Publishing/APGMedia). All rights reserved.",
        "docref": "news/19AAC74B244EC4F0",
        "article_id": "search-hits__hit--4053",
        "content_source": "full_document",
        "year": 2024,
        "month": 7,
        "day": 17,
        "content_type": "News",
        "primary_topic": "Transportation, Infrastructure & Public Works",
        "secondary_topic": "Public Safety & Crime",
        "municipalities": [
            "Easton"
        ],
        "counties": [
            "Talbot County"
        ]
        "key_people": [
            "Alan Lowrey (Easton Police Chief)",
            "Ron Engle (Former Town Council Member)"
        ],
        "key_locations": [
            "Route 50",

        ],
        "key_events_and_initiatives": [
            "Easton Interactive Traffic Dashboard",
            "Strategic Highway Safety Plan",
            "Vision Zero initiative",
            "Pandemic"
        ]
        "key_organizations": [
            "Washington College Geographic Information Systems Program",
            "Washington College",

        ],
        "key_bodies": [
            "Easton Police Department",
            "Maryland Highway Safety Office",
            "National Highway Traffic Safety Administration",
            "Easton Town Council",
            "Maryland General Assembly"
        ]
    }
]
```
