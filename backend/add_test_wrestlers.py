#!/usr/bin/env python3
"""
Add Test Wrestlers to Database
This script adds a few popular wrestlers for testing the expanded database.
"""

import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from wrestler_data_parser import WrestlerDataParser

# Load environment variables
load_dotenv()

def add_test_wrestlers():
    """Add a few test wrestlers to expand the database."""
    
    # Check if we have the API key
    api_key = os.getenv('FIRECRAWL_API_KEY')
    if not api_key:
        print("❌ FIRECRAWL_API_KEY not found in environment variables")
        return
    
    # Initialize Firecrawl
    app = FirecrawlApp(api_key=api_key)
    parser = WrestlerDataParser()
    
    # Test wrestlers to add (ID, Name)
    test_wrestlers = [
        (4, "John Cena"),
        (5, "The Undertaker"),
        (6, "Triple H"),
        (7, "Shawn Michaels"),
        (8, "Bret Hart")
    ]
    
    # Find the latest database
    import glob
    database_files = glob.glob("wrestling_database_*.json")
    if not database_files:
        print("❌ No wrestling database found. Run create_initial_database.py first.")
        return
    
    latest_file = max(database_files, key=os.path.getctime)
    print(f"📁 Using database: {latest_file}")
    
    # Load existing database
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            database = json.load(f)
        print(f"📊 Loaded database with {len(database.get('wrestlers', {}))} wrestlers")
    except Exception as e:
        print(f"❌ Error loading database: {e}")
        return
    
    # Add wrestlers
    added_count = 0
    
    for wrestler_id, wrestler_name in test_wrestlers:
        # Skip if already exists
        if str(wrestler_id) in database.get('wrestlers', {}):
            print(f"⏭️  Skipping {wrestler_name} - already in database")
            continue
        
        print(f"\n🏆 Adding {wrestler_name} (ID: {wrestler_id})...")
        
        try:
            # Construct URL
            profile_url = f"https://www.cagematch.net/?id=2&nr={wrestler_id}"
            
            # Scrape profile
            print(f"  📡 Fetching profile...")
            profile_response = app.scrape_url(profile_url)
            
            if not profile_response or not profile_response.success:
                print(f"  ❌ Failed to scrape {wrestler_name}")
                continue
            
            # Parse data
            print(f"  🔍 Parsing data...")
            parsed_data = parser.parse_wrestler_data(profile_response.markdown)
            
            if not parsed_data:
                print(f"  ❌ Failed to parse {wrestler_name}")
                continue
            
            # Create entry
            wrestler_entry = {
                "wrestler_id": str(wrestler_id),
                "name": wrestler_name,
                "profile_url": profile_url,
                "stats_url": f"https://www.cagematch.net/?id=2&nr={wrestler_id}&page=22",
                "raw_data": {
                    "markdown": profile_response.markdown,
                    "metadata": profile_response.metadata if hasattr(profile_response, 'metadata') else {}
                },
                "parsed_data": parsed_data,
                "scraped_at": datetime.now().isoformat()
            }
            
            # Add to database
            if 'wrestlers' not in database:
                database['wrestlers'] = {}
            
            database['wrestlers'][str(wrestler_id)] = wrestler_entry
            added_count += 1
            
            print(f"  ✅ Added {wrestler_name} successfully")
            
            # Rate limiting
            if added_count < len(test_wrestlers):
                print(f"  ⏳ Waiting 3 seconds...")
                time.sleep(3)
                
        except Exception as e:
            print(f"  ❌ Error adding {wrestler_name}: {e}")
    
    # Save updated database
    if added_count > 0:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"wrestling_database_{timestamp}.json"
        
        try:
            with open(new_filename, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Database saved as: {new_filename}")
            print(f"🎉 Added {added_count} new wrestlers!")
            print(f"📊 Total wrestlers: {len(database.get('wrestlers', {}))}")
            
        except Exception as e:
            print(f"❌ Error saving database: {e}")
    else:
        print(f"\n📝 No new wrestlers were added")

if __name__ == "__main__":
    print("🏆 Adding Test Wrestlers to Database")
    print("=" * 40)
    
    try:
        add_test_wrestlers()
    except KeyboardInterrupt:
        print(f"\n⏹️  Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your API key and internet connection")
