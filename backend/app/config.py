from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    API_KEY: str
    LLM_BASE_URL: str = "https://llm.t1v.scibox.tech/v1"
    LLM_MODEL: str = "Qwen2.5-72B-Instruct-AWQ"
    EMBEDDING_MODEL: str = "bge-m3"
    
    DATA_PATH: str = "../ingestion/data/df.csv"
    VECTOR_STORE_PATH: str = "./data/faiss_index"
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/feedback.db"
    
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K: int = 3
    
    BM25_WEIGHT: float = 0.4
    VECTOR_WEIGHT: float = 0.6
    
    class Config:
        env_file = "/home/kate/T1-hackathon/.env"
        env_file_encoding = 'utf-8'


settings = Settings()

