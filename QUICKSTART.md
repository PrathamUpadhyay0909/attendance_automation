# Quick Start Guide - HR Management System

Get your HR bot up and running in 10 minutes!

## ⚡ Prerequisites Checklist

Before you begin, make sure you have:
- [ ] Python 3.9+ installed (`python --version`)
- [ ] MongoDB installed and running (`mongosh` to test)
- [ ] Groq API key (get from [console.groq.com](https://console.groq.com))
- [ ] Telegram bot token (get from [@BotFather](https://t.me/botfather))

## 🚀 5-Minute Setup

### Step 1: Create Project (30 seconds)

```bash
mkdir hr-bot && cd hr-bot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies (2 minutes)

Save all the provided Python files, then:

```bash
pip install python-telegram-bot==20.7 python-dotenv==1.0.0 langchain==0.1.0 langchain-groq==0.0.1 groq==0.4.2 pymongo==4.6.1 pydantic==2.5.3 python-dateutil==2.8.2
```

### Step 3: Configure (1 minute)

Create `.env` file:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=hr_system
GROQ_API_KEY=your_groq_key_here
TELEGRAM_BOT_TOKEN=your_telegram_token_here
```

### Step 4: Seed Database (1 minute)

```bash
python seed_data.py
```

### Step 5: Run! (30 seconds)

```bash
python main.py
```

You should see:
```
HR Management System Starting...
✓ Configuration validated
✓ Database connection successful
Bot is ready to receive messages!
```

## 📱 Test Your Bot

1. Open Telegram
2. Search for your bot name
3. Send `/start`
4. Try these commands:
   - "Show employee john.smith@company.com"
   - "Show Engineering department attendance"
   - "Who was late this week?"

## 🎯 Next Steps

### Link Your Profile

```
/profile
john.smith@company.com
```

Now you can use:
- `/myattendance` - See your attendance
- `/mark` - Mark your attendance
- "Show my attendance"

### Try These Queries

**Simple Queries:**
- "Show all employees in Sales"
- "Mark attendance for [employee-id]"
- "Who was late yesterday?"

**Complex Queries:**
- "Compare attendance between Engineering and Sales"
- "Show me Engineering employees who were late this month"
- "Generate attendance report for Marketing for last 60 days"

## 🐛 Quick Troubleshooting

### Bot not responding?
```bash
# Check if bot is running
ps aux | grep python

# Check logs
tail -f hr_system.log
```

### Database issues?
```bash
# Test MongoDB
mongosh mongodb://localhost:27017

# Re-seed database
python seed_data.py
```

### API issues?
```bash
# Test Groq API
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer YOUR_GROQ_API_KEY"

# Test Telegram token
curl https://api.telegram.org/botYOUR_TOKEN/getMe
```

## 📚 File Structure

```
hr-bot/
├── main.py              # Start here
├── bot.py               # Telegram handlers
├── agent.py             # AI agent
├── tools.py             # Functions
├── database.py          # MongoDB
├── config.py            # Settings
├── seed_data.py         # Test data
├── .env                 # Your secrets
└── requirements.txt     # Dependencies
```

## 💡 Pro Tips

1. **Use Employee IDs**: The 24-character MongoDB IDs work best for queries
2. **Be Specific**: "Show attendance for John in Engineering" is better than "show attendance"
3. **Date References**: Use "this week", "this month", "last 30 days"
4. **Department Names**: Must match exactly - "Engineering" not "engineering"

## 🆘 Common Issues

| Problem | Solution |
|---------|----------|
| "Invalid API key" | Check Groq API key in `.env` |
| "Connection refused" | Start MongoDB: `brew services start mongodb-community` |
| "No module named X" | Reinstall: `pip install -r requirements.txt` |
| Bot doesn't start | Check token with BotFather |
| Slow responses | Lower `AGENT_MAX_ITERATIONS` in `.env` |

## 📞 Need Help?

1. Check the full [README.md](README.md) for detailed docs
2. Review logs in `hr_system.log`
3. Test individual components:
   ```python
   python -c "from database import db_handler; print(db_handler.client)"
   python -c "from tools import search_employee_by_email; print(search_employee_by_email('john.smith@company.com'))"
   ```

## 🎉 You're Ready!

Your HR bot is now running. Start chatting and let the AI handle your HR queries naturally!

**Example Conversation:**
```
You: Hi
Bot: 👋 Welcome to HR Management System! How can I help you today?

You: Show me who works in Engineering
Bot: 👥 Employees in Engineering (3 total):
     1. John Smith - john.smith@company.com
     2. Sarah Johnson - sarah.johnson@company.com
     3. David Wilson - david.wilson@company.com

You: What's their attendance like?
Bot: 📊 I'll get the attendance report for Engineering department...
```

Enjoy your AI-powered HR assistant! 🚀