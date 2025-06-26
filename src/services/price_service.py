import asyncio
from typing import Dict, Optional
from ..infrastructure.price_api.client import PriceApiClient
from ..app.config import get_settings

class PriceService:
    def __init__(self, price_client: PriceApiClient):
        self.price_client = price_client
        self.settings = get_settings()
        self.prices: Dict[str, float] = {}
        self._task: Optional[asyncio.Task] = None
        
    async def start(self):
        """Start price tracking"""
        if not self._task:
            self._task = asyncio.create_task(self._track_prices())
            
    async def stop(self):
        """Stop price tracking"""
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
            
    async def _track_prices(self):
        """Track prices in background"""
        while True:
            try:
                # Get TON price
                ton_price = await self.price_client.get_ton_price()
                if ton_price:
                    self.prices['TON'] = ton_price
                    # Calculate BOLT price based on TON price
                    self.prices['BOLT'] = ton_price * 0.012
                    
                # Wait for next update
                await asyncio.sleep(self.settings.PRICE_UPDATE_INTERVAL)
                
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(60)  # Wait on error
                
    def get_price(self, symbol: str) -> Optional[float]:
        """Get current price for symbol"""
        return self.prices.get(symbol.upper()) 