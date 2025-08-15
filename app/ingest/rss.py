from datetime import datetime
from typing import Iterable

import feedparser
from dateutil import parser as dateparser
import httpx
from bs4 import BeautifulSoup


def parse_rss(feed_url: str) -> Iterable[dict]:
    """
    Enhanced RSS parser with better error handling and debugging.
    """
    try:
        # Add user agent to avoid blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Parse with custom headers
        feed = feedparser.parse(feed_url, request_headers=headers)
        
        # Debug: check if feed loaded successfully
        if hasattr(feed, 'status') and feed.status >= 400:
            print(f"RSS feed error for {feed_url}: HTTP {feed.status}")
            return
            
        if not feed.entries:
            print(f"No entries found in RSS feed: {feed_url}")
            return
            
        print(f"Successfully parsed {len(feed.entries)} entries from {feed_url}")
        
    except Exception as e:
        print(f"Error parsing RSS feed {feed_url}: {e}")
        return
        
    for e in feed.entries:
        published_at = None
        if getattr(e, "published", None):
            try:
                published_at = dateparser.parse(e.published)
            except Exception:
                published_at = None
        # Attempt media content
        thumb = None
        media = getattr(e, "media_content", None) or getattr(e, "media_thumbnail", None)
        if media:
            try:
                if isinstance(media, list) and media:
                    thumb = media[0].get("url")
                elif isinstance(media, dict):
                    thumb = media.get("url")
            except Exception:
                thumb = None

        # Fallback to og:image
        if not thumb and getattr(e, "link", None):
            try:
                with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                    r = client.get(e.link)
                    if r.status_code == 200:
                        soup = BeautifulSoup(r.text, "html.parser")
                        og = soup.find("meta", property="og:image")
                        if og and og.get("content"):
                            thumb = og.get("content")
                        else:
                            img = soup.find("img")
                            if img and img.get("src"):
                                thumb = img.get("src")
            except Exception:
                thumb = None

        yield {
            "title": getattr(e, "title", None) or "",
            "canonical_url": getattr(e, "link", None) or "",
            "content_snippet": getattr(e, "summary", None) or None,
            "published_at": published_at,
            "thumbnail_url": thumb,
        }


