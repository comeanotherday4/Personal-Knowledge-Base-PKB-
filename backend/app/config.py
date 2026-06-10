from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/knowledge_base"
    REDIS_URL: str = "redis://localhost:6379/0"

    # AI 配置
    OPENAI_API_KEY: str = ""
    OPENAI_API_BASE: str = "https://api.openai.com/v1"

    # R2R 配置
    R2R_API_URL: str = "http://localhost:8001"

    # 文件存储
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 52428800  # 50MB

    # 安全配置
    SECRET_KEY: str = "your_secret_key_here_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ElasticSearch
    ELASTICSEARCH_URL: str = "http://localhost:9200"

    # ChromaDB
    CHROMA_PERSIST_DIR: str = "./data/chroma"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()