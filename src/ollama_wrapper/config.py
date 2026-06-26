import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Ollama endpoint configuration
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    # Request timeout configuration
    request_timeout: float = 60.0
    
    # Security prompt injection static patterns (regex or keyword-based)
    injection_keywords: list[str] = [
        "ignore previous instructions",
        "system prompt override",
        "you are now a",
        "bypass safeguards",
        "jailbreak",
        "disregard guidelines",
    ]

settings = Settings()
