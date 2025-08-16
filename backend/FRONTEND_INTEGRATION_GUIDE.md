# 🏆 Wrestling Database Frontend Integration Guide

Your frontend team can now access comprehensive wrestling data through our API! This guide shows you how to integrate with the wrestling database.

## 🚀 Quick Start

### 1. **Start the API Server**
```bash
cd backend
python wrestling_api.py
```

The API will run on `http://localhost:5001`

### 2. **Test the API**
```bash
curl http://localhost:5001/api/health
```

## 📊 Available API Endpoints

### **Core Endpoints**

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/api/health` | GET | Health check | `GET /api/health` |
| `/api/wrestlers` | GET | Get all wrestlers | `GET /api/wrestlers?limit=10&offset=0` |
| `/api/wrestlers/{id}` | GET | Get specific wrestler | `GET /api/wrestlers/3686` |
| `/api/search` | GET | Search wrestlers | `GET /api/search?q=John Cena&limit=5` |
| `/api/promotions/{name}` | GET | Get wrestlers by promotion | `GET /api/promotions/WWE` |
| `/api/top-rated` | GET | Get top rated wrestlers | `GET /api/top-rated?limit=10` |
| `/api/stats` | GET | Get database statistics | `GET /api/stats` |
| `/api/wrestlers/{id}/stats` | GET | Get wrestler statistics | `GET /api/wrestlers/3686/stats` |

## 🔍 Data Structure Examples

### **Wrestler Profile Data**
```json
{
  "wrestler_id": "3686",
  "name": "Cody Rhodes",
  "profile_url": "https://www.cagematch.net/?id=2&nr=3686",
  "stats_url": "https://www.cagematch.net/?id=2&nr=3686&view=matches",
  "parsed_data": {
    "profile": {
      "age": "40",
      "height": "6' 1\" (185 cm)",
      "weight": "220 lbs (100 kg)",
      "birthplace": "Charlotte, North Carolina, USA",
      "gender": "male",
      "promotion": "World Wrestling Entertainment",
      "brand": "SmackDown",
      "career_start": "13.05.2006",
      "experience": "19 years",
      "wrestling_style": "Allrounder",
      "trainers": ["Al Snow", "Bruno Sassi", "Dusty Rhodes", "Ray Lloyd"],
      "nicknames": ["Dashing", "The American Nightmare", "The Grandson Of A Plumber"],
      "signature_moves": ["Cross Rhodes", "Beautiful Disaster", "Cody Cutter", "DDT"],
      "alter_egos": ["Cody Rhodes", "Cody", "Cody Runnels", "Fuego II", "Stardust"],
      "roles": ["Singles Wrestler", "Tag Team Wrestler", "Promoter", "Referee"],
      "average_rating": "7.86",
      "rating_votes": "1587",
      "total_votes": "1587",
      "total_comments": "561",
      "yearly_ratings": {
        "2025": {"rating": "8.58", "votes": "195"},
        "2024": {"rating": "8.52", "votes": "243"},
        "2023": {"rating": "8.31", "votes": "157"}
      },
      "social_media": {
        "twitter": "CodyRhodes",
        "instagram": "americannightmarecody",
        "tiktok": "americannightmarecody",
        "youtube": "nightmarefamily"
      }
    },
    "statistics": {
      "total_matches": null,
      "wins": null,
      "losses": null,
      "draws": null
    }
  },
  "scraped_at": "2025-08-14T16:35:33.604758"
}
```

### **Database Statistics**
```json
{
  "total_wrestlers": 25,
  "database_file": "wrestling_database_20250814_163533.json",
  "last_updated": "2025-08-14T16:35:33.604758",
  "promotions": {
    "World Wrestling Entertainment": 15,
    "All Elite Wrestling": 8,
    "New Japan Pro-Wrestling": 2
  },
  "wrestling_styles": {
    "Allrounder": 12,
    "High Flyer": 8,
    "Technical": 5
  },
  "total_ratings": 20,
  "average_rating": 7.85
}
```

## 💻 Frontend Integration Examples

### **React/TypeScript Example**

```typescript
// types/wrestler.ts
export interface WrestlerProfile {
  age: string;
  height: string;
  weight: string;
  birthplace: string;
  gender: string;
  promotion: string;
  brand: string;
  career_start: string;
  experience: string;
  wrestling_style: string;
  trainers: string[];
  nicknames: string[];
  signature_moves: string[];
  alter_egos: string[];
  roles: string[];
  average_rating: string;
  rating_votes: string;
  total_votes: string;
  total_comments: string;
  yearly_ratings: Record<string, { rating: string; votes: string }>;
  social_media: Record<string, string>;
}

export interface Wrestler {
  wrestler_id: string;
  name: string;
  profile_url: string;
  stats_url: string;
  parsed_data: {
    profile: WrestlerProfile;
    statistics: any;
  };
  scraped_at: string;
}

// services/wrestlingApi.ts
const API_BASE = 'http://localhost:5001/api';

export class WrestlingAPI {
  static async getAllWrestlers(limit?: number, offset?: number): Promise<Wrestler[]> {
    const params = new URLSearchParams();
    if (limit) params.append('limit', limit.toString());
    if (offset) params.append('offset', offset.toString());
    
    const response = await fetch(`${API_BASE}/wrestlers?${params}`);
    const data = await response.json();
    return data.wrestlers;
  }

  static async getWrestlerById(id: string): Promise<Wrestler> {
    const response = await fetch(`${API_BASE}/wrestlers/${id}`);
    return response.json();
  }

  static async searchWrestlers(query: string, limit: number = 10): Promise<Wrestler[]> {
    const response = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}&limit=${limit}`);
    const data = await response.json();
    return data.results;
  }

  static async getTopRatedWrestlers(limit: number = 10): Promise<any[]> {
    const response = await fetch(`${API_BASE}/top-rated?limit=${limit}`);
    const data = await response.json();
    return data.top_rated_wrestlers;
  }

  static async getWrestlersByPromotion(promotion: string): Promise<Wrestler[]> {
    const response = await fetch(`${API_BASE}/promotions/${encodeURIComponent(promotion)}`);
    const data = await response.json();
    return data.wrestlers;
  }

  static async getDatabaseStats(): Promise<any> {
    const response = await fetch(`${API_BASE}/stats`);
    return response.json();
  }
}

// components/WrestlerCard.tsx
import React from 'react';
import { Wrestler } from '../types/wrestler';

interface WrestlerCardProps {
  wrestler: Wrestler;
  onClick?: () => void;
}

export const WrestlerCard: React.FC<WrestlerCardProps> = ({ wrestler, onClick }) => {
  const profile = wrestler.parsed_data.profile;
  
  return (
    <div className="wrestler-card" onClick={onClick}>
      <h3>{wrestler.name}</h3>
      <div className="wrestler-info">
        <p><strong>Age:</strong> {profile.age}</p>
        <p><strong>Height:</strong> {profile.height}</p>
        <p><strong>Weight:</strong> {profile.weight}</p>
        <p><strong>Promotion:</strong> {profile.promotion}</p>
        <p><strong>Brand:</strong> {profile.brand}</p>
        <p><strong>Rating:</strong> {profile.average_rating}/10 ({profile.rating_votes} votes)</p>
      </div>
      <div className="wrestler-tags">
        {profile.nicknames.slice(0, 3).map((nickname, index) => (
          <span key={index} className="tag">{nickname}</span>
        ))}
      </div>
    </div>
  );
};

// components/WrestlerStats.tsx
import React from 'react';
import { Wrestler } from '../types/wrestler';

interface WrestlerStatsProps {
  wrestler: Wrestler;
}

export const WrestlerStats: React.FC<WrestlerStatsProps> = ({ wrestler }) => {
  const profile = wrestler.parsed_data.profile;
  
  return (
    <div className="wrestler-stats">
      <h2>{wrestler.name} - Statistics</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Basic Info</h3>
          <p><strong>Age:</strong> {profile.age}</p>
          <p><strong>Height:</strong> {profile.height}</p>
          <p><strong>Weight:</strong> {profile.weight}</p>
          <p><strong>Birthplace:</strong> {profile.birthplace}</p>
        </div>
        
        <div className="stat-card">
          <h3>Career</h3>
          <p><strong>Started:</strong> {profile.career_start}</p>
          <p><strong>Experience:</strong> {profile.experience}</p>
          <p><strong>Style:</strong> {profile.wrestling_style}</p>
          <p><strong>Promotion:</strong> {profile.promotion}</p>
        </div>
        
        <div className="stat-card">
          <h3>Ratings</h3>
          <p><strong>Overall:</strong> {profile.average_rating}/10</p>
          <p><strong>Total Votes:</strong> {profile.total_votes}</p>
          <p><strong>Comments:</strong> {profile.total_comments}</p>
        </div>
      </div>
      
      <div className="signature-moves">
        <h3>Signature Moves</h3>
        <div className="moves-list">
          {profile.signature_moves.map((move, index) => (
            <span key={index} className="move-tag">{move}</span>
          ))}
        </div>
      </div>
      
      <div className="yearly-ratings">
        <h3>Yearly Ratings</h3>
        <div className="ratings-chart">
          {Object.entries(profile.yearly_ratings).map(([year, data]) => (
            <div key={year} className="rating-bar">
              <span className="year">{year}</span>
              <div className="bar" style={{ width: `${(parseFloat(data.rating) / 10) * 100}%` }}>
                {data.rating}
              </div>
              <span className="votes">({data.votes} votes)</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
```

## 🎯 Key Features for Frontend

### **1. Wrestler Search & Discovery**
- **Search by name**: Find wrestlers quickly
- **Filter by promotion**: WWE, AEW, NJPW, etc.
- **Top rated wrestlers**: Show the best performers
- **Pagination**: Handle large datasets

### **2. Rich Wrestler Profiles**
- **Complete statistics**: Age, height, weight, experience
- **Career information**: Start date, promotions, brands
- **Signature moves**: Highlight unique techniques
- **Ratings & reviews**: Community feedback
- **Social media**: Direct links to wrestler accounts

### **3. Data Visualization Opportunities**
- **Rating charts**: Yearly performance trends
- **Promotion breakdowns**: Wrestler distribution
- **Style analysis**: Wrestling technique categories
- **Career timelines**: Experience progression

### **4. Real-time Updates**
- **Database reload**: Get fresh data
- **Health monitoring**: API status checks
- **Error handling**: Graceful fallbacks

## 🔧 Development Workflow

### **1. Start Development**
```bash
# Terminal 1: Start the API server
cd backend
python wrestling_api.py

# Terminal 2: Start your frontend
cd frontend
npm start
```

### **2. Test API Endpoints**
```bash
# Test health
curl http://localhost:5001/api/health

# Test wrestler search
curl "http://localhost:5001/api/search?q=John%20Cena"

# Test top rated
curl http://localhost:5001/api/top-rated?limit=5
```

### **3. Build Features**
- Start with basic wrestler listing
- Add search functionality
- Implement detailed profiles
- Add statistics and charts
- Build promotion filters

## 📱 Mobile Considerations

- **Responsive design**: Wrestler cards work on all screen sizes
- **Touch-friendly**: Large tap targets for mobile users
- **Performance**: Lazy load images and data
- **Offline support**: Cache frequently accessed data

## 🚀 Next Steps

1. **Start the API server** and test the endpoints
2. **Build basic wrestler listing** with search
3. **Create detailed wrestler profile pages**
4. **Add statistics and visualization components**
5. **Implement promotion and style filtering**
6. **Add favorites and user preferences**

## 📞 Support

If you need help with:
- **API integration**: Check the endpoint documentation above
- **Data structure**: Review the JSON examples
- **Performance**: Use pagination and limit parameters
- **New features**: The API is extensible for additional endpoints

The wrestling database is now ready to power your frontend application! 🏆
