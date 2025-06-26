import pytest
from src.services.price_service import PriceService
from src.infrastructure.price_api.client import PriceApiClient

@pytest.fixture
def price_client():
    class MockPriceClient:
        async def get_ton_price(self):
            return 2.5  # Mock TON price
            
    return MockPriceClient()

@pytest.fixture
def price_service(price_client):
    return PriceService(price_client)

@pytest.mark.asyncio
async def test_price_tracking():
    """Test price tracking functionality"""
    service = price_service()
    
    # Start tracking
    await service.start()
    
    # Check prices are updated
    assert service.get_price('TON') == 2.5
    assert service.get_price('BOLT') == 2.5 * 0.012
    
    # Stop tracking
    await service.stop()

@pytest.mark.asyncio
async def test_get_price_unknown_token():
    """Test getting price for unknown token"""
    service = price_service()
    assert service.get_price('UNKNOWN') is None 