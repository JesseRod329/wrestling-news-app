#!/usr/bin/env python3
"""
Fetch Accurate Wrestler Data
This script fetches real, accurate data for wrestlers from Cagematch.net and other sources
"""

import json
import os
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import re

class AccurateWrestlerDataFetcher:
    def __init__(self):
        """Initialize the data fetcher"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://www.cagematch.net"
        
    def search_wrestler(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Search for a wrestler on Cagematch.net
        
        Args:
            name (str): Wrestler name to search for
            
        Returns:
            dict: Search result with ID and basic info
        """
        try:
            # Search URL
            search_url = f"{self.base_url}/?id=2&view=search&s={name.replace(' ', '+')}"
            
            print(f"🔍 Searching for: {name}")
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the first wrestler result
            wrestler_link = soup.find('a', href=re.compile(r'\?id=2&nr=\d+'))
            
            if wrestler_link:
                # Extract wrestler ID from URL
                href = wrestler_link.get('href', '')
                match = re.search(r'nr=(\d+)', href)
                if match:
                    wrestler_id = match.group(1)
                    return {
                        'id': wrestler_id,
                        'name': name,
                        'url': f"{self.base_url}/?id=2&nr={wrestler_id}",
                        'found': True
                    }
            
            print(f"❌ No results found for: {name}")
            return None
            
        except Exception as e:
            print(f"❌ Error searching for {name}: {e}")
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
            profile_response = self.session.get(profile_url, timeout=10)
            profile_response.raise_for_status()
            profile_soup = BeautifulSoup(profile_response.content, 'html.parser')
            
            # Fetch stats page
            stats_response = self.session.get(stats_url, timeout=10)
            stats_response.raise_for_status()
            stats_soup = BeautifulSoup(stats_response.content, 'html.parser')
            
            # Parse profile data
            profile_data = self._parse_profile_page(profile_soup, name)
            
            # Parse stats data
            stats_data = self._parse_stats_page(stats_soup)
            
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
            
            print(f"✅ Successfully fetched data for: {name}")
            return wrestler_data
            
        except Exception as e:
            print(f"❌ Error fetching profile for {name}: {e}")
            return None
    
    def _parse_profile_page(self, soup: BeautifulSoup, name: str) -> Dict[str, Any]:
        """Parse the profile page HTML to extract wrestler information"""
        data = {}
        
        try:
            # Find the main content table
            content_table = soup.find('table', {'class': 'TblContent'})
            if not content_table:
                return data
            
            # Extract basic information
            rows = content_table.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    label = cells[0].get_text(strip=True).lower()
                    value = cells[1].get_text(strip=True)
                    
                    if 'birth' in label and 'date' in label:
                        data['birth_date'] = value
                        # Calculate age
                        if value:
                            try:
                                birth_year = int(value.split('.')[-1])
                                current_year = datetime.now().year
                                data['age'] = current_year - birth_year
                            except:
                                data['age'] = None
                    
                    elif 'height' in label:
                        data['height'] = value
                    
                    elif 'weight' in label:
                        data['weight'] = value
                    
                    elif 'birthplace' in label or 'born' in label:
                        data['hometown'] = value
                    
                    elif 'promotion' in label:
                        data['promotion'] = value
                    
                    elif 'experience' in label:
                        data['experience'] = value
                    
                    elif 'style' in label:
                        data['wrestling_style'] = value
                    
                    elif 'rating' in label and 'average' in label:
                        try:
                            data['averageRating'] = float(value)
                        except:
                            data['averageRating'] = None
                    
                    elif 'votes' in label and 'total' in label:
                        try:
                            data['total_votes'] = int(value.replace(',', ''))
                        except:
                            data['total_votes'] = None
            
            # Extract nicknames
            nickname_section = soup.find('td', text=re.compile(r'Nicknames?', re.IGNORECASE))
            if nickname_section:
                nickname_cell = nickname_section.find_next('td')
                if nickname_cell:
                    nicknames = [nick.strip() for nick in nickname_cell.get_text().split(',') if nick.strip()]
                    data['nicknames'] = nicknames
            
            # Extract signature moves
            moves_section = soup.find('td', text=re.compile(r'Signature Moves?', re.IGNORECASE))
            if moves_section:
                moves_cell = moves_section.find_next('td')
                if moves_cell:
                    moves = [move.strip() for move in moves_cell.get_text().split(',') if move.strip()]
                    data['signature_moves'] = moves
            
            # Extract championships
            championships = []
            championship_section = soup.find('td', text=re.compile(r'Championships?', re.IGNORECASE))
            if championship_section:
                championship_cell = championship_section.find_next('td')
                if championship_cell:
                    champ_text = championship_cell.get_text()
                    # Parse championship text
                    champ_matches = re.findall(r'([^,]+?)\s*\(([^)]+)\)', champ_text)
                    for title, reign in champ_matches:
                        championships.append(f"{title.strip()} ({reign.strip()})")
            
            if championships:
                data['championships'] = championships
            
            # Extract career highlights
            highlights = []
            highlights_section = soup.find('td', text=re.compile(r'Career Highlights?', re.IGNORECASE))
            if highlights_section:
                highlights_cell = highlights_section.find_next('td')
                if highlights_cell:
                    highlight_text = highlights_cell.get_text()
                    highlights = [h.strip() for h in highlight_text.split(',') if h.strip()]
            
            if highlights:
                data['career_highlights'] = highlights
            
        except Exception as e:
            print(f"⚠️ Error parsing profile page: {e}")
        
        return data
    
    def _parse_stats_page(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Parse the stats page HTML to extract match statistics"""
        data = {}
        
        try:
            # Find match statistics
            stats_table = soup.find('table', {'class': 'TblContent'})
            if not stats_table:
                return data
            
            # Look for total matches, wins, losses
            rows = stats_table.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    label = cells[0].get_text(strip=True).lower()
                    value = cells[1].get_text(strip=True)
                    
                    if 'total matches' in label:
                        try:
                            data['totalMatches'] = int(value.replace(',', ''))
                        except:
                            data['totalMatches'] = 0
                    
                    elif 'wins' in label:
                        try:
                            data['wins'] = int(value.replace(',', ''))
                        except:
                            data['wins'] = 0
                    
                    elif 'losses' in label:
                        try:
                            data['losses'] = int(value.replace(',', ''))
                        except:
                            data['losses'] = 0
                    
                    elif 'draws' in label:
                        try:
                            data['draws'] = int(value.replace(',', ''))
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
            print(f"⚠️ Error parsing stats page: {e}")
        
        return data
    
    def fetch_wrestler_image(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Try to fetch wrestler image from Wikipedia
        
        Args:
            name (str): Wrestler name
            
        Returns:
            dict: Image data
        """
        try:
            # Try Wikipedia first
            wiki_url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
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
            print(f"⚠️ Error fetching image for {name}: {e}")
            return None
    
    def process_wrestler_list(self, wrestler_names: List[str]) -> List[Dict[str, Any]]:
        """
        Process a list of wrestler names to fetch accurate data
        
        Args:
            wrestler_names (List[str]): List of wrestler names to process
            
        Returns:
            List[Dict[str, Any]]: List of wrestler data
        """
        accurate_wrestlers = []
        
        for i, name in enumerate(wrestler_names):
            print(f"\n{'='*50}")
            print(f"Processing {i+1}/{len(wrestler_names)}: {name}")
            print(f"{'='*50}")
            
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
                    profile_data.setdefault('nickname', f"The {name.split()[-1]}")
                    profile_data.setdefault('real_name', name)
                    
                    accurate_wrestlers.append(profile_data)
                    
                    print(f"✅ Added accurate data for: {name}")
                else:
                    print(f"❌ Failed to fetch profile for: {name}")
            else:
                print(f"❌ Wrestler not found: {name}")
            
            # Rate limiting to be respectful
            time.sleep(2)
        
        return accurate_wrestlers
    
    def save_accurate_database(self, wrestlers: List[Dict[str, Any]]) -> None:
        """Save the accurate wrestler database"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wrestling_database_accurate_{timestamp}.json"
        
        database = {
            "metadata": {
                "version": "3.0",
                "created_at": datetime.now().isoformat(),
                "total_wrestlers": len(wrestlers),
                "description": "Accurate wrestling database with real data from Cagematch.net",
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
    print("🎯 Fetching Accurate Wrestler Data from Cagematch.net")
    print("=" * 60)
    
    # Initialize fetcher
    fetcher = AccurateWrestlerDataFetcher()
    
    # List of wrestlers to fetch accurate data for
    wrestler_names = [
        "Roman Reigns", "Cody Rhodes", "Seth Rollins", "Bianca Belair", "Rhea Ripley",
        "Kenny Omega", "MJF", "Kazuchika Okada", "Will Ospreay", "Brock Lesnar",
        "John Cena", "The Rock", "Stone Cold Steve Austin", "Hulk Hogan",
        "Ric Flair", "Shawn Michaels", "Bret Hart", "Undertaker", "Triple H",
        "Randy Orton", "Edge", "Christian", "Jeff Hardy", "Matt Hardy",
        "CM Punk", "Daniel Bryan", "AJ Styles", "Samoa Joe", "Shinsuke Nakamura",
        "Finn Balor", "Kevin Owens", "Sami Zayn", "Bobby Lashley", "Drew McIntyre"
    ]
    
    print(f"🎯 Will fetch accurate data for {len(wrestler_names)} wrestlers")
    print("⚠️ This will take some time due to rate limiting...")
    
    # Process wrestlers
    accurate_wrestlers = fetcher.process_wrestler_list(wrestler_names)
    
    # Save accurate database
    if accurate_wrestlers:
        fetcher.save_accurate_database(accurate_wrestlers)
        print(f"\n🎉 Successfully fetched accurate data for {len(accurate_wrestlers)} wrestlers!")
    else:
        print("\n❌ No accurate data was fetched!")

if __name__ == "__main__":
    main()
