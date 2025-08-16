#!/usr/bin/env python3
"""
Scrape Recent Match History from Cagematch.net
This script fetches the latest matches for a specific wrestler from their Cagematch profile
"""

import json
import os
import time
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import re

class CagematchMatchScraper:
    def __init__(self):
        """Initialize the match scraper"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://www.cagematch.net"
        
    def scrape_wrestler_matches(self, wrestler_id: str, wrestler_name: str, max_matches: int = 20) -> List[Dict[str, Any]]:
        """
        Scrape recent matches for a specific wrestler
        
        Args:
            wrestler_id: Cagematch wrestler ID
            wrestler_name: Name of the wrestler
            max_matches: Maximum number of matches to scrape
            
        Returns:
            List of match dictionaries
        """
        try:
            # Construct the matches page URL
            matches_url = f"{self.base_url}/?id=2&nr={wrestler_id}&page=4"
            
            print(f"🔍 Scraping matches for {wrestler_name} from: {matches_url}")
            
            response = self.session.get(matches_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the matches table
            matches_table = soup.find('table', {'class': 'TblContent'})
            if not matches_table:
                print("❌ No matches table found")
                return []
            
            matches = []
            rows = matches_table.find_all('tr')[1:]  # Skip header row
            
            for row in rows[:max_matches]:
                match_data = self._parse_match_row(row, wrestler_name)
                if match_data:
                    matches.append(match_data)
            
            print(f"✅ Successfully scraped {len(matches)} matches for {wrestler_name}")
            return matches
            
        except Exception as e:
            print(f"❌ Error scraping matches for {wrestler_name}: {str(e)}")
            return []
    
    def _parse_match_row(self, row, wrestler_name: str) -> Optional[Dict[str, Any]]:
        """Parse a single match row from the table"""
        try:
            cells = row.find_all('td')
            if len(cells) < 4:
                return None
            
            # Extract match information
            date_cell = cells[0].get_text(strip=True)
            promotion_cell = cells[1]
            match_cell = cells[2]
            
            # Parse date
            date = self._parse_date(date_cell)
            
            # Parse promotion
            promotion = self._extract_promotion(promotion_cell)
            
            # Parse match details
            match_info = self._parse_match_details(match_cell, wrestler_name)
            
            if not match_info:
                return None
            
            return {
                'date': date,
                'promotion': promotion,
                'event': match_info.get('event', ''),
                'match_type': match_info.get('match_type', ''),
                'participants': match_info.get('participants', []),
                'result': match_info.get('result', ''),
                'duration': match_info.get('duration', ''),
                'location': match_info.get('location', ''),
                'title': match_info.get('title', '')
            }
            
        except Exception as e:
            print(f"❌ Error parsing match row: {str(e)}")
            return None
    
    def _parse_date(self, date_text: str) -> str:
        """Parse date from Cagematch format (DD.MM.YYYY) to ISO format"""
        try:
            if '.' in date_text:
                day, month, year = date_text.split('.')
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            return date_text
        except:
            return date_text
    
    def _extract_promotion(self, promotion_cell) -> str:
        """Extract promotion name from cell"""
        try:
            # Look for promotion link
            promotion_link = promotion_cell.find('a')
            if promotion_link:
                return promotion_link.get_text(strip=True)
            
            # Fallback to cell text
            return promotion_cell.get_text(strip=True)
        except:
            return "Unknown"
    
    def _parse_match_details(self, match_cell, wrestler_name: str) -> Optional[Dict[str, Any]]:
        """Parse match details from the match cell"""
        try:
            match_text = match_cell.get_text(strip=True)
            
            # Extract title if present (look for text in brackets or after colon)
            title = None
            if ':' in match_text:
                title_part = match_text.split(':')[0]
                if any(keyword in title_part.lower() for keyword in ['title', 'championship', 'belt']):
                    title = title_part.strip()
            
            # Extract match type
            match_type = self._extract_match_type(match_text)
            
            # Extract participants and result
            participants, result = self._extract_participants_and_result(match_text, wrestler_name)
            
            # Extract duration (look for pattern like (XX:XX))
            duration = None
            duration_match = re.search(r'\((\d{1,2}:\d{2})\)', match_text)
            if duration_match:
                duration = duration_match.group(1)
            
            # Extract location (look for @ symbol)
            location = None
            if '@' in match_text:
                location_part = match_text.split('@')[-1].strip()
                location = location_part
            
            # Extract event name (usually before the match details)
            event = self._extract_event_name(match_text)
            
            return {
                'title': title,
                'match_type': match_type,
                'participants': participants,
                'result': result,
                'duration': duration,
                'location': location,
                'event': event
            }
            
        except Exception as e:
            print(f"❌ Error parsing match details: {str(e)}")
            return None
    
    def _extract_match_type(self, match_text: str) -> str:
        """Extract match type from match text"""
        match_types = [
            'Triple Threat', 'Fatal 4-Way', 'Elimination Chamber', 'Royal Rumble',
            'Tag Team', 'Singles', 'Battle Royal', 'Ladder Match', 'Tables Match',
            'Steel Cage', 'Hell in a Cell', 'TLC', 'Money in the Bank'
        ]
        
        for match_type in match_types:
            if match_type.lower() in match_text.lower():
                return match_type
        
        return "Singles"  # Default
    
    def _extract_participants_and_result(self, match_text: str, wrestler_name: str) -> tuple:
        """Extract participants and result from match text"""
        try:
            # Look for vs pattern
            if ' vs ' in match_text:
                parts = match_text.split(' vs ')
                participants = [p.strip() for p in parts]
                result = f"{participants[0]} defeats {participants[1]}"
                return participants, result
            
            # Look for defeat pattern
            if 'defeats' in match_text:
                parts = match_text.split('defeats')
                winner = parts[0].strip()
                loser = parts[1].strip()
                participants = [winner, loser]
                result = match_text
                return participants, result
            
            # Fallback: extract names from text
            names = re.findall(r'\[([^\]]+)\]', match_text)
            if names:
                participants = names
                result = match_text
                return participants, result
            
            return [wrestler_name], match_text
            
        except:
            return [wrestler_name], match_text
    
    def _extract_event_name(self, match_text: str) -> str:
        """Extract event name from match text"""
        try:
            # Look for event patterns
            if '[' in match_text and ']' in match_text:
                event_match = re.search(r'\[([^\]]+)\]', match_text)
                if event_match:
                    return event_match.group(1)
            
            return "Unknown Event"
        except:
            return "Unknown Event"
    
    def save_matches_to_file(self, matches: List[Dict[str, Any]], wrestler_name: str, wrestler_id: str):
        """Save scraped matches to a JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"matches_{wrestler_name.lower().replace(' ', '_')}_{wrestler_id}_{timestamp}.json"
        
        data = {
            'wrestler_name': wrestler_name,
            'wrestler_id': wrestler_id,
            'scraped_at': datetime.now().isoformat(),
            'total_matches': len(matches),
            'matches': matches
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(matches)} matches to {filename}")
        return filename

def main():
    """Main function to test the scraper"""
    scraper = CagematchMatchScraper()
    
    # Test with Bianca Belair (ID: 18242)
    test_wrestlers = [
        {"id": "18242", "name": "Bianca Belair"},
        {"id": "9967", "name": "Roman Reigns"},
        {"id": "3686", "name": "Cody Rhodes"}
    ]
    
    for wrestler in test_wrestlers:
        print(f"\n{'='*60}")
        print(f"Scraping matches for {wrestler['name']} (ID: {wrestler['id']})")
        print(f"{'='*60}")
        
        matches = scraper.scrape_wrestler_matches(
            wrestler['id'], 
            wrestler['name'], 
            max_matches=10
        )
        
        if matches:
            # Save to file
            filename = scraper.save_matches_to_file(matches, wrestler['name'], wrestler['id'])
            
            # Display sample matches
            print(f"\n📊 Sample matches for {wrestler['name']}:")
            for i, match in enumerate(matches[:3], 1):
                print(f"\n{i}. {match['date']} - {match['promotion']}")
                print(f"   Event: {match['event']}")
                print(f"   Type: {match['match_type']}")
                print(f"   Result: {match['result']}")
                if match['duration']:
                    print(f"   Duration: {match['duration']}")
                if match['location']:
                    print(f"   Location: {match['location']}")
        
        # Rate limiting
        time.sleep(2)
    
    print(f"\n{'='*60}")
    print("✅ Match scraping completed!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
