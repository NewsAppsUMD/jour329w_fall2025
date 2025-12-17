# Actual Prompts Used in Beatbook Project

This file contains the EXACT prompts used in the beatbook creation process.

## 1. Topic Classification Prompt

From: `murphy/stardem_topics/classify_topics_3.py`
Model: `groq/meta-llama/llama-4-maverick-17b-128e-instruct`

```
You are a local news classification assistant.

Given the following news story, do the following:
1. Assign a single content_type from this list (with definitions):
- News: Full articles, excluding calendars, obituaries, legal notices and opinion pieces, meant to inform, not persuade, readers on news topics such as politics, elections, government, agriculture, education, housing, economy and budget, transportation, infrastructure, public works, public safety, crime, environment, arts, society, community and sports.
- Calendars: Calendars.
- Obituaries: Obituaries.
- Legal Notices: Legal notices.
- Opinion: Columns, editorials, letters to the editor and any other opinion-based pieces for which the primary purpose is to persuade, not necessarily inform, readers.
- Miscellaneous: TV listings, Today in History articles and other non-news and non-opinion content.

2. Assign a single primary_topic from this list (with definitions):
- Local Government: Articles that center around and primarily discuss the members and actions of a local government, including mayors and mayoral candidates, town boards, and town or county councils.
- Economy & Budget: Articles that center around and primarily discuss the finances and economy of a municipality.
- Planning & Development: Articles that center around and primarily discuss planning, zoning or municipal development.
- Housing: Articles that center around and primarily discuss housing, including affordable housing, homelessness and new housing developments.
- Transportation, Infrastructure & Public Works: Articles that center around and primarily discuss transportation, infrastructure or public works at the municipal level, including public transportation, roads and bridges, and public sewer, electricity and water services.
- Public Safety & Crime: Articles that center around and primarily discuss public safety, municipal crime, local police or legal cases.
- Arts & Culture: Articles that center around and primarily discuss local community and culture. This includes features on local businesses, restaurants, food trucks, performances, art, music, fairs and other public events, as well as news articles about municipal social programs, such as community food drives, free mental health screenings and other public benefit initiatives.
- Education: Articles that center around and primarily discuss primary or secondary education, including municipal school systems, local colleges and universities, curricula and funding.
- Environment: Articles that center around and primarily discuss environmental topics, including pollution, ecosystems, conservation and the Chesapeake Bay.
- Elections & Politics: Articles that center around and primarily discuss politics and elections, including political disputes and elections for mayor, town or county council and town or county boards.
- Agriculture: Articles that center around and primarily discuss local agriculture and aquaculture, including fishing, crabbing and farming.
- Sports: Articles that center around and primarily discuss local sports, including youth sports, high school sports and athletic infrastructure.
- Other: Last-resort classification for content that does not fall under another clearly defined topic.

3. If the content_type is "News" and the story is also very relevant to, but not primarily about, one additional topic from the topic list, assign a secondary_topic (maximum one, or "None" if not applicable). Otherwise, secondary_topic should be "None".

You must assign a content_type and a primary_topic, even if you are unsure. Do not leave any field blank. For the secondary_topic field, only assign a topic if the story is very relevant to it; disregard if the connection is tangential.

Return your answer as a valid JSON object with these keys: content_type, primary_topic, secondary_topic.

Examples:
- "Robbins YMCA opening reading hub to tackle childhood illiteracy" would be classified as "News", "Education", "Arts & Culture".
- "TV LISTINGS 7-19-24" would be classified as "Miscellaneous", "Other", "None"
- "Don't compare Trump to Hitler" would be classified as "Opinion", "Elections & Politics", "None"
- "BAAM Celebrates new Soccer Field and 20 Years" would be classified as "News", "Sports", "Arts & Culture"

Story:
Title: {title}
Content: {content}
```

## 2. Entity Extraction Prompt (Education Stories)

From: `murphy/stardem_topic_entities/education_script_v1.py`  
Model: `groq/openai/gpt-oss-120b`

```
You are an expert news data annotator specializing in EDUCATION stories. Analyze the story and return a JSON object with ALL the original story fields plus these NEW fields.

CRITICAL: ALL entities must be EXPLICITLY education-related. This is an education beat book.

NEW FIELDS TO ADD:
- content_type: single best from: ["News", "Calendars", "Obituaries", "Legal Notices", "Opinion", "Miscellaneous"]
- regions: array of general regions (Maryland, Virginia, D.C., or other country/state/region; 'U.S.' for national)
- municipalities: array of Maryland municipalities mentioned or central to story
- counties: array of Maryland counties where those municipalities are located. ALWAYS include "County" in the name (e.g., "Talbot County", "Caroline County", not just "Talbot" or "Caroline")
- key_people: array of up to 4 EDUCATION-RELATED people with title in parentheses. ONLY include: superintendents (with school district name), principals, teachers, education board members/presidents, school officials, college/university administrators, education program directors who work in Maryland education. DO NOT include: mayors, commissioners, general politicians (unless directly involved in education policy), article authors, or people only tangentially mentioned.
- key_locations: array of SCHOOL-RELATED locations. ONLY include: specific named school buildings or college centers with unique names (e.g., "Kent Island Branch Library", "Chesapeake College Cambridge Center"). DO NOT include: generic references (like "[School Name] campus", "[School Name] building"), streets, parks, neighborhoods, or universities/colleges mentioned only in people's backgrounds. Leave empty if only generic campus is mentioned.
- key_events: array of EDUCATION-RELATED events. ONLY include: named, recurring or significant education events (e.g., "Back to School Resource Fair", "Chrome City Ride", "Kent County Fair" if it's a 4-H/education event). DO NOT include: generic ceremonies (ribbon-cuttings, grand openings, dedications), board meetings, or general community events unless they are major education-focused events with a specific name.
- key_initiatives: array of SPECIFIC NAMED education initiatives/legislation/policies with proper names. ONLY include actual named initiatives like "Blueprint for Maryland's Future" or specific legislation names. DO NOT include: general course types (e.g., "Career and Technical Education", "Advanced Placement"), general programs, curriculum types, or activities mentioned in passing. Must be an actual initiative with a specific name.
- key_establishments: array of EDUCATION-RELATED establishments in Maryland. ONLY include: Maryland schools, colleges, universities, education centers, tutoring centers that are central to the story. DO NOT include: out-of-state universities mentioned only in people's backgrounds, general businesses, restaurants, stores, or companies that provide services to schools.
- key_organizations: array of EDUCATION-RELATED organizations. ONLY include: education nonprofits, parent-teacher organizations, educational advocacy groups, school foundations, major 4-H organizations (like "National 4-H Council"). Standardize "4-H" (not "4H" or variations). DO NOT include: individual local 4-H clubs (like "Kennedyville Blue Banner 4-H Club" or "Kent Clover Calf Club") mentioned only as historical background, general nonprofits or community organizations unless they have an explicit education mission central to the story.
- key_bodies: array of EDUCATION-RELATED government bodies and institutions. ONLY include: school boards, boards of education, school districts, departments of education, education committees. DO NOT include: general government bodies like county commissioners or city councils unless they are acting in a specific education capacity. DO NOT include district numbers or subdivisions - only the main body name (e.g., "Talbot County Board of Education", not "Talbot County Board of Education District 5"). Avoid duplicates and variations of the same body.

RULES:
- Use title case when original is capitalized
- NEVER include 'Star-Democrat', 'Chesapeake Publishing Group', or 'Adams Publishing/APGMedia'
- Leave arrays empty [] if no education-related items exist
- State legislature = 'Maryland General Assembly'
- When in doubt, EXCLUDE the entity - only include if it's clearly education-related
- Return ONLY valid JSON with all original fields plus new fields
```

## 3. Maryland Counties List

From: `murphy/stardem_topic_entities/education_script_v1.py`

The 5 main counties covered:
```python
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
```

Note: The full script also included all 24 Maryland counties (Prince George's, Anne Arundel, Baltimore County, etc.) to catch stories that mentioned other regions.

## 5. Beatbook Generation Prompts

From: `murphy/stardem_draft/generate_comprehensive_beatbook.py`  
Model: `groq/openai/gpt-oss-120b`

### Top Three Issues Prompt

```python
f"""
You are writing the "Top Three Issues on the Education Beat" section for {county}, Maryland.

County Performance Data:
{county_data_section[:800]}

Recent Stories (with full content, summaries, and metadata):
{stories_content}

Metadata from Coverage:
- Key Initiatives: {entities['top_initiatives']}
- Key Events: {entities['top_events']}
- Key Organizations: {entities['top_organizations'][:8]}

Dataset date range: {date_range}

Write a "Top Three Issues on the Education Beat" section.

Requirements:
- Produce **exactly three issues**, each as an **H3 heading (###)**
- Under each heading, write **2-4 paragraphs** of narrative prose
- **Do NOT use bullets or lists**
- Ground each issue in both the story coverage and the performance data
- Cite specific stories by title to support your points
- Issues should be ongoing challenges or policy debates, not one-time events
- Focus on systemic problems: funding, achievement gaps, infrastructure, staffing, policy conflicts
- Write like a beat reporter briefing a colleague
"""
```

### Key Sources Prompt

```python
f"""
You are writing the "Key Sources to Know" section for {county}, Maryland.

County Leadership Data:
{county_data_section[:600]}

Coverage Insights:
- Key People: {entities['top_people']}
- Key Organizations: {entities['top_organizations']}
- Key Establishments: {entities['top_establishments']}

Recent Stories with Context:
{stories_with_context}

Write a "Key Sources to Know" section.

Requirements:
- Use **H4 headings (####)** to label source categories (e.g., "#### District Leadership", "#### School Principals")
- Under each heading, use **bulleted lists**
- Each bullet should identify:
  - A specific person, position, or office
  - What decisions/areas they influence
  - Which stories they appeared in (cite by title)
- Include roles from the county data (superintendent, board members) plus key figures from stories
- Keep bullets concise and factual
"""
```

### Documents Section Prompt

```python
f"""
You are creating a "Key Documents, Records & Websites" section for an education beat book covering five Maryland Eastern Shore counties: Talbot, Kent, Dorchester, Caroline, and Queen Anne's.

Metadata from Coverage:
- Key Initiatives: {all_entities['top_initiatives']}
- Key Organizations: {all_entities['top_organizations'][:10]}

Sample Stories (with summaries showing document references):
{sample_stories_with_content}

Write a consolidated "Key Documents, Records & Websites to Track" section.

Requirements:
- Use **H3 headings (###)** for document categories (e.g., "### Budget & Finance Records", "### Assessment & Accountability Data")
- Under each heading, use **bulleted lists**
- Each bullet should identify:
  - A specific document type or website
  - What information it provides (1 sentence)
  - Whether it's county-level or state-level
- Include: budgets, CIPs, board minutes, MCAP data, enrollment reports, staffing data, Blueprint plans
- Reference documents mentioned in the stories
- Organize logically by topic area
- Keep explanations concise
"""
```
