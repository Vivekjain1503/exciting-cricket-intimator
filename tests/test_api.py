"""
Test script to fetch and verify live IPL matches from API
Requires: CRICKET_API_KEY in .env file
"""
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from score_fetcher import ScoreFetcher

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def test_api():
    """Test Cricket API connection"""
    api_key = os.getenv('CRICKET_API_KEY')
    
    if not api_key:
        print("❌ ERROR: CRICKET_API_KEY not set in .env file")
        print("   Please get a free key from https://cricapi.com/")
        return False
    
    fetcher = ScoreFetcher()
    fetcher.set_api_key(api_key)
    
    print("Testing Cricket API connection and fetching live matches...\n")
    
    matches = fetcher.get_live_matches()
    
    print(f"Found {len(matches)} live matches\n")
    
    if matches:
        print("✅ API test passed! Live matches found:")
        for i, match in enumerate(matches[:3], 1):
            parsed = fetcher.parse_match_score(match)
            print(f"\n{i}. {parsed['team1']} vs {parsed['team2']}")
            print(f"   Status: {parsed['status']}")
            print(f"   Venue: {parsed['venue']}")
        return True
    else:
        print("⚠️  No live matches found (IPL might not be in season)")
        return True  # Not a failure, just no matches

if __name__ == "__main__":
    result = test_api()
    sys.exit(0 if result else 1)
