# Eastern Shore Education Beatbook

A comprehensive news app beatbook for education coverage across Maryland's Eastern Shore counties.

## Generated
December 07, 2025 at 03:34 AM

## Features

- **Overview Dashboard**: Visual charts showing enrollment, budgets, and per-pupil spending
- **County Profiles**: Detailed fiscal and demographic information for each county
- **Recent Stories**: Searchable archive of education news stories with filtering
- **Key Sources**: Profiles of education leaders with quote counts and topic expertise
- **Quote Database**: Searchable database of thousands of quotes from officials

## Counties Covered

- Caroline County
- Dorchester County
- Kent County
- Queen Anne's County
- Talbot County

## Data Sources

This beatbook is built from the following master data files:

- `budget.json` - County fiscal data and budget analysis
- `beatbook_profiles.json` - Profiles of key education sources
- `master_quotes.json` - Database of quotes from officials
- `refined_beatbook_stories.json` - Curated news stories
- County-specific student data files for all five counties

## Usage

Open `index.html` in a web browser to view the beatbook. All data is embedded in the application,
so no server is required.

## Technology

- HTML5, CSS3, JavaScript
- Chart.js for data visualization
- Responsive design for mobile and desktop
- No external dependencies beyond Chart.js CDN

## Generator

This beatbook was generated using `generate_beatbook.py`, a Python script that processes
master data files and creates a standalone web application.
