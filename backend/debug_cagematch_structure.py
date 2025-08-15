#!/usr/bin/env python3
"""
Debug Cagematch HTML Structure
"""

import requests
from bs4 import BeautifulSoup
import json

def debug_wrestler_page():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Test with Roman Reigns
    url = "https://www.cagematch.net/?id=2&nr=9967"
    
    print(f"🔍 Debugging: {url}")
    
    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        # Save the HTML for inspection
        with open("roman_reigns_debug.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        
        print("💾 Saved HTML to roman_reigns_debug.html")
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print("\n🔍 Looking for InformationBoxTable divs...")
        info_tables = soup.find_all('div', {'class': 'InformationBoxTable'})
        print(f"Found {len(info_tables)} InformationBoxTable divs")
        
        for i, table in enumerate(info_tables):
            print(f"\n--- Table {i+1} ---")
            rows = table.find_all('div', {'class': 'InformationBoxRow'})
            print(f"  Rows: {len(rows)}")
            
            for j, row in enumerate(rows[:3]):  # Show first 3 rows
                title_div = row.find('div', {'class': 'InformationBoxTitle'})
                content_div = row.find('div', {'class': 'InformationBoxContents'})
                
                if title_div and content_div:
                    title = title_div.get_text(strip=True)
                    content = content_div.get_text(strip=True)
                    print(f"    Row {j+1}: '{title}' = '{content}'")
                else:
                    print(f"    Row {j+1}: Missing title or content div")
        
        print("\n🔍 Looking for other potential data structures...")
        
        # Look for any divs with "Age" or "Promotion" text
        age_elements = soup.find_all(string=re.compile(r'Age', re.IGNORECASE))
        print(f"Age elements found: {len(age_elements)}")
        for elem in age_elements[:3]:
            print(f"  Age element: {elem}")
            if hasattr(elem, 'parent'):
                print(f"    Parent: {elem.parent}")
        
        promotion_elements = soup.find_all(string=re.compile(r'Promotion', re.IGNORECASE))
        print(f"Promotion elements found: {len(promotion_elements)}")
        for elem in promotion_elements[:3]:
            print(f"  Promotion element: {elem}")
            if hasattr(elem, 'parent'):
                print(f"    Parent: {elem.parent}")
        
        # Look for any table structures
        tables = soup.find_all('table')
        print(f"\nTotal tables found: {len(tables)}")
        
        for i, table in enumerate(tables[:3]):
            print(f"\n--- Table {i+1} ---")
            rows = table.find_all('tr')
            print(f"  Rows: {len(rows)}")
            
            for j, row in enumerate(rows[:3]):
                cells = row.find_all(['td', 'th'])
                if cells:
                    cell_texts = [cell.get_text(strip=True) for cell in cells]
                    print(f"    Row {j+1}: {cell_texts}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import re
    debug_wrestler_page()
