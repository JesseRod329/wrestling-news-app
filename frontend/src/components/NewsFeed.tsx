import React, { useEffect, useMemo, useState } from 'react';

type Article = {
  id: number | string;
  title: string;
  canonical_url?: string | null;
  content_snippet?: string | null;
  thumbnail_url?: string | null;
  published_at?: string | null;
  credibility_score?: number | null;
  credibility_tag?: string | null;
  source_name?: string | null;
  upvotes?: number;
  downvotes?: number;
};

const API_BASE = (process.env.REACT_APP_NEWS_API || 'http://localhost:8000').replace(/\/$/, '');

// Add this function to clean HTML tags
const stripHtml = (html: string | null): string => {
  if (!html) return '';
  // Remove HTML tags and decode HTML entities
  return html
    .replace(/<[^>]*>/g, '') // Remove HTML tags
    .replace(/&amp;/g, '&') // Decode common HTML entities
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .trim();
};

const credibilityBadge = (score?: number | null, tag?: string | null) => {
  if (score == null && !tag) return 'Unknown';
  if (tag) return tag;
  if (score! >= 0.7) return 'Confirmed';
  if (score! >= 0.3) return 'Developing';
  return 'Rumor';
};

const formatDate = (iso?: string | null) => {
  if (!iso) return '';
  try {
    const d = new Date(iso);
    return d.toLocaleString();
  } catch { return ''; }
};

const NewsFeed: React.FC = () => {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState('');
  const [filterCred, setFilterCred] = useState<'all' | 'confirmed' | 'developing' | 'rumor'>('all');

  useEffect(() => {
    const run = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE}/articles?limit=50&sort=latest`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setArticles(Array.isArray(data) ? data : []);
      } catch (e:any) {
        setError(e?.message || 'Failed to load news');
      } finally {
        setLoading(false);
      }
    };
    run();
  }, []);

  const filtered = useMemo(() => {
    let list = articles;
    if (query.trim()) {
      const q = query.toLowerCase();
      list = list.filter(a =>
        (a.title || '').toLowerCase().includes(q) ||
        (a.content_snippet || '').toLowerCase().includes(q) ||
        (a.source_name || '').toLowerCase().includes(q)
      );
    }
    if (filterCred !== 'all') {
      list = list.filter(a => {
        const tag = credibilityBadge(a.credibility_score ?? null, a.credibility_tag ?? undefined).toLowerCase();
        return tag.includes(filterCred);
      });
    }
    return list.slice().sort((a,b) => {
      const ad = a.published_at ? Date.parse(a.published_at) : 0;
      const bd = b.published_at ? Date.parse(b.published_at) : 0;
      return bd - ad;
    });
  }, [articles, query, filterCred]);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-6">
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search headlines, sources…"
          className="w-full sm:w-2/3 rounded-xl bg-white/5 border border-white/10 px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring focus:ring-purple-500/40"
        />
        <select
          value={filterCred}
          onChange={e => setFilterCred(e.target.value as any)}
          className="rounded-xl bg-white/5 border border-white/10 px-3 py-2 text-white focus:outline-none focus:ring focus:ring-purple-500/40"
        >
          <option value="all">All credibility</option>
          <option value="confirmed">Confirmed</option>
          <option value="developing">Developing</option>
          <option value="rumor">Rumor</option>
        </select>
      </div>

      {loading && <div className="text-center text-gray-300">Loading latest articles…</div>}
      {error && <div className="text-center text-red-400">Error: {error}</div>}

      <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {filtered.map(a => (
          <li key={a.id} className="rounded-2xl overflow-hidden bg-white/5 border border-white/10 hover:border-white/20 transition">
            {a.thumbnail_url ? (
              <a href={a.canonical_url || '#'} target="_blank" rel="noreferrer">
                <img
                  src={a.thumbnail_url}
                  alt={a.title || 'thumbnail'}
                  className="w-full h-40 object-cover"
                  loading="lazy"
                />
              </a>
            ) : null}
            <div className="p-4 space-y-2">
              <div className="flex items-center justify-between text-xs text-gray-300">
                <span className="truncate">{a.source_name || 'Unknown source'}</span>
                <span>{formatDate(a.published_at)}</span>
              </div>
              <a
                href={a.canonical_url || '#'}
                target="_blank"
                rel="noreferrer"
                className="block font-semibold text-white hover:underline leading-tight"
              >
                {a.title}
              </a>
              {a.content_snippet ? (
                <p className="text-sm text-gray-300 line-clamp-3">
                  {stripHtml(a.content_snippet)}
                </p>
              ) : null}
              <div className="flex items-center justify-between pt-1">
                <span className="text-xs px-2 py-1 rounded-full bg-white/10 border border-white/10">
                  {credibilityBadge(a.credibility_score ?? null, a.credibility_tag ?? undefined)}
                </span>
                <span className="text-xs text-gray-300">
                  ▲{a.upvotes ?? 0} ▼{a.downvotes ?? 0}
                </span>
              </div>
            </div>
          </li>
        ))}
      </ul>

      {!loading && filtered.length === 0 && (
        <div className="text-center text-gray-300">No articles found.</div>
      )}
    </div>
  );
};

export default NewsFeed;