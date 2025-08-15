import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

interface NewsArticle {
  id: string;
  title: string;
  summary: string;
  fullContent: string;
  url: string;
  published_at: string;
  credibility_score: number;
  source: string;
  tags: string[];
  author?: string;
  readTime?: number;
}

interface NewsFeedProps {
  limit?: number;
  showFilters?: boolean;
  className?: string;
}

const NewsFeed: React.FC<NewsFeedProps> = ({ limit, showFilters = true, className = '' }) => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCredibility, setSelectedCredibility] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('latest');
  const [selectedArticle, setSelectedArticle] = useState<NewsArticle | null>(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = async () => {
    try {
      // Enhanced mock data with full content
      const mockArticles: NewsArticle[] = [
        {
          id: '1',
          title: 'WWE SummerSlam 2025: Major Title Changes Expected',
          summary: 'Sources indicate several championship matches are planned for this year\'s SummerSlam event, with potential surprises in store.',
          fullContent: `The wrestling world is buzzing with anticipation as WWE SummerSlam 2025 approaches. According to multiple sources within the company, several major title changes are expected during this year's flagship event.

The main event is rumored to feature a highly anticipated rematch between current WWE Champion Roman Reigns and challenger Cody Rhodes. Their previous encounter at WrestleMania 41 left fans wanting more, and this SummerSlam showdown promises to deliver an even more intense battle.

In the women's division, the WWE Women's Championship match is expected to be a show-stealer, with current champion Bianca Belair defending against rising star Rhea Ripley. The match has been building for months and could potentially see a new champion crowned.

The tag team division is also set for a shakeup, with multiple teams vying for the WWE Tag Team Championships. The Usos have held the titles for an impressive duration, but their reign may finally come to an end at SummerSlam.

Additionally, sources indicate that several surprise appearances and returns are planned, including the potential return of former WWE superstars who have been absent from television. The event is expected to set new records for attendance and viewership, continuing WWE's recent trend of successful premium live events.

Fans are advised to stay tuned for official announcements and card reveals as the event draws closer.`,
          url: '#',
          published_at: '2025-08-14T10:00:00Z',
          credibility_score: 85,
          source: 'Wrestling Observer',
          tags: ['WWE', 'SummerSlam', 'Championships'],
          author: 'Dave Meltzer',
          readTime: 4
        },
        {
          id: '2',
          title: 'AEW Dynamite Ratings Continue Strong Performance',
          summary: 'All Elite Wrestling\'s flagship show maintains impressive viewership numbers, outperforming expectations.',
          fullContent: `All Elite Wrestling's flagship program, Dynamite, continues to demonstrate remarkable staying power in the competitive Wednesday night television landscape. The latest Nielsen ratings show that AEW Dynamite has maintained consistent viewership numbers, averaging over 800,000 viewers per episode over the past month.

This performance is particularly impressive given the current television climate and the show's position in the Wednesday night "wrestling war" time slot. Industry analysts note that AEW has successfully built a loyal audience base that tunes in week after week, regardless of competing programming.

The success of Dynamite can be attributed to several factors, including the company's commitment to in-ring action, compelling storylines, and the development of homegrown talent. Recent episodes have featured standout performances from wrestlers like MJF, Kenny Omega, and the Young Bucks, all of whom have become household names among wrestling fans.

AEW President Tony Khan has been vocal about the company's growth strategy, emphasizing the importance of creating compelling content that appeals to both hardcore wrestling fans and casual viewers. The company's approach of featuring longer matches and more athletic competition has clearly resonated with audiences.

Looking ahead, AEW has several major events planned that are expected to further boost ratings and viewership. The company's next pay-per-view event is already generating significant buzz, with several high-profile matches announced.

Industry experts predict that AEW's strong performance will continue throughout the remainder of 2025, potentially leading to new television deals and expanded programming opportunities.`,
          url: '#',
          published_at: '2025-08-14T09:30:00Z',
          credibility_score: 92,
          source: 'Sports Business Journal',
          tags: ['AEW', 'Dynamite', 'Ratings'],
          author: 'John Ourand',
          readTime: 3
        },
        {
          id: '3',
          title: 'Former WWE Star Signs with Major Independent Promotion',
          summary: 'A well-known wrestler has reportedly signed a contract with one of the top independent wrestling companies.',
          fullContent: `In a move that has sent shockwaves through the professional wrestling industry, a former WWE superstar has reportedly signed an exclusive contract with one of the top independent wrestling promotions. While the identity of the wrestler has not been officially confirmed, multiple sources indicate that the signing represents a significant coup for the independent wrestling scene.

The wrestler in question is said to have been a prominent figure in WWE for several years, holding multiple championships and participating in numerous high-profile storylines. Their departure from WWE was reportedly amicable, with both parties agreeing that a change of scenery would be beneficial for the wrestler's career.

The independent promotion that secured the signing is known for its innovative approach to professional wrestling, combining traditional sports entertainment with modern storytelling techniques. The company has been aggressively expanding its roster in recent months, signing several high-profile talents from major promotions.

Industry insiders suggest that this signing could signal a broader trend of established wrestlers exploring opportunities outside of the major promotions. The independent wrestling scene has experienced significant growth in recent years, with many companies offering competitive contracts and creative freedom that may not be available elsewhere.

Fans of the wrestler are already expressing excitement about the potential for fresh matchups and storylines. The independent promotion has a reputation for allowing its talent significant creative input, which could lead to some of the most compelling work of the wrestler's career.

The signing is expected to be officially announced within the next week, with the wrestler making their debut for the promotion at an upcoming major event.`,
          url: '#',
          published_at: '2025-08-14T08:45:00Z',
          credibility_score: 78,
          source: 'Pro Wrestling Insider',
          tags: ['Independent', 'Signings', 'WWE Alumni'],
          author: 'Mike Johnson',
          readTime: 4
        },
        {
          id: '4',
          title: 'NJPW Announces International Tour Dates for 2026',
          summary: 'New Japan Pro Wrestling reveals plans for their upcoming international tour, including stops in multiple countries.',
          fullContent: `New Japan Pro Wrestling has officially announced their highly anticipated international tour for 2026, marking the company's most ambitious global expansion effort to date. The tour will include stops in North America, Europe, and Asia, bringing the unique style of Japanese professional wrestling to fans around the world.

The tour will kick off in January 2026 with a series of shows in the United States, including major markets like New York, Los Angeles, and Chicago. These events will feature the full NJPW roster, including current IWGP Heavyweight Champion Kazuchika Okada, Tetsuya Naito, and other top stars.

European fans will have the opportunity to experience NJPW live when the tour visits the United Kingdom, Germany, and France in March and April. This marks the first time that NJPW has held major events in several of these countries, representing a significant expansion of the company's international presence.

The Asian leg of the tour will include stops in Singapore, Thailand, and Australia, further solidifying NJPW's position as the premier wrestling promotion in the Asia-Pacific region. The company has been working closely with local promoters to ensure that these events meet the high standards that fans have come to expect from NJPW.

In addition to the main tour events, NJPW has announced plans for several special "Road to" shows that will serve as warm-up events in smaller markets. These shows will feature up-and-coming talent and provide fans with a more intimate wrestling experience.

The company has also revealed that several major championships will be defended during the tour, with title changes potentially occurring in international markets for the first time in NJPW history. This adds an extra layer of excitement and unpredictability to the tour.

Tickets for the tour are expected to go on sale in the coming months, with pre-sales available to NJPW World subscribers. The company has indicated that they expect strong demand for these events, based on the success of their previous international shows.`,
          url: '#',
          published_at: '2025-08-14T08:00:00Z',
          credibility_score: 88,
          source: 'NJPW Official',
          tags: ['NJPW', 'International', 'Tour'],
          author: 'NJPW Staff',
          readTime: 5
        },
        {
          id: '5',
          title: 'Impact Wrestling Introduces New Championship Division',
          summary: 'Impact Wrestling announces the creation of a new championship division, set to debut at their next major event.',
          fullContent: `Impact Wrestling has made a major announcement that is set to reshape the company's championship landscape. The promotion has revealed plans to introduce a new championship division, which will debut at their upcoming major pay-per-view event.

The new championship will be unlike any other currently in professional wrestling, featuring a unique format that combines elements of traditional wrestling with innovative concepts. While specific details about the championship's design and rules are being kept under wraps, company officials have hinted that it will incorporate elements that have never been seen before in the industry.

The championship tournament will feature sixteen competitors, with qualifying matches taking place over the next several weeks on Impact's weekly television program. The tournament bracket has been designed to create maximum drama and excitement, with several potential dream matches already guaranteed to occur.

Impact Wrestling Executive Vice President Scott D'Amore has been heavily involved in the development of this new championship, working closely with the creative team to ensure that it fits seamlessly into the company's overall vision. D'Amore has stated that this new division represents the next phase of Impact Wrestling's evolution.

The championship will be defended under special rules that are designed to showcase the diverse talents of Impact's roster. The company has been building toward this announcement for several months, with subtle hints and teases being dropped during recent programming.

Fans are already speculating about which wrestlers might be involved in the tournament, with several top names from the Impact roster being mentioned as potential favorites. The company has also hinted that some surprise entrants might participate in the tournament, adding an element of unpredictability.

The championship's debut match is expected to be one of the most talked-about moments in Impact Wrestling history, with the company pulling out all the stops to make it a memorable occasion.`,
          url: '#',
          published_at: '2025-08-14T07:15:00Z',
          credibility_score: 82,
          source: 'Impact Wrestling',
          tags: ['Impact', 'Championships', 'New Division'],
          author: 'Impact Wrestling Staff',
          readTime: 4
        },
        {
          id: '6',
          title: 'Wrestling Hall of Fame Announces 2026 Inductees',
          summary: 'The Professional Wrestling Hall of Fame reveals the first group of inductees for their 2026 ceremony.',
          fullContent: `The Professional Wrestling Hall of Fame has officially announced its 2026 induction class, honoring some of the most influential and beloved figures in professional wrestling history. The announcement was made during a special ceremony at the Hall of Fame's headquarters in Wichita Falls, Texas.

This year's class includes several legendary performers who have left an indelible mark on the industry. Among the inductees are wrestlers who have achieved success in multiple promotions, as well as those who have made significant contributions to the business outside of the ring.

The Modern Era category will see the induction of several wrestlers who have recently retired or are approaching the end of their active careers. These individuals have been selected based on their in-ring accomplishments, their contributions to the industry, and their impact on wrestling culture.

The Legacy category will honor wrestlers from earlier eras whose contributions may have been overlooked in previous years. The Hall of Fame's selection committee has worked diligently to research and recognize these individuals, ensuring that their place in wrestling history is properly acknowledged.

In addition to the wrestler inductees, the Hall of Fame will also honor several non-wrestlers who have made significant contributions to the industry. These include managers, promoters, and other behind-the-scenes figures who have helped shape professional wrestling into what it is today.

The induction ceremony is scheduled to take place in June 2026, with tickets expected to go on sale early next year. The event will feature special presentations for each inductee, including video packages highlighting their careers and contributions to the industry.

The Hall of Fame has also announced plans for several special events leading up to the induction ceremony, including meet-and-greet sessions with current Hall of Fame members and special exhibits showcasing memorabilia from the inductees' careers.

Fans are encouraged to visit the Hall of Fame's website for more information about the inductees and the upcoming ceremony. The organization has stated that this year's class represents one of the most diverse and accomplished groups in the Hall of Fame's history.`,
          url: '#',
          published_at: '2025-08-14T06:30:00Z',
          credibility_score: 95,
          source: 'Hall of Fame Official',
          tags: ['Hall of Fame', 'Inductions', 'Legacy'],
          author: 'Hall of Fame Staff',
          readTime: 5
        }
      ];

      setArticles(mockArticles);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching news:', error);
      setLoading(false);
    }
  };

  const openArticleModal = (article: NewsArticle) => {
    setSelectedArticle(article);
    setShowModal(true);
  };

  const closeArticleModal = () => {
    setShowModal(false);
    setSelectedArticle(null);
  };

  const getCredibilityColor = (score: number) => {
    if (score >= 90) return 'text-green-400 bg-green-400/10 border-green-400/20';
    if (score >= 80) return 'text-blue-400 bg-blue-400/10 border-blue-400/20';
    if (score >= 70) return 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20';
    return 'text-red-400 bg-red-400/10 border-red-400/20';
  };

  const getCredibilityLabel = (score: number) => {
    if (score >= 90) return 'Very High';
    if (score >= 80) return 'High';
    if (score >= 70) return 'Medium';
    return 'Low';
  };

  const filteredArticles = articles
    .filter(article => selectedCredibility === 'all' || 
      (selectedCredibility === 'high' && article.credibility_score >= 80) ||
      (selectedCredibility === 'medium' && article.credibility_score >= 70 && article.credibility_score < 80) ||
      (selectedCredibility === 'low' && article.credibility_score < 70))
    .sort((a, b) => {
      if (sortBy === 'latest') {
        return new Date(b.published_at).getTime() - new Date(a.published_at).getTime();
      } else if (sortBy === 'credibility') {
        return b.credibility_score - a.credibility_score;
      }
      return 0;
    })
    .slice(0, limit || articles.length);

  if (loading) {
    return (
      <div className={`flex items-center justify-center py-12 ${className}`}>
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <>
      <div className={className}>
        {/* Filters */}
        {showFilters && (
          <div className="mb-6 flex flex-wrap gap-4 items-center">
            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium text-gray-300">Credibility:</label>
              <select
                value={selectedCredibility}
                onChange={(e) => setSelectedCredibility(e.target.value)}
                className="bg-white/10 border border-white/20 rounded-md px-3 py-1 text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="all">All</option>
                <option value="high">High (80+)</option>
                <option value="medium">Medium (70-79)</option>
                <option value="low">Low (&lt;70)</option>
              </select>
            </div>
            
            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium text-gray-300">Sort by:</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="bg-white/10 border border-white/20 rounded-md px-3 py-1 text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="latest">Latest</option>
                <option value="credibility">Credibility</option>
              </select>
            </div>
          </div>
        )}

        {/* Articles Grid */}
        <div className="grid gap-6">
          {filteredArticles.map((article) => (
            <article key={article.id} className="group bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10 hover:bg-white/10 transition-all duration-200">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-white group-hover:text-purple-400 transition-colors mb-2">
                    {article.title}
                  </h3>
                  <p className="text-gray-300 mb-3 line-clamp-2">{article.summary}</p>
                  
                  {/* Tags */}
                  <div className="flex flex-wrap gap-2 mb-4">
                    {article.tags.map((tag, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-purple-500/20 text-purple-300 text-xs rounded-full border border-purple-500/30"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  
                  {/* Meta Information */}
                  <div className="flex items-center justify-between text-sm text-gray-400">
                    <div className="flex items-center space-x-4">
                      <span className="flex items-center space-x-1">
                        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                        </svg>
                        <span>{new Date(article.published_at).toLocaleDateString()}</span>
                      </span>
                      <span className="flex items-center space-x-1">
                        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                        </svg>
                        <span>{article.source}</span>
                      </span>
                      {article.author && (
                        <span className="flex items-center space-x-1">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                          </svg>
                          <span>{article.author}</span>
                        </span>
                      )}
                      {article.readTime && (
                        <span className="flex items-center space-x-1">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                          </svg>
                          <span>{article.readTime} min read</span>
                        </span>
                      )}
                    </div>
                    
                    {/* Credibility Score */}
                    <div className={`px-3 py-1 rounded-full border text-xs font-medium ${getCredibilityColor(article.credibility_score)}`}>
                      {getCredibilityLabel(article.credibility_score)} ({article.credibility_score})
                    </div>
                  </div>
                </div>
              </div>
              
              {/* Read More Button */}
              <div className="mt-4">
                <button
                  onClick={() => openArticleModal(article)}
                  className="inline-flex items-center text-purple-400 hover:text-purple-300 text-sm font-medium transition-colors cursor-pointer"
                >
                  Read Full Article
                  <svg className="ml-1 w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </article>
          ))}
        </div>

        {/* No Articles Message */}
        {filteredArticles.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">📰</div>
            <h3 className="text-white text-xl font-semibold mb-2">No News Available</h3>
            <p className="text-gray-400">Try adjusting your filters or check back later for updates.</p>
          </div>
        )}
      </div>

      {/* Article Modal */}
      {showModal && selectedArticle && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-800 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="sticky top-0 bg-slate-800 p-6 border-b border-white/10">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-white">{selectedArticle.title}</h2>
                <button
                  onClick={closeArticleModal}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              {/* Article Meta */}
              <div className="flex items-center space-x-4 mt-4 text-sm text-gray-400">
                <span className="flex items-center space-x-1">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                  </svg>
                  <span>{new Date(selectedArticle.published_at).toLocaleDateString()}</span>
                </span>
                <span className="flex items-center space-x-1">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                  </svg>
                  <span>{selectedArticle.source}</span>
                </span>
                {selectedArticle.author && (
                  <span className="flex items-center space-x-1">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                    </svg>
                    <span>{selectedArticle.author}</span>
                  </span>
                )}
                {selectedArticle.readTime && (
                  <span className="flex items-center space-x-1">
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                    </svg>
                    <span>{selectedArticle.readTime} min read</span>
                  </span>
                )}
              </div>

              {/* Tags */}
              <div className="flex flex-wrap gap-2 mt-4">
                {selectedArticle.tags.map((tag, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-purple-500/20 text-purple-300 text-sm rounded-full border border-purple-500/30"
                  >
                    {tag}
                  </span>
                ))}
              </div>

              {/* Credibility Score */}
              <div className={`inline-block px-3 py-1 rounded-full border text-sm font-medium mt-4 ${getCredibilityColor(selectedArticle.credibility_score)}`}>
                {getCredibilityLabel(selectedArticle.credibility_score)} ({selectedArticle.credibility_score})
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-6">
              <div className="prose prose-invert max-w-none">
                <div className="text-gray-300 leading-relaxed space-y-4">
                  {selectedArticle.fullContent.split('\n\n').map((paragraph, index) => (
                    <p key={index} className="text-base">
                      {paragraph}
                    </p>
                  ))}
                </div>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="sticky bottom-0 bg-slate-800 p-6 border-t border-white/10">
              <div className="flex items-center justify-between">
                <div className="text-sm text-gray-400">
                  Source: {selectedArticle.source}
                </div>
                <button
                  onClick={closeArticleModal}
                  className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg transition-colors"
                >
                  Close Article
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default NewsFeed;
