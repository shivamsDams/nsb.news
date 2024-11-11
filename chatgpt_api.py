import os
import requests
from dotenv import load_dotenv

class ChatGPTAPI:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Set API key from .env
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_response(self, prompt, model="gpt-3.5-turbo"):
        """Generate a response from ChatGPT given a prompt using the requests library."""
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200,
            "temperature": 0.8
        }

        try:
            # Send the POST request to OpenAI's API
            response = requests.post(self.url, headers=self.headers, json=data)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            # Extract and return the response content
            return response.json()['choices'][0]['message']['content']
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return None
