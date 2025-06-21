import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # API Keys
    COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")
    NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")
    # Meeting Configuration
    DEFAULT_ATTENDEE_EMAIL = os.getenv(
        "DEFAULT_ATTENDEE_EMAIL", "abumahfuz21@gmail.com"
    )

    # Nebius LLM Configuration
    NEBIUS_MODEL = os.getenv("NEBIUS_MODEL")
    NEBIUS_BASE_URL = os.getenv("NEBIUS_BASE_URL", "https://api.studio.nebius.ai/v1/")

    # Project Configuration
    TARGET_REPOSITORY = os.getenv("TARGET_REPOSITORY", "vercel/next-learn")

    # Workflow Settings
    ENTITY_ID = "default"
    BUG_LABEL = "bug"
    MEETING_DURATION_MINUTES = 30


settings = Settings()
