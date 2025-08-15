# ProStats Wrestling Platform 🥊📰

A comprehensive wrestling platform combining **wrestling statistics** and **wrestling news** in one unified application.

## 🎯 Features

### Wrestling Statistics
- **Side-by-side wrestler comparison** with interactive cards
- **Detailed wrestler profiles** with complete statistics from Cagematch.net
- **Search functionality** with real-time results
- **Accurate database** with 34+ top wrestlers and real data
- **Momentum scoring system** out of 15 points
- **Recent match tracking** with win/loss/draw badges
- **Career statistics** and championship history

### Wrestling News
- **Real-time wrestling news** aggregation
- **Credibility scoring** system
- **User voting** on articles
- **RSS feed integration**
- **Admin panel** for content management

## 🚀 Tech Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Inter font** for clean typography
- **Glass morphism** design elements

### Backend
- **Python Flask** for wrestling statistics API
- **Python FastAPI** for wrestling news API
- **SQLAlchemy** with SQLite/PostgreSQL support
- **JWT authentication**
- **CORS** enabled for cross-origin requests
- **RESTful API** design

## 📁 Project Structure

```
prostats/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── types/          # TypeScript interfaces
│   │   ├── services/       # API services
│   │   └── hooks/          # Custom React hooks
│   ├── public/
│   └── package.json
├── backend/                 # Python backend APIs
│   ├── wrestling_api.py    # Flask API for wrestler stats
│   ├── app/                # FastAPI news application
│   ├── data/               # Wrestling database files
│   └── requirements.txt
└── README.md
```

## 🛠 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js (v16 or higher)
- npm or yarn

### 1. Clone the Repository
```bash
git clone https://github.com/JesseRod329/wrestling-news-app.git
cd wrestling-news-app
```

### 2. Setup Frontend
```bash
cd frontend
npm install
npm start
```
The frontend will run on http://localhost:3000

### 3. Setup Backend
```bash
cd backend
pip install -r requirements.txt

# Start wrestling statistics API
python wrestling_api.py

# Start wrestling news API (in another terminal)
cd app
uvicorn main:app --reload --port 8000
```

## 🔌 API Endpoints

### Wrestling Statistics API (Flask - Port 5001)
- `GET /api/health` - API health status
- `GET /api/wrestlers` - Get all wrestlers
- `GET /api/wrestlers/:id` - Get specific wrestler by ID
- `GET /api/stats` - Get database statistics

### Wrestling News API (FastAPI - Port 8000)
- `GET /docs` - Interactive API documentation
- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `GET /articles` - Get news articles
- `POST /vote` - Vote on articles
- `POST /admin/ingest` - Trigger news ingestion

## 🎨 Design Features

- **Modern UI** with glass morphism effects
- **Responsive design** for all devices
- **Interactive wrestler cards** with hover animations
- **News feed** with credibility scoring
- **Color-coded momentum scoring** system
- **Smooth transitions** and animations

## 🔧 Development

### Available Scripts

**Frontend:**
- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests

**Backend:**
- `python wrestling_api.py` - Start wrestling stats API
- `uvicorn app.main:app --reload` - Start news API with auto-reload

### Environment Variables
Create a `.env` file in the backend directory:
```env
APP_DATABASE_URL=sqlite:///./dev.db
APP_JWT_SECRET_KEY=your-secret-key
APP_ENVIRONMENT=development
```

## 📊 Database

### Wrestling Statistics
- **34+ top wrestlers** with accurate data from Cagematch.net
- **Real ages, promotions, and career information**
- **Social media links and ratings**
- **Comprehensive wrestling statistics**

### News Database
- **SQLite** for development
- **PostgreSQL** ready for production
- **User authentication and voting system**
- **Credibility scoring algorithm**

## 🚀 Quick Start

1. **Start the wrestling statistics API:**
   ```bash
   cd backend
   python wrestling_api.py
   ```

2. **Start the wrestling news API:**
   ```bash
   cd backend/app
   uvicorn main:app --reload --port 8000
   ```

3. **Start the React frontend:**
   ```bash
   cd frontend
   npm start
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Wrestling Stats API: http://localhost:5001
   - News API Docs: http://localhost:8000/docs

## 📋 Future Features

- [ ] User authentication for wrestling stats
- [ ] Advanced wrestler filtering and sorting
- [ ] Match prediction system
- [ ] Fantasy wrestling leagues
- [ ] Real-time match updates
- [ ] Social media integration
- [ ] Mobile app development

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the ISC License.

## 🙏 Acknowledgments

- Wrestling data from Cagematch.net
- Design inspiration from ESPN and Apple Human Interface Guidelines
- News aggregation and credibility scoring algorithms
