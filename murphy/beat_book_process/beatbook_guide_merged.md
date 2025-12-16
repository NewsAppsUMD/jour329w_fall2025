# How to Build a Beat Book: A Practical Guide from the Trenches

*What I learned building an interactive education beatbook through nine iterations, four months, and way too many Groq accounts*

**By Cat Murphy | December 16, 2025**

---

## What This Guide Is

I built an education beatbook for Maryland's Eastern Shore. Started with 200 Star-Democrat stories in November 2024, thinking I'd classify them and be done in a week. Four months later, I had an interactive dashboard with 175+ stories, 99 source contacts, 47 schools with full data, and a functional (if mediocre) chatbot.

The final version is good. Really good.

But I got there by doing almost everything wrong first.

This guide tells you what actually worked, grounded in the code I wrote and the mistakes I made. It's organized as a practical workflow, but includes the real scripts, models, and failures so you know what you're getting into.

---

## The Core Workflow

**Reality check:** Phases 2 and 3 run in parallel. You need external data before generation, and it informs entity extraction. Don't try to do this linearly.

**Time estimate:** ~100 hours over 4 months. Cost: $15 (mostly OpenAI for document summarization).

---

### Phase 1: Collection & Classification

#### Step 1: Pull stories broadly

I started with 200 stories from the Star-Democrat. They were a mess - news mixed with calendars mixed with sports briefs. I accepted the chaos initially and didn't try to filter yet.

**Lesson:** Over-collection is fine at this stage. You'll filter later.

#### Step 2: Topic classification through iteration

This is where I learned that LLMs are probabilistic chaos machines without constraints.

**classify_topics_1.py:**
- Model: `groq/meta-llama/llama-4-scout-17b-16e-instruct`
- Approach: 18 predefined topics with definitions like "Articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around..."
- **Result:** Classified all 200 stories as "Other"

Why? I had defined categories by what they were NOT. The LLM saw exclusions everywhere and gave up.

**classify_topics_2.py:**
- Model: `groq-kimi-k2`
- Change: Rewrote all definitions positively ("Articles that center around and primarily discuss...")
- Same 18 topics, just better definitions
- **Result:** 40-50% accuracy. Still wrong on editorials ("EDITORIAL: 10-cent paper bag fee" → "Environment"), calendars ("SPRING TRAINING GLANCE" → "Sports"), and "Today in History" articles ("Columns & Editorials")

Better, but not good enough.

**classify_topics_3.py:**
- Model: `groq/meta-llama/llama-4-maverick-17b-128e-instruct`
- Major restructuring: Added `content_type` and `secondary_topic` fields
- Included 4 examples directly in the prompt:

```python
Examples:
- "Robbins YMCA opening reading hub to tackle childhood illiteracy" 
  → "News", "Education", "Arts & Culture"
- "TV LISTINGS 7-19-24" 
  → "Miscellaneous", "Other", "None"
- "Don't compare Trump to Hitler" 
  → "Opinion", "Elections & Politics", "None"
```

**Result:** 
- Took 90 minutes (one story every 15-30 seconds)
- Content type: 144 News, 18 Opinion, 17 Miscellaneous, 9 Calendars, 5 Obituaries
- Primary topic: 57 Arts & Culture, 24 Public Safety, 19 Sports...
- I disagreed with maybe 10 out of 200

This was good enough. I stopped iterating.

**classify_topics_4.py:**
- Tried asking the LLM to generate its own topic names (no predefined list)
- Failed every time
- Gave up on this approach

**Key takeaways:**
- Never define categories by exclusion
- Adding structured fields (content_type, secondary_topic) improves accuracy dramatically
- Examples in prompts help
- Slower models sometimes = better results (90 min vs 5 min, but 95% vs 50% accuracy)
- Validate manually, but you don't need 100% - 95% is fine

#### Step 3: Filter to relevant subset

After classification, I filtered down to beat-worthy stories:
- News stories only (not calendars, obituaries, legal notices)
- Related to my five counties
- About boards of education, public officials, funding, policy

This eliminated 2/3 of entries, leaving 278 stories for the beatbook.

#### Step 4: Lock down your data schema early

Every schema change means re-running every extraction script. I learned this the hard way.

My final schema:
```json
{
  "id": "unique_id",
  "title": "Story headline",
  "content": "Full story text",
  "url": "https://...",
  "date": "YYYY-MM-DD",
  "author": "Reporter name",
  "content_type": "News",
  "primary_topic": "Education",
  "secondary_topic": "Budget",
  "counties": ["Talbot", "Kent"],
  "primary_county": "Talbot"
}
```

Do this once, then stick with it.

---

### Phase 2: External Data Collection

**Start this early. Run it parallel with entity extraction.**

My first beatbook drafts kept referencing things they couldn't explain:
- "Blueprint for Maryland's Future funding increased..."
- "MCAP scores declined..."
- "Student discipline rates rose..."

Stories mentioned these things but didn't provide full context. So I went scraping.

#### What data I got (and why it was painful)

**School discipline data:** Huge hassle. Got numbers by county, school, type, race, gender, disability, offense. Worth it.

**Teacher data:** Number of teachers per county, % increase/decrease, number of new teachers, % who are new. Microsoft Power BI interface wouldn't scrape properly, so I **screenshotted and OCR'd it.**

**MCAP scores:** Statewide data to show how Eastern Shore schools perform comparatively.

**Blueprint funding:** Couldn't get actual budget documents (they're disasters), so pulled summaries from local news network.

**Census data:** Population, poverty, median income, demographics. Relatively easy from ACS.

**School-level enrollment:** Eventually built JavaScript scrapers with Claude's help after Power BI defeated me.

This took FOREVER. Scrapers kept outputting duplicates or misinterpreting tables. Manual verification required.

#### The summary book strategy

Instead of hardcoding stats into generation prompts, I created two summary files:

**county_summary_book.json:**
```json
{
  "Talbot County": {
    "population": 37663,
    "median_income": 81667,
    "poverty_rate": 9.3,
    "total_enrollment": 4529,
    "per_pupil_spending": 19234,
    "num_schools": 8,
    "key_officials": [
      {
        "name": "Sharon Pepukayi",
        "title": "Superintendent",
        "org": "Talbot County Public Schools"
      }
    ]
  }
}
```

**school_summary_book.json:**
```json
{
  "Easton Elementary School": {
    "county": "Talbot County",
    "enrollment": 412,
    "mcap_ela_proficient": 45.2,
    "mcap_math_proficient": 38.7,
    "demographics": {
      "white": 62.3,
      "black": 18.4,
      "hispanic": 12.1
    }
  }
}
```

Then I passed these TO the LLM during generation.

#### Budget document strategy

For massive budget documents (we're talking 1000+ pages), I used ChatGPT to create comprehensive but succinct summary books:

Structure per county:
- Core fiscal table
- Enrollment & per-pupil spending
- Blueprint drivers  
- Capital outlook
- Emerging fiscal/policy issues
- Narrative summary

Plus cross-county comparison tables at the end.

I tried Gemini to compare results - ChatGPT was far and away better in terms of quality, structure, consistency, and relevance.

**This saves the LLM from processing 1000-page PDFs during generation.**

---

### Phase 3: Entity Extraction

**Run parallel with external data. Start after classification.**

I overloaded Copilot twice. Got rate-limited by Groq three times on my FIRST script. Had to switch models mid-extraction (after 55 stories) from `groq/openai/gpt-oss-120b` to a different one, which is why my results file is called `stardem_with_entries_2_ish.json`. Very scientific.

#### The ambitious first attempt

**stardem_entities_script_1.py:**
- Model: `groq/meta-llama/llama-4-scout-17b-16e-instruct`
- Seven new fields: content_type, people, locations, institutions, events, municipalities, county

I built a comprehensive Maryland county/municipality mapping - all 24 counties, hundreds of municipalities. Then I wrote post-processing functions:

```python
# Validate: only allow real municipalities
municipalities = [m for m in municipalities if m in all_municipalities]

# Derive county from municipalities
for muni in municipalities:
    county = municipality_to_county.get(muni)
    if county:
        counties.add(county)

# Remove municipalities/counties from locations field
locations = [l for l in locations if l not in all_municipalities]
```

When it worked, it was beautiful:
```json
{
  "people": ["Albert C. Jones Jr.", "Veronica Taylor"],
  "municipalities": ["Cambridge"],
  "county": ["Dorchester County"],
  "institutions": ["Groove City Black Heritage and Cultural Group Inc."]
}
```

But then I'd get locations like:
```json
"locations": ["Annapolis", "Arundel Olympic Swim Center (Annapolis)", 
"Rams Head Tavern (Annapolis)", "Island Pub (Stevensville)", 
"Rehoboth Ale House (Rehoboth Beach)", "Lefty's Alley & Eats (Lewes)"... ]
```

**Thirty-five locations. For one calendar listing.**

**The problem:** I was feeding it calendars and expecting news analysis. Garbage in, garbage out.

#### Narrowing to education

**education_script_v1.py:**
- Model: `groq/openai/gpt-oss-120b` (for first 55 stories), then switched models mid-run
- Focused on ONE beat: education
- Ultra-specific extraction prompt:

```python
"""
Extract these people and only these people:
- Superintendents (format: Name (Title, Organization))
- Board of Education members with specific titles
- Principals
- State officials directly involved in education policy

Do NOT extract:
- Parents quoted once
- Students
- The story author
"""
```

Split "organizations" into 5 categories:
- Events (one-time occurrences)
- Initiatives (programs/policies)
- Establishments (physical places: schools)
- Organizations (non-government entities)
- Bodies (government institutions)

Used `Counter()` to track entity frequency:
```python
from collections import Counter

people_counter = Counter()
for story in stories:
    for person in story.get('people', []):
        people_counter[person] += 1

# Most frequently mentioned:
# Sharon Pepukayi (Superintendent, Talbot County): 7 stories
# Emily Jackson (President, Talbot County Board): 7 stories
# Dr. Derek Simmons (Superintendent, Caroline County): 6 stories
```

#### Rate limiting reality

**Got rate-limited so many times I created six Groq accounts.**

Ran entity extraction on 779 education stories over 3 days. A few failed (syntax errors, content too long), bunch got duplicated. Ended up with 754 unique entries.

#### What worked, what didn't

**Worked:**
- Municipality list was worth every hour - every "Easton" formatted identically
- Organizational split into 5 categories captured nuance
- `Counter()` for frequency ranking found key sources

**Didn't work:**
- Regions field was hit or miss (extracted Delaware from "she served on a board there years ago")
- Locations field too broad for education (locations WERE the establishments/schools)
- Title format inconsistency: "Sharon Pepukayi (Superintendent of Talbot...)" vs "Sharon Pepukayi (Superintendent, Talbot...)" - one comma difference, infuriating
- False negatives everywhere with ultra-specific prompts

**Key lesson:** Ultra-specific prompts reduce false positives but create false negatives. Accept some manual cleanup.

---

### Phase 4: Beatbook Generation

I asked ChatGPT to write me a generation script based on the class example. Three versions later, I learned what works and what fails spectacularly.

#### First attempt: Everything at once

**generate_beatbook_v1.py:**
- Model: `groq/meta-llama/llama-4-maverick-17b-128e-instruct` (hit token limit, switched to `groq/openai/gpt-oss-120b`)
- Used entity metadata AND full story content
- County-by-county sections
- Outputs: Top 3 Issues, Key Sources, Key Documents
- **Result: 42 pages**

What worked:
- Data/Documents section was impressive (8-11 categories of records per county)
- Found documents I didn't know existed (Facility Master Plans, Superintendent Contracts)

What didn't:
- Sometimes no names: "Principal, Kent County High School" (Cool. What's their name?)
- Wes Moore appeared constantly (he's the governor, tangentially related, not a beat source)
- Hallucinated quotes (badly paraphrased or invented)
- Hallucinated links (tcps.org, uppershorewib.org, kent.k12.md.us) - though major state websites were correct
- Spelling errors: "Talton County" and "Talark County"
- No comprehension of time/chronology
- Tone problems: "proved pivotal," "could redefine Talbot County's educational trajectory"
- Too long

#### Second attempt: Metadata only

**generate_beatbook_v2.py:**
- Model: `groq/qwen/qwen3-32b`
- Change: Titles and metadata ONLY (no full story content)
- Stripped `<think>` tags from output
- **Result: 16 pages**

I expected this to bomb. Thought titles/metadata wouldn't be enough.

Better length. But repetitive and shallow. Every county's "pandemic recovery" section looked identical because it didn't have story details to differentiate. Same with Blueprint for Maryland's Future rollout.

Also focused on bizarre sources: "Julie Hickey – Coordinator of Food Services, Queen Anne's County Public Schools"

Sure, she appeared. But she's not a key beat source.

#### Third attempt: External data integration

**generate_beatbook_v3.py:**
- Model: `groq/openai/gpt-oss-120b`
- Added: County and school summary books
- Added: Date filtering (recent stories vs all-time)
- Passed structured data TO the LLM

This changed everything. The LLM wrote:

> "Despite Talbot County's median income of $81,667 suggesting resources to address the 9.3% poverty rate, MCAP math proficiency remains at 5.2% — below the state average of 15.3%."

Far more sophisticated than vague "declining scores."

#### What I learned about prompts

I gave it too many instructions:
```
exclude candidates from district leadership source lists
exclude star dem writers
get rid of regional education partners and media sections
use footnotes not title references
make SURE you are referencing the correct dates
include science in MCAP data
include state-level figures separately not in each county
do not include the governor except for bill signings
do not include "Neighboring District Superintendents"
do not include "Community & Service Organizations"
no "Law Enforcement & Public Safety"
no "State Education Agency"
```

...and 20 more rules.

**Result:** The LLM started ignoring rules and hallucinating to fill gaps.

It wrote: "Specific principal names were not provided in the source data..."

**I HAD PROVIDED PRINCIPAL NAMES.** They were in my summary book. It couldn't find them in the wall of instructions.

**Lesson:** Keep rules to 10 max. More = confusion.

#### The prompt structure that eventually worked

```python
prompt = f"""
You are writing a beat book for education reporters covering Maryland's Eastern Shore.

COUNTY DATA:
{county_summary_book}

SCHOOL DATA:
{school_summary_book}

STORIES ({len(stories)} total):
{story_summaries}

Generate:
1. Three key issues for the Eastern Shore overall (prevents repetition in county sections)
2. County-by-county section with recent coverage themes
3. Key sources with titles, orgs, areas of expertise
4. Key documents by category (not by county)

Rules:
- Integrate data naturally with specific figures
- Cite stories by ID number (easier to verify than titles)
- Use format: Name (Title, Organization) for all people
- Do NOT include quotes (too error-prone)
- Do NOT include story ideas or investigation suggestions
- Write narrative paragraphs for issues
- Use lists for sources and documents
"""
```

**Key principles:**
1. Pass story data + external data + metadata together
2. Be specific about format (saves editing later)
3. Limit the rules (10 max, not 30)
4. Don't ask for quotes (LLMs hallucinate them)
5. Use Story IDs for citations
6. Add statewide/regional overview to prevent county-section repetition

---

### Phase 5: Fact-Checking

I fact-checked my 40+ page draft cover to cover. Just the first chapter completely taught me what to trust and what to verify ruthlessly.

#### What was accurate

**Data I provided separately:** Near-perfect
- MCAP scores, demographics, enrollment from summary books
- Still spot-checked, but 99%+ accurate

**Data from story content:** 90-95% accurate
- One instance: cited 45% increase when article said 39%
- Dates and timelines often wrong (LLMs are terrible with chronology)

#### What was garbage

**Quotes and citations:** Fatal flaw

I don't think ANY direct quotes were entirely accurate. All were at least partially wrong.

**Favorite mistake:** Directly quoting paraphrases

Stories: "Superintendent Jane Doe emphasized that test scores are concerning."

LLM: `"Test scores are concerning," Superintendent Jane Doe said.`

Technically accurate sentiment. Not an actual quote.

Also: It preferred quoting LLM-generated summaries over actual articles.

Also: Just straight-up invented some quotes.

**Solution:** I pre-extracted quotes into a verified database. If you must include quotes in LLM-generated sections, verify every single one.

#### Tone and currency issues

Watch for:
- Overly lofty language ("proved pivotal," "could redefine")
- Outdated information presented as current
- Election results, vacancies, pending lawsuits, unpassed legislation
- Spelling errors in place names ("Talton County" vs "Talbot County")

#### Fact-checking workflow

1. Check first complete section thoroughly
2. If error rate <5%, spot-check others
3. If error rate >5%, check everything
4. Always verify anything a reporter will rely on

---

### Phase 6: Interface Building

I tried building narrative PDFs first. They worked, but weren't searchable or interactive.

So I built a website. Single-page HTML with embedded JavaScript. No backend, no database.

#### Architecture decisions

**Data embedding strategy:**
```javascript
// Lightweight index (loads on page load)
const storyIndex = [
    {id: 1, title: "...", date: "...", county: "...", topic: "..."}
];

// Full text (loads on demand)
const storyDetails = {
    1: {content: "full story text here..."}
};
```

**Essential features:**
- Search AND filters (don't make users choose)
- County color-coding (visual consistency)
- Result counts ("Showing 23 of 175 stories")
- Progressive disclosure (summary → details on click)

**What I built:**

1. **Schools dashboard:**
   - All 47 schools with enrollment, demographics, MCAP data
   - Filter by county
   - +/- indicators comparing to state averages
   - Sortable columns

2. **Source directory:**
   - 58 source cards (26 from quote extraction + district officials)
   - Searchable by name, subject, county
   - Dynamic loading (Copilot kept hardcoding them - took forever to fix)

3. **Story archive:**
   - Formatted like email inbox
   - Filter by county and year
   - Sort by publication date
   - Search full text
   - Click to open in side panel
   - Had to clean `\n` everywhere in JSON

4. **Meeting calendar:**
   - Claude did deep research and filled it in

5. **Simple chatbot:**
   - Pattern-matching navigation helper
   - Not AI, just keyword triggers
   - Helps users find what they need

#### What broke repeatedly

**File sizes too large:** Claude couldn't handle them. Repeatedly. Had to optimize by:
- Splitting data files
- Loading on demand vs all at once
- Compressing JSON

**Tabs wouldn't switch:** JavaScript conflicts. Copilot and ChatGPT both failed to fix it. Eventually debugged manually.

**Budget summaries integration:** Tried adding them, Claude stopped working entirely.

Eventually got it working through persistence and rage.

---

## Common Mistakes (That I Made)

### Mistake 1: Starting with generation
Don't write prompts before you have clean data. Get metadata right first.

I wasted days on prompts when my data was the problem.

### Mistake 2: Trusting first-pass extraction
Single-pass extraction produces chaos. Iterate through different approaches.

My first topic classification script classified everything as "Other."

### Mistake 3: Adding more instructions when output fails
If your 500-word prompt isn't working, a 1000-word prompt won't save it.

I gave the LLM 30+ rules. It started ignoring them and hallucinating.

### Mistake 4: Trying to build everything at once
I tried integrating education stories + local government stories + budgets + census + meeting minutes simultaneously.

Everything broke. Local government was too sprawling.

### Mistake 5: Assuming LLMs will "figure it out"
They won't. They need structure, constraints, examples, and verification.

The chatbot is pattern-matching, not AI. Manage expectations.

### Mistake 6: Defining categories by exclusion
"All stories except X, Y, Z" fails spectacularly.

Use positive definitions: "Stories that focus on..."

### Mistake 7: Ignoring rate limits
Plan for them. I created 6 Groq accounts and still got rate-limited.

### Mistake 8: Not fact-checking early
Waiting until the end to discover quote hallucinations wastes time.

Check a sample early. Adjust approach before generating everything.

### Mistake 9: Not including statewide/regional overview
For multi-jurisdiction beats, add an overview section for issues affecting all areas.

Otherwise you'll repeat the same thing five times with minor variations.

---

## When Beatbooks Are Most Valuable

**Local journalism:** When you don't have a reporter or editor who's been covering the area for generations. Beatbooks become essential reference.

**College newspapers:** Student journalists graduate and subject matter expertise disappears. Beatbooks preserve institutional knowledge.

**New reporters:** Getting up to speed on complex beats without months-long learning curve.

**Investigative projects:** Having comprehensive source lists and historical context at your fingertips.

**Not as valuable:** Large metro papers where reporters already have deep beat knowledge and extensive contacts.

---

## The Non-Negotiables

### 1. Good metadata is the foundation
You cannot build a useful beatbook without comprehensive, consistent, structured metadata.

Spend 60% of your time on classification and extraction.

### 2. External data transforms quality
Stories reference things they don't explain. Go get the actual data.

Create summary books before generation.

### 3. LLMs hallucinate quotes
Solutions:
- Pre-extract quotes into verified database
- Don't include quotes in LLM-generated sections
- If you must, verify every single one

### 4. Iterative refinement required
My first script classified everything as "Other." My third script got 95% accuracy.

Single-pass = chaos. Improvement emerges through iteration.

### 5. Narrow scope before scaling
One beat. One county. One type of story. Then expand.

I tried to do local government (everything) and it broke.

### 6. Manual validation is essential
Always check samples. Expect 5-15% error rate. Fix it.

---

## Tools & Technical Stack

**Python (3.9+)** for all data processing

**LLM Access:**
- `llm` CLI tool (https://github.com/simonw/llm)
- Groq API (fast, free tier, WILL hit rate limits)
- Anthropic API (Claude, paid, good quality)
- OpenAI API (ChatGPT, paid, best for document summarization)

**Models I actually used:**
- Topic classification: `groq/meta-llama/llama-4-maverick-17b-128e-instruct`
- Entity extraction: `groq/openai/gpt-oss-120b`
- Beatbook generation: `groq/openai/gpt-oss-120b`
- Document summarization: ChatGPT (GPT-4)

**Scrapers:**
- Python: BeautifulSoup, requests
- JavaScript: Puppeteer (for Microsoft Power BI interfaces that hate you)
- OCR: When everything else fails

**Data Processing:**
- JSON for everything
- `Counter()` from collections for frequency ranking
- Datasette for exploration (optional, kept crashing for me)

**Website:**
- Single-page HTML with embedded JavaScript
- Chart.js for visualizations
- GitHub Pages for hosting (free)

**Version Control:**
- Git (use from day one)
- Don't use folders as versions (I did this, it's embarrassing)

---

## Time & Cost Breakdown

**Time invested:** ~100 hours over 4 months
- Data collection: 20 hours
- External data scraping: 30 hours (parallel with entity extraction)
- Entity extraction: 25 hours (parallel with external data)
- Generation iteration: 15 hours
- Website building: 10 hours

**Money spent:**
- Groq: $0 (free tier, but created 6 accounts)
- Claude: $0 (free tier with rate limits)
- OpenAI: ~$15
- **Total: $15**

**Ongoing maintenance:**
- ~3 hours quarterly for updates

---

## What Success Looks Like

**Usage signals:**
- Reporters visit weekly
- Average session >5 minutes
- Return visits same day (coming back while writing)

**Qualitative signals:**
- Reporters send follow-up questions
- Stories cite specific beatbook figures
- Other reporters request access
- Editors reference it in assignments

**Expected ROI:**
- Break-even: 6 months
- Saves ~50 hours/quarter after that
- Plus intangibles: better stories, faster turnaround, expertise reputation

---

## Beat-Specific Guidance

### Education (What I built)
- **Stories:** Board meetings, budget battles, test scores, superintendent changes
- **Entities:** Superintendents, board members, principals, schools, districts
- **External data:** Test scores (MCAP), enrollment, demographics, budgets, teacher counts, graduation rates, discipline data
- **Key questions:** What are scores? Who's the superintendent? What's the budget? How many students?
- **Works well because:** Structured (school districts, boards) with measurable outcomes

### Courts
- **Stories:** Major verdicts, sentencing, judicial appointments, precedent-setting cases
- **Entities:** Judges, attorneys, defendants, law firms, courthouses
- **External data:** Case volumes, disposition rates, sentencing patterns, docket statistics
- **Key questions:** Which judge? What's typical sentence? Who's the defense attorney?

### Local Government
- **Stories:** Budget votes, zoning decisions, council meetings, elections
- **Entities:** Council members, mayors, town managers, departments
- **External data:** Budgets, meeting minutes, voting records, census demographics
- **Key questions:** Who holds power? What's the budget? How do they vote?
- **Warning:** Too sprawling. Consider splitting into sub-beats (Budget, Zoning, Elections)

### Housing
- **Stories:** Evictions, development approvals, tenant advocacy, code violations
- **Entities:** Landlords, tenant organizations, housing authorities, developers
- **External data:** Vacancy rates, median rents, eviction rates, violation records
- **Key questions:** Who owns this? What's the rent? Eviction rate?

### Environment
- **Stories:** Pollution incidents, conservation efforts, regulatory changes
- **Entities:** Agencies, advocacy groups, officials, regulated entities
- **External data:** Water quality, pollution levels, permit violations, cleanup progress
- **Key questions:** What's polluted? Who regulates? What's improving/declining?

---

## Final Principles

**Start small.** One beat. One county. One type of story. I tried to do everything and it broke.

**Expect failure.** My first script classified everything as "Other." That's normal.

**Iterate relentlessly.** Four classification scripts. Three entity extraction scripts. Multiple beatbook generation versions. Each one taught me something.

**Fact-check ruthlessly.** LLMs make mistakes. Verify what matters.

**Ship when good enough.** Perfect is the enemy of useful. My beatbook has flaws. It's still valuable.

**Learn from real use.** Get it in front of users. Watch what they actually do. Adjust.

---

*For the full narrative journey including all the failures and disasters, see `beatbook_journey.md`*
