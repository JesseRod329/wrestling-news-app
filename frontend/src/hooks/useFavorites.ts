import { useState, useEffect } from 'react';
import { Wrestler } from '../types';

const useFavorites = () => {
  const [favorites, setFavorites] = useState<Wrestler[]>([]);

  useEffect(() => {
    const storedFavorites = localStorage.getItem('favorites');
    if (storedFavorites) {
      setFavorites(JSON.parse(storedFavorites));
    }
  }, []);

  const addFavorite = (wrestler: Wrestler) => {
    const newFavorites = [...favorites, wrestler];
    setFavorites(newFavorites);
    localStorage.setItem('favorites', JSON.stringify(newFavorites));
  };

  const removeFavorite = (wrestlerId: string) => {
    const newFavorites = favorites.filter(w => w.id !== wrestlerId);
    setFavorites(newFavorites);
    localStorage.setItem('favorites', JSON.stringify(newFavorites));
  };

  return { favorites, addFavorite, removeFavorite };
};

export default useFavorites; 