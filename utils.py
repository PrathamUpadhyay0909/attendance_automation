"""
Utility functions for HR Management System.
Helper functions for common operations.
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from bson import ObjectId

logger = logging.getLogger(__name__)


def parse_date_string(date_str: str) -> Optional[datetime]:
    """
    Parse a date string into datetime object.
    Supports various formats including natural language.
    
    Args:
        date_str: Date string (e.g., "2025-01-15", "today", "yesterday")
    
    Returns:
        datetime object or None if parsing fails
    """
    date_str = date_str.lower().strip()
    today = datetime.now()
    
    # Handle natural language dates
    if date_str in ["today", "now"]:
        return today
    elif date_str == "yesterday":
        return today - timedelta(days=1)
    elif date_str == "tomorrow":
        return today + timedelta(days=1)
    
    # Try standard formats
    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y/%m/%d"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    logger.warning(f"Could not parse date string: {date_str}")
    return None


def validate_objectid(id_str: str) -> bool:
    """
    Validate if a string is a valid MongoDB ObjectId.
    
    Args:
        id_str: String to validate
    
    Returns:
        True if valid ObjectId, False otherwise
    """
    return ObjectId.is_valid(id_str) and len(id_str) == 24


def format_time(hours: float) -> str:
    """
    Format hours into human-readable time.
    
    Args:
        hours: Number of hours
    
    Returns:
        Formatted time string
    """
    if hours < 0:
        return "0 hours"
    
    whole_hours = int(hours)
    minutes = int((hours - whole_hours) * 60)
    
    if whole_hours == 0:
        return f"{minutes} minutes"
    elif minutes == 0:
        return f"{whole_hours} hours"
    else:
        return f"{whole_hours} hours {minutes} minutes"


def calculate_date_range(period: str) -> tuple[datetime, datetime]:
    """
    Calculate start and end dates for a period.
    
    Args:
        period: Period string (e.g., "this week", "last month", "today")
    
    Returns:
        Tuple of (start_date, end_date)
    """
    now = datetime.now()
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_today = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    period = period.lower().strip()
    
    if period in ["today", "now"]:
        return start_of_today, end_of_today
    
    elif period == "yesterday":
        start = start_of_today - timedelta(days=1)
        end = end_of_today - timedelta(days=1)
        return start, end
    
    elif period in ["this week", "week"]:
        # Start from Monday of current week
        start = start_of_today - timedelta(days=now.weekday())
        return start, end_of_today
    
    elif period == "last week":
        # Previous Monday to Sunday
        start = start_of_today - timedelta(days=now.weekday() + 7)
        end = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        return start, end
    
    elif period in ["this month", "month"]:
        start = start_of_today.replace(day=1)
        return start, end_of_today
    
    elif period == "last month":
        # First day of last month
        first_of_this_month = start_of_today.replace(day=1)
        last_day_of_last_month = first_of_this_month - timedelta(days=1)
        start = last_day_of_last_month.replace(day=1)
        return start, last_day_of_last_month
    
    elif period in ["this year", "year"]:
        start = start_of_today.replace(month=1, day=1)
        return start, end_of_today
    
    else:
        # Default to last 30 days
        start = start_of_today - timedelta(days=30)
        return start, end_of_today


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format a number as a percentage.
    
    Args:
        value: Number to format
        decimals: Number of decimal places
    
    Returns:
        Formatted percentage string
    """
    return f"{value:.{decimals}f}%"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
    
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        input_str: Input string to sanitize
    
    Returns:
        Sanitized string
    """
    # Remove any potentially dangerous characters
    dangerous_chars = ['$', '{', '}', '<', '>', ';']
    sanitized = input_str
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    return sanitized.strip()


def parse_tool_input(input_str: str) -> List[str]:
    """
    Parse tool input that might contain multiple comma-separated values.
    
    Args:
        input_str: Input string (e.g., "user_id,30" or "Engineering,60")
    
    Returns:
        List of parsed values
    """
    return [part.strip() for part in input_str.split(',')]


def format_error_message(error: Exception, user_friendly: bool = True) -> str:
    """
    Format an error message for display to users.
    
    Args:
        error: Exception object
        user_friendly: Whether to show user-friendly message
    
    Returns:
        Formatted error message
    """
    if user_friendly:
        error_messages = {
            "ConnectionFailure": "⚠️ Could not connect to the database. Please try again later.",
            "ValidationError": "⚠️ The data provided is invalid. Please check and try again.",
            "OperationFailure": "⚠️ The operation could not be completed. Please try again.",
            "TimeoutError": "⚠️ The request timed out. Please try again.",
        }
        
        error_type = type(error).__name__
        return error_messages.get(error_type, "⚠️ An unexpected error occurred. Please try again.")
    else:
        return f"Error: {type(error).__name__} - {str(error)}"


def get_working_days_in_period(start_date: datetime, end_date: datetime) -> int:
    """
    Calculate number of working days (Mon-Fri) in a period.
    
    Args:
        start_date: Start date
        end_date: End date
    
    Returns:
        Number of working days
    """
    working_days = 0
    current_date = start_date
    
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday = 0, Friday = 4
            working_days += 1
        current_date += timedelta(days=1)
    
    return working_days


def calculate_attendance_grade(percentage: float) -> str:
    """
    Convert attendance percentage to a grade.
    
    Args:
        percentage: Attendance percentage (0-100)
    
    Returns:
        Grade string with emoji
    """
    if percentage >= 95:
        return "A+ 🌟 Excellent"
    elif percentage >= 90:
        return "A ⭐ Outstanding"
    elif percentage >= 85:
        return "B+ 👍 Very Good"
    elif percentage >= 80:
        return "B 👌 Good"
    elif percentage >= 75:
        return "C+ 📊 Satisfactory"
    elif percentage >= 70:
        return "C ⚠️ Needs Attention"
    elif percentage >= 60:
        return "D 🔴 Below Standard"
    else:
        return "F ❌ Critical"


def format_phone_number(phone: str) -> str:
    """
    Format phone number for display.
    
    Args:
        phone: Phone number string
    
    Returns:
        Formatted phone number
    """
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    # Format based on length
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Return original if can't format


def generate_report_summary(data: Dict[str, Any]) -> str:
    """
    Generate a summary section for reports.
    
    Args:
        data: Dictionary containing report data
    
    Returns:
        Formatted summary string
    """
    summary = "📝 Summary:\n"
    for key, value in data.items():
        formatted_key = key.replace('_', ' ').title()
        summary += f"   • {formatted_key}: {value}\n"
    return summary


def is_within_office_hours(time: datetime, start_hour: int = 9, end_hour: int = 18) -> bool:
    """
    Check if a time is within office hours.
    
    Args:
        time: Datetime to check
        start_hour: Office start hour (default 9)
        end_hour: Office end hour (default 18)
    
    Returns:
        True if within office hours, False otherwise
    """
    return start_hour <= time.hour < end_hour


def calculate_late_time(punch_in_time: str, standard_time: str = "09:30") -> int:
    """
    Calculate how many minutes late someone was.
    
    Args:
        punch_in_time: Actual punch-in time (HH:MM)
        standard_time: Standard start time (HH:MM)
    
    Returns:
        Minutes late (0 if not late)
    """
    try:
        actual_hour, actual_minute = map(int, punch_in_time.split(':'))
        standard_hour, standard_minute = map(int, standard_time.split(':'))
        
        actual_minutes = actual_hour * 60 + actual_minute
        standard_minutes = standard_hour * 60 + standard_minute
        
        late_minutes = actual_minutes - standard_minutes
        return max(0, late_minutes)
    except:
        return 0


# Constants
WORKING_HOURS_PER_DAY = 8
STANDARD_START_TIME = "09:30"
STANDARD_END_TIME = "18:00"
WEEKEND_DAYS = [5, 6]  # Saturday, Sunday

# Status emojis
STATUS_EMOJIS = {
    "Present": "✅",
    "Late": "⏰",
    "Absent": "❌",
    "Leave": "🏖️",
    "Work From Home": "🏠",
    "Half Day": "⏱️"
}


def get_status_emoji(status: str) -> str:
    """Get emoji for a given status."""
    return STATUS_EMOJIS.get(status, "❓")


# Export all utility functions
__all__ = [
    'parse_date_string',
    'validate_objectid',
    'format_time',
    'calculate_date_range',
    'format_percentage',
    'truncate_text',
    'sanitize_input',
    'parse_tool_input',
    'format_error_message',
    'get_working_days_in_period',
    'calculate_attendance_grade',
    'format_phone_number',
    'generate_report_summary',
    'is_within_office_hours',
    'calculate_late_time',
    'get_status_emoji',
    'WORKING_HOURS_PER_DAY',
    'STANDARD_START_TIME',
    'STANDARD_END_TIME',
    'WEEKEND_DAYS',
    'STATUS_EMOJIS'
]