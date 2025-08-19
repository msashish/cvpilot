import os
from dotenv import load_dotenv

# Loads from .env --to--> environment variable
load_dotenv(override=True) # Ensures we always pick from .env and ignores any directly set environment variable

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHAT_OPENAI_API_KEY = os.getenv("CHAT_OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
