"""Configuration management for the application."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Anthropic API
    anthropic_api_key: str
    
    # Database
    database_url: str
    
    # Pinecone
    pinecone_api_key: str
    pinecone_environment: str = "us-east-1-aws"
    pinecone_index_name: str = "ai-assistant-index"
    
    # Web Search (Tavily)
    tavily_api_key: str
    
    # Server
    port: int = 8000
    environment: str = "development"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

