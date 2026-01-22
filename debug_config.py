from config import config
import os

print(f"DEBUG: MONGODB_DB_NAME='{config.MONGODB_DB_NAME}'")
print(f"DEBUG: MONGODB_URI starts with='{config.MONGODB_URI[:15]}...'")

if "." in config.MONGODB_DB_NAME:
    print("ERROR: MONGODB_DB_NAME contains a dot, which is invalid.")
else:
    print("MONGODB_DB_NAME seems valid format-wise.")
