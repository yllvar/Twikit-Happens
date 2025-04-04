#!/usr/bin/env python3
"""
Example script to verify Twitter authentication.
"""

import os
import sys
import logging
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
    """Verify authentication with Twitter."""
    # Load environment variables
    load_dotenv()
    
    # Check if credentials are set
    required_vars = ['TWITTER_USERNAME', 'TWITTER_PASSWORD', 'TWITTER_EMAIL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set them in your .env file")
        return 1
    
    # Create client and attempt authentication
    client = TwikitClient()
    
    try:
        logger.info(f"Attempting to authenticate as {os.getenv('TWITTER_USERNAME')}")
        success = client.login()
        
        if success:
            logger.info("✅ Authentication successful!")
            logger.info(f"Logged in as: {os.getenv('TWITTER_USERNAME')}")
            return 0
        else:
            logger.error("❌ Authentication failed")
            return 1
            
    except TwitterError as e:
        logger.error(f"❌ Authentication error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())