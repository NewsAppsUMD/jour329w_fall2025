# How to Build a Beat Book
## What I Actually Learned Building (and Breaking) an Interactive Beatbook Over Four Months

*A brutally honest account of topics, entities, drafts, disasters, and eventually something that actually works*

---

## Introduction: This Guide Is Different

Most guides tell you what worked. This one tells you what broke, why it broke, and what I learned from breaking it.

I built an education beatbook for five Maryland Eastern Shore counties. I started with 200 Star-Democrat stories in November, thinking I'd classify them by topic and be done in a week. Four months later, I had built (and discarded) eight different versions, burned through six Groq accounts, maxed out Claude's rate limits twice, spent actual money on API calls, and ended up with an interactive dashboard containing 175+ stories, 99 source contacts, school-level data for 47 schools, and a (mediocre but functional) chatbot.

The final version is good. Really good. But I got there by doing almost everything wrong first.

If you're building a beatbook for education, local government, courts, housing, or any complex beat, this guide will save you from my mistakes. Or at least help you make different ones.

---

## Part 1: Iteration One — Topics (Or: Why "Other" Is a Trap)

**November 1. The assignment: classify 200 stories by topic.**

I started confident. I created a CSV with 13 topics and detailed descriptions. Things like:

```
"Local Government","News articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss the members and actions of a local government..."
```

My last topic was "Other" — defined as "obituaries, legal notices, calendars, columns, editorials and any articles that do not otherwise fall under a defined topic."

**The LLM classified all 200 stories as "Other."**

Every. Single. One.

### What I Learned: Be Absurdly Specific, But Not With Negatives

The problem was defining a category by what it's NOT. The LLM saw my list of exclusions and thought, "Oh, these must all be excluded things."

I rewrote the prompt to provide positive definitions only. No more "excluding X, Y, Z" language. Instead: "Articles that center around and primarily discuss..."

I also gave the LLM examples — not just definitions, but actual sample classifications.

**Second run: Still not great.** I got 40+ variations of what should have been the same topic. "Test Results," "MCAP Scores," "Assessment," "Student Performance," "Achievement Data" — all for test score stories.

### The Multi-Pass Strategy (Born From Necessity)

This is where I discovered the most important lesson: **single-pass LLM classification will fail.**

LLMs are probabilistic. Without constraints, you get chaos.

Here's what actually worked:

**Pass 1: Exhaustive Extraction**  
Let it run wild. See what categories emerge naturally. I got 40 variations. That's fine. I needed to see the language actually used.

**Pass 2: Guided Standardization**  
I showed the LLM the topics that already existed:

```python
prompt = f"""
Previously used topics: Budget, Test Scores, Enrollment, Infrastructure, 
Board Actions, Superintendent Changes, Achievement Gaps

Use an existing topic if it fits. Only create new if genuinely different.
"""
```

This reduced 40 variations to 12 stable categories.

**Pass 3: Manual Consolidation**  
I merged near-duplicates myself. "Test Results" and "MCAP Scores" became "Test Scores."

**Pass 4: Human Validation**  
I manually checked 20 stories per category. Found ~15 misclassifications and fixed them.

**Lessons from Topics:**
- Never define a category by exclusion
- Expect chaos on Pass 1; embrace it
- Force consistency through showing prior results
- Always manually validate a sample

---

## Part 2: Iteration Two — Entities (Or: When Specificity Backfires)

**November 5. The assignment: extract people, places, and organizations.**

I got rate-limited by Groq three times and overloaded Copilot twice on my FIRST script. Welcome to entities.

I decided to be comprehensive. Seven new fields:
- `content_type` (News, Calendar, Sports, etc.)
- `people`
- `locations` 
- `institutions`
- `events`
- `municipalities`
- `county`

I was proud of this. Especially the municipalities field — I spent hours building a comprehensive list of every town in all five counties the Star-Dem covers, plus all 19 other Maryland counties just in case stories mentioned them.

**It rate-limited me after 55 stories.**

### What I Got: A Beautiful Mess

When it worked, it worked beautifully:

```json
{
    "people": ["Albert C. Jones Jr.", "Veronica Taylor"],
    "sources": ["politicians", "community leaders"],
    "municipalities": ["Cambridge"],
    "county": ["Dorchester County"],
    "institutions": ["Groove City Black Heritage and Cultural Group Inc."]
}
```

But then I'd get locations like this:

```json
"locations": ["Annapolis", "Arundel Olympic Swim Center (Annapolis)", 
"Rams Head Tavern (Annapolis)", "Island Pub (Stevensville)", 
"Rehoboth Ale House On the Mile (Rehoboth Beach)", "Lefty's Alley & Eats (Lewes)", 
"Market Street Public House (Denton)", "Cult Classic Brewing (Stevensville)", 
"USA Dance Eastern Shore (Easton)", "YMCA Washington (Easton)", 
"Nanticoke Sportsmen's Club (Seaford)", "Severna Park", 
"Jones Station Rd (Severna Park)", "25 Jones Station Rd (Severna Park)", 
"Buckingham Elementary School (Berlin)"]
```

Thirty-five locations. For one calendar listing.

### What I Learned: Garbage In, Garbage Out (Even With Good Prompts)

The Star-Dem data was organized terribly. News mixed with calendars mixed with sports briefs. The LLM couldn't distinguish what mattered because **I** hadn't distinguished what mattered.

Also: asking for "locations" in a beat where schools ARE the locations is circular.

**Key Insight:** The issue wasn't the prompt. It was that I was feeding it calendars and expecting news analysis.

---

## Part 3: Iteration Three — Topic + Entities (Or: The Importance of Narrowing Scope)

**November 10. I chose education as my focus.**

I could have done local government — it had 1,324 stories. But local government is sprawling. Education had 779 stories (after merging primary + secondary topic classifications), and it felt more manageable.

More importantly: **I cared about education.** When you're spending weeks on entity extraction, work on something you actually want to understand.

### The Ultra-Specific Prompt Strategy

Because I was focusing on ONE topic, I could be incredibly specific about what to extract:

```python
"""
Extract these people and only these people:
- Superintendents
- Board of Education members (with specific titles: President, Vice President, Member)
- Principals
- State officials directly involved in education policy
- MSDE officials

Do NOT extract:
- Parents quoted once
- Students
- The story author
- Generic "officials"
"""
```

This worked far better than my generic "important people" approach.

### What I Got Right

**Consistent county/municipality extraction:** By providing that absurdly long list of Maryland towns, it nailed geography. Every "Easton" was formatted identically. Every "Talbot County" was consistent.

**Organizational split:** I broke "organizations" into five categories:
- Key events
- Key initiatives  
- Key establishments (physical places)
- Key organizations (non-government)
- Key bodies (government institutions)

This gave me: "Blueprint for Maryland's Future" (initiative), "Empowerment Academy" (establishment), "Maryland Association of Secondary School Principals" (organization), "Talbot County Board of Education" (body).

### What I Got Wrong

**Title format inconsistency:**  
Sometimes: `"Sharon Pepukayi (Superintendent of Talbot County Public Schools)"`  
Other times: `"Sharon Pepukayi (Superintendent, Talbot County Public Schools)"`

One comma. Same person. Different format. Infuriating.

**Inference failures:**  
Someone called "Board Vice President" didn't get extracted because "education" wasn't explicit in the title, even though I'd extracted this same person in other stories where they were called "Vice President, Board of Education."

**False negatives everywhere:** The ultra-specific prompt excluded people whose relationship to education was implied rather than stated.

### Patterns That Emerged

Most frequently mentioned:
- Sharon Pepukayi, Superintendent, Talbot County (7 stories)
- Emily Jackson, President, Talbot County Board of Education (7 stories)
- Dr. Derek Simmons, Superintendent, Caroline County (6 stories)

Counties covered:
- Talbot County (111 stories)
- Caroline County (54 stories)
- Dorchester County (41 stories)

The consistency was reassuring — it meant the extraction was working reliably across stories.

**Lessons from Entities:**
- Narrow your scope before extraction (one beat, not all beats)
- Be specific about format: "Use format: Name (Title, Organization)"
- Build lookup tables for standardization
- Accept that ultra-specific prompts create false negatives
- Some manual cleanup is inevitable

---

## Part 4: Iteration Four — Choice & First Draft (Or: When More Data ≠ Better Output)

**November 12. I merged everything and ran it all.**

I pulled education stories from other topic files (local government, health, public safety) where education appeared as a secondary topic. Set confidence thresholds: >0.8 for primary education stories, >0.65 for secondary.

Ended up with 779 stories. Re-ran entity extraction on all of them.

**Got rate-limited so many times I created six Groq accounts.**

After removing duplicates and failures: 754 unique entries with full metadata.

Then I wrote a script to filter down to beat book-worthy stories. I defined "relevant" as:
- News stories (not calendars, obituaries, legal notices)
- Related to the five covered counties
- About boards of education, public officials, funding, policy, etc.

This eliminated 2/3 of entries. Left me with 278 stories.

### My First Beatbook Generation Attempt

I gave ChatGPT my metadata schema and asked it to write a beat book generation script based on the example you provided.

The prompt said:
- Use entity metadata AND full story content
- Generate county-by-county sections
- Create three main outputs: Top 3 Issues, Key Sources, Key Documents
- Write in narrative prose (no bullets)
- Make it "feel like a newsroom beat memo"

**It generated 42 pages.**

### What Worked

**Data/Documents section:** Really impressive. 8-11 categories of records per county. Some I didn't even know existed:
- MSDE Report Card Data (school-level)
- Board of Education Meeting Minutes  
- Superintendent Contracts
- Facility Master Plans
- Annual Budget Books

The LLM was better at finding documents than I was.

**Source sections (when it wasn't hallucinating):**

```md
**Richard Barton – Board President**  
Sets board agenda, presides over meetings, champions fiscal stewardship.  
*Reporter hook:* Comments on board approvals, textbook adoption, calendar changes.
```

When it looked like this, I liked it.

### What Didn't Work

**Sometimes it just... didn't include names:**

```md
**Principal, Kent County High School**  
Oversees secondary curriculum, CTE programs, facility needs.
```

Cool. What's their name?

**Wes Moore appeared constantly.** He's the governor. He's tangentially related to education. He's not a beat source.

**Hallucinations:** Facts were mostly accurate, but quotes were invented or badly paraphrased.

**Length:** 42 pages was too long for what should have been a reference document.

### Draft Two: The Overcorrection

I asked Copilot to:
- Simplify and shorten (max 3 paragraphs per issue)
- Remove "why this matters" sections
- Use titles and metadata ONLY (no full story content)
- Use a different model

**It generated 16 pages.**

Better length. But now it was repetitive and shallow. Every county's "pandemic recovery" section looked identical because it didn't have story details to differentiate them.

It also focused on bizarre sources:

```md
**Julie Hickey** – Coordinator of Food Services, Queen Anne's County Public Schools
```

Sure, she appeared in stories. But she's not a key education beat source.

### What I Learned About Generation

**Story content matters.** Metadata alone isn't enough for nuanced analysis.

**But full content without constraints = bloat.** The 42-page version included way too much.

**The LLM needs data that ISN'T in stories.** Test scores, budgets, demographics. Stories reference these things but don't explain them. Go get the actual data.

**Lessons from First Drafts:**
- Metadata-only = shallow and repetitive
- Full content without limits = bloated
- You need external data to contextualize stories
- Length is a design choice, not an accident
- LLMs will hallucinate quotes unless constrained

---

## Part 5: Iteration Five — Draft V2 (Or: Data Changes Everything)

**November 22. I went and got the actual data.**

My first drafts kept referencing things they couldn't explain:
- "Blueprint for Maryland's Future funding increased..."
- "MCAP scores declined..."
- "Student discipline rates rose..."

Stories mentioned these things but didn't provide full context. So I went scraping.

### What I Scraped (And Why It Was Painful)

**School discipline data:** Huge hassle. Got numbers by county, school, type, race, gender, disability, and offense. Worth it.

**Teacher data:** Number of teachers per county, % increase/decrease from prior year, number of new teachers, % of all teachers who are new. Microsoft Power BI interface wouldn't scrape properly, so I screenshotted and OCR'd it.

**MCAP scores:** Statewide data to show how Eastern Shore schools perform comparatively.

**Blueprint funding:** Had to pull summaries from local news network since actual budget documents were disasters.

**Census data:** Already had this (population, poverty, median income, demographics).

This took FOREVER. Scrapers kept outputting duplicates or misinterpreting tables. Manual verification required.

### The County Summary Book Strategy

Instead of hardcoding stats into my generation prompts, I created two summary files:

**`county_summary_book.json`:** County- and district-level data
- Board members with titles
- Superintendents and key officials  
- Demographics and enrollment
- MCAP scores
- Teacher counts
- Budget info

**`school_summary_book.json`:** School-level data (47 schools)
- Individual MCAP scores
- Suspension data
- Enrollment by race/gender
- Free/Reduced Meals rates

Then I passed these TO the LLM during generation:

```python
prompt = f"""
You are writing a beat book for education reporters.

COUNTY DATA:
{county_summary_book}

SCHOOL DATA:
{school_summary_book}

STORIES:
{story_texts}

Integrate the data naturally. Reference specific figures.
Always cite which stories support your claims.
"""
```

### What Changed

The LLM wrote things like:

> "Despite Talbot County's median income of $81,667 suggesting resources to address the 9.3% poverty rate, MCAP math proficiency remains at 5.2% — below the state average of 15.3%."

Far more sophisticated than my first draft's vague references to "declining scores."

### What Still Sucked

**I gave it too many instructions.** My prompt adjustments:

```
exclude candidates from district leadership source lists
exclude star dem writers
get rid of regional education partners and media sections
use footnotes not title references
make SURE you are referencing the correct dates
include science in MCAP data
include state-level figures separately not in each county
do not include the governor except for bill signings
```

...and 10 more rules.

**Result:** The LLM started ignoring rules and hallucinating to fill gaps.

It wrote: "Specific principal names were not provided in the source data; please refer to the Kent County Public Schools website..."

I HAD PROVIDED PRINCIPAL NAMES. They were in my county summary book. It just couldn't find them in the wall of instructions.

**Formatting degraded.** Instead of lists, it gave me semicolon-separated strings.

### I Switched Models

Tried `groq/meta-llama/llama-4-maverick-17b-128e-instruct` instead of GPT.

Better organization and citations. Slightly more reasonable length. But still not great.

**Key Realization:** I was still missing enrollment broken down by race and special populations. Needed this for context on suspension rates.

**Lessons from Draft V2:**
- External data makes narratives 10x better
- Create summary books BEFORE generation
- Too many prompt rules = LLM confusion
- Model choice matters for different tasks
- You'll always realize you're missing data

---

## Part 6: Iteration Six — Draft V3 & The Local Government Disaster

**November 29. I tried to do local government. It broke everything.**

I thought: if education worked, local government will too. Just... more of it.

I processed 748 local government stories, whittled down to the ~170 most relevant and timely.

I went out and got MORE data:
- Budget analysis for each county
- Census data (already had this)
- County and municipal officials
- Election data  
- **Recent council meeting minutes for EVERY county**

I asked Claude to generate enormous summary documents analyzing each county's budget and meeting minutes. I downloaded all of this **by hand**.

I manually fed it names and titles of government officials when town websites had Cloudflare systems that blocked my scrapers.

**It became too much.**

### What Went Wrong

**Information overload.** I had so much data the LLM couldn't process it meaningfully.

**Organizing into folders didn't help.** The prompts couldn't handle "look at these 15 different file types and synthesize them."

**Every draft sucked.** Some worse than others. I generated five versions. Hated all of them.

**Hallucinations increased.** Example from v2:

> "Municipal leaders, notably Federalsburg's mayor, act as advocates for town-level concerns such as tax differentials and service parity."

No shit, really? This is filler garbage.

**Length was WRONG.** I expected 60+ pages given the data volume. Got 25 pages. Half-empty tables. Full tables that just repeated the paragraph above them.

**Generation was suspiciously fast.** Education beatbook took appropriate time to generate. Local government ones spit out 25 pages in 12 seconds.

The LLM wasn't "trying." It was just filling space.

### The AI Intervention Chain

Frustrated, I tried a new strategy: **LLM collaboration.**

1. Fed terrible output to ChatGPT. It said:

> "The beatbook is pretty strong structurally but nowhere near the standard you want (both for your own reporting and for Howard Center/NYT-style clarity)."

(Thanks, OpenAI memory feature from when I practiced resume writing with you two weeks ago.)

ChatGPT was brutal: "this reads like you're tripping on acid" (paraphrasing).

2. ChatGPT gave me a new script.

3. Copilot had to fix it because it had 25 issues.

4. Ran the script. Gave output to **Claude**.

Claude said:

> "Your prompt is burying the model under too much instruction and not enough clear signal about what matters."

Also:

> "Use a better model - groq/openai/gpt-oss-120b is not ideal for this. Try claude-3-5-sonnet-20241022 via the Anthropic API directly."

(Nice "please don't use our competitor's model" touch, Claude.)

5. Claude wrote a script. Produced **82 pages.** Considerably better quality, but still redundant and weird.

6. Gave feedback to Claude. Rewrote script.

**102 pages.** 12-point font.

And it included gems like this:

```
1. Trace the $1.2‑million‑pluscostofthe287(g)ICE‑enforcementmodelmentionedonSeptember 30 2025;theFY 2026budgetshowsnoallocation,suggestingahiddenfundingsource.2. ComparethevoteontheAugust 28 2025sewer‑capacitymoratorium(reportedinStory 8)withtheabsenceofarecordedroll‑call;identifyanycommissionerswhorepeatedlyabstainedwithoutexplanation.3. ExaminetheRoyal FarmsdevelopmentapprovalprocessonApril...
```

Yeah. Word salad with no spaces.

### What I Learned From Failure

**More data ≠ better output.** There's a sweet spot. I exceeded it dramatically.

**Local government is too sprawling.** Unlike education (which focuses on schools, boards, test scores), local government covers EVERYTHING. Budget, zoning, public works, elections, crime, development, infrastructure...

Each subtopic needed its own beatbook. I was trying to do 7 beatbooks in one.

**I kept trying to add story ideas.** Every LLM wanted to suggest investigations and FOIA requests. I kept telling them: this is a GUIDE, not a pitch document. But when I removed that, they invented new unnecessary sections.

**Lessons from the Disaster:**
- Some beats are too broad for one beatbook
- There IS such a thing as too much context
- Fast generation = shallow analysis
- Sometimes you need to walk away and start over

---

## Part 7: Iteration Seven — Different (Or: Building the Website)

**December 6. I pivoted to building a browser-based interface.**

Narrative beatbooks are fine. But what if reporters could INTERACT with the data?

### What I Built (Early Versions)

Tabs:
- Data Dashboard (suspension data, MCAP visualizations)
- Five Key Issues
- Sources
- Six county filters (five counties + "all counties")

This worked great... at first.

Then I tried adding more. Created budget summaries. Asked Claude to integrate them.

**Claude couldn't handle the file sizes.** It literally stopped working. Repeatedly.

Tried ChatGPT and Copilot to fix the HTML. Neither could.

Everything broke. Tabs wouldn't switch. Data wouldn't load. HTML files were too large.

### The Breakthroughs

While fighting with the website, I tried parallel experiments:

**1. Asked ChatGPT to create a comprehensive budget databook**

Compressed 10 massive budget documents into one structured file.

Sections per county:
- Core fiscal table
- Enrollment & per-pupil spending
- Blueprint drivers
- Capital outlook
- Emerging fiscal/policy issues
- Narrative summary

Plus:
- Cross-county comparison tables
- Regional takeaways

This was one of the best summary books I made. ChatGPT crushed it.

**2. Asked Copilot to extract all quotes and generate source profiles**

Problem: Generated beatbooks kept hallucinating quotes. Badly paraphrased, nonsensical, or fully invented.

Solution: Pull quotes into their own file FIRST. Then generate profiles using ONLY those verified quotes.

Script extracted quotes and generated 26 profiles — one for every key player quoted 5+ times.

**3. Went back to Claude and made a narrative beatbook (again)**

For some reason, the narrative beatbooks I generated THIS time were fire.

Random Groq model: pretty good.

Switched to `gpt-oss-120b`: INSANE quality.

I think it was the budget data. But the dramatic improvement floored me — and pissed me off. NOW you work?

**4. One more try at the website**

I had very little hope. Everything was too large. Claude kept breaking.

**But it worked.**

After many tweaks:
- Five key issues with "critical findings" summaries, paragraphs, and data tables
- County-level narrative breakdowns with key statistics (enrollment, budget, state funding)
- **Interactive schools dashboard:** All 47 schools. Filter by county. Click to see enrollment, demographics, student groups (disabilities, FARMS, multilingual learners, economically disadvantaged).
- **Searchable sources table:** 58 source cards with titles, organizations, topics they're quoted on, number of quotes.

**Lessons from Different:**
- Sometimes you need to abandon an approach entirely
- Build components separately, then integrate
- Source verification requires pre-extraction
- The right model + right data = dramatic quality jumps
- Persistence eventually pays off (or you hit your breaking point)

---

## Part 8: Iteration Eight — Nearly Final (Or: Fact-Checking Reveals Everything)

**December 11. I fact-checked my draft. Cover to cover.**

My draft was 40+ pages. Each county chapter had the same structure. I fact-checked the first chapter completely.

### What Was Accurate

**Data I provided separately:** Near-perfect. MCAP scores, demographic info, enrollment figures — all correct when I'd given the LLM clean summary books.

**Data from story content:** Good, but not perfect. One instance: cited 45% increase in student homelessness when the article clearly said 39%.

### What Was Garbage

**Quotes and citations:** This was the fatal flaw.

I don't think ANY of the "direct quotes" were entirely accurate. All were at least partially wrong.

**Favorite LLM mistake:** Directly quoting paraphrases.

Stories structured like: "Superintendent Jane Doe emphasized that test scores are concerning."

LLM quoted: `"Test scores are concerning," Superintendent Jane Doe said.`

Technically accurate sentiment. Not an actual quote.

**Also:** It preferred quoting LLM-generated summaries over actual articles.

**And:** It just straight-up invented some quotes.

**Citations:** Kept referencing stories using "footnotes" but never defined the footnotes. When it tried to reference headlines, it would misstate them or quote parts while paraphrasing the rest.

### The Structural Problem

**Too repetitive.** County-by-county structure meant saying the same thing five times with minor variations.

Better structure:
- Three key issues for Eastern Shore education overall
- Then county-by-county section with recent coverage themes specific to each

### Ideas for Improvement

**Pull quotes into separate document** organized by topic. Assign full names to quotes. Give LLM a concrete database of who-said-what.

**Prompt to cite by row ID:** "Story #25" instead of trying to reference headlines. Then build a Datasette so reporters can look up Story #25.

**Add school-level enrollment data** with census tract data. Would allow better analysis of scores vs. demographics.

(I tried scraping this from MSDE but Microsoft Power BI is terrible. Eventually built JavaScript scrapers with Claude's help.)

**Lessons from Fact-Checking:**
- LLMs are great with structured data you provide
- LLMs are terrible with quotes
- Pre-extract quotes if accuracy matters
- Verify everything a human will rely on
- Structure determines repetition

---

## Part 9: Iteration Nine — Final (Or: The One That Actually Works)

**December 15. This is it.**

I was pleased with Nearly Final structurally. Didn't want to overhaul anything.

Just build out specific features and improve navigation.

### What I Built

**1. Reorganized schools page**

- Added MCAP data that was missing before
- Added +/- indicators comparing to state averages
- Changed dropdowns to popups (less clunky)
- Added county and school-level filters
- Added sortable columns: by name (A-Z), enrollment, FARMS rate, economically disadvantaged %, race, ELA proficiency, math proficiency (both high-to-low and low-to-high)

**2. Fixed source directory**

Originally tried subject and county filters. They didn't work — contacts were there but not searchable.

Asked Claude to do deep research and get me more contacts/documents. Had Copilot integrate them.

Copilot kept hardcoding instead of loading dynamically. Eventually fixed it.

**3. Story archive (the ambitious one)**

Formatted like an email inbox:
- Filter by county and year
- Sort by publication date
- Search full text
- Click article to open in side panel

Stories were hardcoded initially (couldn't get JSON loading to work). Eventually got dynamic loading working.

Had to remove some irrelevant stories (board meeting overviews, newsletter intros).

Biggest challenge: formatting. JSON had `\n` everywhere and extraneous metadata. Cleaned it up.

**Future goal:** Sort by metadata topics and mentioned people. Not there yet.

**4. Meeting calendar**

Claude did deep research and filled it in. Moved it to county profiles page. Easy addition.

**5. Local impact sections**

Added clickable tabs showing county-specific implications for each major issue.

Went back and forth on language/formatting. Eventually worked seamlessly.

**6. More demographic data**

Required more scraping (graduation rates, additional breakdowns). Already had scraper templates. Not too difficult.

**7. The chatbot (frustrating)**

Started okay with Claude in-browser. Tried to improve it. Lost all functionality.

Tried integrating Groq. Disaster.

Ended up with mediocre chatbot. Want better one. Need more time.

### What I Didn't Get To

**Document repository:** Asked Copilot to add it to sources. Never happened. Ran out of time.

### What I'm Proud Of

**Navigability:** Organization, structure, user experience.

**Data integration:** Everything connects. Stories → sources → schools → counties.

**Interactivity:** Can actually explore, not just read.

### What Needs Work

**JavaScript cleanup:** Inline CSS/JS needs refactoring.

**Chatbot:** Needs to actually be good.

**More features:** Ideas for spring.

**Lessons from Final:**
- Feature creep is real (manage it)
- Sometimes "good enough" ships
- Iterative improvement beats perfection
- User testing would have helped (didn't do it)
- Interactive > static for beat books

---

## Part 10: What Actually Matters (Lessons From Nine Iterations)

### The Non-Negotiables

**1. Good metadata is the foundation**

You cannot build a useful beatbook without comprehensive, consistent, structured metadata. Period.

This means:
- Spending 60% of your time on classification and extraction
- Multi-pass processing to force consistency  
- Manual validation of samples
- Standardization rules for names, titles, locations

The story text matters, but metadata makes it searchable, filterable, and analyzable.

**2. External data transforms quality**

Stories reference things they don't explain. Go get the actual data:
- Demographics
- Budgets  
- Test scores (education)
- Case outcomes (courts)
- Eviction rates (housing)

Create summary books BEFORE generation. Let the LLM reference concrete figures.

**3. LLMs hallucinate quotes**

They don't mean to. But they do. Constantly.

Solutions:
- Pre-extract quotes into verified database
- Generate profiles using ONLY verified quotes
- Never trust an LLM quote without checking
- Consider not using quotes in LLM-generated sections

**4. Prompts have limits**

You cannot prompt your way out of structural problems.

- If your data is disorganized, prompts won't fix it
- If you're feeding 1000 pages of context, prompts won't process it meaningfully
- If your beat is too broad, prompts won't focus it

Fix the problem, don't prompt around it.

**5. Model choice matters**

Different models are good at different things.

I used:
- `groq/meta-llama/llama-4-maverick-17b-128e-instruct` for structured extraction
- `groq/openai/gpt-oss-120b` for narrative generation
- Claude (via API) for complex synthesis and web interface building
- ChatGPT for document summarization

Test multiple models. Use the right tool for each task.

### The Workflow That Works

**Phase 1: Collection & Classification (Weeks 1-2)**

1. Pull stories broadly (accept over-collection)
2. Classify by topic (multi-pass)
3. Filter to relevant subset
4. Lock down data schema

**Phase 2: Entity Extraction (Weeks 3-4)**

1. Choose your focus (one beat, not everything)
2. Build ultra-specific extraction prompts
3. Run extraction (expect rate limits)
4. Manually validate samples
5. Create standardization lookups

**Phase 3: External Data (Weeks 5-6)**

1. Identify what data stories reference but don't explain
2. Build scrapers (or find existing datasets)
3. Create summary books
4. Structure for LLM consumption

**Phase 4: Generation (Week 7)**

1. Start with simple prompt, full content
2. Pass story data + external data + extraction metadata
3. Generate draft
4. Fact-check thoroughly
5. Iterate on prompt based on failures

**Phase 5: Interface (Week 8+)**

1. Decide: narrative PDF, interactive website, or both
2. Build components separately
3. Integrate incrementally
4. Test navigation and search
5. Ship when "good enough"

### The Common Mistakes

**Mistake 1: Starting with generation**

Don't write prompts before you have clean data. You'll just regenerate endlessly as data improves.

**Mistake 2: Trusting first-pass extraction**

Single-pass extraction produces chaos. Always multi-pass.

**Mistake 3: Adding more instructions when output fails**

If your 500-word prompt isn't working, a 1000-word prompt won't save it. Simplify or restructure.

**Mistake 4: Trying to build everything at once**

I tried to do local government beat book with budgets, meeting minutes, census data, stories, official lists, and election results simultaneously. It failed.

Build one component, test it, then add the next.

**Mistake 5: Assuming LLMs will "figure it out"**

They won't. They need structure, constraints, examples, and verification.

### What I'd Do Differently

**If starting today:**

1. **Design the schema first** — Spent too much time re-running extractions due to schema changes.

2. **Pick a narrow scope** — Education worked. Local government was too broad. Start focused.

3. **Get external data week 1** — Enriched data makes every subsequent step better.

4. **Build interface mockup first** — Realized I needed different organization after writing everything.

5. **Fact-check earlier** — Waiting until nearly-final draft to discover quote hallucinations was stupid.

6. **Use Git from day one** — Used folders instead of version control. Lost some work.

7. **Test on mobile** — Retrofitting mobile support was painful.

### What I'd Keep

1. **Iterative approach** — Each failure taught me something essential.

2. **LLM for synthesis, not replacement** — AI analyzes patterns. Humans verify and decide.

3. **Multiple models** — No single model does everything well.

4. **Summary books** — Best strategy for managing complex external data.

5. **Brutal honesty** — When something sucks, start over. Don't polish garbage.

---

## Part 11: For Different Beats

The process works for any beat. Swap the specifics:

### Education (What I Built)
- **Stories:** Board meetings, budget battles, test scores, superintendent changes
- **Entities:** Superintendents, board members, principals, schools, districts
- **External data:** MCAP scores, enrollment, demographics, budgets, teacher counts
- **Key questions:** What are scores? Who's the super? What's the budget?

### Courts
- **Stories:** Major verdicts, sentencing, judicial appointments, precedent-setting cases
- **Entities:** Judges, attorneys, defendants, law firms, courthouses
- **External data:** Case volumes, disposition rates, sentencing patterns, docket stats
- **Key questions:** Which judge? What's typical sentence? Who's the defense attorney?

### Local Government  
- **Stories:** Budget votes, zoning decisions, council meetings, elections
- **Entities:** Council members, mayors, town managers, departments
- **External data:** Budgets, meeting minutes, voting records, census demographics
- **Key questions:** Who holds power? What's the budget? How do they vote?

### Housing
- **Stories:** Evictions, development approvals, tenant advocacy, code violations
- **Entities:** Landlords, tenant orgs, housing authorities, developers
- **External data:** Vacancy rates, median rents, eviction rates, violation records
- **Key questions:** Who owns this? What's the rent? What violations exist?

### Environment
- **Stories:** Pollution incidents, conservation efforts, regulatory changes, Chesapeake Bay
- **Entities:** Agencies, advocacy groups, officials, regulated entities
- **External data:** Water quality, pollution levels, permit violations, cleanup progress
- **Key questions:** What's polluted? Who regulates? What's improving/declining?

**The pattern:**
1. Understand the recurring story types
2. Identify the key actors
3. Find the data that contextualizes stories
4. Answer the questions reporters ask weekly

---

## Part 12: Tools & Technical Details

**Python** (3.9+) for data processing

**LLM Access:**
- `llm` CLI tool (https://github.com/simonw/llm)
- Groq API (fast, free tier, rate limits)
- Anthropic API (Claude, paid, quality)
- OpenAI API (ChatGPT, paid, document summarization)

**Scrapers:**
- Python: BeautifulSoup, requests
- JavaScript: Puppeteer (for terrible Microsoft Power BI interfaces)
- OCR: When scraping fails entirely

**Data Processing:**
- JSON for everything
- Datasette for exploration (optional)
- Manual validation in VS Code

**Website Building:**
- Single-page HTML with embedded JavaScript
- All data hard-coded in JS objects (no backend)
- Chart.js for visualizations
- GitHub Pages for hosting (free)

**Version Control:**
- Git (should have used from start)
- Didn't. Used folders. Regretted it.

**Development Environment:**
- VS Code
- Terminal for LLM commands
- Claude/Copilot for script generation
- ChatGPT for document summarization

---

## Part 13: The Honest ROI

**Time invested:** ~100 hours over 4 months
- Data collection: 20 hours
- Entity extraction: 25 hours
- External data scraping: 30 hours
- Generation iteration: 15 hours
- Website building: 10 hours

**Money spent:**
- Groq: $0 (free tier, but created 6 accounts)
- Claude: $0 (hit limits, waited for resets)
- OpenAI: ~$15 (document summarization)
- Total: $15

**What it does:**
- Saves ~30 minutes per story on background research
- Provides instant source contacts
- Contextualizes test scores/budgets/demographics
- Shows coverage patterns
- Prevents duplicate angles

**Intangibles:**
- Deeper beat understanding
- Faster onboarding for new reporters
- Data-driven story ideas
- Expertise reputation

**Would I do it again?** Yes.

**Would I do it the same way?** God, no.

---

## Appendix: The Three Most Important Lessons

After nine iterations, six Groq accounts, countless Claude rate limits, and one near-total disaster with local government:

### 1. Start With the End User, Not The Data

Before one line of code:
- Who will use this? (Beat reporters on deadline)
- When will they use it? (Writing stories, needing quick facts)
- What questions does it answer? (Who's the super? What are scores? Who do I call?)

I didn't do this. I started classifying stories and figured out the purpose later. Wasted weeks.

### 2. Iterate Based on Real Failures

Version 1 wasn't bad because I'm a bad coder. It was bad because I didn't know what good looked like yet.

Each iteration taught me:
- V1: Prompts need positive definitions, not negative exclusions
- V2: Entity extraction needs ultra-specificity
- V3: Narrow scope before scaling
- V4: External data transforms everything
- V5: Too many prompt rules = LLM confusion
- V6: Information overload is real
- V7: Build components separately
- V8: Fact-check reveals all problems
- V9: Ship when good enough

You cannot learn this without building and breaking things.

### 3. LLMs Require Humans in the Loop

I thought AI would "replace" journalism grunt work. It doesn't.

It requires:
- Humans to curate data
- Humans to write prompts
- Humans to validate outputs
- Humans to fact-check quotes
- Humans to decide what matters

But it enables:
- Pattern detection across hundreds of stories
- Synthesis no human could do manually
- Extraction at scale
- Interactive interfaces

**AI is a tool, not a replacement. Use it like one.**

---

## Final Thoughts

This beatbook took four months. The final version is 100x better than v1.

Not because I learned to code better.

Because I learned what actually matters:

- Clean metadata > clever prompts
- Narrow scope > comprehensive coverage
- External data > more stories
- Fact-checking > trusting AI
- Iteration > perfection

If you're building a beatbook:

**Start small.** One beat. One county. One type of story.

**Expect failure.** Your first draft will suck. That's fine.

**Fact-check ruthlessly.** LLMs hallucinate quotes. Always.

**Ship when good enough.** Perfect is the enemy of useful.

**Learn from what breaks.** Every failure teaches something essential.

Good luck. You'll need it. But you'll build something valuable.