import os
import requests
from dotenv import load_dotenv

class ThreadsAPI:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # API credentials and URLs
        self.app_id = os.getenv("THREADS_APP_ID")
        self.api_secret = os.getenv("THREADS_API_SECRET")
        self.redirect_uri = os.getenv("THREADS_REDIRECT_URI")
        self.scope = os.getenv("THREADS_SCOPE")
        self.auth_url = "https://threads.net/oauth/authorize"
        self.token_url = "https://graph.threads.net/oauth/access_token"
        self.exchange_url = "https://graph.threads.net/access_token"
        self.post_url = "https://graph.threads.net/v1.0/"
        
        # Load tokens and user ID from .env if they exist
        self.authorization_code = os.getenv("THREADS_AUTHORIZATION_CODE")
        self.access_token = os.getenv("THREADS_ACCESS_TOKEN")
        self.user_id = os.getenv("THREADS_USER_ID")
        self.lt_access_token = os.getenv("THREADS_LONG_TERM_ACCESS_TOKEN")

    def update_env_file(self, key, value):
        """Update .env file with unique key-value pairs, enclosed in double quotes."""
        # Load existing .env content
        with open(".env", "r") as env_file:
            lines = env_file.readlines()
        
        # Prepare the new key-value pair
        new_line = f'{key}="{value}"\n'
        found = False

        # Check if the key already exists and update it if found
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = new_line
                found = True
                break

        # If the key wasn't found, append it
        if not found:
            lines.append(new_line)

        # Write back the updated .env content
        with open(".env", "w") as env_file:
            env_file.writelines(lines)

    def generate_authorization_url(self):
        """Generate and print the authorization URL for manual use."""
        url = f"{self.auth_url}?client_id={self.app_id}&redirect_uri={self.redirect_uri}&scope={self.scope}&response_type=code"
        print("Please open this URL in a browser to authorize:")
        print(url)
        print("After authorizing, copy the 'code' parameter from the URL and save it in your .env file as THREADS_AUTHORIZATION_CODE")

    def exchange_authorization_code(self):
        """Exchange authorization code for an access token and retrieve user ID."""
        self.authorization_code = os.getenv("THREADS_AUTHORIZATION_CODE")
        
        if not self.authorization_code:
            print("Authorization code not found. Run generate_authorization_url() to obtain it.")
            return

        data = {
            "client_id": self.app_id,
            "client_secret": self.api_secret,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "code": self.authorization_code
        }
        response = requests.post(self.token_url, data=data)
        if response.status_code == 200:
            json_data = response.json()
            self.access_token = json_data.get("access_token")
            self.user_id = json_data.get("user_id")
            print("Access token and user ID obtained successfully.")

            # Store access token and user ID in .env for future use
            self.update_env_file("THREADS_ACCESS_TOKEN", self.access_token)
            self.update_env_file("THREADS_USER_ID", self.user_id)
        else:
            print("Failed to exchange authorization code.")
            print("Status code:", response.status_code)
            print("Response:", response.text)

    def get_long_term_token(self):
        """Exchange short-lived access token for a long-term token."""
        if not self.access_token:
            print("Access token not found. Run exchange_authorization_code() first.")
            return

        params = {
            "grant_type": "th_exchange_token",
            "client_secret": self.api_secret,
            "access_token": self.access_token
        }
        response = requests.get(self.exchange_url, params=params)
        if response.status_code == 200:
            json_data = response.json()
            self.lt_access_token = json_data.get("access_token")
            print("Long-term access token obtained.")

            # Update .env with the new long-term access token
            self.update_env_file("THREADS_LONG_TERM_ACCESS_TOKEN", self.lt_access_token)
        else:
            print("Failed to obtain long-term access token.")
            print("Status code:", response.status_code)
            print("Response:", response.text)

    def create_container(self, text):
        """Create a container for a new post and return the container ID."""
        # Load the latest long-term access token and user ID
        self.lt_access_token = os.getenv("THREADS_LONG_TERM_ACCESS_TOKEN")
        self.user_id = os.getenv("THREADS_USER_ID")

        # Ensure access_token and user_id are available
        if not self.lt_access_token or not self.user_id:
            print("Access token or user ID not found. Please authenticate and update .env file.")
            return None

        url = f"{self.post_url}{self.user_id}/threads"
        params = {
            "media_type": "TEXT",
            "text": text,
            "access_token": self.lt_access_token
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            json_data = response.json()
            container_id = json_data.get("id")
            print("Container ID obtained:", container_id)
            return container_id
        else:
            print("Failed to create container.")
            print("Status code:", response.status_code)
            print("Response:", response.text)
            return None

    def post_container(self, container_id):
        """Publish a container (post) to Threads."""
        # Load the latest long-term access token and user ID
        self.lt_access_token = os.getenv("THREADS_LONG_TERM_ACCESS_TOKEN")
        self.user_id = os.getenv("THREADS_USER_ID")

        # Ensure access_token and user_id are available
        if not self.lt_access_token or not self.user_id:
            print("Access token or user ID not found. Please authenticate and update .env file.")
            return

        url = f"{self.post_url}{self.user_id}/threads_publish"
        params = {
            "creation_id": container_id,
            "access_token": self.lt_access_token
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            json_data = response.json()
            print("Post published successfully:", json_data)
        else:
            print("Failed to publish post.")
            print("Status code:", response.status_code)
            print("Response:", response.text)

# Example usage:
# threads_api = ThreadsAPI()
# threads_api.generate_authorization_url()  # Run once to get the authorization code
# threads_api.exchange_authorization_code()  # Use saved code to get access token and user ID
# threads_api.get_long_term_token()  # Get long-term token for posting
# container_id = threads_api.create_container("Hello, Threads!")
# threads_api.post_container(container_id)
