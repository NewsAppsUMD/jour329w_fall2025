from playwright.sync_api import sync_playwright
import time
import os

# Create downloads directory
download_dir = '/workspaces/jour329w_fall2025/murphy/stardem_final/master_data/downloads'
os.makedirs(download_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()
    
    url = 'https://reportcard.msde.maryland.gov/Graphs/#/Assessments/ElaPerformance/AELAA/A/12/3/1/05/XXXX/2025'
    page.goto(url, wait_until='networkidle', timeout=20000)
    time.sleep(5)
    
    # Try to find and click Download CSV
    try:
        # Wait for the download to start
        with page.expect_download() as download_info:
            # Try different selectors for the CSV download button
            try:
                page.click('text=Download CSV', timeout=5000)
            except:
                try:
                    page.click('a:has-text("CSV")', timeout=5000)
                except:
                    page.click('a[href*="csv"]', timeout=5000)
        
        download = download_info.value
        
        # Save the file
        save_path = os.path.join(download_dir, 'caroline_white_ela.csv')
        download.save_as(save_path)
        print(f"Downloaded CSV to: {save_path}")
        
        # Read and display the content
        with open(save_path, 'r') as f:
            content = f.read()
            print("\nCSV Content:")
            print(content)
            
    except Exception as e:
        print(f"Error downloading CSV: {e}")
        
        # Try to see what links are available
        print("\nLooking for download links...")
        content = page.locator('body').inner_text()
        if 'Download' in content:
            idx = content.find('Download')
            print(f"Context around Download: {content[idx-50:idx+150]}")
    
    browser.close()
