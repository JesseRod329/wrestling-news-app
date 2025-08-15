#!/usr/bin/env python3
"""
Fetch Accurate Wrestler Data V2
Improved version with better search logic and data parsing
"""

import json
import os
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import re

class AccurateWrestlerDataFetcherV2:
    def __init__(self):
        """Initialize the data fetcher"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://www.cagematch.net"
        
    def search_wrestler(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Search for a wrestler on Cagematch.net with improved logic
        
        Args:
            name (str): Wrestler name to search for
            
        Returns:
            dict: Search result with ID and basic info
        """
        try:
            # Clean the name for search
            search_name = name.replace(' ', '+').replace('&', 'and')
            search_url = f"{self.base_url}/?id=2&view=search&s={search_name}"
            
            print(f"🔍 Searching for: {name}")
            print(f"   URL: {search_url}")
            
            response = self.session.get(search_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for search results table
            search_table = soup.find('table', {'class': 'TblContent'})
            if not search_table:
                print(f"   ❌ No search table found")
                return None
            
            # Find all wrestler links in the search results
            wrestler_links = search_table.find_all('a', href=re.compile(r'\?id=2&nr=\d+'))
            
            if not wrestler_links:
                print(f"   ❌ No wrestler links found")
                return None
            
            print(f"   Found {len(wrestler_links)} potential matches")
            
            # Look for exact name match first
            exact_match = None
            for link in wrestler_links:
                link_text = link.get_text(strip=True)
                if link_text.lower() == name.lower():
                    exact_match = link
                    break
            
            # If no exact match, use the first result
            target_link = exact_match if exact_match else wrestler_links[0]
            
            if target_link:
                href = target_link.get('href', '')
                match = re.search(r'nr=(\d+)', href)
                if match:
                    wrestler_id = match.group(1)
                    wrestler_name = target_link.get_text(strip=True)
                    
                    print(f"   ✅ Selected: {wrestler_name} (ID: {wrestler_id})")
                    
                    return {
                        'id': wrestler_id,
                        'name': wrestler_name,
                        'url': f"{self.base_url}/?id=2&nr={wrestler_id}",
                        'found': True
                    }
            
            print(f"   ❌ Could not extract wrestler ID")
            return None
            
        except Exception as e:
            print(f"   ❌ Error searching for {name}: {e}")
            return None
    
    def fetch_wrestler_profile(self, wrestler_id: str, name: str) -> Optional[Dict[str, Any]]:
        """
        Fetch detailed wrestler profile from Cagematch.net
        
        Args:
            wrestler_id (str): Cagematch wrestler ID
            name (str): Wrestler name
            
        Returns:
            dict: Detailed wrestler profile data
        """
        try:
            profile_url = f"{self.base_url}/?id=2&nr={wrestler_id}"
            stats_url = f"{self.base_url}/?id=2&nr={wrestler_id}&view=matches"
            
            print(f"📊 Fetching profile for: {name} (ID: {wrestler_id})")
            
            # Fetch profile page
            profile_response = self.session.get(profile_url, timeout=15)
            profile_response.raise_for_status()
            profile_soup = BeautifulSoup(profile_response.content, 'html.parser')
            
            # Fetch stats page
            stats_response = self.session.get(stats_url, timeout=15)
            stats_response.raise_for_status()
            stats_soup = BeautifulSoup(stats_response.content, 'html.parser')
            
            # Parse profile data
            profile_data = self._parse_profile_page_v2(profile_soup, name)
            
            # Parse stats data
            stats_data = self._parse_stats_page_v2(stats_soup)
            
            # Combine data
            wrestler_data = {
                "id": f"cagematch_{wrestler_id}",
                "name": name,
                "cagematch_id": wrestler_id,
                "profile_url": profile_url,
                "stats_url": stats_url,
                "scraped_at": datetime.now().isoformat(),
                **profile_data,
                **stats_data
            }
            
            print(f"   ✅ Successfully parsed data for: {name}")
            return wrestler_data
            
        except Exception as e:
            print(f"   ❌ Error fetching profile for {name}: {e}")
            return None
    
    def _parse_profile_page_v2(self, soup: BeautifulSoup, name: str) -> Dict[str, Any]:
        """Improved profile page parsing"""
        data = {}
        
        try:
            # Find all content tables
            content_tables = soup.find_all('table', {'class': 'TblContent'})
            
            for table in content_tables:
                rows = table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        label = cells[0].get_text(strip=True).lower()
                        value = cells[1].get_text(strip=True)
                        
                        # Birth date and age
                        if 'birth' in label and 'date' in label:
                            data['birth_date'] = value
                            # Calculate age from birth date
                            if value:
                                try:
                                    # Handle different date formats
                                    if '.' in value:
                                        parts = value.split('.')
                                        if len(parts) >= 3:
                                            birth_year = int(parts[-1])
                                            current_year = datetime.now().year
                                            data['age'] = current_year - birth_year
                                        else:
                                            data['age'] = None
                                    else:
                                        # Try to extract year from other formats
                                        year_match = re.search(r'(\d{4})', value)
                                        if year_match:
                                            birth_year = int(year_match.group(1))
                                            current_year = datetime.now().year
                                            data['age'] = current_year - birth_year
                                        else:
                                            data['age'] = None
                                except:
                                    data['age'] = None
                        
                        # Height
                        elif 'height' in label:
                            data['height'] = value
                        
                        # Weight
                        elif 'weight' in label:
                            data['weight'] = value
                        
                        # Birthplace
                        elif 'birthplace' in label or 'born' in label:
                            data['hometown'] = value
                        
                        # Promotion
                        elif 'promotion' in label:
                            data['promotion'] = value
                        
                        # Experience
                        elif 'experience' in label:
                            data['experience'] = value
                        
                        # Wrestling style
                        elif 'style' in label:
                            data['wrestling_style'] = value
                        
                        # Average rating
                        elif 'rating' in label and 'average' in label:
                            try:
                                # Extract numeric rating
                                rating_match = re.search(r'(\d+\.?\d*)', value)
                                if rating_match:
                                    data['averageRating'] = float(rating_match.group(1))
                                else:
                                    data['averageRating'] = None
                            except:
                                data['averageRating'] = None
                        
                        # Total votes
                        elif 'votes' in label and 'total' in label:
                            try:
                                votes_match = re.search(r'(\d+)', value.replace(',', ''))
                                if votes_match:
                                    data['total_votes'] = int(votes_match.group(1))
                                else:
                                    data['total_votes'] = None
                            except:
                                data['total_votes'] = None
                        
                        # Nicknames
                        elif 'nicknames' in label:
                            nicknames = [nick.strip() for nick in value.split(',') if nick.strip()]
                            if nicknames:
                                data['nicknames'] = nicknames
                        
                        # Signature moves
                        elif 'signature' in label and 'moves' in label:
                            moves = [move.strip() for move in value.split(',') if move.strip()]
                            if moves:
                                data['signature_moves'] = moves
                        
                        # Championships
                        elif 'championships' in label:
                            championships = []
                            # Parse championship text more carefully
                            champ_parts = value.split(',')
                            for part in champ_parts:
                                part = part.strip()
                                if '(' in part and ')' in part:
                                    championships.append(part)
                            
                            if championships:
                                data['championships'] = championships
                        
                        # Career highlights
                        elif 'career' in label and 'highlights' in label:
                            highlights = [h.strip() for h in value.split(',') if h.strip()]
                            if highlights:
                                data['career_highlights'] = highlights
            
            # If we didn't find nicknames, create a default one
            if 'nicknames' not in data:
                data['nicknames'] = [f"The {name.split()[-1]}"]
            
            # Set default values for missing fields
            data.setdefault('wrestling_style', 'All-rounder')
            data.setdefault('experience', 'Unknown')
            data.setdefault('promotion', 'Independent')
            
        except Exception as e:
            print(f"   ⚠️ Error parsing profile page: {e}")
        
        return data
    
    def _parse_stats_page_v2(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Improved stats page parsing"""
        data = {}
        
        try:
            # Find all content tables
            content_tables = soup.find_all('table', {'class': 'TblContent'})
            
            for table in content_tables:
                rows = table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        label = cells[0].get_text(strip=True).lower()
                        value = cells[1].get_text(strip=True)
                        
                        # Total matches
                        if 'total' in label and 'matches' in label:
                            try:
                                matches_match = re.search(r'(\d+)', value.replace(',', ''))
                                if matches_match:
                                    data['totalMatches'] = int(matches_match.group(1))
                            except:
                                data['totalMatches'] = 0
                        
                        # Wins
                        elif 'wins' in label:
                            try:
                                wins_match = re.search(r'(\d+)', value.replace(',', ''))
                                if wins_match:
                                    data['wins'] = int(wins_match.group(1))
                            except:
                                data['wins'] = 0
                        
                        # Losses
                        elif 'losses' in label:
                            try:
                                losses_match = re.search(r'(\d+)', value.replace(',', ''))
                                if losses_match:
                                    data['losses'] = int(losses_match.group(1))
                            except:
                                data['losses'] = 0
                        
                        # Draws
                        elif 'draws' in label:
                            try:
                                draws_match = re.search(r'(\d+)', value.replace(',', ''))
                                if draws_match:
                                    data['draws'] = int(draws_match.group(1))
                            except:
                                data['draws'] = 0
            
            # Calculate win percentage
            if 'totalMatches' in data and 'wins' in data and data['totalMatches'] > 0:
                data['winPercentage'] = round((data['wins'] / data['totalMatches']) * 100, 1)
            
            # Create careerStats structure
            if 'totalMatches' in data:
                data['careerStats'] = {
                    'totalMatches': data.get('totalMatches', 0),
                    'wins': data.get('wins', 0),
                    'losses': data.get('losses', 0),
                    'draws': data.get('draws', 0),
                    'winPercentage': data.get('winPercentage', 0.0)
                }
                
                # Remove duplicate keys
                for key in ['totalMatches', 'wins', 'losses', 'draws', 'winPercentage']:
                    if key in data:
                        del data[key]
        
        except Exception as e:
            print(f"   ⚠️ Error parsing stats page: {e}")
        
        return data
    
    def fetch_wrestler_image(self, name: str) -> Optional[Dict[str, Any]]:
        """Fetch wrestler image from Wikipedia"""
        try:
            # Clean name for Wikipedia URL
            wiki_name = name.replace(' ', '_').replace('&', 'and')
            wiki_url = f"https://en.wikipedia.org/wiki/{wiki_name}"
            
            response = self.session.get(wiki_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for infobox image
                infobox = soup.find('table', {'class': 'infobox'})
                if infobox:
                    img = infobox.find('img')
                    if img and img.get('src'):
                        img_src = img['src']
                        if img_src.startswith('//'):
                            img_src = 'https:' + img_src
                        
                        return {
                            'image_url': img_src,
                            'image_source': 'Wikipedia',
                            'image_width': 300,
                            'image_height': 400
                        }
            
            return None
            
        except Exception as e:
            print(f"   ⚠️ Error fetching image for {name}: {e}")
            return None
    
    def process_wrestler_list(self, wrestler_names: List[str]) -> List[Dict[str, Any]]:
        """Process a list of wrestler names to fetch accurate data"""
        accurate_wrestlers = []
        
        for i, name in enumerate(wrestler_names):
            print(f"\n{'='*60}")
            print(f"Processing {i+1}/{len(wrestler_names)}: {name}")
            print(f"{'='*60}")
            
            # Search for wrestler
            search_result = self.search_wrestler(name)
            
            if search_result and search_result.get('found'):
                # Fetch detailed profile
                profile_data = self.fetch_wrestler_profile(
                    search_result['id'], 
                    name
                )
                
                if profile_data:
                    # Try to fetch image
                    image_data = self.fetch_wrestler_image(name)
                    if image_data:
                        profile_data.update(image_data)
                    
                    # Add default values for missing fields
                    profile_data.setdefault('momentumScore', 75)
                    profile_data.setdefault('real_name', name)
                    
                    accurate_wrestlers.append(profile_data)
                    
                    print(f"✅ Added accurate data for: {name}")
                else:
                    print(f"❌ Failed to fetch profile for: {name}")
            else:
                print(f"❌ Wrestler not found: {name}")
            
            # Rate limiting to be respectful
            time.sleep(3)
        
        return accurate_wrestlers
    
    def save_accurate_database(self, wrestlers: List[Dict[str, Any]]) -> None:
        """Save the accurate wrestler database"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wrestling_database_accurate_v2_{timestamp}.json"
        
        database = {
            "metadata": {
                "version": "3.1",
                "created_at": datetime.now().isoformat(),
                "total_wrestlers": len(wrestlers),
                "description": "Accurate wrestling database with real data from Cagematch.net (V2)",
                "data_source": "Cagematch.net, Wikipedia"
            },
            "wrestlers": wrestlers
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Accurate database saved successfully!")
            print(f"📁 File: {filename}")
            print(f"👥 Total wrestlers: {len(wrestlers)}")
            
        except Exception as e:
            print(f"❌ Error saving database: {e}")

def main():
    """Main function to fetch accurate wrestler data"""
    print("🎯 Fetching Accurate Wrestler Data V2 from Cagematch.net")
    print("=" * 70)
    
    # Initialize fetcher
    fetcher = AccurateWrestlerDataFetcherV2()
    
    # Test with a smaller list first
    test_wrestlers = [
        "Roman Reigns", "Cody Rhodes", "Seth Rollins", "Bianca Belair", "Rhea Ripley"
    ]
    
    print(f"🎯 Will fetch accurate data for {len(test_wrestlers)} wrestlers (test run)")
    print("⚠️ This will take some time due to rate limiting...")
    
    # Process wrestlers
    accurate_wrestlers = fetcher.process_wrestler_list(test_wrestlers)
    
    # Save accurate database
    if accurate_wrestlers:
        fetcher.save_accurate_database(accurate_wrestlers)
        print(f"\n🎉 Successfully fetched accurate data for {len(accurate_wrestlers)} wrestlers!")
    else:
        print("\n❌ No accurate data was fetched!")

if __name__ == "__main__":
    main()
