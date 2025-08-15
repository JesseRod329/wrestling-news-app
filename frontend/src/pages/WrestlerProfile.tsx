import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import apiService from '../services/api';
import { Wrestler } from '../types';
import useFavorites from '../hooks/useFavorites';

const WrestlerProfile: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [wrestler, setWrestler] = useState<Wrestler | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { favorites, addFavorite, removeFavorite } = useFavorites();

  useEffect(() => {
    const fetchWrestler = async () => {
      if (id) {
        try {
          setLoading(true);
          setError(null);
          const wrestlerData = await apiService.getWrestler(id);
          if (wrestlerData) {
            setWrestler(wrestlerData);
          } else {
            setError('Wrestler not found');
          }
        } catch (error) {
          console.error('Failed to fetch wrestler:', error);
          setError('Failed to load wrestler data');
        } finally {
          setLoading(false);
        }
      }
    };
    fetchWrestler();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#1a1a1a] to-[#2d1b1b] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-[#e9242a] mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading Wrestler Profile...</p>
        </div>
      </div>
    );
  }

  if (error || !wrestler) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#1a1a1a] to-[#2d1b1b] flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-white text-xl font-bold mb-4">Error Loading Profile</h2>
          <p className="text-gray-300 mb-6">{error || 'Wrestler not found'}</p>
          <Link
            to="/"
            className="bg-[#e9242a] text-white px-6 py-3 rounded-lg hover:bg-[#d11a1a] transition-colors duration-200"
          >
            Back to Home
          </Link>
        </div>
      </div>
    );
  }

  const isFavorite = favorites.some((fav: Wrestler) => fav.id === wrestler.id);

  const handleFavoriteClick = () => {
    if (isFavorite) {
      removeFavorite(wrestler.id);
    } else {
      addFavorite(wrestler);
    }
  };

  const formatRating = (rating: string | undefined) => {
    if (!rating) return 'N/A';
    return `${rating}/10`;
  };

  const formatMomentum = (score: number) => {
    if (score > 0) return `+${score}`;
    if (score < 0) return `${score}`;
    return '0';
  };

  const renderYearlyRatings = () => {
    if (!wrestler.yearlyRatings || Object.keys(wrestler.yearlyRatings).length === 0) {
      return <p className="text-gray-400">No yearly ratings available</p>;
    }

    const sortedYears = Object.keys(wrestler.yearlyRatings).sort().reverse();
    
    return (
      <div className="space-y-3">
        {sortedYears.map(year => {
          const yearData = wrestler.yearlyRatings![year];
          const rating = parseFloat(yearData.rating);
          const percentage = (rating / 10) * 100;
          
          return (
            <div key={year} className="flex items-center gap-3">
              <span className="text-white font-medium min-w-[60px]">{year}</span>
              <div className="flex-1 bg-gray-700 rounded-full h-3">
                <div 
                  className="bg-gradient-to-r from-[#e9242a] to-[#ff6b6b] h-3 rounded-full transition-all duration-300"
                  style={{ width: `${percentage}%` }}
                ></div>
              </div>
              <span className="text-white font-bold min-w-[80px] text-right">
                {yearData.rating}/10
              </span>
              <span className="text-gray-400 text-sm min-w-[60px] text-right">
                ({yearData.votes} votes)
              </span>
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#1a1a1a] to-[#2d1b1b]">
      {/* Hero Section */}
      <div className="relative">
        <div
          className="h-64 md:h-80 bg-cover bg-center relative"
          style={{ backgroundImage: `url(${wrestler.image})` }}
        >
          <div className="absolute inset-0 bg-black bg-opacity-50"></div>
          <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent"></div>
        </div>
        
        {/* Back Button */}
        <Link
          to="/"
          className="absolute top-4 left-4 bg-black bg-opacity-50 text-white p-2 rounded-full hover:bg-opacity-70 transition-all duration-200"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
        </Link>

        {/* Favorite Button */}
        <button
          onClick={handleFavoriteClick}
          className="absolute top-4 right-4 bg-black bg-opacity-50 text-white p-3 rounded-full hover:bg-opacity-70 transition-all duration-200"
        >
          <span className="text-2xl">{isFavorite ? '★' : '☆'}</span>
        </button>
      </div>

      {/* Profile Content */}
      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Header Info */}
        <div className="bg-[#261c1c] rounded-xl p-6 mb-8 shadow-lg">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-4xl md:text-5xl font-bold text-white mb-2">
                {wrestler.name}
              </h1>
              {wrestler.nickname && (
                <p className="text-[#e9242a] text-xl font-medium italic">
                  "{wrestler.nickname}"
                </p>
              )}
              {wrestler.promotion && (
                <p className="text-[#b89d9e] text-lg mt-2">
                  {wrestler.promotion} • {wrestler.brand || 'All Brands'}
                </p>
              )}
            </div>
            
            {/* Rating Display */}
            <div className="text-center bg-[#1a1a1a] rounded-lg p-4 min-w-[120px]">
              <div className="text-[#b89d9e] text-sm">Rating</div>
              <div className="text-white text-3xl font-bold">
                {formatRating(wrestler.averageRating)}
              </div>
              {wrestler.totalVotes && (
                <div className="text-[#b89d9e] text-xs">
                  {wrestler.totalVotes} votes
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Personal Info */}
          <div className="lg:col-span-1 space-y-6">
            {/* Personal Data */}
            <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg">
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <span className="text-[#e9242a]">👤</span>
                Personal Data
              </h2>
              <div className="space-y-3">
                {wrestler.age > 0 && (
                  <div className="flex justify-between">
                    <span className="text-[#b89d9e]">Age:</span>
                    <span className="text-white font-medium">{wrestler.age} years</span>
                  </div>
                )}
                {wrestler.height && (
                  <div className="flex justify-between">
                    <span className="text-[#b89d9e]">Height:</span>
                    <span className="text-white font-medium">{wrestler.height}</span>
                  </div>
                )}
                {wrestler.weight && (
                  <div className="flex justify-between">
                    <span className="text-[#b89d9e]">Weight:</span>
                    <span className="text-white font-medium">{wrestler.weight}</span>
                  </div>
                )}
                {wrestler.hometown && (
                  <div className="flex justify-between">
                    <span className="text-[#b89d9e]">Hometown:</span>
                    <span className="text-white font-medium">{wrestler.hometown}</span>
                  </div>
                )}
                {wrestler.experience && (
                  <div className="flex justify-between">
                    <span className="text-[#b89d9e]">Experience:</span>
                    <span className="text-white font-medium">{wrestler.experience}</span>
                  </div>
                )}
                {wrestler.wrestlingStyle && (
                  <div className="flex justify-between">
                    <span className="text-[#b89d9e]">Style:</span>
                    <span className="text-white font-medium">{wrestler.wrestlingStyle}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Signature Moves */}
            {wrestler.signatureMoves && wrestler.signatureMoves.length > 0 && (
              <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg">
                <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                  <span className="text-[#e9242a]">⚡</span>
                  Signature Moves
                </h2>
                <div className="flex flex-wrap gap-2">
                  {wrestler.signatureMoves.map((move, index) => (
                    <span
                      key={index}
                      className="px-3 py-2 bg-[#e9242a] text-white text-sm rounded-full font-medium"
                    >
                      {move}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Social Media */}
            {wrestler.socialMedia && Object.keys(wrestler.socialMedia).length > 0 && (
              <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg">
                <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                  <span className="text-[#e9242a]">🌐</span>
                  Social Media
                </h2>
                <div className="space-y-2">
                  {Object.entries(wrestler.socialMedia).map(([platform, url]) => (
                    <a
                      key={platform}
                      href={url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 text-[#b89d9e] hover:text-white transition-colors duration-200"
                    >
                      <span className="capitalize">{platform}:</span>
                      <span className="text-blue-400 hover:underline">{url}</span>
                    </a>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Career & Stats */}
          <div className="lg:col-span-2 space-y-6">
            {/* Career Data */}
            <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg">
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <span className="text-[#e9242a]">🏆</span>
                Career Information
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {wrestler.roles && wrestler.roles.length > 0 && (
                  <div>
                    <h3 className="text-[#b89d9e] font-medium mb-2">Roles</h3>
                    <div className="flex flex-wrap gap-2">
                      {wrestler.roles.map((role, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-[#382929] text-white text-xs rounded"
                        >
                          {role}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {wrestler.alterEgos && wrestler.alterEgos.length > 0 && (
                  <div>
                    <h3 className="text-[#b89d9e] font-medium mb-2">Alter Egos</h3>
                    <div className="flex flex-wrap gap-2">
                      {wrestler.alterEgos.map((ego, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-[#382929] text-white text-xs rounded"
                        >
                          {ego}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {wrestler.trainers && wrestler.trainers.length > 0 && (
                  <div className="md:col-span-2">
                    <h3 className="text-[#b89d9e] font-medium mb-2">Trainers</h3>
                    <div className="flex flex-wrap gap-2">
                      {wrestler.trainers.map((trainer, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-[#382929] text-white text-xs rounded"
                        >
                          {trainer}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Yearly Ratings */}
            <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg">
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <span className="text-[#e9242a]">📊</span>
                Yearly Performance
              </h2>
              {renderYearlyRatings()}
            </div>

            {/* Momentum Score */}
            <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg">
              <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                <span className="text-[#e9242a]">📈</span>
                Momentum Score
              </h2>
              <div className="text-center">
                <div className={`text-4xl font-bold mb-2 ${
                  wrestler.momentumScore > 0 ? 'text-green-400' : 
                  wrestler.momentumScore < 0 ? 'text-red-400' : 'text-gray-400'
                }`}>
                  {formatMomentum(wrestler.momentumScore)}
                </div>
                <p className="text-[#b89d9e]">
                  {wrestler.momentumScore > 0 ? 'Rising Star' : 
                   wrestler.momentumScore < 0 ? 'Declining' : 'Stable Performance'}
                </p>
              </div>
            </div>

            {/* Bio */}
            {wrestler.bio && (
              <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg">
                <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
                  <span className="text-[#e9242a]">📖</span>
                  Biography
                </h2>
                <p className="text-white leading-relaxed">{wrestler.bio}</p>
              </div>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to={`/wrestlers/${wrestler.id}/stats`}
            className="bg-[#e9242a] text-white px-8 py-3 rounded-lg hover:bg-[#d11a1a] transition-colors duration-200 text-center font-semibold"
          >
            View Detailed Statistics
          </Link>
          <button
            onClick={handleFavoriteClick}
            className={`px-8 py-3 rounded-lg transition-colors duration-200 text-center font-semibold ${
              isFavorite 
                ? 'bg-yellow-500 text-black hover:bg-yellow-400' 
                : 'bg-[#382929] text-white hover:bg-[#4a3a3a]'
            }`}
          >
            {isFavorite ? '★ Remove from Favorites' : '☆ Add to Favorites'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default WrestlerProfile; 