import React from 'react';
import useFavorites from '../hooks/useFavorites';
import WrestlerAvatar from '../components/WrestlerAvatar';

const Favorites: React.FC = () => {
  const { favorites } = useFavorites();

  return (
    <div className="text-white p-4">
      {favorites.length === 0 ? (
        <p className="text-center text-gray-400">Tap the star on a wrestler's profile to add them to your favorites!</p>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {favorites.map(wrestler => (
            <WrestlerAvatar key={wrestler.id} id={wrestler.id} img={wrestler.image} />
          ))}
        </div>
      )}
    </div>
  );
};

export default Favorites; 