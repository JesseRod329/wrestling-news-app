import React, { useState, useEffect, useRef } from 'react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
  suggestions?: string[];
  className?: string;
}

const SearchBar: React.FC<SearchBarProps> = ({ 
  onSearch, 
  placeholder = "Search...",
  suggestions = [],
  className = ""
}) => {
  const [query, setQuery] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const searchRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (query.trim() === '') {
      setFilteredSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    const filtered = suggestions.filter(suggestion =>
      suggestion.toLowerCase().includes(query.toLowerCase())
    );
    setFilteredSuggestions(filtered);
    setShowSuggestions(filtered.length > 0);
    setSelectedIndex(-1);
  }, [query, suggestions]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex(prev => 
        prev < filteredSuggestions.length - 1 ? prev + 1 : prev
      );
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex(prev => prev > 0 ? prev - 1 : -1);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedIndex >= 0 && filteredSuggestions[selectedIndex]) {
        handleSuggestionClick(filteredSuggestions[selectedIndex]);
      } else if (query.trim()) {
        handleSearch();
      }
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
      setSelectedIndex(-1);
    }
  };

  const handleSearch = () => {
    if (query.trim()) {
      onSearch(query.trim());
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setQuery(suggestion);
    onSearch(suggestion);
    setShowSuggestions(false);
    setSelectedIndex(-1);
  };

  const handleInputFocus = () => {
    if (filteredSuggestions.length > 0) {
      setShowSuggestions(true);
    }
  };

  return (
    <div ref={searchRef} className={`relative ${className}`}>
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onFocus={handleInputFocus}
          placeholder={placeholder}
          className="w-full px-4 py-3 pl-12 pr-20 bg-white/10 border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 backdrop-blur-sm"
        />
        
        {/* Search Icon */}
        <div className="absolute left-4 top-1/2 transform -translate-y-1/2">
          <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>

        {/* Search Button */}
        <button
          onClick={handleSearch}
          disabled={!query.trim()}
          className="absolute right-2 top-1/2 transform -translate-y-1/2 px-4 py-1.5 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white text-sm font-medium rounded-lg transition-all duration-200"
        >
          Search
        </button>
      </div>

      {/* Suggestions Dropdown */}
      {showSuggestions && (
        <div className="absolute z-50 w-full mt-2 bg-white/10 backdrop-blur-md border border-white/20 rounded-xl shadow-2xl overflow-hidden animate-in slide-in-from-top-2 duration-200">
          {filteredSuggestions.map((suggestion, index) => (
            <button
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
              className={`w-full px-4 py-3 text-left text-white hover:bg-white/20 transition-colors duration-150 ${
                index === selectedIndex ? 'bg-purple-600/30' : ''
              } ${index === filteredSuggestions.length - 1 ? '' : 'border-b border-white/10'}`}
            >
              <div className="flex items-center space-x-3">
                <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <span className="truncate">{suggestion}</span>
              </div>
            </button>
          ))}
        </div>
      )}

      {/* Quick Search Tips */}
      {!showSuggestions && query.trim() === '' && (
        <div className="absolute z-40 w-full mt-2 p-4 bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl text-center">
          <p className="text-gray-400 text-sm">
            💡 Try searching for: wrestlers, promotions, championships, or wrestling styles
          </p>
        </div>
      )}
    </div>
  );
};

export default SearchBar; 