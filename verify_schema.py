from database import db_handler
import sys

try:
    print("Connecting to database...")
    if not db_handler.client:
        print("ERROR: Could not connect to database (client is None)")
        sys.exit(1)
        
    print(f"Connected to: {db_handler.db.name}")
    
    # Check users collection
    user_count = db_handler.db.users.count_documents({})
    print(f"Users found: {user_count}")
    
    if user_count > 0:
        print("\n--- Sample User Schema ---")
        sample_user = db_handler.db.users.find_one()
        for key, value in sample_user.items():
            print(f"  {key}: {type(value).__name__}")
            
        # Check critical fields
        required = ['name', 'email', 'role', 'designation']
        missing = [f for f in required if f not in sample_user]
        if missing:
            print(f"\n WARNING: Missing expected fields: {missing}")
        else:
            print("\n SUCCESS: Critical user fields present.")
    else:
        print("\n WARNING: 'users' collection is empty!")

    # Check attendances collection
    att_count = db_handler.db.attendances.count_documents({})
    print(f"\nAttendances found: {att_count}")

except Exception as e:
    print(f"ERROR: {e}")
finally:
    db_handler.close()
