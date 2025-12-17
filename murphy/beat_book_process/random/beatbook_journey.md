# Building a Beat Book: My Journey Through Nine Iterations

*A brutally honest account of failures, disasters, rate limits, and eventual success*

**Updated December 16, 2025** — This version includes additional details from the actual notes: specific script names, model switches mid-extraction, classification failures with calendars and "Today in History", token limit issues, hallucinated links, spelling errors, dating problems, tone issues, the quote extraction breakthrough context, and more accurate descriptions of what actually happened at each stage.

---

## Introduction

Most guides tell you what worked. This one tells you what broke, why it broke, and what I learned from breaking it.

I built an education beatbook for five Maryland Eastern Shore counties. I started with 200 Star-Democrat stories in November, thinking I'd classify them by topic and be done in a week. Four months later, I had built (and discarded) eight different versions, burned through six Groq accounts, maxed out Claude's rate limits twice, spent actual money on API calls, and ended up with an interactive dashboard containing 175+ stories, 99 source contacts, school-level data for 47 schools, and a (mediocre but functional) chatbot.

The final version is good. Really good.

But I got there by doing almost everything wrong first.

This is the story of what broke, why it broke, and what I learned from breaking it.

---

## Iteration One: Topics (Or: Why "Other" Is a Trap)

**November 1. The assignment: classify 200 stories by topic.**

I started confident. I created a CSV with 13 topics and detailed descriptions:

```
"Local Government","News articles, excluding obituaries, legal notices, calendars, columns and editorials, that center around and primarily discuss the members and actions of a local government..."
```

My last topic was "Other" — defined as "obituaries, legal notices, calendars, columns, editorials and any articles that do not otherwise fall under a defined topic."

I ran the script (`classify_topics_1.py`).

**The LLM classified all 200 stories as "Other."**

Every. Single. One.

(The funny thing? I can't replicate this now. I've rerun the script and it classifies the first three stories and then fails. But that first time, it worked — just catastrophically wrong.)

### What Went Wrong

I had defined a category by what it's NOT. The LLM saw my list of exclusions in every topic definition and thought, "Oh, these must all be excluded things."

### The Fix (Attempt 1)

I rewrote the prompts to provide positive definitions only. No more "excluding X, Y, Z" language. Instead: "Articles that center around and primarily discuss..."

I also gave the LLM examples.

**Second run: Still not great.**

It got maybe 40-50% right. But there were issues:

- "EDITORIAL: 10-cent paper bag fee should be optional" → classified as "Environment" (not wrong, but it's an EDITORIAL)
- "SPRING TRAINING GLANCE 3-10-24" → classified as "Sports" (it's a table/calendar)
- All the "Today in History" articles → classified as "Columns & Editorials" (no)

And I got 40+ variations of what should have been the same topic:
- "Test Results"
- "MCAP Scores"  
- "Assessment"
- "Student Performance"
- "Achievement Data"

All for test score stories.

### The Multi-Pass Strategy (Born From Necessity)

This is where I discovered: **single-pass classification will fail.**

AI is probabilistic. Without constraints, you get chaos.

**First attempt:**  
I had 18 predefined topics with definitions that said what they WEREN'T ("Articles, excluding obituaries, legal notices, calendars, columns and editorials...").

**Result:** Classified all 200 stories as "Other" because every definition listed exclusions.

**Second attempt:**  
Rewrote all definitions to say what topics ARE. Same 18 topics, removed "excluding..." language.

**Result:** 40-50% accuracy. Got "EDITORIAL: 10-cent paper bag fee" as "Environment" (not wrong, but it's an editorial). Got "Today in History" as "Columns & Editorials" (no).

**Third attempt:**
Major restructuring. Added two new categories: `content_type` (to distinguish news from opinion) and `secondary_topic` (for stories about multiple things).

I gave it examples:
```
- "Robbins YMCA opening reading hub to tackle childhood illiteracy" = News, Education, Arts & Culture
- "TV LISTINGS 7-19-24" = Miscellaneous, Other, None
```

This took 90 minutes to run.

**Results:**
- Content type breakdown: 144 News, 18 Opinion, 17 Miscellaneous, 9 Calendars, 6 blank, 5 Obituaries, 1 Legal Notice
- Primary topic: 57 Arts & Culture, 24 Public Safety, 19 Sports, 18 Other, etc.
- Out of 200 stories, I disagreed with maybe 10

**Fourth attempt:**
I tried letting the AI generate its own topic names. Failed every time. Gave up on this.

**Validation:** 
Manually checked 20 stories per category. The third attempt was good enough that I stopped.

### Lessons Learned

- Never define a category by exclusion ("articles excluding X, Y, Z")
- Adding structured fields (content_type, secondary_topic) improves accuracy dramatically
- Including examples in prompts helps
- Different models have different strengths - test multiple
- Slower models sometimes = better results (90 min vs 5 min, but 95% accurate vs 50%)
- Manual validation required even with good scripts

---

## Iteration Two: Entities (Or: When Specificity Backfires)

**November 5. The assignment: extract people, places, and organizations.**

I overloaded Copilot. Twice.

I got rate-limited three times on my FIRST attempt.

I also had to switch AI models mid-extraction after 55 stories because I hit rate limits again.

### The Ambitious Plan

I decided to be comprehensive. Seven new categories:
- Content type (News, Calendar, Sports, etc.)
- People
- Locations 
- Institutions
- Events
- Municipalities
- County

I was proud of this. Especially the municipalities—I spent hours building a comprehensive list of every town in all five counties the Star-Dem covers, plus all 19 other Maryland counties just in case stories mentioned them.

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

Perfect. Exactly what I wanted.

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

**Thirty-five locations. For one calendar listing.**

And events like this:

```json
["Tuskegee syphilis experiment", "in vitro fertilization", "Woolworth's sit-in protests", 
"Air France Concorde crash", "Wikileaks Afghanistan war records", 
"Ukrainian presidential phone call", "Indigenous residential schools apology"]
```

Yeah.

### What I Learned

**The problem wasn't the prompt.** It was that I was feeding it calendars and expecting news analysis.

The Star-Dem data was organized terribly. News mixed with calendars mixed with sports briefs. The LLM couldn't distinguish what mattered because I hadn't distinguished what mattered.

Also: asking for "locations" in a beat where schools ARE the locations is circular.

**Key insight:** Garbage in, garbage out. Even with good prompts.

### Datasette Kept Crashing

Oh, and Datasette crashed every time I tried to facet using its clickable "suggested" facets. Made it even harder to analyze the data.

### Lessons Learned

- Clean your data before extraction
- Some categories don't make sense for every beat
- Rate limits are real (plan for them)
- Microsoft Power BI interfaces are terrible for scraping

---

## Iteration Three: Topic + Entities (Or: The Importance of Narrowing Scope)

**November 10. I chose education as my focus.**

I could have done local government — it had 1,324 stories. But local government is sprawling. Everything from budgets to zoning to public works to elections.

Education had 779 stories (after merging primary + secondary topic classifications). More manageable.

More importantly: **I cared about education.** When you're spending weeks on entity extraction, work on something you actually want to understand.

### The Ultra-Specific Prompt Strategy

Because I was focusing on ONE topic, I could be incredibly specific:

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

This worked far better than my generic "important people" approach from Iteration 2.

### What Worked

**Consistent county/municipality extraction:** By providing that absurdly long list of Maryland towns, it nailed geography. Every "Easton" was formatted identically. Every "Talbot County" was consistent.

The municipality list was worth every hour I spent building it. Official Maryland websites only list official municipalities, not unincorporated communities or CDPs, so I used Wikipedia's lists for all 24 Maryland counties.

**Organizational split:** I broke "organizations" into five categories:
- Key events
- Key initiatives  
- Key establishments (physical places)
- Key organizations (non-government)
- Key bodies (government institutions)

Example output:
- "Blueprint for Maryland's Future" (initiative)
- "Empowerment Academy" (establishment)
- "Maryland Association of Secondary School Principals" (organization)
- "Talbot County Board of Education" (body)

### What Didn't Work  

**The regions field was hit or miss.** I added it to find stories that mentioned other states, but it often extracted irrelevant stuff. Like, a teacher gets an award and she served on a board in Delaware years ago, so Delaware gets extracted as a region. I told it to exclude those, and it was okay with organizations but the regions field was messy.

**The locations field was too broad.** The idea worked better for non-education stories. For education, the locations WERE the establishments (schools), so it was just duplicate, niche information.

**Title format inconsistency:**  
Sometimes: `"Sharon Pepukayi (Superintendent of Talbot County Public Schools)"`  
Other times: `"Sharon Pepukayi (Superintendent, Talbot County Public Schools)"`

One comma difference. Same person. Infuriating.

**Inference failures:**  
Someone called "Board Vice President" didn't get extracted because "education" wasn't explicit in the title, even though I'd extracted this same person in other stories where they were called "Vice President, Board of Education."

**False negatives everywhere:** The ultra-specific prompt excluded people whose relationship to education was implied rather than stated.

### The Patterns

Most frequently mentioned:
- Sharon Pepukayi, Superintendent, Talbot County (7 stories)
- Emily Jackson, President, Talbot County Board of Education (7 stories)
- Dr. Derek Simmons, Superintendent, Caroline County (6 stories)

Counties covered:
- Talbot County (111 stories)
- Caroline County (54 stories)
- Dorchester County (41 stories)

The consistency was reassuring — it meant the extraction was working reliably across stories.

### Lessons Learned

- Narrow your scope before extraction (one beat, not all beats)
- Be specific about format in your prompts
- Build lookup tables for standardization
- Accept that ultra-specific prompts create false negatives
- Some manual cleanup is inevitable

---

## Iteration Four: Choice & First Draft (Or: When More Data ≠ Better Output)

**November 12. I merged everything and ran it all.**

I pulled education stories from other topic files (local government, health, public safety) where education appeared as a secondary topic.

Set confidence thresholds:
- >0.8 for primary education stories
- >0.65 for secondary education stories

Ended up with 779 stories. Re-ran entity extraction on all of them.

**Got rate-limited so many times I created six Groq accounts.**

After removing duplicates and failures: 754 unique entries with full metadata.

### Filtering Down

Then I wrote a script to filter to beat book-worthy stories. I defined "relevant" as:
- News stories (not calendars, obituaries, legal notices)
- Related to the five covered counties
- About boards of education, public officials, funding, policy

This eliminated 2/3 of entries. Left me with 278 stories.

### My First Beatbook Generation Attempt

I gave ChatGPT my metadata schema and asked it to write a beatbook generation script based on the example from class.

(Chat log: https://chatgpt.com/share/6918d97e-5d48-800c-890b-bdc2e50300de)

The prompt said:
- Use entity metadata AND full story content
- Generate county-by-county sections
- Create three main outputs: Top 3 Issues, Key Sources, Key Documents
- Write in narrative prose (no bullets)
- Make it "feel like a newsroom beat memo"

**It generated 42 pages.**

I used model `meta-llama/llama-4-maverick-17b-128e-instruct` initially, but hit the token limit. Switched to `openai/gpt-oss-120b` and it worked.

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

**Hallucinations:** Facts were mostly accurate, but quotes were invented or badly paraphrased. It also hallucinated some links (tcps.org, uppershorewib.org, kent.k12.md.us) though it got major state websites right (mgaleg.maryland.gov).

**Names I thought were hallucinated but weren't:** Kept seeing "Mark Jones" and "Sarah Jones" and thought it was making them up. Nope. Those really are their names.

**Spelling errors:** "Talton County" and "Talark County" instead of "Talbot County."

**Dating issues:** No comprehension of time or chronology. Things were out of order and at times completely wrong.

**Tone problems:** Would slip into "proved pivotal" and "could redefine Talbot County's educational trajectory" nonsense. Too lofty and presumptive.

**Length:** 42 pages was too long for a reference document.

### Draft Two: The Overcorrection

I asked Copilot to:
- Simplify and shorten (max 3 paragraphs per issue)
- Remove "why this matters" sections
- Use titles and metadata ONLY (no full story content)
- Strip out the content in `<think></think>` tags
- Use `groq/qwen/qwen3-32b`

**It generated 16 pages.**

100% expected this to bomb. I really didn't think titles and metadata would be enough information.

Better length. But now it was repetitive and shallow. Every county's "pandemic recovery" section looked identical because it didn't have story details to differentiate them. The pandemic was a central issue for basically every county, but without specific information, the summaries all looked the same.

Same with Blueprint for Maryland's Future rollout — incredibly repetitive across counties.

It also focused on bizarre sources:

```md
**Julie Hickey** – Coordinator of Food Services, Queen Anne's County Public Schools
```

Sure, she appeared in stories. But she's not a key education beat source.

### Lessons Learned

- Metadata-only = shallow and repetitive
- Full content without limits = bloated
- You need external data to contextualize stories
- Length is a design choice, not an accident
- LLMs will hallucinate quotes unless constrained

---

## Iteration Five: Draft V2 (Or: Data Changes Everything)

**November 22. I went and got the actual data.**

My first drafts kept referencing things they couldn't explain:
- "Blueprint for Maryland's Future funding increased..."
- "MCAP scores declined..."
- "Student discipline rates rose..."

Stories mentioned these things but didn't provide full context. So I went scraping.

### What I Scraped (And Why It Was Painful)

**School discipline data:** Huge hassle. Got numbers by county, school, type, race, gender, disability, and offense. Worth it.

**Teacher data:** Number of teachers per county, % increase/decrease from prior year, number of new teachers, % of all teachers who are new.

Microsoft Power BI interface wouldn't scrape properly, so I **screenshotted and OCR'd it.**

**MCAP scores:** Statewide data to show how Eastern Shore schools perform comparatively.

**Blueprint funding:** Had to pull summaries from local news network since actual budget documents were disasters.

**Census data:** Already had this (population, poverty, median income, demographics).

This took FOREVER. Scrapers kept outputting duplicates or misinterpreting tables. Manual verification required.

Getting the school budgets was "nearly impossible" — when you CAN get them, they're such a disaster it's not even worth it. So I pulled Blueprint funding summaries from the local news network instead.

### The County Summary Book Strategy

Instead of hardcoding stats into my generation prompts, I created two summary files:

**`county_summary_book.json`:** County- and district-level data

**`school_summary_book.json`:** School-level data (47 schools)

Then I passed these TO the LLM during generation.

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
do not include "Neighboring District Superintendents"
do not include "Community & Service Organizations"
no "Law Enforcement & Public Safety"
no "State Education Agency"
```

...and more.

**Result:** The LLM started ignoring rules and hallucinating to fill gaps.

It wrote: "Specific principal names were not provided in the source data; please refer to the Kent County Public Schools website..."

**I HAD PROVIDED PRINCIPAL NAMES.** They were in my county summary book. It just couldn't find them in the wall of instructions.

**Formatting degraded.** Instead of lists, it gave me semicolon-separated strings.

### I Switched Models

Tried `groq/meta-llama/llama-4-maverick-17b-128e-instruct` instead of GPT.

Better organization and citations. Slightly more reasonable length. But still not great.

Also realized I was still missing key data — specifically enrollment broken down by race and special populations. Tried to scrape it from MSDE but Microsoft Power BI proved "very difficult" to scrape. Moved on to easier data for now.

### Key Realization

I was still missing enrollment broken down by race and special populations. Needed this for context on suspension rates.

### Lessons Learned

- External data makes narratives 10x better
- Create summary books BEFORE generation
- Too many prompt rules = LLM confusion
- Model choice matters for different tasks
- You'll always realize you're missing data

---

## Iteration Six: Draft V3 & The Local Government Disaster

**November 29. I tried to do local government. It broke everything.**

I thought: if education worked, local government will too. Just... more of it.

I processed 748 local government stories, whittled down to the ~170 most relevant and timely.

I went out and got MORE data:
- Budget analysis for each county
- Census data (already had this)
- County and municipal officials
- Election data  
- **Recent council meeting minutes for EVERY county**

I asked Claude to generate enormous summary documents analyzing each county's budget and meeting minutes.

I downloaded all of this **by hand.**

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

**1. Fed terrible output to ChatGPT**

It said:

> "The beatbook is pretty strong structurally but nowhere near the standard you want (both for your own reporting and for Howard Center/NYT-style clarity)."

(Thanks, OpenAI memory feature from when I practiced resume writing with you two weeks ago.)

ChatGPT was brutal: "this reads like you're tripping on acid" (paraphrasing).

**2. ChatGPT gave me a new script**

**3. Copilot had to fix it** because it had 25 issues.

**4. Ran the script. Gave output to Claude.**

Claude said:

> "Your prompt is burying the model under too much instruction and not enough clear signal about what matters."

Also:

> "Use a better model - groq/openai/gpt-oss-120b is not ideal for this. Try claude-3-5-sonnet-20241022 via the Anthropic API directly."

(Nice "please don't use our competitor's model" touch, Claude.)

**5. Claude wrote a script. Produced 82 pages.** 

Considerably better quality, but still redundant and weird.

**6. Gave feedback to Claude. Rewrote script.**

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

### Lessons Learned

- Some beats are too broad for one beatbook
- There IS such a thing as too much context
- Fast generation = shallow analysis
- Sometimes you need to walk away and start over

---

## Iteration Seven: Different (Or: Building the Website)

**December 6. I pivoted to building a browser-based interface.**

Narrative beatbooks are fine. But what if reporters could INTERACT with the data?

### The Early Versions

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

### The Parallel Experiments

While fighting with the website, I tried other things:

**1. Asked ChatGPT to create a comprehensive budget databook**

In an effort to compress 10 massive budget documents into a single file, I had ChatGPT generate a comprehensive but succinct data book. 

I tried using Gemini to compare results, but ChatGPT's was far and away better in terms of quality, structure, consistency, and relevance. Took some back and forth, but the final product had:

Sections per county:
- Core fiscal table
- Enrollment & per-pupil spending
- Blueprint drivers
- Capital outlook
- Emerging fiscal/policy issues
- Narrative summary

Plus two additional chapters at the end:
- Cross-county comparison tables
- Regional takeaways

This was one of the best summary books I made. ChatGPT crushed it.

**2. Asked Copilot to extract all quotes and generate source profiles**

Problem: Generated beatbooks kept hallucinating quotes. Badly paraphrased, nonsensical, or fully invented.

I realized during fact-checking that quotes were GARBAGE. Everything from badly paraphrased to utterly nonsensical to pure hallucination. But the data it used (when I provided it separately) was completely accurate.

The solution: If I pre-extract quotes and provide them to the LLM as structured data (like I do with test scores), it should handle them better.

Script extracted quotes and generated 26 profiles — one for every key player quoted 5+ times. Initially it kept hallucinating quotes IN the profiles, so I had to keep tweaking to get it to pull ONLY relevant quotes and use ONLY those quotes plus story content for the bios.

**3. Went back to Claude and made a narrative beatbook (again)**

For some reason, the narrative beatbooks I generated THIS time were fire.

Random Groq model: pretty good.

Switched to `gpt-oss-120b`: INSANE quality.

I think it was the budget data. But the dramatic improvement floored me — and pissed me off. **NOW you work?**

**4. One more try at the website**

I had very little hope. Everything was too large. Claude kept breaking.

**But it worked.**

After many tweaks:
- Five key issues with "critical findings" summaries, paragraphs, and data tables
- County-level narrative breakdowns with key statistics (enrollment, budget, state funding)
- **Interactive schools dashboard:** All 47 schools. Filter by county. Click to see enrollment, demographics, student groups.
- **Searchable sources table:** 58 source cards with titles, organizations, topics quoted on, number of quotes.

### Lessons Learned

- Sometimes you need to abandon an approach entirely
- Build components separately, then integrate
- Source verification requires pre-extraction
- The right model + right data = dramatic quality jumps
- Persistence eventually pays off (or you hit your breaking point)

---

## Iteration Eight: Nearly Final (Or: Fact-Checking Reveals Everything)

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

**Pull quotes into separate document** organized by topic. Assign full names to quotes.

**Prompt to cite by row ID:** "Story #25" instead of trying to reference headlines. Build a Datasette so reporters can look up Story #25.

**Add school-level enrollment data** with census tract data.

(I tried scraping from MSDE but Microsoft Power BI is terrible. Eventually built JavaScript scrapers with Claude's help.)

### Lessons Learned

- LLMs are great with structured data you provide
- LLMs are terrible with quotes
- Pre-extract quotes if accuracy matters
- Verify everything a human will rely on
- Structure determines repetition

---

## Iteration Nine: Final (Or: The One That Actually Works)

**December 15. This is it.**

I was pleased with Nearly Final structurally. Didn't want to overhaul anything.

Just build out specific features and improve navigation.

### What I Built

**1. Reorganized schools page**
- Added MCAP data that was missing
- Added +/- indicators comparing to state averages
- Changed dropdowns to popups (less clunky)
- Added county and school-level filters
- Added sortable columns

**2. Fixed source directory**
- Subject and county filters
- Eventually got dynamic loading working (Copilot kept hardcoding them instead of loading dynamically, which took forever to fix)
- 58 source cards total (26 from quote extraction + district officials I'd scraped earlier)

**3. Story archive (the ambitious one)**
- Formatted like an email inbox
- Filter by county and year
- Sort by publication date
- Search full text
- Click article to open in side panel

Had to remove some irrelevant stories (board meeting overviews, newsletter intros).

Biggest challenge: formatting. JSON had `\n` everywhere.

**Future goal:** Sort by metadata topics and mentioned people.

**4. Meeting calendar**
Claude did deep research and filled it in. Easy addition.

**5. Local impact sections**
Added clickable tabs showing county-specific implications for each major issue.

**6. More demographic data**
Required more scraping (graduation rates, additional breakdowns).

**7. The chatbot (frustrating)**
Started okay. Tried to improve it. Lost all functionality.

Tried integrating Groq. Disaster.

Ended up with mediocre chatbot. Want better one. Need more time.

### What I Didn't Get To

**Document repository:** Ran out of time.

### What I'm Proud Of

**Navigability:** Organization, structure, user experience.

**Data integration:** Everything connects. Stories → sources → schools → counties.

**Interactivity:** Can actually explore, not just read.

### What Needs Work

**JavaScript cleanup:** Inline CSS/JS needs refactoring.

**Chatbot:** Needs to actually be good.

**More features:** Ideas for spring.

### Lessons Learned

- Feature creep is real (manage it)
- Sometimes "good enough" ships
- Iterative improvement beats perfection
- User testing would have helped (didn't do it — should have watched real reporters use it)
- Interactive > static for beat books
- Inline CSS/JS is heinous (clean it up before showing anyone)

---

## What I Wish I'd Known

Looking back at the entire journey, here's what I'd tell myself in November:

**You will break it. Multiple times.** That's fine. That's the process.

**The first model that works isn't the best model.** Keep testing.

**External data is the difference between "okay" and "actually useful."** Get it early.

**LLMs are terrible with time.** Dates will be wrong. Chronology will be confused. Check everything.

**You cannot prompt your way out of structural problems.** Fix the data, don't add more instructions.

**Some beats are too big for one beatbook.** Education worked. Local government was too sprawling.

**Fact-check early, not at the end.** Discover problems when you can still fix them easily.

**Git from day one.** Folders are not version control.

**The chatbot will be harder than you think.** Start with pattern-matching, not AI integration.

**Document your failures.** They're more valuable than your successes.

---

## What I Wish I'd Known

Looking back at the entire journey, here's what I'd tell myself in November:

**You will break it. Multiple times.** That's fine. That's the process.

**The first model that works isn't the best model.** Keep testing.

**External data is the difference between "okay" and "actually useful."** Get it early.

**LLMs are terrible with time.** Dates will be wrong. Chronology will be confused. Check everything.

**You cannot prompt your way out of structural problems.** Fix the data, don't add more instructions.

**Some beats are too big for one beatbook.** Education worked. Local government was too sprawling.

**Fact-check early, not at the end.** Discover problems when you can still fix them easily.

**Git from day one.** Folders are not version control.

**The chatbot will be harder than you think.** Start with pattern-matching, not AI integration.

**Document your failures.** They're more valuable than your successes.

---

## Reflection: What Actually Matters

After nine iterations, six Groq accounts, countless Claude rate limits, and one near-total disaster with local government:

### The Three Most Important Lessons

**1. Start With the End User, Not The Data**

Before one line of code:
- Who will use this? (Beat reporters on deadline)
- When will they use it? (Writing stories, needing quick facts)
- What questions does it answer? (Who's the super? What are scores? Who do I call?)

I didn't do this. I started classifying stories and figured out the purpose later. Wasted weeks.

**2. Iterate Based on Real Failures**

Version 1 wasn't bad because I'm a bad coder. It was bad because I didn't know what good looked like yet.

Each iteration taught me something I couldn't have learned without building and breaking things.

**3. LLMs Require Humans in the Loop**

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

## The Honest ROI

**Time invested:** ~100 hours over 4 months

**Money spent:** ~$15

**What it does:**
- Saves ~30 minutes per story on background research
- Provides instant source contacts
- Contextualizes test scores/budgets/demographics
- Shows coverage patterns

**Would I do it again?** Yes.

**Would I do it the same way?** God, no.

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
