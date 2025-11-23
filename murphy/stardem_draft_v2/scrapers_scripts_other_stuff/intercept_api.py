#!/usr/bin/env python3
"""
Intercept network requests to find the API endpoint
"""

import asyncio
import json
from playwright.async_api import async_playwright

async def intercept_requests():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Store all API requests
        api_requests = []
        
        async def log_request(request):
            if 'api' in request.url.lower() or '.json' in request.url or 'data' in request.url.lower():
                api_requests.append({
                    'url': request.url,
                    'method': request.method,
                    'headers': dict(request.headers)
                })
                print(f"API Request: {request.method} {request.url}")
        
        page.on("request", log_request)
        
        # Navigate to Preston Elementary staffing page
        url = "https://reportcard.msde.maryland.gov/Graphs/#/Staffing/School/99/05/0401/2024"
        print(f"Navigating to: {url}\n")
        
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await asyncio.sleep(10)
        
        print(f"\n\nFound {len(api_requests)} API requests:")
        for req in api_requests:
            print(f"\n{req['method']} {req['url']}")
        
        # Save to file
        with open('api_requests.json', 'w') as f:
            json.dump(api_requests, f, indent=2)
        
        print("\n✓ Saved: api_requests.json")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(intercept_requests())
