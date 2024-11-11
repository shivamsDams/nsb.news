from bing_api import BingAPI
from chatgpt_api import ChatGPTAPI
from threads_api import ThreadsAPI  # Import ThreadsAPI

def format_message(headline, story):
    """Format the message by combining headline and story without specific labels."""
    return f"Breaking News: {headline}\n\n{story}"

def fetch_unique_news(bing_api):
    """Fetch a unique news article from BingAPI."""
    print("Fetching the latest unique news article...")
    return bing_api.fetch_latest_news()

def generate_story(chatgpt_api, news_article):
    """Generate a sarcastic story based on a news article using ChatGPT."""
    prompt = (
        f"Create sarcastic Stort news Title and a short brief of max 6 and 40 words sequncially,based on the following news"
        f"\n'{news_article['headline']}'\n'{news_article['description']}'"
        f"Ensure the combined character count is 400 characters or fewer also include hashtags"
        f"Make sure that news makes sense and humanised"
        f"The tone should be playful, witty to avoid copyright"
    )
    print("Generating a sarcastic story...")
    return chatgpt_api.generate_response(prompt)

def post_to_threads(threads_api, message):
    """Post the formatted message to Meta Threads using ThreadsAPI."""
    container_id = threads_api.create_container(message)
    if container_id:
        threads_api.post_container(container_id)
        print("Posted successfully to Meta Threads.")
        return True
    else:
        print("Failed to create container.")
        return False

def main():
    """Main function to fetch unique news, generate a sarcastic take, and post it."""
    # Initialize the APIs
    bing_api = BingAPI()
    chatgpt_api = ChatGPTAPI()
    threads_api = ThreadsAPI()  # Initialize ThreadsAPI for posting

    try:
        news_article = fetch_unique_news(bing_api)

        if news_article:
            sarcastic_story = generate_story(chatgpt_api, news_article)

            if sarcastic_story:
                # Format the message and check character limit
                message = format_message(news_article['headline'], sarcastic_story)
                
                if len(message) <= 500:
                    print(str(len(message)) + ": Length")
                    success = post_to_threads(threads_api, message)
                    
                    if not success:
                        # Remove headline from database if post failed
                        bing_api.db.delete_headline(news_article['headline'])
                        print("Removed headline from database due to failed post.")
                else:
                    print("Generated content exceeds 500 characters. Skipping post.")
                    # Remove headline if message is too long
                    bing_api.db.delete_headline(news_article['headline'])
                    print(str(len(message)) + ": Length")
                    print("Removed headline from database due to length limit.")
            else:
                print("Failed to generate sarcastic story.")
                # Remove headline if story generation fails
                bing_api.db.delete_headline(news_article['headline'])
                print("Removed headline from database due to failed story generation.")
        else:
            print("No unique news articles available.")
    finally:
        # Ensure the database connection closes regardless of success or failure
        bing_api.db.close()

if __name__ == "__main__":
    main()
