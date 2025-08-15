from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
from typing import Dict, Any, List

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

class WrestlingAPI:
    """API server for accessing wrestling database data."""
    
    def __init__(self):
        self.database = {}
        self.database_file = None
        self.load_latest_database()
    
    def load_latest_database(self):
        """Load the most recent wrestling database file."""
        try:
            # Look for the most recent database file
            database_files = [f for f in os.listdir('.') if f.startswith('wrestling_database_') and f.endswith('.json')]
            
            if database_files:
                # Sort by creation time and get the latest
                database_files.sort(key=lambda x: os.path.getctime(x), reverse=True)
                latest_file = database_files[0]
                
                with open(latest_file, 'r', encoding='utf-8') as f:
                    self.database = json.load(f)
                self.database_file = latest_file
                
                print(f"📂 Loaded database: {latest_file}")
                print(f"   Total wrestlers: {len(self.database.get('wrestlers', {}))}")
            else:
                print("⚠️  No wrestling database files found. Run the auto-scraper first.")
                
        except Exception as e:
            print(f"Error loading database: {str(e)}")
    
    def reload_database(self):
        """Reload the database from file."""
        self.load_latest_database()
        return {"message": "Database reloaded", "total_wrestlers": len(self.database.get('wrestlers', {}))}
    
    def get_all_wrestlers(self, limit: int = None, offset: int = 0) -> Dict[str, Any]:
        """Get all wrestlers with optional pagination."""
        wrestlers_data = self.database.get('wrestlers', [])
        
        # Handle both old dictionary format and new list format
        if isinstance(wrestlers_data, dict):
            wrestlers = list(wrestlers_data.values())
        else:
            wrestlers = wrestlers_data
        
        if limit:
            wrestlers = wrestlers[offset:offset + limit]
        
        return {
            "wrestlers": wrestlers,
            "total": len(wrestlers),
            "limit": limit,
            "offset": offset
        }
    
    def get_wrestler_by_id(self, wrestler_id: str) -> Dict[str, Any]:
        """Get a specific wrestler by ID."""
        wrestlers_data = self.database.get('wrestlers', [])
        
        # Handle both old dictionary format and new list format
        if isinstance(wrestlers_data, dict):
            wrestler = wrestlers_data.get(wrestler_id)
        else:
            # For list format, find by ID field
            wrestler = next((w for w in wrestlers_data if w.get('id') == wrestler_id), None)
        
        if not wrestler:
            return {"error": "Wrestler not found"}, 404
        
        return wrestler
    
    def search_wrestlers(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search wrestlers by name or other criteria."""
        query = query.lower()
        results = []
        
        wrestlers_data = self.database.get('wrestlers', [])
        
        # Handle both old dictionary format and new list format
        if isinstance(wrestlers_data, dict):
            wrestlers_to_search = wrestlers_data.values()
        else:
            wrestlers_to_search = wrestlers_data
        
        for wrestler in wrestlers_to_search:
            name = wrestler.get('name', '').lower()
            if query in name:
                results.append(wrestler)
                
                if len(results) >= limit:
                    break
        
        return {
            "query": query,
            "results": results,
            "total_found": len(results),
            "wrestlers": results  # Add this for compatibility
        }
    
    def get_wrestlers_by_promotion(self, promotion: str) -> Dict[str, Any]:
        """Get all wrestlers from a specific promotion."""
        results = []
        
        wrestlers_data = self.database.get('wrestlers', [])
        
        # Handle both old dictionary format and new list format
        if isinstance(wrestlers_data, dict):
            wrestlers_to_search = wrestlers_data.values()
        else:
            wrestlers_to_search = wrestlers_data
        
        for wrestler in wrestlers_to_search:
            # Handle both old and new data structures
            if 'parsed_data' in wrestler:
                # Old format
                parsed_data = wrestler.get('parsed_data', {})
                profile = parsed_data.get('profile', {})
                wrestler_promotion = profile.get('promotion', '')
            else:
                # New format - direct fields
                wrestler_promotion = wrestler.get('promotion', '')
            
            if promotion.lower() in wrestler_promotion.lower():
                results.append(wrestler)
        
        return {
            "promotion": promotion,
            "wrestlers": results,
            "total": len(results)
        }
    
    def get_top_rated_wrestlers(self, limit: int = 10) -> Dict[str, Any]:
        """Get top rated wrestlers."""
        wrestlers_with_ratings = []
        
        wrestlers_data = self.database.get('wrestlers', [])
        
        # Handle both old dictionary format and new list format
        if isinstance(wrestlers_data, dict):
            wrestlers_to_search = wrestlers_data.values()
        else:
            wrestlers_to_search = wrestlers_data
        
        for wrestler in wrestlers_to_search:
            # Handle both old and new data structures
            if 'parsed_data' in wrestler:
                # Old format
                parsed_data = wrestler.get('parsed_data', {})
                profile = parsed_data.get('profile', {})
                rating = profile.get('average_rating')
                promotion = profile.get('promotion', 'Unknown')
            else:
                # New format - direct fields
                rating = wrestler.get('averageRating') or wrestler.get('average_rating')
                promotion = wrestler.get('promotion', 'Unknown')
            
            if rating:
                try:
                    rating_float = float(rating)
                    wrestlers_with_ratings.append({
                        'id': wrestler.get('id', wrestler.get('wrestler_id', 'Unknown')),
                        'name': wrestler.get('name', 'Unknown'),
                        'rating': rating_float,
                        'promotion': promotion,
                        'wrestler_data': wrestler
                    })
                except ValueError:
                    continue
        
        # Sort by rating (highest first)
        wrestlers_with_ratings.sort(key=lambda x: x['rating'], reverse=True)
        
        return {
            "wrestlers": [w['wrestler_data'] for w in wrestlers_with_ratings[:limit]],
            "total": len(wrestlers_with_ratings)
        }
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get overall database statistics."""
        wrestlers_data = self.database.get('wrestlers', [])
        
        # Handle both old dictionary format and new list format
        if isinstance(wrestlers_data, dict):
            wrestlers = wrestlers_data
        else:
            wrestlers = wrestlers_data
        
        stats = {
            "total_wrestlers": len(wrestlers),
            "database_file": self.database_file,
            "last_updated": self.database.get('metadata', {}).get('scraped_at'),
            "promotions": {},
            "wrestling_styles": {},
            "total_ratings": 0,
            "average_rating": 0.0
        }
        
        total_rating_sum = 0
        rated_wrestlers = 0
        
        # Handle both old dictionary format and new list format
        if isinstance(wrestlers, dict):
            wrestlers_to_iterate = wrestlers.items()
        else:
            wrestlers_to_iterate = [(w.get('id', i), w) for i, w in enumerate(wrestlers)]
        
        for wrestler_id, wrestler in wrestlers_to_iterate:
            # Handle both old and new data structures
            if 'parsed_data' in wrestler:
                # Old format
                parsed_data = wrestler.get('parsed_data', {})
                profile = parsed_data.get('profile', {})
                promotion = profile.get('promotion', 'Unknown')
                style = profile.get('wrestling_style', 'Unknown')
                rating = profile.get('average_rating')
            else:
                # New format - direct fields
                promotion = wrestler.get('promotion', 'Unknown')
                style = wrestler.get('wrestling_style', 'Unknown')
                rating = wrestler.get('averageRating') or wrestler.get('average_rating')
            
            # Count by promotion
            if promotion not in stats['promotions']:
                stats['promotions'][promotion] = 0
            stats['promotions'][promotion] += 1
            
            # Count by wrestling style
            if style not in stats['wrestling_styles']:
                stats['wrestling_styles'][style] = 0
            stats['wrestling_styles'][style] += 1
            
            # Calculate rating statistics
            if rating:
                try:
                    rating_float = float(rating)
                    total_rating_sum += rating_float
                    rated_wrestlers += 1
                except ValueError:
                    continue
        
        if rated_wrestlers > 0:
            stats['total_ratings'] = rated_wrestlers
            stats['average_rating'] = round(total_rating_sum / rated_wrestlers, 2)
        
        return stats

# Initialize the API
wrestling_api = WrestlingAPI()

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database_loaded": bool(wrestling_api.database)
    })

@app.route('/api/reload', methods=['POST'])
def reload_database():
    """Reload the wrestling database."""
    return jsonify(wrestling_api.reload_database())

@app.route('/api/wrestlers', methods=['GET'])
def get_wrestlers():
    """Get all wrestlers with optional pagination."""
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', 0, type=int)
    
    return jsonify(wrestling_api.get_all_wrestlers(limit=limit, offset=offset))

@app.route('/api/wrestlers/<wrestler_id>', methods=['GET'])
def get_wrestler(wrestler_id):
    """Get a specific wrestler by ID."""
    return jsonify(wrestling_api.get_wrestler_by_id(wrestler_id))

@app.route('/api/search', methods=['GET'])
def search_wrestlers():
    """Search wrestlers by query."""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)
    
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    return jsonify(wrestling_api.search_wrestlers(query, limit=limit))

@app.route('/api/promotions/<promotion>', methods=['GET'])
def get_wrestlers_by_promotion(promotion):
    """Get wrestlers by promotion."""
    return jsonify(wrestling_api.get_wrestlers_by_promotion(promotion))

@app.route('/api/top-rated', methods=['GET'])
def get_top_rated():
    """Get top rated wrestlers."""
    limit = request.args.get('limit', 10, type=int)
    return jsonify(wrestling_api.get_top_rated_wrestlers(limit=limit))

@app.route('/api/stats', methods=['GET'])
def get_database_stats():
    """Get database statistics."""
    return jsonify(wrestling_api.get_database_stats())

@app.route('/api/wrestlers/<wrestler_id>/stats', methods=['GET'])
def get_wrestler_stats(wrestler_id):
    """Get structured statistics for a specific wrestler."""
    wrestler = wrestling_api.get_wrestler_by_id(wrestler_id)
    
    if 'error' in wrestler:
        return jsonify(wrestler), 404
    
    # Extract just the parsed data for frontend consumption
    parsed_data = wrestler.get('parsed_data', {})
    
    return jsonify({
        "wrestler_id": wrestler_id,
        "name": wrestler.get('name', 'Unknown'),
        "profile": parsed_data.get('profile', {}),
        "statistics": parsed_data.get('statistics', {}),
        "last_updated": wrestler.get('scraped_at')
    })

if __name__ == '__main__':
    print("🚀 Starting Wrestling API Server")
    print("=" * 40)
    print("Available endpoints:")
    print("  GET  /api/health              - Health check")
    print("  POST /api/reload              - Reload database")
    print("  GET  /api/wrestlers           - Get all wrestlers")
    print("  GET  /api/wrestlers/<id>      - Get specific wrestler")
    print("  GET  /api/search?q=<query>    - Search wrestlers")
    print("  GET  /api/promotions/<name>   - Get wrestlers by promotion")
    print("  GET  /api/top-rated           - Get top rated wrestlers")
    print("  GET  /api/stats               - Get database statistics")
    print("  GET  /api/wrestlers/<id>/stats - Get wrestler statistics")
    print("=" * 40)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
