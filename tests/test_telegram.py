"""
Test script to verify Telegram bot connection
Requires: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env file
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from telegram_notifier import TelegramNotifier

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

async def test_telegram():
    """Test Telegram bot connection"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set in .env file")
        print("   Please configure .env file first")
        return False
    
    notifier = TelegramNotifier(bot_token, chat_id)
    
    print("Testing Telegram bot connection...")
    success = await notifier.send_notification(
        "<b>✅ Test Message</b>\n\n"
        "Your IPL Match Tracker bot is working correctly!\n"
        f"<i>Sent from test at {__import__('datetime').datetime.now().strftime('%H:%M:%S')}</i>"
    )
    
    if success:
        print("✅ Telegram test passed! Bot is working.")
        return True
    else:
        print("❌ Telegram test failed. Check your credentials.")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_telegram())
    sys.exit(0 if result else 1)
