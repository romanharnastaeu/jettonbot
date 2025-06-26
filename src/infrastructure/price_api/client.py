import aiohttp
from typing import Optional, Dict, Any
from ...app.config import get_settings

class PriceApiClient:
    def __init__(self):
        self.settings = get_settings()
        self.session: Optional[aiohttp.ClientSession] = None
        self.base_url = "https://api.coingecko.com/api/v3"
        
    async def initialize(self):
        """Initialize API client"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def close(self):
        """Close API client"""
        if self.session:
            await self.session.close()
            self.session = None
            
    async def get_ton_price(self) -> Optional[float]:
        """Get TON price in USD"""
        if not self.session:
            await self.initialize()
            
        try:
            async with self.session.get(
                f"{self.base_url}/simple/price",
                params={
                    "ids": "the-open-network",
                    "vs_currencies": "usd"
                }
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data["the-open-network"]["usd"]
                return None
        except Exception:
            return None 