"""Application configuration management."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    app_name: str = "XJTLU Food Recommendation System"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # DeepSeek API
    deepseek_api_key: str
    deepseek_api_base: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"
    temperature: float = 0.7
    max_context_length: int = 4000
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./data/users.db"
    vector_db_path: str = "./data/chroma_db"
    
    # Model Settings
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
