import os
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings:
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

settings = Settings()