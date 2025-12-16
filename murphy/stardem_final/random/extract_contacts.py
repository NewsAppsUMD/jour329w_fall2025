#!/usr/bin/env python3
"""Extract contacts data from dashboard.html and save as JSON"""

import json
import re

# Read dashboard.html
with open('dashboard.html', 'r') as f:
    content = f.read()

# Find the CONTACTS_DATA array
match = re.search(r'const CONTACTS_DATA = \[(.*?)\];', content, re.DOTALL)
if not match:
    print("Could not find CONTACTS_DATA in HTML")
    exit(1)

contacts_js = match.group(1)

# Convert JavaScript object notation to JSON
# Replace single quotes with double quotes (carefully)
contacts_js = re.sub(r"name: '([^']*)'", r'name: "\1"', contacts_js)
contacts_js = re.sub(r'name: "([^"]*)"', r'"name": "\1"', contacts_js)
contacts_js = re.sub(r'position: "([^"]*)"', r'"position": "\1"', contacts_js)
contacts_js = re.sub(r'organization: "([^"]*)"', r'"organization": "\1"', contacts_js)
contacts_js = re.sub(r'county: "([^"]*)"', r'"county": "\1"', contacts_js)
contacts_js = re.sub(r'roleType: "([^"]*)"', r'"roleType": "\1"', contacts_js)
contacts_js = re.sub(r'phone: "([^"]*)"', r'"phone": "\1"', contacts_js)
contacts_js = re.sub(r'email: "([^"]*)"', r'"email": "\1"', contacts_js)
contacts_js = re.sub(r'address: "([^"]*)"', r'"address": "\1"', contacts_js)
contacts_js = re.sub(r'background: "([^"]*)"', r'"background": "\1"', contacts_js)

# Remove comments
contacts_js = re.sub(r'//.*?\n', '\n', contacts_js)

# Wrap in array
contacts_json = '[' + contacts_js + ']'

try:
    contacts_data = json.loads(contacts_json)
    print(f"Successfully parsed {len(contacts_data)} contacts")
    
    # Save to file
    with open('contacts_data.json', 'w') as f:
        json.dump(contacts_data, f, indent=2)
    
    print(f"Saved contacts_data.json with {len(contacts_data)} contacts")
except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")
    print("Attempting manual extraction...")
    
    # Manual extraction as fallback
    contacts = []
    # Split by contact blocks
    blocks = re.findall(r'\{[^{}]*name:[^}]+\}', contacts_js, re.DOTALL)
    
    for block in blocks:
        try:
            # Extract fields
            name = re.search(r'name:\s*"([^"]*)"', block)
            position = re.search(r'position:\s*"([^"]*)"', block)
            organization = re.search(r'organization:\s*"([^"]*)"', block)
            county = re.search(r'county:\s*"([^"]*)"', block)
            roleType = re.search(r'roleType:\s*"([^"]*)"', block)
            phone = re.search(r'phone:\s*"([^"]*)"', block)
            email = re.search(r'email:\s*"([^"]*)"', block)
            address = re.search(r'address:\s*"([^"]*)"', block)
            background = re.search(r'background:\s*"([^"]*)"', block)
            
            if all([name, position, organization, county, roleType, phone, email, address, background]):
                contacts.append({
                    "name": name.group(1),
                    "position": position.group(1),
                    "organization": organization.group(1),
                    "county": county.group(1),
                    "roleType": roleType.group(1),
                    "phone": phone.group(1),
                    "email": email.group(1),
                    "address": address.group(1),
                    "background": background.group(1)
                })
        except Exception as e:
            print(f"Error parsing block: {e}")
            continue
    
    print(f"Manually extracted {len(contacts)} contacts")
    
    with open('contacts_data.json', 'w') as f:
        json.dump(contacts, f, indent=2)
    
    print("Saved contacts_data.json")
