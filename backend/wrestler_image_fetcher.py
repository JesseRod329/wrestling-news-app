#!/usr/bin/env python3
"""
Wrestler Image Fetcher
Fetches wrestler images from Wikipedia and other sources
"""

import requests
import json
import os
from typing import Dict, List, Optional
import time
from urllib.parse import quote

class WrestlerImageFetcher:
    """Fetches wrestler images from various sources."""
    
    def __init__(self):
        self.wikipedia_api = "https://en.wikipedia.org/api/rest_v1/page/summary/"
        self.wikimedia_api = "https://commons.wikimedia.org/w/api.php"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WrestlingStats/1.0 (Educational Project)'
        })
        
    def fetch_wikipedia_image(self, wrestler_name: str) -> Optional[Dict]:
        """Fetch wrestler image from Wikipedia."""
        try:
            # Clean the wrestler name for URL
            clean_name = wrestler_name.replace(' ', '_')
            url = f"{self.wikipedia_api}{quote(clean_name)}"
            
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                
                # Check if there's a thumbnail image
                if 'thumbnail' in data:
                    return {
                        'source': 'wikipedia',
                        'url': data['thumbnail']['source'],
                        'width': data['thumbnail']['width'],
                        'height': data['thumbnail']['height'],
                        'title': data.get('title', wrestler_name),
                        'description': data.get('description', '')
                    }
                elif 'content_urls' in data and 'desktop' in data['content_urls']:
                    # Fallback to page URL if no image
                    return {
                        'source': 'wikipedia_page',
                        'url': data['content_urls']['desktop']['page'],
                        'title': data.get('title', wrestler_name),
                        'description': data.get('description', '')
                    }
            
            return None
            
        except Exception as e:
            print(f"Error fetching Wikipedia image for {wrestler_name}: {e}")
            return None
    
    def search_wikimedia_images(self, wrestler_name: str, limit: int = 5) -> List[Dict]:
        """Search for images on Wikimedia Commons."""
        try:
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': f"{wrestler_name} wrestler",
                'srlimit': limit,
                'srnamespace': 6  # File namespace
            }
            
            response = self.session.get(self.wikimedia_api, params=params)
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get('query', {}).get('search', []):
                    # Get file info
                    file_params = {
                        'action': 'query',
                        'format': 'json',
                        'prop': 'imageinfo',
                        'titles': item['title'],
                        'iiprop': 'url|size|mime'
                    }
                    
                    file_response = self.session.get(self.wikimedia_api, params=file_params)
                    if file_response.status_code == 200:
                        file_data = file_response.json()
                        pages = file_data.get('query', {}).get('pages', {})
                        
                        for page_id, page_data in pages.items():
                            if 'imageinfo' in page_data:
                                for img_info in page_data['imageinfo']:
                                    results.append({
                                        'source': 'wikimedia',
                                        'url': img_info['url'],
                                        'width': img_info.get('width', 0),
                                        'height': img_info.get('height', 0),
                                        'title': item['title'],
                                        'description': item.get('snippet', ''),
                                        'mime': img_info.get('mime', '')
                                    })
                
                return results
            
            return []
            
        except Exception as e:
            print(f"Error searching Wikimedia for {wrestler_name}: {e}")
            return []
    
    def fetch_wwe_image(self, wrestler_name: str) -> Optional[Dict]:
        """Fetch wrestler image from WWE.com (basic approach)."""
        try:
            # This is a simplified approach - in production you'd want more sophisticated scraping
            search_url = f"https://www.wwe.com/search?q={quote(wrestler_name)}"
            
            # For now, return a placeholder - actual WWE scraping would require more complex logic
            return {
                'source': 'wwe_placeholder',
                'url': f"https://www.wwe.com/search?q={quote(wrestler_name)}",
                'title': f"WWE Search: {wrestler_name}",
                'description': f"Search results for {wrestler_name} on WWE.com"
            }
            
        except Exception as e:
            print(f"Error fetching WWE image for {wrestler_name}: {e}")
            return None
    
    def get_wrestler_images(self, wrestler_name: str) -> Dict:
        """Get all available images for a wrestler."""
        print(f"🔍 Fetching images for: {wrestler_name}")
        
        images = {
            'wrestler_name': wrestler_name,
            'images': [],
            'best_image': None
        }
        
        # Try Wikipedia first
        wiki_image = self.fetch_wikipedia_image(wrestler_name)
        if wiki_image:
            images['images'].append(wiki_image)
            if wiki_image['source'] == 'wikipedia':
                images['best_image'] = wiki_image
        
        # Try Wikimedia Commons
        wikimedia_images = self.search_wikimedia_images(wrestler_name)
        if wikimedia_images:
            images['images'].extend(wikimedia_images)
            if not images['best_image'] and wikimedia_images:
                images['best_image'] = wikimedia_images[0]
        
        # Try WWE as fallback
        wwe_image = self.fetch_wwe_image(wrestler_name)
        if wwe_image:
            images['images'].append(wwe_image)
        
        print(f"   Found {len(images['images'])} image sources")
        return images
    
    def update_database_with_images(self, database_file: str):
        """Update the wrestling database with image information."""
        try:
            # Load the database
            with open(database_file, 'r', encoding='utf-8') as f:
                database = json.load(f)
            
            print(f"📁 Updating database: {database_file}")
            print(f"   Total wrestlers: {len(database.get('wrestlers', {}))}")
            
            updated_count = 0
            
            for wrestler_id, wrestler in database.get('wrestlers', {}).items():
                wrestler_name = wrestler.get('name', '')
                if wrestler_name:
                    print(f"   🔍 Processing: {wrestler_name}")
                    
                    # Get images for this wrestler
                    image_data = self.get_wrestler_images(wrestler_name)
                    
                    # Add image data to wrestler
                    if 'parsed_data' not in wrestler:
                        wrestler['parsed_data'] = {}
                    
                    wrestler['parsed_data']['images'] = image_data
                    
                    # Add a direct image URL for easy access
                    if image_data.get('best_image'):
                        wrestler['image_url'] = image_data['best_image']['url']
                        wrestler['image_source'] = image_data['best_image']['source']
                    
                    updated_count += 1
                    
                    # Rate limiting to be respectful
                    time.sleep(1)
            
            # Update metadata
            if 'metadata' not in database:
                database['metadata'] = {}
            
            database['metadata'].update({
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "images_added": updated_count,
                "image_fetcher_version": "1.0"
            })
            
            # Save updated database
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            new_filename = f"wrestling_database_with_images_{timestamp}.json"
            
            with open(new_filename, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Database updated with images: {new_filename}")
            print(f"🎉 Successfully processed {updated_count} wrestlers")
            
            return new_filename
            
        except Exception as e:
            print(f"❌ Error updating database: {e}")
            return None

def main():
    """Main function to demonstrate image fetching."""
    fetcher = WrestlerImageFetcher()
    
    # Test with a few wrestlers
    test_wrestlers = [
        "Cody Rhodes",
        "Hulk Hogan", 
        "The Rock",
        "Stone Cold Steve Austin"
    ]
    
    print("🏆 Wrestler Image Fetcher Test")
    print("=" * 40)
    
    for wrestler in test_wrestlers:
        print(f"\n🔍 Testing: {wrestler}")
        images = fetcher.get_wrestler_images(wrestler)
        
        if images['best_image']:
            print(f"   ✅ Best image: {images['best_image']['source']}")
            print(f"   📏 Size: {images['best_image'].get('width', 'N/A')}x{images['best_image'].get('height', 'N/A')}")
        else:
            print(f"   ❌ No images found")
        
        print(f"   📊 Total sources: {len(images['images'])}")
    
    print(f"\n🚀 Image fetching test completed!")
    print(f"   Ready to update your wrestling database with images")

if __name__ == "__main__":
    main()
