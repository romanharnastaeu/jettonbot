import aiohttp
from typing import Optional, Dict, Any
from ...app.config import get_settings

class TonApiClient:
    def __init__(self):
        self.settings = get_settings()
        self.session: Optional[aiohttp.ClientSession] = None
        self.base_url = "https://tonapi.io/v2"
        
    async def initialize(self):
        """Initialize API client"""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.settings.TON_API_KEY}"}
            )
            
    async def close(self):
        """Close API client"""
        if self.session:
            await self.session.close()
            self.session = None
            
    async def get_account_info(self, address: str) -> Optional[Dict[str, Any]]:
        """Get account information including balance and tokens"""
        if not self.session:
            await self.initialize()
            
        try:
            async with self.session.get(
                f"{self.base_url}/accounts/{address}"
            ) as response:
                if response.status == 200:
                    return await response.json()
                return None
        except Exception:
            return None
            
    async def get_jettons(self, address: str) -> Optional[Dict[str, Any]]:
        """Get jetton balances for address"""
        if not self.session:
            await self.initialize()
            
        try:
            async with self.session.get(
                f"{self.base_url}/accounts/{address}/jettons"
            ) as response:
                if response.status == 200:
                    return await response.json()
                return None
        except Exception:
            return None 