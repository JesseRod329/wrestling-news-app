# 🏆 Ultimate Wrestling Platform - Integration Guide

## Overview
This guide explains how to integrate your two wrestling applications:
1. **ProStats** - Wrestling statistics and wrestler profiles
2. **NewsSite** - Wrestling news aggregation and RSS feeds

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements_integrated.txt
```

### 2. Start the Integrated Backend
```bash
cd backend
python run_integrated.py
```

### 3. Start the Frontend
```bash
cd frontend
npm start
```

## 🏗️ Architecture

### Backend Integration
- **FastAPI** as the main framework (replaces Flask)
- **Unified API** with prefixes:
  - `/stats/*` - Wrestling statistics endpoints
  - `/news/*` - News aggregation endpoints
- **Single Database** for both applications
- **Unified CORS** and middleware

### Frontend Integration
- **React + TypeScript** application
- **Unified Navigation** with news section
- **Shared Components** and styling
- **News Feed** integrated into homepage

## 📁 File Structure

```
prostats/
├── backend/
│   ├── integrated_app.py          # Main FastAPI application
│   ├── run_integrated.py          # Startup script
│   ├── config_integrated.py       # Configuration
│   ├── requirements_integrated.txt # Combined dependencies
│   └── wrestling_api.py           # Stats functionality
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── NewsFeed.tsx       # News display component
│   │   │   └── EnhancedImageDisplay.tsx # Image handling
│   │   ├── pages/
│   │   │   ├── News.tsx           # News page
│   │   │   └── Homepage.tsx       # Updated homepage
│   │   └── index.tsx              # Updated routing
│   └── package.json
└── newsite/                       # Original news application
    ├── app/                       # News backend modules
    └── static/                    # News frontend
```

## 🔌 API Endpoints

### Stats Endpoints (from ProStats)
- `GET /stats/wrestlers` - All wrestlers
- `GET /stats/wrestlers/{id}` - Specific wrestler
- `GET /stats/search?q={query}` - Search wrestlers
- `GET /stats/top-rated` - Top-rated wrestlers
- `GET /stats/database-stats` - Database statistics

### News Endpoints (from NewsSite)
- `GET /news/articles` - All news articles
- `GET /news/articles/{id}` - Specific article
- `POST /news/vote` - Vote on articles
- `GET /news/sources` - News sources
- `POST /news/admin/ingest` - Trigger news ingestion

### Health & Documentation
- `GET /health` - Application health
- `/docs` - FastAPI documentation (Swagger UI)

## 🎨 Frontend Features

### Navigation
- **Home** - Wrestling stats + news preview
- **News** - Full wrestling news feed
- **Search** - Wrestler search functionality
- **Favorites** - Saved wrestlers
- **Settings** - Application configuration

### News Integration
- **News Preview** on homepage (3 latest articles)
- **Full News Page** with filtering and voting
- **Credibility Tags** (High/Medium/Low)
- **Source Attribution** for all articles
- **Voting System** (upvote/downvote)

### Enhanced Image Handling
- **Smart Positioning** for wrestler photos
- **Fallback Images** when photos fail to load
- **Responsive Design** for all screen sizes
- **Loading States** and error handling

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
INTEGRATED_ENVIRONMENT=dev
INTEGRATED_DATABASE_URL=sqlite:///./integrated_wrestling.db
INTEGRATED_JWT_SECRET_KEY=your-secret-key-change-in-production
INTEGRATED_API_HOST=0.0.0.0
INTEGRATED_API_PORT=8000
```

### Database Setup
The integrated application will automatically:
- Create SQLite database for development
- Seed news sources
- Start news polling (every 15 minutes)
- Handle database migrations

## 🔄 Data Flow

### News Ingestion
1. **RSS Feeds** are polled every 15 minutes
2. **Articles** are fetched and processed
3. **Credibility scores** are calculated
4. **Database** is updated with new content

### Stats Management
1. **Wrestler data** is scraped from Cagematch
2. **Images** are fetched from multiple sources
3. **Statistics** are calculated and stored
4. **API** serves data to frontend

## 🧪 Testing

### Backend Testing
```bash
cd backend
python run_integrated.py
# Visit http://localhost:8000/docs for API testing
```

### Frontend Testing
```bash
cd frontend
npm start
# Visit http://localhost:3000 for frontend testing
```

### API Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test stats endpoint
curl http://localhost:8000/stats/wrestlers

# Test news endpoint
curl http://localhost:8000/news/articles
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Make sure newsite is accessible
# Check Python path in run_integrated.py
```

#### 2. Database Connection
```bash
# Verify database file permissions
# Check database URL in config
```

#### 3. News Not Loading
```bash
# Check news sources are seeded
# Verify RSS feeds are accessible
# Check news poller is running
```

#### 4. Images Not Displaying
```bash
# Verify image URLs in database
# Check CORS settings
# Test image endpoints directly
```

### Debug Mode
Enable debug logging by setting:
```env
INTEGRATED_ENVIRONMENT=dev
```

## 🔮 Future Enhancements

### Planned Features
- **User Authentication** for personalized news
- **News Categories** (WWE, AEW, NJPW, etc.)
- **Push Notifications** for breaking news
- **Advanced Analytics** combining stats and news
- **Mobile App** using React Native

### Scalability
- **PostgreSQL** for production
- **Redis** for caching
- **Elasticsearch** for advanced search
- **Docker** containerization
- **Kubernetes** orchestration

## 📚 Additional Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)

### API References
- [Wrestling Observer RSS](https://www.f4wonline.com/rss.xml)
- [PWInsider RSS](http://www.pwinsider.com/rss.php)
- [Cagematch.net](https://www.cagematch.net/)

## 🤝 Contributing

### Development Workflow
1. **Feature Branch** from main
2. **Code Review** and testing
3. **Integration Testing** with both apps
4. **Documentation** updates
5. **Merge** to main branch

### Code Standards
- **TypeScript** for frontend
- **Python** for backend
- **PEP 8** for Python code
- **ESLint** for TypeScript
- **Prettier** for code formatting

---

## 🎯 Getting Started Checklist

- [ ] Install integrated dependencies
- [ ] Configure environment variables
- [ ] Start integrated backend
- [ ] Start frontend application
- [ ] Test news functionality
- [ ] Test stats functionality
- [ ] Verify image display
- [ ] Check API documentation
- [ ] Test navigation between sections

**Congratulations! You now have a unified wrestling platform that combines the best of both applications! 🏆📰📊**
