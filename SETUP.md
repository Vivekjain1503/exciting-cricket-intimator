# Detailed Setup Guide

This guide provides step-by-step instructions for setting up the IPL Match Tracker.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Getting Credentials](#getting-credentials)
4. [Configuration](#configuration)
5. [Running Tests](#running-tests)
6. [Starting the Tracker](#starting-the-tracker)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: Minimum 256MB
- **Disk Space**: ~100MB for installation
- **Internet**: Required for API calls

### Check Python Version
```bash
python --version
# Should output Python 3.8.0 or higher
```

If you don't have Python, download from https://www.python.org/

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/exciting-cricket-matches-tracker.git
cd exciting-cricket-matches-tracker
```

### Step 2: Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### Step 3: Upgrade pip
```bash
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- requests - HTTP client
- python-telegram-bot - Telegram API wrapper
- python-dotenv - Environment variable management
- schedule - Job scheduling
- beautifulsoup4 - Web scraping
- lxml - XML/HTML parsing

## Getting Credentials

### Cricket API Key

1. **Visit** https://cricapi.com/
2. **Sign Up** for a free account
3. **Verify** your email
4. **Go to Dashboard** and find "Your API Key"
5. **Copy** the key (looks like: `abc123def456...`)
6. **Free Tier**: 300 requests per month

### Telegram Bot Token

1. **Open Telegram** app or web
2. **Search for** @BotFather
3. **Send** `/start`
4. **Send** `/newbot`
5. **Choose bot name** (e.g., "IPL Match Tracker")
6. **Choose username** (must end with "bot", e.g., "ipl_match_tracker_bot")
7. **Copy** the token you receive (format: `123456789:ABCdefGHIjklmnoPQRstuvWXYZ...`)

### Telegram Chat ID

**Method 1: Using @userinfobot (Easiest)**
1. **Search for** @userinfobot on Telegram
2. **Send** `/start`
3. **You'll see your user ID** (this is your Chat ID)

**Method 2: Using the Bot API**
1. **Add your bot** to a chat or group
2. **Send any message** (e.g., "hi")
3. **Open your browser** and visit:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
   Replace `<YOUR_BOT_TOKEN>` with your actual token
4. **Find Chat ID** - Look for `"id": <number>` in the JSON response
5. **Copy the number** - that's your Chat ID

## Configuration

### Step 1: Create .env File
```bash
cp .env.example .env
```

### Step 2: Edit .env File
Open `.env` in your text editor:

```env
# Cricket API (required)
CRICKET_API_KEY=paste_your_api_key_here

# Telegram (required)
TELEGRAM_BOT_TOKEN=paste_your_bot_token_here
TELEGRAM_CHAT_ID=paste_your_chat_id_here

# Optional Settings
CHECK_INTERVAL=60              # Check every 60 seconds (min: 30)
EXCITEMENT_THRESHOLD=0.5       # 0.0 = most alerts, 1.0 = least alerts
DEBUG=False                    # Set to True for verbose logging
LOG_FILE=logs/cricket_tracker.log
```

### Step 3: Verify Configuration
Ensure no spaces around `=` and values don't have quotes:
```env
# ✅ CORRECT
CRICKET_API_KEY=abc123def456

# ❌ INCORRECT
CRICKET_API_KEY = "abc123def456"
```

### Step 4: Protect Your .env File
The .env file contains sensitive information:
```bash
# Make sure .env is in .gitignore (it should be by default)
# Set permissions on Linux/macOS:
chmod 600 .env
```

## Running Tests

Before running the tracker, test each component:

### Test 1: Telegram Bot Connection
```bash
python tests/test_telegram.py
```

Expected output:
```
Testing Telegram bot connection...
✅ Telegram test passed! Bot is working.
```

### Test 2: Cricket API
```bash
python tests/test_api.py
```

Expected output:
```
Testing Cricket API connection and fetching live matches...
Found X live matches
✅ API test passed! Live matches found:
1. Team1 vs Team2
   Status: ...
```

### Test 3: Excitement Detection
```bash
python tests/test_excitement.py
```

Expected output:
```
TESTING EXCITEMENT DETECTION ALGORITHM
...
✅ All excitement detection tests passed!
```

## Starting the Tracker

### Run the Tracker
```bash
cd src
python tracker.py
```

You should see:
```
2026-04-16 22:41:26 - __main__ - INFO - Starting IPL Match Tracker
2026-04-16 22:41:26 - __main__ - INFO - Check interval: 60 seconds
2026-04-16 22:41:26 - __main__ - INFO - Excitement threshold: 0.5
2026-04-16 22:41:26 - __main__ - INFO - Checking for live IPL matches...
```

### Stop the Tracker
Press `Ctrl+C` in your terminal.

### Run in Background

**Windows:**
```powershell
# Create a batch file: run_tracker.bat
@echo off
cd src
python tracker.py
pause
```

**macOS/Linux:**
```bash
# Create a shell script: run_tracker.sh
#!/bin/bash
cd src
python tracker.py &
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'X'"
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or upgrade pip first
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### "CRICKET_API_KEY not configured"
- Verify `.env` file exists: `ls .env`
- Check API key is set: `CRICKET_API_KEY=your_key_here`
- No spaces around equals sign
- No quotes around the value

### "Telegram test fails"
- Check bot token in `.env`: `TELEGRAM_BOT_TOKEN=...`
- Verify bot token is correct from @BotFather
- Check chat ID in `.env`: `TELEGRAM_CHAT_ID=...`
- Make sure bot is added to your chat/group
- Check internet connection

### "No live matches found"
- This is normal! IPL only runs during season
- Check https://cricapi.com/ for available matches
- Verify API key hasn't exceeded monthly limit
- Try again when IPL season starts

### "Python: command not found" on macOS/Linux
```bash
# Try python3 instead
python3 tracker.py
```

### Port Already in Use
The tracker doesn't use ports, so this shouldn't occur. If it does:
```bash
# Kill any Python processes
pkill -f python  # Linux/macOS
# or manually close other terminals running tracker.py
```

### Still Having Issues?

1. **Check Logs**
   ```bash
   tail logs/cricket_tracker.log  # macOS/Linux
   Get-Content logs/cricket_tracker.log -Tail 50  # Windows
   ```

2. **Run Tests Again**
   ```bash
   python tests/test_telegram.py
   python tests/test_api.py
   ```

3. **Enable Debug Mode**
   - Set `DEBUG=True` in `.env`
   - Run tracker again to see detailed logs

4. **Open GitHub Issue**
   - Include error messages
   - Share relevant logs (remove API keys first!)
   - Describe your setup (OS, Python version, etc.)

## Next Steps

- [Read the README](README.md) for features overview
- [Check the Code](src/) to understand how it works
- [Contributing Guide](CONTRIBUTING.md) to help improve the project
- Star the repo if you found it useful ⭐

---

**Happy tracking! 🏏**
