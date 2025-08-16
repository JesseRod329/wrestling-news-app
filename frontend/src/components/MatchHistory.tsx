import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

interface Match {
  id: string;
  date: string;
  promotion: string;
  event: string;
  matchType: string;
  participants: string[];
  result: string;
  duration?: string;
  location?: string;
  title?: string;
}

interface MatchHistoryProps {
  wrestlerId: string;
  wrestlerName: string;
  className?: string;
}

const MatchHistory: React.FC<MatchHistoryProps> = ({ wrestlerId, wrestlerName, className = '' }) => {
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMatchHistory();
  }, [wrestlerId]);

  const fetchMatchHistory = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // For now, using mock data that mimics Cagematch.net structure
      // In production, this would call an API that scrapes Cagematch.net
      const mockMatches: Match[] = [
        {
          id: '1',
          date: '2025-04-20',
          promotion: 'WWE',
          event: 'WrestleMania 41 - Sunday',
          matchType: 'Triple Threat',
          participants: ['IYO SKY (c)', wrestlerName, 'Rhea Ripley'],
          result: 'IYO SKY defeats ' + wrestlerName + ' and Rhea Ripley',
          duration: '14:26',
          location: 'Allegiant Stadium, Paradise, Nevada, USA',
          title: 'WWE Women\'s World Title'
        },
        {
          id: '2',
          date: '2025-03-01',
          promotion: 'WWE',
          event: 'Elimination Chamber 2025',
          matchType: 'Elimination Chamber',
          participants: [wrestlerName, 'Alexa Bliss', 'Bayley', 'Liv Morgan', 'Naomi', 'Roxanne Perez'],
          result: wrestlerName + ' defeats all opponents',
          duration: '29:15',
          location: 'Rogers Centre, Toronto, Ontario, Canada',
          title: 'WWE Women\'s World Title #1 Contendership'
        },
        {
          id: '3',
          date: '2025-02-28',
          promotion: 'WWE',
          event: 'Friday Night SmackDown #1332',
          matchType: 'Tag Team',
          participants: ['Roxanne Perez & The Judgment Day (Liv Morgan & Raquel Rodriguez)', 'Bayley', wrestlerName, 'Naomi'],
          result: 'Roxanne Perez & The Judgment Day defeat Bayley, ' + wrestlerName + ' & Naomi',
          duration: '8:55',
          location: 'Scotiabank Arena, Toronto, Ontario, Canada'
        },
        {
          id: '4',
          date: '2025-02-24',
          promotion: 'WWE',
          event: 'Monday Night RAW #1657',
          matchType: 'Tag Team Title Match',
          participants: ['The Judgment Day (Liv Morgan & Raquel Rodriguez)', wrestlerName + ' & Naomi (c)'],
          result: 'The Judgment Day defeat ' + wrestlerName + ' & Naomi - TITLE CHANGE!',
          duration: '11:59',
          location: 'Heritage Bank Center, Cincinnati, Ohio, USA',
          title: 'WWE Women\'s Tag Team Title'
        },
        {
          id: '5',
          date: '2025-02-07',
          promotion: 'WWE',
          event: 'Friday Night SmackDown #1329',
          matchType: 'Singles',
          participants: [wrestlerName, 'Piper Niven'],
          result: wrestlerName + ' defeats Piper Niven',
          duration: '8:05',
          location: 'FedExForum, Memphis, Tennessee, USA',
          title: 'Elimination Chamber Qualifying'
        }
      ];

      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 800));
      
      setMatches(mockMatches);
    } catch (error) {
      console.error('Error fetching match history:', error);
      setError('Failed to load match history');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getResultColor = (result: string, wrestlerName: string) => {
    if (result.includes(wrestlerName + ' defeats') || result.includes(wrestlerName + ' wins')) {
      return 'text-green-400';
    } else if (result.includes(wrestlerName + ' loses') || result.includes(wrestlerName + ' defeated')) {
      return 'text-red-400';
    }
    return 'text-gray-300';
  };

  if (loading) {
    return (
      <div className={`bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 ${className}`}>
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
          <span className="ml-3 text-gray-300">Loading match history...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 ${className}`}>
        <div className="text-center py-8">
          <div className="text-red-400 text-4xl mb-3">⚠️</div>
          <h3 className="text-white text-lg font-semibold mb-2">Error Loading Matches</h3>
          <p className="text-gray-400 mb-4">{error}</p>
          <button
            onClick={fetchMatchHistory}
            className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white/5 backdrop-blur-sm rounded-xl border border-white/10 ${className}`}>
      {/* Header */}
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-bold text-white mb-2">Recent Match History</h3>
            <p className="text-gray-400">Latest matches and results for {wrestlerName}</p>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-400 bg-white/10 px-3 py-1 rounded-full">
              {matches.length} matches
            </span>
            <button
              onClick={fetchMatchHistory}
              className="p-2 bg-purple-600/20 hover:bg-purple-600/30 text-purple-400 rounded-lg transition-colors"
              title="Refresh matches"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Matches List */}
      <div className="divide-y divide-white/10">
        {matches.map((match) => (
          <div key={match.id} className="p-6 hover:bg-white/5 transition-colors duration-200">
            <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-3 lg:space-y-0">
              {/* Match Info */}
              <div className="flex-1 space-y-2">
                {/* Date and Promotion */}
                <div className="flex items-center space-x-3 text-sm">
                  <span className="text-purple-400 font-medium">{formatDate(match.date)}</span>
                  <span className="text-gray-400">•</span>
                  <span className="text-blue-400 font-medium">{match.promotion}</span>
                  {match.duration && (
                    <>
                      <span className="text-gray-400">•</span>
                      <span className="text-gray-300">{match.duration}</span>
                    </>
                  )}
                </div>

                {/* Event */}
                <h4 className="text-white font-semibold text-lg">{match.event}</h4>

                {/* Match Type and Title */}
                <div className="flex items-center space-x-3">
                  {match.title && (
                    <span className="bg-yellow-600/20 text-yellow-400 text-xs px-2 py-1 rounded-full border border-yellow-600/30">
                      {match.title}
                    </span>
                  )}
                  <span className="text-gray-300 text-sm">{match.matchType}</span>
                </div>

                {/* Participants */}
                <div className="text-gray-300 text-sm">
                  <span className="text-gray-400">Participants: </span>
                  {match.participants.join(' vs ')}
                </div>

                {/* Result */}
                <div className={`font-medium ${getResultColor(match.result, wrestlerName)}`}>
                  {match.result}
                </div>

                {/* Location */}
                {match.location && (
                  <div className="text-gray-400 text-sm flex items-center space-x-1">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span>{match.location}</span>
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              <div className="flex items-center space-x-2 lg:ml-4">
                <button className="bg-purple-600/20 hover:bg-purple-600/30 text-purple-400 px-3 py-2 rounded-lg text-sm transition-colors">
                  View Details
                </button>
                <button className="bg-white/10 hover:bg-white/20 text-gray-300 px-3 py-2 rounded-lg text-sm transition-colors">
                  Share
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="p-6 border-t border-white/10 bg-white/5">
        <div className="text-center">
          <p className="text-gray-400 text-sm mb-3">
            Match data sourced from Cagematch.net
          </p>
          <Link
            to={`https://www.cagematch.net/?id=2&nr=${wrestlerId}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center text-purple-400 hover:text-purple-300 text-sm transition-colors"
          >
            View Full Profile on Cagematch.net
            <svg className="ml-1 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
            </svg>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default MatchHistory;
