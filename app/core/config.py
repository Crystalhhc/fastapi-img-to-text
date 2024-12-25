from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict 
from pydantic import field_validator
from dotenv import load_dotenv
from functools import lru_cache

class Settings(BaseSettings):            
    app_auth_token: str
    debug: bool = False
    echo_active: bool = False
    app_auth_token_prod: str = None
    skip_auth: bool = False
    max_file_size: int = 10 * 1024 * 1024  # 10 MB
    allowed_file_types: list = ["image/jpeg", "image/png"]
 
    model_config = SettingsConfigDict(
        env_file='.venv', 
        env_file_encoding='utf-8',
        validate_default=False,
        extra='ignore'
        )

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
DEBUG=settings.debug

BASE_DIR = Path(__file__).parent.parent.parent # path to /Users/chenhsihu/eval/fastapi-img-to-text/
UPLOAD_DIR = BASE_DIR / "uploads"
