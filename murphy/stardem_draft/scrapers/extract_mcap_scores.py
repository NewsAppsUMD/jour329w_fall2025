"""
Extract MCAP Test Scores from Enhanced School Data

Parses the collected MCAP data to extract specific test scores
for English Language Arts, Mathematics, and Science.
"""

import json
import pandas as pd
import re
from typing import Dict, List

def extract_mcap_scores(mcap_text: str) -> Dict:
    """Extract MCAP test scores from the raw text content"""
    scores = {}
    
    if not mcap_text or len(mcap_text) < 50:
        return scores
    
    # Look for percentage patterns - MCAP shows "XX.X% Proficient"
    # Pattern: number followed by % or "percent"
    
    # Try to find ELA scores
    ela_match = re.search(r'ELA.*?(\d+\.?\d*)%?\s*proficient', mcap_text, re.IGNORECASE)
    if ela_match:
        scores['ela_proficient_pct'] = float(ela_match.group(1))
    
    # Try to find Math scores
    math_match = re.search(r'Math(?:ematics)?.*?(\d+\.?\d*)%?\s*proficient', mcap_text, re.IGNORECASE)
    if math_match:
        scores['math_proficient_pct'] = float(math_match.group(1))
    
    # Try to find Science scores
    science_match = re.search(r'Science.*?(\d+\.?\d*)%?\s*proficient', mcap_text, re.IGNORECASE)
    if science_match:
        scores['science_proficient_pct'] = float(science_match.group(1))
    
    # Look for specific grade level scores if present
    # Pattern: "Grade X: YY.Y%"
    grade_scores = re.findall(r'Grade\s*(\d+).*?(\d+\.?\d*)%', mcap_text, re.IGNORECASE)
    if grade_scores:
        for grade, score in grade_scores[:3]:  # Limit to first 3
            scores[f'grade_{grade}_pct'] = float(score)
    
    return scores


def main():
    """Extract MCAP scores for all schools"""
    
    print("Extracting MCAP Test Scores...")
    print("="*80)
    
    # Load enhanced data
    with open('schools_enhanced_data.json', 'r') as f:
        schools = json.load(f)
    
    # Extract scores for each school
    results = []
    
    for school in schools:
        mcap_data = school.get('mcap_data', '')
        
        record = {
            'school_name': school['school_name'],
            'county': school['county'],
            'star_rating': school.get('star_rating', None),
            'percentile_rank': school.get('percentile_rank', None),
        }
        
        # Extract MCAP scores
        scores = extract_mcap_scores(mcap_data)
        record.update(scores)
        
        results.append(record)
        
        # Show progress
        if scores:
            score_str = ', '.join([f"{k}: {v}%" for k, v in scores.items()])
            print(f"✓ {school['school_name'][:45]:<45} | {score_str}")
        else:
            print(f"○ {school['school_name'][:45]:<45} | No MCAP scores found")
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Save to files
    output_csv = 'mcap_test_scores.csv'
    output_json = 'mcap_test_scores.json'
    
    df.to_csv(output_csv, index=False)
    
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*80)
    print("MCAP TEST SCORES SUMMARY")
    print("="*80)
    
    # Count how many schools have scores
    schools_with_ela = df['ela_proficient_pct'].notna().sum()
    schools_with_math = df['math_proficient_pct'].notna().sum()
    schools_with_science = df['science_proficient_pct'].notna().sum()
    
    print(f"\nSchools with ELA scores: {schools_with_ela}/{len(df)}")
    print(f"Schools with Math scores: {schools_with_math}/{len(df)}")
    print(f"Schools with Science scores: {schools_with_science}/{len(df)}")
    
    if schools_with_ela > 0:
        print(f"\nELA Proficiency:")
        print(f"  Mean: {df['ela_proficient_pct'].mean():.1f}%")
        print(f"  Median: {df['ela_proficient_pct'].median():.1f}%")
        print(f"  Range: {df['ela_proficient_pct'].min():.1f}% - {df['ela_proficient_pct'].max():.1f}%")
    
    if schools_with_math > 0:
        print(f"\nMath Proficiency:")
        print(f"  Mean: {df['math_proficient_pct'].mean():.1f}%")
        print(f"  Median: {df['math_proficient_pct'].median():.1f}%")
        print(f"  Range: {df['math_proficient_pct'].min():.1f}% - {df['math_proficient_pct'].max():.1f}%")
    
    if schools_with_science > 0:
        print(f"\nScience Proficiency:")
        print(f"  Mean: {df['science_proficient_pct'].mean():.1f}%")
        print(f"  Median: {df['science_proficient_pct'].median():.1f}%")
        print(f"  Range: {df['science_proficient_pct'].min():.1f}% - {df['science_proficient_pct'].max():.1f}%")
    
    # County averages
    if schools_with_ela > 0 or schools_with_math > 0:
        print("\n" + "="*80)
        print("MCAP SCORES BY COUNTY")
        print("="*80)
        
        for county in sorted(df['county'].unique()):
            county_df = df[df['county'] == county]
            ela_avg = county_df['ela_proficient_pct'].mean()
            math_avg = county_df['math_proficient_pct'].mean()
            
            print(f"\n{county} County:")
            if pd.notna(ela_avg):
                print(f"  ELA:  {ela_avg:.1f}%")
            if pd.notna(math_avg):
                print(f"  Math: {math_avg:.1f}%")
    
    print("\n" + "="*80)
    print(f"✓ Saved to: {output_csv}")
    print(f"✓ Saved to: {output_json}")
    print("="*80)
    
    # If scores weren't found, provide guidance
    if schools_with_ela == 0 and schools_with_math == 0:
        print("\n⚠ Note: MCAP scores not automatically extracted from text.")
        print("The MCAP data is in the 'mcap_data' field but needs manual review.")
        print("Run the enhanced scraper with specific MCAP extraction to get scores.")


if __name__ == "__main__":
    main()
