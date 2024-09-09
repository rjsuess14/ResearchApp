import os
from dotenv import load_dotenv
import http.client
import urllib.parse
import json
from datetime import datetime, timedelta

# Actual API key is stored in a .env file.  Not good to store API key directly in script.
load_dotenv(dotenv_path='.env', override=True)
apikey = os.environ.get("MARKETAUX_KEY")

# Combine fetching and parsing news data
def get_news(ticker):
    # Fetch news data
    published_window = (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d')
    conn = http.client.HTTPSConnection('api.marketaux.com')
    params = urllib.parse.urlencode({
        'api_token': apikey,
        'symbols': ticker,
        'limit': 3,
        'min_match_score': 10,
        'language':'en',
        'published_after': published_window,
        'filter_entities':'true'
    })
    conn.request('GET', '/v1/news/all?{}'.format(params))
    res = conn.getresponse()
    data = res.read()
    news_data = json.loads(data.decode('utf-8'))

    # Parse news data
    articles = news_data.get('data', [])
    results = []  # Store results for return
    
    for article in articles:
        title = article.get('title')
        description = article.get('description')
        published_at = article.get('published_at')
        url = article.get('url')
        image_url = article.get('image_url')
        
        # Collecting the results
        results.append((title, description, published_at, url, image_url))

    return results  # Return the collected results

