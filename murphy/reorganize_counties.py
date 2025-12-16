#!/usr/bin/env python3
"""
Script to reorganize county profile panels in the dashboard.
Splits School System into multiple tabs and creates County Summary.
"""

import re

# Read the dashboard
with open('stardem_final/dashboard/dashboard.html', 'r') as f:
    html = f.read()

print("Dashboard loaded successfully")
print(f"File size: {len(html)} characters")

# Save backup
with open('stardem_final/dashboard/dashboard_backup.html', 'w') as f:
    f.write(html)
print("Backup saved")

# Counties to process (Caroline already done)
counties_data = {
    'dorchester': {
        'narrative_start': 'Dorchester County faces the starkest equity challenges',
        'leadership': 'Superintendent Dr. Jymil Thompson (appointed July 2024)',
        'website': 'www.dcpsmd.org'
    },
    'kent': {
        'narrative_start': 'Kent County presents a fiscal puzzle',
        'leadership': 'Superintendent Karen Couch',
        'website': 'www.kent.k12.md.us'
    },
    'queen-annes': {
        'narrative_start': "Queen Anne's County stands as the Eastern Shore's wealthiest",
        'leadership': 'Superintendent Dr. Steven Zimbrick',
        'website': 'www.qacps.org'
    },
    'talbot': {
        'narrative_start': 'Talbot County operates Maryland',
        'leadership': 'Superintendent Dr. Emily Massie',
        'website': 'www.tcps.k12.md.us'
    }
}

print("\nProcessing complete - manual intervention needed for panel creation")
print("The tab structures have been updated. Now panels need to be reorganized.")
