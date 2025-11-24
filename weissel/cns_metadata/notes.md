CNS Metadata 9/27/25

The tag I chose to look into last time was "Donald Trump". I picked 5 stories with that same tag

1. Story: Pardoned Maryland Jan. 6 participants find support after convictions (https://cnsmaryland.org/2025/05/09/pardoned-maryland-jan-6-participants-find-support-after-convictions/)

- 3 key people: Donald Trump, Steven Cook, Joe Biden

- 3 main organizations/institutions: U.S. Governemnt, Republican Women of Baltimore County, Maryland Republicans

- 3 geographic locations: Washington D.C., Maryland, Fredrick County

- 3 short (two-word) topics: Election-Results, Maryland-Politics, Donald Trump

- Story type: Feature

- 1-5 rating with focus on impact on people: 2

LLM Prompt: uv run python -m newspaper --url=https://cnsmaryland.org/2025/05/09/pardoned-maryland-jan-6-participants-find-support-after-convictions/ -of=text | uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "Extract structured metadata from this news story and return as JSON with these exact fields:
{
  \"url\": \"the url of the story\",
  \"people\": [\"list of up to 3 people with their titles/roles\"],
  \"organizations\": [\"government agencies, companies, groups mentioned\"],  
  \"locations\": [\"cities, counties, states, specific places\"],
  \"topics\": [\"3-5 topic tags, max 2 words each\"],
  \"story_type\": \"breaking news, feature, analysis, investigation, other\",
  \"impact\": \"a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people\",
  \"
}"

I started with this prompt and got this results: 


LLM Response: "url": "https://cnsmaryland.org/interactives/2025/pardoned-maryland-jan-6-participants-find-support-after-convictions/",
  "people": [
    "Steven Cook — pardoned Jan. 6 rioter, assaulted police",
    "Louise Baker — president, Republican Women of Baltimore County",
    "Robert Pape — director, Chicago Project on Security & Threats"
  ],
  "organizations": [
    "Republican Women of Baltimore County",
    "Salisbury University",
    "American Legion Post #10",
    "Chicago Project on Security & Threats",
    "Justice Department",
    "House Freedom Caucus",
    "Office of Congressional Ethics"
  ],
  "locations": [
    "Boonsboro, Maryland",
    "Frederick County, Maryland",
    "Salisbury, Maryland",
    "Pylesville, Maryland",
    "Millersville, Maryland",
    "Montgomery County, Maryland",
    "Howard County, Maryland",
    "Baltimore County, Maryland",
    "Frederick City, Maryland",
    "Hyattsville, Maryland",
    "Gaithersburg, Maryland",
    "Silver Spring, Maryland"
  ],
  "topics": ["Jan 6 pardons", "political violence", "Maryland GOP", "extremism", "Trump support"],
  "story_type": "feature",
  "impact": 4

  Overall what I expected but I need to empasize I only want 3 locations in my future requests. 


2. Story: Government shutdown and mass firings loom: budget agreement yet to be reached (https://cnsmaryland.org/2025/09/25/government-shutdown-and-mass-firings-loom-budget-agreement-yet-to-be-reached/)

- 3 key people: Donald Trump, Chuck Schumer, Ben Cardin

- 3 main organizations/institutions: White House Office of Management and Budget, Sentate, House of Reps

- 3 geographic locations: Washington, D.C., California, DMV

- 3 short (two-word) topics: Government-Shutdown, Civilian-Employees, Government-Spending

- Story type: Analysis

- 1-5 rating with focus on impact on people: 5

Prompt: uv run python -m newspaper --url=https://cnsmaryland.org/2025/09/25/government-shutdown-and-mass-firings-loom-budget-agreement-yet-to-be-reached/ -of=text | uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "Extract structured metadata from this news story and return as JSON with these exact fields:
{
  \"url\": \"the url of the story\",
  \"people\": [\"list of up to 3 people with their titles/roles\"],
  \"organizations\": [\"government agencies, companies, groups mentioned\"],  
  \"locations\": [\"total of 3 cities, counties, states, specific places\"],
  \"topics\": [\"3-5 topic tags, max 2 words each\"],
  \"story_type\": \"breaking news, feature, analysis, investigation, other\",
  \"impact\": \"a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people\",
  \"
}"

Response: "url": "",
  "people": [
    "Sen. Chris Van Hollen, D-Maryland",
    "Senate Majority Leader John Thune, R-South Dakota",
    "Senate Minority Leader Chuck Schumer, D-New York"
  ],
  "organizations": [
    "White House Office of Management and Budget (OMB)",
    "House of Representatives",
    "Senate",
    "Capital News Service"
  ],
  "locations": [
    "Washington, D.C.",
    "Maryland",
    "South Dakota"
  ],
  "topics": [
    "government shutdown",
    "budget impasse",
    "federal workers"
  ],
  "story_type": "breaking news",
  "impact": 5

  For some reason it did not supply the URL back to me. I think this article is a bit more analysis than breaking news but that is just me. South Daokta is a total miss here. The state is mentioned because of John Thune but it has nothing to do with the impact of this story. 

3. Story: Some Maryland brewers concerned tariffs will make tough times tougher (https://cnsmaryland.org/2025/05/14/maryland-brewers-concerned-tariffs-will-make-tough-times-tougher/)

- 3 key people: Donald Trump, Adam Benesch, 

- 3 main organizations/institutions: Union Craft Brewing, U.S. Government, 

- 3 geographic locations: Maryland, China, U.S.

- 3 short (two-word) topics: Tarrifs, Breweries, Business-Closure

- Story type: Feature

- 1-5 rating with focus on impact on people: 2

Promt: uv run python -m newspaper --url=https://cnsmaryland.org/2025/05/14/maryland-brewers-concerned-tariffs-will-make-tough-times-tougher/ -of=text | uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "Extract structured metadata from this news story and return as JSON with these exact fields:
{
  \"url\": \"the url of the story\",
  \"people\": [\"list of up to 3 people with their titles/roles\"],
  \"organizations\": [\"government agencies, companies, groups mentioned\"],  
  \"locations\": [\"total of 3 cities, counties, states, specific places\"],
  \"topics\": [\"3-5 topic tags, max 2 words each\"],
  \"story_type\": \"breaking news, feature, analysis, investigation, other\",
  \"impact\": \"a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people\",
  \"
}"

Response: "url": "https://cnsmaryland.org/2025/04/15/some-maryland-brewers-concerned-tariffs-will-make-tough-times-tougher/",
  "people": [
    "Adam Benesch – cofounder, Union Craft Brewing",
    "Hugh Sisson – CEO/founder, Heavy Seas Beer",
    "Rep. Nikema Williams – U.S. representative (D-GA), co-chair Small Brewers Caucus"
  ],
  "organizations": [
    "Union Craft Brewing",
    "Heavy Seas Beer",
    "Brewers Association",
    "Trump administration",
    "Guinness Open Gate Brewery",
    "Flying Dog Brewery",
    "DuClaw Brewing"
  ],
  "locations": [
    "Baltimore, Maryland",
    "Relay, Maryland",
    "Frederick, Maryland"
  ],
  "topics": [
    "aluminum tariffs",
    "craft beer",
    "consumer prices",
    "supply chain",
    "business closures"
  ],
  "story_type": "feature",
  "impact": 4
}

Lots of Organizations provided. A much more focused look at locations than me. 

4. Story:Maryland lawmakers decry possible Medicaid cuts amid 24-hour protest near US Capitol (https://cnsmaryland.org/2025/05/08/maryland-lawmakers-decry-possible-medicaid-cuts-amid-24-hour-protest-near-us-capitol/)

- 3 key people: Chris Van Hollen, Donald Trump, Nicole Jorwic

- 3 main organizations/institutions: Caring Across Generations, U.S. Government 

- 3 geographic locations: U.S. Capitol, Maryland

- 3 short (two-word) topics: Medicaid, Protest, Democrats

- Story type: analysis

- 1-5 rating with focus on impact on people: 3

Prompt: uv run python -m newspaper --url=https://cnsmaryland.org/2025/05/08/maryland-lawmakers-decry-possible-medicaid-cuts-amid-24-hour-protest-near-us-capitol/ -of=text | uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "Extract structured metadata from this news story and return as JSON with these exact fields:
{
  \"url\": \"the url of the story\",
  \"people\": [\"list of up to 3 people with their titles/roles\"],
  \"organizations\": [\"government agencies, companies, groups mentioned\"],  
  \"locations\": [\"total of 3 cities, counties, states, specific places\"],
  \"topics\": [\"3-5 topic tags, max 2 words each\"],
  \"story_type\": \"breaking news, feature, analysis, investigation, other\",
  \"impact\": \"a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people\",
  \"
}"

Response: "url": "https://cnsmaryland.org/2025/04/10/maryland-lawmakers-decry-possible-medicaid-cuts-amid-24-hour-protest-near-us-capitol/",
  "people": [
    "Nicole Jorwic – chief program officer, Caring Across Generations",
    "Sen. Chris Van Hollen – U.S. senator, Maryland",
    "Rep. Jamie Raskin – U.S. representative, Maryland"
  ],
  "organizations": [
    "Caring Across Generations",
    "Medicaid",
    "House Energy and Commerce Committee",
    "National Partnership for Women and Families"
  ],
  "locations": [
    "Washington, D.C.",
    "Carroll County, Maryland",
    "National Mall"
  ],
  "topics": [
    "Medicaid cuts",
    "healthcare advocacy",
    "disability rights",
    "protest vigil"
  ],
  "story_type": "feature",
  "impact": 4

  Very Similar people included by LLM and me. Probably the best response of the 4 so far. 


5. Story:As Black Lives Matter Plaza becomes rubble, onlookers mourn symbol of hope (https://cnsmaryland.org/2025/03/13/as-black-lives-matter-plaza-becomes-rubble-onlookers-mourn-symbol-of-hope/)

- 3 key people: Muriel Bowser, Donald Trump

- 3 main organizations/institutions: D.C. Government, D.C. Residents

- 3 geographic locations: D.C. Maryland

- 3 short (two-word) topics: BLM, Donald Trump, Muriel Bowser

- Story type: Feature

- 1-5 rating with focus on impact on people: 3

Prompt: uv run python -m newspaper --url=https://cnsmaryland.org/2025/03/13/as-black-lives-matter-plaza-becomes-rubble-onlookers-mourn-symbol-of-hope/ -of=text | uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "Extract structured metadata from this news story and return as JSON with these exact fields:
{
  \"url\": \"the url of the story\",
  \"people\": [\"list of up to 3 people with their titles/roles\"],
  \"organizations\": [\"government agencies, companies, groups mentioned\"],  
  \"locations\": [\"total of 3 cities, counties, states, specific places\"],
  \"topics\": [\"3-5 topic tags, max 2 words each\"],
  \"story_type\": \"breaking news, feature, analysis, investigation, other\",
  \"impact\": \"a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people\",
  \"
}"

Response: 
  "url": "",
  "people": ["Karen Byrd (chef from Columbus, OH)", "Giselle Mörch (Silver Spring, MD resident)", "Dr. Donna Huntley-Newby (nurse from Providence, RI)"],
  "organizations": ["Black Lives Matter", "D.C. Mayor Muriel Bowser's office", "Republican-controlled Congress"],
  "locations": ["Washington, D.C.", "Columbus, Ohio", "Silver Spring, Maryland"],
  "topics": ["racial justice", "public art", "political symbolism"],
  "story_type": "feature",
  "impact": 4


Once again no URL, not sure why that is happening. The Columbus, Ohio is another weird one where I asked the LLM to give me 3 so it just graps for a third answer.


Reflection: 

The LLM does an acceptable job at generating metadata for these stories. Compared to my responses it seems to lack some of the context. For example when asking about location a few times I was provided with a third location that was not super relevant but I was proivded with it just becasue I asked. For the last story it provided Columbus, Ohio when the story was about the removal of the BLM Plaza in D.C., but since one of the people in the story who was interviewed was from OH then it gave me that. 

I did not feel like the stories I picked were super impactful so I feel the LLM over inflated the impact. My average impact was 3 and the LLM was a 4. This I think it just the LLM not knowing the context. Telling the LLM to search the web for similiar stories to access impact could be a good way to help with this.

In the future giving the LLM a range of up to five responses would be the best way to have it generate metadata as then it would not supply a response for the sake of it. 

I tried this again for the first story and here is what I got: 

Prompt: uv run python -m newspaper --url=https://cnsmaryland.org/2025/05/09/pardoned-maryland-jan-6-participants-find-support-after-convictions/ -of=text | uv run llm -m groq/moonshotai/kimi-k2-instruct-0905 "Please help me extract structured metadata from this news story and return as JSON with these exact fields:

Please only supply metadata if it is important, no not give additional details.
{
  \"url\": \"the url of the story\",
  \"people\": [\"list of up to 5 people with their titles/roles\"],
  \"organizations\": [\"list of up to 5 government agencies, companies, groups mentioned\"],  
  \"locations\": [\"list of up to 5 cities, counties, states, specific places\"],
  \"topics\": [\"list of up to 5 topic tags, max 2 words each\"],
  \"story_type\": \"breaking news, feature, analysis, investigation, other\",
  \"impact\": \"a rating of the story's importance on a scale from 1 to 5, taking into account its impact on people\",
  \"
}"

Response: "url": "",
  "people": ["Steven Cook - Jan 6 pardoned rioter", "Louise Baker - RWBC president", "Robert Pape - U Chicago security scholar", "Robinson Woodward-Burns - Howard University professor", "Adam Obest - pardoned rioter"],
  "organizations": ["Republican Women of Baltimore County", "University of Chicago Project on Security & Threats", "American Legion Post #10", "Salisbury University", "Justice Department"],
  "locations": ["Boonsboro MD", "Frederick County MD", "Salisbury MD", "Montgomery County MD", "Baltimore County MD"],
  "topics": ["Jan 6 pardons", "political violence", "Maryland GOP", "extremism normalization", "suburban rage"],
  "story_type": "feature",
  "impact": 4
}

It needs some more fine tuning but it did eliminate the issue of giving info just to give it. In the future I would also supply the LLM with more info on CNS and the specific reason I want metadata. In our last acitivty with tags when I supplied more info on CNS and what I wanted I was happier with the results. So I think doing this with more (50-500) stoires would be extremly beneficial becasue you could tell the LLM to create a plan for generating metadata that always follows the same format instead of generating it each time. In an ideal scenario CNS would set up an LLM to supply metadata for each story added to the website and tweak any past stories not that the new one is added if a change is neemed. Having an LLM supply somthing like metadata would be a great use. 

This process could be simlified by prompting the LLM one longer response and then asking for the metadata in a chart. Using the \ format made it a bit more complicated so exporting to another file would also work. It would be nice to have a spreadsheet to then compare every story and then easily see what speciifc pieces of the Metadata are being used the most. 