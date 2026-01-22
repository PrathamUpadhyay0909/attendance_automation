from dotenv import load_dotenv
import os

load_dotenv()

print("--- Environment Variable Check ---")
print(f"Loading .env from: {os.getcwd()}")

api_key = os.getenv("OPENROUTER_API_KEY")
model = os.getenv("OPENROUTER_MODEL")

if api_key:
    # Print first few chars to verify it's not empty, but mask the rest
    masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***"
    print(f"✅ OPENROUTER_API_KEY found: {masked_key}")
else:
    print("❌ OPENROUTER_API_KEY NOT found")

if model:
    print(f"✅ OPENROUTER_MODEL found: {model}")
else:
    print("❌ OPENROUTER_MODEL NOT found (using default)")
    
print("-" * 30)
