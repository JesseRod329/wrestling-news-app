import json
import os
import re
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

class WrestlingAPI:
    def __init__(self):
        self.database_file = 'wrestling_database_accurate_final_v2_20250815_023309.json'
        self.data = self.load_database()
    
    def load_database(self):
        """Load the accurate Cagematch database"""
        try:
            if os.path.exists(self.database_file):
                with open(self.database_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ Loaded accurate database with {data.get('metadata', {}).get('total_wrestlers', 0)} wrestlers")
                    return data
            else:
                print(f"❌ Database file {self.database_file} not found")
                return {"wrestlers": [], "metadata": {}}
        except Exception as e:
            print(f"❌ Error loading database: {e}")
            return {"wrestlers": [], "metadata": {}}
    
    def get_all_wrestlers(self):
        """Get all wrestlers from the accurate database"""
        wrestlers_data = self.data.get('wrestlers', [])
        print(f"🔍 Raw wrestlers data count: {len(wrestlers_data)}")
        
        # Transform the data to match frontend expectations
        transformed_wrestlers = []
        for wrestler in wrestlers_data:
            # Debug: Print what we're working with
            print(f"🔍 Processing wrestler: {wrestler.get('name', 'Unknown')}")
            print(f"   - cagematch_id: {wrestler.get('cagematch_id')}")
            print(f"   - profile_url: {wrestler.get('profile_url')}")
            print(f"   - image_url: {wrestler.get('image_url')}")
            
            transformed_wrestler = {
                'id': wrestler.get('id', ''),
                'name': wrestler.get('name', ''),
                'nickname': wrestler.get('nicknames', [''])[0] if wrestler.get('nicknames') else '',
                'realName': wrestler.get('real_name', ''),
                'image_url': self.get_wrestler_image(wrestler),  # This should now work
                'age': wrestler.get('age_numeric', 0),
                'height': wrestler.get('height', ''),
                'weight': wrestler.get('weight', ''),
                'hometown': wrestler.get('hometown', ''),
                'promotion': wrestler.get('promotion', ''),
                'wrestlingStyle': wrestler.get('wrestling_style', ''),
                'experience': wrestler.get('experience', ''),
                'trainers': wrestler.get('trainers', []),
                'signatureMoves': wrestler.get('signature_moves', []),
                'socialMedia': wrestler.get('social_media', {}),
                'averageRating': wrestler.get('averageRating', 0),
                'totalRatings': wrestler.get('total_votes', 0),
                'careerStats': self.calculate_career_stats(wrestler),
                'championships': self.get_championships(wrestler),
                'bio': self.generate_bio(wrestler),
                'cagematch_id': wrestler.get('cagematch_id', ''),
                'profile_url': wrestler.get('profile_url', ''),
                'stats_url': wrestler.get('stats_url', ''),
                'debut': wrestler.get('debut', ''),
                'background_sports': wrestler.get('background_sports', ''),
                'alter_egos': wrestler.get('alter_egos', []),
                'roles': wrestler.get('roles', []),
                'brand': wrestler.get('brand', ''),
                'gender': wrestler.get('gender', ''),
                'total_comments': wrestler.get('total_comments', 0)
            }
            
            print(f"   - Final image_url: {transformed_wrestler['image_url']}")
            transformed_wrestlers.append(transformed_wrestler)
        
        return transformed_wrestlers
    
    def get_wrestler_image(self, wrestler):
        """Get the best available image for a wrestler with working fallbacks"""
        wrestler_name = wrestler.get('name', 'Unknown')
        
        # Try to get image from the wrestler's own image field first
        if wrestler.get('image_url') and wrestler['image_url'].strip():
            print(f"🔍 Using wrestler's own image: {wrestler['image_url']} for {wrestler_name}")
            return wrestler['image_url']
        
        # Try to get image from profile_url if available
        profile_url = wrestler.get('profile_url', '')
        if profile_url and 'nr=' in profile_url:
            match = re.search(r'nr=(\d+)', profile_url)
            if match:
                wrestler_id = match.group(1)
                image_url = f"https://www.cagematch.net/pictures/profile/{wrestler_id}.jpg"
                print(f"🔍 Trying profile URL image: {image_url} for {wrestler_name}")
                return image_url
        
        # Try to get image from stats_url if available
        stats_url = wrestler.get('stats_url', '')
        if stats_url and 'nr=' in stats_url:
            match = re.search(r'nr=(\d+)', stats_url)
            if match:
                wrestler_id = match.group(1)
                image_url = f"https://www.cagematch.net/pictures/profile/{wrestler_id}.jpg"
                print(f"🔍 Trying stats URL image: {image_url} for {wrestler_name}")
                return image_url
        
        # Generate a nice avatar with the wrestler's initials as fallback
        print(f"⚠️ No image found for {wrestler_name}, using generated avatar")
        initials = ''.join([name[0].upper() for name in wrestler_name.split()[:2]])
        return f"https://ui-avatars.com/api/?name={wrestler_name}&background=6366f1&color=fff&size=200&font-size=0.4&length=2&bold=true&initials={initials}"
    
    def calculate_career_stats(self, wrestler):
        """Calculate career statistics (placeholder for now)"""
        # In a real implementation, this would scrape match history
        return {
            'totalMatches': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'winPercentage': 0
        }
    
    def get_championships(self, wrestler):
        """Get championships (would need to be scraped from Cagematch)"""
        # Placeholder - would need to scrape championship history
        return []
    
    def generate_bio(self, wrestler):
        """Generate a bio from available data"""
        parts = []
        
        if wrestler.get('hometown'):
            parts.append(f"From {wrestler['hometown']}")
        
        if wrestler.get('experience'):
            parts.append(f"Professional wrestler with {wrestler['experience']} of experience")
        
        if wrestler.get('wrestling_style'):
            parts.append(f"Known for {wrestler['wrestling_style']} wrestling style")
        
        if wrestler.get('trainers'):
            parts.append(f"Trained by {', '.join(wrestler['trainers'])}")
        
        if wrestler.get('background_sports'):
            parts.append(f"Background in {wrestler['background_sports']}")
        
        if not parts:
            return f"Professional wrestler {wrestler.get('name', '')}"
        
        return '. '.join(parts) + '.'
    
    def get_database_stats(self):
        """Get database statistics"""
        metadata = self.data.get('metadata', {})
        return {
            'total_wrestlers': metadata.get('total_wrestlers', 0),
            'source': metadata.get('data_source', 'Unknown'),
            'scraper_version': metadata.get('version', 'Unknown'),
            'scraped_at': metadata.get('created_at', 'Unknown'),
            'data_quality': metadata.get('data_quality', 'Unknown')
        }
    
    def get_wrestler_by_id(self, wrestler_id):
        """Get a specific wrestler by ID"""
        wrestlers = self.get_all_wrestlers()
        for wrestler in wrestlers:
            if wrestler['id'] == wrestler_id:
                return wrestler
        return None

def search_wrestlers(self, query: str):
    """Search wrestlers by name"""
    query = query.lower()
    if not query:
        return []
    
    wrestlers = self.get_all_wrestlers()
    results = [
        wrestler for wrestler in wrestlers 
        if query in wrestler['name'].lower() or 
           query in wrestler.get('nickname', '').lower() or
           query in wrestler.get('realName', '').lower()
    ]
    
    return results

def get_top_rated_wrestlers(self, limit: int = 10):
    """Get top-rated wrestlers"""
    wrestlers = self.get_all_wrestlers()
    # Sort by average rating (highest first)
    sorted_wrestlers = sorted(
        wrestlers, 
        key=lambda x: float(x.get('averageRating', 0)), 
        reverse=True
    )
    return sorted_wrestlers[:limit]

def get_promotions(self):
    """Get all unique promotions"""
    wrestlers = self.get_all_wrestlers()
    promotions = set()
    for wrestler in wrestlers:
        if wrestler.get('promotion'):
            promotions.add(wrestler['promotion'])
    return list(promotions)

def get_wrestler(self, wrestler_id: str):
    """Alias for get_wrestler_by_id to match expected method name"""
    return self.get_wrestler_by_id(wrestler_id)

# Initialize database
database = WrestlingAPI()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database_loaded': len(database.data.get('wrestlers', [])) > 0,
        'total_wrestlers': len(database.data.get('wrestlers', []))
    })

@app.route('/api/wrestlers', methods=['GET'])
def get_all_wrestlers():
    """Get all wrestlers"""
    try:
        wrestlers = database.get_all_wrestlers()
        return jsonify({'wrestlers': wrestlers})  # Wrap in object with 'wrestlers' key
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/wrestlers/<wrestler_id>', methods=['GET'])
def get_wrestler(wrestler_id):
    """Get a specific wrestler by ID"""
    try:
        wrestler = database.get_wrestler_by_id(wrestler_id)
        if wrestler:
            return jsonify(wrestler)
        else:
            return jsonify({'error': 'Wrestler not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_database_stats():
    """Get database statistics"""
    try:
        stats = database.get_database_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search_wrestlers():
    """Search wrestlers by name"""
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify({'results': []})  # Wrap in object with 'results' key
        
        wrestlers = database.get_all_wrestlers()
        results = [
            wrestler for wrestler in wrestlers 
            if query in wrestler['name'].lower() or 
               query in wrestler.get('nickname', '').lower() or
               query in wrestler.get('realName', '').lower()
        ]
        
        return jsonify({'results': results})  # Wrap in object with 'results' key
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/wrestlers/<wrestler_id>/stats', methods=['GET'])
def get_wrestler_stats(wrestler_id):
    """Get statistics for a specific wrestler"""
    try:
        wrestler = database.get_wrestler_by_id(wrestler_id)
        if wrestler:
            # Return the wrestler's career stats
            stats = {
                'wrestler_id': wrestler_id,
                'name': wrestler.get('name', ''),
                'careerStats': wrestler.get('careerStats', {}),
                'averageRating': wrestler.get('averageRating', 0),
                'totalRatings': wrestler.get('totalRatings', 0),
                'championships': wrestler.get('championships', []),
                'experience': wrestler.get('experience', ''),
                'wrestlingStyle': wrestler.get('wrestlingStyle', ''),
                'promotion': wrestler.get('promotion', ''),
                'debut': wrestler.get('debut', ''),
                'background_sports': wrestler.get('background_sports', ''),
                'trainers': wrestler.get('trainers', []),
                'signatureMoves': wrestler.get('signatureMoves', [])
            }
            return jsonify(stats)
        else:
            return jsonify({'error': 'Wrestler not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Wrestling API with ACCURATE Cagematch data...")
    print(f"📊 Database: {database.database_file}")
    print(f"👥 Wrestlers loaded: {len(database.data.get('wrestlers', []))}")
    print(f"🔗 API will be available at: http://localhost:5001")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=True)
