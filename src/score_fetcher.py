"""
Module to fetch live IPL match scores from cricket APIs
"""
import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ScoreFetcher:
    """Fetches live cricket scores from external APIs"""
    
    # IPL series ID - Update this if it changes for different years
    # You can find the current IPL series ID by:
    # 1. Running find_series_id.py script
    # 2. Checking cricapi.com dashboard
    # 3. Or set it via set_series_id() method
    IPL_SERIES_ID = "87c62aac-bc3c-4738-ab93-19da0690488f"
    
    def __init__(self, series_id: str = None):
        # Using CricketData API (free tier available)
        self.api_url = "https://api.cricapi.com/v1"
        # You can get a free API key from https://cricapi.com/
        self.api_key = None  # Will be set from config
        self.series_id = series_id or self.IPL_SERIES_ID  # Use IPL series ID by default
        logger.info(f"ScoreFetcher initialized with series_id: {self.series_id}")
        
    def set_api_key(self, api_key: str):
        """Set the API key for cricket data"""
        self.api_key = api_key
    
    def set_series_id(self, series_id: str):
        """Set the series ID to track (default is IPL)"""
        self.series_id = series_id
        logger.info(f"Series ID set to: {series_id}")
        
    def get_live_matches(self) -> List[Dict]:
        """
        Fetch all live IPL matches
        
        Returns:
            List of match dictionaries with live data
        """
        if not self.api_key:
            logger.error("API key not set. Cannot fetch matches.")
            return []
            
        try:
            params = {
                "apikey": self.api_key,
            }
            response = requests.get(
                f"{self.api_url}/currentMatches",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                # Filter for matches with the specified series ID (IPL)
                ipl_matches = [
                    match for match in data.get("data", [])
                    if match.get("series_id") == self.series_id or 
                       "IPL" in match.get("series", "").upper()  # Fallback to series name
                ]
                return ipl_matches
            else:
                logger.warning("API returned unsuccessful status")
                return []
                
        except requests.RequestException as e:
            logger.error(f"Error fetching live matches: {e}")
            return []
    
    def get_match_details(self, match_id: str) -> Optional[Dict]:
        """
        Fetch detailed information about a specific match
        
        Args:
            match_id: The ID of the match
            
        Returns:
            Dictionary with match details or None if error
        """
        if not self.api_key:
            logger.error("API key not set. Cannot fetch match details.")
            return None
            
        try:
            params = {
                "apikey": self.api_key,
                "id": match_id,
            }
            response = requests.get(
                f"{self.api_url}/matchInfo",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                return data.get("data", {})
            else:
                logger.warning(f"API returned unsuccessful status for match {match_id}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Error fetching match details for {match_id}: {e}")
            return None
    
    def get_series_matches(self, series_name: str = "IPL") -> List[Dict]:
        """
        Fetch all matches for a specific series
        
        Args:
            series_name: Name of the series (default: IPL)
            
        Returns:
            List of match dictionaries
        """
        if not self.api_key:
            logger.error("API key not set. Cannot fetch series matches.")
            return []
            
        try:
            params = {
                "apikey": self.api_key,
            }
            response = requests.get(
                f"{self.api_url}/series",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                series_matches = []
                for series in data.get("data", []):
                    if series_name.lower() in series.get("name", "").lower():
                        series_matches.extend(series.get("matches", []))
                return series_matches
            else:
                logger.warning("API returned unsuccessful status for series")
                return []
                
        except requests.RequestException as e:
            logger.error(f"Error fetching series matches: {e}")
            return []
    
    def get_available_series(self) -> List[Dict]:
        """
        Get all available cricket series
        
        Returns:
            List of series dictionaries with name and ID
        """
        if not self.api_key:
            logger.error("API key not set. Cannot fetch series list.")
            return []
            
        try:
            params = {
                "apikey": self.api_key,
            }
            response = requests.get(
                f"{self.api_url}/series",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                series_list = []
                for series in data.get("data", []):
                    series_list.append({
                        "id": series.get("id"),
                        "name": series.get("name"),
                    })
                return series_list
            else:
                logger.warning("API returned unsuccessful status")
                return []
                
        except requests.RequestException as e:
            logger.error(f"Error fetching series list: {e}")
            return []
    
    def parse_match_score(self, match: Dict) -> Dict:
        """
        Parse and extract key information from match data
        
        Args:
            match: Match dictionary from API
            
        Returns:
            Dictionary with parsed score information
        """
        # Extract team names from score inning information if t1/t2 not available
        team1 = match.get("t1", "Team1")
        team2 = match.get("t2", "Team2")
        
        score = match.get("score", [])
        
        # If score is a list of dicts, extract team names from inning field
        if isinstance(score, list) and len(score) > 0 and isinstance(score[0], dict):
            if "inning" in score[0]:
                team1 = score[0]["inning"].split(" Inning")[0].strip()
            if len(score) > 1 and "inning" in score[1]:
                team2 = score[1]["inning"].split(" Inning")[0].strip()
            
            # Convert dict scores to display format
            score_display = []
            for s in score:
                if isinstance(s, dict):
                    runs = s.get("r", 0)
                    wickets = s.get("w", 0)
                    overs = s.get("o", 0)
                    score_display.append(f"{runs}-{wickets} {overs}")
                else:
                    score_display.append(str(s))
            score = score_display
        
        return {
            "match_id": match.get("id"),
            "team1": team1,
            "team2": team2,
            "status": match.get("status"),
            "score": score,
            "updated_at": datetime.now().isoformat(),
            "venue": match.get("venue", ""),
            "series": match.get("series", ""),
            "live": "live" in match.get("status", "").lower() or 
                   "need" in match.get("status", "").lower() or
                   match.get("matchType") == "t20",
        }
