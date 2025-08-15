# RingStats 🥊

A modern web application for wrestling statistics, featuring clean UI and comprehensive wrestler profiles with side-by-side comparisons.

## 🎯 Features

- **Side-by-side wrestler comparison** with interactive cards
- **Detailed wrestler profiles** with complete statistics
- **Search functionality** with real-time results
- **Responsive design** for mobile, tablet, and desktop
- **Momentum scoring system** out of 15 points
- **Recent match tracking** with win/loss/draw badges
- **Career statistics** and championship history

## 🚀 Tech Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Inter font** for clean typography

### Backend
- **Node.js** with Express.js
- **CORS** enabled for cross-origin requests
- **RESTful API** design
- **Environment-based configuration**

## 📁 Project Structure

```
prostats/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   │   ├── Navbar.tsx
│   │   │   └── WrestlerCard.tsx
│   │   ├── pages/          # Page components
│   │   │   ├── Homepage.tsx
│   │   │   └── WrestlerProfile.tsx
│   │   ├── types/          # TypeScript interfaces
│   │   │   └── index.ts
│   │   ├── data/           # Sample data
│   │   │   └── sampleData.ts
│   │   └── App.tsx
│   ├── public/
│   └── package.json
└── backend/                 # Node.js backend API
    ├── routes/             # API route handlers
    │   └── wrestlers.js
    ├── data/              # Data storage
    │   └── wrestlers.js
    ├── server.js          # Main server file
    ├── .env              # Environment variables
    └── package.json
```

## 🛠 Installation & Setup

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### 1. Clone the Repository
```bash
git clone <repository-url>
cd prostats
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
npm install
npm run dev
```
The backend API will run on http://localhost:5000

## 🔌 API Endpoints

### Wrestlers
- `GET /api/wrestlers` - Get all wrestlers (supports ?search and ?limit query params)
- `GET /api/wrestlers/:id` - Get specific wrestler by ID
- `GET /api/wrestlers/:id/matches` - Get wrestler's match history
- `GET /api/wrestlers/:id/stats` - Get wrestler's career statistics

### Health Check
- `GET /api/health` - API health status

### Example API Response
```json
{
  "success": true,
  "count": 3,
  "data": [
    {
      "id": "john-cena",
      "name": "John Cena",
      "nickname": "The Cenation Leader",
      "momentumScore": 11,
      "careerStats": {
        "totalMatches": 2847,
        "wins": 1892,
        "losses": 832,
        "draws": 123,
        "winPercentage": 66.4
      }
    }
  ]
}
```

## 🎨 Design Features

- **Apple-inspired UI** with clean typography
- **Frosted glass effects** on navigation
- **Hover animations** and smooth transitions
- **Color-coded momentum scoring**:
  - 🟢 Green (12-15): High momentum
  - 🟡 Yellow (8-11): Medium momentum  
  - 🔴 Red (0-7): Low momentum
- **Responsive grid layouts**
- **Interactive cards** with hover effects

## 🔧 Development

### Available Scripts

**Frontend:**
- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests

**Backend:**
- `npm run dev` - Start with nodemon (auto-restart)
- `npm start` - Start production server

### Environment Variables
Create a `.env` file in the backend directory:
```env
PORT=5000
NODE_ENV=development
CORS_ORIGIN=http://localhost:3000
```

## 📋 Future Features

### Planned Enhancements
- [ ] Database integration (PostgreSQL)
- [ ] User authentication and profiles
- [ ] Favorite wrestler bookmarking
- [ ] Dark/Light mode toggle
- [ ] Advanced filtering and sorting
- [ ] Match rating system
- [ ] Win-loss streak tracking
- [ ] PPV-only match filtering
- [ ] Hot streak indicators
- [ ] Admin panel for data management

### Potential Integrations
- [ ] Real data scraping from cagematch.net
- [ ] Social media integration
- [ ] Push notifications for match results
- [ ] Fantasy wrestling leagues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the ISC License.

## 🙏 Acknowledgments

- Wrestling data inspired by WWE and AEW
- Images from Unsplash
- Design inspiration from ESPN and Apple Human Interface Guidelines 