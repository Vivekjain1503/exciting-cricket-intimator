"""
Module to send Telegram notifications for exciting cricket moments
"""
import logging
from typing import Optional, List
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Handles sending notifications to Telegram"""
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize Telegram notifier
        
        Args:
            bot_token: Telegram bot token from BotFather
            chat_id: Chat ID where messages should be sent
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = Bot(token=bot_token)
        self.sent_messages = set()  # Track sent messages to avoid duplicates
        
    async def send_notification(self, message: str, parse_mode: str = "HTML") -> bool:
        """
        Send a notification message to Telegram
        
        Args:
            message: Message text to send
            parse_mode: Format for message (HTML, Markdown, etc.)
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=parse_mode,
            )
            logger.info(f"Telegram notification sent: {message[:50]}...")
            return True
        except TelegramError as e:
            logger.error(f"Error sending Telegram notification: {e}")
            return False
    
    async def send_excitement_alert(
        self,
        match_name: str,
        excitement_level: str,
        reason: str,
        current_score: str,
    ) -> bool:
        """
        Send an exciting match alert to Telegram
        
        Args:
            match_name: Name/teams of the match
            excitement_level: Level of excitement (emoji + description)
            reason: Reason why match is exciting
            current_score: Current match score
            
        Returns:
            True if sent successfully
        """
        message = f"""
<b>🏏 IPL MATCH UPDATE</b>

<b>Match:</b> {match_name}
<b>Status:</b> {excitement_level}

<b>Reason:</b> {reason}
<b>Score:</b> {current_score}

⏰ <i>Updated at {__import__('datetime').datetime.now().strftime('%H:%M:%S')}</i>
"""
        return await self.send_notification(message)
    
    async def send_wicket_alert(self, match_name: str, event: str, score: str) -> bool:
        """
        Send a wicket alert
        
        Args:
            match_name: Match teams
            event: Event description
            score: Current score
            
        Returns:
            True if sent successfully
        """
        message = f"""
<b>⚠️ WICKET ALERT!</b>

<b>Match:</b> {match_name}
<b>Event:</b> {event}
<b>Score:</b> {score}

⏰ <i>Updated at {__import__('datetime').datetime.now().strftime('%H:%M:%S')}</i>
"""
        return await self.send_notification(message)
    
    async def send_match_start_alert(self, match_name: str, venue: str) -> bool:
        """
        Send a match start notification
        
        Args:
            match_name: Match teams
            venue: Venue of the match
            
        Returns:
            True if sent successfully
        """
        message = f"""
<b>🎉 IPL MATCH STARTING</b>

<b>Match:</b> {match_name}
<b>Venue:</b> {venue}

Follow for live updates on exciting moments!

⏰ <i>Updated at {__import__('datetime').datetime.now().strftime('%H:%M:%S')}</i>
"""
        return await self.send_notification(message)
    
    async def send_match_end_alert(
        self,
        match_name: str,
        result: str,
        final_score: str,
    ) -> bool:
        """
        Send a match end notification
        
        Args:
            match_name: Match teams
            result: Match result
            final_score: Final score
            
        Returns:
            True if sent successfully
        """
        message = f"""
<b>🏁 MATCH FINISHED</b>

<b>Match:</b> {match_name}
<b>Result:</b> {result}
<b>Final Score:</b> {final_score}

Thanks for following with us!

⏰ <i>Updated at {__import__('datetime').datetime.now().strftime('%H:%M:%S')}</i>
"""
        return await self.send_notification(message)
    
    async def send_close_finish_alert(
        self,
        match_name: str,
        runs_needed: int,
        overs_left: int,
        score: str,
    ) -> bool:
        """
        Send alert for a close match finish
        
        Args:
            match_name: Match teams
            runs_needed: Runs needed to win
            overs_left: Overs remaining
            score: Current score
            
        Returns:
            True if sent successfully
        """
        message = f"""
<b>🔥 CLOSE FINISH!</b>

<b>Match:</b> {match_name}
<b>Runs Needed:</b> {runs_needed}
<b>Overs Left:</b> {overs_left}
<b>Current Score:</b> {score}

This is INTENSE! 🎯

⏰ <i>Updated at {__import__('datetime').datetime.now().strftime('%H:%M:%S')}</i>
"""
        return await self.send_notification(message)
    
    def deduplicate_message(self, message_key: str) -> bool:
        """
        Check if message has already been sent
        
        Args:
            message_key: Unique key for the message
            
        Returns:
            True if this is a new message (not sent before)
        """
        if message_key in self.sent_messages:
            return False
        
        self.sent_messages.add(message_key)
        return True
    
    async def send_batch_alert(self, alerts: List[str]) -> int:
        """
        Send multiple alerts
        
        Args:
            alerts: List of message strings
            
        Returns:
            Number of successfully sent messages
        """
        success_count = 0
        for alert in alerts:
            if await self.send_notification(alert):
                success_count += 1
        return success_count
