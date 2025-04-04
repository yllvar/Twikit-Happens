#!/usr/bin/env python3
"""
Example script to post a tweet.
"""

import os
import sys
import logging
import argparse
from dotenv import load_dotenv

# Add the src directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.twikit_happens import TwikitClient, TwitterError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Post a tweet to Twitter."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Post a tweet to Twitter")
    parser.add_argument("--text", "-t", type=str, help="Text content of the tweet")
    parser.add_argument("--reply-to", "-r", type=str, help="Tweet ID to reply to")
    args = parser.parse_args()
    
    # Get tweet text from arguments or prompt
    tweet_text = args.text
    if not tweet_text:
        tweet_text = input("Enter your tweet: ")
        
    if not tweet_text:
        logger.error("No tweet text provided")
        return 1
        
    # Load environment variables
    load_dotenv()
    
    # Create client and attempt to post tweet
    client = TwikitClient()
    
    try:
        # Authenticate
        logger.info("Authenticating...")
        client.login()
        
        # Post the tweet
        logger.info("Posting tweet...")
        tweet_params = {"text": tweet_text}
        
        if args.reply_to:
            tweet_params["reply_to"] = args.reply_to
            logger.info(f"This tweet is a reply to tweet ID: {args.reply_to}")
            
        result = client.post_tweet(**tweet_params)
        
        # Display success message
        logger.info(f"✅ Tweet posted successfully!")
        logger.info(f"Tweet ID: {result.get('id')}")
        logger.info(f"Content: {result.get('text')}")
        return 0
        
    except TwitterError as e:
        logger.error(f"❌ Error posting tweet: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())