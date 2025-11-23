#!/usr/bin/env python3
"""
Scrape statewide MCAP average data from MSDE Report Card website.
This collects statewide proficiency rates for comparison with Eastern Shore schools.
"""

import asyncio
import json
import re
from datetime import datetime
from playwright.async_api import async_playwright


async def scrape_statewide_mcap():
    """Scrape statewide MCAP proficiency data from Maryland Report Card."""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Data structure to store results
        mcap_data = {
            "ELA_5": None,
            "ELA_8": None,
            "ELA_10": None,
            "Math_5": None,
            "Math_8": None,
            "Math_Algebra_1": None,
            "Science_5": None,
            "Science_8": None,
            "Science_Biology": None,
            "metadata": {
                "source": "Maryland Report Card",
                "date_scraped": datetime.now().strftime("%Y-%m-%d"),
                "url": "https://reportcard.msde.maryland.gov/",
                "note": "Statewide MCAP proficiency rates (PL 3/4)"
            }
        }
        
        print("Starting statewide MCAP data scraping...")
        
        # Define what we need to scrape
        # Format: (key, nav_link_id, assessment_type_id, grade_display_name)
        scrape_list = [
            ("ELA_5", "lnkELA", "5ELA", "ELA 5"),
            ("ELA_8", "lnkELA", "8ELA", "ELA 8"),
            ("ELA_10", "lnkELA", "10ELA", "English 10"),
            ("Math_5", "lnkMath", "5MAT", "Math 5"),
            ("Math_8", "lnkMath", "8MAT", "Math 8"),
            ("Math_Algebra_1", "lnkMath", "ALGE1", "Algebra I"),
            ("Science_5", "lnkSci", "5SCI", "Science 5"),
            ("Science_8", "lnkSci", "8SCI", "Science 8"),
            ("Science_Biology", "lnkSci", "BIOL", "Biology"),
        ]
        
        # Start with the ELA page
        start_url = "https://reportcard.msde.maryland.gov/Graphs/#/Assessments/ElaPerformance/3ELA/3/5/3/1/99/XXXX/2025"
        await page.goto(start_url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(5)
        
        for key, nav_link, assessment_id, grade_display in scrape_list:
            print(f"\nScraping {key} ({grade_display})...")
            
            try:
                # First, click the subject navigation link if needed (ELA, Math, Science)
                if nav_link:
                    print(f"  Clicking subject nav: {nav_link}")
                    nav_element = page.locator(f"#{nav_link}")
                    if await nav_element.count() > 0:
                        await nav_element.click()
                        await asyncio.sleep(2)
                
                # Click the assessment type dropdown combobox
                print(f"  Opening assessment dropdown...")
                assessment_dropdown = page.locator("#combo-MCAP2AssessmentType-1-2")
                await assessment_dropdown.click()
                await asyncio.sleep(1)
                
                # Click the specific assessment option
                print(f"  Selecting: {grade_display} (ID: {assessment_id})")
                assessment_option = page.locator(f'a[data-group="MCAP2AssessmentType"][id="{assessment_id}"]')
                if await assessment_option.count() > 0:
                    await assessment_option.click()
                    await asyncio.sleep(3)
                else:
                    print(f"  ✗ Could not find assessment option: {assessment_id}")
                    continue
                
                # Click "Show Table" button to reveal the data table
                print(f"  Looking for Show Table button...")
                show_table_button = page.locator("button:has-text('Show Table'), a:has-text('Show Table')")
                if await show_table_button.count() > 0:
                    await show_table_button.first.click()
                    print(f"  ✓ Clicked 'Show Table' button")
                    await asyncio.sleep(3)
                
                # Take a screenshot for debugging
                await page.screenshot(path=f'debug_{key}.png')
                
                # Extract data from the table
                # Look for table rows with Level 3 and Level 4 data
                try:
                    # Try to find table data
                    table_cells = await page.locator("table td, table th").all_text_contents()
                    
                    # Look for Level 3 and Level 4 percentages in table
                    level_3 = None
                    level_4 = None
                    
                    for i, cell in enumerate(table_cells):
                        if 'Level 3' in cell or 'Level3' in cell:
                            # Next cell might have the percentage
                            for j in range(i+1, min(i+5, len(table_cells))):
                                match = re.search(r'(\d+\.?\d*)\s*%?', table_cells[j])
                                if match and float(match.group(1)) < 100:
                                    level_3 = float(match.group(1))
                                    break
                        
                        if 'Level 4' in cell or 'Level4' in cell:
                            for j in range(i+1, min(i+5, len(table_cells))):
                                match = re.search(r'(\d+\.?\d*)\s*%?', table_cells[j])
                                if match and float(match.group(1)) < 100:
                                    level_4 = float(match.group(1))
                                    break
                    
                    if level_3 is not None and level_4 is not None:
                        proficiency_rate = level_3 + level_4
                        print(f"  ✓ Level 3: {level_3}%, Level 4: {level_4}%")
                        print(f"  ✓ Total proficiency: {proficiency_rate}%")
                        mcap_data[key] = proficiency_rate
                        continue
                    elif level_3 is not None or level_4 is not None:
                        print(f"  Partial data: Level 3={level_3}, Level 4={level_4}")
                
                except Exception as e:
                    print(f"  Table extraction error: {e}")
                
                # Try looking in the page text as fallback
                body_text = await page.locator('body').text_content()
                level_3_match = re.search(r'Level\s*3[:\s]+(\d+\.?\d*)\s*%', body_text, re.IGNORECASE)
                level_4_match = re.search(r'Level\s*4[:\s]+(\d+\.?\d*)\s*%', body_text, re.IGNORECASE)
                
                if level_3_match and level_4_match:
                    level_3 = float(level_3_match.group(1))
                    level_4 = float(level_4_match.group(1))
                    proficiency_rate = level_3 + level_4
                    print(f"  ✓ Found in text - Level 3: {level_3}%, Level 4: {level_4}%")
                    print(f"  ✓ Total proficiency: {proficiency_rate}%")
                    mcap_data[key] = proficiency_rate
                else:
                    print(f"  ✗ Could not extract proficiency rate")
                    print(f"  → See debug_{key}.png")
                    
            except Exception as e:
                print(f"  Error scraping {key}: {str(e)}")
        
        await browser.close()
        
        # Save results
        output_file = "state_mcap_averages.json"
        with open(output_file, 'w') as f:
            json.dump(mcap_data, f, indent=2)
        
        print(f"\n✓ Saved statewide MCAP data to: {output_file}")
        print("\nStatewide MCAP Proficiency Rates:")
        print(f"ELA - Grade 5: {mcap_data['ELA_5']}%, Grade 8: {mcap_data['ELA_8']}%, Grade 10: {mcap_data['ELA_10']}%")
        print(f"Math - Grade 5: {mcap_data['Math_5']}%, Grade 8: {mcap_data['Math_8']}%, Algebra 1: {mcap_data['Math_Algebra_1']}%")
        print(f"Science - Grade 5: {mcap_data['Science_5']}%, Grade 8: {mcap_data['Science_8']}%, Biology: {mcap_data['Science_Biology']}%")
        
        return mcap_data


if __name__ == "__main__":
    asyncio.run(scrape_statewide_mcap())
