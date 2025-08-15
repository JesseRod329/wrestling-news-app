import os
import json
from datetime import datetime
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class CagematchScraper:
    def __init__(self):
        """Initialize the Firecrawl app with API key from environment variables."""
        api_key = os.getenv('FIRECRAWL_API_KEY')
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY not found in environment variables")
        
        self.app = FirecrawlApp(api_key=api_key)
        self.base_url = "https://www.cagematch.net"
        
    def scrape_wrestler_profile(self, wrestler_id):
        """
        Scrape a specific wrestler's profile page.
        
        Args:
            wrestler_id (str): The wrestler ID from cagematch.net
            
        Returns:
            dict: Scraped wrestler data
        """
        url = f"{self.base_url}/?id=2&nr={wrestler_id}"
        
        try:
            print(f"Scraping wrestler profile: {url}")
            scraped_data = self.app.scrape_url(url)
            
            if scraped_data and hasattr(scraped_data, 'success') and scraped_data.success:
                return {
                    'wrestler_id': wrestler_id,
                    'url': url,
                    'markdown': scraped_data.markdown if hasattr(scraped_data, 'markdown') else '',
                    'metadata': scraped_data.metadata if hasattr(scraped_data, 'metadata') else {},
                    'scraped_at': datetime.now().isoformat()
                }
            else:
                error_msg = scraped_data.error if hasattr(scraped_data, 'error') else 'Unknown error'
                print(f"Failed to scrape wrestler profile: {url} - {error_msg}")
                return None
                
        except Exception as e:
            print(f"Error scraping wrestler profile {wrestler_id}: {str(e)}")
            return None
    
    def scrape_wrestler_stats(self, wrestler_id):
        """
        Scrape a wrestler's statistics page.
        
        Args:
            wrestler_id (str): The wrestler ID from cagematch.net
            
        Returns:
            dict: Scraped statistics data
        """
        url = f"{self.base_url}/?id=2&nr={wrestler_id}&view=matches"
        
        try:
            print(f"Scraping wrestler stats: {url}")
            scraped_data = self.app.scrape_url(url)
            
            if scraped_data and hasattr(scraped_data, 'success') and scraped_data.success:
                return {
                    'wrestler_id': wrestler_id,
                    'url': url,
                    'markdown': scraped_data.markdown if hasattr(scraped_data, 'markdown') else '',
                    'metadata': scraped_data.metadata if hasattr(scraped_data, 'metadata') else {},
                    'scraped_at': datetime.now().isoformat()
                }
            else:
                error_msg = scraped_data.error if hasattr(scraped_data, 'error') else 'Unknown error'
                print(f"Failed to scrape wrestler stats: {url} - {error_msg}")
                return None
                
        except Exception as e:
            print(f"Error scraping wrestler stats {wrestler_id}: {str(e)}")
            return None
    
    def search_wrestlers(self, query, limit=10):
        """
        Search for wrestlers on cagematch.net.
        
        Args:
            query (str): Search query (e.g., wrestler name)
            limit (int): Maximum number of results
            
        Returns:
            list: Search results
        """
        try:
            print(f"Searching for wrestlers: {query}")
            search_results = self.app.search(
                query,
                limit=limit
            )
            
            if search_results.success and search_results.data:
                return search_results.data
            else:
                print(f"Search failed or no results: {search_results.error}")
                return []
            
        except Exception as e:
            print(f"Error searching for wrestlers: {str(e)}")
            return []
    
    def crawl_wrestling_events(self, start_date=None, end_date=None):
        """
        Crawl wrestling events from cagematch.net.
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            list: Crawled event data
        """
        # Build the events URL with date filters if provided
        events_url = f"{self.base_url}/?id=1"
        if start_date:
            events_url += f"&view=date&date={start_date}"
        if end_date:
            events_url += f"&date2={end_date}"
        
        try:
            print(f"Crawling wrestling events: {events_url}")
            crawl_result = self.app.crawl_url(events_url)
            
            return crawl_result
            
        except Exception as e:
            print(f"Error crawling wrestling events: {str(e)}")
            return []
    
    def save_data_to_file(self, data, filename):
        """
        Save scraped data to a JSON file.
        
        Args:
            data: Data to save
            filename (str): Name of the file to save to
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data to {filename}: {str(e)}")

def main():
    """Main function to demonstrate the scraper usage."""
    try:
        # Initialize the scraper
        scraper = CagematchScraper()
        
        # Example 1: Search for a specific wrestler
        print("=== Searching for wrestlers ===")
        search_results = scraper.search_wrestlers("John Cena", limit=5)
        for result in search_results:
            print(f"Found: {result.get('title', 'N/A')}")
            print(f"URL: {result.get('url', 'N/A')}")
            print(f"Description: {result.get('description', 'N/A')[:100]}...")
            print("---")
        
        # Example 2: Scrape a specific wrestler profile (you'll need to find the actual ID)
        print("\n=== Scraping wrestler profile ===")
        # Note: You'll need to find actual wrestler IDs from cagematch.net
        # This is just an example - replace with real IDs
        wrestler_data = scraper.scrape_wrestler_profile("12345")
        if wrestler_data:
            scraper.save_data_to_file(wrestler_data, 'wrestler_profile.json')
        
        # Example 3: Crawl recent wrestling events
        print("\n=== Crawling wrestling events ===")
        events_data = scraper.crawl_wrestling_events()
        if events_data:
            scraper.save_data_to_file(events_data, 'wrestling_events.json')
        
        print("\nScraping completed successfully!")
        
    except Exception as e:
        print(f"Error in main function: {str(e)}")

if __name__ == "__main__":
    main()
