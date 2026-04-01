import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Auto-Mail 2.0"
    APP_VERSION: str = "0.1.0"
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")


settings = Settings()