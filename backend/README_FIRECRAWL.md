# Firecrawl Cagematch.net Scraper

This directory contains Python scripts to scrape wrestling data from cagematch.net using the Firecrawl API.

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API key:**
   - Create a `.env` file in the `backend/` directory
   - Add your Firecrawl API key:
     ```
     FIRECRAWL_API_KEY=your_api_key_here
     ```

## Files

- **`test_firecrawl.py`** - Test script to verify your API key and connection
- **`scrape_wrestler.py`** - Simple script to scrape wrestler data
- **`scrape_cagematch.py`** - Comprehensive scraper class with multiple functions

## Quick Start

1. **Test your connection:**
   ```bash
   python test_firecrawl.py
   ```

2. **Search for a wrestler:**
   ```bash
   python scrape_wrestler.py
   ```

## Usage Examples

### Search for a wrestler by name:
```python
from scrape_wrestler import scrape_wrestler

# Search for John Cena
data = scrape_wrestler("John Cena")
```

### Scrape specific wrestler by ID:
```python
from scrape_wrestler import scrape_wrestler

# Scrape wrestler with ID 12345
data = scrape_wrestler("Wrestler Name", "12345")
```

### Use the comprehensive scraper:
```python
from scrape_cagematch import CagematchScraper

scraper = CagematchScraper()

# Search for wrestlers
results = scraper.search_wrestlers("John Cena", limit=5)

# Scrape wrestler profile
profile = scraper.scrape_wrestler_profile("12345")

# Scrape wrestler stats
stats = scraper.scrape_wrestler_stats("12345")

# Crawl wrestling events
events = scraper.crawl_wrestling_events()
```

## Finding Wrestler IDs

To scrape a specific wrestler's profile, you need their ID from cagematch.net:

1. Go to cagematch.net
2. Search for the wrestler
3. Look at the URL - it will contain `&nr=XXXXX` where XXXXX is the wrestler ID
4. Use that ID in the scraper

## Output

All scraped data is saved as JSON files with timestamps:
- `wrestler_john_cena_20241201_143022.json`
- `wrestler_profile.json`
- `wrestling_events.json`

## Data Structure

The scraped data includes:
- **Profile data**: Wrestler information, biography, etc.
- **Statistics**: Match history, win/loss records, etc.
- **Metadata**: Source URLs, timestamps, etc.
- **Markdown content**: Clean, structured content from the website

## Rate Limiting

Firecrawl has rate limits based on your plan. Be mindful of:
- Number of requests per minute
- Total requests per month
- Concurrent crawling jobs

## Troubleshooting

- **API Key Error**: Make sure your `.env` file is in the `backend/` directory
- **Import Error**: Install dependencies with `pip install -r requirements.txt`
- **No Results**: Some searches might not return results - try different search terms
- **Connection Issues**: Check your internet connection and Firecrawl service status

## Next Steps

Once you have the scraped data, you can:
1. Parse the JSON files for specific information
2. Store data in a database
3. Build a wrestling statistics application
4. Create a search interface for wrestling data
