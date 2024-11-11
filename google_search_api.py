import requests
import openai

# Set up your Google API key and Search Engine ID
google_api_key = 'AIzaSyAwiIZeXZqgoaYntAG8QXNgBKSpVkXF_To'  # Replace with your Google API key
search_engine_id = '35ea20e3687e74aa2'  # Replace with your Custom Search Engine ID
openai.api_key = 'your-openai-api-key'  # Replace with your OpenAI API key

# Google Custom Search API URL
google_url = 'https://www.googleapis.com/customsearch/v1'

def fetch_latest_news(query='top stories'):
    """Fetch the latest headlines and descriptions using Google Custom Search API."""
    params = {
        'key': google_api_key,  # Your API key
        'cx': search_engine_id,  # Your CSE ID
        'q': query,  # Search query (can be 'breaking news' or specific topics)
        'num': 5,  # Number of articles to return
        'fileType': 'news',  # Optional: specify type to limit to news
        'sort': 'date',  # Sort by most recent
    }

    response = requests.get(google_url, params=params)

    if response.status_code == 200:
        articles = response.json()['items']
        # Extract only the headline and description from the response
        news_data = [
            {
                'headline': article['title'],
                'description': article.get('snippet', 'No description available'),
                'url': article['link']  # Full URL to the article
            }
            for article in articles
        ]
        return news_data
    else:
        print(f"Error fetching news: {response.status_code}")
        return []

def generate_sarcastic_story(news_articles):
    """Generate a sarcastic story based on fetched news headlines and descriptions."""
    # Prepare a prompt for GPT-4 using the fetched news data
    news_content = "\n".join([f"Headline: {article['headline']}\nDescription: {article['description']}\n" for article in news_articles])
    
    prompt = f"Create a sarcastic headline and a 100-word story based on the following news headlines and descriptions. The tone should be playful, witty, and critical, with a humorous, exaggerated take on the situation. Write it as if it's for social media.\n\n{news_content}"

    # Call GPT-4 to generate the sarcastic story
    response = openai.Completion.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=200,
        temperature=0.8
    )

    return response.choices[0].text.strip()

def main():
    """Main function to fetch news and generate a sarcastic take."""
    print("Fetching the latest news...")
    news_articles = fetch_latest_news()

    print(news_articles)

    # if news_articles:
    #     print("\nGenerated Sarcastic Story:")
    #     sarcastic_story = generate_sarcastic_story(news_articles)
    #     print(sarcastic_story)

if __name__ == "__main__":
    main()
