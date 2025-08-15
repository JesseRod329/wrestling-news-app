import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Wrestler } from '../types';
import EnhancedImageDisplay from './EnhancedImageDisplay';

interface WrestlerCardProps {
  wrestler: Wrestler;
  className?: string;
}

const WrestlerCard: React.FC<WrestlerCardProps> = ({ wrestler, className = '' }) => {
  const [isHovered, setIsHovered] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);

  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  const handleImageError = () => {
    setImageLoaded(false);
  };

  return (
    <div
      className={`group relative bg-white/5 backdrop-blur-sm rounded-xl overflow-hidden border border-white/10 hover:border-purple-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-purple-500/20 hover:-translate-y-1 ${className}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Background Image */}
      <div className="relative h-48 overflow-hidden">
        {wrestler.image_url || wrestler.image ? (
          <EnhancedImageDisplay
            src={wrestler.image_url || wrestler.image}
            alt={wrestler.name}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
            onLoad={handleImageLoad}
            onError={handleImageError}
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center">
            <span className="text-4xl font-bold text-white">
              {wrestler.name.charAt(0).toUpperCase()}
            </span>
          </div>
        )}

        {/* Overlay Gradient */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

        {/* Hover Info */}
        <div className={`absolute inset-0 flex items-end p-4 transition-all duration-300 ${
          isHovered ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
        }`}>
          <div className="text-white">
            <p className="text-sm text-gray-300 mb-1">
              {wrestler.promotion || 'Unknown Promotion'}
            </p>
            {wrestler.averageRating && (
              <div className="flex items-center space-x-2">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <svg
                      key={i}
                      className={`w-4 h-4 ${
                        i < Math.floor(parseFloat(wrestler.averageRating || '0'))
                          ? 'text-yellow-400 fill-current'
                          : 'text-gray-400'
                      }`}
                      viewBox="0 0 20 20"
                    >
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  ))}
                </div>
                <span className="text-sm font-medium">
                  {wrestler.averageRating}
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Quick Stats Badge */}
        {wrestler.careerStats && wrestler.careerStats.totalMatches > 0 && (
          <div className="absolute top-3 right-3 bg-black/60 backdrop-blur-sm text-white text-xs px-2 py-1 rounded-full border border-white/20">
            {wrestler.careerStats.totalMatches} matches
          </div>
        )}

        {/* Rating Badge */}
        {wrestler.averageRating && (
          <div className="absolute top-3 left-3 bg-yellow-600/80 backdrop-blur-sm text-white text-xs px-2 py-1 rounded-full border border-yellow-400/40 font-medium">
            ⭐ {wrestler.averageRating}
          </div>
        )}
      </div>

      {/* Card Content */}
      <div className="p-4">
        <div className="mb-3">
          <h3 className="text-lg font-semibold text-white group-hover:text-purple-400 transition-colors duration-200 mb-1">
            {wrestler.name}
          </h3>
          
          {wrestler.nickname && (
            <p className="text-sm text-gray-400 italic">"{wrestler.nickname}"</p>
          )}
        </div>

        {/* Quick Info */}
        <div className="space-y-2 mb-4">
          {wrestler.age && wrestler.age > 0 && (
            <div className="flex items-center text-sm text-gray-300">
              <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              {wrestler.age} years old
            </div>
          )}

          {wrestler.promotion && wrestler.promotion !== 'Unknown' && (
            <div className="flex items-center text-sm text-gray-300">
              <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
              {wrestler.promotion}
            </div>
          )}

          {wrestler.hometown && wrestler.hometown !== 'Unknown' && (
            <div className="flex items-center text-sm text-gray-300">
              <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {wrestler.hometown}
            </div>
          )}

          {wrestler.wrestlingStyle && (
            <div className="flex items-center text-sm text-gray-300">
              <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              {wrestler.wrestlingStyle}
            </div>
          )}

          {wrestler.experience && (
            <div className="flex items-center text-sm text-gray-300">
              <svg className="w-4 h-4 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {wrestler.experience}
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-2">
          <Link
            to={`/wrestlers/${wrestler.id}`}
            className="flex-1 bg-purple-600 hover:bg-purple-700 text-white text-sm font-medium py-2 px-3 rounded-lg transition-colors duration-200 text-center group-hover:shadow-lg group-hover:shadow-purple-500/25"
          >
            View Profile
          </Link>
          
          <button
            className="p-2 bg-white/10 hover:bg-white/20 text-gray-300 hover:text-white rounded-lg transition-colors duration-200 border border-white/20 hover:border-white/40"
            title="Add to Favorites"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </button>
        </div>

        {/* Momentum Score Indicator */}
        {wrestler.momentumScore !== undefined && wrestler.momentumScore !== 0 && (
          <div className="mt-3 pt-3 border-t border-white/10">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-400">Momentum</span>
              <span className={`font-medium ${
                wrestler.momentumScore > 0 ? 'text-green-400' : 
                wrestler.momentumScore < 0 ? 'text-red-400' : 'text-gray-400'
              }`}>
                {wrestler.momentumScore > 0 ? '+' : ''}{wrestler.momentumScore}
              </span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-1.5 mt-1">
              <div 
                className={`h-1.5 rounded-full transition-all duration-300 ${
                  wrestler.momentumScore > 0 ? 'bg-green-500' : 
                  wrestler.momentumScore < 0 ? 'bg-red-500' : 'bg-gray-500'
                }`}
                style={{ 
                  width: `${Math.min(Math.abs(wrestler.momentumScore) / 100 * 100, 100)}%` 
                }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Hover Glow Effect */}
      <div className={`absolute inset-0 rounded-xl pointer-events-none transition-opacity duration-300 ${
        isHovered ? 'opacity-100' : 'opacity-0'
      }`}>
        <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-blue-500/20 rounded-xl" />
      </div>
    </div>
  );
};

export default WrestlerCard; 