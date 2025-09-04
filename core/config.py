import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
    RESMAN_URL = os.getenv('RESMAN_URL')
    DATABASE_URL = os.getenv('DATABASE_URL')
    SYNC_USER_TOKEN = os.getenv('SYNC_USER_TOKEN')
    SYNC_GROUP_TOKEN = os.getenv('SYNC_GROUP_TOKEN')
    REQUEST_URL = os.getenv('REQUEST_URL')
    REQUEST_TOKEN = os.getenv('REQUEST_TOKEN')

settings = Settings()