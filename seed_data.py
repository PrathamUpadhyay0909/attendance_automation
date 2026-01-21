"""
Database seed script for HR Management System.
Creates sample users and attendance records for testing.
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
import random

def seed_database(mongodb_uri="mongodb://localhost:27017", db_name="hr_system"):
    """Seed the database with sample data."""
    
    print("=" * 60)
    print("HR Management System - Database Seed Script")
    print("=" * 60)
    
    # Connect to MongoDB
    print("\n📡 Connecting to MongoDB...")
    client = MongoClient(mongodb_uri)
    db = client[db_name]
    
    # Clear existing data
    print("🗑️  Clearing existing data...")
    db.users.delete_many({})
    db.attendances.delete_many({})
    print("   ✓ Data cleared")
    
    # Sample users
    print("\n👥 Creating sample employees...")
    
    sample_users = [
        {
            "_id": ObjectId(),
            "name": "John Smith",
            "email": "john.smith@company.com",
            "password": "$2b$10$hashedpassword",  # Hashed password
            "role": "employee",
            "designation": "Engineering",
            "phone": "+1-555-0101",
            "dateOfJoining": "2023-01-15",
            "dateOfBirth": "1990-05-20",
            "bloodGroup": "A+",
            "isDisabled": False,
            "isDeleted": False,
            "isWorkFromHome": False,
            "emergencyContactNumber": "+1-555-0199",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "__v": 0
        },
        {
            "_id": ObjectId(),
            "name": "Sarah Johnson",
            "email": "sarah.johnson@company.com",
            "password": "$2b$10$hashedpassword",
            "role": "employee",
            "designation": "Engineering",
            "phone": "+1-555-0102",
            "dateOfJoining": "2023-02-01",
            "dateOfBirth": "1992-08-15",
            "bloodGroup": "B+",
            "isDisabled": False,
            "isDeleted": False,
            "isWorkFromHome": False,
            "emergencyContactNumber": "+1-555-0198",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "__v": 0
        },
        {
            "_id": ObjectId(),
            "name": "Michael Chen",
            "email": "michael.chen@company.com",
            "password": "$2b$10$hashedpassword",
            "role": "employee",
            "designation": "Sales",
            "phone": "+1-555-0103",
            "dateOfJoining": "2023-03-10",
            "dateOfBirth": "1988-12-05",
            "bloodGroup": "O+",
            "isDisabled": False,
            "isDeleted": False,
            "isWorkFromHome": False,
            "emergencyContactNumber": "+1-555-0197",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "__v": 0
        },
        {
            "_id": ObjectId(),
            "name": "Emily Davis",
            "email": "emily.davis@company.com",
            "password": "$2b$10$hashedpassword",
            "role": "employee",
            "designation": "Marketing",
            "phone": "+1-555-0104",
            "dateOfJoining": "2023-04-05",
            "dateOfBirth": "1995-03-12",
            "bloodGroup": "AB+",
            "isDisabled": False,
            "isDeleted": False,
            "isWorkFromHome": True,
            "emergencyContactNumber": "+1-555-0196",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "__v": 0
        },
        {
            "_id": ObjectId(),
            "name": "David Wilson",
            "email": "david.wilson@company.com",
            "password": "$2b$10$hashedpassword",
            "role": "employee",
            "designation": "Engineering",
            "phone": "+1-555-0105",
            "dateOfJoining": "2023-05-20",
            "dateOfBirth": "1987-11-30",
            "bloodGroup": "O-",
            "isDisabled": False,
            "isDeleted": False,
            "isWorkFromHome": False,
            "emergencyContactNumber": "+1-555-0195",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "__v": 0
        },
        {
            "_id": ObjectId(),
            "name": "Lisa Anderson",
            "email": "lisa.anderson@company.com",
            "password": "$2b$10$hashedpassword",
            "role": "hr",
            "designation": "HR",
            "phone": "+1-555-0106",
            "dateOfJoining": "2022-11-01",
            "dateOfBirth": "1985-07-18",
            "bloodGroup": "A-",
            "isDisabled": False,
            "isDeleted": False,
            "isWorkFromHome": False,
            "emergencyContactNumber": "+1-555-0194",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "__v": 0
        },
        {
            "_id": ObjectId(),
            "name": "Robert Martinez",
            "email": "robert.martinez@company.com",
            "password": "$2b$10$hashedpassword",
            "role": "employee",
            "designation": "Sales",
            "phone": "+1-555-0107",
            "dateOfJoining": "2023-06-15",
            "dateOfBirth": "1993-09-25",
            "bloodGroup": "B-",
            "isDisabled": False,
            "isDeleted": False,
            "isWorkFromHome": False,
            "emergencyContactNumber": "+1-555-0193",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "__v": 0
        },
        {
            "_id": ObjectId(),
            "name": "Jennifer Taylor",
            "email": "jennifer.taylor@company.com",
            "password": "$2b$10$hashedpassword",
            "role": "employee",
            "designation": "Marketing",
            "phone": "+1-555-0108",
            "dateOfJoining": "2023-07-01",
            "dateOfBirth": "1991-04-08",
            "bloodGroup": "A+",
            "isDisabled": False,
            "isDeleted": False,
            "isWorkFromHome": False,
            "emergencyContactNumber": "+1-555-0192",
            "createdAt": datetime.now(),
            "updatedAt": datetime.now(),
            "__v": 0
        }
    ]
    
    # Insert users
    db.users.insert_many(sample_users)
    print(f"   ✓ Created {len(sample_users)} employees")
    
    # Generate attendance records
    print("\n📅 Generating attendance records...")
    
    attendance_count = 0
    statuses = ["Present", "Late"]
    
    for user in sample_users:
        print(f"   → {user['name']}")
        
        # Generate records for last 60 days
        for days_ago in range(60):
            date = datetime.now() - timedelta(days=days_ago)
            
            # Skip weekends
            if date.weekday() >= 5:  # Saturday = 5, Sunday = 6
                continue
            
            # 92% attendance rate (realistic)
            if random.random() < 0.92:
                # Random punch-in time between 08:00 and 10:30
                punch_in_hour = random.randint(8, 10)
                if punch_in_hour == 10:
                    punch_in_minute = random.randint(0, 30)
                else:
                    punch_in_minute = random.randint(0, 59)
                
                # Determine status (late if after 09:30)
                is_late = (punch_in_hour > 9) or (punch_in_hour == 9 and punch_in_minute > 30)
                status = "Late" if is_late else "Present"
                
                # Random punch-out time between 17:00 and 20:00
                punch_out_hour = random.randint(17, 20)
                punch_out_minute = random.randint(0, 59)
                
                # Calculate working hours
                total_minutes = (punch_out_hour * 60 + punch_out_minute) - (punch_in_hour * 60 + punch_in_minute)
                work_hours = round(total_minutes / 60, 2)
                
                attendance = {
                    "_id": ObjectId(),
                    "userId": user["_id"],
                    "date": date.replace(hour=0, minute=0, second=0, microsecond=0),
                    "punchIn": f"{punch_in_hour:02d}:{punch_in_minute:02d}",
                    "punchOut": f"{punch_out_hour:02d}:{punch_out_minute:02d}",
                    "status": status,
                    "totalWorkingHours": work_hours,
                    "punchInLocation": {
                        "type": "Point",
                        "coordinates": [72.8311 + random.uniform(-0.01, 0.01), 
                                      18.9200 + random.uniform(-0.01, 0.01)]
                    },
                    "punchOutLocation": {
                        "type": "Point",
                        "coordinates": [72.8311 + random.uniform(-0.01, 0.01), 
                                      18.9200 + random.uniform(-0.01, 0.01)]
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
                attendance_count += 1
    
    print(f"   ✓ Created {attendance_count} attendance records")
    
    # Create indexes
    print("\n🔍 Creating database indexes...")
    db.users.create_index([("email", 1)], unique=True)
    db.users.create_index([("role", 1)])
    db.users.create_index([("designation", 1)])
    db.attendances.create_index([("userId", 1)])
    db.attendances.create_index([("date", -1)])
    db.attendances.create_index([("status", 1)])
    print("   ✓ Indexes created")
    
    # Print summary
    print("\n" + "=" * 60)
    print("✅ Database seeding completed successfully!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   • Total employees: {db.users.count_documents({})}")
    print(f"   • Total attendance records: {db.attendances.count_documents({})}")
    print(f"   • Database: {db_name}")
    
    print("\n👤 Sample Employee IDs for testing:\n")
    for user in db.users.find().limit(5):
        print(f"   {user['name']:25} | Email: {user['email']:30} | ID: {user['_id']}")
    
    print("\n💡 Quick Start Commands:")
    print("   • Search employee: 'Show employee john.smith@company.com'")
    print("   • View attendance: Use any of the above employee IDs")
    print("   • Mark attendance: Provide your employee ID first via /profile")
    print("   • Department report: 'Show Engineering department attendance'")
    
    client.close()
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    import sys
    
    # Get MongoDB URI from command line or use default
    mongodb_uri = sys.argv[1] if len(sys.argv) > 1 else "mongodb://localhost:27017"
    db_name = sys.argv[2] if len(sys.argv) > 2 else "hr_system"
    
    seed_database(mongodb_uri, db_name)