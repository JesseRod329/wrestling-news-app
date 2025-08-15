#!/usr/bin/env python3
"""
Test Cagematch Search Functionality
"""

import requests
from bs4 import BeautifulSoup

def test_search():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    # Test different search URLs
    test_urls = [
        "https://www.cagematch.net/?id=4&view=search&s=Roman+Reigns",
        "https://www.cagematch.net/?id=4&view=search&s=Roman",
        "https://www.cagematch.net/?id=4&view=search",
        "https://www.cagematch.net/?id=4",
        "https://www.cagematch.net/?id=4&view=search&s=Roman&view=wrestlers"
    ]
    
    for url in test_urls:
        print(f"\n🔍 Testing: {url}")
        try:
            response = session.get(url, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for any links
                links = soup.find_all('a', href=True)
                wrestler_links = [l for l in links if 'nr=' in l['href']]
                
                print(f"Total links: {len(links)}")
                print(f"Wrestler links: {len(wrestler_links)}")
                
                if wrestler_links:
                    print("Sample wrestler links:")
                    for link in wrestler_links[:5]:
                        print(f"  {link.get_text(strip=True)} -> {link['href']}")
                
                # Look for search form
                search_form = soup.find('form')
                if search_form:
                    print("Found search form!")
                    print(f"Action: {search_form.get('action', 'N/A')}")
                    print(f"Method: {search_form.get('method', 'N/A')}")
                    
                    inputs = search_form.find_all('input')
                    for inp in inputs:
                        print(f"  Input: {inp.get('name', 'N/A')} = {inp.get('value', 'N/A')}")
                
            else:
                print(f"Error: {response.status_code}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
