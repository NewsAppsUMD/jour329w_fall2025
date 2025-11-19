# 🎓 Maryland School Data Collection - Complete Guide

## 📊 What Was Collected

Successfully scraped data for **50 schools** across **5 Maryland counties**:
- **Talbot County**: 8 schools
- **Kent County**: 5 schools  
- **Dorchester County**: 13 schools
- **Caroline County**: 10 schools
- **Queen Anne's County**: 14 schools

## 📁 Files Generated

### Basic Data (Already Collected)
1. **`schools_list.json`** - All 50 schools with names, URLs, and counties
2. **`schools_detailed.json`** - Page content for each school
3. **`schools_data.csv`** - Basic data in CSV format
4. **`screenshots/`** - 50 full-page screenshots of school pages

### Enhanced Data (Optional - Can Extract)
5. **`schools_enhanced_data.json`** - Star ratings, percentile ranks, demographics, test scores
6. **`schools_enhanced_data.csv`** - Enhanced data in CSV format

## 🚀 How to Use

### View the Basic Data (Already Done!)
```bash
# View the schools list
cat schools_list.json

# Open CSV in Excel/Sheets
# Download schools_data.csv and open in your spreadsheet app

# View screenshots
ls screenshots/
```

### Extract More Detailed Data (Optional)
```bash
# Run enhanced extraction for all 50 schools (takes ~5-10 minutes)
./run_enhanced_extraction.sh

# Or manually:
python extract_detailed_data.py

# Test on just 3 schools first:
python extract_detailed_data.py 3
```

## 📈 What Data Is Available

### Basic Information (Already Collected)
- School name and ID code
- County
- School type (Elementary, Middle, High)
- Direct URL to report card
- Full page content
- Screenshots

### Enhanced Information (Can Extract with `extract_detailed_data.py`)
- **Star Rating** (1-5 stars)
- **Percentile Rank** (0-100)
- **Total Enrollment**
- **Demographics**:
  - Race/ethnicity breakdown
  - Economically disadvantaged %
  - Special education %
  - English learners %
- **MCAP Test Scores** (Maryland Comprehensive Assessment Program)
- **Attendance rates**
- **Educator qualifications**
- **Per-pupil expenditures**

## 🛠️ Technical Details

### Scripts
1. **`get_school_data_playwright.py`** - Main scraper (uses Playwright)
2. **`extract_detailed_data.py`** - Enhanced data extractor
3. **`run_enhanced_extraction.sh`** - Convenience script to run extraction

### Dependencies
```bash
pip install playwright beautifulsoup4 pandas
python -m playwright install chromium
sudo python -m playwright install-deps chromium
```

### Data Source
Maryland State Department of Education Report Card
- Website: https://reportcard.msde.maryland.gov/SchoolsList/
- Each school has unique URL pattern: `/Graphs/#/ReportCards/ReportCardSchool/...`

## 📊 Sample Data Analysis Ideas

### With Basic Data
- Map all schools by county
- Count schools by type (Elementary, Middle, High)
- Create directory of school websites

### With Enhanced Data
- Compare star ratings across counties
- Analyze enrollment sizes
- Study demographic patterns
- Compare test scores (MCAP)
- Identify high-performing schools
- Analyze achievement gaps

## 🔍 Example: Loading Data in Python

```python
import json
import pandas as pd

# Load basic school list
with open('schools_list.json', 'r') as f:
    schools = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(schools)
print(df.groupby('county').size())

# Load enhanced data (if extracted)
with open('schools_enhanced_data.json', 'r') as f:
    enhanced = json.load(f)

df_enhanced = pd.DataFrame(enhanced)
print(df_enhanced[['school_name', 'star_rating', 'percentile_rank']].head())
```

## 📝 School Breakdown by County

### Talbot County (8 schools)
**Elementary:** Chapel District, Easton, St. Michaels, Tilghman, White Marsh  
**Middle:** Easton Middle, St. Michaels Middle/High  
**High:** Easton High

### Kent County (5 schools)
**Elementary:** Galena, H.H. Garnett, Rock Hall  
**Middle:** Kent County Middle  
**High:** Kent County High

### Dorchester County (13 schools)
**Elementary:** Choptank, Hurlock, Maple, Sandy Hill, Vienna, Warwick  
**K-8:** South Dorchester  
**Middle:** Mace's Lane, North Dorchester Middle  
**High:** Cambridge-South Dorchester, North Dorchester High  
**Career/Tech:** Career and Technology Center  
**Early Childhood:** Judith P. Hoyer Early Childhood Center

### Caroline County (10 schools)
**Elementary:** Denton, Federalsburg, Greensboro, Preston, Ridgely  
**Middle:** Colonel Richardson Middle, Lockerman Middle  
**High:** Colonel Richardson High, North Caroline High  
**Career/Tech:** Career & Technology Center

### Queen Anne's County (14 schools)
**Elementary:** Bayside, Centreville, Church Hill, Grasonville, Kennard, Kent Island, Matapeake, Sudlersville  
**Middle:** Centreville Middle, Matapeake Middle, Stevensville Middle, Sudlersville Middle  
**High:** Kent Island High, Queen Anne's County High

## 🎯 Next Steps

1. **Analyze the basic data** - Already collected and ready to use
2. **Extract enhanced data** (optional) - Run `./run_enhanced_extraction.sh`
3. **Create visualizations** - Use Excel, Python, Tableau, etc.
4. **Compare across counties** - Look for patterns and insights
5. **Track over time** - Re-run scraper periodically for trend analysis

## 💡 Tips

- The Maryland Report Card website updates annually (usually in fall)
- Star ratings are relative within school level (Elementary, Middle, High)
- Percentile ranks compare schools of the same level statewide
- Some data may be suppressed for privacy (small student groups)
- Screenshots are useful for visual reference when interpreting data

## 📧 Questions?

See `SCHOOLS_DATA_README.md` for more technical details about the scraping process.

---
**Data Source:** Maryland State Department of Education  
**Collection Date:** November 2025  
**Total Schools:** 50 across 5 counties
