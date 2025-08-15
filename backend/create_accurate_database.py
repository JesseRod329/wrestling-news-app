#!/usr/bin/env python3
"""
Create Accurate Wrestling Database
Uses the correct Cagematch IDs to fetch accurate data for all top wrestlers
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
        
        # Correct Cagematch IDs from our search
        self.correct_wrestler_ids = {
            "Roman Reigns": "9967",
            "Cody Rhodes": "3686", 
            "Seth Rollins": "2250",
            "Bianca Belair": "18242",
            "Rhea Ripley": "16519",
            "Kenny Omega": "2906",
            "MJF": "17012",
            "Kazuchika Okada": "4324",
            "Will Ospreay": "14028",
            "Brock Lesnar": "669",
            "John Cena": "691",
            "The Rock": "960",
            "Stone Cold Steve Austin": "635",
            "Hulk Hogan": "504",
            "Ric Flair": "1091",
            "Shawn Michaels": "796",
            "Bret Hart": "565",
            "Undertaker": "761",
            "Triple H": "496",
            "Randy Orton": "998",
            "Edge": "932",
            "Christian": "820",
            "Jeff Hardy": "891",
            "Matt Hardy": "99",
            "CM Punk": "80",
            "Daniel Bryan": "86",
            "AJ Styles": "801",
            "Samoa Joe": "676",
            "Shinsuke Nakamura": "56",
            "Finn Balor": "2742",
            "Kevin Owens": "1499",
            "Sami Zayn": "1523",
            "Bobby Lashley": "1194",
            "Drew McIntyre": "2879"
        }
        
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
            print(f"   Profile: {profile_url}")
            print(f"   Stats: {stats_url}")
            
            # Fetch profile page
            profile_response = self.session.get(profile_url, timeout=15)
            profile_response.raise_for_status()
            profile_soup = BeautifulSoup(profile_response.content, 'html.parser')
            
            # Fetch stats page
            stats_response = self.session.get(stats_url, timeout=15)
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
            
            print(f"   ✅ Successfully parsed data for: {name}")
            return wrestler_data
            
        except Exception as e:
            print(f"   ❌ Error fetching profile for {name}: {e}")
            return None
    
    def _parse_profile_page(self, soup: BeautifulSoup, name: str) -> Dict[str, Any]:
        """Parse the profile page HTML using the correct Cagematch structure"""
        data = {}
        
        try:
            # Find all InformationBoxTable divs
            info_tables = soup.find_all('div', {'class': 'InformationBoxTable'})
            
            for table in info_tables:
                rows = table.find_all('div', {'class': 'InformationBoxRow'})
                
                for row in rows:
                    title_div = row.find('div', {'class': 'InformationBoxTitle'})
                    content_div = row.find('div', {'class': 'InformationBoxContents'})
                    
                    if title_div and content_div:
                        title = title_div.get_text(strip=True)
                        content = content_div.get_text(strip=True)
                        
                        # Parse specific fields
                        if title == "Current gimmick":
                            data["current_gimmick"] = content
                        elif title == "Age":
                            data["age"] = content
                            # Extract numeric age
                            age_match = re.search(r'(\d+)', content)
                            if age_match:
                                data["age_numeric"] = int(age_match.group(1))
                        elif title == "Promotion":
                            data["promotion"] = content
                        elif title == "Brand":
                            data["brand"] = content
                        elif title == "Roles":
                            data["roles"] = [content]
                        elif title == "Hometown":
                            data["hometown"] = content
                        elif title == "Gender":
                            data["gender"] = content
                        elif title == "Height":
                            data["height"] = content
                        elif title == "Weight":
                            data["weight"] = content
                        elif title == "Background in sports":
                            data["background_sports"] = content
                        elif title == "Alter egos":
                            data["alter_egos"] = [content]
                        elif title == "Debut":
                            data["debut"] = content
                        elif title == "Experience":
                            data["experience"] = content
                        elif title == "Wrestling style":
                            data["wrestling_style"] = content
                        elif title == "Trainers":
                            data["trainers"] = [content]
                        elif title == "Nicknames":
                            data["nicknames"] = [content]
                        elif title == "Signature moves":
                            data["signature_moves"] = [content]
            
            # Try to find real name
            real_name_elem = soup.find('div', string=re.compile(r'Real name:', re.IGNORECASE))
            if real_name_elem:
                real_name_text = real_name_elem.get_text(strip=True)
                real_name_match = re.search(r'Real name:\s*(.+)', real_name_text, re.IGNORECASE)
                if real_name_match:
                    data["real_name"] = real_name_match.group(1).strip()
            
            # Try to find social media links
            social_media = {}
            social_links = soup.find_all('a', href=re.compile(r'(twitter\.com|x\.com|instagram\.com|tiktok\.com|youtube\.com)'))
            for link in social_links:
                href = link['href']
                if 'twitter.com' in href or 'x.com' in href:
                    social_media["Twitter"] = href
                elif 'instagram.com' in href:
                    social_media["Instagram"] = href
                elif 'tiktok.com' in href:
                    social_media["TikTok"] = href
                elif 'youtube.com' in href:
                    social_media["YouTube"] = href
            
            if social_media:
                data["social_media"] = social_media
            
            # Try to find image
            image_elem = soup.find('img', {'class': 'ProfilePicture'})
            if image_elem and image_elem.get('src'):
                data["image_url"] = image_elem['src']
                data["image_source"] = "Cagematch"
            
        except Exception as e:
            print(f"      ⚠️ Error parsing profile: {e}")
        
        return data
    
    def _parse_stats_page(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Parse the stats page HTML"""
        data = {}
        
        try:
            # Look for rating information
            rating_elem = soup.find('div', string=re.compile(r'Average rating:', re.IGNORECASE))
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                rating_match = re.search(r'Average rating:\s*([\d.]+)', rating_text, re.IGNORECASE)
                if rating_match:
                    data["averageRating"] = float(rating_match.group(1))
            
            # Look for vote count
            votes_elem = soup.find('div', string=re.compile(r'Total votes:', re.IGNORECASE))
            if votes_elem:
                votes_text = votes_elem.get_text(strip=True)
                votes_match = re.search(r'Total votes:\s*(\d+)', votes_text, re.IGNORECASE)
                if votes_match:
                    data["total_votes"] = int(votes_match.group(1))
            
            # Look for comment count
            comments_elem = soup.find('div', string=re.compile(r'Total comments:', re.IGNORECASE))
            if comments_elem:
                comments_text = comments_elem.get_text(strip=True)
                comments_match = re.search(r'Total comments:\s*(\d+)', comments_text, re.IGNORECASE)
                if comments_match:
                    data["total_comments"] = int(comments_match.group(1))
                    
        except Exception as e:
            print(f"      ⚠️ Error parsing stats: {e}")
        
        return data
    
    def fetch_all_wrestlers(self) -> List[Dict[str, Any]]:
        """Fetch data for all wrestlers"""
        wrestlers = []
        
        print(f"🚀 Starting to fetch data for {len(self.correct_wrestler_ids)} wrestlers...")
        print("=" * 80)
        
        for i, (name, wrestler_id) in enumerate(self.correct_wrestler_ids.items(), 1):
            print(f"\n[{i}/{len(self.correct_wrestler_ids)}] ", end="")
            
            wrestler_data = self.fetch_wrestler_profile(wrestler_id, name)
            if wrestler_data:
                wrestlers.append(wrestler_data)
            
            # Be respectful with delays
            if i < len(self.correct_wrestler_ids):
                time.sleep(3)
        
        print(f"\n✅ Successfully fetched data for {len(wrestlers)} wrestlers!")
        return wrestlers
    
    def save_database(self, wrestlers: List[Dict[str, Any]]) -> None:
        """Save the accurate wrestling database"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wrestling_database_accurate_final_{timestamp}.json"
        
        database = {
            "metadata": {
                "version": "4.0",
                "created_at": datetime.now().isoformat(),
                "total_wrestlers": len(wrestlers),
                "description": "Comprehensive accurate wrestling database with correct Cagematch IDs",
                "data_source": "Cagematch.net",
                "data_quality": "High - Verified IDs and accurate parsing"
            },
            "wrestlers": wrestlers
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Accurate database saved to: {filename}")
        
        # Also save a simple mapping file
        mapping_filename = f"wrestler_id_mapping_final_{timestamp}.json"
        simple_mapping = {name: self.correct_wrestler_ids[name] for name in self.correct_wrestler_ids.keys()}
        
        with open(mapping_filename, 'w', encoding='utf-8') as f:
            json.dump(simple_mapping, f, indent=2, ensure_ascii=False)
        
        print(f"💾 ID mapping saved to: {mapping_filename}")

def main():
    """Main function"""
    fetcher = AccurateWrestlerDataFetcher()
    
    print("🎯 Creating Accurate Wrestling Database")
    print("=" * 80)
    
    # Fetch all wrestler data
    wrestlers = fetcher.fetch_all_wrestlers()
    
    if wrestlers:
        # Save the database
        fetcher.save_database(wrestlers)
        
        # Display summary
        print("\n📊 Database Summary:")
        print("-" * 50)
        for wrestler in wrestlers:
            print(f"✅ {wrestler['name']}: {wrestler.get('age', 'N/A')} years, {wrestler.get('promotion', 'N/A')}")
        
        print(f"\n🎉 Successfully created accurate database with {len(wrestlers)} wrestlers!")
    else:
        print("❌ No wrestler data fetched!")

if __name__ == "__main__":
    main()
