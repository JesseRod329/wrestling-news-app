import os
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

def test_connection():
    """Test the Firecrawl connection and API key."""
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('FIRECRAWL_API_KEY')
    if not api_key:
        print("❌ Error: FIRECRAWL_API_KEY not found in .env file")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        # Initialize Firecrawl
        app = FirecrawlApp(api_key=api_key)
        print("✅ Firecrawl app initialized successfully")
        
        # Test with a simple search
        print("🔍 Testing search functionality...")
        test_results = app.search(
            "wrestling",
            limit=1
        )
        
        print(f"✅ Search test successful!")
        print(f"   Success: {test_results.success}")
        print(f"   Found {len(test_results.data)} results:")
        
        for i, result in enumerate(test_results.data):
            print(f"   {i+1}. {result.get('title', 'N/A')}")
            print(f"      URL: {result.get('url', 'N/A')}")
            print(f"      Description: {result.get('description', 'N/A')[:100]}...")
        
        print("\n🎉 Firecrawl connection test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Firecrawl: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()
