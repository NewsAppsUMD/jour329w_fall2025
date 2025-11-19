# Eastern Shore Education Data - Summary Book

This directory contains comprehensive education data for **5 Maryland Eastern Shore counties**: Talbot, Kent, Dorchester, Caroline, and Queen Anne's.

## 📊 Summary Files (Main Directory)

### `COUNTY_SUMMARY_BOOK.md`
**Human-readable markdown report** with complete analysis for each county including:
- Demographics & economics
- District leadership (superintendents & board members)
- Board meeting schedules
- Academic performance (MCAP scores)
- Individual school profiles

### `county_summary_book.json`
**Machine-readable JSON** with the same data in structured format for analysis/visualization.

---

## 📁 Folder Organization

### `scraped_files/` (23 files)
All raw data collected from various sources:
- School lists and enhanced data
- MCAP test scores (aggregate and grade-level)
- District officials and board members
- Census/demographic data
- Board meeting schedules
- Superintendent and principal contact information

### `scrapers/` (35 files)
All Python scripts used to collect the data:
- Playwright-based web scrapers
- Data extraction and processing scripts
- Analysis and summary generation tools

---

## 🎯 Key Data Points

### Schools
- **50 schools** total across 5 counties
- **45 schools** with complete MCAP data
- Elementary (27), Middle (11), High (9), Career/Tech (3)

### MCAP Performance (Highest Grades)
- **Grade 5** for elementary schools
- **Grade 8** for middle schools  
- **Grade 10** for high schools

**Regional Average Proficiency:**
- ELA: 45.0%
- Math: 18.8%
- Science: 27.6%

### District Leadership
- 5 superintendents identified
- 27 board members total
- Complete meeting schedules for all districts

### Census Data (All 5 Counties)
- Total population: 173,434
- School-age population (5-17 years)
- Poverty rates
- Median household income
- Broadband access rates
- Education attainment levels

---

## 📈 County Rankings by Academic Performance

1. **Queen Anne's County** - 38.9% average (highest)
2. **Caroline County** - 29.3% average
3. **Talbot County** - 31.6% average
4. **Kent County** - 25.6% average
5. **Dorchester County** - 23.7% average

---

## 🔍 How to Use This Data

### For Journalism
- Compare school performance across counties
- Analyze relationship between poverty rates and test scores
- Contact district officials for interviews
- Attend board meetings (schedules provided)

### For Research
- Load `county_summary_book.json` into Python/R/Excel
- Cross-reference census data with academic performance
- Analyze demographic patterns and educational outcomes

### For Data Visualization
- Use JSON data for interactive dashboards
- Create county comparison charts
- Map school performance geographically

---

## 📅 Data Collection Date

**November 2025**

---

## 🌐 Data Sources

1. **Maryland State Department of Education Report Card**  
   `reportcard.msde.maryland.gov`
   - School star ratings and percentile ranks
   - MCAP test scores (2024-2025 school year)

2. **U.S. Census Bureau American Community Survey**  
   - Population and demographic data
   - Economic indicators
   - Education attainment

3. **County School District Websites**  
   - Superintendent contact information
   - School principal listings
   - District leadership structure

4. **BoardDocs**  
   `go.boarddocs.com/mabe/`
   - Board of Education members
   - Meeting schedules and agendas
   - Election/appointment dates

---

## 📧 Contact Information Available

The data includes contact information for:
- All 5 county superintendents (email, phone)
- All school principals (50 schools)
- Board of Education office locations and phone numbers

---

## ⚠️ Data Notes

- MCAP scores represent **proficiency rates** (Performance Levels 3 & 4 combined)
- 5 schools excluded from MCAP analysis (career/technical centers without standard grade testing)
- Some schools have data gaps due to suppression rules (small sample sizes)
- Census data from most recent American Community Survey estimates

---

## 🛠️ Technical Details

### Scraping Methods
- **Playwright** for JavaScript-rendered pages (Maryland Report Card)
- **BeautifulSoup4** for HTML parsing
- **Asyncio** for efficient concurrent scraping
- Headless Chromium browser automation

### Data Processing
- Python 3.12+
- Pandas for CSV operations
- JSON for structured data storage

### Success Rates
- School basic data: 50/50 (100%)
- Star ratings: 45/50 (90%)
- MCAP grade-level scores: 345/369 attempts (93.5%)
- District officials: 5/5 counties (100%)

---

## 📝 File Naming Convention

- `schools_*.json/csv` - School-related data
- `mcap_*.json/csv` - MCAP test scores
- `district_*.json` - District leadership
- `board_*.json` - Board of Education data
- `census_*.json` - Demographic/census data

---

## 🎓 Research Questions This Data Can Answer

1. How does poverty rate correlate with school performance?
2. Which counties have the largest achievement gaps?
3. Do schools with higher broadband access perform better?
4. How do rural vs. suburban districts compare?
5. What is the relationship between education attainment of adults and student performance?
6. Which schools are improving or declining over time?
7. How accessible are board meetings to the public?

---

*For questions about this data or to report issues, refer to the scraper scripts in the `scrapers/` directory for documentation.*
