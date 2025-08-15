#!/usr/bin/env python3
"""
Advanced Wrestler Image Fetcher
Fetches high-quality wrestler images from multiple sources
"""

import requests
import json
import os
import re
from typing import Dict, List, Optional
import time
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
import random

class AdvancedImageFetcher:
    """Advanced image fetcher with multiple source support."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Image sources configuration
        self.sources = {
            'wikipedia': {
                'enabled': True,
                'priority': 1,
                'api_url': 'https://en.wikipedia.org/api/rest_v1/page/summary/'
            },
            'wikimedia': {
                'enabled': True,
                'priority': 2,
                'api_url': 'https://commons.wikimedia.org/w/api.php'
            },
            'wwe': {
                'enabled': True,
                'priority': 3,
                'base_url': 'https://www.wwe.com'
            },
            'aew': {
                'enabled': True,
                'priority': 4,
                'base_url': 'https://www.allelitewrestling.com'
            },
            'cagematch': {
                'enabled': True,
                'priority': 5,
                'base_url': 'https://www.cagematch.net'
            }
        }
    
    def fetch_wikipedia_images(self, wrestler_name: str) -> List[Dict]:
        """Fetch images from Wikipedia with multiple size options."""
        images = []
        
        try:
            # Try different name variations
            name_variations = [
                wrestler_name,
                wrestler_name.replace(' ', '_'),
                f"{wrestler_name}_(wrestler)",
                f"{wrestler_name}_(professional_wrestler)"
            ]
            
            for name_var in name_variations:
                url = f"{self.sources['wikipedia']['api_url']}{quote(name_var)}"
                response = self.session.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Get thumbnail
                    if 'thumbnail' in data:
                        images.append({
                            'source': 'wikipedia',
                            'url': data['thumbnail']['source'],
                            'width': data['thumbnail']['width'],
                            'height': data['thumbnail']['height'],
                            'title': data.get('title', wrestler_name),
                            'description': data.get('description', ''),
                            'priority': self.sources['wikipedia']['priority']
                        })
                    
                    # Get larger image if available
                    if 'originalimage' in data:
                        images.append({
                            'source': 'wikipedia_original',
                            'url': data['originalimage']['source'],
                            'width': data['originalimage']['width'],
                            'height': data['originalimage']['height'],
                            'title': data.get('title', wrestler_name),
                            'description': data.get('description', ''),
                            'priority': self.sources['wikipedia']['priority'] - 0.5
                        })
                    
                    break  # Found a match, no need to try other variations
                    
        except Exception as e:
            print(f"Wikipedia error for {wrestler_name}: {e}")
        
        return images
    
    def fetch_wwe_images(self, wrestler_name: str) -> List[Dict]:
        """Fetch images from WWE.com."""
        images = []
        
        try:
            # Search WWE.com for the wrestler
            search_url = f"{self.sources['wwe']['base_url']}/search?q={quote(wrestler_name)}"
            response = self.session.get(search_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for wrestler profile images
                # This is a simplified approach - WWE.com structure may vary
                img_tags = soup.find_all('img', src=re.compile(r'\.(jpg|jpeg|png|webp)', re.I))
                
                for img in img_tags[:5]:  # Limit to 5 images
                    src = img.get('src')
                    if src and wrestler_name.lower() in img.get('alt', '').lower():
                        # Convert relative URLs to absolute
                        if src.startswith('/'):
                            src = urljoin(self.sources['wwe']['base_url'], src)
                        
                        images.append({
                            'source': 'wwe',
                            'url': src,
                            'alt': img.get('alt', ''),
                            'priority': self.sources['wwe']['priority']
                        })
            
        except Exception as e:
            print(f"WWE error for {wrestler_name}: {e}")
        
        return images
    
    def fetch_cagematch_images(self, wrestler_name: str) -> List[Dict]:
        """Fetch images from Cagematch.net."""
        images = []
        
        try:
            # Search Cagematch for the wrestler
            search_url = f"{self.sources['cagematch']['base_url']}/?id=2&view=workers&search={quote(wrestler_name)}"
            response = self.session.get(search_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for wrestler images
                img_tags = soup.find_all('img', src=re.compile(r'wrestlers|workers', re.I))
                
                for img in img_tags[:3]:  # Limit to 3 images
                    src = img.get('src')
                    if src:
                        # Convert relative URLs to absolute
                        if src.startswith('/'):
                            src = urljoin(self.sources['cagematch']['base_url'], src)
                        
                        images.append({
                            'source': 'cagematch',
                            'url': src,
                            'alt': img.get('alt', ''),
                            'priority': self.sources['cagematch']['priority']
                        })
            
        except Exception as e:
            print(f"Cagematch error for {wrestler_name}: {e}")
        
        return images
    
    def fetch_social_media_images(self, wrestler_name: str) -> List[Dict]:
        """Fetch images from social media profiles (placeholder for future implementation)."""
        # This would require more sophisticated scraping and API access
        # For now, return empty list
        return []
    
    def get_all_wrestler_images(self, wrestler_name: str) -> Dict:
        """Get all available images for a wrestler from all sources."""
        print(f"🔍 Fetching images for: {wrestler_name}")
        
        all_images = []
        
        # Fetch from Wikipedia
        if self.sources['wikipedia']['enabled']:
            wiki_images = self.fetch_wikipedia_images(wrestler_name)
            all_images.extend(wiki_images)
            print(f"   📚 Wikipedia: {len(wiki_images)} images")
        
        # Fetch from WWE
        if self.sources['wwe']['enabled']:
            wwe_images = self.fetch_wwe_images(wrestler_name)
            all_images.extend(wwe_images)
            print(f"   🏆 WWE: {len(wwe_images)} images")
        
        # Fetch from Cagematch
        if self.sources['cagematch']['enabled']:
            cagematch_images = self.fetch_cagematch_images(wrestler_name)
            all_images.extend(cagematch_images)
            print(f"   📊 Cagematch: {len(cagematch_images)} images")
        
        # Sort by priority and quality
        all_images.sort(key=lambda x: (x.get('priority', 999), x.get('width', 0) * x.get('height', 0)), reverse=True)
        
        # Select best image
        best_image = all_images[0] if all_images else None
        
        result = {
            'wrestler_name': wrestler_name,
            'total_images': len(all_images),
            'images': all_images,
            'best_image': best_image,
            'sources_checked': [k for k, v in self.sources.items() if v['enabled']]
        }
        
        if best_image:
            print(f"   ✅ Best image: {best_image['source']} ({best_image.get('width', 'N/A')}x{best_image.get('height', 'N/A')})")
        else:
            print(f"   ❌ No images found")
        
        return result
    
    def update_database_with_images(self, database_file: str, delay: float = 2.0):
        """Update the wrestling database with comprehensive image information."""
        try:
            # Load the database
            with open(database_file, 'r', encoding='utf-8') as f:
                database = json.load(f)
            
            print(f"📁 Updating database: {database_file}")
            print(f"   Total wrestlers: {len(database.get('wrestlers', {}))}")
            
            updated_count = 0
            total_images_found = 0
            
            for wrestler_id, wrestler in database.get('wrestlers', {}).items():
                wrestler_name = wrestler.get('name', '')
                if wrestler_name:
                    print(f"\n   🔍 Processing: {wrestler_name}")
                    
                    # Get all images for this wrestler
                    image_data = self.get_all_wrestler_images(wrestler_name)
                    
                    # Add image data to wrestler
                    if 'parsed_data' not in wrestler:
                        wrestler['parsed_data'] = {}
                    
                    wrestler['parsed_data']['images'] = image_data
                    
                    # Add direct image URLs for easy access
                    if image_data.get('best_image'):
                        wrestler['image_url'] = image_data['best_image']['url']
                        wrestler['image_source'] = image_data['best_image']['source']
                        wrestler['image_width'] = image_data['best_image'].get('width')
                        wrestler['image_height'] = image_data['best_image'].get('height')
                    
                    # Add all image URLs
                    wrestler['all_image_urls'] = [img['url'] for img in image_data.get('images', [])]
                    
                    updated_count += 1
                    total_images_found += image_data.get('total_images', 0)
                    
                    # Rate limiting to be respectful
                    time.sleep(delay)
            
            # Update metadata
            if 'metadata' not in database:
                database['metadata'] = {}
            
            database['metadata'].update({
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "images_added": updated_count,
                "total_images_found": total_images_found,
                "image_fetcher_version": "2.0",
                "sources_used": list(self.sources.keys())
            })
            
            # Save updated database
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            new_filename = f"wrestling_database_with_images_{timestamp}.json"
            
            with open(new_filename, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Database updated with images: {new_filename}")
            print(f"🎉 Successfully processed {updated_count} wrestlers")
            print(f"📸 Total images found: {total_images_found}")
            
            return new_filename
            
        except Exception as e:
            print(f"❌ Error updating database: {e}")
            return None

def main():
    """Main function to demonstrate advanced image fetching."""
    fetcher = AdvancedImageFetcher()
    
    # Test with a few wrestlers
    test_wrestlers = [
        "Cody Rhodes",
        "Hulk Hogan", 
        "The Rock",
        "Stone Cold Steve Austin"
    ]
    
    print("🏆 Advanced Wrestler Image Fetcher Test")
    print("=" * 50)
    
    for wrestler in test_wrestlers:
        print(f"\n🔍 Testing: {wrestler}")
        images = fetcher.get_all_wrestler_images(wrestler)
        
        if images['best_image']:
            print(f"   ✅ Best image: {images['best_image']['source']}")
            print(f"   📏 Size: {images['best_image'].get('width', 'N/A')}x{images['best_image'].get('height', 'N/A')}")
        else:
            print(f"   ❌ No images found")
        
        print(f"   📊 Total sources: {len(images['sources_checked'])}")
        print(f"   🖼️  Total images: {images['total_images']}")
    
    print(f"\n🚀 Advanced image fetching test completed!")
    print(f"   Ready to update your wrestling database with comprehensive images")

if __name__ == "__main__":
    main()
