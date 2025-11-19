#!/usr/bin/env python3
"""
Census Data Retrieval Agent for Maryland Counties
Fetches demographic and education-related data for:
- Talbot County, MD
- Kent County, MD
- Dorchester County, MD
- Caroline County, MD
- Queen Anne's County, MD
"""

import requests
import json
import os

# Census API configuration
CENSUS_API_KEY = os.environ.get("CENSUS_API_KEY", "")
CENSUS_API_BASE = "https://api.census.gov/data"

# Maryland FIPS code
MD_STATE_FIPS = "24"

# County FIPS codes for Maryland
COUNTY_FIPS = {
    "Talbot County": "041",
    "Kent County": "029",
    "Dorchester County": "019",
    "Caroline County": "011",
    "Queen Anne's County": "035"
}

# Data variables to fetch from ACS 5-Year estimates
# https://api.census.gov/data/2022/acs/acs5/variables.html
VARIABLES = {
    # Population
    "B01003_001E": "Total Population",
    
    # Age groups (school-age)
    "B01001_003E": "Male Under 5 years",
    "B01001_004E": "Male 5 to 9 years",
    "B01001_005E": "Male 10 to 14 years",
    "B01001_006E": "Male 15 to 17 years",
    "B01001_007E": "Male 18 and 19 years",
    "B01001_027E": "Female Under 5 years",
    "B01001_028E": "Female 5 to 9 years",
    "B01001_029E": "Female 10 to 14 years",
    "B01001_030E": "Female 15 to 17 years",
    "B01001_031E": "Female 18 and 19 years",
    
    # Race/Ethnicity
    "B02001_002E": "White alone",
    "B02001_003E": "Black or African American alone",
    "B02001_005E": "Asian alone",
    "B03003_003E": "Hispanic or Latino",
    
    # Educational Attainment (25 years and over)
    "B15003_001E": "Total population 25 years and over",
    "B15003_017E": "High school graduate",
    "B15003_022E": "Bachelor's degree",
    "B15003_023E": "Master's degree",
    "B15003_024E": "Professional school degree",
    "B15003_025E": "Doctorate degree",
    
    # School Enrollment
    "B14001_001E": "Total population 3 years and over",
    "B14001_002E": "Enrolled in school",
    "B14001_003E": "Enrolled in nursery school, preschool",
    "B14001_004E": "Enrolled in kindergarten",
    "B14001_005E": "Enrolled in grade 1 to grade 4",
    "B14001_006E": "Enrolled in grade 5 to grade 8",
    "B14001_007E": "Enrolled in grade 9 to grade 12",
    "B14001_008E": "Enrolled in college, undergraduate",
    
    # Poverty Status
    "B17001_001E": "Total population for poverty determination",
    "B17001_002E": "Income below poverty level",
    
    # Median Household Income
    "B19013_001E": "Median household income",
    
    # Language Spoken at Home
    "B16001_001E": "Total population 5 years and over",
    "B16001_002E": "Speak only English",
    "B16001_003E": "Speak Spanish",
    
    # Computer and Internet Access
    "B28002_001E": "Total households",
    "B28002_004E": "Has computer, has broadband internet",
    "B28002_007E": "Has computer, no internet",
    "B28002_013E": "No computer",
}


def fetch_acs_data(year=2022):
    """
    Fetch ACS 5-Year estimates for all counties
    """
    # Build variable list for API request
    var_list = ",".join(VARIABLES.keys())
    
    results = {}
    
    for county_name, county_fips in COUNTY_FIPS.items():
        print(f"Fetching data for {county_name}...")
        
        url = f"{CENSUS_API_BASE}/{year}/acs/acs5"
        params = {
            "get": var_list,
            "for": f"county:{county_fips}",
            "in": f"state:{MD_STATE_FIPS}",
        }
        
        if CENSUS_API_KEY:
            params["key"] = CENSUS_API_KEY
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # First row is headers, second row is data
            if len(data) < 2:
                print(f"  ⚠️  No data returned for {county_name}")
                continue
            
            headers = data[0]
            values = data[1]
            
            # Create a dictionary of variable -> value
            county_data = {}
            for i, var_code in enumerate(headers):
                if var_code in VARIABLES:
                    var_name = VARIABLES[var_code]
                    value = values[i]
                    # Convert to int if possible, handle null values
                    try:
                        county_data[var_name] = int(value) if value not in [None, "", "-"] else None
                    except (ValueError, TypeError):
                        county_data[var_name] = value
            
            # Calculate derived metrics
            county_data["School-Age Population (5-17)"] = sum([
                county_data.get("Male 5 to 9 years", 0) or 0,
                county_data.get("Male 10 to 14 years", 0) or 0,
                county_data.get("Male 15 to 17 years", 0) or 0,
                county_data.get("Female 5 to 9 years", 0) or 0,
                county_data.get("Female 10 to 14 years", 0) or 0,
                county_data.get("Female 15 to 17 years", 0) or 0,
            ])
            
            # Calculate poverty rate
            total_poverty = county_data.get("Total population for poverty determination")
            below_poverty = county_data.get("Income below poverty level")
            if total_poverty and below_poverty:
                county_data["Poverty Rate (%)"] = round((below_poverty / total_poverty) * 100, 1)
            
            # Calculate school enrollment rate
            total_3_plus = county_data.get("Total population 3 years and over")
            enrolled = county_data.get("Enrolled in school")
            if total_3_plus and enrolled:
                county_data["School Enrollment Rate (%)"] = round((enrolled / total_3_plus) * 100, 1)
            
            # Calculate internet access rate
            total_households = county_data.get("Total households")
            with_broadband = county_data.get("Has computer, has broadband internet")
            if total_households and with_broadband:
                county_data["Broadband Access Rate (%)"] = round((with_broadband / total_households) * 100, 1)
            
            results[county_name] = county_data
            print(f"  ✓ Retrieved {len(county_data)} data points")
            
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error fetching data for {county_name}: {e}")
            continue
    
    return results


def save_results(data, filename="census_data.json"):
    """Save census data to JSON file"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n✓ Data saved to {filename}")


def print_summary(data):
    """Print a summary of key metrics"""
    print("\n" + "="*80)
    print("CENSUS DATA SUMMARY")
    print("="*80)
    
    for county, metrics in data.items():
        print(f"\n{county}:")
        print(f"  Total Population: {metrics.get('Total Population', 'N/A'):,}")
        print(f"  School-Age Population (5-17): {metrics.get('School-Age Population (5-17)', 'N/A'):,}")
        print(f"  Median Household Income: ${metrics.get('Median household income', 'N/A'):,}")
        print(f"  Poverty Rate: {metrics.get('Poverty Rate (%)', 'N/A')}%")
        print(f"  School Enrollment Rate: {metrics.get('School Enrollment Rate (%)', 'N/A')}%")
        print(f"  Broadband Access Rate: {metrics.get('Broadband Access Rate (%)', 'N/A')}%")


def main():
    print("Census Data Retrieval Agent")
    print("="*80)
    print("\nFetching data for Maryland counties:")
    for county in COUNTY_FIPS.keys():
        print(f"  - {county}")
    
    if not CENSUS_API_KEY:
        print("\n⚠️  No Census API key found in environment variable CENSUS_API_KEY")
        print("   The script will attempt to fetch data without a key (limited requests)")
        print("   Get a free API key at: https://api.census.gov/data/key_signup.html")
    
    print("\nFetching 2022 ACS 5-Year Estimates...")
    print("-"*80)
    
    data = fetch_acs_data(year=2022)
    
    if data:
        save_results(data, "census_education_data.json")
        print_summary(data)
    else:
        print("\n✗ No data retrieved")


if __name__ == "__main__":
    main()
