import csv
import os
from pathlib import Path

# Define the counties and races
counties = ['caroline', 'dorchester', 'kent', 'queen_annes', 'talbot']
races = ['black', 'hispanic', 'white']

# Output data structure
all_data = []

# Process each county
for county in counties:
    county_path = Path(f'/workspaces/jour329w_fall2025/murphy/stardem_final/master_data/grad_rates/{county}')
    
    for race in races:
        csv_file = county_path / f'{race}.csv'
        
        if csv_file.exists():
            with open(csv_file, 'r') as f:
                lines = f.readlines()
                
                # Find the data rows (skip header lines)
                data_started = False
                for line in lines:
                    # Look for year data rows (starting with a year like 2020, 2021, etc.)
                    if line.strip().startswith('20'):
                        parts = [p.strip() for p in line.split(',')]
                        year = parts[0]
                        
                        # Get the graduation rate for the specific race
                        # Format: Year, All Students Rate, All Students Count, Race Rate, Race Count
                        if len(parts) >= 4:
                            race_rate = parts[3]  # The rate for the specific race (4th column)
                            
                            # Clean up the rate value
                            if race_rate:
                                all_data.append({
                                    'year': year,
                                    'county': county.replace('_', ' ').title(),
                                    'race': race.title(),
                                    'graduation_rate': race_rate
                                })

# Sort by year, county, race
all_data.sort(key=lambda x: (x['year'], x['county'], x['race']))

# Write to combined CSV
output_file = '/workspaces/jour329w_fall2025/murphy/stardem_final/master_data/grad_rates/combined_grad_rates.csv'
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['year', 'county', 'race', 'graduation_rate'])
    writer.writeheader()
    writer.writerows(all_data)

print(f"Combined {len(all_data)} records into {output_file}")
print("\nFirst 10 rows:")
for i, row in enumerate(all_data[:10]):
    print(f"{row['year']}, {row['county']}, {row['race']}, {row['graduation_rate']}")
