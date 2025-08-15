import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import WrestlerAvatar from '../components/WrestlerAvatar';
import WrestlerCard from '../components/WrestlerCard';
import { Wrestler } from '../types';
import apiService from '../services/api';

const Home: React.FC = () => {
  const [favorites, setFavorites] = useState<Wrestler[]>([]);
  const [comparison, setComparison] = useState<Wrestler[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<Wrestler[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const wrestlers = await apiService.getWrestlers();
        setFavorites(wrestlers.slice(0, 5));
        setComparison(wrestlers.slice(5, 7));
      } catch (error) {
        console.error('Failed to fetch wrestlers:', error);
      }
    };
    fetchData();
  }, []);

  useEffect(() => {
    if (searchQuery.trim() === '') {
      setSearchResults([]);
      return;
    }

    const fetchSearch = async () => {
      try {
        // Use searchWrestlers for search functionality
        const results = await apiService.searchWrestlers(searchQuery);
        // Transform search results to match Wrestler interface
        const transformedResults = results.map(result => ({
          id: result.wrestler_id,
          name: result.name,
          image: `https://via.placeholder.com/400x300/1a1a1a/ffffff?text=${encodeURIComponent(result.name)}`,
          age: 0,
          height: 'Unknown',
          weight: 'Unknown',
          hometown: 'Unknown',
          signatureMoves: [],
          recentMatches: [],
          momentumScore: 0,
          careerStats: {
            totalMatches: 0,
            wins: 0,
            losses: 0,
            draws: 0,
            winPercentage: 0
          },
          championships: []
        }));
        setSearchResults(transformedResults);
      } catch (error) {
        console.error('Failed to fetch search results:', error);
      }
    };

    const debounce = setTimeout(() => {
      fetchSearch();
    }, 300);

    return () => clearTimeout(debounce);
  }, [searchQuery]);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  return (
    <div>
      <SearchBar onSearch={handleSearch} placeholder="Search wrestlers..." />
      {searchResults.length > 0 ? (
        <div className="p-4">
          {searchResults.map(w => (
            <Link to={`/wrestlers/${w.id}`} key={w.id} className="block text-white p-2 border-b border-gray-700">
              {w.name}
            </Link>
          ))}
        </div>
      ) : (
        <>
          <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Favorite Wrestlers</h2>
          <div className="flex overflow-y-auto [-ms-scrollbar-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
            <div className="flex items-stretch p-4 gap-8">
              {favorites.map(w => (
                <WrestlerAvatar key={w.id} id={w.id} img={w.image} />
              ))}
            </div>
          </div>
          <h2 className="text-white text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Wrestler Comparison</h2>
          {comparison.map(w => (
            <WrestlerCard key={w.id} wrestler={w} />
          ))}
        </>
      )}
    </div>
  );
};

export default Home; 