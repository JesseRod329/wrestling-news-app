import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import apiService from '../services/api';
import { Wrestler } from '../types';

const WrestlerStats: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [wrestler, setWrestler] = useState<Wrestler | null>(null);

  useEffect(() => {
    const fetchWrestler = async () => {
      if (id) {
        try {
          const wrestlerData = await apiService.getWrestler(id);
          setWrestler(wrestlerData);
        } catch (error) {
          console.error('Failed to fetch wrestler stats:', error);
        }
      }
    };
    fetchWrestler();
  }, [id]);

  if (!wrestler) {
    return <div>Loading...</div>;
  }

  return (
    <div className="bg-[#171212] min-h-screen text-white p-4">
      <h1 className="text-2xl font-bold mb-4">{wrestler.name}'s Stats</h1>
      {/* Add more detailed stats here */}
    </div>
  );
};

export default WrestlerStats; 