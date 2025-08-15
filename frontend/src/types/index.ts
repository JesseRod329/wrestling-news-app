export interface Match {
  id: string;
  opponent: string;
  result: 'W' | 'L' | 'D';
  date: string;
  event: string;
  rating?: number;
}

export interface Wrestler {
  id: string;
  name: string;
  nickname?: string;
  realName?: string;
  image: string;
  age: number;
  height: string;
  weight: string;
  hometown: string;
  signatureMoves: string[];
  recentMatches: Match[];
  momentumScore: number;
  careerStats: {
    totalMatches: number;
    wins: number;
    losses: number;
    draws: number;
    winPercentage: number;
  };
  championships: string[];
  bio?: string;
  
  // New backend fields
  promotion?: string;
  brand?: string;
  experience?: string;
  wrestlingStyle?: string;
  averageRating?: string;
  totalVotes?: string;
  yearlyRatings?: Record<string, { rating: string; votes: string }>;
  socialMedia?: Record<string, string>;
  trainers?: string[];
  alterEgos?: string[];
  roles?: string[];
  
  // Image fields
  image_url?: string;
  image_source?: string;
  image_width?: number;
  image_height?: number;
  all_image_urls?: string[];
}

// New interfaces for backend integration
export interface SearchResult {
  wrestler_id: string;
  name: string;
  profile_url: string;
  stats_url: string;
}

export interface DatabaseStats {
  total_wrestlers: number;
  scraped_at: string;
  source: string;
  scraper_version: string;
}

export interface WrestlerProfile {
  wrestler_id: string;
  name: string;
  profile_url: string;
  stats_url: string;
  raw_data: any;
  parsed_data: {
    profile: any;
    statistics: any;
  };
  scraped_at: string;
} 