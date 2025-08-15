import json
import os
from datetime import datetime
from wrestler_data_parser import parse_wrestler_data

def create_initial_database():
    """Create an initial wrestling database from existing Cody Rhodes data."""
    
    print("🏗️  Creating Initial Wrestling Database...")
    
    # Load the existing Cody Rhodes data
    try:
        with open('cody_rhodes_20250814_163533.json', 'r', encoding='utf-8') as f:
            cody_data = json.load(f)
        print("✅ Loaded existing Cody Rhodes data")
    except FileNotFoundError:
        print("❌ Cody Rhodes data file not found!")
        return
    
    # Parse the data using our parser
    profile_markdown = cody_data['profile_data']['markdown']
    stats_markdown = cody_data['stats_data']['markdown']
    
    parsed_data = parse_wrestler_data(profile_markdown, stats_markdown)
    
    # Create the database structure
    database = {
        'metadata': {
            'total_wrestlers': 1,
            'scraped_at': datetime.now().isoformat(),
            'source': 'cagematch.net',
            'scraper_version': '1.0.0',
            'note': 'Initial database created from existing Cody Rhodes data'
        },
        'wrestlers': {
            '3686': {  # Cody Rhodes ID
                'wrestler_id': '3686',
                'name': 'Cody Rhodes',
                'profile_url': cody_data['profile_url'],
                'stats_url': cody_data['stats_url'],
                'raw_data': cody_data,
                'parsed_data': parsed_data,
                'scraped_at': cody_data['scraped_at']
            }
        }
    }
    
    # Save the database
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"wrestling_database_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Database created: {filename}")
    print(f"   Total wrestlers: {database['metadata']['total_wrestlers']}")
    print(f"   Wrestler: {database['wrestlers']['3686']['name']}")
    
    return filename

if __name__ == "__main__":
    create_initial_database()
