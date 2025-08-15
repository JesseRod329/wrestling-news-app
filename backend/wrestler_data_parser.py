import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

class WrestlerDataParser:
    """Parse scraped wrestling data into structured format for database storage."""
    
    def __init__(self):
        self.patterns = {
            'age': r'Age:\s*(\d+)\s*years',
            'height': r'Height:\s*([^\\n]+)',
            'weight': r'Weight:\s*([^\\n]+)',
            'birthplace': r'Birthplace:\s*([^\\n]+)',
            'gender': r'Gender:\s*([^\\n]+)',
            'promotion': r'Promotion:\s*\[([^\]]+)\]',
            'brand': r'Brand:\s*([^\\n]+)',
            'career_start': r'Beginning of in-ring career:\s*([^\\n]+)',
            'experience': r'In-ring experience:\s*([^\\n]+)',
            'wrestling_style': r'Wrestling style:\s*([^\\n]+)',
            'trainers': r'Trainer:\s*([^\\n]+)',
            'nicknames': r'Nicknames:\s*([^\\n]+)',
            'signature_moves': r'Signature moves:\s*([^\\n]+)',
            'alter_egos': r'Alter egos:\s*([^\\n]+)',
            'roles': r'Roles:\s*([^\\n]+)',
            'rating': r'Average rating:\s*([^\\[]+)',
            'total_votes': r'Valid votes:\s*(\d+)',
            'total_comments': r'Number of comments:\s*(\d+)'
        }
    
    def parse_wrestler_profile(self, markdown_content: str) -> Dict[str, Any]:
        """Extract structured data from wrestler profile markdown."""
        if not markdown_content:
            return {}
        
        profile_data = {}
        
        # Extract basic information
        profile_data['age'] = self._extract_pattern(markdown_content, self.patterns['age'])
        profile_data['height'] = self._extract_pattern(markdown_content, self.patterns['height'])
        profile_data['weight'] = self._extract_pattern(markdown_content, self.patterns['weight'])
        profile_data['birthplace'] = self._extract_pattern(markdown_content, self.patterns['birthplace'])
        profile_data['gender'] = self._extract_pattern(markdown_content, self.patterns['gender'])
        profile_data['promotion'] = self._extract_pattern(markdown_content, self.patterns['promotion'])
        profile_data['brand'] = self._extract_pattern(markdown_content, self.patterns['brand'])
        profile_data['career_start'] = self._extract_pattern(markdown_content, self.patterns['career_start'])
        profile_data['experience'] = self._extract_pattern(markdown_content, self.patterns['experience'])
        profile_data['wrestling_style'] = self._extract_pattern(markdown_content, self.patterns['wrestling_style'])
        
        # Extract trainers
        trainers_text = self._extract_pattern(markdown_content, self.patterns['trainers'])
        profile_data['trainers'] = self._parse_trainers(trainers_text)
        
        # Extract nicknames
        nicknames_text = self._extract_pattern(markdown_content, self.patterns['nicknames'])
        profile_data['nicknames'] = self._parse_nicknames(nicknames_text)
        
        # Extract signature moves
        moves_text = self._extract_pattern(markdown_content, self.patterns['signature_moves'])
        profile_data['signature_moves'] = self._parse_signature_moves(moves_text)
        
        # Extract alter egos
        egos_text = self._extract_pattern(markdown_content, self.patterns['alter_egos'])
        profile_data['alter_egos'] = self._parse_alter_egos(egos_text)
        
        # Extract roles
        roles_text = self._extract_pattern(markdown_content, self.patterns['roles'])
        profile_data['roles'] = self._parse_roles(roles_text)
        
        # Extract ratings
        rating_text = self._extract_pattern(markdown_content, self.patterns['rating'])
        if rating_text:
            # Clean up the rating text and extract the number
            rating_clean = rating_text.strip()
            profile_data['average_rating'] = rating_clean
        
        profile_data['total_votes'] = self._extract_pattern(markdown_content, self.patterns['total_votes'])
        profile_data['total_comments'] = self._extract_pattern(markdown_content, self.patterns['total_comments'])
        
        # Extract yearly ratings
        profile_data['yearly_ratings'] = self._extract_yearly_ratings(markdown_content)
        
        # Extract social media links
        profile_data['social_media'] = self._extract_social_media(markdown_content)
        
        return profile_data
    
    def parse_match_statistics(self, markdown_content: str) -> Dict[str, Any]:
        """Extract match statistics from the stats page."""
        if not markdown_content:
            return {}
        
        stats_data = {}
        
        # Look for match statistics patterns
        # This will need to be customized based on the actual stats page format
        stats_data['total_matches'] = self._extract_total_matches(markdown_content)
        stats_data['wins'] = self._extract_wins(markdown_content)
        stats_data['losses'] = self._extract_losses(markdown_content)
        stats_data['draws'] = self._extract_draws(markdown_content)
        
        return stats_data
    
    def _extract_pattern(self, content: str, pattern: str) -> Optional[str]:
        """Extract a single pattern from content."""
        match = re.search(pattern, content)
        return match.group(1).strip() if match else None
    
    def _parse_trainers(self, trainers_text: str) -> List[str]:
        """Parse trainers into a list."""
        if not trainers_text:
            return []
        
        # Split by comma and clean up
        trainers = [trainer.strip() for trainer in trainers_text.split(',')]
        return [t for t in trainers if t]
    
    def _parse_nicknames(self, nicknames_text: str) -> List[str]:
        """Parse nicknames into a list."""
        if not nicknames_text:
            return []
        
        # Remove quotes and split
        nicknames = nicknames_text.replace('"', '').split('\\n')
        return [n.strip() for n in nicknames if n.strip()]
    
    def _parse_signature_moves(self, moves_text: str) -> List[str]:
        """Parse signature moves into a list."""
        if not moves_text:
            return []
        
        # Split by newline and clean up
        moves = moves_text.split('\\n')
        return [m.strip() for m in moves if m.strip()]
    
    def _parse_alter_egos(self, egos_text: str) -> List[str]:
        """Parse alter egos into a list."""
        if not egos_text:
            return []
        
        # Split by newline and clean up
        egos = egos_text.split('\\n')
        return [e.strip() for e in egos if e.strip()]
    
    def _parse_roles(self, roles_text: str) -> List[str]:
        """Parse roles into a list."""
        if not roles_text:
            return []
        
        # Split by comma and clean up
        roles = [role.strip() for role in roles_text.split(',')]
        return [r for r in roles if r]
    
    def _extract_yearly_ratings(self, content: str) -> Dict[str, str]:
        """Extract yearly ratings from the content."""
        yearly_ratings = {}
        
        # Look for patterns like "Average rating in 2025: 8.58[195]"
        pattern = r'Average rating in (\d{4}): ([^\\[]+)'
        matches = re.findall(pattern, content)
        
        for year, rating in matches:
            yearly_ratings[year] = {
                'rating': rating.strip(),
                'votes': '0'  # We'll extract this separately if needed
            }
        
        return yearly_ratings
    
    def _extract_social_media(self, content: str) -> Dict[str, str]:
        """Extract social media links."""
        social_media = {}
        
        # Look for social media links
        patterns = {
            'twitter': r'https://x\.com/([^\\s]+)',
            'instagram': r'https://www\.instagram\.com/([^\\s]+)',
            'tiktok': r'https://www\.tiktok\.com/@([^\\s]+)',
            'youtube': r'https://www\.youtube\.com/@([^\\s]+)'
        }
        
        for platform, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                social_media[platform] = match.group(1)
        
        return social_media
    
    def _extract_total_matches(self, content: str) -> Optional[int]:
        """Extract total number of matches."""
        # This is a placeholder - actual implementation depends on stats page format
        pattern = r'Total matches:\s*(\d+)'
        match = re.search(pattern, content)
        return int(match.group(1)) if match else None
    
    def _extract_wins(self, content: str) -> Optional[int]:
        """Extract total wins."""
        pattern = r'Wins:\s*(\d+)'
        match = re.search(pattern, content)
        return int(match.group(1)) if match else None
    
    def _extract_losses(self, content: str) -> Optional[int]:
        """Extract total losses."""
        pattern = r'Losses:\s*(\d+)'
        match = re.search(pattern, content)
        return int(match.group(1)) if match else None
    
    def _extract_draws(self, content: str) -> Optional[int]:
        """Extract total draws."""
        pattern = r'Draws:\s*(\d+)'
        match = re.search(pattern, content)
        return int(match.group(1)) if match else None

def parse_wrestler_data(profile_markdown: str, stats_markdown: str = None) -> Dict[str, Any]:
    """Main function to parse wrestler data from scraped content."""
    parser = WrestlerDataParser()
    
    parsed_data = {
        'profile': parser.parse_wrestler_profile(profile_markdown),
        'statistics': parser.parse_match_statistics(stats_markdown) if stats_markdown else {},
        'parsed_at': datetime.now().isoformat()
    }
    
    return parsed_data

if __name__ == "__main__":
    # Test the parser with sample data
    print("Wrestler Data Parser - Test Mode")
    print("Use this module to parse scraped wrestling data into structured format.")
