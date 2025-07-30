from dotenv import load_dotenv
import os

load_dotenv();

def get_env(key: str, default=None):
    """Fetch environment variable with optional default."""
    return os.getenv(key, default)