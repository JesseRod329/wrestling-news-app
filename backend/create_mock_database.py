#!/usr/bin/env python3
"""
Create Mock Wrestling Database
This script creates a mock database with sample wrestler data for testing.
"""

import json
import os
from datetime import datetime

def create_mock_wrestler(wrestler_id, name, **kwargs):
    """Create a mock wrestler entry with realistic data."""
    
    # Default values
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
        "nicknames": ["The Phenomenal One", "The Face That Runs The Place"],
        "signature_moves": ["Styles Clash", "Phenomenal Forearm", "Calf Crusher"],
        "roles": ["Singles Wrestler", "Tag Team Wrestler"],
        "alter_egos": [name],
        "trainers": ["Ricky Steamboat", "Harley Race"],
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
        }
    }
    
    # Override with provided values
    defaults.update(kwargs)
    
    # Create the mock wrestler
    wrestler = {
        "wrestler_id": str(wrestler_id),
        "name": name,
        "profile_url": f"https://www.cagematch.net/?id=2&nr={wrestler_id}",
        "stats_url": f"https://www.cagematch.net/?id=2&nr={wrestler_id}&page=22",
        "raw_data": {
            "markdown": f"# {name}\n\nMock data for testing purposes.",
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
            "statistics": {
                "total_matches": 850,
                "wins": 520,
                "losses": 280,
                "draws": 50,
                "win_percentage": 61.2
            }
        },
        "scraped_at": datetime.now().isoformat()
    }
    
    return wrestler

def create_mock_database():
    """Create a mock wrestling database with multiple wrestlers."""
    
    # Create mock wrestlers with realistic data
    mock_wrestlers = {
        "3686": create_mock_wrestler(
            3686, "Cody Rhodes",
            age=40,
            height="6' 1\" (185 cm)",
            weight="220 lbs (100 kg)",
            hometown="Charlotte, North Carolina, USA",
            promotion="World Wrestling Entertainment",
            brand="SmackDown",
            experience="19 years",
            wrestling_style="Allrounder",
            average_rating="7.86",
            total_votes="1587",
            nicknames=["The American Nightmare", "Dashing", "The Grandson Of A Plumber"],
            signature_moves=["Cross Rhodes", "Beautiful Disaster", "Cody Cutter"],
            roles=["Singles Wrestler", "Tag Team Wrestler", "Promoter"],
            alter_egos=["Cody Rhodes", "Stardust", "Fuego II"],
            trainers=["Al Snow", "Bruno Sassi", "Dusty Rhodes", "Ray Lloyd"],
            social_media={
                "Twitter": "https://x.com/CodyRhodes",
                "Instagram": "https://www.instagram.com/americannightmarecody",
                "TikTok": "https://www.tiktok.com/@americannightmarecody",
                "YouTube": "https://www.youtube.com/@nightmarefamily"
            },
            yearly_ratings={
                "2025": {"rating": "8.58", "votes": "195"},
                "2024": {"rating": "8.52", "votes": "243"},
                "2023": {"rating": "8.31", "votes": "157"},
                "2022": {"rating": "8.14", "votes": "139"},
                "2021": {"rating": "7.62", "votes": "130"}
            }
        ),
        
        "4": create_mock_wrestler(
            4, "John Cena",
            age=47,
            height="6' 1\" (185 cm)",
            weight="251 lbs (114 kg)",
            hometown="West Newbury, Massachusetts, USA",
            promotion="World Wrestling Entertainment",
            brand="Free Agent",
            experience="22 years",
            wrestling_style="Powerhouse",
            average_rating="8.2",
            total_votes="2100",
            nicknames=["The Champ", "The Face of WWE", "The Doctor of Thuganomics"],
            signature_moves=["Attitude Adjustment", "STF", "Five Knuckle Shuffle"],
            roles=["Singles Wrestler", "Tag Team Wrestler", "Actor"],
            alter_egos=["John Cena", "The Prototype"],
            trainers=["Ultimate Pro Wrestling", "Ohio Valley Wrestling"],
            social_media={
                "Twitter": "https://twitter.com/JohnCena",
                "Instagram": "https://www.instagram.com/johncena"
            },
            yearly_ratings={
                "2025": {"rating": "8.4", "votes": "180"},
                "2024": {"rating": "8.2", "votes": "220"},
                "2023": {"rating": "8.1", "votes": "200"},
                "2022": {"rating": "8.3", "votes": "250"},
                "2021": {"rating": "8.0", "votes": "300"}
            }
        ),
        
        "5": create_mock_wrestler(
            5, "The Undertaker",
            age=59,
            height="6' 10\" (208 cm)",
            weight="299 lbs (136 kg)",
            hometown="Houston, Texas, USA",
            promotion="World Wrestling Entertainment",
            brand="Legends",
            experience="30 years",
            wrestling_style="Brawler",
            average_rating="9.1",
            total_votes="3500",
            nicknames=["The Deadman", "The Phenom", "The American Bad Ass"],
            signature_moves=["Tombstone Piledriver", "Chokeslam", "Last Ride"],
            roles=["Singles Wrestler", "Tag Team Wrestler", "Hall of Famer"],
            alter_egos=["The Undertaker", "Mean Mark Callous", "Kane"],
            trainers=["Don Jardine", "Boris Malenko"],
            social_media={
                "Twitter": "https://twitter.com/undertaker",
                "Instagram": "https://www.instagram.com/undertaker"
            },
            yearly_ratings={
                "2025": {"rating": "9.2", "votes": "100"},
                "2024": {"rating": "9.1", "votes": "150"},
                "2023": {"rating": "9.0", "votes": "200"},
                "2022": {"rating": "9.3", "votes": "300"},
                "2021": {"rating": "9.1", "votes": "400"}
            }
        ),
        
        "6": create_mock_wrestler(
            6, "Triple H",
            age=54,
            height="6' 4\" (193 cm)",
            weight="255 lbs (116 kg)",
            hometown="Greenwich, Connecticut, USA",
            promotion="World Wrestling Entertainment",
            brand="Executive",
            experience="28 years",
            wrestling_style="Technical",
            average_rating="8.7",
            total_votes="2800",
            nicknames=["The Game", "The Cerebral Assassin", "The King of Kings"],
            signature_moves=["Pedigree", "Spinebuster", "Facebuster"],
            roles=["Singles Wrestler", "Tag Team Wrestler", "Executive"],
            alter_egos=["Triple H", "Hunter Hearst Helmsley", "Terra Ryzing"],
            trainers=["Killer Kowalski"],
            social_media={
                "Twitter": "https://twitter.com/TripleH",
                "Instagram": "https://www.instagram.com/tripleh"
            },
            yearly_ratings={
                "2025": {"rating": "8.8", "votes": "80"},
                "2024": {"rating": "8.7", "votes": "120"},
                "2023": {"rating": "8.6", "votes": "150"},
                "2022": {"rating": "8.8", "votes": "200"},
                "2021": {"rating": "8.5", "votes": "250"}
            }
        ),
        
        "7": create_mock_wrestler(
            7, "Shawn Michaels",
            age=58,
            height="6' 1\" (185 cm)",
            weight="225 lbs (102 kg)",
            hometown="San Antonio, Texas, USA",
            promotion="World Wrestling Entertainment",
            brand="Legends",
            experience="32 years",
            wrestling_style="High Flyer",
            average_rating="9.3",
            total_votes="3200",
            nicknames=["The Heartbreak Kid", "HBK", "Mr. WrestleMania"],
            signature_moves=["Sweet Chin Music", "Flying Elbow Drop", "Moonsault"],
            roles=["Singles Wrestler", "Tag Team Wrestler", "Hall of Famer"],
            alter_egos=["Shawn Michaels", "The Rockers"],
            trainers=["Jose Lothario"],
            social_media={
                "Twitter": "https://twitter.com/ShawnMichaels",
                "Instagram": "https://www.instagram.com/shawnmichaels"
            },
            yearly_ratings={
                "2025": {"rating": "9.4", "votes": "90"},
                "2024": {"rating": "9.3", "votes": "130"},
                "2023": {"rating": "9.2", "votes": "180"},
                "2022": {"rating": "9.4", "votes": "250"},
                "2021": {"rating": "9.1", "votes": "300"}
            }
        ),
        
        "8": create_mock_wrestler(
            8, "Bret Hart",
            age=66,
            height="6' 0\" (183 cm)",
            weight="235 lbs (107 kg)",
            hometown="Calgary, Alberta, Canada",
            promotion="World Wrestling Entertainment",
            brand="Legends",
            experience="35 years",
            wrestling_style="Technical",
            average_rating="9.4",
            total_votes="2800",
            nicknames=["The Hitman", "The Excellence of Execution", "The Best There Is"],
            signature_moves=["Sharpshooter", "Russian Leg Sweep", "Piledriver"],
            roles=["Singles Wrestler", "Tag Team Wrestler", "Hall of Famer"],
            alter_egos=["Bret Hart", "The Hart Foundation"],
            trainers=["Stu Hart", "Dynamite Kid"],
            social_media={
                "Twitter": "https://twitter.com/BretHart",
                "Instagram": "https://www.instagram.com/brethart"
            },
            yearly_ratings={
                "2025": {"rating": "9.5", "votes": "70"},
                "2024": {"rating": "9.4", "votes": "110"},
                "2023": {"rating": "9.3", "votes": "160"},
                "2022": {"rating": "9.5", "votes": "220"},
                "2021": {"rating": "9.2", "votes": "280"}
            }
        )
    }
    
    # Create the database structure
    database = {
        "wrestlers": mock_wrestlers,
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "total_wrestlers": len(mock_wrestlers),
            "source": "Mock Database for Testing",
            "scraper_version": "1.0.0",
            "description": "Mock wrestling database with sample data for testing the frontend without requiring additional Firecrawl API calls"
        }
    }
    
    return database

def main():
    """Main function to create and save the mock database."""
    
    print("🏆 Creating Mock Wrestling Database")
    print("=" * 40)
    
    try:
        # Create the mock database
        database = create_mock_database()
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wrestling_database_mock_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Mock database created successfully!")
        print(f"📁 File: {filename}")
        print(f"👥 Wrestlers: {len(database['wrestlers'])}")
        print(f"📊 Total wrestlers: {database['metadata']['total_wrestlers']}")
        
        # Show wrestler list
        print(f"\n🏆 Wrestlers in Mock Database:")
        for wrestler_id, wrestler_data in database['wrestlers'].items():
            name = wrestler_data['name']
            rating = wrestler_data['parsed_data']['profile']['average_rating']
            print(f"   {wrestler_id}: {name} - Rating: {rating}/10")
        
        print(f"\n💡 You can now test the expanded frontend with multiple wrestlers!")
        print(f"   The API will automatically use this new database file.")
        
    except Exception as e:
        print(f"❌ Error creating mock database: {e}")

if __name__ == "__main__":
    main()
