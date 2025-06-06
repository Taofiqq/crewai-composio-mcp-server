import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")
NEBIUS_MODEL = os.getenv("NEBIUS_MODEL")
NEBIUS_BASE_URL = os.getenv("NEBIUS_BASE_URL")

# Composio Settings
COMPOSIO_ENTITY_ID = "default"

# Workflow Settings
MAX_RETRY_LIMIT = 3
VERBOSE_MODE = True

# GitHub Settings
GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER", "")
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME", "")
USER_EMAIL = os.getenv("USER_EMAIL", "abumahfuz21@gmail.com")
