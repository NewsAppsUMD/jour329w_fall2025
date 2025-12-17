# How to Build a Beat Book: A Practical Guide

*Lessons from building an interactive education beatbook over four months*

---

## What This Guide Is

This is a practical guide for building a beatbook. It tells you what works, what doesn't, and how to avoid common mistakes. No coding experience required—though you'll need to work with AI tools and organize data carefully.

---

## The Core Workflow

**Timeline Note:** You'll work on gathering external data while also extracting information from stories. Both need to be done before you generate the final beatbook.

### Phase 1: Collection & Classification (Weeks 1-2)

**1. Pull stories broadly**
- Cast a wide net at first
- Include anything that might be relevant
- Don't worry about being perfect yet

**2. Classify stories by topic**

This takes multiple attempts to get right. Here's what worked:

**First attempt:** I wrote topic definitions that said what they were NOT ("excluding obituaries, legal notices..."). The AI classified everything as "Other."

**Second attempt:** I rewrote definitions to say what topics ARE ("Articles about school board meetings, budget decisions..."). Better, but still only 40-50% accurate. It couldn't tell editorials from news stories.

**Third attempt:** I added categories for content type (News vs. Opinion vs. Calendar) and allowed stories to have a secondary topic. I also included examples in my instructions to the AI. This got me to 90%+ accuracy.

**Key lesson:** You'll need to refine your categories and instructions multiple times before the AI understands what you want.

**3. Filter to your best stories**
- Define what "relevant" means for your beat
- Remove calendars, briefs, unrelated content
- Aim for quality over quantity

**4. Decide on your data structure early**

Figure out what information you need for each story:
- Unique ID
- Headline
- Full text
- Publication date
- Author
- Topic categories
- Geographic tags

**Once you settle on this structure, don't change it.** Every change means re-processing all your stories.

---

### Phase 2: Gather External Data (Weeks 3-4)

**Start this early.** Your stories reference things they don't fully explain. You need to go get that context.

**What data to gather:**

**For your region:**
- Population, poverty rates, median income
- Demographic breakdowns
- Other relevant stats (broadband access, unemployment, etc.)

**For specific jurisdictions (like school districts):**
- Spending data
- Number of facilities
- Staff counts and ratios
- Performance metrics

**For individual entities (schools, courts, etc.):**
- Enrollment or case loads
- Test scores, graduation rates, or other outcomes
- Demographic information

**Where to get it:**
- U.S. Census Bureau
- State agencies (Education, Courts, Health, etc.)
- Local government websites

**How to organize it:**

Create summary documents BEFORE asking AI to generate your beatbook.

Organize your data clearly:
- One file for each county/jurisdiction with all relevant stats
- Include population, demographics, budget info
- List key officials with their titles
- Note important metrics (test scores, spending per pupil, etc.)

**If you're working with huge budget documents:**

Don't feed a 1,000-page PDF to an AI. Instead:
1. Use ChatGPT or Claude to summarize the key points
2. Create a structured summary with tables comparing jurisdictions
3. Focus on: main budget numbers, major changes from last year, new initiatives, capital projects
4. This makes generation much faster and more accurate

---

### Phase 3: Extract Key Information from Stories (Weeks 3-5)

**Do this while gathering external data. Start after your stories are classified.**

**The goal:** Pull out people, places, organizations, and events mentioned in your stories.

**Key lesson:** Being too specific means you'll miss things. Being too broad means you'll get junk.

**What to extract:**

For an education beat:
- Superintendents, principals, board members
- Schools, districts, education nonprofits
- State education officials
- Major initiatives (like "Blueprint for Maryland's Future")

**What NOT to extract:**
- Parents quoted only once
- Students
- The reporter who wrote the story

**How to stay organized:**

Create a lookup list of all towns/cities in your coverage area. This helps the AI tag locations consistently.

Decide on a standard format for names: "Sharon Pepukayi (Superintendent, Talbot County Public Schools)"

After extraction, count how many times each person/place appears. The most-mentioned ones are your key sources.

**Expect to iterate:** You'll probably need to adjust your instructions 2-3 times before you get clean results.

**Be prepared for rate limits:** If you're processing hundreds of stories, you might hit daily limits on free AI tools. Plan for this to take a few days.

---

### Phase 4: Generate Your Beatbook (Weeks 6-7)

**Now you're ready to have AI write your beatbook.**

**What to give the AI:**

1. Your county/jurisdiction data summaries
2. Your school/entity data summaries  
3. Your story content (or at minimum, headlines and summaries)
4. Clear instructions about what you want

**What to ask for:**

1. Three major issues affecting your beat overall
2. Breakdown by county/jurisdiction with specific coverage themes
3. List of key sources (with their titles and what they're quoted about)
4. List of key documents (budget reports, meeting minutes, etc.)

**Critical rules for the AI:**

- Use specific numbers from the data you provided
- Reference which stories support each claim (by story number or headline)
- Format all names consistently: "Name (Title, Organization)"
- Do NOT make up quotes
- Write in clear paragraphs, not bullet points (for issues section)
- Use lists only for sources and documents

**Important:** Keep your instructions simple. 10 rules maximum. If you give the AI 30 different rules, it'll ignore half of them or start making things up to fill gaps.

**For multi-county beats:** Start with an overview section covering issues that affect all areas. This prevents you from repeating the same thing five times.

---

### Phase 5: Fact-Checking

**What to check:**

✅ **Data from your summary books** (usually accurate)
- Demographics, test scores, budgets
- Verify spot-checks anyway

⚠️ **Data from story content** (90-95% accurate)
- Statistics mentioned in articles
- Dates and timelines (LLMs are terrible with chronology)
- Expect ~5% error rate

❌ **Quotes** (often wrong)
- Paraphrases presented as direct quotes
- Quotes from summaries, not original articles
- Invented quotes to fill gaps
- **Solution:** Don't include quotes in LLM-generated sections

🔍 **Tone and currency**
- Watch for overly lofty language ("proved pivotal," "could redefine")
- Check that information is current, not outdated
- Verify election results, vacancies, pending lawsuits, unpassed legislation
- Look for spelling errors in place names ("Talton County" vs. "Talbot County")

**Fact-checking workflow:****
1. Check first complete section thoroughly
2. If error rate is <5%, spot-check others
3. If error rate is >5%, check everything
4. Always verify anything a reporter will rely on

---

### Phase 6: Build Your Interface (Week 8+)

**You have two options:**

**Option 1: Simple document (PDF or Google Doc)**
- Easier to create
- Works fine for smaller datasets
- Easy to share and read
- Hard to search through lots of information

**Option 2: Interactive website**
- More useful for reporters in the field
- Searchable and filterable
- Can include charts and visualizations
- Requires more work to build

**If you build a website:**

You don't need a database or complex backend. A simple HTML page with JavaScript can do everything you need.

**Essential features:**
- Search bar AND filters (let users find things multiple ways)
- Visual indicators for different counties/beats
- Show result counts ("23 of 175 stories")
- Click to expand details (don't show everything at once)

**Nice-to-have features:**
- Sortable tables
- Charts showing trends
- Story archive that looks like an email inbox
- Searchable source directory
- Meeting calendar
- Simple chatbot to help navigate

---

## Common Mistakes to Avoid

### Mistake 1: Starting with generation
Don't ask AI to write your beatbook before you have clean, organized data.

### Mistake 2: Trusting the first attempt
Your first pass at extracting information will be messy. Plan to refine and re-run.

### Mistake 3: Adding more rules when things fail
If 10 instructions didn't work, 30 instructions won't either. Simplify your approach instead.

### Mistake 4: Trying to do everything at once
Build one piece at a time. Test it. Then move to the next piece.

### Mistake 5: Assuming AI will figure it out
AI needs clear structure, examples, and specific instructions.

### Mistake 6: Defining topics by what they're NOT
Don't say "all stories except calendars and sports." Say "stories about budget decisions and policy changes."

### Mistake 7: Ignoring rate limits
Free AI tools have daily limits. If you have 500 stories, this will take multiple days.

### Mistake 8: Waiting to fact-check
Check a sample section early. Don't discover problems after generating everything.

### Mistake 9: Not including an overview
For multi-county beats, write one overview section covering issues that affect everyone. Otherwise you'll repeat yourself.

---

## When Beatbooks Are Most Valuable

**Local journalism:** When you don't have a reporter or editor who's been covering the area for generations, beatbooks become essential reference.

**College newspapers:** Student journalists graduate and subject matter expertise disappears. Beatbooks preserve institutional knowledge.

**New reporters:** Getting up to speed on complex beats without a months-long learning curve.

**Investigative projects:** Having comprehensive source lists and historical context at your fingertips.

**Not as valuable:** Large metro papers where reporters already have deep beat knowledge and extensive contacts.

---

## The Non-Negotiables

### 1. Clean data is everything
You cannot build a useful beatbook without organized, consistent data. Spend most of your time getting this right.

### 2. External data makes it valuable
Stories mention things without explaining them. Go find the actual numbers and context.

### 3. AI makes up quotes
Don't ask AI to include quotes unless you plan to verify every single one.

### 4. Expect to re-run things multiple times
Your first attempt won't be perfect. Build in time to refine and improve.

### 5. Start narrow
One beat. One county. Get that working, then expand.

### 6. Always spot-check
Manually verify samples. Expect 5-15% of AI output to have errors.

---

## Tools You'll Need

**AI Tools:**
- ChatGPT, Claude, or similar for generating summaries and beatbook text
- Free tiers work but have daily limits
- Budget $10-20 if you want faster processing

**For gathering data:**
- Web scraping tools (if you're technical)
- Manual copy/paste into spreadsheets (if you're not)
- Sometimes you'll need to screenshot and OCR difficult interfaces

**For organizing:**
- Excel or Google Sheets
- JSON files (simple text format for data)
- Any text editor

**For building a website (optional):**
- Basic HTML and JavaScript
- GitHub Pages for free hosting
- Chart libraries like Chart.js for visualizations

---

## Time & Cost

**Time:** Plan for 100 hours spread over 3-4 months
- Gathering and classifying stories: 20 hours
- Finding external data: 30 hours
- Extracting information from stories: 25 hours
- Generating and refining beatbook: 15 hours
- Building interface: 10 hours

**Cost:** $10-20 for AI tools (if using paid options)
- Free options work fine but are slower

**Ongoing:** ~3 hours every few months to update

---

## What Success Looks Like

**Reporters actually use it:**
- They visit weekly when working on beat stories
- They spend 5+ minutes (not just quick lookups)
- They come back multiple times while writing

**Quality indicators:**
- Reporters ask follow-up questions about beatbook info
- Stories cite specific stats from the beatbook
- Other reporters ask for access
- Editors reference it in story assignments

**Long-term value:**
- After 6 months, it saves more time than you spent building it
- Better, more informed stories
- Faster turnaround on breaking news

---

## Final Principles

**Start small.** One beat. One area. Get it working before expanding.

**Expect problems.** Your first version will have issues. That's normal.

**Check everything.** AI makes mistakes. Verify anything important.

**Ship it.** Don't wait for perfect. Launch when it's good enough.

**Improve from use.** Watch how people actually use it, then make it better.
