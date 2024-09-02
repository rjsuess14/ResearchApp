import os
from dotenv import load_dotenv
import http.client
import urllib.parse
import json
from datetime import datetime, timedelta

# Actual API key is stored in a .env file.  Not good to store API key directly in script.
load_dotenv()
apikey = os.environ.get("MARKETAUX_KEY")

#Retreive news data from API endpoint
def fetch_news():
    # Calculate the date 30 days ago
    published_window = (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d')

    conn = http.client.HTTPSConnection('api.marketaux.com')

    params = urllib.parse.urlencode({
        'api_token': apikey,
        'symbols': 'AAPL',
        'limit': 3,
        'min_match_score': 10,
        'language':'en',
        'published_after': published_window,
        'filter_entities':'true'
    })

    conn.request('GET', '/v1/news/all?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode('utf-8'))

#Parse through response data and pull out relevant fields
def parse_news(news_data):
    articles = news_data.get('data', [])
    
    for article in articles:
        title = article.get('title')
        description = article.get('description')
        published_at = article.get('published_at')
        url = article.get('url')
        image_url = article.get('image_url')
        
        # Extract sentiment score
        entities = article.get('entities', [])
        sentiment_score = None
        if entities:
            sentiment_score = entities[0].get('sentiment_score')
        
        print(f"Title: {title}")
        print(f"Published at: {published_at}")
        print(f"Description: {description}")
        print(f"Sentiment: {sentiment_score}")
        print(f"URL: {url}")
        print("-" * 50)

if __name__ == "__main__":
    news_data = fetch_news()
    parse_news(news_data)


