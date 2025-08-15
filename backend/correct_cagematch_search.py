#!/usr/bin/env python3
"""
Correct Cagematch Search for Wrestler IDs
"""

import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import re

class CorrectCagematchSearch:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.base_url = "https://www.cagematch.net"
        
        self.top_wrestlers = [
            "Roman Reigns", "Cody Rhodes", "Seth Rollins", "Bianca Belair", 
            "Rhea Ripley", "Kenny Omega", "MJF", "Kazuchika Okada", 
            "Will Ospreay", "Brock Lesnar", "John Cena", "The Rock",
            "Stone Cold Steve Austin", "Hulk Hogan", "Ric Flair", 
            "Shawn Michaels", "Bret Hart", "Undertaker", "Triple H",
            "Randy Orton", "Edge", "Christian", "Jeff Hardy", "Matt Hardy",
            "CM Punk", "Daniel Bryan", "AJ Styles", "Samoa Joe", 
            "Shinsuke Nakamura", "Finn Balor", "Kevin Owens", "Sami Zayn",
            "Bobby Lashley", "Drew McIntyre"
        ]
    
    def search_wrestler(self, name: str) -> Optional[Dict[str, Any]]:
        """Search for wrestler using correct Cagematch search"""
        try:
            # Use the correct search URL structure
            search_url = f"{self.base_url}/?id=666&search={name.replace(' ', '+')}"
            
            print(f"🔍 Searching for: {name}")
            print(f"   URL: {search_url}")
            
            response = self.session.get(search_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for wrestler profile links
            wrestler_links = soup.find_all('a', href=re.compile(r'\?id=2&nr=\d+'))
            
            if not wrestler_links:
                print(f"   ❌ No wrestler links found")
                return None
            
            print(f"   Found {len(wrestler_links)} potential matches")
            
            # Find best match
            best_match = None
            best_score = 0
            
            for link in wrestler_links:
                link_text = link.get_text(strip=True)
                wrestler_id = re.search(r'nr=(\d+)', link['href'])
                
                if not wrestler_id:
                    continue
                    
                wrestler_id = wrestler_id.group(1)
                score = self._calculate_similarity(name, link_text)
                
                print(f"      {link_text} (ID: {wrestler_id}, Score: {score:.2f})")
                
                if score > best_score:
                    best_score = score
                    best_match = {
                        "name": link_text,
                        "cagematch_id": wrestler_id,
                        "score": score,
                        "profile_url": f"{self.base_url}/?id=2&nr={wrestler_id}"
                    }
            
            if best_match and best_match["score"] >= 0.6:
                print(f"   ✅ Best match: {best_match['name']} (ID: {best_match['cagematch_id']})")
                return best_match
            else:
                print(f"   ❌ No good match found")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def _calculate_similarity(self, search_name: str, found_name: str) -> float:
        """Calculate name similarity score"""
        search_lower = search_name.lower()
        found_lower = found_name.lower()
        
        if search_lower == found_lower:
            return 1.0
        
        if search_lower in found_lower:
            return 0.9
        
        if found_lower in search_lower:
            return 0.8
        
        # Word-based similarity
        search_words = set(search_lower.split())
        found_words = set(found_lower.split())
        
        if search_words & found_words:
            intersection = len(search_words & found_words)
            union = len(search_words | found_words)
            return intersection / union
        
        return 0.0
    
    def find_all_ids(self) -> Dict[str, Dict[str, Any]]:
        """Find IDs for all wrestlers"""
        results = {}
        
        print(f"🚀 Starting search for {len(self.top_wrestlers)} wrestlers...")
        print("=" * 60)
        
        for i, name in enumerate(self.top_wrestlers, 1):
            print(f"\n[{i}/{len(self.top_wrestlers)}] ", end="")
            result = self.search_wrestler(name)
            if result:
                results[name] = result
            
            if i < len(self.top_wrestlers):
                time.sleep(2)
        
        print(f"\n✅ Found {len(results)} wrestlers")
        return results
    
    def save_results(self, results: Dict[str, Dict[str, Any]]):
        """Save results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"correct_ids_{timestamp}.json"
        
        data = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "total_found": len(results)
            },
            "wrestlers": results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to: {filename}")

def main():
    searcher = CorrectCagematchSearch()
    results = searcher.find_all_ids()
    
    if results:
        searcher.save_results(results)
        print("\n📊 Results:")
        for name, info in results.items():
            print(f"✅ {name}: {info['name']} (ID: {info['cagematch_id']})")
    else:
        print("❌ No results found!")

if __name__ == "__main__":
    main()
