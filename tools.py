"""
LangChain tools for HR Management System.
Each tool provides specific functionality for the agent.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from langchain.tools import Tool
from bson import ObjectId
from database import db_handler

logger = logging.getLogger(__name__)


def search_employee_by_email(email: str) -> str:
    """
    Search for an employee by their email address.
    
    Args:
        email: Employee's email address
    
    Returns:
        Formatted employee information or error message
    """
    try:
        user = db_handler.get_user_by_email(email)
        
        if not user:
            return f"❌ No employee found with email: {email}"
        
        return _format_employee_info(user)
    except Exception as e:
        logger.error(f"Error searching employee by email: {e}")
        return f"⚠️ Error searching for employee: {str(e)}"


def search_employee_by_id(user_id: str) -> str:
    """
    Search for an employee by their user ID.
    
    Args:
        user_id: Employee's MongoDB ObjectId as string
    
    Returns:
        Formatted employee information or error message
    """
    try:
        if not ObjectId.is_valid(user_id):
            return f"❌ Invalid user ID format: {user_id}"
        
        user = db_handler.get_user_by_id(user_id)
        
        if not user:
            return f"❌ No employee found with ID: {user_id}"
        
        return _format_employee_info(user)
    except Exception as e:
        logger.error(f"Error searching employee by ID: {e}")
        return f"⚠️ Error searching for employee: {str(e)}"


def search_employees_by_designation(designation: str) -> str:
    """
    Search for all employees in a specific designation/department.
    
    Args:
        designation: Department or designation name
    
    Returns:
        List of employees in that designation or error message
    """
    try:
        users = db_handler.get_users_by_department(designation)
        
        if not users:
            return f"❌ No employees found in designation: {designation}"
        
        result = f"👥 Employees in {designation} ({len(users)} total):\n\n"
        
        for idx, user in enumerate(users, 1):
            result += f"{idx}. {user['name']} - {user['email']}\n"
            if user.get('phone'):
                result += f"   📞 {user['phone']}\n"
        
        return result
    except Exception as e:
        logger.error(f"Error searching employees by designation: {e}")
        return f"⚠️ Error searching for employees: {str(e)}"


def get_employee_attendance_summary(user_id: str, days: int = 30) -> str:
    """
    Get attendance summary for an employee for the last N days.
    
    Args:
        user_id: Employee's MongoDB ObjectId or string "user_id,days"
        days: Number of days to look back (default: 30)
    
    Returns:
        Formatted attendance summary or error message
    """
    try:
        # Handle composite input "user_id,days"
        if isinstance(user_id, str) and "," in user_id:
            try:
                parts = user_id.split(",")
                user_id = parts[0].strip()
                days = int(parts[1].strip())
            except ValueError:
                pass  # Use default days if parsing fails
        if not ObjectId.is_valid(user_id):
            return f"❌ Invalid user ID format: {user_id}"
        
        # Get user info
        user = db_handler.get_user_by_id(user_id)
        if not user:
            return f"❌ No employee found with ID: {user_id}"
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get attendances
        attendances = db_handler.get_user_attendances(
            user_id, start_date, end_date
        )
        
        if not attendances:
            return f"📊 No attendance records found for {user['name']} in the last {days} days."
        
        # Calculate statistics
        stats = _calculate_attendance_stats(attendances, days)
        
        result = f"📊 Attendance Summary - Last {days} Days\n\n"
        result += f"👤 Employee: {user['name']} ({user['email']})\n"
        result += f"📅 Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n\n"
        result += f"✅ Present: {stats['present']} days ({stats['present_percentage']:.1f}%)\n"
        result += f"❌ Absent: {stats['absent']} days\n"
        result += f"⏰ Late Arrivals: {stats['late']} times\n"
        result += f"🏠 Work From Home: {stats['wfh']} days\n"
        result += f"⏱️ Total Hours: {stats['total_hours']:.1f} hours\n"
        result += f"📈 Average: {stats['avg_hours']:.1f} hours/day\n\n"
        
        if stats['present_percentage'] >= 95:
            result += "💡 Excellent attendance! Keep up the great work."
        elif stats['present_percentage'] >= 85:
            result += "💡 Good attendance record."
        else:
            result += "💡 Attendance needs improvement."
        
        return result
    except Exception as e:
        logger.error(f"Error getting attendance summary: {e}")
        return f"⚠️ Error retrieving attendance summary: {str(e)}"


def mark_attendance(user_id: str, punch_in_time: Optional[str] = None) -> str:
    """
    Mark attendance for an employee for today.
    
    Args:
        user_id: Employee's MongoDB ObjectId or string "user_id,time"
        punch_in_time: Punch-in time in HH:MM format (optional, defaults to now)
    
    Returns:
        Confirmation message or error
    """
    try:
        # Handle composite input "user_id,time"
        if isinstance(user_id, str) and "," in user_id:
            try:
                parts = user_id.split(",")
                user_id = parts[0].strip()
                punch_in_time = parts[1].strip()
            except ValueError:
                pass
        if not ObjectId.is_valid(user_id):
            return f"❌ Invalid user ID format: {user_id}"
        
        # Get user info
        user = db_handler.get_user_by_id(user_id)
        if not user:
            return f"❌ No employee found with ID: {user_id}"
        
        # Check if attendance already exists for today
        today = datetime.now()
        existing = db_handler.get_attendance_by_user_and_date(user_id, today)
        
        if existing:
            return f"⚠️ Attendance already marked for {user['name']} today."
        
        # Parse punch-in time or use current time
        if punch_in_time:
            try:
                hour, minute = map(int, punch_in_time.split(':'))
                punch_in_dt = today.replace(hour=hour, minute=minute, second=0, microsecond=0)
            except ValueError:
                return f"❌ Invalid time format. Please use HH:MM format."
        else:
            punch_in_dt = today
        
        # Determine status (Present/Late)
        status = "Present"
        if punch_in_dt.hour > 9 or (punch_in_dt.hour == 9 and punch_in_dt.minute > 30):
            status = "Late"
        
        # Create attendance record
        attendance_data = {
            "userId": ObjectId(user_id),
            "date": today.replace(hour=0, minute=0, second=0, microsecond=0),
            "punchIn": punch_in_dt.strftime("%H:%M"),
            "punchOut": None,
            "status": status,
            "totalWorkingHours": 0,
            "punchInLocation": {
                "type": "Point",
                "coordinates": [0.0, 0.0]  # Default location
            },
            "punchOutLocation": {
                "type": "Point",
                "coordinates": [0.0, 0.0]
            },
            "areaRestriction": {
                "type": "Point",
                "coordinates": [0.0, 0.0],
                "radius": 500
            },
            "organization": user.get("organization"),
            "isWorkFromHome": user.get("isWorkFromHome", False),
            "createdAt": today,
            "updatedAt": today,
            "__v": 0
        }
        
        attendance_id = db_handler.create_attendance(attendance_data)
        
        if attendance_id:
            result = f"✅ Attendance marked successfully!\n\n"
            result += f"👤 Employee: {user['name']}\n"
            result += f"📅 Date: {today.strftime('%Y-%m-%d')}\n"
            result += f"⏰ Punch In: {punch_in_dt.strftime('%H:%M')}\n"
            result += f"📊 Status: {status}\n"
            
            if status == "Late":
                result += f"\n⚠️ Note: Marked as late (punch-in after 09:30)"
            
            return result
        else:
            return "⚠️ Failed to mark attendance. Please try again."
    
    except Exception as e:
        logger.error(f"Error marking attendance: {e}")
        return f"⚠️ Error marking attendance: {str(e)}"


def get_department_attendance_report(designation: str, days: int = 30) -> str:
    """
    Get attendance report for an entire department.
    
    Args:
        designation: Department name or string "designation,days"
        days: Number of days to look back (default: 30)
    
    Returns:
        Formatted department attendance report or error message
    """
    try:
        # Handle composite input "designation,days"
        if isinstance(designation, str) and "," in designation:
            try:
                parts = designation.split(",")
                designation = parts[0].strip()
                days = int(parts[1].strip())
            except ValueError:
                pass
        # Get all users in department
        users = db_handler.get_users_by_department(designation)
        
        if not users:
            return f"❌ No employees found in designation: {designation}"
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        result = f"📊 Department Attendance Report\n\n"
        result += f"🏢 Department: {designation}\n"
        result += f"📅 Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n"
        result += f"👥 Total Employees: {len(users)}\n\n"
        
        total_present = 0
        total_records = 0
        
        result += "📋 Individual Statistics:\n\n"
        
        for user in users:
            user_id = str(user['_id'])
            attendances = db_handler.get_user_attendances(
                user_id, start_date, end_date
            )
            
            stats = _calculate_attendance_stats(attendances, days)
            total_present += stats['present']
            total_records += len(attendances)
            
            result += f"• {user['name']}\n"
            result += f"  Present: {stats['present']}/{days} days ({stats['present_percentage']:.1f}%)\n"
            result += f"  Late: {stats['late']} times\n\n"
        
        # Overall statistics
        avg_attendance = (total_present / (len(users) * days) * 100) if users else 0
        
        result += f"📈 Department Average: {avg_attendance:.1f}%\n"
        
        return result
    except Exception as e:
        logger.error(f"Error getting department report: {e}")
        return f"⚠️ Error generating department report: {str(e)}"


def get_late_arrivals(days: int = 7) -> str:
    """
    Get list of employees who arrived late in the last N days.
    
    Args:
        days: Number of days to look back (default: 7)
    
    Returns:
        List of late arrivals or message
    """
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Query for late attendance
        pipeline = [
            {
                "$match": {
                    "status": "Late",
                    "date": {"$gte": start_date, "$lte": end_date}
                }
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "userId",
                    "foreignField": "_id",
                    "as": "user_info"
                }
            },
            {"$unwind": "$user_info"},
            {
                "$project": {
                    "userName": "$user_info.name",
                    "userEmail": "$user_info.email",
                    "date": 1,
                    "punchIn": 1
                }
            },
            {"$sort": {"date": -1}}
        ]
        
        late_records = db_handler.aggregate_query("attendances", pipeline)
        
        if not late_records:
            return f"✅ No late arrivals in the last {days} days. Great!"
        
        result = f"⏰ Late Arrivals - Last {days} Days\n\n"
        result += f"Total: {len(late_records)} instances\n\n"
        
        for record in late_records:
            date_str = record['date'].strftime('%Y-%m-%d')
            result += f"• {record['userName']} ({record['userEmail']})\n"
            result += f"  Date: {date_str}, Punch In: {record['punchIn']}\n\n"
        
        return result
    except Exception as e:
        logger.error(f"Error getting late arrivals: {e}")
        return f"⚠️ Error retrieving late arrivals: {str(e)}"


# Helper functions

def _format_employee_info(user: Dict) -> str:
    """Format employee information for display."""
    result = f"👤 Employee Information\n\n"
    result += f"Name: {user['name']}\n"
    result += f"Email: {user['email']}\n"
    result += f"Role: {user.get('role', 'N/A')}\n"
    
    if user.get('designation'):
        result += f"Designation: {user['designation']}\n"
    
    if user.get('phone'):
        result += f"Phone: {user['phone']}\n"
    
    if user.get('dateOfJoining'):
        result += f"Date of Joining: {user['dateOfJoining']}\n"
    
    if user.get('dateOfBirth'):
        result += f"Date of Birth: {user['dateOfBirth']}\n"
    
    if user.get('bloodGroup'):
        result += f"Blood Group: {user['bloodGroup']}\n"
    
    if user.get('emergencyContactNumber'):
        result += f"Emergency Contact: {user['emergencyContactNumber']}\n"
    
    result += f"\nStatus: {'🟢 Active' if not user.get('isDisabled') else '🔴 Disabled'}"
    
    if user.get('isWorkFromHome'):
        result += " | 🏠 Work From Home"
    
    return result


def _calculate_attendance_stats(attendances: list, total_days: int) -> Dict[str, Any]:
    """Calculate attendance statistics from records."""
    present_count = sum(1 for a in attendances if a['status'] in ['Present', 'Late'])
    late_count = sum(1 for a in attendances if a['status'] == 'Late')
    wfh_count = sum(1 for a in attendances if a.get('isWorkFromHome'))
    
    total_hours = 0
    for attendance in attendances:
        hours = attendance.get('totalWorkingHours', 0)
        if isinstance(hours, (int, float)):
            total_hours += hours
        elif isinstance(hours, str):
            try:
                total_hours += float(hours)
            except ValueError:
                pass
    
    avg_hours = total_hours / present_count if present_count > 0 else 0
    present_percentage = (present_count / total_days * 100) if total_days > 0 else 0
    
    return {
        'present': present_count,
        'absent': total_days - present_count,
        'late': late_count,
        'wfh': wfh_count,
        'total_hours': total_hours,
        'avg_hours': avg_hours,
        'present_percentage': present_percentage
    }


# Create LangChain tools
tools = [
    Tool(
        name="search_employee_by_email",
        func=search_employee_by_email,
        description="""
        Search for an employee using their email address.
        Input should be a valid email address string.
        Returns complete employee profile including name, role, designation, contact details, and status.
        Use this when the user asks about a specific person by email or mentions an email address.
        Example inputs: "john.smith@company.com", "employee@example.com"
        """
    ),
    Tool(
        name="search_employee_by_id",
        func=search_employee_by_id,
        description="""
        Search for an employee using their unique employee ID (MongoDB ObjectId).
        Input should be a 24-character hexadecimal string.
        Returns complete employee profile including name, role, designation, contact details, and status.
        Use this when the user provides or mentions an employee ID.
        Example inputs: "507f1f77bcf86cd799439011", "64a5f2c8d9e1234567890abc"
        """
    ),
    Tool(
        name="search_employees_by_designation",
        func=search_employees_by_designation,
        description="""
        Find all employees in a specific department or designation.
        Input should be the designation/department name as a string.
        Returns a list of all employees in that designation with their names, emails, and phone numbers.
        Use this when the user asks about a department, team, or asks "who works in [department]".
        Example inputs: "Engineering", "Sales", "HR", "Marketing", "Senior Developer"
        """
    ),
    Tool(
        name="get_employee_attendance_summary",
        func=get_employee_attendance_summary,
        description="""
        Get a comprehensive attendance summary for a specific employee.
        Input should be in the format: "user_id" or "user_id,days"
        where user_id is the employee's MongoDB ObjectId and days is the number of days to analyze (default 30).
        Returns detailed statistics including: present days, absent days, late arrivals, work from home days,
        total hours worked, average hours per day, and attendance percentage.
        Use this when the user asks about someone's attendance, work hours, or attendance record.
        Example inputs: "507f1f77bcf86cd799439011", "507f1f77bcf86cd799439011,60"
        """
    ),
    Tool(
        name="mark_attendance",
        func=mark_attendance,
        description="""
        Mark attendance for an employee for today.
        Input should be in the format: "user_id" or "user_id,HH:MM"
        where user_id is the employee's MongoDB ObjectId and HH:MM is the punch-in time (optional).
        If time is not provided, current time is used.
        Automatically determines if the employee is late (after 09:30).
        Returns confirmation with employee name, date, punch-in time, and status.
        Use this when the user says "mark my attendance", "I'm here", "punch in", etc.
        Example inputs: "507f1f77bcf86cd799439011", "507f1f77bcf86cd799439011,09:00"
        """
    ),
    Tool(
        name="get_department_attendance_report",
        func=get_department_attendance_report,
        description="""
        Generate a comprehensive attendance report for an entire department.
        Input should be in the format: "designation" or "designation,days"
        where designation is the department name and days is the number of days to analyze (default 30).
        Returns statistics for each employee in the department including attendance percentage,
        late arrivals, and department-wide averages.
        Use this when the user asks about department performance, team attendance, or comparisons.
        Example inputs: "Engineering", "Engineering,60", "Sales", "Marketing,90"
        """
    ),
    Tool(
        name="get_late_arrivals",
        func=get_late_arrivals,
        description="""
        Get a list of all employees who arrived late in a specified time period.
        Input should be the number of days to look back (default 7 if not specified).
        Returns list of employees with their late arrival dates and punch-in times.
        Use this when the user asks "who was late", "show late arrivals", "who came late this week".
        Example inputs: "7", "30", "1" (for today)
        """
    )
]