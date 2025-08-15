from typing import Iterable

import httpx
from bs4 import BeautifulSoup
from dateutil import parser as dateparser


def scrape_wwe_news(index_url: str = "https://www.wwe.com/news") -> Iterable[dict]:
    """
    Fixed WWE scraper with specific selectors to avoid pagination/nav links.
    Uses multiple selector strategies to find actual news article links.
    """
    with httpx.Client(timeout=20.0) as client:
        r = client.get(index_url)
        r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # Strategy 1: Look for main content area and news-specific selectors
    seen_links = set()
    
    # Try multiple selector patterns for WWE news
    selectors = [
        # Look for news card components
        ".news-card a, .article-card a, .story-card a",
        # Look for headline links in main content
        "main h1 a, main h2 a, main h3 a, .main-content h1 a, .main-content h2 a",
        # Look for content areas with article links
        ".content a[href*='/news/'], .news-section a, .articles a",
        # Fallback: article links but exclude common nav patterns
        "article a:not([href*='page']):not([href*='#']):not([class*='nav']):not([class*='pagination'])"
    ]
    
    for selector in selectors:
        try:
            links = soup.select(selector)
            for a in links:
                href = a.get("href")
                title = a.get_text(strip=True)
                
                # Skip obviously bad links
                if not href or not title or len(title) < 10:
                    continue
                    
                # Skip pagination and navigation text
                if any(skip in title.lower() for skip in ["page", "next", "previous", "last", "first", ">>", "<<"]):
                    continue
                    
                # Skip numeric-only titles (pagination)
                if title.isdigit():
                    continue
                    
                # Build full URL
                if href.startswith("/"):
                    link = "https://www.wwe.com" + href
                else:
                    link = href
                    
                # Skip if we've seen this link already
                if link in seen_links:
                    continue
                seen_links.add(link)
                
                # Only process links that look like news articles
                if "/news/" not in link and "/articles/" not in link:
                    continue

                # Extract thumbnail
                thumb = None
                try:
                    with httpx.Client(timeout=8.0, follow_redirects=True) as client:
                        r2 = client.get(link)
                        if r2.status_code == 200:
                            s2 = BeautifulSoup(r2.text, "html.parser")
                            og = s2.find("meta", property="og:image")
                            if og and og.get("content"):
                                thumb = og.get("content")
                            else:
                                # Look for first content image
                                img = s2.select_one("main img, .content img, article img")
                                if img and img.get("src"):
                                    thumb = img.get("src")
                                    if thumb.startswith("/"):
                                        thumb = "https://www.wwe.com" + thumb
                except Exception:
                    thumb = None

                yield {
                    "title": title,
                    "canonical_url": link,
                    "content_snippet": None,
                    "thumbnail_url": thumb,
                    "published_at": None,
                }
                
        except Exception:
            continue


def scrape_pwi(index_url: str = "https://pwi-online.com") -> Iterable[dict]:
    with httpx.Client(timeout=20.0) as client:
        r = client.get(index_url)
        r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.select("article a, h2 a, h3 a"):
        href = a.get("href")
        title = a.get_text(strip=True)
        if not href or not title:
            continue
        if href.startswith("/"):
            link = index_url.rstrip("/") + href
        else:
            link = href
        # Thumbnail discovery
        thumb = None
        try:
            with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                r2 = client.get(link)
                if r2.status_code == 200:
                    s2 = BeautifulSoup(r2.text, "html.parser")
                    og = s2.find("meta", property="og:image")
                    if og and og.get("content"):
                        thumb = og.get("content")
                    else:
                        img = s2.find("img")
                        if img and img.get("src"):
                            thumb = img.get("src")
        except Exception:
            thumb = None

        yield {
            "title": title,
            "canonical_url": link,
            "content_snippet": None,
            "thumbnail_url": thumb,
            "published_at": None,
        }


def scrape_aew(index_url: str = "https://www.allelitewrestling.com/aew-news") -> Iterable[dict]:
    """
    Fixed AEW scraper targeting main news content blocks instead of all links.
    Filters out navigation, footer, and sidebar links.
    """
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        r = client.get(index_url)
        r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    seen_links = set()
    
    # Target news-specific selectors for AEW
    selectors = [
        # Look for news/content card components
        ".news-item a, .article-card a, .post-card a, .story-card a",
        # Look for main content headlines
        "main h1 a, main h2 a, main h3 a, .main-content h1 a, .main-content h2 a, .main-content h3 a",
        # Look for content/news sections
        ".content-area a[href*='news'], .news-section a, .articles a, .posts a",
        # Content blocks that contain articles
        ".entry-title a, .post-title a, .headline a",
        # Fallback: links in main content areas but exclude common nav
        "main a:not([class*='nav']):not([class*='menu']):not([href*='#']):not([class*='footer'])"
    ]
    
    for selector in selectors:
        try:
            links = soup.select(selector)
            for a in links:
                href = a.get("href")
                title = a.get_text(strip=True)
                
                # Skip bad/empty links
                if not href or not title or len(title) < 10:
                    continue
                
                # Skip obvious navigation/footer text
                nav_keywords = ["partners", "press only", "contact", "about", "privacy", "terms", 
                               "menu", "home", "shop", "tickets", "watch", "subscribe", "login"]
                if any(nav in title.lower() for nav in nav_keywords):
                    continue
                
                # Skip short or generic titles
                if len(title) < 10 or title.lower() in ["read more", "learn more", "click here"]:
                    continue
                
                # Build full URL
                if href.startswith("/"):
                    link = "https://www.allelitewrestling.com" + href
                else:
                    link = href
                
                # Skip if seen or doesn't look like news
                if link in seen_links:
                    continue
                seen_links.add(link)
                
                # Only process links that look like news/posts
                if not any(pattern in link.lower() for pattern in ["/news", "/post", "/article", "/story", "/aew-"]):
                    continue

                # Extract thumbnail
                thumb = None
                try:
                    with httpx.Client(timeout=8.0, follow_redirects=True) as client:
                        r2 = client.get(link)
                        if r2.status_code == 200:
                            s2 = BeautifulSoup(r2.text, "html.parser")
                            og = s2.find("meta", property="og:image")
                            if og and og.get("content"):
                                thumb = og.get("content")
                            else:
                                # Look for content images
                                img = s2.select_one("main img, .content img, article img, .post-content img")
                                if img and img.get("src"):
                                    thumb = img.get("src")
                                    if thumb.startswith("/"):
                                        thumb = "https://www.allelitewrestling.com" + thumb
                except Exception:
                    thumb = None

                yield {
                    "title": title,
                    "canonical_url": link,
                    "content_snippet": None,
                    "thumbnail_url": thumb,
                    "published_at": None,
                }
                
        except Exception:
            continue


