# HR Management System

An AI-powered HR Management System using LangChain, Groq API, MongoDB, and Telegram Bot for natural language interaction with HR data.

## 🌟 Features

### Core Capabilities
- **Natural Language Queries**: Ask questions in plain English
- **Employee Management**: Search and view employee information
- **Attendance Tracking**: Mark and monitor attendance records
- **Department Analytics**: Generate comprehensive reports
- **Multi-step Reasoning**: Handle complex queries intelligently
- **Context Awareness**: Remember conversation history
- **Interactive Interface**: User-friendly Telegram bot with inline keyboards

### Technical Features
- **LangChain ReAct Agent**: Intelligent reasoning and action
- **Groq API Integration**: Fast LLM inference with llama-3.3-70b
- **MongoDB Database**: Scalable document storage
- **Production-Ready**: Comprehensive error handling and logging
- **Modular Architecture**: Easy to extend and maintain

## 📋 Table of Contents

- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Database Setup](#-database-setup)
- [Running the Application](#-running-the-application)
- [Usage Examples](#-usage-examples)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [API Documentation](#-api-documentation)

## 🏗️ Architecture

```
┌─────────────────┐
│  Telegram Bot   │  ← User Interface
└────────┬────────┘
         │
┌────────▼────────┐
│  Agent Executor │  ← LangChain ReAct Agent
└────────┬────────┘
         │
    ┌────┼─────┐
    │    │     │
┌───▼┐ ┌─▼──┐ ┌▼────┐
│Tool│ │Tool│ │Tool │  ← Specialized Functions
└───┬┘ └─┬──┘ └┬────┘
    │    │     │
    └────┼─────┘
         │
┌────────▼────────┐
│    MongoDB      │  ← Data Layer
└─────────────────┘
```

### Components

1. **Telegram Bot** (`bot.py`): Handles user interactions
2. **LangChain Agent** (`agent.py`): Processes queries and orchestrates tools
3. **Tools** (`tools.py`): Specific operations (search, attendance, reports)
4. **Database Handler** (`database.py`): MongoDB operations
5. **Configuration** (`config.py`): Environment and settings management

## 🔧 Prerequisites

### Required Software
- **Python**: 3.9 or higher
- **MongoDB**: 4.4 or higher (local or MongoDB Atlas)
- **Telegram Bot Token**: From [@BotFather](https://t.me/botfather)
- **Groq API Key**: From [Groq Console](https://console.groq.com)

### System Requirements
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 500MB for application and dependencies
- **Network**: Internet connection for API calls

## 📦 Installation

### Step 1: Clone or Create Project Directory

```bash
mkdir hr-management-system
cd hr-management-system
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -c "import langchain; import pymongo; import telegram; print('All packages installed successfully!')"
```

## ⚙️ Configuration

### Step 1: Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

### Step 2: Configure Environment Variables

Edit `.env` file with your actual credentials:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=hr_system

# Groq API Configuration
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather

# Agent Configuration (Optional - defaults shown)
AGENT_MAX_ITERATIONS=10
AGENT_TEMPERATURE=0.1
LOG_LEVEL=INFO
```

### Getting Required Credentials

#### 1. Groq API Key
1. Visit [Groq Console](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste into `.env`

#### 2. Telegram Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the token provided
5. Paste into `.env`

#### 3. MongoDB Setup

**Option A: Local MongoDB**
```bash
# Install MongoDB locally
# On macOS:
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB
brew services start mongodb-community

# Use default URI:
MONGODB_URI=mongodb://localhost:27017
```

**Option B: MongoDB Atlas (Cloud)**
1. Visit [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user
4. Whitelist your IP (or use 0.0.0.0/0 for development)
5. Get connection string
6. Update `.env`:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

## 🗄️ Database Setup

### Step 1: Start MongoDB

```bash
# If using local MongoDB
mongosh  # Connect to MongoDB shell
```

### Step 2: Create Database and Import Sample Data

Create a file `seed_data.py`:

```python
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
import random

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["hr_system"]

# Clear existing data
db.users.delete_many({})
db.attendances.delete_many({})

# Sample users
sample_users = [
    {
        "_id": ObjectId(),
        "name": "John Smith",
        "email": "john.smith@company.com",
        "password": "hashed_password",
        "role": "employee",
        "designation": "Engineering",
        "phone": "+1234567890",
        "dateOfJoining": "2023-01-15",
        "dateOfBirth": "1990-05-20",
        "bloodGroup": "A+",
        "isDisabled": False,
        "isDeleted": False,
        "isWorkFromHome": False,
        "emergencyContactNumber": "+1234567899",
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
        "__v": 0
    },
    {
        "_id": ObjectId(),
        "name": "Sarah Johnson",
        "email": "sarah.johnson@company.com",
        "password": "hashed_password",
        "role": "employee",
        "designation": "Engineering",
        "phone": "+1234567891",
        "dateOfJoining": "2023-02-01",
        "dateOfBirth": "1992-08-15",
        "bloodGroup": "B+",
        "isDisabled": False,
        "isDeleted": False,
        "isWorkFromHome": False,
        "emergencyContactNumber": "+1234567892",
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
        "__v": 0
    },
    {
        "_id": ObjectId(),
        "name": "Michael Chen",
        "email": "michael.chen@company.com",
        "password": "hashed_password",
        "role": "employee",
        "designation": "Sales",
        "phone": "+1234567893",
        "dateOfJoining": "2023-03-10",
        "dateOfBirth": "1988-12-05",
        "bloodGroup": "O+",
        "isDisabled": False,
        "isDeleted": False,
        "isWorkFromHome": False,
        "emergencyContactNumber": "+1234567894",
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
        "__v": 0
    }
]

# Insert users
db.users.insert_many(sample_users)
print(f"Inserted {len(sample_users)} users")

# Generate attendance records for last 30 days
for user in sample_users:
    for days_ago in range(30):
        date = datetime.now() - timedelta(days=days_ago)
        
        # 90% attendance rate
        if random.random() < 0.9:
            # Random punch-in time between 08:00 and 10:30
            punch_in_hour = random.randint(8, 10)
            punch_in_minute = random.randint(0, 59) if punch_in_hour < 10 else random.randint(0, 30)
            
            # Determine status
            status = "Late" if (punch_in_hour > 9 or (punch_in_hour == 9 and punch_in_minute > 30)) else "Present"
            
            # Random work hours between 7-10
            work_hours = round(random.uniform(7, 10), 2)
            
            attendance = {
                "_id": ObjectId(),
                "userId": user["_id"],
                "date": date.replace(hour=0, minute=0, second=0, microsecond=0),
                "punchIn": f"{punch_in_hour:02d}:{punch_in_minute:02d}",
                "punchOut": None,
                "status": status,
                "totalWorkingHours": work_hours,
                "punchInLocation": {
                    "type": "Point",
                    "coordinates": [72.8311, 18.9200]  # Sample coordinates
                },
                "punchOutLocation": {
                    "type": "Point",
                    "coordinates": [72.8311, 18.9200]
                },
                "areaRestriction": {
                    "type": "Point",
                    "coordinates": [72.8311, 18.9200],
                    "radius": 500
                },
                "organization": None,
                "isWorkFromHome": user.get("isWorkFromHome", False),
                "createdAt": date,
                "updatedAt": date,
                "__v": 0
            }
            
            db.attendances.insert_one(attendance)

print("Sample data inserted successfully!")
print(f"Total users: {db.users.count_documents({})}")
print(f"Total attendance records: {db.attendances.count_documents({})}")

# Print sample user IDs for testing
print("\nSample Employee IDs for testing:")
for user in db.users.find().limit(3):
    print(f"- {user['name']}: {user['_id']}")

client.close()
```

Run the seed script:

```bash
python seed_data.py
```

## 🚀 Running the Application

### Development Mode

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the application
python main.py
```

You should see output like:

```
============================================================
HR Management System Starting...
============================================================
2025-01-21 10:00:00 - __main__ - INFO - Validating environment configuration...
2025-01-21 10:00:00 - __main__ - INFO - ✓ Configuration validated
2025-01-21 10:00:00 - database - INFO - Successfully connected to MongoDB
2025-01-21 10:00:00 - __main__ - INFO - ✓ Database connection successful
2025-01-21 10:00:00 - agent - INFO - HR Agent initialized successfully
2025-01-21 10:00:00 - bot - INFO - Starting HR Management Bot...
2025-01-21 10:00:00 - bot - INFO - Bot is ready to receive messages!
```

### Production Mode

For production, use a process manager like `systemd` or `supervisor`:

```bash
# Example with systemd
sudo nano /etc/systemd/system/hr-bot.service
```

```ini
[Unit]
Description=HR Management Telegram Bot
After=network.target mongodb.service

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/hr-management-system
Environment="PATH=/path/to/hr-management-system/venv/bin"
ExecStart=/path/to/hr-management-system/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable hr-bot
sudo systemctl start hr-bot
sudo systemctl status hr-bot
```

## 💬 Usage Examples

### Basic Interactions

1. **Start the Bot**
   ```
   User: /start
   Bot: Welcome message with quick action buttons
   ```

2. **Setup Profile**
   ```
   User: /profile
   Bot: Please provide your employee email or ID
   User: john.smith@company.com
   Bot: ✅ Profile linked successfully!
   ```

3. **Simple Employee Search**
   ```
   User: Show employee john.smith@company.com
   Bot: 👤 Employee Information
        Name: John Smith
        Email: john.smith@company.com
        Role: employee
        ...
   ```

4. **Check Attendance**
   ```
   User: Show my attendance for this month
   Bot: 📊 Attendance Summary - Last 30 Days
        ...statistics...
   ```

5. **Mark Attendance**
   ```
   User: Mark my attendance
   Bot: ✅ Attendance marked successfully!
   ```

6. **Department Reports**
   ```
   User: Show Engineering department attendance
   Bot: 📊 Department Attendance Report
        ...detailed statistics...
   ```

7. **Complex Queries**
   ```
   User: Who was late in Engineering this week?
   Bot: ⏰ Late Arrivals - Last 7 Days
        ...filtered results...
   ```

## 🧪 Testing

### Manual Testing

1. **Test Employee Search**:
   - Search by email
   - Search by ID
   - Search non-existent employee

2. **Test Attendance**:
   - Mark attendance
   - View attendance summary
   - Check late arrivals

3. **Test Department Queries**:
   - List employees in department
   - Department attendance report

### Automated Testing (Optional)

Create `test_tools.py`:

```python
import pytest
from tools import search_employee_by_email, mark_attendance
from datetime import datetime

def test_search_employee():
    result = search_employee_by_email("john.smith@company.com")
    assert "John Smith" in result

def test_mark_attendance_invalid_id():
    result = mark_attendance("invalid_id")
    assert "❌" in result

# Add more tests...
```

Run tests:

```bash
pytest test_tools.py -v
```

## 🌐 Deployment

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6.0
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  hr_bot:
    build: .
    depends_on:
      - mongodb
    env_file:
      - .env
    restart: always

volumes:
  mongo_data:
```

Deploy:

```bash
docker-compose up -d
```

### Cloud Deployment (Heroku Example)

1. Create `Procfile`:
```
worker: python main.py
```

2. Create `runtime.txt`:
```
python-3.9.18
```

3. Deploy:
```bash
heroku create your-hr-bot
heroku config:set MONGODB_URI=your_mongodb_atlas_uri
heroku config:set GROQ_API_KEY=your_groq_key
heroku config:set TELEGRAM_BOT_TOKEN=your_bot_token
git push heroku main
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Bot Not Responding

**Problem**: Telegram bot doesn't respond to messages

**Solutions**:
- Check bot token is correct
- Verify bot is running (`ps aux | grep python`)
- Check logs: `tail -f hr_system.log`
- Test bot token: `curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getMe`

#### 2. Database Connection Failed

**Problem**: Cannot connect to MongoDB

**Solutions**:
```bash
# Test MongoDB connection
mongosh mongodb://localhost:27017

# Check if MongoDB is running
# On macOS:
brew services list
# On Linux:
systemctl status mongod

# Check connection string
echo $MONGODB_URI
```

#### 3. Groq API Errors

**Problem**: Agent returns API errors

**Solutions**:
- Verify API key is valid
- Check API rate limits
- Test API key:
```bash
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

#### 4. Agent Not Understanding Queries

**Problem**: Agent gives incorrect or unexpected responses

**Solutions**:
- Check agent prompt in `agent.py`
- Adjust temperature (lower = more deterministic)
- Increase max_iterations if needed
- Review tool descriptions

#### 5. Slow Response Times

**Problem**: Bot takes too long to respond

**Solutions**:
- Add database indexes (already in `database.py`)
- Use MongoDB Atlas for better performance
- Cache frequently accessed data
- Reduce max_iterations

## 📚 API Documentation

### Tools API

#### search_employee_by_email(email: str) -> str
Searches for an employee by email address.

**Parameters**:
- `email` (str): Employee's email address

**Returns**:
- str: Formatted employee information or error message

#### search_employee_by_id(user_id: str) -> str
Searches for an employee by MongoDB ObjectId.

**Parameters**:
- `user_id` (str): 24-character MongoDB ObjectId

**Returns**:
- str: Formatted employee information or error message

#### get_employee_attendance_summary(user_id: str, days: int = 30) -> str
Gets attendance summary for an employee.

**Parameters**:
- `user_id` (str): Employee's MongoDB ObjectId
- `days` (int): Number of days to analyze (default: 30)

**Returns**:
- str: Formatted attendance statistics

#### mark_attendance(user_id: str, punch_in_time: Optional[str] = None) -> str
Marks attendance for an employee.

**Parameters**:
- `user_id` (str): Employee's MongoDB ObjectId
- `punch_in_time` (Optional[str]): Time in HH:MM format

**Returns**:
- str: Confirmation message

#### get_department_attendance_report(designation: str, days: int = 30) -> str
Generates department-wide attendance report.

**Parameters**:
- `designation` (str): Department name
- `days` (int): Number of days to analyze

**Returns**:
- str: Formatted department statistics

#### get_late_arrivals(days: int = 7) -> str
Gets list of late arrivals.

**Parameters**:
- `days` (int): Number of days to look back

**Returns**:
- str: List of late employees

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- LangChain for the agent framework
- Groq for fast LLM inference
- MongoDB for the database
- Telegram for the bot platform

## 📞 Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Contact: support@yourcompany.com

## 🗺️ Roadmap

Future enhancements:
- [ ] Leave management system
- [ ] Payroll integration
- [ ] Performance reviews
- [ ] Document management
- [ ] Multi-language support
- [ ] Voice message support
- [ ] Analytics dashboard
- [ ] Email notifications
- [ ] Calendar integration
- [ ] Mobile app

---

**Built with ❤️ using Python, LangChain, and AI**