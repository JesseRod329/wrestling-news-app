import os
import json
from datetime import datetime
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def scrape_wrestler(wrestler_name, wrestler_id=None):
    """
    Scrape wrestler data from cagematch.net
    
    Args:
        wrestler_name (str): Name of the wrestler to search for
        wrestler_id (str, optional): Specific wrestler ID if known
    """
    
    # Initialize Firecrawl
    api_key = os.getenv('FIRECRAWL_API_KEY')
    if not api_key:
        print("Error: FIRECRAWL_API_KEY not found in .env file")
        return
    
    app = FirecrawlApp(api_key=api_key)
    base_url = "https://www.cagematch.net"
    
    try:
        if wrestler_id:
            # Scrape specific wrestler by ID
            print(f"Scraping wrestler with ID: {wrestler_id}")
            
            # Profile page
            profile_url = f"{base_url}/?id=2&nr={wrestler_id}"
            profile_data = app.scrape_url(profile_url)
            
            # Stats/matches page
            stats_url = f"{base_url}/?id=2&nr={wrestler_id}&view=matches"
            stats_data = app.scrape_url(stats_url)
            
            wrestler_info = {
                'name': wrestler_name,
                'wrestler_id': wrestler_id,
                'profile_url': profile_url,
                'stats_url': stats_url,
                'profile_data': {
                    'success': profile_data.success if hasattr(profile_data, 'success') else None,
                    'markdown': profile_data.markdown if hasattr(profile_data, 'markdown') else None,
                    'metadata': profile_data.metadata if hasattr(profile_data, 'metadata') else None,
                    'error': profile_data.error if hasattr(profile_data, 'error') else None
                },
                'stats_data': {
                    'success': stats_data.success if hasattr(stats_data, 'success') else None,
                    'markdown': stats_data.markdown if hasattr(stats_data, 'markdown') else None,
                    'metadata': stats_data.metadata if hasattr(stats_data, 'metadata') else None,
                    'error': stats_data.error if hasattr(stats_data, 'error') else None
                },
                'scraped_at': datetime.now().isoformat()
            }
            
        else:
            # Search for wrestler first
            print(f"Searching for wrestler: {wrestler_name}")
            search_results = app.search(
                wrestler_name,
                limit=5
            )
            
            if not search_results.success or not search_results.data:
                print(f"No results found for {wrestler_name}")
                return
            
            print(f"Found {len(search_results.data)} results:")
            for i, result in enumerate(search_results.data):
                print(f"{i+1}. {result.get('title', 'N/A')}")
                print(f"   URL: {result.get('url', 'N/A')}")
                print(f"   Description: {result.get('description', 'N/A')[:100]}...")
            
            # Use first result for now
            first_result = search_results.data[0]
            wrestler_info = {
                'name': wrestler_name,
                'search_results': search_results.data,
                'selected_result': first_result,
                'scraped_at': datetime.now().isoformat()
            }
        
        # Save to file
        filename = f"wrestler_{wrestler_name.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(wrestler_info, f, indent=2, ensure_ascii=False)
        
        print(f"\nData saved to: {filename}")
        return wrestler_info
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    """Main function - modify these values to scrape different wrestlers"""
    
    # Example 1: Search for a wrestler by name
    print("=== Example 1: Search for wrestler by name ===")
    scrape_wrestler("John Cena")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Scrape specific wrestler by ID (you'll need to find the actual ID)
    print("=== Example 2: Scrape specific wrestler by ID ===")
    # Note: Replace "12345" with an actual wrestler ID from cagematch.net
    # You can find IDs by searching for a wrestler first
    scrape_wrestler("Example Wrestler", "12345")

if __name__ == "__main__":
    main()
