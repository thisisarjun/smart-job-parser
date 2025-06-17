from pathlib import Path

from dynaconf import Dynaconf, Validator


# Get project root
def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(__file__).parent


project_root = get_project_root()

settings = Dynaconf(
    envvar_prefix="",  # No prefix for environment variables
    settings_files=["settings.toml"],  # Load settings.toml
    environments=True,  # Enable environments
    load_dotenv=True,  # Load .env files
    env_switcher="ENV",  # Use ENV environment variable to switch environments
    dotenv_path=project_root / ".env",  # Default .env file
    validators=[
        # API Settings
        Validator("API_PREFIX", default="/api/v1"),
        Validator("PROJECT_NAME", default="Smart Job Parser"),
        # Server Settings
        Validator("HOST", default="0.0.0.0"),
        Validator("PORT", default=8000, cast=int),
        # RapidAPI Settings
        Validator("JSEARCH_API_KEY", default="test_api_key"),
        Validator("RAPIDAPI_HOST", default="jsearch.p.rapidapi.com"),
        # Vector Store Settings
        Validator("VECTOR_STORE_TYPE", default="memory"),
        # Model Settings
        Validator("EMBEDDING_MODEL", default="mxbai-embed-large"),
        # Pinecone Settings
        Validator("PINECONE_API_KEY", default="test_pinecone_key"),
        Validator("PINECONE_INDEX", default="test_index"),
        Validator("PINECONE_NAMESPACE", default="test_namespace"),
        # JSearch Settings
        Validator("JSEARCH_BASE_URL", default="https://jsearch.p.rapidapi.com"),
        Validator("JSEARCH_HEADER_HOST", default="jsearch.p.rapidapi.com"),
    ],
)
