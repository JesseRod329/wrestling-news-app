#!/usr/bin/env python3
"""
Find Correct Cagematch IDs for Top Wrestlers
This script searches for wrestlers by name and extracts their correct Cagematch IDs
"""

import json
import os
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import re

class CagematchIDFinder:
    def __init__(self):
        """Initialize the ID finder"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://www.cagematch.net"
        
        # List of top wrestlers to find IDs for
        self.top_wrestlers = [
            "Roman Reigns",
            "Cody Rhodes", 
            "Seth Rollins",
            "Bianca Belair",
            "Rhea Ripley",
            "Kenny Omega",
            "MJF",
            "Kazuchika Okada",
            "Will Ospreay",
            "Brock Lesnar",
            "John Cena",
            "The Rock",
            "Stone Cold Steve Austin",
            "Hulk Hogan",
            "Ric Flair",
            "Shawn Michaels",
            "Bret Hart",
            "Undertaker",
            "Triple H",
            "Randy Orton",
            "Edge",
            "Christian",
            "Jeff Hardy",
            "Matt Hardy",
            "CM Punk",
            "Daniel Bryan",
            "AJ Styles",
            "Samoa Joe",
            "Shinsuke Nakamura",
            "Finn Balor",
            "Kevin Owens",
            "Sami Zayn",
            "Bobby Lashley",
            "Drew McIntyre"
        ]
        
    def search_wrestler(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Search for a wrestler by name and extract their Cagematch ID
        
        Args:
            name (str): Wrestler name to search for
            
        Returns:
            dict: Wrestler info with ID, or None if not found
        """
        try:
            # Search URL for wrestlers
            search_url = f"{self.base_url}/?id=4&view=search&s={name.replace(' ', '+')}"
            
            print(f"🔍 Searching for: {name}")
            print(f"   Search URL: {search_url}")
            
            # Fetch search results
            response = self.session.get(search_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for wrestler links in search results
            wrestler_links = soup.find_all('a', href=re.compile(r'\?id=2&nr=\d+'))
            
            if not wrestler_links:
                print(f"   ❌ No wrestler links found for: {name}")
                return None
            
            # Find the best match (exact name match first)
            best_match = None
            best_score = 0
            
            for link in wrestler_links:
                link_text = link.get_text(strip=True)
                wrestler_id = re.search(r'nr=(\d+)', link['href'])
                
                if not wrestler_id:
                    continue
                    
                wrestler_id = wrestler_id.group(1)
                
                # Calculate match score
                score = self._calculate_name_similarity(name, link_text)
                
                print(f"      Found: {link_text} (ID: {wrestler_id}, Score: {score})")
                
                if score > best_score:
                    best_score = score
                    best_match = {
                        "name": link_text,
                        "cagematch_id": wrestler_id,
                        "search_score": score,
                        "profile_url": f"{self.base_url}/?id=2&nr={wrestler_id}"
                    }
            
            if best_match and best_match["search_score"] >= 0.7:  # Good match threshold
                print(f"   ✅ Best match: {best_match['name']} (ID: {best_match['cagematch_id']}, Score: {best_match['search_score']:.2f})")
                return best_match
            else:
                print(f"   ❌ No good match found for: {name}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error searching for {name}: {e}")
            return None
    
    def _calculate_name_similarity(self, search_name: str, found_name: str) -> float:
        """
        Calculate similarity score between search name and found name
        
        Args:
            search_name (str): Original search name
            found_name (str): Name found in search results
            
        Returns:
            float: Similarity score (0.0 to 1.0)
        """
        search_lower = search_name.lower()
        found_lower = found_name.lower()
        
        # Exact match
        if search_lower == found_lower:
            return 1.0
        
        # Contains search name
        if search_lower in found_lower:
            return 0.9
        
        # Contains found name
        if found_lower in search_lower:
            return 0.8
        
        # Check for partial matches
        search_words = set(search_lower.split())
        found_words = set(found_lower.split())
        
        if search_words & found_words:  # Intersection
            intersection = len(search_words & found_words)
            union = len(search_words | found_words)
            return intersection / union
        
        return 0.0
    
    def find_all_wrestler_ids(self) -> Dict[str, Dict[str, Any]]:
        """
        Find Cagematch IDs for all top wrestlers
        
        Returns:
            dict: Mapping of wrestler names to their info
        """
        results = {}
        
        print(f"🚀 Starting search for {len(self.top_wrestlers)} top wrestlers...")
        print("=" * 60)
        
        for i, wrestler_name in enumerate(self.top_wrestlers, 1):
            print(f"\n[{i}/{len(self.top_wrestlers)}] ", end="")
            
            result = self.search_wrestler(wrestler_name)
            if result:
                results[wrestler_name] = result
            
            # Be respectful with delays
            if i < len(self.top_wrestlers):
                time.sleep(2)
        
        print("\n" + "=" * 60)
        print(f"✅ Search completed! Found {len(results)} wrestlers")
        
        return results
    
    def save_results(self, results: Dict[str, Dict[str, Any]]) -> None:
        """Save the search results to a JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"correct_cagematch_ids_{timestamp}.json"
        
        data = {
            "metadata": {
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "total_wrestlers": len(results),
                "description": "Correct Cagematch IDs for top wrestlers found through systematic search"
            },
            "wrestlers": results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {filename}")
        
        # Also save a simple mapping file
        mapping_filename = f"wrestler_id_mapping_{timestamp}.json"
        simple_mapping = {name: info["cagematch_id"] for name, info in results.items()}
        
        with open(mapping_filename, 'w', encoding='utf-8') as f:
            json.dump(simple_mapping, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Simple mapping saved to: {mapping_filename}")

def main():
    """Main function"""
    finder = CagematchIDFinder()
    
    print("🎯 Cagematch ID Finder for Top Wrestlers")
    print("=" * 60)
    
    # Find all wrestler IDs
    results = finder.find_all_wrestler_ids()
    
    if results:
        # Save results
        finder.save_results(results)
        
        # Display summary
        print("\n📊 Search Summary:")
        print("-" * 40)
        for name, info in results.items():
            print(f"✅ {name}: {info['name']} (ID: {info['cagematch_id']})")
        
        print(f"\n🎉 Successfully found {len(results)} out of {len(finder.top_wrestlers)} wrestlers!")
    else:
        print("❌ No wrestler IDs found!")

if __name__ == "__main__":
    main()
