"""
Utility functions for the Twikit Happens package.
"""

import time
import os
import logging
import functools
from typing import Callable, TypeVar, Any, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Type variable for generic function return type
T = TypeVar('T')

class TwitterError(Exception):
    """Custom exception for Twitter-related errors."""
    pass

def handle_rate_limit(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator to automatically retry on rate limits.
    
    Args:
        func: The function to decorate
        
    Returns:
        Wrapped function that handles rate limiting
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> T:
        max_retries = 3
        retry_count = 0
        wait_time = int(os.getenv('RATE_LIMIT_WAIT_TIME', '60'))
        
        while retry_count < max_retries:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_message = str(e).lower()
                
                # Check for rate limit errors
                if any(phrase in error_message for phrase in 
                      ["rate limit", "too many requests", "429"]):
                    retry_count += 1
                    if retry_count >= max_retries:
                        logger.error(f"Rate limit exceeded after {max_retries} retries")
                        raise TwitterError(f"Rate limit exceeded: {str(e)}")
                    
                    # Exponential backoff
                    sleep_time = wait_time * (2 ** (retry_count - 1))
                    logger.warning(f"Rate limit hit - waiting {sleep_time}s (attempt {retry_count}/{max_retries})")
                    time.sleep(sleep_time)
                else:
                    # Not a rate limit error, re-raise
                    raise TwitterError(f"Twitter API error: {str(e)}")
                    
        # This should never be reached due to the raise in the loop
        raise TwitterError("Maximum retries exceeded")
    
    return wrapper

def safe_request(request_func: Callable[[], T], error_message: str) -> T:
    """
    Execute a request function with error handling.
    
    Args:
        request_func: Function that makes the API request
        error_message: Message to include in exception if request fails
        
    Returns:
        The result of the request function
        
    Raises:
        TwitterError: If the request fails
    """
    try:
        return request_func()
    except Exception as e:
        logger.error(f"{error_message}: {str(e)}")
        raise TwitterError(f"{error_message}: {str(e)}")

def create_thread(tweets: list[str], client: Any) -> list[Dict[str, Any]]:
    """
    Post a thread of tweets.
    
    Args:
        tweets: List of tweet texts
        client: Authenticated TwikitClient instance
        
    Returns:
        List of posted tweet objects
        
    Raises:
        TwitterError: If thread creation fails
    """
    if not tweets:
        raise TwitterError("No tweets provided for thread")
    
    results = []
    previous_id = None
    
    for i, tweet_text in enumerate(tweets):
        try:
            if previous_id:
                tweet = client.post_tweet(tweet_text, reply_to=previous_id)
            else:
                tweet = client.post_tweet(tweet_text)
                
            results.append(tweet)
            previous_id = tweet.get("id")
            
            # Small delay between tweets to avoid rapid-fire posting
            if i < len(tweets) - 1:
                time.sleep(2)
                
        except Exception as e:
            logger.error(f"Failed to post tweet {i+1} in thread: {str(e)}")
            raise TwitterError(f"Thread creation failed at tweet {i+1}: {str(e)}")
    
    return results