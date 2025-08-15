import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import WrestlerCard from '../components/WrestlerCard';
import apiService from '../services/api';
import { Wrestler } from '../types';

interface FilterOptions {
  name: string;
  promotion: string;
  brand: string;
  minRating: string;
  maxRating: string;
  minAge: string;
  maxAge: string;
  experience: string;
  wrestlingStyle: string;
  hometown: string;
}

const AdvancedSearch: React.FC = () => {
  const [wrestlers, setWrestlers] = useState<Wrestler[]>([]);
  const [filteredWrestlers, setFilteredWrestlers] = useState<Wrestler[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<FilterOptions>({
    name: '',
    promotion: '',
    brand: '',
    minRating: '',
    maxRating: '',
    minAge: '',
    maxAge: '',
    experience: '',
    wrestlingStyle: '',
    hometown: ''
  });

  // Get unique values for filter dropdowns
  const [uniqueValues, setUniqueValues] = useState({
    promotions: [] as string[],
    brands: [] as string[],
    wrestlingStyles: [] as string[],
    hometowns: [] as string[]
  });

  useEffect(() => {
    loadWrestlers();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [filters, wrestlers]);

  const loadWrestlers = async () => {
    try {
      setLoading(true);
      const data = await apiService.getWrestlers();
      setWrestlers(data);
      
      // Extract unique values for filters
      const promotions = Array.from(new Set(data.map(w => w.promotion).filter((p): p is string => Boolean(p))));
      const brands = Array.from(new Set(data.map(w => w.brand).filter((b): b is string => Boolean(b))));
      const styles = Array.from(new Set(data.map(w => w.wrestlingStyle).filter((s): s is string => Boolean(s))));
      const hometowns = Array.from(new Set(data.map(w => w.hometown).filter((h): h is string => Boolean(h))));
      
      setUniqueValues({
        promotions: promotions.sort(),
        brands: brands.sort(),
        wrestlingStyles: styles.sort(),
        hometowns: hometowns.sort()
      });
    } catch (error) {
      console.error('Failed to load wrestlers:', error);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...wrestlers];

    // Name filter (case-insensitive)
    if (filters.name.trim()) {
      filtered = filtered.filter(w => 
        w.name.toLowerCase().includes(filters.name.toLowerCase()) ||
        w.nickname?.toLowerCase().includes(filters.name.toLowerCase())
      );
    }

    // Promotion filter
    if (filters.promotion) {
      filtered = filtered.filter(w => w.promotion === filters.promotion);
    }

    // Brand filter
    if (filters.brand) {
      filtered = filtered.filter(w => w.brand === filters.brand);
    }

    // Rating range filter
    if (filters.minRating || filters.maxRating) {
      filtered = filtered.filter(w => {
        const rating = parseFloat(w.averageRating || '0');
        const min = filters.minRating ? parseFloat(filters.minRating) : 0;
        const max = filters.maxRating ? parseFloat(filters.maxRating) : 10;
        return rating >= min && rating <= max;
      });
    }

    // Age range filter
    if (filters.minAge || filters.maxAge) {
      filtered = filtered.filter(w => {
        const age = w.age || 0;
        const min = filters.minAge ? parseInt(filters.minAge) : 0;
        const max = filters.maxAge ? parseInt(filters.maxAge) : 100;
        return age >= min && age <= max;
      });
    }

    // Experience filter
    if (filters.experience) {
      filtered = filtered.filter(w => w.experience === filters.experience);
    }

    // Wrestling style filter
    if (filters.wrestlingStyle) {
      filtered = filtered.filter(w => w.wrestlingStyle === filters.wrestlingStyle);
    }

    // Hometown filter
    if (filters.hometown) {
      filtered = filtered.filter(w => w.hometown === filters.hometown);
    }

    setFilteredWrestlers(filtered);
  };

  const clearFilters = () => {
    setFilters({
      name: '',
      promotion: '',
      brand: '',
      minRating: '',
      maxRating: '',
      minAge: '',
      maxAge: '',
      experience: '',
      wrestlingStyle: '',
      hometown: ''
    });
  };

  const handleFilterChange = (field: keyof FilterOptions, value: string) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const getFilterCount = () => {
    return Object.values(filters).filter(value => value !== '').length;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#1a1a1a] to-[#2d1b1b] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-[#e9242a] mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading Advanced Search...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#1a1a1a] to-[#2d1b1b]">
      {/* Header */}
      <div className="bg-[#261c1c] shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white mb-2">
                🔍 Advanced Search
              </h1>
              <p className="text-[#b89d9e] text-lg">
                Find wrestlers with specific criteria
              </p>
            </div>
            <Link
              to="/"
              className="bg-[#e9242a] text-white px-6 py-3 rounded-lg hover:bg-[#d11a1a] transition-colors duration-200"
            >
              Back to Home
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Filters Section */}
        <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-white">Search Filters</h2>
            <div className="flex items-center gap-4">
              <span className="text-[#b89d9e]">
                {getFilterCount()} active filters
              </span>
              <button
                onClick={clearFilters}
                className="bg-[#382929] text-white px-4 py-2 rounded-lg hover:bg-[#4a3a3a] transition-colors duration-200"
              >
                Clear All
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Name Search */}
            <div>
              <label className="block text-[#b89d9e] font-medium mb-2">
                Name or Nickname
              </label>
              <input
                type="text"
                value={filters.name}
                onChange={(e) => handleFilterChange('name', e.target.value)}
                placeholder="Search by name..."
                className="w-full bg-[#382929] text-white border border-[#4a3a3a] rounded-lg px-4 py-2 focus:outline-none focus:border-[#e9242a]"
              />
            </div>

            {/* Promotion Filter */}
            <div>
              <label className="block text-[#b89d9e] font-medium mb-2">
                Promotion
              </label>
              <select
                value={filters.promotion}
                onChange={(e) => handleFilterChange('promotion', e.target.value)}
                className="w-full bg-[#382929] text-white border border-[#4a3a3a] rounded-lg px-4 py-2 focus:outline-none focus:border-[#e9242a]"
              >
                <option value="">All Promotions</option>
                {uniqueValues.promotions.map(promotion => (
                  <option key={promotion} value={promotion}>{promotion}</option>
                ))}
              </select>
            </div>

            {/* Brand Filter */}
            <div>
              <label className="block text-[#b89d9e] font-medium mb-2">
                Brand
              </label>
              <select
                value={filters.brand}
                onChange={(e) => handleFilterChange('brand', e.target.value)}
                className="w-full bg-[#382929] text-white border border-[#4a3a3a] rounded-lg px-4 py-2 focus:outline-none focus:border-[#e9242a]"
              >
                <option value="">All Brands</option>
                {uniqueValues.brands.map(brand => (
                  <option key={brand} value={brand}>{brand}</option>
                ))}
              </select>
            </div>

            {/* Rating Range */}
            <div>
              <label className="block text-[#b89d9e] font-medium mb-2">
                Rating Range
              </label>
              <div className="flex gap-2">
                <input
                  type="number"
                  min="0"
                  max="10"
                  step="0.1"
                  value={filters.minRating}
                  onChange={(e) => handleFilterChange('minRating', e.target.value)}
                  placeholder="Min"
                  className="flex-1 bg-[#382929] text-white border border-[#4a3a3a] rounded-lg px-3 py-2 focus:outline-none focus:border-[#e9242a]"
                />
                <span className="text-[#b89d9e] self-center">to</span>
                <input
                  type="number"
                  min="0"
                  max="10"
                  step="0.1"
                  value={filters.maxRating}
                  onChange={(e) => handleFilterChange('maxRating', e.target.value)}
                  placeholder="Max"
                  className="flex-1 bg-[#382929] text-white border border-[#4a3a3a] rounded-lg px-3 py-2 focus:outline-none focus:border-[#e9242a]"
                />
              </div>
            </div>

            {/* Age Range */}
            <div>
              <label className="block text-[#b89d9e] font-medium mb-2">
                Age Range
              </label>
              <div className="flex gap-2">
                <input
                  type="number"
                  min="18"
                  max="100"
                  value={filters.minAge}
                  onChange={(e) => handleFilterChange('minAge', e.target.value)}
                  placeholder="Min"
                  className="flex-1 bg-[#382929] text-white border border-[#4a3a3a] rounded-lg px-3 py-2 focus:outline-none focus:border-[#e9242a]"
                />
                <span className="text-[#b89d9e] self-center">to</span>
                <input
                  type="number"
                  min="18"
                  max="100"
                  value={filters.maxAge}
                  onChange={(e) => handleFilterChange('maxAge', e.target.value)}
                  placeholder="Max"
                  className="flex-1 bg-[#382929] text-white border border-[#4a3a3a] rounded-lg px-3 py-2 focus:outline-none focus:border-[#e9242a]"
                />
              </div>
            </div>

            {/* Wrestling Style */}
            <div>
              <label className="block text-[#b89d9e] font-medium mb-2">
                Wrestling Style
              </label>
              <select
                value={filters.wrestlingStyle}
                onChange={(e) => handleFilterChange('wrestlingStyle', e.target.value)}
                className="w-full bg-[#382929] text-white border border-[#4a3a3a] rounded-lg px-4 py-2 focus:outline-none focus:border-[#e9242a]"
              >
                <option value="">All Styles</option>
                {uniqueValues.wrestlingStyles.map(style => (
                  <option key={style} value={style}>{style}</option>
                ))}
              </select>
            </div>

            {/* Hometown */}
            <div>
              <label className="block text-[#b89d9e] font-medium mb-2">
                Hometown
              </label>
              <select
                value={filters.hometown}
                onChange={(e) => handleFilterChange('hometown', e.target.value)}
                className="w-full bg-[#382929] text-white border border-[#4a3a3a] rounded-lg px-4 py-2 focus:outline-none focus:border-[#e9242a]"
              >
                <option value="">All Locations</option>
                {uniqueValues.hometowns.map(hometown => (
                  <option key={hometown} value={hometown}>{hometown}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Results Section */}
        <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-white">
              Search Results
            </h2>
            <div className="text-[#b89d9e]">
              {filteredWrestlers.length} wrestler{filteredWrestlers.length !== 1 ? 's' : ''} found
            </div>
          </div>

          {filteredWrestlers.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-gray-400 text-6xl mb-4">🔍</div>
              <h3 className="text-white text-xl font-semibold mb-2">
                No wrestlers found
              </h3>
              <p className="text-[#b89d9e] mb-4">
                Try adjusting your search criteria or clearing some filters.
              </p>
              <button
                onClick={clearFilters}
                className="bg-[#e9242a] text-white px-6 py-3 rounded-lg hover:bg-[#d11a1a] transition-colors duration-200"
              >
                Clear All Filters
              </button>
            </div>
          ) : (
            <div className="grid gap-6">
              {filteredWrestlers.map((wrestler) => (
                <WrestlerCard key={wrestler.id} wrestler={wrestler} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdvancedSearch;
