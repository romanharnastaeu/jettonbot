from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path
from typing import Dict, ClassVar
import os

class Settings(BaseSettings):
    # Bot Configuration - Use environment variables
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    DEBUG: bool = True
    
    # API Keys - Use environment variables
    TON_API_KEY: str = os.getenv("TON_API_KEY", "YOUR_TON_API_KEY_HERE")
    
    # Storage Configuration
    DATA_DIR: Path = Path("data")
    USER_DATA_FILE: Path = DATA_DIR / "user_data.json"
    WALLET_DATA_FILE: Path = DATA_DIR / "wallets.json"
    LOG_DIR: Path = Path("logs")
    
    # Feature Flags
    ENABLE_PRICE_TRACKING: bool = True
    ENABLE_WHALE_TRACKING: bool = True
    ENABLE_NOTIFICATIONS: bool = True
    
    # Limits & Timeouts
    MAX_TRACKED_WALLETS: int = 5
    PRICE_UPDATE_INTERVAL: int = 60  # seconds
    REQUEST_TIMEOUT: int = 10  # seconds
    MAX_RETRIES: int = 3
    
    # Cache Configuration
    CACHE_TTL: int = 300  # 5 minutes
    PRICE_CACHE_TTL: int = 60  # 1 minute
    WALLET_CACHE_TTL: int = 120  # 2 minutes
    
    # State Management
    STATE_EXPIRY_MINUTES: int = 30
    
    # Command Configuration
    COMMAND_PREFIX: str = "/"
    
    # Contract Addresses (Public blockchain addresses - these are safe to keep)
    BOLT_CONTRACT: str = "EQD0vdSA_NedR9uvbgN9EikRX-suesDxGeFg69XQMavfLqIw"
    BOLT_JETTON: str = "0:f4bdd480fcd79d47dbaf6e037d1229115feb2e7ac0f119e160ebd5d031abdf2e"
    
    # Error Messages
    ERROR_MESSAGES: ClassVar[Dict[str, str]] = {
        "wallet_limit": "You've reached the maximum number of tracked wallets (5)",
        "invalid_address": "Invalid TON address provided",
        "api_error": "Error connecting to TON API. Please try again later",
        "timeout": "Request timed out. Please try again"
    }
    
    # API URLs (Public APIs - safe to keep)
    TON_API_BASE_URL: str = "https://tonapi.io/v2"
    PRICE_API_BASE_URL: str = "https://api.coingecko.com/api/v3"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings() 