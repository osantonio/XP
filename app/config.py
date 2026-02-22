import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://secop:secop123@localhost:1234/secop_db")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    ITEMS_PER_PAGE = 10
