import json
from collections import OrderedDict

# Load the county summary book
with open('county_summary_book.json', 'r') as f:
    county_book = json.load(f, object_pairs_hook=OrderedDict)

# Move staffing data inside district for each county
for county_name in ["Caroline", "Dorchester", "Kent", "Queen Anne's", "Talbot"]:
    if county_name in county_book:
        county_data = county_book[county_name]
        
        # Check if staffing exists as a separate key
        if 'staffing' in county_data and 'district' in county_data:
            # Move staffing into district
            county_data['district']['staffing'] = county_data['staffing']
            
            # Remove the standalone staffing key and rebuild the county data
            new_county = OrderedDict()
            for key, value in county_data.items():
                if key != 'staffing':
                    new_county[key] = value
            
            county_book[county_name] = new_county

# Save updated county_summary_book
with open('county_summary_book.json', 'w') as f:
    json.dump(county_book, f, indent=2)

print("✓ Moved staffing data into district key for all counties")

# Verify the change
with open('county_summary_book.json', 'r') as f:
    data = json.load(f)

print("\nVerification - Talbot County structure:")
print("Keys in Talbot:", list(data['Talbot'].keys()))
print("Keys in Talbot district:", list(data['Talbot']['district'].keys()))
