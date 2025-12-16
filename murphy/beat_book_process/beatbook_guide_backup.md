# How to Build a Beat Book: A Practical Guide

*Lessons distilled from four months of building an interactive education beatbook*

---

## What This Guide Is

This is the practical, actionable guide extracted from building a beatbook through nine iterations. It tells you what works, what doesn't, and how to avoid common mistakes.

For the full story of failures, disasters, and eventual success, see `beatbook_journey.md`.

---

## The Core Workflow

### Phase 1: Collection & Classification (Weeks 1-2)

**1. Pull stories broadly**
- Accept over-collection initially
- Include all stories that might be relevant
- Don't try to be perfect at this stage

**2. Classify by topic using multi-pass strategy**

**Pass 1: Exhaustive Extraction**
- Let the LLM run wild
- See what categories emerge naturally
- Expect chaos (40+ topic variations is normal)

**Pass 2: Guided Standardization**
```python
prompt = f"""
Previously used topics: Budget, Test Scores, Enrollment, Infrastructure, 
Board Actions, Superintendent Changes, Achievement Gaps

Use an existing topic if it fits. Only create new if genuinely different.
"""
```

**Pass 3: Manual Consolidation**
- Merge near-duplicates yourself
- "Test Results" + "MCAP Scores" → "Test Scores"

**Pass 4: Human Validation**
- Manually check 20 stories per category
- Fix misclassifications
- Expect ~15% error rate

**3. Filter to relevant subset**
- Define "relevant" for your beat
- Remove calendars, briefs, unrelated content
- Aim for quality over quantity

**4. Lock down data schema**
```json
{
  "id": "unique_id",
  "title": "Story headline",
  "content": "Full story text",
  "url": "https://...",
  "date": "YYYY-MM-DD",
  "author": "Reporter name",
  "primary_topic": "Budget",
  "counties": ["Talbot", "Kent"],
  "primary_county": "Talbot"
}
```

**Every schema change means re-running every extraction script. Do this once.**

---

### Phase 2: Entity Extraction (Weeks 3-4)

**1. Choose your focus**
- Pick ONE beat, not everything
- Education worked. Local government was too broad.
- You can always expand later

**2. Build ultra-specific extraction prompts**

For education:
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

**3. Create geographic lookups early**
```python
municipality_to_county = {
    "Easton": "Talbot County",
    "Cambridge": "Dorchester County",
    "Chestertown": "Kent County"
}
```

**4. Split organizations into meaningful categories**
- Events (one-time occurrences)
- Initiatives (programs/policies)
- Establishments (physical places)
- Organizations (non-government entities)
- Bodies (government institutions)

**5. Run extraction (expect rate limits)**
- You will hit rate limits
- You will need multiple accounts or API keys
- Plan for this

**6. Manually validate samples**
- Check 20-30 stories per category
- Look for false positives and false negatives
- Adjust prompts based on failures

**7. Create standardization rules**
```python
# Standardize name formats
"Dr. Pepukayi" → "Sharon Pepukayi (Superintendent, Talbot County Public Schools)"

# Always use: Name (Title, Organization)
```

---

### Phase 3: External Data (Weeks 5-6)

**What data to get:**

**County level:**
- Population, poverty rate, median income
- Demographics (racial/ethnic breakdown)
- Broadband access (if relevant)

**District/jurisdiction level (education example):**
- Per-pupil spending (local vs. state)
- Number of schools by type
- Teacher count, student-teacher ratio
- Graduation rates

**Entity level (school/courthouse/building):**
- Enrollment or usage data
- Performance metrics (test scores, disposition rates, etc.)
- Demographics

**Where to get it:**
- U.S. Census Bureau (American Community Survey)
- State agencies (Department of Education, Courts, Housing)
- Local government websites (budgets, reports)

**How to structure it:**

Create summary books BEFORE generation:

**county_summary_book.json:**
```json
{
  "Talbot County": {
    "population": 37663,
    "median_income": 81667,
    "poverty_rate": 9.3,
    "total_enrollment": 4529,
    "per_pupil_spending": 19234,
    "key_officials": [
      {"name": "Sharon Pepukayi", "title": "Superintendent", "org": "Talbot County Public Schools"}
    ]
  }
}
```

**Budget Analysis Strategy:**

If you have massive budget documents:
1. Use ChatGPT to create comprehensive but succinct summary books
2. Structure: Core fiscal table, enrollment/spending, policy drivers, capital outlook, emerging issues, narrative summary
3. Include cross-jurisdiction comparison tables
4. This saves the LLM from processing 1000-page PDFs

---

### Phase 4: Generation (Week 7)

**The prompt structure that works:**

```python
prompt = f"""
You are writing a beat book for {beat} reporters.

COUNTY DATA:
{county_summary_book}

SCHOOL/ENTITY DATA:
{entity_summary_book}

STORIES ({len(stories)} total):
{story_texts}

Generate:
1. Three key issues for {region} overall
2. County-by-county section with recent coverage themes
3. Key sources (with titles, orgs, areas of expertise)
4. Key documents (by category, not by county)

Rules:
- Integrate data naturally with specific figures
- Cite which stories support claims (use Story ID numbers)
- Use format: Name (Title, Organization) for all people
- Do NOT include quotes (too error-prone)
- Do NOT include story ideas or investigation suggestions
- Write in narrative paragraphs for issues
- Use lists for sources and documents
"""
```

**Key principles:**

1. **Pass story data + external data + metadata together**
2. **Be specific about format** (saves editing later)
3. **Limit the rules** (10 max, not 30)
4. **Don't ask for quotes** (LLMs hallucinate them)
5. **Use Story IDs for citations** (easier to verify)

**Model recommendations:**
- Narrative generation: `groq/openai/gpt-oss-120b` or Claude
- Document summarization: ChatGPT (GPT-4)
- Structured extraction: `groq/meta-llama/llama-4-maverick-17b-128e-instruct`

---

### Phase 5: Fact-Checking

**What to check:**

✅ **Data from your summary books** (usually accurate)
- Demographics, test scores, budgets
- Verify spot-checks anyway

⚠️ **Data from story content** (90-95% accurate)
- Statistics mentioned in articles
- Dates and timelines
- Expect ~5% error rate

❌ **Quotes** (often wrong)
- Paraphrases presented as direct quotes
- Quotes from summaries, not original articles
- Invented quotes to fill gaps
- **Solution:** Don't include quotes in LLM-generated sections

**Fact-checking workflow:**
1. Check first complete section thoroughly
2. If error rate is <5%, spot-check others
3. If error rate is >5%, check everything
4. Always verify anything a reporter will rely on

---

### Phase 6: Interface (Week 8+)

**Two options:**

**Option 1: Narrative PDF/Markdown**
- Easier to build
- Works for smaller datasets
- Easy to share
- Hard to search/filter

**Option 2: Interactive Website**
- More useful for reporters
- Searchable and filterable
- Can embed visualizations
- Requires more technical skill

**If building interactive:**

**Architecture:**
- Single-page HTML with embedded JavaScript
- All data hard-coded in JS objects
- No backend/database needed
- Host on GitHub Pages (free)

**Essential features:**
- **Search AND filters** (don't make users choose)
- **County/jurisdiction color-coding** (visual consistency)
- **Result counts** ("Showing 23 of 175 stories")
- **Progressive disclosure** (summary → details on click)

**Useful additions:**
- Sortable tables
- Data visualizations (Chart.js)
- Story archive (formatted like email inbox)
- Source directory (searchable)
- Meeting calendar
- Simple chatbot (pattern-matching navigation helper)

**Data embedding strategy:**
```javascript
// Lightweight index (loads on page load)
const storyIndex = [
    {id: 1, title: "...", date: "...", county: "..."}
];

// Full text (loads on demand)
const storyDetails = {
    1: {content: "full story text here..."}
};
```

---

## Common Mistakes to Avoid

### Mistake 1: Starting with generation
Don't write prompts before you have clean data. Get metadata right first.

### Mistake 2: Trusting first-pass extraction
Single-pass extraction produces chaos. Always use multi-pass strategy.

### Mistake 3: Adding more instructions when output fails
If your 500-word prompt isn't working, a 1000-word prompt won't save it. Simplify or restructure the problem.

### Mistake 4: Trying to build everything at once
Build one component, test it, then add the next. Don't try to integrate budgets + stories + census + meeting minutes + officials simultaneously.

### Mistake 5: Assuming LLMs will "figure it out"
They won't. They need structure, constraints, examples, and verification.

### Mistake 6: Defining categories by exclusion
"All stories except X, Y, Z" fails. Use positive definitions: "Stories that focus on..."

### Mistake 7: Ignoring rate limits
Plan for them. Have multiple API accounts or switch models.

### Mistake 8: Not fact-checking early
Waiting until the end to discover quote hallucinations wastes time. Check a sample early.

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
- If you must include them, verify every single one

### 4. Multi-pass processing is required
Single-pass = chaos. Consistency emerges through constraint and repetition.

### 5. Narrow scope before scaling
One beat. One county. One type of story. Then expand.

### 6. Manual validation is essential
Always check samples. Expect 5-15% error rate. Fix it.

---

## Beat-Specific Guidance

### Education
- **Stories:** Board meetings, budget battles, test scores, superintendent changes
- **Entities:** Superintendents, board members, principals, schools, districts
- **External data:** Test scores (MCAP, SAT, etc.), enrollment, demographics, budgets, teacher counts, graduation rates, discipline data
- **Key questions:** What are scores? Who's the superintendent? What's the budget? How many students?

### Courts
- **Stories:** Major verdicts, sentencing, judicial appointments, precedent-setting cases
- **Entities:** Judges, attorneys, defendants, law firms, courthouses
- **External data:** Case volumes, disposition rates, sentencing patterns, docket statistics
- **Key questions:** Which judge? What's typical sentence? Who's the defense attorney? Case history?

### Local Government
- **Stories:** Budget votes, zoning decisions, council meetings, elections
- **Entities:** Council members, mayors, town managers, departments
- **External data:** Budgets, meeting minutes, voting records, census demographics
- **Key questions:** Who holds power? What's the budget? How do they vote? What's proposed?

### Housing
- **Stories:** Evictions, development approvals, tenant advocacy, code violations
- **Entities:** Landlords, tenant organizations, housing authorities, developers
- **External data:** Vacancy rates, median rents, eviction rates, violation records
- **Key questions:** Who owns this? What's the rent? What violations exist? Eviction rate?

### Environment
- **Stories:** Pollution incidents, conservation efforts, regulatory changes
- **Entities:** Agencies, advocacy groups, officials, regulated entities
- **External data:** Water quality, pollution levels, permit violations, cleanup progress
- **Key questions:** What's polluted? Who regulates? What's improving/declining?

---

## Tools & Technical Stack

**Python** (3.9+) for data processing

**LLM Access:**
- `llm` CLI tool (https://github.com/simonw/llm)
- Groq API (fast, free tier, rate limits)
- Anthropic API (Claude, paid, quality)
- OpenAI API (ChatGPT, paid, document summarization)

**Scrapers:**
- Python: BeautifulSoup, requests
- JavaScript: Puppeteer (for difficult interfaces like Microsoft Power BI)
- OCR: When scraping fails entirely

**Data Processing:**
- JSON for everything
- Datasette for exploration (optional)
- Manual validation in VS Code

**Website Building:**
- Single-page HTML with embedded JavaScript
- Chart.js for visualizations
- GitHub Pages for hosting (free)

**Version Control:**
- Git (use from day one)
- Don't use folders as versions

---

## Time & Cost Estimates

**Time invested:** ~100 hours over 4 months
- Data collection: 20 hours
- Entity extraction: 25 hours
- External data scraping: 30 hours
- Generation iteration: 15 hours
- Website building: 10 hours

**Money spent:**
- Groq: $0 (free tier)
- Claude: $0 (free tier with rate limits)
- OpenAI: ~$15
- **Total: $15**

**Ongoing maintenance:**
- ~3 hours quarterly for updates

---

## What Success Looks Like

**Usage signals:**
- Reporters visit weekly
- Average session > 5 minutes
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

## Final Principles

**Start small.** One beat. One county. One type of story.

**Expect failure.** Your first draft will have issues. That's normal.

**Fact-check ruthlessly.** LLMs make mistakes. Verify what matters.

**Ship when good enough.** Perfect is the enemy of useful.

**Iterate based on real use.** Get it in front of users and learn from their behavior.

---

*For the full story of how these lessons were learned through failures and iterations, see `beatbook_journey.md`*
