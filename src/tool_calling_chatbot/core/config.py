"""Configuration management for the tool calling chatbot."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass
class Config:
    """Configuration class for the chatbot."""
    
    openai_api_key: str
    model: str = "gpt-4o-mini"
    temperature: float = 1.2
    max_tokens: int = 1000
    
    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it in your .env file or environment."
            )
        
        return cls(
            openai_api_key=api_key,
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "1.2")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1000")),
        )
    
    def validate(self) -> None:
        """Validate configuration values."""
        if not self.openai_api_key:
            raise ValueError("OpenAI API key cannot be empty")
        
        if not (0.0 <= self.temperature <= 2.0):
            raise ValueError("Temperature must be between 0.0 and 2.0")
        
        if self.max_tokens <= 0:
            raise ValueError("Max tokens must be positive")
        
        if not self.model:
            raise ValueError("Model name cannot be empty") 