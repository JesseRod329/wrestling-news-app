import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import apiService from '../services/api';
import { Wrestler, DatabaseStats } from '../types';

interface DashboardStats {
  totalWrestlers: number;
  averageRating: number;
  topRatedWrestler: Wrestler | null;
  ratingDistribution: { range: string; count: number }[];
  promotionBreakdown: { promotion: string; count: number }[];
  ageDistribution: { range: string; count: number }[];
  experienceBreakdown: { experience: string; count: number }[];
  wrestlingStyleBreakdown: { style: string; count: number }[];
  hometownBreakdown: { hometown: string; count: number }[];
}

const StatisticsDashboard: React.FC = () => {
  const [wrestlers, setWrestlers] = useState<Wrestler[]>([]);
  const [databaseStats, setDatabaseStats] = useState<DatabaseStats | null>(null);
  const [dashboardStats, setDashboardStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedWrestler, setSelectedWrestler] = useState<Wrestler | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [wrestlersData, statsData] = await Promise.all([
        apiService.getWrestlers(),
        apiService.getDatabaseStats()
      ]);
      
      setWrestlers(wrestlersData);
      setDatabaseStats(statsData);
      calculateDashboardStats(wrestlersData);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateDashboardStats = (wrestlersData: Wrestler[]) => {
    if (!wrestlersData.length) return;

    // Calculate average rating
    const totalRating = wrestlersData.reduce((sum, w) => {
      const rating = parseFloat(w.averageRating || '0');
      return sum + rating;
    }, 0);
    const averageRating = totalRating / wrestlersData.length;

    // Find top rated wrestler
    const topRated = wrestlersData.reduce((top, current) => {
      const topRating = parseFloat(top.averageRating || '0');
      const currentRating = parseFloat(current.averageRating || '0');
      return currentRating > topRating ? current : top;
    });

    // Rating distribution
    const ratingDistribution = [
      { range: '9.0-10.0', count: 0 },
      { range: '8.0-8.9', count: 0 },
      { range: '7.0-7.9', count: 0 },
      { range: '6.0-6.9', count: 0 },
      { range: '5.0-5.9', count: 0 },
      { range: '0.0-4.9', count: 0 }
    ];

    wrestlersData.forEach(w => {
      const rating = parseFloat(w.averageRating || '0');
      if (rating >= 9.0) ratingDistribution[0].count++;
      else if (rating >= 8.0) ratingDistribution[1].count++;
      else if (rating >= 7.0) ratingDistribution[2].count++;
      else if (rating >= 6.0) ratingDistribution[3].count++;
      else if (rating >= 5.0) ratingDistribution[4].count++;
      else ratingDistribution[5].count++;
    });

    // Promotion breakdown
    const promotionCounts: { [key: string]: number } = {};
    wrestlersData.forEach(w => {
      const promotion = w.promotion || 'Unknown';
      promotionCounts[promotion] = (promotionCounts[promotion] || 0) + 1;
    });
    const promotionBreakdown = Object.entries(promotionCounts)
      .map(([promotion, count]) => ({ promotion, count }))
      .sort((a, b) => b.count - a.count);

    // Age distribution
    const ageDistribution = [
      { range: '18-25', count: 0 },
      { range: '26-35', count: 0 },
      { range: '36-45', count: 0 },
      { range: '46-55', count: 0 },
      { range: '56+', count: 0 }
    ];

    wrestlersData.forEach(w => {
      const age = w.age || 0;
      if (age <= 25) ageDistribution[0].count++;
      else if (age <= 35) ageDistribution[1].count++;
      else if (age <= 45) ageDistribution[2].count++;
      else if (age <= 55) ageDistribution[3].count++;
      else ageDistribution[4].count++;
    });

    // Experience breakdown
    const experienceCounts: { [key: string]: number } = {};
    wrestlersData.forEach(w => {
      const experience = w.experience || 'Unknown';
      experienceCounts[experience] = (experienceCounts[experience] || 0) + 1;
    });
    const experienceBreakdown = Object.entries(experienceCounts)
      .map(([experience, count]) => ({ experience, count }))
      .sort((a, b) => b.count - a.count);

    // Wrestling style breakdown
    const styleCounts: { [key: string]: number } = {};
    wrestlersData.forEach(w => {
      const style = w.wrestlingStyle || 'Unknown';
      styleCounts[style] = (styleCounts[style] || 0) + 1;
    });
    const wrestlingStyleBreakdown = Object.entries(styleCounts)
      .map(([style, count]) => ({ style, count }))
      .sort((a, b) => b.count - a.count);

    // Hometown breakdown
    const hometownCounts: { [key: string]: number } = {};
    wrestlersData.forEach(w => {
      const hometown = w.hometown || 'Unknown';
      hometownCounts[hometown] = (hometownCounts[hometown] || 0) + 1;
    });
    const hometownBreakdown = Object.entries(hometownCounts)
      .map(([hometown, count]) => ({ hometown, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10); // Top 10 hometowns

    setDashboardStats({
      totalWrestlers: wrestlersData.length,
      averageRating: Math.round(averageRating * 100) / 100,
      topRatedWrestler: topRated,
      ratingDistribution,
      promotionBreakdown,
      ageDistribution,
      experienceBreakdown,
      wrestlingStyleBreakdown,
      hometownBreakdown
    });
  };

  const StatCard: React.FC<{ title: string; value: string | number; subtitle?: string; icon: string }> = ({ title, value, subtitle, icon }) => (
    <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-[#b89d9e] text-sm font-medium">{title}</p>
          <p className="text-white text-3xl font-bold">{value}</p>
          {subtitle && <p className="text-[#b89d9e] text-sm mt-1">{subtitle}</p>}
        </div>
        <div className="text-4xl">{icon}</div>
      </div>
    </div>
  );

  const ChartBar: React.FC<{ label: string; value: number; maxValue: number; color: string }> = ({ label, value, maxValue, color }) => (
    <div className="mb-4">
      <div className="flex justify-between text-sm mb-1">
        <span className="text-[#b89d9e]">{label}</span>
        <span className="text-white font-medium">{value}</span>
      </div>
      <div className="w-full bg-[#382929] rounded-full h-3">
        <div
          className={`${color} h-3 rounded-full transition-all duration-300`}
          style={{ width: `${(value / maxValue) * 100}%` }}
        ></div>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#1a1a1a] to-[#2d1b1b] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-[#e9242a] mx-auto mb-4"></div>
          <p className="text-white text-lg">Loading Statistics Dashboard...</p>
        </div>
      </div>
    );
  }

  if (!dashboardStats) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#1a1a1a] to-[#2d1b1b] flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-white text-xl font-bold mb-4">No Data Available</h2>
          <p className="text-gray-300 mb-6">Unable to load statistics data.</p>
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#1a1a1a] to-[#2d1b1b]">
      {/* Header */}
      <div className="bg-[#261c1c] shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white mb-2">
                📊 Statistics Dashboard
              </h1>
              <p className="text-[#b89d9e] text-lg">
                Wrestling Database Analytics & Insights
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
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Wrestlers"
            value={dashboardStats.totalWrestlers}
            icon="👥"
          />
          <StatCard
            title="Average Rating"
            value={`${dashboardStats.averageRating}/10`}
            icon="⭐"
          />
          <StatCard
            title="Top Rated"
            value={dashboardStats.topRatedWrestler?.name || 'N/A'}
            subtitle={`${dashboardStats.topRatedWrestler?.averageRating || 'N/A'}/10`}
            icon="🏆"
          />
          <StatCard
            title="Database Status"
            value="Active"
            subtitle={databaseStats?.scraped_at ? `Updated: ${new Date(databaseStats.scraped_at).toLocaleDateString()}` : ''}
            icon="✅"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Rating Distribution */}
          <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-white mb-4">📈 Rating Distribution</h3>
            {dashboardStats.ratingDistribution.map((item, index) => (
              <ChartBar
                key={index}
                label={item.range}
                value={item.count}
                maxValue={Math.max(...dashboardStats.ratingDistribution.map(r => r.count))}
                color="bg-gradient-to-r from-[#e9242a] to-[#ff6b6b]"
              />
            ))}
          </div>

          {/* Promotion Breakdown */}
          <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-white mb-4">🏢 Promotion Breakdown</h3>
            {dashboardStats.promotionBreakdown.slice(0, 8).map((item, index) => (
              <ChartBar
                key={index}
                label={item.promotion}
                value={item.count}
                maxValue={Math.max(...dashboardStats.promotionBreakdown.map(p => p.count))}
                color="bg-gradient-to-r from-[#4f46e5] to-[#7c3aed]"
              />
            ))}
          </div>

          {/* Age Distribution */}
          <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-white mb-4">🎂 Age Distribution</h3>
            {dashboardStats.ageDistribution.map((item, index) => (
              <ChartBar
                key={index}
                label={item.range}
                value={item.count}
                maxValue={Math.max(...dashboardStats.ageDistribution.map(a => a.count))}
                color="bg-gradient-to-r from-[#059669] to-[#10b981]"
              />
            ))}
          </div>

          {/* Wrestling Style Breakdown */}
          <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-white mb-4">⚡ Wrestling Style Breakdown</h3>
            {dashboardStats.wrestlingStyleBreakdown.slice(0, 8).map((item, index) => (
              <ChartBar
                key={index}
                label={item.style}
                value={item.count}
                maxValue={Math.max(...dashboardStats.wrestlingStyleBreakdown.map(s => s.count))}
                color="bg-gradient-to-r from-[#f59e0b] to-[#fbbf24]"
              />
            ))}
          </div>
        </div>

        {/* Top Hometowns */}
        <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg mt-8">
          <h3 className="text-xl font-bold text-white mb-4">🌍 Top Hometowns</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {dashboardStats.hometownBreakdown.map((item, index) => (
              <div key={index} className="bg-[#382929] rounded-lg p-4">
                <div className="flex justify-between items-center">
                  <span className="text-white font-medium">{item.hometown}</span>
                  <span className="text-[#e9242a] font-bold">{item.count}</span>
                </div>
                <div className="w-full bg-[#1a1a1a] rounded-full h-2 mt-2">
                  <div
                    className="bg-[#e9242a] h-2 rounded-full"
                    style={{ width: `${(item.count / Math.max(...dashboardStats.hometownBreakdown.map(h => h.count))) * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Experience Breakdown */}
        <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg mt-8">
          <h3 className="text-xl font-bold text-white mb-4">⏰ Experience Breakdown</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {dashboardStats.experienceBreakdown.map((item, index) => (
              <div key={index} className="bg-[#382929] rounded-lg p-4">
                <div className="flex justify-between items-center">
                  <span className="text-white font-medium">{item.experience}</span>
                  <span className="text-[#4f46e5] font-bold">{item.count}</span>
                </div>
                <div className="w-full bg-[#1a1a1a] rounded-full h-2 mt-2">
                  <div
                    className="bg-[#4f46e5] h-2 rounded-full"
                    style={{ width: `${(item.count / Math.max(...dashboardStats.experienceBreakdown.map(e => e.count))) * 100}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-[#261c1c] rounded-xl p-6 shadow-lg mt-8">
          <h3 className="text-xl font-bold text-white mb-4">🚀 Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link
              to="/search"
              className="bg-[#e9242a] text-white p-4 rounded-lg text-center hover:bg-[#d11a1a] transition-colors duration-200"
            >
              <div className="text-2xl mb-2">🔍</div>
              <div className="font-semibold">Advanced Search</div>
              <div className="text-sm opacity-80">Find specific wrestlers</div>
            </Link>
            
            <Link
              to="/"
              className="bg-[#4f46e5] text-white p-4 rounded-lg text-center hover:bg-[#4338ca] transition-colors duration-200"
            >
              <div className="text-2xl mb-2">🏠</div>
              <div className="font-semibold">Browse All</div>
              <div className="text-sm opacity-80">View all wrestlers</div>
            </Link>
            
            <button
              onClick={() => window.print()}
              className="bg-[#059669] text-white p-4 rounded-lg text-center hover:bg-[#047857] transition-colors duration-200"
            >
              <div className="text-2xl mb-2">🖨️</div>
              <div className="font-semibold">Export Report</div>
              <div className="text-sm opacity-80">Print or save as PDF</div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatisticsDashboard;
