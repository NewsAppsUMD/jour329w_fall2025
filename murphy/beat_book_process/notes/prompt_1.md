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

I need to make a python script called `starmdem_entities_script_1.py`.

Here are the script requirements:
- Use the `llm` command-line tool with the model `groq/meta-llama/llama-4-scout-17b-16e-instruct`
- Use subprocess to call the `llm` command
- Have the LLM process each story from `stardem_sample.json`
- Have the LLM add four fields to each story: `content_type`, `people`, `events`, `locations`, `municipalities`, `county`, `institutions`.
- Have the LLM save the updated stories to `stories_with_entities_1.json`
- Print progress as it processes stories

Here are the guidelines:
- The `content_type` field should contain the single best-fitting content type from list provided in `content_type_list`.
- The `people` field should contain a list, separated by `;`, of all people mentioned or quoted in the story. When people are mentioned across multiple stories, ensure their names are standardized. This excludes the author of the article.
- The `events` field should contain the names of specific events mentioned in the text. 
- The `locations` field should contain a list, separated by `;`, of all specific places within municipalities that are mentioned in the story, such as rivers, parks, neighborhoods and street names. Unabbreviate abbreviated street suffixes, do not include the number of the address, and, when possible, include in parentheses the name of the municipality where the place is located. 
- The `municipalities` field should contain a list, separated by `;`, of all municipalities mentioned in or central to the story. Exclude "Easton" if it is only mentioned in the dateline in the context of the location of the Star-Democrat, but not the main body of the story. If there is no municipality mentioned, put "N/A". 
- The `county` field should contain a list, separated by `;`, of the counties where the municipalities mentioned in the the story are located, based on `maryland_county_list`. When localities are mentioned across multiple stories, ensure their names are standardized. If there is no relation to one of the listed counties, put "N/A". Use title case when a county, municipality or location is capitalized in the text.
- The `institutions` field should contain a list, separated by `;`, of all organizations, businesses, government agencies, councils, boards, teams and other institutions mentioned in the story. When organizations are mentioned across multiple stories, ensure their names are standardized. Exclude the name of the main paper, the "Star-Democrat", and the names of the publishers, "Chesapeake Publishing Group" and "Adams Publishing/APGMedia", but when the article was written by someone other than the Star-Democrat, include the name of the organization. When events take place at specific institutions, like libraries, schools or businesses, these places should be considered `institutions`, not locations. When an institution is also the name of the event, but it in both `institutions` and `events`.

Be careful when `content_type` == "Sports" — many of the teams will be referred to by multiple names, and they may appear to be people when they are not. For example, the "Stephen Decatur High School Seahawks" will also be referred to as "Stephen Decatur", "Decatur" and "Seahawks."

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
        "people": "Angie Hengst; Brian Snow",
        "events": "Maryland Ironman",
        "locations": "Gerry Boyle Park at Great Marsh; Choptank River; Blackwater Wildlife Refuge",
        "municipalities": "Cambridge; Salisbury; Annapolis",
        "county": "Dorchester County",
        "institutions": "Ironman Foundation; Airbnb; The Yacht Club"
    },
    {
        "title": "Events around Caroline",
        "date": "2025-01-15",
        "author": "Connie Connolly",
        "content": "Events around Caroline\n\n January 15, 2025 | Star Democrat, The (Easton, MD)\n\n Author/Byline: Connie Connolly | Section: Calendar \n \n 488\n Words \n\n Read News Document\n\n Those looking to have an event included in the weekly Caroline County calendar are asked to email details to community@stardem.com.DENTONArtist of the month exhibit, Friday, Jan. 17, 4 to 6 p.m., The Foundry, 401 Market St. Experience the raw intensity of self-taught artist Andrew Wingate's bold, vivid paintings created during his journey to sobriety. His work reflects transformation and resilience.\nAnime matinee, Saturday, Jan. 18, 1 to 3 p.m., Central Library. For teens. Grab some popcorn and Pocky and watch \"The Boy and the Beast,\" an adventurous and heart-warming story full of action, fantasy and fun.\nMartin Luther King Jr. Day march, Jan. 20, 9 a.m., Lockerman Middle School. March begins at 10 a.m. and concludes at the Caroline County Courthouse where the \"I Have a Dream Speech\" will be read and bag lunches will be distributed to everyone.\nBingo, 7:30 p.m., Tuesdays, American Legion Post 29, 9238 Legion Road. 5 p.m. doors open, 7:30 p.m. games start. Info:410-479-2708.\nSamaritan House Thrift Shop, 10 a.m. to 2 p.m. Wednesday to Friday; 9 a.m. to noon Saturday. 5th Street behind the post office.\nThird Thursdays in Downtown Denton, 5 to 7 p.m., third Thursdays, downtown. Businesses extend their hours and offer specials. Info: DowntownDenton.com.\nAaron's Place Food Pantry, 9:30 a.m. to 2:30 p.m., Tuesday & Wednesday, 401 Aldersgate Drive.\nPaws for Reading, 3:40 to 4:25 p.m., every fourth Thursday, Central Branch library. Children ages 5 to 12 can proactice reading to a trained service dog. One registrant per session. Register: carolib.libcal.com.\nStorytime, 10:30 to 11 a.m. every Wednesday through April 30, Central Branch library. For children ages birth to 5.\nMuseum of Rural Life, 11 a.m. to 4 p.m., every Saturday, 16 N. Second Street. World War I and II, a sharecropper's cabin, new Buffalo Soldier exhibit, among many other artifacts and stories about Caroline County. A docent is on hand for tours. Free to the public. Info: carolinehistory.org or 410-479-2055 and leave a message.\nFEDERALSBURGMonday Bingo, 6 p.m. doors open; 7 p.m. bingo begins., Every Monday. Federalsburg VFW Post 5246, 2630 Veterans Drive. Cash prizes, food available.\nAaron's Place Food Pantry, 4 to 6 p.m., Wednesdays, Community Civic League, 3439 Laurel Grove Road.\nFederalsburg Floods, Fridays 10 a.m. to noon, Saturdays 10 a.m. to 2 p.m., Federalsburg Heritage Museum, 100 Covey Williams Ave. Eight significant floods that devastated Federalsburg in the 20th century are highlighted in a new exhibit at the Historical Society's museum.\nGOLDSBOROGiving Grace Food Pantry, Goldsboro VFC, 700 Old Line Road. 7 a.m. until; second Saturdays. Info: 302-270-1948.\nGREENSBOROFood pantry, 4 to 7 p.m. Thursday, 7 to 9 a.m. Saturday, 10 a.m. to 1 p.m. Monday. Aaron's Place Pantry at Greensboro Connects, 111 S. Main St., side entrance.\nStorytime, 10:30 to 11 a.m. every Tuesday through April 29, North County Branch library. For children ages birth to 5.\nRIDGELYMartin's House & Barn, First Saturdays thrift store open 8 a.m. to noon. Drive-thru pantry and thrift store hours: 8:30 to 11:30 a.m. Tuesday, Thursday and Friday; 6 to 7:30 p.m. Wednesday. \n\n © Copyright © 2025 Star Democrat, Chesapeake Publishing Group (Adams Publishing/APGMedia). All rights reserved.",
        "docref": "news/19E1EFE119E0EC78",
        "article_id": "search-hits__hit--1987",
        "content_source": "full_document",
        "year": 2025,
        "month": 1,
        "day": 15,
        "content_type": "Calendars",
        "people": "Andrew Wingate",
        "events": "Artist of the month exhibit; Anime matinee; Martin Luther King Jr. Day march; Bingo; Paws for Reading; Storytime; Federalsburg Floods; Aaron's Place Food Pantry; Giving Grace Food Pantry; Food pantry; Drive-thru pantry and thrift store.",
        "locations": "Market Street (Denton); Legion Road (Denton); 5th Street (Denton); Aldersgate Drive (Denton); N. Second Street (Denton); Veterans Drive (Federalsburg); Laurel Grove Road (Federalsburg); Covey Williams Avenue (Federalsburg); Old Line Road (Goldsboro); S. Main Street (Goldsboro)",
        "municipalities": "Denton; Federalsburg; Goldsboro; Ridgely",
        "county": "Caroline County",
        "institutions": "The Foundry; Central Library; Lockerman Middle School; Caroline County Courthouse; American Legion Post 29; Samaritan House Thrift Shop; Aaron's Place Food Pantry; Museum of Rural Life; VFW Post 5246; Central Branch Library; Community Civic League; Federalsburg Heritage Museum; Historical Society; Goldsboro VFC; Giving Grace Food Pantry; Greensboro Connects; North County Branch library; Martin's House & Barn"
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
        "people": "Sydney Pinder; Kara Ringold; Dee Fisher; Hayden Legg; James Donelan; Josh Huster; Jesse Link; Cypress Schnatterly; Joe Chen; Ryan Canter; Hayden Kent; Daniel Ryu; Mason Layne; Shafay Qaiser; Rishi Kandagatla; Gavin O'Brien; Yossin Roblero-Velasquez; Landon Blumenthal; Rebecca White; Lucy Taylor; Meg Taylor; Ana Pena; Emily Ferguson; Marylee Kline; Brooke Berquist; Kalli Nordstrom; Anika Karl; Emmie Weber",
        "events": "Tennis; Bayside Conference championship",
        "locations": "",
        "municipalities": "Easton",
        "county": "Queen Anne's County; Caroline County; Talbot County",
        "institutions": "Queen Anne's County High; Lions; Queen Anne's County High Lions; Stephen Decatur; Washington College; Bayside Conference; North Caroline; Bulldogs; North Caroline Bulldogs; James M. Bennett; Clippers; James M. Bennett Clippers; Bennett; St. Michaels; Easton; Schnatterly; Decatur; Seahawks; Stephen Decatur Seahawks"
  }
]
```

uv run python stardem_entities_script_1.py --model groq/meta-llama/llama-4-scout-17b-16e-instruct --input stardem_sample.json