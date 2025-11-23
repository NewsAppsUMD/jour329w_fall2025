# Eastern Shore Education Data Summary

## Data Collected

### 1. Suspension Data (2023-2024 School Year)
**Source**: Maryland State Department of Education official PDFs

**Files**:
- `eastern_shore_suspensions_2023_2024.csv`
- `eastern_shore_suspensions_2023_2024.json`

**Coverage**: 41 schools across 5 counties

**Total Suspensions**: 3,818
- In-school: 779
- Out-of-school: 3,039

**By County**:
- Caroline: 9 schools, 937 total suspensions
- Dorchester: 10 schools, 1,547 total suspensions
- Kent: 4 schools, 518 total suspensions
- Queen Anne's: 13 schools, 464 total suspensions
- Talbot: 5 schools, 352 total suspensions

**Demographics Tracked**:
- Gender (male/female)
- Race/ethnicity (Black, Hispanic, White, Asian, Two or more races)
- Students with disabilities

### 2. Blueprint Funding Data (FY2019 to FY2024)
**Source**: CNS Maryland "Behind the Blueprint" county reports

**Files**:
- `blueprint_funding_data.json`
- `blueprint_funding_summary.csv`

**Per-Pupil Funding Increases**:
- Talbot: 49.0% increase (highest)
- Caroline: 40.3% increase
- Dorchester: 36.9% increase
- Kent: 33.8% increase
- Queen Anne's: 25.4% increase (lowest)

**Additional Data**:
- Strengths identified by state Accountability and Implementation Board
- Areas needing improvement
- Blueprint implementation plan assessments

### 3. County Budget Data
**Source**: County Board of Education budget PDFs

**File**: `county_budgets/budget_summary.csv`

**Data Extracted**:
- Total budgets
- State aid
- Local appropriations
- Teacher salaries
- Fund balances
- Federal funds

## Data Quality Notes

### Suspension Data
- ✅ Actual student counts (not percentages)
- ✅ School-level detail with demographic breakdowns
- ✅ Official MSDE source
- ✅ Complete coverage of all 5 Eastern Shore counties

### Blueprint Funding
- ✅ Per-pupil funding increase percentages
- ✅ Fiscal year comparisons (2019-2024)
- ✅ Qualitative assessments from state board
- ⚠️  Rankings not captured for all counties

### Budget Data
- ✅ County-level budget totals
- ⚠️  Data completeness varies by county
- ⚠️  Some extraction issues with PDF formats
