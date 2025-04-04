#!/usr/bin/env python3
"""
Example script to read a user's timeline.
"""

import os
import sys
import logging
import argparse
import json
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
    """Fetch and display tweets from a user's timeline."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Read a user's Twitter timeline")
    parser.add_argument("--username", "-u", type=str, help="Twitter username to fetch tweets from")
    parser.add_argument("--count", "-c", type=int, default=10, help="Number of tweets to fetch")
    parser.add_argument("--output", "-o", type=str, help="Output file for JSON results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed tweet information")
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Create client and fetch timeline
    client = TwikitClient()
    
    try:
        # Authenticate
        logger.info("Authenticating...")
        client.login()
        
        # Get username from arguments, environment, or prompt
        username = args.username or os.getenv('TWITTER_USERNAME')
        if not username:
            username = input("Enter Twitter username to fetch: ")
            
        if not username:
            logger.error("No username provided")
            return 1
            
        # Fetch timeline
        logger.info(f"Fetching {args.count} tweets from @{username}'s timeline...")
        tweets = client.get_user_timeline(username=username, count=args.count)
        
        # Display results
        logger.info(f"✅ Successfully fetched {len(tweets)} tweets")
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(tweets, f, indent=2)
            logger.info(f"Saved tweets to {args.output}")
        
        # Print tweets
        for i, tweet in enumerate(tweets, 1):
            if args.verbose:
                # Detailed output
                print(f"\n--- Tweet {i} ---")
                print(f"ID: {tweet.get('id')}")
                print(f"Created at: {tweet.get('created_at')}")
                print(f"Text: {tweet.get('text')}")
                print(f"Likes: {tweet.get('favorite_count', 0)}")
                print(f"Retweets: {tweet.get('retweet_count', 0)}")
            else:
                # Simple output
                print(f"{i}. {tweet.get('text')}")
                
        return 0
        
    except TwitterError as e:
        logger.error(f"❌ Error fetching timeline: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())