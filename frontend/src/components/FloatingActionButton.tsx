import React, { useState } from 'react';
import { Link } from 'react-router-dom';

interface FloatingActionButtonProps {
  className?: string;
}

const FloatingActionButton: React.FC<FloatingActionButtonProps> = ({ className = '' }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const actions = [
    {
      label: 'Quick Search',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      ),
      href: '/search',
      color: 'bg-purple-600 hover:bg-purple-700'
    },
    {
      label: 'Latest News',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
        </svg>
      ),
      href: '/news',
      color: 'bg-blue-600 hover:bg-blue-700'
    },
    {
      label: 'Statistics',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      ),
      href: '/statistics',
      color: 'bg-green-600 hover:bg-green-700'
    },
    {
      label: 'Favorites',
      icon: (
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
      ),
      href: '/favorites',
      color: 'bg-red-600 hover:bg-red-700'
    }
  ];

  return (
    <div className={`fixed bottom-6 right-6 z-50 ${className}`}>
      {/* Action Menu */}
      <div className={`absolute bottom-16 right-0 mb-2 transition-all duration-300 ${
        isOpen ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
      }`}>
        {actions.map((action, index) => (
          <div
            key={action.label}
            className="mb-3 transition-all duration-200"
            style={{ transitionDelay: `${index * 100}ms` }}
          >
            <Link
              to={action.href}
              className={`group flex items-center justify-center w-12 h-12 ${action.color} text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-110`}
              onClick={() => setIsOpen(false)}
            >
              {action.icon}
            </Link>
            <div className="absolute right-16 top-1/2 transform -translate-y-1/2 bg-gray-900 text-white text-sm px-2 py-1 rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-200">
              {action.label}
            </div>
          </div>
        ))}
      </div>

      {/* Main FAB Button */}
      <button
        onClick={toggleMenu}
        className={`w-14 h-14 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-110 focus:outline-none focus:ring-4 focus:ring-purple-500/50 ${
          isOpen ? 'rotate-45' : ''
        }`}
        aria-label="Quick Actions"
      >
        <svg className="w-6 h-6 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
      </button>

      {/* Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  );
};

export default FloatingActionButton;
