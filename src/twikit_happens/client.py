"""
Twitter client implementation with authentication handling.
"""

from typing import Optional, Dict, Any, List, Union
import os
import logging
from dotenv import load_dotenv

# This is a placeholder for the actual Twikit library
# Replace with the actual import when using the real library
try:
    from twikit import Client
except ImportError:
    # For development/testing without the actual library
    class Client:
        def __init__(self):
            self.authenticated = False
            
        def login(self, **kwargs):
            self.authenticated = True
            
        def post_tweet(self, text):
            return {"id": "123456", "text": text}
            
        def get_user_timeline(self, username, count=20):
            return [{"id": f"{i}", "text": f"Tweet {i}"} for i in range(count)]

from .utils import handle_rate_limit, TwitterError, safe_request

# Configure logging
logger = logging.getLogger(__name__)

class TwikitClient:
    """
    A wrapper around the Twikit Client that provides additional functionality
    and error handling.
    """
    
    def __init__(self, load_env: bool = True) -> None:
        """
        Initialize the TwikitClient.
        
        Args:
            load_env: Whether to automatically load environment variables from .env
        """
        if load_env:
            load_dotenv()
        
        self.client = Client()
        self._authenticated = False
        self.username = os.getenv('TWITTER_USERNAME')
        self.rate_limit_wait = int(os.getenv('RATE_LIMIT_WAIT_TIME', '60'))
        
    def login(self, username: Optional[str] = None, password: Optional[str] = None, 
              email: Optional[str] = None) -> bool:
        """
        Authenticate using credentials from .env or provided parameters.
        
        Args:
            username: Twitter username (optional if in .env)
            password: Twitter password (optional if in .env)
            email: Twitter email (optional if in .env)
            
        Returns:
            bool: True if authentication was successful
            
        Raises:
            TwitterError: If authentication fails
        """
        try:
            # Use provided credentials or fall back to .env
            username = username or os.getenv('TWITTER_USERNAME')
            password = password or os.getenv('TWITTER_PASSWORD')
            email = email or os.getenv('TWITTER_EMAIL')
            
            if not all([username, password, email]):
                raise TwitterError("Missing authentication credentials. "
                                  "Provide them as parameters or in .env file.")
            
            logger.info(f"Authenticating as {username}")
            
            # Perform the actual authentication
            self.client.login(
                auth_info_1=username,
                auth_info_2=password,
                auth_info_3=email
            )
            
            self._authenticated = True
            logger.info("Authentication successful")
            return True
            
        except Exception as e:
            self._authenticated = False
            logger.error(f"Authentication failed: {str(e)}")
            raise TwitterError(f"Authentication failed: {str(e)}")
    
    @property
    def is_authenticated(self) -> bool:
        """Check if the client is authenticated."""
        return self._authenticated
    
    def _ensure_authenticated(self) -> None:
        """Ensure the client is authenticated before making requests."""
        if not self._authenticated:
            raise TwitterError("Not authenticated. Call login() first.")
    
    @handle_rate_limit
    def post_tweet(self, text: str, media_ids: Optional[List[str]] = None, 
                  reply_to: Optional[str] = None) -> Dict[str, Any]:
        """
        Post a tweet to Twitter.
        
        Args:
            text: The text content of the tweet
            media_ids: Optional list of media IDs to attach
            reply_to: Optional tweet ID to reply to
            
        Returns:
            Dict containing the posted tweet data
            
        Raises:
            TwitterError: If posting fails
        """
        self._ensure_authenticated()
        
        params = {"text": text}
        if media_ids:
            params["media_ids"] = media_ids
        if reply_to:
            params["reply_to"] = reply_to
            
        return safe_request(
            lambda: self.client.post_tweet(**params),
            "Failed to post tweet"
        )
    
    @handle_rate_limit
    def get_user_timeline(self, username: Optional[str] = None, 
                         count: int = 20) -> List[Dict[str, Any]]:
        """
        Get tweets from a user's timeline.
        
        Args:
            username: The username to fetch tweets from (defaults to authenticated user)
            count: Number of tweets to retrieve
            
        Returns:
            List of tweet objects
            
        Raises:
            TwitterError: If retrieval fails
        """
        self._ensure_authenticated()
        
        username = username or self.username
        if not username:
            raise TwitterError("No username provided or found in environment")
            
        return safe_request(
            lambda: self.client.get_user_timeline(username=username, count=count),
            f"Failed to get timeline for user {username}"
        )
    
    @handle_rate_limit
    def search_tweets(self, query: str, count: int = 100) -> List[Dict[str, Any]]:
        """
        Search for tweets matching a query.
        
        Args:
            query: Search query string
            count: Maximum number of results
            
        Returns:
            List of matching tweet objects
            
        Raises:
            TwitterError: If search fails
        """
        self._ensure_authenticated()
        
        return safe_request(
            lambda: self.client.search_tweets(query=query, count=count),
            f"Failed to search tweets with query: {query}"
        )