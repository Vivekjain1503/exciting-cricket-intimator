"""
Main IPL Match Tracker Script
Monitors live IPL matches and sends Telegram alerts for exciting moments
"""
import asyncio
import logging
import schedule
import time
from typing import Dict, Optional
from datetime import datetime

from score_fetcher import ScoreFetcher
from excitement_detector import ExcitementDetector
from telegram_notifier import TelegramNotifier
from config import (
    CRICKET_API_KEY,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    CHECK_INTERVAL,
    EXCITEMENT_THRESHOLD,
)

logger = logging.getLogger(__name__)


class MatchTracker:
    """Main orchestrator for tracking IPL matches"""
    
    def __init__(self):
        self.fetcher = ScoreFetcher()
        self.fetcher.set_api_key(CRICKET_API_KEY)
        
        self.detector = ExcitementDetector()
        self.detector.excitement_threshold = EXCITEMENT_THRESHOLD
        
        self.notifier = TelegramNotifier(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        
        self.tracked_matches = {}  # Store previous state of matches
        self.running = False
        
    async def check_matches(self):
        """Periodically check for live matches and detect exciting moments"""
        try:
            logger.info("Checking for live IPL matches...")
            
            # Fetch live matches
            matches = self.fetcher.get_live_matches()
            
            if not matches:
                logger.debug("No live matches found")
                return
            
            logger.info(f"Found {len(matches)} live matches")
            
            # Process each match
            for match in matches:
                await self._process_match(match)
                
        except Exception as e:
            logger.error(f"Error checking matches: {e}", exc_info=True)
    
    async def _process_match(self, match: Dict):
        """Process a single match"""
        try:
            match_id = match.get("id")
            if not match_id:
                logger.warning("Match without ID found, skipping")
                return
            
            # Parse match score
            parsed_match = self.fetcher.parse_match_score(match)
            team1 = parsed_match.get("team1", "Team1")
            team2 = parsed_match.get("team2", "Team2")
            match_name = f"{team1} vs {team2}"
            
            # Check if this is a new match
            if match_id not in self.tracked_matches:
                logger.info(f"New match detected: {match_name}")
                self.tracked_matches[match_id] = {
                    "match": parsed_match,
                    "notified_excitement": False,
                    "notified_major_event": set(),
                }
                
                # Send match start alert
                venue = parsed_match.get("venue", "N/A")
                await self.notifier.send_match_start_alert(match_name, venue)
            
            # Detect exciting moments
            is_exciting, reason, excitement_score = self.detector.is_match_exciting(parsed_match)
            
            if is_exciting:
                # Get excitement level description
                excitement_level = self.detector.get_excitement_level(excitement_score)
                score_display = " | ".join(parsed_match.get("score", ["N/A"]))
                
                # Send alert if this is the first exciting notification or excitement level changed
                previous_state = self.tracked_matches[match_id]
                if not previous_state.get("notified_excitement"):
                    logger.info(f"Exciting match detected: {match_name} - {reason}")
                    await self.notifier.send_excitement_alert(
                        match_name,
                        excitement_level,
                        reason,
                        score_display,
                    )
                    previous_state["notified_excitement"] = True
            
            # Detect major events (wickets, big runs)
            previous_match = self.tracked_matches[match_id].get("match")
            major_event = self.detector.detect_major_event(parsed_match, previous_match)
            
            if major_event:
                event_key = f"{match_id}_{major_event}"
                if self.notifier.deduplicate_message(event_key):
                    logger.info(f"Major event in {match_name}: {major_event}")
                    score_display = " | ".join(parsed_match.get("score", ["N/A"]))
                    await self.notifier.send_wicket_alert(match_name, major_event, score_display)
            
            # Check if match has ended
            status = parsed_match.get("status", "").upper()
            if "RESULT" in status or "FINISHED" in status or "COMPLETED" in status:
                if not previous_state.get("notified_end"):
                    logger.info(f"Match ended: {match_name}")
                    score_display = " | ".join(parsed_match.get("score", ["N/A"]))
                    await self.notifier.send_match_end_alert(
                        match_name,
                        status,
                        score_display,
                    )
                    previous_state["notified_end"] = True
                    # Remove from tracked matches after notifying
                    del self.tracked_matches[match_id]
            else:
                # Update tracked state
                self.tracked_matches[match_id]["match"] = parsed_match
            
        except Exception as e:
            logger.error(f"Error processing match: {e}", exc_info=True)
    
    async def run(self):
        """Start the match tracker"""
        logger.info("Starting IPL Match Tracker")
        logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
        logger.info(f"Excitement threshold: {EXCITEMENT_THRESHOLD}")
        
        self.running = True
        
        # Schedule the check task
        schedule.every(CHECK_INTERVAL).seconds.do(self._schedule_check)
        
        try:
            while self.running:
                schedule.run_pending()
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Match tracker stopped by user")
            self.stop()
        except Exception as e:
            logger.error(f"Error in match tracker: {e}", exc_info=True)
    
    def _schedule_check(self):
        """Wrapper for scheduled tasks"""
        asyncio.create_task(self.check_matches())
    
    def stop(self):
        """Stop the tracker"""
        self.running = False
        logger.info("Match tracker stopped")


async def main():
    """Main entry point"""
    tracker = MatchTracker()
    
    # Run initial check
    await tracker.check_matches()
    
    # Start continuous monitoring
    await tracker.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
