import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        load_dotenv()
        self.DEBUG = os.getenv("DEBUG", "false").lower() == "true"
        self.LINE_ACCESS_TOKEN = self._require("LINE_ACCESS_TOKEN")
        self.LINE_CHANNEL_SECRET = self._require("LINE_CHANNEL_SECRET")
        self.RESMAN_URL = self._require("RESMAN_URL")
        self.DATABASE_URL = self._require("DATABASE_URL")
        self.SYNC_USER_TOKEN = self._require("SYNC_USER_TOKEN")
        self.SYNC_GROUP_TOKEN = self._require("SYNC_GROUP_TOKEN")
        self.REQUEST_SLC_URL = self._require("REQUEST_SLC_URL")
        self.REQUEST_SLC_TOKEN = self._require("REQUEST_SLC_TOKEN")
        self.RNDBA_GROUP_ID = self._require("RNDBA_GROUP_ID")

    @staticmethod
    def _require(key: str) -> str:
        value = os.getenv(key)
        if value is None:
            raise EnvironmentError(f"Missing required environment variable: {key}")
        return value

settings = Settings()
