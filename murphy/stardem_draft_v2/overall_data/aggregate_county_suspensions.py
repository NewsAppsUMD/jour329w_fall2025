import json
import csv
from collections import defaultdict

# Read the school-level data
with open('/workspaces/jour329w_fall2025/murphy/stardem_draft_v2/overall_data/school_level_suspensions_2023_2024.json', 'r') as f:
    schools = json.load(f)

# Aggregate by county and suspension type
county_data = defaultdict(lambda: {
    'in_school': {'total': 0, 'asian': 0, 'black': 0, 'hispanic': 0, 'white': 0, 'two_or_more': 0},
    'out_of_school': {'total': 0, 'asian': 0, 'black': 0, 'hispanic': 0, 'white': 0, 'two_or_more': 0}
})

for school in schools:
    county = school['county']
    susp_type = school['suspension_type']
    
    county_data[county][susp_type]['total'] += school['total_suspensions']
    county_data[county][susp_type]['asian'] += school['race']['asian']
    county_data[county][susp_type]['black'] += school['race']['black']
    county_data[county][susp_type]['hispanic'] += school['race']['hispanic']
    county_data[county][susp_type]['white'] += school['race']['white']
    county_data[county][susp_type]['two_or_more'] += school['race']['two_or_more']

# Create CSV output
output_file = '/workspaces/jour329w_fall2025/murphy/stardem_draft_v2/overall_data/county_suspensions_by_race.csv'

with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    
    # Write header
    writer.writerow([
        'county', 'suspension_type', 'total_suspensions',
        'asian', 'asian_pct',
        'black', 'black_pct',
        'hispanic', 'hispanic_pct',
        'white', 'white_pct',
        'two_or_more', 'two_or_more_pct'
    ])
    
    # Write data
    for county in sorted(county_data.keys()):
        for susp_type in ['in_school', 'out_of_school']:
            data = county_data[county][susp_type]
            total = data['total']
            
            if total > 0:
                writer.writerow([
                    county,
                    susp_type,
                    total,
                    data['asian'],
                    round(data['asian'] / total * 100, 1) if total > 0 else 0,
                    data['black'],
                    round(data['black'] / total * 100, 1) if total > 0 else 0,
                    data['hispanic'],
                    round(data['hispanic'] / total * 100, 1) if total > 0 else 0,
                    data['white'],
                    round(data['white'] / total * 100, 1) if total > 0 else 0,
                    data['two_or_more'],
                    round(data['two_or_more'] / total * 100, 1) if total > 0 else 0
                ])

print(f"County-level suspension data by race written to {output_file}")

# Display summary
print("\nSummary:")
for county in sorted(county_data.keys()):
    total_in = county_data[county]['in_school']['total']
    total_out = county_data[county]['out_of_school']['total']
    print(f"{county}: In-School={total_in}, Out-of-School={total_out}, Total={total_in + total_out}")
