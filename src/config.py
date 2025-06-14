import os
from pathlib import Path

from dotenv import load_dotenv


def load_config():
    """Load configuration from .env file if it exists."""
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(env_path)

    return {
        # API Settings
        "API_PREFIX": "/api/v1",
        "PROJECT_NAME": "Smart Job Parser",
        # Server Settings
        "HOST": "0.0.0.0",
        "PORT": int(os.getenv("PORT", "8000")),
        # RapidAPI Settings
        "RAPIDAPI_KEY": os.getenv("RAPIDAPI_KEY"),
        "RAPIDAPI_HOST": "jsearch.p.rapidapi.com",
        # Vector Store Settings
        "VECTOR_STORE_TYPE": os.getenv("VECTOR_STORE_TYPE", "memory"),
        # Model Settings
        "EMBEDDING_MODEL": os.getenv("EMBEDDING_MODEL", "mxbai-embed-large"),
        # Pinecone Settings
        "PINECONE_API_KEY": os.getenv("PINECONE_API_KEY"),
        "PINECONE_INDEX": os.getenv("PINECONE_INDEX"),
        "PINECONE_NAMESPACE": os.getenv("PINECONE_NAMESPACE"),
    }


# Load configuration
config = load_config()
