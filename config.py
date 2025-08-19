import os
from dotenv import load_dotenv

# Loads from .env --to--> environment variable
load_dotenv(override=True) # Ensures we always pick from .env and ignores any directly set environment variable

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
