import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import WrestlerCard from '../components/WrestlerCard';
import NewsFeed from '../components/NewsFeed';
import LoadingSpinner from '../components/LoadingSpinner';
import apiService from '../services/api';
import { Wrestler, DatabaseStats } from '../types';

const Homepage: React.FC = () => {
  const [topWrestlers, setTopWrestlers] = useState<Wrestler[]>([]);
  const [databaseStats, setDatabaseStats] = useState<DatabaseStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchSuggestions] = useState([
    'John Cena', 'Roman Reigns', 'Brock Lesnar', 'WWE', 'AEW', 'Championship',
    'Tag Team', 'Women\'s Division', 'Independent Wrestling', 'NJPW'
  ]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const [wrestlersData, statsData] = await Promise.all([
          apiService.getWrestlers(),
          apiService.getDatabaseStats()
        ]);
        
        setTopWrestlers(wrestlersData.slice(0, 6)); // Take first 6 wrestlers
        setDatabaseStats(statsData);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Failed to load data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleSearch = (query: string) => {
    if (query.trim()) {
      window.location.href = `/search?q=${encodeURIComponent(query)}`;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="flex items-center justify-center min-h-screen">
          <LoadingSpinner 
            size="xl" 
            color="white" 
            text="Loading Wrestling Universe..." 
          />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center max-w-md mx-auto p-6">
            <div className="text-red-500 text-6xl mb-4">⚠️</div>
            <h2 className="text-white text-xl font-bold mb-4">Error Loading Data</h2>
            <p className="text-gray-300 mb-6">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors duration-200"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Hero Section - News Focused */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-purple-900/80 to-blue-900/80"></div>
        <div className="relative z-10 px-4 py-16 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight text-white sm:text-6xl animate-fade-in-up">
              <span className="block">Wrestling</span>
                <span className="block text-purple-400">News & Stats</span>
            </h1>
            <p className="mt-6 text-xl text-gray-300 max-w-3xl mx-auto animate-fade-in-up animation-delay-200">
              Stay updated with the latest wrestling news, rumors, and comprehensive statistics from across the industry.
            </p>
            
            {/* Quick Search Bar */}
            <div className="mt-8 max-w-2xl mx-auto animate-fade-in-up animation-delay-400">
              <SearchBar
                onSearch={handleSearch}
                placeholder="Search wrestlers, promotions, or championships..."
                suggestions={searchSuggestions}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="px-4 py-12 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          
          {/* News Section - Primary Focus */}
          <section className="mb-16 animate-fade-in-up animation-delay-600">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h2 className="text-3xl font-bold text-white mb-2">Latest Wrestling News</h2>
                <p className="text-gray-400">Breaking stories, rumors, and updates from the wrestling world</p>
              </div>
              <Link
                to="/news"
                className="group inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 transition-all duration-200 hover:scale-105"
              >
                View All News
                <svg className="ml-2 -mr-1 w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </Link>
            </div>
            
            {/* News Feed - Enhanced Display */}
            <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10 hover:bg-white/10 transition-all duration-300">
              <NewsFeed limit={6} showFilters={false} />
            </div>
          </section>

          {/* Wrestling Stats Section - Secondary Feature */}
          <section className="mb-16 animate-fade-in-up animation-delay-800">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h2 className="text-3xl font-bold text-white mb-2">Wrestling Statistics</h2>
                <p className="text-gray-400">Explore comprehensive stats and rankings</p>
              </div>
              <Link
                to="/statistics"
                className="group inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-all duration-200 hover:scale-105"
              >
                View Full Stats
                <svg className="ml-2 -mr-1 w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </Link>
            </div>
            
            {/* Stats Overview Cards */}
            {databaseStats && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div className="group bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:bg-white/10 hover:border-purple-500/50 transition-all duration-300 hover:-translate-y-1">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center group-hover:bg-purple-600 transition-colors">
                        <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-400">Total Wrestlers</p>
                      <p className="text-2xl font-bold text-white">{databaseStats.total_wrestlers}</p>
                    </div>
                  </div>
                </div>

                <div className="group bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:bg-white/10 hover:border-blue-500/50 transition-all duration-300 hover:-translate-y-1">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center group-hover:bg-blue-600 transition-colors">
                        <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                        </svg>
                      </div>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-400">Database Source</p>
                      <p className="text-2xl font-bold text-white">{databaseStats.source || 'Unknown'}</p>
                    </div>
                  </div>
                </div>

                <div className="group bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:bg-white/10 hover:border-green-500/50 transition-all duration-300 hover:-translate-y-1">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center group-hover:bg-green-600 transition-colors">
                        <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
                        </svg>
                      </div>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-400">Scraper Version</p>
                      <p className="text-2xl font-bold text-white">{databaseStats.scraper_version || 'N/A'}</p>
                    </div>
                  </div>
                </div>

                <div className="group bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:bg-white/10 hover:border-yellow-500/50 transition-all duration-300 hover:-translate-y-1">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-yellow-500 rounded-lg flex items-center justify-center group-hover:bg-yellow-600 transition-colors">
                        <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                        </svg>
                      </div>
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-400">Last Updated</p>
                      <p className="text-2xl font-bold text-white">
                        {databaseStats.scraped_at ? new Date(databaseStats.scraped_at).toLocaleDateString() : 'Unknown'}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Top Wrestlers Preview */}
            <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10 hover:bg-white/10 transition-all duration-300">
              <h3 className="text-xl font-semibold text-white mb-6">Featured Wrestlers</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {topWrestlers.slice(0, 6).map((wrestler, index) => (
                  <div 
                    key={wrestler.id} 
                    className="animate-fade-in-up"
                    style={{ animationDelay: `${(index + 1) * 100}ms` }}
                  >
                    <WrestlerCard wrestler={wrestler} />
                  </div>
                ))}
              </div>
              <div className="text-center mt-8">
                <Link
                  to="/statistics"
                  className="group inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-all duration-200 hover:scale-105"
                >
                  View All Wrestlers
                  <svg className="ml-2 -mr-1 w-5 h-5 group-hover:translate-x-1 transition-transform duration-200" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </Link>
              </div>
            </div>
          </section>

          {/* Quick Actions */}
          <section className="mb-16 animate-fade-in-up animation-delay-1000">
            <h2 className="text-3xl font-bold text-white mb-8">Quick Actions</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Link
                to="/news"
                className="group bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:bg-white/10 hover:border-purple-500/50 transition-all duration-300 hover:-translate-y-1"
              >
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center group-hover:bg-purple-600 transition-colors">
                      <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M2 5a2 2 0 012-2h8a2 2 0 012 2v10a2 2 0 002 2H4a2 2 0 01-2-2V5zm3 1h6v4H5V6zm6 6H5v2h6v-2z" clipRule="evenodd" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-white group-hover:text-purple-400 transition-colors">Wrestling News</h3>
                    <p className="text-gray-400">Latest updates and rumors</p>
                  </div>
                </div>
              </Link>

              <Link
                to="/advanced-search"
                className="group bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:bg-white/10 hover:border-blue-500/50 transition-all duration-300 hover:-translate-y-1"
              >
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center group-hover:bg-blue-600 transition-colors">
                      <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414L10.89 12.89A6 6 0 012 8z" clipRule="evenodd" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-white group-hover:text-blue-400 transition-colors">Advanced Search</h3>
                    <p className="text-gray-400">Find wrestlers by criteria</p>
                  </div>
                </div>
              </Link>

              <Link
                to="/statistics"
                className="group bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:bg-white/10 hover:border-green-500/50 transition-all duration-300 hover:-translate-y-1"
              >
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center group-hover:bg-green-600 transition-colors">
                      <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" />
                        <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-white group-hover:text-green-400 transition-colors">Statistics</h3>
                    <p className="text-gray-400">Analytics and rankings</p>
                  </div>
                </div>
              </Link>

              <Link
                to="/search"
                className="group bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:bg-white/10 hover:border-yellow-500/50 transition-all duration-300 hover:-translate-y-1"
              >
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-yellow-500 rounded-lg flex items-center justify-center group-hover:bg-yellow-600 transition-colors">
                      <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                      </svg>
                    </div>
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-white group-hover:text-yellow-400 transition-colors">Quick Search</h3>
                    <p className="text-gray-400">Find wrestlers fast</p>
                  </div>
                </div>
              </Link>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default Homepage;
