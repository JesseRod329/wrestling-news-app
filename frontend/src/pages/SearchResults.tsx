import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import apiService from '../services/api';
import { Wrestler, SearchResult } from '../types';
import WrestlerCard from '../components/WrestlerCard';

const SearchResults: React.FC = () => {
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q') || '';
  const [results, setResults] = useState<Wrestler[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      setLoading(true);
      try {
        if (query.trim()) {
          // Use searchWrestlers for search functionality
          const searchResults = await apiService.searchWrestlers(query);
          
          // Transform search results to match Wrestler interface
          const transformedResults = searchResults.map(result => ({
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
          
          setResults(transformedResults);
        } else {
          // If no query, get all wrestlers
          const allWrestlers = await apiService.getWrestlers();
          setResults(allWrestlers);
        }
      } catch (error) {
        console.error('Failed to fetch search results:', error);
        setResults([]);
      }
      setLoading(false);
    };
    fetchResults();
  }, [query]);

  return (
    <div className="bg-[#171212] min-h-screen text-white p-4">
      <h1 className="text-2xl font-bold mb-4">Search Results for "{query}"</h1>
      {loading ? (
        <p>Loading...</p>
      ) : results.length === 0 ? (
        <p className="text-center text-gray-400">No wrestlers found for '{query}'.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {results.map(wrestler => (
            <WrestlerCard key={wrestler.id} wrestler={wrestler} />
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchResults; 