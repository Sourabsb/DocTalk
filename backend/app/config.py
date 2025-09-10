import os
from dotenv import load_dotenv

load_dotenv()

AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Increase session timeout to 24 hours instead of 30 minutes
SESSION_TIMEOUT = 24 * 60 * 60  # 24 hours
MAX_FILE_SIZE = 20 * 1024 * 1024
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
