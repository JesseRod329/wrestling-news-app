import os
import json
import time
import random
from datetime import datetime
from typing import List, Dict, Any, Optional
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from wrestler_data_parser import parse_wrestler_data

class AutoWrestlerScraper:
    """Automated system to discover and scrape wrestler data from cagematch.net."""
    
    def __init__(self):
        """Initialize the auto-scraper with Firecrawl API."""
        load_dotenv()
        
        api_key = os.getenv('FIRECRAWL_API_KEY')
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY not found in environment variables")
        
        self.app = FirecrawlApp(api_key=api_key)
        self.base_url = "https://www.cagematch.net"
        self.scraped_wrestlers = {}
        self.discovered_ids = set()
        
        # Rate limiting settings
        self.delay_between_requests = 2  # seconds
        self.max_requests_per_minute = 30
        
    def discover_wrestler_ids(self, search_terms: List[str], max_per_term: int = 10) -> List[str]:
        """
        Discover wrestler IDs by searching for common wrestling terms.
        
        Args:
            search_terms: List of search terms to find wrestlers
            max_per_term: Maximum wrestlers to find per search term
            
        Returns:
            List of discovered wrestler IDs
        """
        discovered_ids = []
        
        for term in search_terms:
            print(f"🔍 Searching for wrestlers with term: '{term}'")
            
            try:
                # Search for wrestlers
                search_results = self.app.search(
                    f"{term} wrestler",
                    limit=max_per_term
                )
                
                if search_results and hasattr(search_results, 'data'):
                    for result in search_results.data:
                        url = result.get('url', '')
                        # Look for cagematch.net URLs with wrestler IDs
                        if 'cagematch.net' in url and 'nr=' in url:
                            wrestler_id = self._extract_wrestler_id(url)
                            if wrestler_id and wrestler_id not in discovered_ids:
                                discovered_ids.append(wrestler_id)
                                print(f"   Found wrestler ID: {wrestler_id} from {url}")
                
                # Rate limiting
                time.sleep(self.delay_between_requests)
                
            except Exception as e:
                print(f"Error searching for '{term}': {str(e)}")
                continue
        
        print(f"🎯 Total unique wrestler IDs discovered: {len(discovered_ids)}")
        return discovered_ids
    
    def _extract_wrestler_id(self, url: str) -> Optional[str]:
        """Extract wrestler ID from cagematch.net URL."""
        import re
        match = re.search(r'nr=(\d+)', url)
        return match.group(1) if match else None
    
    def scrape_wrestler_batch(self, wrestler_ids: List[str], max_batch_size: int = 5) -> Dict[str, Any]:
        """
        Scrape multiple wrestlers in batches to respect rate limits.
        
        Args:
            wrestler_ids: List of wrestler IDs to scrape
            max_batch_size: Maximum wrestlers to scrape in one batch
            
        Returns:
            Dictionary of scraped wrestler data
        """
        all_wrestler_data = {}
        
        # Process wrestlers in batches
        for i in range(0, len(wrestler_ids), max_batch_size):
            batch = wrestler_ids[i:i + max_batch_size]
            print(f"\n📦 Processing batch {i//max_batch_size + 1}: {len(batch)} wrestlers")
            
            for wrestler_id in batch:
                try:
                    print(f"   Scraping wrestler ID: {wrestler_id}")
                    wrestler_data = self._scrape_single_wrestler(wrestler_id)
                    
                    if wrestler_data:
                        all_wrestler_data[wrestler_id] = wrestler_data
                        print(f"   ✅ Successfully scraped wrestler ID: {wrestler_id}")
                    else:
                        print(f"   ❌ Failed to scrape wrestler ID: {wrestler_id}")
                    
                    # Rate limiting between individual scrapes
                    time.sleep(self.delay_between_requests)
                    
                except Exception as e:
                    print(f"   ❌ Error scraping wrestler {wrestler_id}: {str(e)}")
                    continue
            
            # Longer delay between batches
            if i + max_batch_size < len(wrestler_ids):
                print(f"   ⏳ Waiting {self.delay_between_requests * 2} seconds before next batch...")
                time.sleep(self.delay_between_requests * 2)
        
        return all_wrestler_data
    
    def _scrape_single_wrestler(self, wrestler_id: str) -> Optional[Dict[str, Any]]:
        """Scrape a single wrestler's profile and stats."""
        try:
            # Scrape profile page
            profile_url = f"{self.base_url}/?id=2&nr={wrestler_id}"
            profile_data = self.app.scrape_url(profile_url)
            
            # Scrape stats page
            stats_url = f"{self.base_url}/?id=2&nr={wrestler_id}&view=matches"
            stats_data = self.app.scrape_url(stats_url)
            
            if not profile_data or not hasattr(profile_data, 'success') or not profile_data.success:
                return None
            
            # Extract wrestler name from profile
            wrestler_name = self._extract_wrestler_name(profile_data.markdown)
            
            # Parse the raw data into structured format
            parsed_data = parse_wrestler_data(
                profile_data.markdown if hasattr(profile_data, 'markdown') else '',
                stats_data.markdown if stats_data and hasattr(stats_data, 'markdown') else ''
            )
            
            # Combine raw and parsed data
            wrestler_info = {
                'wrestler_id': wrestler_id,
                'name': wrestler_name or f"Wrestler_{wrestler_id}",
                'profile_url': profile_url,
                'stats_url': stats_url,
                'raw_data': {
                    'profile': {
                        'success': profile_data.success,
                        'markdown': profile_data.markdown if hasattr(profile_data, 'markdown') else None,
                        'metadata': profile_data.metadata if hasattr(profile_data, 'metadata') else None,
                        'error': profile_data.error if hasattr(profile_data, 'error') else None
                    },
                    'stats': {
                        'success': stats_data.success if stats_data else None,
                        'markdown': stats_data.markdown if stats_data and hasattr(stats_data, 'markdown') else None,
                        'metadata': stats_data.metadata if stats_data and hasattr(stats_data, 'metadata') else None,
                        'error': stats_data.error if stats_data and hasattr(stats_data, 'error') else None
                    }
                },
                'parsed_data': parsed_data,
                'scraped_at': datetime.now().isoformat()
            }
            
            return wrestler_info
            
        except Exception as e:
            print(f"Error in _scrape_single_wrestler: {str(e)}")
            return None
    
    def _extract_wrestler_name(self, markdown_content: str) -> Optional[str]:
        """Extract wrestler name from markdown content."""
        if not markdown_content:
            return None
        
        import re
        # Look for the main heading with the wrestler's name
        match = re.search(r'# ([^\\n]+)', markdown_content)
        return match.group(1).strip() if match else None
    
    def save_database(self, wrestler_data: Dict[str, Any], filename: str = None) -> str:
        """Save the scraped wrestler database to a JSON file."""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"wrestling_database_{timestamp}.json"
        
        database = {
            'metadata': {
                'total_wrestlers': len(wrestler_data),
                'scraped_at': datetime.now().isoformat(),
                'source': 'cagematch.net',
                'scraper_version': '1.0.0'
            },
            'wrestlers': wrestler_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Database saved to: {filename}")
        return filename
    
    def load_database(self, filename: str) -> Dict[str, Any]:
        """Load an existing wrestler database."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                database = json.load(f)
            print(f"📂 Database loaded from: {filename}")
            return database
        except Exception as e:
            print(f"Error loading database: {str(e)}")
            return {}
    
    def get_wrestler_stats_summary(self, wrestler_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of wrestler statistics for the frontend."""
        summary = {
            'total_wrestlers': len(wrestler_data),
            'wrestlers_by_promotion': {},
            'wrestlers_by_style': {},
            'top_rated_wrestlers': [],
            'recently_scraped': []
        }
        
        for wrestler_id, data in wrestler_data.items():
            parsed = data.get('parsed_data', {})
            profile = parsed.get('profile', {})
            
            # Count by promotion
            promotion = profile.get('promotion', 'Unknown')
            if promotion not in summary['wrestlers_by_promotion']:
                summary['wrestlers_by_promotion'][promotion] = 0
            summary['wrestlers_by_promotion'][promotion] += 1
            
            # Count by wrestling style
            style = profile.get('wrestling_style', 'Unknown')
            if style not in summary['wrestlers_by_style']:
                summary['wrestlers_by_style'][style] = 0
            summary['wrestlers_by_style'][style] += 1
            
            # Track top rated wrestlers
            rating = profile.get('average_rating')
            if rating:
                try:
                    rating_float = float(rating)
                    summary['top_rated_wrestlers'].append({
                        'id': wrestler_id,
                        'name': data.get('name', 'Unknown'),
                        'rating': rating_float,
                        'promotion': promotion
                    })
                except ValueError:
                    pass
            
            # Track recently scraped
            scraped_at = data.get('scraped_at')
            if scraped_at:
                summary['recently_scraped'].append({
                    'id': wrestler_id,
                    'name': data.get('name', 'Unknown'),
                    'scraped_at': scraped_at
                })
        
        # Sort top rated wrestlers
        summary['top_rated_wrestlers'].sort(key=lambda x: x['rating'], reverse=True)
        summary['top_rated_wrestlers'] = summary['top_rated_wrestlers'][:10]
        
        # Sort recently scraped
        summary['recently_scraped'].sort(key=lambda x: x['scraped_at'], reverse=True)
        summary['recently_scraped'] = summary['recently_scraped'][:10]
        
        return summary

def main():
    """Main function to run the auto-scraper."""
    try:
        # Initialize the scraper
        scraper = AutoWrestlerScraper()
        
        # Define search terms to discover wrestlers
        search_terms = [
            "WWE", "AEW", "NJPW", "ROH", "Impact", "TNA",
            "John Cena", "Roman Reigns", "Cody Rhodes", "Kenny Omega",
            "Kazuchika Okada", "Will Ospreay", "MJF", "CM Punk"
        ]
        
        print("🚀 Starting Auto Wrestler Scraper")
        print("=" * 50)
        
        # Step 1: Discover wrestler IDs
        print("\n📡 Phase 1: Discovering Wrestler IDs")
        discovered_ids = scraper.discover_wrestler_ids(search_terms, max_per_term=5)
        
        if not discovered_ids:
            print("❌ No wrestler IDs discovered. Exiting.")
            return
        
        # Step 2: Scrape wrestler data
        print(f"\n🔄 Phase 2: Scraping {len(discovered_ids)} Wrestlers")
        wrestler_data = scraper.scrape_wrestler_batch(discovered_ids, max_batch_size=3)
        
        if not wrestler_data:
            print("❌ No wrestler data scraped. Exiting.")
            return
        
        # Step 3: Save database
        print(f"\n💾 Phase 3: Saving Database")
        database_file = scraper.save_database(wrestler_data)
        
        # Step 4: Generate summary
        print(f"\n📊 Phase 4: Generating Summary")
        summary = scraper.get_wrestler_stats_summary(wrestler_data)
        
        # Save summary separately
        summary_file = f"wrestling_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"📈 Summary saved to: {summary_file}")
        print(f"\n🎉 Auto-scraping completed successfully!")
        print(f"   Total wrestlers scraped: {len(wrestler_data)}")
        print(f"   Database file: {database_file}")
        print(f"   Summary file: {summary_file}")
        
    except Exception as e:
        print(f"❌ Error in main function: {str(e)}")

if __name__ == "__main__":
    main()
