import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import FloatingActionButton from './FloatingActionButton';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();

  const navItems = [
    { href: '/', icon: 'Home', label: 'Home' },
    { href: '/news', icon: 'Newspaper', label: 'News' },
    { href: '/search', icon: 'Search', label: 'Search' },
    { href: '/advanced-search', icon: 'Filter', label: 'Advanced Search' },
    { href: '/statistics', icon: 'ChartBar', label: 'Statistics' },
    { href: '/favorites', icon: 'Heart', label: 'Favorites' },
    { href: '/settings', icon: 'Cog', label: 'Settings' }
  ];

  const icons: Record<string, React.ReactNode> = {
    Home: (
      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
      </svg>
    ),
    Newspaper: (
      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M2 5a2 2 0 012-2h8a2 2 0 012 2v10a2 2 0 002 2H4a2 2 0 01-2-2V5zm3 1h6v4H5V6zm6 6H5v2h6v-2z" clipRule="evenodd" />
      </svg>
    ),
    Search: (
      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414L10.89 12.89A6 6 0 012 8z" clipRule="evenodd" />
      </svg>
    ),
    Filter: (
      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M3 3a1 1 0 011-1h12a1 1 0 011 1v3a1 1 0 01-.293.707L12 11.414V15a1 1 0 01-.293.707l-2 2A1 1 0 018 17v-5.586L3.293 6.707A1 1 0 013 6V3z" clipRule="evenodd" />
      </svg>
    ),
    ChartBar: (
      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" />
        <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" />
      </svg>
    ),
    Heart: (
      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
      </svg>
    ),
    Cog: (
      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
      </svg>
    )
  };

  const getHeaderTitle = () => {
    switch (location.pathname) {
      case '/':
        return 'Wrestling News & Stats';
      case '/news':
        return 'Wrestling News';
      case '/search':
        return 'Search Wrestlers';
      case '/advanced-search':
        return 'Advanced Search';
      case '/statistics':
        return 'Wrestling Statistics';
      case '/favorites':
        return 'My Favorites';
      case '/settings':
        return 'Settings';
      default:
        return 'Wrestling News & Stats';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="bg-white/5 backdrop-blur-sm border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo and Title */}
            <div className="flex items-center">
              <Link to="/" className="flex items-center space-x-3 group">
                <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg flex items-center justify-center group-hover:from-purple-600 group-hover:to-blue-600 transition-all duration-200">
                  <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M2 5a2 2 0 012-2h8a2 2 0 012 2v10a2 2 0 002 2H4a2 2 0 01-2-2V5zm3 1h6v4H5V6zm6 6H5v2h6v-2z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="hidden sm:block">
                  <h1 className="text-xl font-bold text-white group-hover:text-purple-400 transition-colors">
                    {getHeaderTitle()}
                  </h1>
                </div>
              </Link>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex space-x-1">
              {navItems.map((item) => {
                const isActive = location.pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    to={item.href}
                    className={`px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                      isActive
                        ? 'bg-purple-600 text-white shadow-lg'
                        : 'text-gray-300 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    <div className="flex items-center space-x-2">
                      {icons[item.icon]}
                      <span>{item.label}</span>
                    </div>
                  </Link>
                );
              })}
            </nav>

            {/* Mobile menu button */}
            <div className="md:hidden">
              <button className="text-gray-300 hover:text-white p-2 rounded-md hover:bg-white/10 transition-colors">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white/5 backdrop-blur-sm border-t border-white/10 mt-16">
        <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-gray-400 text-sm">
              © 2025 Wrestling News & Stats. Your ultimate source for wrestling information and analytics.
            </p>
            <div className="mt-4 flex justify-center space-x-6">
              <Link to="/news" className="text-gray-400 hover:text-purple-400 transition-colors text-sm">
                News
              </Link>
              <Link to="/statistics" className="text-gray-400 hover:text-blue-400 transition-colors text-sm">
                Statistics
              </Link>
              <Link to="/search" className="text-gray-400 hover:text-green-400 transition-colors text-sm">
                Search
              </Link>
            </div>
          </div>
        </div>
      </footer>

      {/* Floating Action Button */}
      <FloatingActionButton />
    </div>
  );
};

export default Layout; 