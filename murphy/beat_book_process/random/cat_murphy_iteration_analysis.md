# Cat Murphy: Beatbook Development Process - Technical Analysis

**Analyzed by:** Code Review
**Date:** December 16, 2025
**Scope:** Complete Python script analysis across all iteration directories

---

## Executive Summary

Cat Murphy developed a multi-stage pipeline for generating local government and education beatbooks from news archives. The work progressed through **three major phases:**

1. **Phase 1: Topic Classification & Entity Extraction** (stardem_topics, stardem_entities, stardem_topic_entities)
2. **Phase 2: Initial Beatbook Generation** (stardem_choice) 
3. **Phase 3: External Data Integration & Refinement** (stardem_draft → draft_v2 → draft_v3 → different → final)

Key findings:
- **Model evolution:** Started with Llama-4-scout → tested Groq-Kimi-k2 and Maverick → settled on GPT-OSS-120b
- **Field expansion:** Basic topics → comprehensive entity extraction → structured beatbook sections
- **Deduplication:** Minimal in early stages; later versions used Counter() to rank by frequency
- **External data:** Integrated Census data, MCAP scores, school data, election data in draft versions

---

## Phase 1: Topic Classification & Entity Extraction

### Directory: `murphy/stardem_topics/`

#### Script 1: `classify_topics_1.py`
**Model:** `groq/meta-llama/llama-4-scout-17b-16e-instruct`

**Fields Extracted:**
- `topic` (single classification)

**Prompt Structure:**
```
Assign this news story to exactly ONE topic from the following list:
- Local Government
- Economy & Budget
- Planning & Development
- Housing
- Transportation, Infrastructure & Public Works
- Public Safety & Crime
- Arts & Society
- Education
- Environment
- Community Outreach
- Elections
- Agriculture
- Sports
- Calendars
- Obituaries
- Legal Notices
- Columns & Editorials
- Other

Return only the topic name from the list above.
```

**Key Details:**
- Simple classification - one topic per story
- No deduplication logic
- Direct LLM call via subprocess
- Output: `topic` as string field

---

#### Script 2: `classify_topics_2.py`
**Model:** `groq-kimi-k2`

**What Changed:**
- Changed model from Llama-4-scout to Groq-Kimi-k2
- Added "Columns, Editorials & Letters to the Editor" (combined category)
- Same single-topic classification approach
- No other structural changes

**Fields Extracted:**
- `topic` (single classification)

---

#### Script 3: `classify_topics_3.py`
**Model:** `groq/meta-llama/llama-4-maverick-17b-128e-instruct`

**Major Evolution:**
- **Added content_type classification** (News, Sports, Calendars, Obituaries, Legal Notices, Opinion, Miscellaneous)
- **Added primary_topic and secondary_topic** (with max one secondary topic)
- Returns JSON object instead of single string
- Model changed to Maverick

**Fields Extracted:**
```json
{
  "content_type": "News|Sports|Calendars|Obituaries|Legal Notices|Opinion|Miscellaneous",
  "primary_topic": "Single topic from 13 categories",
  "secondary_topic": "One additional topic or None"
}
```

**Prompt Changes:**
- Required valid JSON output
- Provided examples in prompt
- "Only assign secondary_topic if story is VERY relevant to it"

**Deduplication/Consolidation:** None

---

#### Script 4: `classify_topics_4.py`
**Model:** `groq/meta-llama/llama-4-maverick-17b-128e-instruct`

**Major Change:**
- **Simplified to open-ended topic extraction**
- No predefined topic list - LLM generates 1-2 word broad topics
- Maintains consistency by passing `used_topics` set to LLM
- **First script to implement deduplication logic**

**Fields Extracted:**
- `primary_topic` (1-2 word broad topic, LLM-generated)

**Deduplication Logic:**
```python
used_topics = set()  # Track all topics used
if used_topics:
    topic_hint = f"Topics used so far: {', '.join(sorted(used_topics))}"
```

**Key Innovation:** Asked LLM to "use the same topic name for consistency" when similar stories appear

---

### Directory: `murphy/stardem_entities/`

#### Script 1: `stardem_entities_script_1.py`
**Model:** `groq/meta-llama/llama-4-scout-17b-16e-instruct`

**Fields Extracted:**
```json
{
  "content_type": "News|Sports|Calendars|Obituaries|Legal Notices|Opinion|Miscellaneous",
  "people": "Semicolon-separated list",
  "events": "Named events only (not generic activities)",
  "locations": "Physical places within municipalities",
  "municipalities": "Valid MD municipalities from predefined list",
  "county": "Derived from municipalities",
  "institutions": "Organizations, businesses, agencies, teams"
}
```

**Major Features:**
- **First entity extraction script**
- Comprehensive Maryland county/municipality mapping (24 counties, hundreds of municipalities)
- Post-processing: `fix_county_field()` and `clean_fields()` functions
- Validation: only allows real municipalities/counties from predefined lists
- **No topic field** - pure entity extraction

**Municipality Validation:**
```python
# Only allow real municipalities
municipalities = [m for m in municipalities if m in all_municipalities]

# Only allow real counties  
counties = [c for c in counties if c in all_counties]

# Remove municipalities/counties from locations field
locations = [l for l in locations if l not in all_municipalities and l not in all_counties]
```

**Deduplication:** None - just validation against lists

---

#### Script 2: `stardem_entities_script_2.py`
**Model:** `groq/openai/gpt-oss-120b`

**What Changed:**
- **Model switch:** Llama-4-scout → GPT-OSS-120b
- **Added topic field**
- **Added sources field**
- Expanded county list to ALL 24 Maryland counties (vs 5 Eastern Shore counties)

**Fields Added:**
```json
{
  "topic": "Single best topic from 10 categories",
  "sources": "Categories: government officials, politicians, residents, advocates, organizers, community leaders, coaches"
}
```

**New Topics:**
- Local Government & Politics (merged Elections into this)
- Economy & Budget
- Planning & Development
- Transportation, Infrastructure & Public Works
- Public Safety & Crime
- Arts & Culture (merged Community Outreach)
- Education
- Agriculture & Environment (merged two categories)
- Sports & Recreation
- Other

**Key Change:** Consolidated 18 topics down to 10 broader categories

---

#### Script 3: `stardem_entities_script_2_ish.py`
**Model:** `groq/meta-llama/llama-4-maverick-17b-128e-instruct`

**What Changed:**
- Model: GPT-OSS-120b → Llama-4-maverick
- Same fields and structure as script_2
- Likely a testing variation

---

#### Utility Script: `convert_to_arrays.py`

**Purpose:** Post-processing utility
**No LLM calls**

**Function:**
- Converts semicolon-separated string fields to JSON arrays
- Processes: people, sources, events, locations, municipalities, county, institutions
- Handles "N/A" and empty strings → converts to `[]`

```python
# Example transformation
"people": "John Doe; Jane Smith" → "people": ["John Doe", "Jane Smith"]
"municipalities": "N/A" → "municipalities": []
```

---

### Directory: `murphy/stardem_topic_entities/`

#### Script: `add_entities.py`
**Model:** `groq/openai/gpt-oss-120b`

**Purpose:** Combined topic + entity extraction (same as stardem_entities_script_2.py)
- Identical to `stardem_entities_script_2.py`
- Likely a consolidated version moved to this directory

---

#### Script: `education_script_v1.py`
**Model:** `groq/openai/gpt-oss-120b`

**Major Innovation:** **First education-specific script**

**Fields Extracted:**
```json
{
  "content_type": "News|Calendars|Obituaries|Legal Notices|Opinion|Miscellaneous",
  "regions": ["Maryland", "Virginia", "D.C.", "U.S.", etc.],
  "municipalities": ["MD municipalities"],
  "counties": ["Must include 'County' suffix"],
  "key_people": ["Up to 4 education people with titles"],
  "key_locations": ["School-related locations only"],
  "key_events": ["Named education events"],
  "key_initiatives": ["Named programs like 'Blueprint for Maryland's Future'"],
  "key_establishments": ["MD schools, colleges, education centers"],
  "key_organizations": ["Education nonprofits, PTOs"],
  "key_bodies": ["School boards, boards of education"]
}
```

**Massive Prompt Engineering:**
- **Highly specific exclusion rules**
- "ONLY include superintendents, principals, teachers, education board members"
- "DO NOT include mayors, commissioners, general politicians"
- "ONLY include named initiatives like 'Blueprint for Maryland's Future'"
- "DO NOT include general course types like 'AP' or 'CTE'"
- Standardization rules: "4-H" not "4H"
- Avoids local 4-H clubs mentioned in historical context

**Critical Rules:**
```
CRITICAL: ALL entities must be EXPLICITLY education-related. This is an education beat book.
```

**Batch Processing:**
- `--batch-size` parameter (default 10)
- Progress saving after each batch
- Resume capability
- `--continuous` mode for full processing
- `--dry-run` for testing

**No Deduplication:** Extracts per-story entities

---

## Phase 2: Initial Beatbook Generation

### Directory: `murphy/stardem_choice/`

#### Script: `generate_beatbook_v1.py`
**Model:** `groq/openai/gpt-oss-120b`

**Purpose:** First attempt at generating narrative beatbook sections

**Input Data:**
- File: `selected_processed_education_stories.json`
- Stories already have entity metadata

**Entity Aggregation Logic:**
```python
def extract_entities(stories):
    counters = {
        "people": Counter(),
        "organizations": Counter(),
        "initiatives": Counter(),
        "events": Counter(),
        "establishments": Counter(),
        "municipalities": Counter(),
        "regions": Counter(),
    }
    
    for s in stories:
        if s.get("llm_failed", False) is True:
            continue  # Skip failed stories
        
        for p in s.get("key_people", []):
            counters["people"][p] += 1
        # ... repeat for all entity types
    
    def top(counter):
        return [x for x, _ in counter.most_common(10)] or ["None found"]
```

**First Deduplication:** Uses `Counter()` to rank entities by frequency, returns top 10

**Sections Generated:**
1. **Top Three Issues** (H3 headings, 3-4 paragraphs narrative, NO bullets)
2. **Key Sources to Know** (H4 headings + bullets allowed)

**Prompts:**
- Provided metadata + sample titles + **FULL STORY CONTENT** (main evidence)
- "Base your assessment primarily on the full story content"
- Output format: Markdown with specific heading levels

**Output:** `education_beatbook_draft_v1.md`

---

#### Script: `generate_beatbook_v2.py`
**Model:** `groq/qwen/qwen3-32b`

**What Changed:**
- **Model:** GPT-OSS-120b → Qwen3-32b
- **Removed full story content** - only uses titles and metadata
- **Added `<think>` tag stripping**
- Simplified "Top Issues" section to **max 3 paragraphs** (was 3-4)
- Removed "Why This Matters" subsection from Key Sources

**Key Simplifications:**
```python
def run_llm(prompt: str) -> str:
    output = result.stdout.decode("utf-8")
    # Strip out <think>...</think> content
    output = re.sub(r'<think>.*?</think>', '', output, flags=re.DOTALL)
    return output.strip()
```

**Rationale:** Reduce prompt size and processing time by not sending full content

---

#### Script: `generate_beatbook_v3.py`
**Model:** `groq/openai/gpt-oss-120b` (back to GPT-OSS)

**What Changed:**
- Model: Qwen3-32b → back to GPT-OSS-120b
- **Added date filtering:** Separates recent (Nov 2024+) vs historical stories
- **Added story summaries** to prompt
- Prioritizes recent coverage for issue identification

**New Feature - Date Partitioning:**
```python
RECENT_CUTOFF = "2024-11-01"

def partition_stories_by_date(stories):
    recent = []
    historical = []
    
    for story in stories:
        date_str = story.get("date", "")
        if date_str >= RECENT_CUTOFF:
            recent.append(story)
        else:
            historical.append(story)
    
    return recent, historical
```

**Enhanced Titles Format:**
```python
def format_titles_with_summaries(stories, limit=20):
    for s in stories[:limit]:
        if summary:
            formatted.append(f"- [{date}] {title}\n  Summary: {summary}")
```

**Prompt Changes:**
```
**PRIORITIZE RECENT COVERAGE (Nov 2024 forward)** - These stories should drive your issue selection.
Use historical stories (before Nov 2024) only as context to understand how issues have developed.
```

---

## Phase 3: External Data Integration

### Directory: `murphy/stardem_draft/`

#### Script: `generate_comprehensive_beatbook.py`
**Model:** `groq/openai/gpt-oss-120b`

**MAJOR EVOLUTION:** First script to integrate external data sources

**Input Files:**
1. `refined_beat_book_stories.json` (story data)
2. `COUNTY_SUMMARY_BOOK.md` (external demographic/performance data)

**New Data Integration:**
```python
def parse_county_data(md_file: str) -> dict:
    """Parse COUNTY_SUMMARY_BOOK.md to extract county-specific data"""
    # Splits by ## headers (county sections)
    # Returns dict mapping county name to markdown section
```

**New Sections Generated:**
1. **County Overview & Context** (synthesizes demographics + story coverage)
2. **Top Three Issues** (grounded in both stories AND performance data)
3. **Key Sources to Know** (includes county leadership from external data)
4. **Recent Coverage Themes** (narrative synthesis of story patterns)
5. **Key Documents, Records & Websites** (consolidated across all counties)

**Enhanced Prompts:**
```
County Data:
{county_data_section}

Story Coverage Insights:
- Total stories analyzed: {story_count}
- Key People mentioned: {entities['top_people'][:10]}
...

Write a comprehensive overview section that helps a new reporter understand {county}'s education landscape.
```

**Prompt Instructions Evolution:**
- "Highlight notable patterns (e.g., achievement gaps, resource challenges)"
- "Use data from the county section to ground your observations"
- "Reference specific stories by title to illustrate key issues"
- "Include a 'Quick Facts' subsection with key numbers in bullet form"

**Output Structure:**
- Table of Contents
- One section per county
- Consolidated documents section at end

---

### Directory: `murphy/stardem_draft_v2/beatbook_drafts/`

#### Script: `generate_beatbook_v3_enhanced.py`
**Model:** `groq/meta-llama/llama-4-maverick-17b-128e-instruct`

**What Changed:**
- Model: GPT-OSS-120b → Llama-4-maverick
- **Changed data format:** Markdown → JSON for county/school data
- **Added school-level data** (new input file)
- **Added Blueprint summaries** (markdown file)
- **Added retry logic** with timeouts

**Input Files:**
1. `refined_beatbook_stories.json`
2. `county_summary_book_v2.json` (was .md, now .json)
3. `school_summary_book_v2.json` (NEW)
4. `blueprint_summaries.md` (NEW)

**New Parsing Functions:**
```python
def parse_county_data(json_file: str) -> dict:
    """Parse county JSON - county names as top-level keys"""

def parse_school_data(json_file: str) -> dict:
    """Parse school JSON - returns dict mapping county to list of schools"""

def parse_blueprint_data(md_file: str) -> str:
    """Parse Blueprint markdown"""
```

**Enhanced Retry Logic:**
```python
def run_llm(prompt: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        try:
            result = subprocess.run(..., timeout=120)  # 2 minute timeout
            # Handle timeouts and errors
            time.sleep(5)  # Wait between retries
```

**Data Formatting:**
```python
def format_county_data(county_name: str, county_entry: dict) -> str:
    """Convert county JSON to readable text with bulleted MCAP data"""
    # Changed from semicolon-separated to bulleted lists
```

**Key Enhancement:** More structured data inputs allow better prompt engineering

---

### Directory: `murphy/stardem_draft_v3/`

#### Script: `generate_beatbook_v1.py` (Local Government)
**Model:** `groq/openai/gpt-oss-120b`

**MAJOR SHIFT:** Education → Local Government beatbook

**Input Files (per county):**
- `{county}_census.json` (Census Bureau 2024 data)
- `{county}_county_officials.json`
- `{county}_municipal_officials.json`
- `{county}_municipalities_census.json`
- `{county}_elections.json`
- `{county}_school_data.json`
- `{county}_mcap_scores.json`
- `{county}_board_meetings.json`
- `{county}_budget_data.json`

**Story Analysis:**
```python
def extract_story_insights(stories: list, county_filter: str = None) -> dict:
    """Extract key insights from stories for a specific county"""
    # Count stories by topic tags
    topic_counter = Counter()
    for story in filtered_stories:
        topic = story.get("beatbook_tag", "Other")
        topic_counter[topic] += 1
    
    return {
        "total_stories": len(filtered_stories),
        "date_range": date_range,
        "top_topics": topic_counter.most_common(10),
        "sample_stories": filtered_stories[:15]
    }
```

**Data Formatting:**
```python
def format_county_data_section(county: str, ...) -> str:
    """Format comprehensive data section including:
    1. Census data (JSON)
    2. County officials (JSON)
    3. Municipal officials (JSON)
    4. Elections data (JSON)
    5. School data (JSON)
    6. MCAP scores (JSON)
    7. Board meetings analysis
    8. Budget data (JSON)
    """
```

**Huge Prompts:** Entire data packages embedded as JSON in prompts (~190K tokens)

---

#### Script: `generate_beatbook_v5.py` (Local Government - Optimized)
**Model:** `groq/openai/gpt-oss-120b`

**MAJOR OPTIMIZATION:** "Pre-digest all data into narrative fact blocks (no raw JSON in prompt)"

**Key Innovation:**
```python
def build_county_facts_block(county: str) -> str:
    """Build a clean facts block from county data"""
    
    census_api = census_data.get("census_api_data", {})
    pop_data = census_api.get("population", {})
    
    facts = f"""
## VERIFIED FACTS: {county_name.upper()}

### Demographics (U.S. Census Bureau, 2025)
- **Total Population**: {pop_data.get('total', 'N/A'):,}
- **Median Age**: {pop_data.get('median_age', 'N/A')}
- **Racial Composition**: 
  - White: {race_data.get('white_alone', 'N/A'):,} ({pct:.1f}%)
...
"""
```

**Prompt Size Reduction:** ~190K tokens → ~20K tokens

**Processing Strategy:**
- "Generate iteratively: one county at a time, one section at a time"
- "Pre-build Key Sources tables before LLM sees them"
- "Specific, measurable requirements for each section"
- "Immediate validation and error catching"

**Output:** `beatbook_v5.md`

---

### Directory: `murphy/stardem_different/`

**Note:** This directory contains website building scripts and data processing utilities
- `generate_beatbook_profiles.py` - Uses both `gpt-oss-120b` and `llama-3.3-70b-versatile`
- Focus on extracting quotes, filtering by relevance and recency
- Demographic data processing scripts
- No major new LLM techniques - mostly data transformation

---

### Directory: `murphy/stardem_final/`

**Note:** Primarily data scraping and processing scripts
- Web scraping for MCAP scores, graduation rates
- CSV downloads and data aggregation
- Manual inspection utilities
- `generate_narrative_beatbook.py` - Uses `groq/openai/gpt-oss-120b`

---

## Summary: Model Evolution

### Topic Classification Models
1. `groq/meta-llama/llama-4-scout-17b-16e-instruct` (classify_topics_1)
2. `groq-kimi-k2` (classify_topics_2)
3. `groq/meta-llama/llama-4-maverick-17b-128e-instruct` (classify_topics_3, 4)

### Entity Extraction Models
1. `groq/meta-llama/llama-4-scout-17b-16e-instruct` (entities_1)
2. `groq/openai/gpt-oss-120b` (entities_2, became the standard)
3. `groq/meta-llama/llama-4-maverick-17b-128e-instruct` (entities_2_ish, testing)

### Beatbook Generation Models
1. `groq/openai/gpt-oss-120b` (v1, v3, most draft versions) **← Primary Model**
2. `groq/qwen/qwen3-32b` (v2, brief experiment)
3. `groq/meta-llama/llama-4-maverick-17b-128e-instruct` (draft_v2_enhanced)
4. `groq/llama-3.3-70b-versatile` (stardem_different profiles)

**Final Model Choice:** `groq/openai/gpt-oss-120b` for most production work

---

## Summary: Field Evolution

### Phase 1 - Basic Classification
- `topic` (single string)

### Phase 2 - Multi-Field Classification  
- `content_type`, `primary_topic`, `secondary_topic`

### Phase 3 - Entity Extraction
- `people`, `events`, `locations`, `municipalities`, `county`, `institutions`
- Added `sources` category field

### Phase 4 - Education-Specific Extraction
- `regions`, `key_people`, `key_locations`, `key_events`, `key_initiatives`
- `key_establishments`, `key_organizations`, `key_bodies`
- Highly restrictive rules for education relevance

### Phase 5 - Beatbook Sections
- Aggregated entities using `Counter()` to get top 10-15 by frequency
- Generated narrative sections with specific formatting rules
- Integrated external data sources

---

## Summary: Deduplication & Consolidation Logic

### Early Scripts (Topics 1-3)
- **No deduplication** - each story classified independently
- Direct string output from LLM

### classify_topics_4.py
- **First deduplication:** Maintains `used_topics` set
- Passes previously used topics to LLM in prompt
- Asks LLM to reuse topic names for consistency

### Entity Scripts
- **Validation not deduplication:** Checks against predefined municipality/county lists
- Post-processing: `clean_fields()` and `fix_county_field()`
- Removes duplicates within a story (e.g., `sorted(set(municipalities))`)

### Beatbook Generation
- **Frequency-based ranking:** 
  ```python
  Counter() to count entity occurrences across stories
  .most_common(10) to get top entities
  ```
- Aggregates across all stories for a county/beat
- Returns ranked lists to LLM for context

### No Global Deduplication
- Entities not normalized across entire dataset
- "John Smith (Superintendent)" vs "John Smith" could be separate
- Relied on LLM to standardize names within prompts

---

## Summary: Key Prompt Engineering Patterns

### 1. Progressive Specificity
- Started: "Return only the topic name"
- Evolved to: Multi-page instructions with exclusion rules

### 2. Example-Based Learning
- Early: No examples
- Later: "e.g., 'Blueprint for Maryland's Future' YES, 'AP courses' NO"

### 3. Format Enforcement
- Started: String output
- Evolved to: "Return ONLY valid JSON with these exact field names"

### 4. Error Prevention
- "CRITICAL: ALL entities must be EXPLICITLY education-related"
- "DO NOT include: mayors, commissioners..." (explicit exclusions)
- "When in doubt, EXCLUDE the entity"

### 5. Context Management
- v1: Full story content (very large prompts)
- v2: Only titles and metadata (reduced size)
- v3: Summaries + titles (balanced approach)
- v5: Pre-digested fact blocks (optimized)

### 6. Output Formatting
- Markdown structure with specific heading levels (H3, H4)
- Bullet vs. narrative specifications
- Length constraints ("max 3 paragraphs")

---

## Key Insights from Code Analysis

1. **Model Selection Stabilized:** Tried 5+ models, settled on GPT-OSS-120b for reliability
2. **Prompt Engineering Dominated:** Most iteration was refining instructions, not changing models
3. **Data Integration Evolved:** Stories alone → + external data → pre-processed data
4. **Minimal Traditional NLP:** No spaCy, no vector embeddings - pure prompt engineering
5. **Counter() = Primary Dedup:** Simple frequency counting for entity ranking
6. **Retry Logic Added Late:** Error handling improved in later versions
7. **Batch Processing Important:** Large datasets required progress saving and resume capability
8. **Education → Local Gov Shift:** Reused same pipeline architecture for different beats

---

## Technical Debt & Limitations Observed

1. **No Entity Normalization:** "Talbot County Public Schools" vs "TCPS" could be separate
2. **No Cross-Story Linking:** Each story processed independently
3. **LLM Dependency:** No fallback if model fails or changes API
4. **Prompt Size Limitations:** Had to reduce from full content to summaries
5. **Inconsistent Validation:** Some scripts validate municipalities, others don't
6. **Manual Curation Still Needed:** Scripts produce drafts requiring editing

---

## Files Generated (Outputs)

### Topic Classification
- `stardem_topics_classified_1.json`
- `stardem_topics_classified_2.json`  
- `stardem_topics_classified_5.json`
- `stardem_topics_classified_4.json`

### Entity Extraction
- `stories_with_entities_1.json`
- `stories_with_entities_2.json`
- `stories_with_entities_2_ish.json`
- `education_stories_with_entities.json`

### Beatbooks
- `education_beatbook_draft_v1.md`
- `education_beatbook_draft_v2.md`
- `education_beatbook_draft_v3.md`
- `comprehensive_education_beatbook_v2.md`
- `comprehensive_education_beatbook_v3_enhanced.md`
- `beatbook_v5.md` (local government)

---

## Conclusion

Cat Murphy's work demonstrates a **systematic, iterative approach to LLM-based document generation:**

1. **Start simple** (single topic classification)
2. **Add complexity incrementally** (multi-field extraction)
3. **Test multiple models** (5+ tried)
4. **Settle on reliable choice** (GPT-OSS-120b)
5. **Enhance with external data** (Census, education metrics)
6. **Optimize for performance** (prompt engineering > model swapping)
7. **Build reusable pipelines** (education → local government)

The codebase shows **strong software engineering practices:**
- Progress saving and resume capability
- Retry logic with exponential backoff
- Validation against known entity lists
- Separation of concerns (topic → entities → beatbook)
- Comprehensive error handling in later versions

**Most important finding:** Success came from **prompt refinement and data preparation**, not from finding the "perfect" model. The GPT-OSS-120b model used in v1 remained the standard through final versions - what changed was **how data was presented** to the model.
