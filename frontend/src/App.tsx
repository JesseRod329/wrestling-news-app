import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Homepage from './pages/Homepage';
import Home from './pages/Home';
import SearchResults from './pages/SearchResults';
import WrestlerProfile from './pages/WrestlerProfile';
import AdvancedSearch from './pages/AdvancedSearch';
import StatisticsDashboard from './pages/StatisticsDashboard';
import News from './pages/News';
import Favorites from './pages/Favorites';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';
import { ToastProvider } from './contexts/ToastContext';

function App() {
  return (
    <ToastProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Homepage />} />
            <Route path="/home" element={<Home />} />
            <Route path="/search" element={<SearchResults />} />
            <Route path="/wrestlers/:id" element={<WrestlerProfile />} />
            <Route path="/advanced-search" element={<AdvancedSearch />} />
            <Route path="/statistics" element={<StatisticsDashboard />} />
            <Route path="/news" element={<News />} />
            <Route path="/favorites" element={<Favorites />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Layout>
      </Router>
    </ToastProvider>
  );
}

export default App;
