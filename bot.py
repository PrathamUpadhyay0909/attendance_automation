"""
Telegram Bot implementation for HR Management System.
Handles user interactions and integrates with the LangChain agent.
"""

import logging
from typing import Dict, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from agent import hr_agent
from config import config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store user sessions (in production, use Redis or similar)
user_sessions: Dict[int, Dict] = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    user = update.effective_user
    user_id = user.id
    
    # Initialize user session
    user_sessions[user_id] = {
        'name': user.full_name,
        'username': user.username,
        'employee_id': None,  # Will be set after authentication
        'last_query': None
    }
    
    welcome_message = f"""👋 Welcome to HR Management System, {user.first_name}!

I'm your AI-powered HR assistant. I can help you with:

📊 **Attendance Management**
• Check your attendance records
• Mark your attendance
• View attendance statistics

👥 **Employee Information**
• Search for employees
• View employee profiles
• Get department information

📈 **Reports & Analytics**
• Generate attendance reports
• Department-wise statistics
• Late arrival tracking

💡 **How to use me:**
Just ask me questions in natural language! For example:
• "Show my attendance for this month"
• "Mark my attendance"
• "Who works in Engineering?"
• "Show me late arrivals this week"

**Quick Commands:**
/help - Show this message again
/profile - Setup your employee profile
/myattendance - Quick attendance summary
/mark - Mark today's attendance

Let's get started! How can I help you today?"""
    
    # Create quick action keyboard
    keyboard = [
        [
            InlineKeyboardButton("📊 My Attendance", callback_data='my_attendance'),
            InlineKeyboardButton("✅ Mark Attendance", callback_data='mark_attendance')
        ],
        [
            InlineKeyboardButton("👥 Search Employee", callback_data='search_employee'),
            InlineKeyboardButton("❓ Help", callback_data='help')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    help_text = """🤖 **HR Assistant Help Guide**

**Natural Language Queries:**
You can ask me anything about HR in plain English. Here are some examples:

**Employee Information:**
• "Show me employee with email john@company.com"
• "Who works in the Engineering department?"
• "Find employee ID 507f1f77bcf86cd799439011"

**Attendance Queries:**
• "Show my attendance for January"
• "How many days have I been present this month?"
• "What's my attendance percentage?"
• "Show attendance for last 60 days"

**Mark Attendance:**
• "Mark my attendance"
• "I'm here" or "Punch in"
• "Mark attendance for 09:30"

**Department Reports:**
• "Show Engineering department attendance"
• "Compare attendance between Sales and Marketing"
• "Which department has best attendance?"

**Late Arrivals:**
• "Who was late yesterday?"
• "Show me late arrivals this week"
• "Late arrivals in last 30 days"

**Commands:**
/start - Start the bot
/help - Show this help message
/profile - Setup your employee profile
/myattendance - Quick attendance summary
/mark - Mark today's attendance
/reset - Reset conversation context

**Tips:**
✅ Be specific with dates and names
✅ Use employee IDs or emails for accuracy
✅ I remember context from previous messages
✅ If I don't understand, I'll ask for clarification

Need more help? Just ask! 😊"""
    
    await update.message.reply_text(help_text)


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /profile command."""
    user_id = update.effective_user.id
    
    profile_text = """👤 **Employee Profile Setup**

To use personalized features like "my attendance", I need to link your Telegram account to your employee profile.

Please provide your employee email address or MongoDB user ID.

**Example:**
`john.smith@company.com`
or
`507f1f77bcf86cd799439011`

Once linked, you can use commands like:
• "Show my attendance"
• "Mark my attendance"
• "How many leaves do I have?"
"""
    
    # Set state to expect profile setup
    if user_id not in user_sessions:
        user_sessions[user_id] = {}
    user_sessions[user_id]['awaiting_profile'] = True
    
    await update.message.reply_text(profile_text)


async def myattendance_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /myattendance command."""
    user_id = update.effective_user.id
    
    # Check if user has linked profile
    if user_id not in user_sessions or not user_sessions[user_id].get('employee_id'):
        await update.message.reply_text(
            "⚠️ Please setup your profile first using /profile command."
        )
        return
    
    employee_id = user_sessions[user_id]['employee_id']
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Query the agent
    query = f"Show attendance summary for employee ID {employee_id} for last 30 days"
    response = hr_agent.process_query(query)
    
    await update.message.reply_text(response)


async def mark_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /mark command."""
    user_id = update.effective_user.id
    
    # Check if user has linked profile
    if user_id not in user_sessions or not user_sessions[user_id].get('employee_id'):
        await update.message.reply_text(
            "⚠️ Please setup your profile first using /profile command."
        )
        return
    
    employee_id = user_sessions[user_id]['employee_id']
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Query the agent
    query = f"Mark attendance for employee ID {employee_id}"
    response = hr_agent.process_query(query)
    
    await update.message.reply_text(response)


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /reset command."""
    hr_agent.reset_memory()
    await update.message.reply_text(
        "🔄 Conversation context has been reset. Starting fresh!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages from users."""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    # Initialize session if doesn't exist
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            'name': update.effective_user.full_name,
            'username': update.effective_user.username,
            'employee_id': None
        }
    
    # Check if user is in profile setup mode
    if user_sessions[user_id].get('awaiting_profile'):
        await handle_profile_setup(update, context, message_text)
        return
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Add user context if employee_id is available
    user_context = None
    if user_sessions[user_id].get('employee_id'):
        user_context = {
            'employee_id': user_sessions[user_id]['employee_id'],
            'telegram_id': user_id
        }
    
    # Process query with agent
    try:
        response = hr_agent.process_query(message_text, user_context)
        
        # Store last query
        user_sessions[user_id]['last_query'] = message_text
        
        # Send response
        try:
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            logger.warning(f"Markdown parsing failed, sending plain text: {e}")
            await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text(
            "⚠️ I encountered an error processing your request. Please try again or rephrase your question."
        )


async def handle_profile_setup(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    input_text: str
) -> None:
    """Handle profile setup flow."""
    user_id = update.effective_user.id
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Try to search for employee by email or ID
    if '@' in input_text:
        # Search by email
        query = f"Search employee by email {input_text}"
    else:
        # Assume it's an ID
        query = f"Search employee by ID {input_text}"
    
    response = hr_agent.process_query(query)
    
    # Check if employee was found
    if "❌" not in response and "Employee Information" in response:
        # Success - link the profile
        user_sessions[user_id]['employee_id'] = input_text if len(input_text) == 24 else None
        user_sessions[user_id]['awaiting_profile'] = False
        
        success_message = f"✅ Profile linked successfully!\n\n{response}\n\n"
        success_message += "You can now use personalized commands like:\n"
        success_message += "• /myattendance - View your attendance\n"
        success_message += "• /mark - Mark your attendance\n"
        success_message += "• Or just ask 'show my attendance'"
        
        await update.message.reply_text(success_message)
    else:
        # Failed to find employee
        await update.message.reply_text(
            f"{response}\n\nPlease try again with a valid email or employee ID, or use /start to cancel."
        )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard button clicks."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    callback_data = query.data
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    if callback_data == 'my_attendance':
        if user_id not in user_sessions or not user_sessions[user_id].get('employee_id'):
            await query.message.reply_text(
                "⚠️ Please setup your profile first using /profile command."
            )
        else:
            employee_id = user_sessions[user_id]['employee_id']
            agent_query = f"Show attendance summary for employee ID {employee_id} for last 30 days"
            response = hr_agent.process_query(agent_query)
            await query.message.reply_text(response)
    
    elif callback_data == 'mark_attendance':
        if user_id not in user_sessions or not user_sessions[user_id].get('employee_id'):
            await query.message.reply_text(
                "⚠️ Please setup your profile first using /profile command."
            )
        else:
            employee_id = user_sessions[user_id]['employee_id']
            agent_query = f"Mark attendance for employee ID {employee_id}"
            response = hr_agent.process_query(agent_query)
            await query.message.reply_text(response)
    
    elif callback_data == 'search_employee':
        await query.message.reply_text(
            "👥 **Search Employee**\n\nPlease provide:\n• Employee email address\n• Or employee ID\n\nExample: john@company.com"
        )
    
    elif callback_data == 'help':
        await help_command(update, context)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ An unexpected error occurred. Please try again later or contact support."
        )


def main() -> None:
    """Start the Telegram bot."""
    try:
        # Validate configuration
        config.validate()
        
        # Create application
        application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("profile", profile_command))
        application.add_handler(CommandHandler("myattendance", myattendance_command))
        application.add_handler(CommandHandler("mark", mark_command))
        application.add_handler(CommandHandler("reset", reset_command))
        
        # Add message handler
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Add callback query handler
        application.add_handler(CallbackQueryHandler(handle_callback))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        logger.info("Starting HR Management Bot...")
        logger.info("Bot is ready to receive messages!")
        
        # Start the bot
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


if __name__ == "__main__":
    main()