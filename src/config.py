# src/config.py

from dotenv import load_dotenv
import os

# Always load .env from project root
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if not load_dotenv(dotenv_path=dotenv_path):
    print(f"⚠️ Warning: .env file not found at {dotenv_path}")

# Define your configuration variables here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_BACKEND = os.getenv("LLM_BACKEND", "OPENAI")

# Validate critical variables
if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is not set.\n"
        "Please create a .env file or set it as an environment variable."
    )