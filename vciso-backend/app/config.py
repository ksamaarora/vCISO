# vciso-backend/app/config.py
from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# config.py - Application configuration settings
# This module defines the application settings using Pydantic's BaseSettings.
# It loads configuration values from environment variables and a .env file.
# The Settings class includes various configuration options such as API keys,
# environment settings, API prefixes, and LLM parameters.

load_dotenv()

class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    
    # LLM Configuration
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

    # Vector Database Settings
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp-free")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "vciso-frameworks")
    
    # Embedding Settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", "1536"))
    
    # RAG Settings
    RAG_TOP_K: int = int(os.getenv("RAG_TOP_K", "5"))  # Top K chunks to retrieve
    RAG_SIMILARITY_THRESHOLD: float = float(os.getenv("RAG_SIMILARITY_THRESHOLD", "0.7"))
    
    # Pydantic Configuration
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
