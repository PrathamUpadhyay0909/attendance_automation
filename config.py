"""
Configuration management for HR Management System.
Loads environment variables and provides configuration settings.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    """Configuration class holding all environment variables."""
    
    # MongoDB Configuration
    MONGODB_URI: str
    MONGODB_DB_NAME: str
    
    # Groq API Configuration
    GROQ_API_KEY: str
    
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN: str
    
    # OpenRouter API Configuration
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openai/gpt-3.5-turbo"
    
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # Agent Configuration
    AGENT_MAX_ITERATIONS: int = 10
    AGENT_TEMPERATURE: float = 0.1
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    
    # Application Settings
    MAX_CONTEXT_LENGTH: int = 4096
    RESPONSE_TIMEOUT: int = 30  # seconds

    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        return cls(
            MONGODB_URI=os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
            MONGODB_DB_NAME=os.getenv("MONGODB_DB_NAME", "hr_system"),
            GROQ_API_KEY=os.getenv("GROQ_API_KEY", ""),
            OPENROUTER_API_KEY=os.getenv("OPENROUTER_API_KEY", ""),
            OPENROUTER_MODEL=os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo"),
            GROQ_MODEL=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            AGENT_MAX_ITERATIONS=int(os.getenv("AGENT_MAX_ITERATIONS", "10")),
            AGENT_TEMPERATURE=float(os.getenv("AGENT_TEMPERATURE", "0.1")),
            LOG_LEVEL=os.getenv("LOG_LEVEL", "INFO"),
            MAX_CONTEXT_LENGTH=int(os.getenv("MAX_CONTEXT_LENGTH", "4096")),
            RESPONSE_TIMEOUT=int(os.getenv("RESPONSE_TIMEOUT", "30"))
        )
    
    def validate(self) -> None:
        """Validate that required configuration is present."""
        if not self.MONGODB_URI:
            raise ValueError("MONGODB_URI is required")
        
        # Check that at least one LLM provider is configured
        if not self.GROQ_API_KEY and not self.OPENROUTER_API_KEY:
            raise ValueError("Either GROQ_API_KEY or OPENROUTER_API_KEY is required")
            
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")


# Global configuration instance
config = Config.from_env()