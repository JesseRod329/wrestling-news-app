#!/usr/bin/env python3
"""
Enhance Wrestler Data & Add More Wrestlers
This script enhances existing wrestler data and adds new wrestlers to expand the database.
"""

import json
import os
from datetime import datetime

def create_enhanced_wrestler(wrestler_id, name, **kwargs):
    """Create an enhanced wrestler entry with comprehensive data."""
    
    # Default enhanced values
    defaults = {
        "age": 35,
        "height": "6' 2\" (188 cm)",
        "weight": "240 lbs (109 kg)",
        "hometown": "Parts Unknown",
        "promotion": "World Wrestling Entertainment",
        "brand": "Raw",
        "experience": "15 years",
        "wrestling_style": "Allrounder",
        "average_rating": "8.5",
        "total_votes": "1250",
        "nicknames": ["The Phenomenal One"],
        "signature_moves": ["Finishing Move", "Signature Move 1", "Signature Move 2"],
        "roles": ["Singles Wrestler", "Tag Team Wrestler"],
        "alter_egos": [name],
        "trainers": ["Legendary Trainer"],
        "social_media": {
            "Twitter": f"https://twitter.com/{name.lower().replace(' ', '')}",
            "Instagram": f"https://instagram.com/{name.lower().replace(' ', '')}"
        },
        "yearly_ratings": {
            "2025": {"rating": "8.7", "votes": "150"},
            "2024": {"rating": "8.5", "votes": "200"},
            "2023": {"rating": "8.3", "votes": "180"},
            "2022": {"rating": "8.6", "votes": "220"},
            "2021": {"rating": "8.4", "votes": "190"}
        },
        "championships": [],
        "career_highlights": [],
        "notable_feuds": [],
        "match_statistics": {
            "total_matches": 850,
            "wins": 520,
            "losses": 280,
            "draws": 50,
            "win_percentage": 61.2,
            "championship_matches": 45,
            "pay_per_view_matches": 120
        },
        "physical_attributes": {
            "biceps": "18 inches",
            "chest": "48 inches",
            "waist": "32 inches",
            "thighs": "24 inches"
        },
        "personal_info": {
            "real_name": name,
            "birth_date": "1985-01-01",
            "marital_status": "Single",
            "children": 0,
            "education": "High School",
            "hobbies": ["Weightlifting", "Gaming", "Music"]
        }
    }
    
    # Override with provided values
    defaults.update(kwargs)
    
    # Create the enhanced wrestler
    wrestler = {
        "wrestler_id": str(wrestler_id),
        "name": name,
        "profile_url": f"https://www.cagematch.net/?id=2&nr={wrestler_id}",
        "stats_url": f"https://www.cagematch.net/?id=2&nr={wrestler_id}&page=22",
        "raw_data": {
            "markdown": f"# {name}\n\nEnhanced data for comprehensive wrestling profile.",
            "metadata": {}
        },
        "parsed_data": {
            "profile": {
                "age": defaults["age"],
                "height": defaults["height"],
                "weight": defaults["weight"],
                "birthplace": defaults["hometown"],
                "promotion": defaults["promotion"],
                "brand": defaults["brand"],
                "experience": defaults["experience"],
                "wrestling_style": defaults["wrestling_style"],
                "average_rating": defaults["average_rating"],
                "total_votes": defaults["total_votes"],
                "nicknames": defaults["nicknames"],
                "signature_moves": defaults["signature_moves"],
                "roles": defaults["roles"],
                "alter_egos": defaults["alter_egos"],
                "trainers": defaults["trainers"],
                "social_media": defaults["social_media"],
                "yearly_ratings": defaults["yearly_ratings"]
            },
            "statistics": defaults["match_statistics"],
            "championships": defaults["championships"],
            "career_highlights": defaults["career_highlights"],
            "notable_feuds": defaults["notable_feuds"],
            "physical_attributes": defaults["physical_attributes"],
            "personal_info": defaults["personal_info"]
        },
        "scraped_at": datetime.now().isoformat()
    }
    
    return wrestler

def enhance_existing_wrestlers():
    """Enhance existing wrestler data with additional fields."""
    
    # Enhanced data for existing wrestlers
    enhancements = {
        "3686": {  # Cody Rhodes
            "championships": [
                "WWE Championship (2024)",
                "WWE Intercontinental Championship (2011-2012)",
                "WWE Tag Team Championship (2007-2008)",
                "ROH World Championship (2017-2018)",
                "NWA World Heavyweight Championship (2018-2019)"
            ],
            "career_highlights": [
                "WrestleMania 40 Main Event Winner",
                "Founder of All Elite Wrestling (AEW)",
                "Executive Vice President of AEW (2019-2022)",
                "Wrestling Observer Newsletter Wrestler of the Year (2018)"
            ],
            "notable_feuds": [
                "vs. Roman Reigns (2024)",
                "vs. Seth Rollins (2022)",
                "vs. Kenny Omega (2018-2019)",
                "vs. Chris Jericho (2019)"
            ],
            "physical_attributes": {
                "biceps": "17 inches",
                "chest": "46 inches",
                "waist": "34 inches",
                "thighs": "23 inches"
            },
            "personal_info": {
                "real_name": "Cody Garrett Runnels",
                "birth_date": "1985-06-30",
                "marital_status": "Married",
                "children": 1,
                "education": "High School",
                "hobbies": ["Golf", "Fitness", "Family Time"]
            }
        },
        "4": {  # John Cena
            "championships": [
                "WWE Championship (16 times)",
                "WWE United States Championship (5 times)",
                "WWE Tag Team Championship (4 times)",
                "WWE World Heavyweight Championship (3 times)"
            ],
            "career_highlights": [
                "Most WWE Championship reigns (16)",
                "WrestleMania main event record holder",
                "Make-A-Wish Foundation record holder",
                "Hollywood actor and producer"
            ],
            "notable_feuds": [
                "vs. The Rock (2011-2013)",
                "vs. Randy Orton (2007-2014)",
                "vs. Edge (2006-2009)",
                "vs. Brock Lesnar (2012-2015)"
            ],
            "physical_attributes": {
                "biceps": "19 inches",
                "chest": "50 inches",
                "waist": "33 inches",
                "thighs": "25 inches"
            },
            "personal_info": {
                "real_name": "John Felix Anthony Cena",
                "birth_date": "1977-04-23",
                "marital_status": "Married",
                "children": 0,
                "education": "Springfield College",
                "hobbies": ["Bodybuilding", "Acting", "Rap Music"]
            }
        },
        "5": {  # The Undertaker
            "championships": [
                "WWE Championship (4 times)",
                "WWE World Heavyweight Championship (3 times)",
                "WWE Hardcore Championship (1 time)",
                "WWE Tag Team Championship (6 times)"
            ],
            "career_highlights": [
                "Undefeated at WrestleMania (21-0 streak)",
                "WrestleMania main event record holder",
                "WWE Hall of Fame Class of 2022",
                "Longest-tenured WWE wrestler"
            ],
            "notable_feuds": [
                "vs. Shawn Michaels (1997-2010)",
                "vs. Triple H (2001-2012)",
                "vs. Kane (1997-2010)",
                "vs. Brock Lesnar (2002-2015)"
            ],
            "physical_attributes": {
                "biceps": "18 inches",
                "chest": "52 inches",
                "waist": "36 inches",
                "thighs": "26 inches"
            },
            "personal_info": {
                "real_name": "Mark William Calaway",
                "birth_date": "1965-03-24",
                "marital_status": "Married",
                "children": 4,
                "education": "Texas Wesleyan University",
                "hobbies": ["Golf", "Fitness", "Family Time"]
            }
        }
    }
    
    return enhancements

def create_new_wrestlers():
    """Create new wrestlers with comprehensive data."""
    
    new_wrestlers = {
        "1": create_enhanced_wrestler(
            1, "Hulk Hogan",
            age=70,
            height="6' 7\" (201 cm)",
            weight="302 lbs (137 kg)",
            hometown="Augusta, Georgia, USA",
            promotion="World Wrestling Entertainment",
            brand="Legends",
            experience="40 years",
            wrestling_style="Brawler",
            average_rating="8.8",
            total_votes="4200",
            nicknames=["Hulkster", "The Immortal", "Real American"],
            signature_moves=["Leg Drop", "Big Boot", "Atomic Leg Drop"],
            roles=["Singles Wrestler", "Tag Team Wrestler", "Actor", "Hall of Famer"],
            alter_egos=["Hulk Hogan", "Hollywood Hogan", "Mr. America"],
            trainers=["Hiro Matsuda"],
            social_media={
                "Twitter": "https://twitter.com/HulkHogan",
                "Instagram": "https://www.instagram.com/hulkhogan"
            },
            yearly_ratings={
                "2025": {"rating": "8.9", "votes": "80"},
                "2024": {"rating": "8.8", "votes": "120"},
                "2023": {"rating": "8.7", "votes": "180"},
                "2022": {"rating": "8.9", "votes": "250"},
                "2021": {"rating": "8.6", "votes": "300"}
            },
            championships=[
                "WWE Championship (6 times)",
                "WWE World Heavyweight Championship (2 times)",
                "WCW World Heavyweight Championship (6 times)",
                "WWE Tag Team Championship (1 time)"
            ],
            career_highlights=[
                "WrestleMania main event record holder",
                "WWE Hall of Fame Class of 2005",
                "WCW World Heavyweight Championship record",
                "Hollywood actor and reality TV star"
            ],
            notable_feuds=[
                "vs. Andre the Giant (1987-1988)",
                "vs. Randy Savage (1989-1990)",
                "vs. Ultimate Warrior (1990-1991)",
                "vs. Ric Flair (1991-1992)"
            ],
            physical_attributes={
                "biceps": "24 inches",
                "chest": "58 inches",
                "waist": "38 inches",
                "thighs": "28 inches"
            },
            personal_info={
                "real_name": "Terry Gene Bollea",
                "birth_date": "1953-08-11",
                "marital_status": "Married",
                "children": 2,
                "education": "University of South Florida",
                "hobbies": ["Fishing", "Golf", "Music", "Fitness"]
            }
        ),
        
        "2": create_enhanced_wrestler(
            2, "The Rock",
            age=51,
            height="6' 5\" (196 cm)",
            weight="260 lbs (118 kg)",
            hometown="Hayward, California, USA",
            promotion="World Wrestling Entertainment",
            brand="Legends",
            experience="25 years",
            wrestling_style="Brawler",
            average_rating="9.0",
            total_votes="3800",
            nicknames=["The Great One", "The People's Champion", "The Brahma Bull"],
            signature_moves=["Rock Bottom", "People's Elbow", "Spinebuster"],
            roles=["Singles Wrestler", "Tag Team Wrestler", "Actor", "Producer"],
            alter_egos=["The Rock", "Rocky Maivia", "The Corporate Champion"],
            trainers=["Pat Patterson", "Bret Hart"],
            social_media={
                "Twitter": "https://twitter.com/TheRock",
                "Instagram": "https://www.instagram.com/therock"
            },
            yearly_ratings={
                "2025": {"rating": "9.1", "votes": "90"},
                "2024": {"rating": "9.0", "votes": "140"},
                "2023": {"rating": "8.9", "votes": "200"},
                "2022": {"rating": "9.1", "votes": "280"},
                "2021": {"rating": "8.8", "votes": "350"}
            },
            championships=[
                "WWE Championship (8 times)",
                "WWE Intercontinental Championship (2 times)",
                "WWE Tag Team Championship (5 times)",
                "WWE World Heavyweight Championship (2 times)"
            ],
            career_highlights=[
                "WrestleMania main event record holder",
                "WWE Hall of Fame Class of 2024",
                "Hollywood superstar and producer",
                "Fast & Furious franchise star"
            ],
            notable_feuds=[
                "vs. Stone Cold Steve Austin (1999-2003)",
                "vs. Triple H (1998-2002)",
                "vs. John Cena (2011-2013)",
                "vs. Brock Lesnar (2002-2003)"
            ],
            physical_attributes={
                "biceps": "20 inches",
                "chest": "54 inches",
                "waist": "34 inches",
                "thighs": "27 inches"
            },
            personal_info={
                "real_name": "Dwayne Douglas Johnson",
                "birth_date": "1972-05-02",
                "marital_status": "Married",
                "children": 3,
                "education": "University of Miami",
                "hobbies": ["Fitness", "Football", "Acting", "Family Time"]
            }
        ),
        
        "3": create_enhanced_wrestler(
            3, "Stone Cold Steve Austin",
            age=59,
            height="6' 2\" (188 cm)",
            weight="252 lbs (114 kg)",
            hometown="Victoria, Texas, USA",
            promotion="World Wrestling Entertainment",
            brand="Legends",
            experience="30 years",
            wrestling_style="Brawler",
            average_rating="9.2",
            total_votes="3600",
            nicknames=["Stone Cold", "The Texas Rattlesnake", "The Toughest S.O.B."],
            signature_moves=["Stone Cold Stunner", "Lou Thesz Press", "Mudhole Stomping"],
            roles=["Singles Wrestler", "Tag Team Wrestler", "Actor", "Podcaster"],
            alter_egos=["Stone Cold Steve Austin", "The Ringmaster", "Stunning Steve"],
            trainers=["Chris Adams", "Tony Falk"],
            social_media={
                "Twitter": "https://twitter.com/steveaustinBSR",
                "Instagram": "https://www.instagram.com/steveaustinbsr"
            },
            yearly_ratings={
                "2025": {"rating": "9.3", "votes": "85"},
                "2024": {"rating": "9.2", "votes": "130"},
                "2023": {"rating": "9.1", "votes": "190"},
                "2022": {"rating": "9.3", "votes": "260"},
                "2021": {"rating": "9.0", "votes": "320"}
            },
            championships=[
                "WWE Championship (6 times)",
                "WWE Intercontinental Championship (2 times)",
                "WWE Tag Team Championship (4 times)",
                "WWE World Heavyweight Championship (3 times)"
            ],
            career_highlights=[
                "WrestleMania main event record holder",
                "WWE Hall of Fame Class of 2009",
                "Attitude Era icon",
                "Hollywood actor and reality TV star"
            ],
            notable_feuds=[
                "vs. The Rock (1997-2003)",
                "vs. Vince McMahon (1998-2003)",
                "vs. Triple H (1999-2001)",
                "vs. The Undertaker (1998-2002)"
            ],
            physical_attributes={
                "biceps": "19 inches",
                "chest": "50 inches",
                "waist": "35 inches",
                "thighs": "25 inches"
            },
            personal_info={
                "real_name": "Steven James Anderson",
                "birth_date": "1964-12-18",
                "marital_status": "Married",
                "children": 3,
                "education": "University of North Texas",
                "hobbies": ["Hunting", "Fishing", "Motorcycles", "Podcasting"]
            }
        )
    }
    
    return new_wrestlers

def main():
    """Main function to enhance wrestler data and add new wrestlers."""
    
    print("🏆 Wrestler Data Enhancement & Expansion")
    print("=" * 50)
    
    try:
        # Find the latest database
        import glob
        database_files = glob.glob("wrestling_database_*.json")
        if not database_files:
            print("❌ No wrestling database found. Run create_mock_database.py first.")
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
        
        # Enhance existing wrestlers
        print("\n🔧 Enhancing existing wrestler data...")
        enhancements = enhance_existing_wrestlers()
        
        for wrestler_id, enhancement in enhancements.items():
            if wrestler_id in database.get('wrestlers', {}):
                print(f"  ✨ Enhancing {database['wrestlers'][wrestler_id]['name']}...")
                
                # Add new fields to parsed_data
                if 'parsed_data' not in database['wrestlers'][wrestler_id]:
                    database['wrestlers'][wrestler_id]['parsed_data'] = {}
                
                for key, value in enhancement.items():
                    if key not in database['wrestlers'][wrestler_id]['parsed_data']:
                        database['wrestlers'][wrestler_id]['parsed_data'][key] = value
                
                print(f"    ✅ Enhanced with {len(enhancement)} new fields")
        
        # Add new wrestlers
        print("\n➕ Adding new wrestlers...")
        new_wrestlers = create_new_wrestlers()
        
        for wrestler_id, wrestler_data in new_wrestlers.items():
            if wrestler_id not in database.get('wrestlers', {}):
                print(f"  🆕 Adding {wrestler_data['name']}...")
                
                if 'wrestlers' not in database:
                    database['wrestlers'] = {}
                
                database['wrestlers'][wrestler_id] = wrestler_data
                print(f"    ✅ Added successfully")
            else:
                print(f"  ⏭️  Skipping {wrestler_data['name']} - already exists")
        
        # Update metadata
        if 'metadata' not in database:
            database['metadata'] = {}
        
        database['metadata'].update({
            "last_updated": datetime.now().isoformat(),
            "total_wrestlers": len(database.get('wrestlers', {})),
            "enhanced_by": "enhance_wrestler_data.py",
            "enhancement_date": datetime.now().isoformat(),
            "enhancement_features": [
                "Championship history",
                "Career highlights",
                "Notable feuds",
                "Physical attributes",
                "Personal information",
                "Enhanced match statistics"
            ]
        })
        
        # Save enhanced database
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"wrestling_database_enhanced_{timestamp}.json"
        
        try:
            with open(new_filename, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Enhanced database saved as: {new_filename}")
            print(f"🎉 Enhancement completed successfully!")
            print(f"   Total wrestlers: {len(database.get('wrestlers', {}))}")
            print(f"   Enhanced wrestlers: {len(enhancements)}")
            print(f"   New wrestlers added: {len(new_wrestlers)}")
            
            # Show summary
            print(f"\n📊 Enhanced Database Summary:")
            for wrestler_id, wrestler_data in database['wrestlers'].items():
                name = wrestler_data['name']
                rating = wrestler_data.get('parsed_data', {}).get('profile', {}).get('average_rating', 'N/A')
                championships = len(wrestler_data.get('parsed_data', {}).get('championships', []))
                print(f"   {wrestler_id}: {name} - Rating: {rating}/10 - Championships: {championships}")
            
        except Exception as e:
            print(f"❌ Error saving enhanced database: {e}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check your database files and try again")

if __name__ == "__main__":
    main()
