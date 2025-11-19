#!/bin/bash
# Quick command to run all schools through enhanced data extraction

cd /workspaces/jour329w_fall2025/murphy/stardem_draft

echo "=================================================="
echo "Maryland Schools - Enhanced Data Extraction"
echo "=================================================="
echo ""
echo "This will extract detailed data for all 50 schools"
echo "including star ratings, percentile ranks, demographics,"
echo "and test scores (MCAP data)."
echo ""
echo "This may take 5-10 minutes..."
echo ""

/workspaces/jour329w_fall2025/.venv/bin/python extract_detailed_data.py

echo ""
echo "=================================================="
echo "✅ COMPLETE!"
echo "=================================================="
echo ""
echo "Files created:"
echo "  - schools_enhanced_data.json"
echo "  - schools_enhanced_data.csv"
echo ""
echo "You can now analyze the data using:"
echo "  - Excel/Google Sheets (open the CSV)"
echo "  - Python/pandas (load the JSON)"
echo "  - Any data analysis tool"
