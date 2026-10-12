import os
from dotenv import load_dotenv

load_dotenv()

OPEN_API_KEY =      os.getenv("LLM_API_KEY")
DATABASE_URL = os.getenv("DATABSE_URL")
QDRANT_URL = os.getenv("QDRANT_URL")

print(OPEN_API_KEY)