import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import Layout from './components/Layout';
import Homepage from './pages/Homepage';
import Home from './pages/Home';
import SearchResults from './pages/SearchResults';
import AdvancedSearch from './pages/AdvancedSearch';
import StatisticsDashboard from './pages/StatisticsDashboard';
import News from './pages/News';
import WrestlerProfile from './pages/WrestlerProfile';
import WrestlerStats from './pages/WrestlerStats';
import Favorites from './pages/Favorites';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/home" element={<Home />} />
          <Route path="/search" element={<SearchResults />} />
          <Route path="/advanced-search" element={<AdvancedSearch />} />
          <Route path="/statistics" element={<StatisticsDashboard />} />
          <Route path="/news" element={<News />} />
          <Route path="/wrestlers/:id" element={<WrestlerProfile />} />
          <Route path="/wrestlers/:id/stats" element={<WrestlerStats />} />
          <Route path="/favorites" element={<Favorites />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Layout>
    </Router>
  </React.StrictMode>
); 