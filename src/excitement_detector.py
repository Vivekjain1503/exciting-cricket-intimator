"""
Module to detect exciting moments in cricket matches
"""
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ExcitementDetector:
    """Analyzes match data to detect exciting moments"""
    
    def __init__(self):
        self.previous_state = {}  # Track previous match state to detect changes
        self.excitement_threshold = 0.5  # Threshold for considering a match exciting (0-1)
        
    def is_match_exciting(self, match: Dict) -> Tuple[bool, str, float]:
        """
        Determine if a match is in an exciting phase
        
        Args:
            match: Match data dictionary
            
        Returns:
            Tuple of (is_exciting: bool, reason: str, excitement_score: float)
        """
        excitement_score = 0.0
        reasons = []
        
        # Check if match is live
        if not match.get("live"):
            return False, "Match is not live", 0.0
        
        # Extract score information
        score = match.get("score", [])
        if not score or len(score) < 2:
            return False, "Insufficient score data", 0.0
        
        team1_score = self._parse_score(score[0])
        team2_score = self._parse_score(score[1])
        
        if not team1_score or not team2_score:
            return False, "Could not parse score data", 0.0
        
        # Check for close match
        run_diff = abs(team1_score["runs"] - team2_score["runs"])
        if run_diff <= 20 and team1_score["wickets"] + team2_score["wickets"] >= 3:
            excitement_score += 0.3
            reasons.append("Close match")
        
        # Check for batting team losing wickets quickly
        batting_team = team2_score if team1_score["overs"] > team2_score["overs"] else team1_score
        if batting_team["wickets"] >= 4:
            excitement_score += 0.25
            reasons.append(f"Batting team in trouble ({batting_team['wickets']} wickets down)")
        
        # Check for high scoring rate
        if batting_team["overs"] > 0:
            run_rate = batting_team["runs"] / batting_team["overs"]
            if run_rate > 10:
                excitement_score += 0.2
                reasons.append(f"High scoring rate ({run_rate:.1f} runs/over)")
        
        # Check for last overs (typically exciting)
        batting_team_overs = batting_team["overs"]
        if 18 <= batting_team_overs <= 20:
            excitement_score += 0.15
            reasons.append("Last overs - high tension")
        elif batting_team_overs > 16:
            excitement_score += 0.1
            reasons.append("Death overs approach")
        
        # Check for chasing situation
        if len(score) == 2:
            target = team1_score["runs"]
            current = team2_score["runs"]
            overs_left = max(0, 20 - team2_score["overs"])
            
            if team2_score["overs"] > 0 and overs_left > 0:
                runs_needed = max(0, target - current)
                run_rate_needed = runs_needed / overs_left if overs_left > 0 else float('inf')
                current_rate = team2_score["runs"] / team2_score["overs"] if team2_score["overs"] > 0 else 0
                
                if 0 < runs_needed < 50 and overs_left <= 5:
                    excitement_score += 0.3
                    reasons.append(f"Close finish: {runs_needed} runs needed")
        
        # Cap excitement score at 1.0
        excitement_score = min(excitement_score, 1.0)
        
        is_exciting = excitement_score >= self.excitement_threshold
        reason = " | ".join(reasons) if reasons else "Regular match"
        
        return is_exciting, reason, excitement_score
    
    def detect_major_event(self, current_match: Dict, previous_match: Optional[Dict]) -> Optional[str]:
        """
        Detect major events like wickets or significant score changes
        
        Args:
            current_match: Current match state
            previous_match: Previous match state (can be None for first check)
            
        Returns:
            Event description string or None if no major event
        """
        if not previous_match:
            return None
        
        current_score = current_match.get("score", [])
        previous_score = previous_match.get("score", [])
        
        if not current_score or not previous_score:
            return None
        
        try:
            current_team1 = self._parse_score(current_score[0])
            previous_team1 = self._parse_score(previous_score[0])
            current_team2 = self._parse_score(current_score[1])
            previous_team2 = self._parse_score(previous_score[1])
            
            # Check for wicket loss (team 2 batting)
            if current_team2["wickets"] > previous_team2["wickets"]:
                wickets_lost = current_team2["wickets"] - previous_team2["wickets"]
                return f"⚠️ WICKET! {current_team2['wickets']} wickets down"
            
            # Check for big runs scored
            if current_team2["runs"] - previous_team2["runs"] >= 10:
                runs_scored = current_team2["runs"] - previous_team2["runs"]
                return f"🔥 {runs_scored} runs scored in last over!"
            
            # Check for significant momentum shift
            current_rr = (current_team2["runs"] / current_team2["overs"]) if current_team2["overs"] > 0 else 0
            previous_rr = (previous_team2["runs"] / previous_team2["overs"]) if previous_team2["overs"] > 0 else 0
            
            if previous_rr > 0 and current_rr > previous_rr * 1.5:
                return f"📈 Momentum shift! Run rate: {current_rr:.1f}"
            
        except Exception as e:
            logger.error(f"Error detecting major event: {e}")
        
        return None
    
    def _parse_score(self, score_str: str) -> Optional[Dict]:
        """
        Parse score string into components
        Format: "Runs-Wickets Overs"
        Example: "67-3 10.2"
        
        Args:
            score_str: Score string to parse
            
        Returns:
            Dictionary with runs, wickets, and overs or None if parse fails
        """
        try:
            if not isinstance(score_str, str):
                return None
            
            parts = score_str.strip().split()
            if len(parts) < 2:
                return None
            
            # Parse runs and wickets
            runs_wickets = parts[0].split("-")
            if len(runs_wickets) != 2:
                return None
            
            runs = int(runs_wickets[0].strip())
            wickets = int(runs_wickets[1].strip())
            
            # Parse overs
            overs_parts = parts[1].split(".")
            if len(overs_parts) == 2:
                overs = int(overs_parts[0]) + int(overs_parts[1]) / 6.0
            else:
                overs = float(parts[1])
            
            return {
                "runs": runs,
                "wickets": wickets,
                "overs": overs,
            }
        except (ValueError, IndexError) as e:
            logger.debug(f"Error parsing score '{score_str}': {e}")
            return None
    
    def get_excitement_level(self, excitement_score: float) -> str:
        """
        Get a human-readable excitement level based on score
        
        Args:
            excitement_score: Score from 0 to 1
            
        Returns:
            String describing excitement level
        """
        if excitement_score >= 0.8:
            return "🔥 EXTREME - Must watch!"
        elif excitement_score >= 0.6:
            return "⚡ HIGH - Very exciting"
        elif excitement_score >= 0.4:
            return "📊 MEDIUM - Interesting"
        elif excitement_score >= 0.2:
            return "😐 LOW - Regular match"
        else:
            return "😴 BORING - Not exciting"
