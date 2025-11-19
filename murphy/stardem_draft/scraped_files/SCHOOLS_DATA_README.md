# Maryland School Data Scraper

This directory contains a web scraping tool that collects school data from the Maryland State Department of Education Report Card website for five counties.

## Counties Covered
- **Talbot County** (8 schools)
- **Kent County** (5 schools)
- **Dorchester County** (13 schools)
- **Caroline County** (10 schools)
- **Queen Anne's County** (14 schools)

**Total: 50 schools**

## Files Generated

### Data Files
- **`schools_list.json`** - List of all 50 schools with names, URLs, and county assignments
- **`schools_detailed.json`** - Detailed information for each school including page content
- **`schools_data.csv`** - All school data in CSV format for easy analysis in Excel or other tools

### Documentation
- **`page_source_Talbot.html`** - Saved HTML source for reference
- **`screenshot_Talbot.png`** - Screenshot of the school selection page
- **`screenshots/`** - Directory containing 50 individual school page screenshots

## Scripts

### Main Scraper (Recommended)
**`get_school_data_playwright.py`**
- Uses Playwright for JavaScript-rendered content
- Collects school names, URLs, and page content
- Takes screenshots of each school page
- Works in headless mode (no visible browser)

### Alternative Scrapers
- **`get_school_data.py`** - Basic requests/BeautifulSoup scraper (doesn't handle JavaScript)
- **`get_school_data_selenium.py`** - Selenium-based scraper (requires Chrome installation)

## Running the Scraper

### Prerequisites
```bash
pip install playwright beautifulsoup4 pandas
python -m playwright install chromium
sudo python -m playwright install-deps chromium
```

### Execute
```bash
python get_school_data_playwright.py
```

## Data Source
Maryland State Department of Education Report Card
- Main URL: https://reportcard.msde.maryland.gov/SchoolsList/
- School detail pages: https://reportcard.msde.maryland.gov/Graphs/#/ReportCards/ReportCardSchool/...

## School Breakdown by County

### Talbot County (8 schools)
- Elementary: Chapel District, Easton, St. Michaels, Tilghman, White Marsh
- Middle: Easton Middle, St. Michaels Middle/High
- High: Easton High

### Kent County (5 schools)
- Elementary: Galena, H.H. Garnett, Rock Hall
- Middle: Kent County Middle
- High: Kent County High

### Dorchester County (13 schools)
- Elementary: Choptank, Hurlock, Maple, Sandy Hill, Vienna, Warwick
- K-8: South Dorchester
- Middle: Mace's Lane, North Dorchester Middle
- High: Cambridge-South Dorchester, North Dorchester High
- Career/Tech: Dorchester County Career and Technology Center
- Early Childhood: Judith P. Hoyer Early Childhood Center

### Caroline County (10 schools)
- Elementary: Denton, Federalsburg, Greensboro, Preston, Ridgely
- Middle: Colonel Richardson Middle, Lockerman Middle
- High: Colonel Richardson High, North Caroline High
- Career/Tech: Caroline Career & Technology Center

### Queen Anne's County (14 schools)
- Elementary: Bayside, Centreville, Church Hill, Grasonville, Kennard, Kent Island, Matapeake, Sudlersville
- Middle: Centreville Middle, Matapeake Middle, Stevensville Middle, Sudlersville Middle
- High: Kent Island High, Queen Anne's County High

## Next Steps

The scraper currently collects basic information. To extract more detailed data from each school page:

1. **Enrollment Data** - Student counts by grade level
2. **Demographics** - Race/ethnicity, economic status
3. **Performance Metrics** - Test scores, graduation rates
4. **Staff Information** - Teacher counts, qualifications
5. **Programs** - Special education, gifted, athletics

You can enhance the `get_school_details()` function in the scraper to extract specific data points by:
- Looking for specific CSS selectors or text patterns
- Parsing tables and charts
- Extracting numerical data from the JavaScript-rendered content

## Notes

- The website uses JavaScript to load content dynamically, which is why Playwright (not basic HTTP requests) is needed
- Each school has a unique URL pattern: `/Graphs/#/ReportCards/ReportCardSchool/1/{level}/1/{county_code}/{school_code}/0`
- Screenshots are saved in full-page mode for reference
- The scraper includes polite delays (0.5s between requests) to avoid overwhelming the server
