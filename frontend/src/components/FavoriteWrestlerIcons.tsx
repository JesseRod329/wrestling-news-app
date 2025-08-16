import React from 'react';
import { Link } from 'react-router-dom';
import useFavorites from '../hooks/useFavorites';

interface FavoriteWrestlerIconsProps {
  className?: string;
}

const FavoriteWrestlerIcons: React.FC<FavoriteWrestlerIconsProps> = ({ className = '' }) => {
  const { favorites } = useFavorites();

  // Only show if there are favorites
  if (favorites.length === 0) {
    return null;
  }

  // Take the first 3 favorites
  const displayFavorites = favorites.slice(0, 3);

  return (
    <div className={`mb-8 ${className}`}>
      <div className="text-center">
        <h3 className="text-lg font-semibold text-white mb-4">Your Favorite Wrestlers</h3>
        <div className="flex justify-center items-center space-x-6">
          {displayFavorites.map((wrestler) => (
            <Link
              key={wrestler.id}
              to={`/statistics?wrestler=${wrestler.id}`}
              className="group relative"
            >
              <div className="w-20 h-20 rounded-full overflow-hidden border-4 border-purple-500/30 hover:border-purple-400 transition-all duration-300 hover:scale-110 hover:shadow-lg hover:shadow-purple-500/25">
                {wrestler.image_url ? (
                  <img
                    src={wrestler.image_url}
                    alt={wrestler.name}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.src = `https://www.cagematch.net/pictures/profile/${wrestler.id}.jpg`;
                    }}
                  />
                ) : (
                  <div className="w-full h-full bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center">
                    <span className="text-white text-2xl font-bold">
                      {wrestler.name.split(' ').map(n => n[0]).join('')}
                    </span>
                  </div>
                )}
              </div>
              
              {/* Wrestler Name */}
              <div className="mt-2 text-center">
                <p className="text-sm text-white font-medium group-hover:text-purple-400 transition-colors duration-200">
                  {wrestler.name}
                </p>
              </div>
              
              {/* Hover Effect Ring */}
              <div className="absolute inset-0 rounded-full border-2 border-transparent group-hover:border-purple-400/50 transition-all duration-300 scale-110 opacity-0 group-hover:opacity-100"></div>
            </Link>
          ))}
        </div>
        
        {/* View All Favorites Link */}
        {favorites.length > 3 && (
          <div className="mt-4">
            <Link
              to="/favorites"
              className="inline-flex items-center text-sm text-purple-400 hover:text-purple-300 transition-colors duration-200"
            >
              View All Favorites
              <svg className="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default FavoriteWrestlerIcons;
