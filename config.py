import os
from pathlib import Path

from dotenv import load_dotenv


# Get project root
def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).parent


project_root = get_project_root()

dotenv_path = project_root / ".env.test" if os.getenv("ENV") == "testing" else project_root / ".env"
# Load .env file
load_dotenv(dotenv_path, override=True)


class Settings:
    """Application settings loaded from environment variables"""

    def __init__(self):

        self.dotenv_path = dotenv_path
        # Environment Settings
        self.ENV = os.getenv("ENV", "development")

        # API Settings
        self.API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
        self.PROJECT_NAME = os.getenv("PROJECT_NAME", "Smart Job Parser")

        # Server Settings
        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = int(os.getenv("PORT", "8000"))

        # RapidAPI Settings
        self.JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY", "test_api_key")
        self.RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "jsearch.p.rapidapi.com")

        # Vector Store Settings
        self.VECTOR_STORE_TYPE = os.getenv("VECTOR_STORE_TYPE", "memory")

        # Model Settings
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "mxbai-embed-large")

        # Pinecone Settings
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "test_pinecone_key")
        self.PINECONE_INDEX = os.getenv("PINECONE_INDEX", "test_index")
        self.PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "test_namespace")

        # JSearch Settings
        self.JSEARCH_BASE_URL = os.getenv("JSEARCH_BASE_URL", "https://jsearch.p.rapidapi.com")
        self.JSEARCH_HEADER_HOST = os.getenv("JSEARCH_HEADER_HOST", "jsearch.p.rapidapi.com")

        # Debug settings
        self.DEBUG = os.getenv("DEBUG", "false").lower() == "true"


# Create settings instance
settings = Settings()
