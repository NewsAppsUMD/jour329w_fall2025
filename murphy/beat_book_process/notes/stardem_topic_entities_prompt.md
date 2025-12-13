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

I need to make a python script called `education_script_v1.py`.

Here are the script requirements:
- Use the `llm` command-line tool with the model `groq/moonshotai/kimi-k2-instruct-0905`
- Use subprocess to call the `llm` command
- Have the LLM process each story from `education_stories.json`
- Have the LLM add the following fields to each story: `content_type`,`regions`, `municipalities`, `counties`, `key_people`, `key_locations`, `key_events`, `key_initiatives`, `key_establishments`, `key_organizations`, `key_bodies`.
- Have the LLM save the updated stories to `education_stories_with_entities.json`
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
- The `key_events` field should contain a json array of the names of relevant organized events or initiatives central to the story. This includes named, planned events, like a county fair or a march. It does not include generalized events like a fire or funeral.
- The `key_initiatives` field should contain a json array of the names of relevant initiatives central to the story, like legislation, policies or a town plan. 
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
        "title": "Delean-Botkin resigns from Talbot Board of Education",
        "date": "2023-08-04",
        "author": "Maggie Trovato; mtrovato@chespub.com",
        "content": "Delean-Botkin resigns from Talbot Board of Education\n\n August 4, 2023 | Star Democrat, The (Easton, MD)\n\n Author/Byline: Maggie Trovato; mtrovato@chespub.com | Page: 1 | Section: News \n \n 472\n Words \n\n Read News Document\n\n EASTON - Susan Delean-Botkin has stepped down from the Talbot County Board of Education since being appointed an Oxford Commissioner.In an interview, Delean-Botkin said she made the decision to leave the school board due to personal reasons and her new role in Oxford's local government.Delean-Botkin said she already misses being on the Board of Education \"tremendously.\" \"School board was a fabulous experience,\" she said. \"Interacting with really great administrators, wonderful teachers, fantastic students, working with the board members, all of whom were really top quality people to work with.\" Delean-Botkin was sworn into the Talbot County Board of Education District 5 seat in January 2017. She was elected president of the board in December 2020 and held the role through 2022.Moving forward, Delean-Botkin said she hopes the Board of Education continues to maintain the county's high graduation rate and low dropout rate, expand its Career and Technical Education completer courses and implement the Blueprint for Maryland's Future, a statewide plan to increase public education funding, improve student outcomes and improve the quality of public education.\"The other big thing that we're very proud of is having as many students as wish to go ahead and take the Advanced Placement classes and exams,\" Delean-Botkin said.At a July 19 Talbot County Board of Education meeting, President Emily Jackson said the board wishes Delean-Botkin the best of luck.\"We will miss her words of wisdom and her guidance,\" Jackson said.Talbot County Public Schools Executive Assistant Charlene Gould said in an email that the governor's office has been notified of the vacancy and will appoint a new board member to fill Delean-Botkin's seat until elections in November 2024.She said interested candidates can submit an application to the Governor's Appointments Office.In June, Commissioners Tom Costigan and Jimmy Jaramillo appointed Delean-Botkin to fill Commissioner Brian Wells' seat.Wells resigned at the June 27 Commissioners of Oxford meeting. He said he was resigning because he was moving to Easton.Before being appointed, Delean-Botkin ran against and lost to now Commissioner Katrina Greer. Greer took the seat of Jaramillo, who did not seek reelection.Delean-Botkin said her new role as Oxford commissioner is a \"challenging\" one.\"I think what we have to look at is, Oxford a town of about 600 folks,\" she said.\"Three sides are surrounded by water, so we have limits on growth. People tend to want to move to Oxford because of the quality of life.Majority of people that I talk to do not want to see many things change. They want to maintain the integrity of the town.\" \n \n Caption: PHOTO BY MAGGIE TROVATO\n \nSusan Delean-Botkin has resigned from the Talbot County Board of Education. \n \n Memo: \"The other big thing that we're very proud of is having as many students as wish to go ahead and take the Advanced Placement classes and exams.\" - Susan Delean-Botkin \n\n © Copyright © 2023 Star Democrat, Chesapeake Publishing Group (Adams Publishing/APGMedia). All rights reserved.",
        "docref": "news/19344042DCBF8EE0",
        "article_id": "search-hits__hit--8987",
        "content_source": "full_document",
        "year": 2023,
        "month": 8,
        "day": 4,
        "content_type": "News",
        "primary_topic": "Education",
        "secondary_topic": "Local Government & Politics",
        "regions": [
            "Maryland"
        ],
        "municipalities": [
            "Oxford"
        ],
        "counties": [
            "Talbot County"
        ],
        "key_people": [
            "Susan Delean-Botkin (Former Talbot County Board of Education Member)",
            "Emily Jackson (Talbot County Board of Education President)"
        ],
        "key_locations": [],
        "key_events": [],
        "key_initiatives":[
            "Blueprint for Maryland's Future"
        ],
        "key_establishments": [],
        "key_organizations": [],
        "key_bodies": [
            "Talbot County Board of Education",
            "Talbot County Public Schools",
            "Governor's Appointments Office",
            "Commissioners of Oxford"
        ]
    },
    {
        "title": "New director hired at Chesapeake College in Cambridge",
        "date": "2023-08-08",
        "author": "",
        "content": "New director hired at Chesapeake College in Cambridge\n\n August 8, 2023 | Star Democrat, The (Easton, MD)\n\n Page: A1 | Section: News \n \n 442\n Words \n\n Read News Document\n\n CAMBRIDGE - Lorelly Solano is combining her interests in education and public policy in her new role as director of the Chesapeake College Cambridge Center.\"I enjoyed working directly with the students - hearing about their dreams and learning about their challenges while I've helped them plan their academic journeys,\" Solano said.\"This new role will be a bit different for me, but I will try to bring that student perspective into everything I do here.\" As director of the center, located on Race Street, Solano will lead the staff in providing all the services Cambridge-based students need to be successful.In the coming months, Cambridge residents are likely to meet Solano as she begins her community outreach efforts.The Cambridge Center, Solano said, is a resource for everyone in Dorchester County, playing a critical role in the economic and social health of the downtown area.In addition to credit classes in both transfer and career programs, the center offers workforce training, personal enrichment opportunities and meeting spaces for community organizations.The center also houses the American Job Center.\"We're an education center for students of all ages, but I hope residents here also see us as a center of community growth,\" Solano said.Solano first joined Chesapeake as an English as a Second Language instructor. She was later the academic and career adviser guiding students through actionable plans to achieve their goals.A native of Costa Rica, Solano came to the United States as a graduate student.After earning her bachelor's degree in Costa Rica, she worked for an international flower exporter as she continued her studies toward licensure at the University of Costa Rica.Her future plans took a turn when a professor at the university asked if she was adventurous.Thinking that the professor meant bungee jumping or some other daredevil sport, Solano prepared to decline. Instead, the professor asked if she would be interested in taking on a new academic challenge in a different country. He recommended her for a graduate research post at the University of Maryland.While working on \"green\" roof research and earning her master's degree in natural resources science at College Park, Solano's interest grew in building sustainable communities through policy and education.She went on to earn a Ph.D.in public policy and urban affairs at the University of Delaware.\"It's ironic that I studied urban affairs and ended up in a rural area,\" Solano said. \"Rural and urban areas face many of the same challenges, though, and people in both areas want the same things.\" Better lives and a greater sense of community, Solano said, are common desires for most people.The Cambridge Center provides both, she added. \n \n Caption: SUBMITTED.\n \nLorelly Solano is the new director of the Chesapeake College Cambridge Center. \n\n © Copyright © 2023 Star Democrat, Chesapeake Publishing Group (Adams Publishing/APGMedia). All rights reserved.",
        "docref": "news/1934F50946BF3FC8",
        "article_id": "search-hits__hit--8950",
        "content_source": "full_document",
        "year": 2023,
        "month": 8,
        "day": 8,
        "content_type": "News",
        "primary_topic": "Education",
        "secondary_topic": "Economy & Budget",
        "regions": [
            "Maryland",
            # you might want to include "Costa Rica", but it's not relevant to the story because it has nothing to do with the board of education in Oxford itself
            "Delaware"
        ],
        "municipalities": [
            "Cambridge"
        ],
        "counties": [
            "Dorchester County"
        ],
        "key_people": [
            "Lorelly Solano (Director, Chesapeake College Cambridge Center)"
        ],
        "key_locations": [
            "Race Street (Cambridge)",
            "College Park"
        ],
        "key_events": [],
        "key_initiatives": [],
        "key_establishments": [
            "Chesapeake College Cambridge Center",
            "American Job Center"
        ],
        "key_organizations": [
            # you might want to include "University of Costa Rica", but it's not relevant to the story because it has nothing to do with the board of education in Oxford itself, only to the person, who the story is not about
            "University of Maryland",
            "University of Delaware"
        ],
        "key_bodies": []
    }
]
```
]

uv run python education_script_v1.py --model groq/moonshotai/kimi-k2-instruct-0905 --input education_stories.json --output education_stories_with_entities.json