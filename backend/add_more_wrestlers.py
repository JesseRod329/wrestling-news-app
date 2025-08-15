#!/usr/bin/env python3
"""
Add More Wrestlers to Database
This script adds popular wrestlers to expand our wrestling database.
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

class WrestlerDatabaseExpander:
    def __init__(self):
        self.api_key = os.getenv('FIRECRAWL_API_KEY')
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY not found in environment variables")
        
        self.app = FirecrawlApp(api_key=self.api_key)
        self.parser = WrestlerDataParser()
        
        # Popular wrestlers to add (ID, Name)
        self.popular_wrestlers = [
            (3686, "Cody Rhodes"),  # Already exists, but good for testing
            (1, "Hulk Hogan"),
            (2, "The Rock"),
            (3, "Stone Cold Steve Austin"),
            (4, "John Cena"),
            (5, "The Undertaker"),
            (6, "Triple H"),
            (7, "Shawn Michaels"),
            (8, "Bret Hart"),
            (9, "Ric Flair"),
            (10, "Randy Savage"),
            (11, "Andre the Giant"),
            (12, "Mick Foley"),
            (13, "Kane"),
            (14, "Big Show"),
            (15, "Kurt Angle"),
            (16, "Eddie Guerrero"),
            (17, "Chris Benoit"),
            (18, "Diamond Dallas Page"),
            (19, "Goldberg"),
            (20, "Booker T"),
            (21, "Rey Mysterio"),
            (22, "Edge"),
            (23, "Christian"),
            (24, "Jeff Hardy"),
            (25, "Matt Hardy"),
            (26, "CM Punk"),
            (27, "Daniel Bryan"),
            (28, "AJ Styles"),
            (29, "Seth Rollins"),
            (30, "Roman Reigns"),
            (31, "Dean Ambrose"),
            (32, "Bray Wyatt"),
            (33, "Finn Balor"),
            (34, "Shinsuke Nakamura"),
            (35, "Kevin Owens"),
            (36, "Sami Zayn"),
            (37, "Cesaro"),
            (38, "Sheamus"),
            (39, "Randy Orton"),
            (40, "Brock Lesnar"),
            (41, "Bobby Lashley"),
            (42, "Drew McIntyre"),
            (43, "Braun Strowman"),
            (44, "Aleister Black"),
            (45, "Tommaso Ciampa"),
            (46, "Johnny Gargano"),
            (47, "Adam Cole"),
            (48, "Kyle O'Reilly"),
            (49, "Roderick Strong"),
            (50, "Bobby Fish")
        ]
        
        # Load existing database
        self.database_path = self._find_latest_database()
        self.database = self._load_database()
        
    def _find_latest_database(self):
        """Find the most recent wrestling database file."""
        import glob
        database_files = glob.glob("wrestling_database_*.json")
        if not database_files:
            raise FileNotFoundError("No wrestling database found. Run create_initial_database.py first.")
        
        # Sort by creation time and get the latest
        latest_file = max(database_files, key=os.path.getctime)
        print(f"Using database: {latest_file}")
        return latest_file
    
    def _load_database(self):
        """Load the existing wrestling database."""
        try:
            with open(self.database_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"Loaded database with {len(data.get('wrestlers', {}))} wrestlers")
                return data
        except Exception as e:
            print(f"Error loading database: {e}")
            return {"wrestlers": {}, "metadata": {}}
    
    def _save_database(self):
        """Save the updated database with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"wrestling_database_{timestamp}.json"
        
        try:
            with open(new_filename, 'w', encoding='utf-8') as f:
                json.dump(self.database, f, indent=2, ensure_ascii=False)
            
            print(f"Database saved as: {new_filename}")
            
            # Update the current database path
            self.database_path = new_filename
            return new_filename
        except Exception as e:
            print(f"Error saving database: {e}")
            return None
    
    def scrape_wrestler(self, wrestler_id, wrestler_name):
        """Scrape a single wrestler's profile."""
        try:
            print(f"Scraping {wrestler_name} (ID: {wrestler_id})...")
            
            # Construct the cagematch.net URL
            profile_url = f"https://www.cagematch.net/?id=2&nr={wrestler_id}"
            
            # Scrape the profile page
            print(f"  Fetching profile from: {profile_url}")
            profile_response = self.app.scrape_url(profile_url)
            
            if not profile_response or not profile_response.success:
                print(f"  ❌ Failed to scrape profile for {wrestler_name}")
                return None
            
            # Parse the markdown content
            print(f"  Parsing profile data...")
            parsed_data = self.parser.parse_wrestler_data(profile_response.markdown)
            
            if not parsed_data:
                print(f"  ❌ Failed to parse data for {wrestler_name}")
                return None
            
            # Create wrestler entry
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
            
            print(f"  ✅ Successfully scraped {wrestler_name}")
            return wrestler_entry
            
        except Exception as e:
            print(f"  ❌ Error scraping {wrestler_name}: {e}")
            return None
    
    def add_wrestlers_to_database(self, max_wrestlers=10, delay=2):
        """Add multiple wrestlers to the database."""
        print(f"Starting to add up to {max_wrestlers} wrestlers to the database...")
        print(f"Current database has {len(self.database.get('wrestlers', {}))} wrestlers")
        
        added_count = 0
        skipped_count = 0
        
        for i, (wrestler_id, wrestler_name) in enumerate(self.popular_wrestlers):
            if added_count >= max_wrestlers:
                break
                
            # Check if wrestler already exists
            if str(wrestler_id) in self.database.get('wrestlers', {}):
                print(f"⏭️  Skipping {wrestler_name} - already in database")
                skipped_count += 1
                continue
            
            print(f"\n[{i+1}/{len(self.popular_wrestlers)}] Processing {wrestler_name}...")
            
            # Scrape the wrestler
            wrestler_data = self.scrape_wrestler(wrestler_id, wrestler_name)
            
            if wrestler_data:
                # Add to database
                if 'wrestlers' not in self.database:
                    self.database['wrestlers'] = {}
                
                self.database['wrestlers'][str(wrestler_id)] = wrestler_data
                added_count += 1
                
                print(f"  ✅ Added {wrestler_name} to database")
                
                # Save database periodically
                if added_count % 5 == 0:
                    print(f"  💾 Saving database...")
                    self._save_database()
                
                # Rate limiting
                if delay > 0:
                    print(f"  ⏳ Waiting {delay} seconds...")
                    time.sleep(delay)
            else:
                print(f"  ❌ Failed to add {wrestler_name}")
        
        # Final save
        print(f"\n💾 Saving final database...")
        self._save_database()
        
        # Update metadata
        if 'metadata' not in self.database:
            self.database['metadata'] = {}
        
        self.database['metadata'].update({
            "last_updated": datetime.now().isoformat(),
            "total_wrestlers": len(self.database.get('wrestlers', {})),
            "expanded_by": "add_more_wrestlers.py",
            "expansion_date": datetime.now().isoformat()
        })
        
        print(f"\n🎉 Database expansion complete!")
        print(f"   Added: {added_count} wrestlers")
        print(f"   Skipped: {skipped_count} wrestlers")
        print(f"   Total: {len(self.database.get('wrestlers', {}))} wrestlers")
        
        return added_count
    
    def show_database_summary(self):
        """Show a summary of the current database."""
        wrestlers = self.database.get('wrestlers', {})
        
        print(f"\n📊 Database Summary:")
        print(f"   Total Wrestlers: {len(wrestlers)}")
        print(f"   Database File: {self.database_path}")
        
        if wrestlers:
            print(f"\n🏆 Wrestlers in Database:")
            for wrestler_id, wrestler_data in wrestlers.items():
                name = wrestler_data.get('name', 'Unknown')
                rating = wrestler_data.get('parsed_data', {}).get('profile', {}).get('average_rating', 'N/A')
                print(f"   {wrestler_id}: {name} - Rating: {rating}")
        
        # Show metadata
        metadata = self.database.get('metadata', {})
        if metadata:
            print(f"\n📋 Metadata:")
            for key, value in metadata.items():
                print(f"   {key}: {value}")

def main():
    """Main function to run the wrestler database expansion."""
    try:
        print("🏆 Wrestler Database Expander")
        print("=" * 50)
        
        # Initialize the expander
        expander = WrestlerDatabaseExpander()
        
        # Show current database status
        expander.show_database_summary()
        
        # Ask user how many wrestlers to add
        print(f"\n❓ How many new wrestlers would you like to add? (max {len(expander.popular_wrestlers)})")
        try:
            max_wrestlers = int(input("Enter number (or press Enter for 5): ") or "5")
            max_wrestlers = min(max_wrestlers, len(expander.popular_wrestlers))
        except ValueError:
            max_wrestlers = 5
            print(f"Invalid input, using default: {max_wrestlers}")
        
        # Ask for delay between requests
        try:
            delay_input = input("Enter delay between requests in seconds (or press Enter for 2): ") or "2"
            delay = float(delay_input)
        except ValueError:
            delay = 2.0
            print(f"Invalid input, using default: {delay} seconds")
        
        print(f"\n🚀 Starting to add {max_wrestlers} wrestlers with {delay}s delay...")
        
        # Add wrestlers to database
        added_count = expander.add_wrestlers_to_database(max_wrestlers=max_wrestlers, delay=delay)
        
        # Show final summary
        expander.show_database_summary()
        
        print(f"\n✅ Database expansion completed successfully!")
        print(f"   New wrestlers added: {added_count}")
        
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Operation cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your API key and internet connection")

if __name__ == "__main__":
    main()
