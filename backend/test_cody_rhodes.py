import os
import json
from datetime import datetime
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def scrape_cody_rhodes():
    """Scrape Cody Rhodes' data from cagematch.net using his ID 3686."""
    
    # Initialize Firecrawl
    api_key = os.getenv('FIRECRAWL_API_KEY')
    if not api_key:
        print("Error: FIRECRAWL_API_KEY not found in .env file")
        return
    
    app = FirecrawlApp(api_key=api_key)
    base_url = "https://www.cagematch.net"
    
    try:
        print("=== Scraping Cody Rhodes (ID: 3686) ===")
        
        # Scrape Cody Rhodes' profile page
        profile_url = f"{base_url}/?id=2&nr=3686"
        print(f"Scraping profile: {profile_url}")
        profile_data = app.scrape_url(profile_url)
        
        # Scrape Cody Rhodes' statistics/matches page
        stats_url = f"{base_url}/?id=2&nr=3686&view=matches"
        print(f"Scraping stats: {stats_url}")
        stats_data = app.scrape_url(stats_url)
        
        # Prepare the data
        cody_data = {
            'name': 'Cody Rhodes',
            'wrestler_id': '3686',
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
        
        # Save to file
        filename = f"cody_rhodes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(cody_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Data saved to: {filename}")
        
        # Display some key information
        if profile_data and hasattr(profile_data, 'success') and profile_data.success:
            print(f"✅ Profile scraping successful")
            if hasattr(profile_data, 'markdown') and profile_data.markdown:
                print(f"   Profile content length: {len(profile_data.markdown)} characters")
        else:
            print(f"❌ Profile scraping failed: {getattr(profile_data, 'error', 'Unknown error')}")
        
        if stats_data and hasattr(stats_data, 'success') and stats_data.success:
            print(f"✅ Stats scraping successful")
            if hasattr(stats_data, 'markdown') and stats_data.markdown:
                print(f"   Stats content length: {len(stats_data.markdown)} characters")
        else:
            print(f"❌ Stats scraping failed: {getattr(stats_data, 'error', 'Unknown error')}")
        
        return cody_data
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    scrape_cody_rhodes()
