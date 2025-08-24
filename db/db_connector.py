from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv(".env")

NEON_DB_URL = os.getenv("NEON_DB_URL")
engine = create_engine(NEON_DB_URL)
print("DB URL:", NEON_DB_URL)

def get_connection():
    return engine.connect()
