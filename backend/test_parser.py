import json
from wrestler_data_parser import parse_wrestler_data

def test_parser():
    """Test the data parser with real scraped data."""
    
    # Load the Cody Rhodes data we scraped
    try:
        with open('cody_rhodes_20250814_163533.json', 'r', encoding='utf-8') as f:
            cody_data = json.load(f)
        
        print("✅ Loaded Cody Rhodes data successfully")
        print(f"   Profile content length: {len(cody_data['profile_data']['markdown'])} characters")
        print(f"   Stats content length: {len(cody_data['stats_data']['markdown'])} characters")
        
    except FileNotFoundError:
        print("❌ Cody Rhodes data file not found. Run the scraper first.")
        return
    except Exception as e:
        print(f"❌ Error loading data: {str(e)}")
        return
    
    # Test the parser
    print("\n🔍 Testing Data Parser...")
    
    profile_markdown = cody_data['profile_data']['markdown']
    stats_markdown = cody_data['stats_data']['markdown']
    
    parsed_data = parse_wrestler_data(profile_markdown, stats_markdown)
    
    print("\n📊 Parsed Profile Data:")
    print("=" * 40)
    
    profile = parsed_data.get('profile', {})
    
    # Display key information
    key_fields = [
        'age', 'height', 'weight', 'birthplace', 'gender',
        'promotion', 'brand', 'career_start', 'experience',
        'wrestling_style', 'average_rating', 'total_votes'
    ]
    
    for field in key_fields:
        value = profile.get(field, 'Not found')
        print(f"{field.replace('_', ' ').title()}: {value}")
    
    print(f"\nTrainers: {', '.join(profile.get('trainers', []))}")
    print(f"Nicknames: {', '.join(profile.get('nicknames', []))}")
    print(f"Signature Moves: {', '.join(profile.get('signature_moves', []))}")
    print(f"Alter Egos: {', '.join(profile.get('alter_egos', []))}")
    print(f"Roles: {', '.join(profile.get('roles', []))}")
    
    print(f"\nSocial Media:")
    social_media = profile.get('social_media', {})
    for platform, handle in social_media.items():
        print(f"  {platform.title()}: {handle}")
    
    print(f"\nYearly Ratings:")
    yearly_ratings = profile.get('yearly_ratings', {})
    for year, data in yearly_ratings.items():
        print(f"  {year}: {data['rating']}/10 ({data['votes']} votes)")
    
    print(f"\n📈 Parsed Statistics Data:")
    print("=" * 40)
    
    stats = parsed_data.get('statistics', {})
    for key, value in stats.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print(f"\n🎯 Parser Test Summary:")
    print("=" * 40)
    print(f"Profile fields extracted: {len([k for k, v in profile.items() if v])}")
    print(f"Statistics fields extracted: {len([k for k, v in stats.items() if v])}")
    print(f"Total data points: {len(parsed_data)}")
    
    # Save parsed data for inspection
    output_file = f"parsed_cody_rhodes_{cody_data['scraped_at'][:10]}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Parsed data saved to: {output_file}")
    
    return parsed_data

if __name__ == "__main__":
    test_parser()
