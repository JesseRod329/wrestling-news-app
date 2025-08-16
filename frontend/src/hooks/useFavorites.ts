import { useState, useEffect } from 'react';
import { Wrestler } from '../types';

const useFavorites = () => {
  const [favorites, setFavorites] = useState<Wrestler[]>([]);

  useEffect(() => {
    const storedFavorites = localStorage.getItem('favorites');
    if (storedFavorites) {
      const parsedFavorites = JSON.parse(storedFavorites);
      console.log('Loaded favorites from localStorage:', parsedFavorites.map((f: Wrestler) => ({ id: f.id, name: f.name })));
      setFavorites(parsedFavorites);
    }
  }, []);

  const addFavorite = (wrestler: Wrestler) => {
    console.log('Adding wrestler to favorites:', wrestler.id, wrestler.name);
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