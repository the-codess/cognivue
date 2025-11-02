"""
Configuration settings for the Intelligent Report System
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # Project paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    SAMPLE_DATA_DIR: Path = DATA_DIR / "sample"
    MODELS_DIR: Path = BASE_DIR / "models"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    # LLM Settings (Ollama - Open Source)
    LLM_MODEL: str = Field(default="llama2", description="Ollama model name")
    LLM_BASE_URL: str = Field(default="http://localhost:11434", description="Ollama API URL")
    LLM_TEMPERATURE: float = Field(default=0.7, description="LLM temperature")
    LLM_MAX_TOKENS: int = Field(default=2000, description="Max tokens for LLM")
    
    # Embedding Model Settings
    EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Sentence transformer model"
    )
    EMBEDDING_DIMENSION: int = Field(default=384, description="Embedding dimension")
    
    # Vector Database Settings
    VECTOR_DB_PATH: Path = BASE_DIR / "data" / "vector_db"
    COLLECTION_NAME: str = Field(default="reports_collection", description="ChromaDB collection")
    
    # OCR Settings
    TESSERACT_PATH: Optional[str] = Field(default=None, description="Path to tesseract executable")
    OCR_LANGUAGE: str = Field(default="eng", description="OCR language")
    
    # NLP Settings
    SPACY_MODEL: str = Field(default="en_core_web_sm", description="spaCy model")
    MAX_TEXT_LENGTH: int = Field(default=1000000, description="Max text length for processing")
    
    # Topic Modeling Settings
    MIN_TOPIC_SIZE: int = Field(default=10, description="Minimum topic size for BERTopic")
    N_TOPICS: Optional[int] = Field(default=None, description="Number of topics (None for auto)")
    
    # Database Settings
    DB_TYPE: str = Field(default="sqlite", description="Database type")
    DB_PATH: Path = BASE_DIR / "data" / "app.db"
    POSTGRES_HOST: str = Field(default="localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL port")
    POSTGRES_DB: str = Field(default="report_system", description="PostgreSQL database")
    POSTGRES_USER: str = Field(default="postgres", description="PostgreSQL user")
    POSTGRES_PASSWORD: str = Field(default="", description="PostgreSQL password")
    
    MONGO_HOST: str = Field(default="localhost", description="MongoDB host")
    MONGO_PORT: int = Field(default=27017, description="MongoDB port")
    MONGO_DB: str = Field(default="report_system", description="MongoDB database")
    
    # API Settings
    API_HOST: str = Field(default="0.0.0.0", description="API host")
    API_PORT: int = Field(default=8000, description="API port")
    API_RELOAD: bool = Field(default=True, description="API auto-reload")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    
    # Processing Settings
    BATCH_SIZE: int = Field(default=32, description="Batch size for processing")
    MAX_WORKERS: int = Field(default=4, description="Max worker threads")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create global settings instance
settings = Settings()

# Ensure directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.SAMPLE_DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)
settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
settings.VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)