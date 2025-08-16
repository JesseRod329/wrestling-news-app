import axios from 'axios';
import { Wrestler, WrestlerProfile, SearchResult, DatabaseStats } from '../types';

const API_URL = 'http://localhost:5001/api';

class ApiService {
  // Health check
  async getHealth(): Promise<any> {
    try {
      const response = await axios.get(`${API_URL}/health`);
      return response.data;
    } catch (error) {
      console.error('Error checking API health:', error);
      return null;
    }
  }

  // Get all wrestlers
  async getWrestlers(): Promise<Wrestler[]> {
    try {
      const response = await axios.get(`${API_URL}/wrestlers`);
      return this.transformBackendData(response.data.wrestlers);
    } catch (error) {
      console.error('Error fetching wrestlers:', error);
      return [];
    }
  }

  // Get wrestler by ID
  async getWrestler(id: string): Promise<Wrestler | null> {
    try {
      const response = await axios.get(`${API_URL}/wrestlers/${id}`);
      return this.transformBackendData([response.data])[0] || null;
    } catch (error) {
      console.error(`Error fetching wrestler with id ${id}:`, error);
      return null;
    }
  }

  // Search wrestlers
  async searchWrestlers(query: string): Promise<SearchResult[]> {
    try {
      const response = await axios.get(`${API_URL}/search`, {
        params: { q: query }
      });
      return response.data.results || [];
    } catch (error) {
      console.error('Error searching wrestlers:', error);
      return [];
    }
  }

  // Get wrestler statistics
  async getWrestlerStats(id: string): Promise<any> {
    try {
      const response = await axios.get(`${API_URL}/wrestlers/${id}/stats`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching wrestler stats for id ${id}:`, error);
      return null;
    }
  }

  // Get database statistics
  async getDatabaseStats(): Promise<DatabaseStats | null> {
    try {
      const response = await axios.get(`${API_URL}/stats`);
      const data = response.data;
      
      // Transform backend stats to frontend format
      return {
        total_wrestlers: data.total_wrestlers || 0,
        source: data.database_file || 'Unknown',
        scraper_version: data.average_rating ? `v${data.average_rating}` : 'N/A',
        scraped_at: data.last_updated || new Date().toISOString()
      };
    } catch (error) {
      console.error('Error fetching database stats:', error);
      return null;
    }
  }

  // Transform backend data to frontend format
  private transformBackendData(backendWrestlers: any[]): Wrestler[] {
    return backendWrestlers.map(wrestler => {
      // Handle both old and new data structures
      let profile: any = {};
      let wrestlerId = '';
      
      if (wrestler.parsed_data) {
        // Old format
        profile = wrestler.parsed_data?.profile || {};
        wrestlerId = wrestler.wrestler_id;
      } else {
        // New format - direct fields
        profile = wrestler;
        wrestlerId = wrestler.id || wrestler.cagematch_id;
      }
      
      // Get the best available image
      const imageUrl = this.getBestWrestlerImage(wrestler);
      
      return {
        id: wrestlerId,
        name: wrestler.name,
        nickname: profile.nicknames?.[0] || wrestler.nicknames?.[0] || '',
        realName: wrestler.real_name || wrestler.name,
        image: imageUrl,
        image_url: imageUrl,
        age: profile.age_numeric || parseInt(profile.age) || wrestler.age_numeric || 0,
        height: profile.height || wrestler.height || 'Unknown',
        weight: profile.weight || wrestler.weight || 'Unknown',
        hometown: profile.birthplace || profile.hometown || wrestler.hometown || 'Unknown',
        signatureMoves: profile.signature_moves || wrestler.signature_moves || [],
        recentMatches: [], // Will be populated from stats endpoint
        momentumScore: this.calculateMomentumScore(profile.yearly_ratings || wrestler.yearly_ratings),
        careerStats: {
          totalMatches: 0, // Will be populated from stats endpoint
          wins: 0,
          losses: 0,
          draws: 0,
          winPercentage: 0
        },
        championships: [], // Will be populated from additional data
        bio: this.generateBio(profile, wrestler),
        // Additional backend fields
        promotion: profile.promotion || wrestler.promotion,
        brand: profile.brand || wrestler.brand,
        experience: profile.experience || wrestler.experience,
        wrestlingStyle: profile.wrestling_style || wrestler.wrestling_style,
        averageRating: profile.average_rating || wrestler.averageRating,
        totalVotes: profile.total_votes || wrestler.total_votes,
        yearlyRatings: profile.yearly_ratings || wrestler.yearly_ratings,
        socialMedia: profile.social_media || wrestler.social_media,
        trainers: profile.trainers || wrestler.trainers,
        alterEgos: profile.alter_egos || wrestler.alter_egos,
        roles: profile.roles || wrestler.roles,
        // Image fields from backend
        image_source: wrestler.image_source,
        image_width: wrestler.image_width,
        image_height: wrestler.image_height,
        all_image_urls: wrestler.all_image_urls
      };
    });
  }

  // Get the best available image for a wrestler
  private getBestWrestlerImage(wrestler: any): string {
    // Priority order for images
    if (wrestler.image_url) return wrestler.image_url;
    if (wrestler.all_image_urls && wrestler.all_image_urls.length > 0) return wrestler.all_image_urls[0];
    
    // Try to get image from Cagematch profile
    if (wrestler.profile_url) {
      // Extract wrestler ID from profile URL for potential image
      const match = wrestler.profile_url.match(/nr=(\d+)/);
      if (match) {
        const wrestlerId = match[1];
        return `https://www.cagematch.net/pictures/profile/${wrestlerId}.jpg`;
      }
    }
    
    // Fallback to placeholder with wrestler name
    return this.getWrestlerImage(wrestler.name);
  }

  // Generate placeholder image URL based on wrestler name
  private getWrestlerImage(wrestlerName: string): string {
    // For now, return a placeholder. In production, you'd have actual images
    return `https://via.placeholder.com/400x300/1a1a1a/ffffff?text=${encodeURIComponent(wrestlerName)}`;
  }

  // Calculate momentum score based on recent ratings
  private calculateMomentumScore(yearlyRatings: any): number {
    if (!yearlyRatings) return 0;
    
    const years = Object.keys(yearlyRatings).sort().reverse();
    if (years.length < 2) return 0;
    
    const currentYear = years[0];
    const previousYear = years[1];
    
    const currentRating = parseFloat(yearlyRatings[currentYear]?.rating || '0');
    const previousRating = parseFloat(yearlyRatings[previousYear]?.rating || '0');
    
    return Math.round((currentRating - previousRating) * 100);
  }

  // Generate bio from profile data
  private generateBio(profile: any, wrestler: any): string {
    const parts = [];
    
    // Handle both old and new data structures
    const birthplace = profile.birthplace || profile.hometown || wrestler.hometown;
    const experience = profile.experience || wrestler.experience;
    const wrestlingStyle = profile.wrestling_style || wrestler.wrestling_style;
    const trainers = profile.trainers || wrestler.trainers;
    
    if (birthplace) parts.push(`Born in ${birthplace}`);
    if (experience) parts.push(`Has ${experience} of in-ring experience`);
    if (wrestlingStyle) parts.push(`Known for ${wrestlingStyle} wrestling style`);
    if (trainers?.length) parts.push(`Trained by ${trainers.join(', ')}`);
    
    return parts.join('. ') + '.' || 'Professional wrestler with extensive experience in the industry.';
  }
}

export default new ApiService(); 