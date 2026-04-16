# 🏏 IPL Match Tracker - Telegram Alerts

An intelligent Python application that monitors live IPL cricket match scores and sends real-time Telegram alerts when matches get exciting!

## 🎯 Features

- **Live Match Monitoring**: Continuously tracks all live IPL matches via Cricket API
- **Smart Excitement Detection**: AI-powered analysis to identify exciting moments:
  - Close matches with low run margins
  - Batting team under pressure (4+ wickets down)
  - High scoring rates (>10 runs/over)
  - Death overs and crucial final moments
  - Last-minute winning chases
- **Telegram Notifications**: Instant alerts for:
  - Match start announcements
  - Exciting match moments
  - Wickets and major events
  - Close finish scenarios
  - Match end results
- **Configurable Thresholds**: Customize excitement detection sensitivity
- **Efficient Polling**: Rate-limited API calls to avoid throttling
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Easy Setup**: Simple configuration with .env file

## 📋 Prerequisites

- Python 3.8 or higher
- Telegram account
- Internet connection

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd exciting-cricket-matches-tracker
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Get Your Credentials

#### Cricket API Key (Free)
1. Visit [cricapi.com](https://cricapi.com/)
2. Sign up for a free account
3. Copy your API key from the dashboard
4. Free tier: 300 requests/month (sufficient for monitoring)

#### Telegram Bot Token
1. Open Telegram and search for **@BotFather**
2. Send `/start` then `/newbot`
3. Follow prompts to create bot
4. Copy the bot token (format: `123456789:ABCdefGHIjklmnoPQRstuvWXYZabcd`)

#### Telegram Chat ID
**Option 1: Using @userinfobot**
1. Search for **@userinfobot** on Telegram
2. Send `/start` to get your chat ID

**Option 2: Using the API**
1. Add your bot to a chat or group
2. Send any message
3. Open: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find your chat ID (look for `"id": <number>`)

### 5. Configure Environment

Copy `.env.example` to `.env` and add your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```env
CRICKET_API_KEY=your_actual_api_key_here
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
TELEGRAM_CHAT_ID=your_actual_chat_id_here
CHECK_INTERVAL=60
EXCITEMENT_THRESHOLD=0.5
DEBUG=False
```

**Configuration Options:**
- `CHECK_INTERVAL`: Seconds between API checks (minimum 30, default 60)
- `EXCITEMENT_THRESHOLD`: Excitement sensitivity 0.0-1.0 (default 0.5)
  - Lower = more alerts (0.0 = alert on everything)
  - Higher = fewer alerts (1.0 = only extreme matches)
- `DEBUG`: Enable verbose logging (True/False)

### 6. Run the Tracker

```bash
cd src
python tracker.py
```

You'll see output like:
```
2026-04-16 22:41:26,494 - __main__ - INFO - Starting IPL Match Tracker
2026-04-16 22:41:26,494 - __main__ - INFO - Check interval: 60 seconds
2026-04-16 22:41:26,494 - INFO - Checking for live IPL matches...
```

**The tracker will:**
- Check for live matches every 60 seconds
- Analyze excitement levels
- Send Telegram alerts for exciting moments
- Continue until you press `Ctrl+C`

## 🧪 Testing

### Test Telegram Bot
```bash
python tests/test_telegram.py
```

### Test Cricket API
```bash
python tests/test_api.py
```

### Test Excitement Detection
```bash
python tests/test_excitement.py
```

All tests use credentials from your `.env` file.

## 📊 How It Works

### Excitement Detection Algorithm

The tracker analyzes multiple factors to determine match excitement:

| Factor | Weight | Description |
|--------|--------|-------------|
| Run Difference | 0.3 | Matches with <20 run margin |
| Wicket Pressure | 0.25 | Batting team losing 4+ wickets |
| Scoring Rate | 0.2 | High run rate (>10 per over) |
| Death Overs | 0.15-0.25 | Last overs are inherently exciting |
| Chase Dynamics | 0.3 | Close chase with <50 runs needed |

**Excitement Levels:**
- 🔥 **0.8-1.0**: EXTREME - Must watch!
- ⚡ **0.6-0.8**: HIGH - Very exciting
- 📊 **0.4-0.6**: MEDIUM - Interesting
- 😐 **0.2-0.4**: LOW - Regular match
- 😴 **<0.2**: BORING - Not exciting

### Alert Types

1. **Match Start**: When new IPL match begins
2. **Excitement Alert**: Match reaches excitement threshold
3. **Event Alerts**: Wickets, big runs, momentum shifts
4. **Close Finish**: Thrilling final moments
5. **Match End**: Final result notification

## 📁 Project Structure

```
exciting-cricket-matches-tracker/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── tracker.py               # Main application
│   ├── config.py                # Configuration management
│   ├── score_fetcher.py         # Cricket API integration
│   ├── excitement_detector.py   # Match analysis
│   └── telegram_notifier.py     # Telegram integration
├── tests/
│   ├── test_telegram.py         # Test Telegram bot
│   ├── test_api.py              # Test Cricket API
│   └── test_excitement.py       # Test excitement detection
├── docs/                        # Documentation
├── logs/                        # Application logs
├── .env.example                 # Configuration template
├── .env                         # Your actual credentials (git-ignored)
├── .gitignore                   # Git ignore patterns
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔧 Troubleshooting

### "API key not set" Error
- Ensure `.env` file exists
- Verify `CRICKET_API_KEY` is set correctly
- Key should be from https://cricapi.com/

### No Telegram Alerts Received
- Verify bot token and chat ID are correct
- Ensure bot has permission to send messages
- Check logs: `cat logs/cricket_tracker.log`
- Run: `python tests/test_telegram.py`

### "No live matches found"
- IPL might not be in season (typically March-May)
- Check Cricket API dashboard for available matches
- If you've exceeded free tier, upgrade on cricapi.com

### "ModuleNotFoundError" When Running Tests
- Ensure virtual environment is activated
- Run tests from project root, not from tests/ directory
- Check that `src/` directory exists

## 📝 Logging

Logs are stored in `logs/cricket_tracker.log` and printed to console.

**Enable Debug Logging:**
```env
DEBUG=True
```

**View Logs:**
```bash
# Last 50 lines
tail -50 logs/cricket_tracker.log

# Windows
Get-Content logs/cricket_tracker.log -Tail 50
```

## 🎮 Usage Examples

### Basic Run
```bash
cd src
python tracker.py
```

### More Frequent Checks
```env
# Edit .env
CHECK_INTERVAL=30  # Check every 30 seconds
```

### More Sensitive Alerts
```env
# Edit .env
EXCITEMENT_THRESHOLD=0.3  # Alert on lower excitement
```

### Debug Mode
```env
DEBUG=True
```

## 🔐 Security

⚠️ **IMPORTANT:**
- **Never commit `.env` file** to version control
- `.env.example` contains only placeholders and is safe to commit
- Keep your API keys and bot token confidential
- Don't share your TELEGRAM_CHAT_ID
- Consider rotating credentials periodically

## 📊 API Limits

| Resource | Limit | Note |
|----------|-------|------|
| Cricket API (Free) | 300 req/month | ~10 checks/day during season |
| Telegram Bot | Generous | No practical limit for alerts |
| Check Interval | Minimum 30s | Recommended 60-120s during season |

**Recommended Settings During IPL Season:**
```env
CHECK_INTERVAL=60       # 1 check/minute = ~43k/month
EXCITEMENT_THRESHOLD=0.5  # Balanced alerts
```

## 📚 Resources

- **Cricket API**: https://cricapi.com/ - Get live cricket data
- **Telegram Bot API**: https://core.telegram.org/bots/api - Bot documentation
- **python-telegram-bot**: https://python-telegram-bot.readthedocs.io/ - Python wrapper

## 🤝 Contributing

Contributions welcome! Ideas for improvements:

- [ ] Machine learning-based excitement prediction
- [ ] Multi-language notifications
- [ ] Discord bot integration
- [ ] Player performance tracking
- [ ] Historical match statistics
- [ ] Web dashboard for monitoring
- [ ] Mobile app integration

## 📄 License

MIT License - Feel free to use for personal and commercial projects.

## ⚠️ Disclaimer

This project is for educational and personal use. It's not affiliated with IPL, Telegram, or Cricket APIs. Use responsibly and respect API rate limits and terms of service.

## 🐛 Issues & Support

- Check `logs/cricket_tracker.log` for error messages
- Verify all credentials are correctly set in `.env`
- Run diagnostic tests: `python tests/test_*.py`
- Ensure you have internet connection and firewall isn't blocking APIs

## 🚀 Future Enhancements

- [ ] Support for other cricket leagues (Big Bash, PSL, etc.)
- [ ] Predictive analytics for match outcomes
- [ ] Player and team statistics dashboard
- [ ] Customizable notification rules
- [ ] Multiple telegram chat support
- [ ] WhatsApp and SMS integration
- [ ] Web UI for configuration

---

**Enjoy tracking exciting IPL moments! 🏏🔥**

Made with ❤️ for cricket enthusiasts
