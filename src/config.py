"""
Configuration module for IPL Match Tracker
"""
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Cricket API Configuration
CRICKET_API_KEY = os.getenv("CRICKET_API_KEY", "")
if not CRICKET_API_KEY or CRICKET_API_KEY == "your_cricket_api_key_here":
    raise ValueError(
        "CRICKET_API_KEY not configured. Please set it in .env file. "
        "Get a free key from https://cricapi.com/"
    )

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "your_telegram_bot_token_here":
    raise ValueError(
        "TELEGRAM_BOT_TOKEN not configured. Please set it in .env file. "
        "Get a token from @BotFather on Telegram"
    )

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
if not TELEGRAM_CHAT_ID or TELEGRAM_CHAT_ID == "your_chat_id_here":
    raise ValueError(
        "TELEGRAM_CHAT_ID not configured. Please set it in .env file. "
        "Get your chat ID from @userinfobot on Telegram"
    )

# Tracking Configuration
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))
EXCITEMENT_THRESHOLD = float(os.getenv("EXCITEMENT_THRESHOLD", "0.5"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_FILE = os.getenv("LOG_FILE", "logs/cricket_tracker.log")

# Logging Configuration
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

# Setup logging
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)

# Validation
if CHECK_INTERVAL < 30:
    raise ValueError("CHECK_INTERVAL should be at least 30 seconds to avoid rate limiting")

if not 0 <= EXCITEMENT_THRESHOLD <= 1:
    raise ValueError("EXCITEMENT_THRESHOLD should be between 0 and 1")

# Export configuration
__all__ = [
    "CRICKET_API_KEY",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "CHECK_INTERVAL",
    "EXCITEMENT_THRESHOLD",
    "DEBUG",
    "LOG_FILE",
    "LOG_LEVEL",
]
