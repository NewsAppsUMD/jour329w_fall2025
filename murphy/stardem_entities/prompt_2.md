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

I need to make a python script called `starmdem_entities_script_1.py`.

Here are the script requirements:
- Use the `llm` command-line tool with the model `groq/meta-llama/llama-4-scout-17b-16e-instruct`
- Use subprocess to call the `llm` command
- Have the LLM process each story from `stardem_sample.json`
- Have the LLM add four fields to each story: `content_type`, `topic`, `people`, `events`, `locations`, `municipalities`, `county`, `institutions`.
- Have the LLM save the updated stories to `stories_with_entities_1.json`
- Print progress as it processes stories

Here are the guidelines:
- The `content_type` field should contain the single best-fitting content type from list provided in `content_type_list`.
- The `topic` field should contain the single best-fitting topic from list provided in `topic_list`.
- The `people` field should contain a list, separated by `;`, of important people mentioned or quoted in the story. Important people would include people like politicians, political candidates, coaches, community leaders, public officials, board members and council members.
- The `events` field should contain the names of relevant events mentioned in the text. This includes named, organized events, like a county fair or a march, and not generalized events like a fire. Use title case when an event is capitalized in the text.
- The `locations` field should contain a list, separated by `;`, of all specific places within municipalities that are mentioned in the story, such as rivers, parks, neighborhoods, buildings, and street names. Unabbreviate abbreviated street suffixes, do not include the number of the address, and, when possible, include in parentheses the name of the municipality where the place is located. 
- The `municipalities` field should contain a list, separated by `;`, of all municipalities mentioned in or central to the story. Exclude "Easton" if it is only mentioned in the dateline in the context of the location of the Star-Democrat, but not the main body of the story. If there is no municipality mentioned, put "N/A". 
- The `county` field should contain a list, separated by `;`, of the counties where the municipalities mentioned in the the story are located, based on `maryland_county_list`. When localities are mentioned across multiple stories, ensure their names are standardized. If there is no relation to one of the listed counties, put "N/A". Use title case when a county, municipality or location is capitalized in the text.
- The `institutions` field should contain a list, separated by `;`, of relevant organizations, businesses, government agencies, councils, boards, teams and other entities mentioned in the story. When organizations are mentioned across multiple stories, ensure their names are standardized. Exclude the name of the main paper, the "Star-Democrat", and the names of the publishers, "Chesapeake Publishing Group" and "Adams Publishing/APGMedia", but when the article was written by someone other than the Star-Democrat, include the name of the organization.

Things to keep in mind:
- Be careful when `content_type` == "Sports" — many of the teams will be referred to by multiple names, and they may appear to be people when they are not. For example, the "Stephen Decatur High School Seahawks" will also be referred to as "Stephen Decatur", "Decatur" and "Seahawks."
- The distinguishing characteristic between an `institution` and a `location` is that an `institution` is a body, like county board or school systemm, while a `location` is a physical place, like a town hall or school. A police department is generally an institution unless it is referenced as the site of a event, as in a physical police station.

example_output = [
    {
        "title": "Ironman brings economic boost to Cambridge",
        "date": "2025-09-19",
        "author": "Lily Tierney",
        "content": "Ironman brings economic boost to Cambridge\n\n September 19, 2025 | Star Democrat, The (Easton, MD)\n\n Author/Byline: Lily Tierney | Section: Dorchester \n \n 394\n Words \n\n Read News Document\n\n CAMBRIDGE — Cambridge residents may have noticed it has been trickier getting around this past week.Traffic has increased, reservations at their favorite restaurant are difficult to get and all hotels and Airbnb's from Salisbury to Annapolis are filled, according to Operations Manager at the Ironman Angie Hengst.\n1,250 athletes who will be participating in the Maryland Ironman on Saturday began making their way to Cambridge on Monday to preview the courses, enjoy their welcoming events and attend athlete briefings.\n\"Driving around town, it's about three times as busy as you would normally see it,\" Hengst said.\nA few years ago, the Ironman did an economic impact study on Cambridge and Dorchester Counting post-event that discovered the event has a $7.14 million impact on the community, Hengst said. This number may have increased since the study.\nThis is the 11th annual Maryland Ironman, an extreme triathlon race that requires approximately 1,200 volunteers to pull off. The Ironman Foundation has grant funding available for local nonprofits that volunteer for the race, per this year's Race Director Brian Snow.\n\"We have over $40,000 in nonprofit money, and it goes to volunteers and groups to help stimulate the economy with people participating as volunteers,\" Snow said.\nBoth Hengst and Snow said Friday that they were still looking for volunteers for Saturday's big race.\nThe race will include a 2.4-mile swim in the Choptank River in between Gerry Boyle Park at Great Marsh and the Yacht Club, finishing at the boat ramp at Gerry Boyle Park. Next, there will be a 112-mile bike ride through Dorchester County and the scenic Blackwater Wildlife Refuge. The race will finish with a 26.2-mile run through historic downtown Cambridge and beyond.\nSnow said athletes from all 50 states and over 30 countries will be participating on Saturday. He said every athlete generally comes with one other person considering the intensity of the race.\nBoth Snow and Hengst expressed their gratitude to the volunteers and residents of Cambridge and Dorchester County for being gracious hosts.\n\"I do want to put a huge thank you out to the community, you know, Cambridge, Dorchester County, everyone, for being so welcoming and supportive of the athletes,\" Hengst said.\n\"We're one of the smaller towns that hosts an event of this size, and we couldn't do it without the community's support. The athletes always comment about how nice everyone is and how welcoming it is here,\" she said. \n\n © Copyright © 2025 Star Democrat, Chesapeake Publishing Group (Adams Publishing/APGMedia). All rights reserved.",
        "docref": "news/1A33A6215B20A808",
        "article_id": "search-hits__hit--380",
        "content_source": "full_document",
        "year": 2025,
        "month": 9,
        "day": 19,
        "content_type": "News",
        "topic": "Economy & Budget",
        "people": "Angie Hengst; Brian Snow",
        "events": "Maryland Ironman",
        "locations": "Gerry Boyle Park at Great Marsh; Choptank River; Blackwater Wildlife Refuge; The Yacht Club",
        "municipalities": "Cambridge; Salisbury; Annapolis",
        "county": "Dorchester County",
        "institutions": "Ironman Foundation; Airbnb"
    },
    {
        "title": "Lions rally for first Bayside title; Caroline boys defend throne",
        "date": "2024-05-15",
        "author": "Bill Haufe",
        "content": "Lions rally for first Bayside title; Caroline boys defend throne\n\n May 15, 2024 | Star Democrat, The (Easton, MD)\n\n Author/Byline: Bill Haufe | Section: Sports \n \n 838\n Words \n\n Read News Document\n\n Queen Anne's County High's No. 3 girls doubles team of Sydney Pinder and Kara Ringold were down 4-1 when head coach Dee Fisher approached.\"I asked them, 'Hey, are you guys having fun?'\" Fisher said. \"And they were like, 'No. We're not.' I was like, 'You guys need to go out there and have fun and relax.' Just the things you can say to kids, and nothing tennis related, and it just made them relax.\"\nPinder and Ringold rallied to win, then watched Hayden Legg rally for a clinching victory at No. 3 singles Tuesday, May 7, helping Queen Anne's defeat Stephen Decatur, 4-3, at Washington College for its first Bayside Conference championship in girls tennis.\nWhile the Lions were winning their first title, North Caroline's boys were winning a second straight conference crown, topping James M. Bennett, 4-3, to cap a perfect 15-0 season.\n\"We lost one match last season,\" Bulldogs second-year boys head coach James Donelan said. \"It was their goal to go undefeated this year. And we were able to do that, which was huge.\nWe had a couple of close matches at the end of the season that just took some real grit to pull out and some real mental toughness from our boys,\" Donelan said of a 4-3 win at St. Michaels on April 24 and a 4-3 victory over Easton in the regular-season finale May 1. \"It was really impressive to watch. Their growth and their ability to face adversity, face everybody coming at you, giving you their best every single night and just finding a way to win.\"\nThe Bulldogs did that again against the South champion Clippers.\nNorth Caroline's No. 1 singles team of Josh Huster and Jesse Link defeated Cypress Schnatterly and Joe Chen, 9-7, while Ryan Canter and Hayden Kent beat Bennett's Daniel Ryu and Mason Layne, 8-4, in second doubles. But the Clippers avoided a double sweep, when Shafay Qaiser and Rishi Kandagatla earned an 8-5 win over Gavin O'Brien and Yossin Roblero-Velasquez at No. 3.\nIt remained close, as Bennett's Chen defeated Link, 8-5, at second singles, and Ryu outlasted Canter, 9-7 at No. 3. But Roblero-Velasquez rolled to an 8-1 victory over Landon Blumenthal at No. 4. Huster, who last year teamed with Rebecca White to win the Class 2A state mixed doubles title — North Caroline's first-ever state tennis title of any kind — clinched the victory against Bennett and the perfect record with an 8-3 victory over Schnatterly at No. 1.\n\"Going into this season, after the success that we had last year, we were definitely very confident,\" Donelan said. \"We knew it wasn't going to be handed to us. We knew that everybody was going to be putting a target on our back, and that they knew we only graduated one senior and then all these boys were returning.\"\nUnlike Donelan, Fisher entered the season thinking rebuild after graduating nine seniors from a year ago. Instead, the Lions went unbeaten in the North and 13-1 overall, with the lone loss coming against Decatur.\nAnd while Queen Anne's drew a rematch with the Seahawks for the Bayside championship, Fisher didn't want his team deviating from its usual approach.\n\"Just treat it like a regular match and have fun,\" Fisher said to his team.\nThe Lions' No. 1 doubles team of Lucy Taylor and younger sister Meg Taylor lost 8-6 to Decatur's Ana Pena and Emily Ferguson. But Queen Anne's Hayden Legg and Marylee Kline beat Brooke Berquist and Kalli Nordstrom, 8-2, at No. 2, while Pinder and Ringold erased their 4-1 deficit en route to an 8-6 victory over Anika Karl and Emmie Weber at No. 3.\nThe Seahawks moved to a 3-2 lead, when Pena defeated Lucy Taylor, 8-2 at first singles, and Ferguson earned an 8-2 win over Meg Taylor at No. 2. Kline tied the match at 3-3 with her 8-6 win over Nordstrom at No. 4.\nThat left No. 3 singles, where Karl built a 4-1 lead on Legg. Again Fisher spoke with his player.\n\"I was like, 'Come on Hayden. You can play better,'\" Fisher said. \"'Focus. Take your time.' And basically she just started turning it around.\"\nLegg did turn it around, rallying for an 8-6 title-clinching victory.\n\"I was like, 'It's going to be tough,'\" Fisher said. \"She's like the most chill person. She just kept coming back and coming back.\"\nYet after Legg had completed her comeback to seal the title, nobody from Queen Anne's stormed the court or hoisted their teammate onto their shoulders for a victory lap.\n\"Nobody got excited,\" Fisher said. \"We just all like took it all in, like, 'Good job Hayden.'\" Fisher said. \"I think that's just the mentality of our team. We treat it like a regular match. We just do what we do.\n\"It felt even better because we lost to Decatur during the regular season,\" Fisher said. \"Hey we fixed our wrongs, made some corrections and won it.\"\nWhat Fisher wasn't expecting came next.\n\"They were like, 'Come here coach Fisher and take a picture,'\" Fisher said. \"And then they started spraying me with silly string. It was fun.\" \n\n © Copyright © 2024 Star Democrat, Chesapeake Publishing Group (Adams Publishing/APGMedia). All rights reserved.",
        "docref": "news/1991795D2BD2A0C0",
        "article_id": "search-hits__hit--4769",
        "content_source": "full_document",
        "year": 2024,
        "month": 5,
        "day": 15,
        "content_type": "Sports",
        "people": "Dee Fisher; James Donelan",
        "events": "Bayside Conference championship",
        "locations": "Queen Anne's County High; Stephen Decatur; Washington College; James M. Bennett; St. Michaels; Easton; North Caroline High School",
        "municipalities": "Easton",
        "county": "Queen Anne's County; Caroline County; Talbot County",
        "institutions": "Lions; Bayside Conference; Bulldogs; Clippers; Seahawks"
  }
]
```

uv run python stardem_entities_script_1.py --model groq/meta-llama/llama-4-scout-17b-16e-instruct --input stardem_sample.json