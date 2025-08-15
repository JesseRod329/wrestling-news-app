#!/usr/bin/env python3
"""
Test script for wrestler image fetching
"""

from wrestler_image_fetcher import WrestlerImageFetcher
from advanced_image_fetcher import AdvancedImageFetcher

def test_basic_image_fetcher():
    """Test the basic image fetcher."""
    print("🧪 Testing Basic Image Fetcher")
    print("=" * 40)
    
    fetcher = WrestlerImageFetcher()
    
    # Test with Cody Rhodes
    print("\n🔍 Testing: Cody Rhodes")
    images = fetcher.get_wrestler_images("Cody Rhodes")
    
    if images['best_image']:
        print(f"   ✅ Found image: {images['best_image']['source']}")
        print(f"   📏 Size: {images['best_image'].get('width', 'N/A')}x{images['best_image'].get('height', 'N/A')}")
        print(f"   🔗 URL: {images['best_image']['url']}")
    else:
        print("   ❌ No images found")
    
    print(f"   📊 Total sources: {len(images['images'])}")

def test_advanced_image_fetcher():
    """Test the advanced image fetcher."""
    print("\n🧪 Testing Advanced Image Fetcher")
    print("=" * 40)
    
    fetcher = AdvancedImageFetcher()
    
    # Test with a few wrestlers
    test_wrestlers = ["Cody Rhodes", "Hulk Hogan"]
    
    for wrestler in test_wrestlers:
        print(f"\n🔍 Testing: {wrestler}")
        images = fetcher.get_all_wrestler_images(wrestler)
        
        if images['best_image']:
            print(f"   ✅ Best image: {images['best_image']['source']}")
            print(f"   📏 Size: {images['best_image'].get('width', 'N/A')}x{images['best_image'].get('height', 'N/A')}")
            print(f"   🔗 URL: {images['best_image']['url']}")
        else:
            print("   ❌ No images found")
        
        print(f"   📊 Total images: {images['total_images']}")
        print(f"   🔍 Sources checked: {', '.join(images['sources_checked'])}")

def main():
    """Main test function."""
    print("🏆 Wrestler Image Fetcher Test Suite")
    print("=" * 50)
    
    try:
        # Test basic fetcher
        test_basic_image_fetcher()
        
        # Test advanced fetcher
        test_advanced_image_fetcher()
        
        print("\n🎉 All tests completed successfully!")
        print("\n💡 Next steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Run: python wrestler_image_fetcher.py")
        print("   3. Or run: python advanced_image_fetcher.py")
        print("   4. Update your database with images!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("   Make sure you have installed the required dependencies:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
