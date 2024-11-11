import os
import requests
from dotenv import load_dotenv
from database import Database
import random

class BingAPI:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Set the Bing API key and available categories
        self.api_key = os.getenv("BING_API_KEY")
        self.base_url = 'https://api.bing.microsoft.com/v7.0/news'
        self.categories = [
            "Business", "Entertainment_MovieAndTV", "Entertainment_Music",
            "Politics", "Technology", "Science", "Sports", "US", "World",
            "World_Africa", "World_Americas", "World_Asia", "World_Europe", "World_MiddleEast"
        ]
        self.db = Database()

    def fetch_latest_news(self):
        """Fetch the latest news and skip headlines that are already posted."""
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key
        }

        # Shuffle categories to switch between them randomly
        random.shuffle(self.categories)
        
        for category in self.categories:
            print(f"Fetching news for category: {category}")
            params = {
                'category': category,
                'count': 5,
                'sortBy': 'Date',
                'mkt': 'en-US',
                'freshness': 'Day'
            }

            response = requests.get(self.base_url, headers=headers, params=params)
            if response.status_code == 200:
                articles = response.json().get('value', [])
                for article in articles:
                    headline = article['name']
                    if not self.db.is_headline_used(headline):
                        # Add the new headline to the database and return the article
                        self.db.add_headline(headline)
                        return {
                            'headline': headline,
                            'description': article.get('description', 'No description available'),
                            'url': article['url']
                        }
            else:
                print(f"Error fetching news: {response.status_code}")

        print("No new articles found in any category.")
        return None
