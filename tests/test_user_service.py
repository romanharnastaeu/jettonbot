import pytest
from src.core.models.user import User
from src.services.user_service import UserService

@pytest.fixture
def user_repository():
    class MockRepository:
        def __init__(self):
            self.users = {}
            
        async def get(self, id: str) -> User:
            return self.users.get(id)
            
        async def save(self, id: str, user: User) -> User:
            self.users[id] = user
            return user
            
    return MockRepository()

@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository)

@pytest.mark.asyncio
async def test_create_user(user_service):
    user_id = "123"
    user = await user_service.create_user(user_id)
    assert user.id == user_id
    assert user.saved_address is None
    assert len(user.tracked_wallets) == 0

@pytest.mark.asyncio
async def test_add_tracked_wallet(user_service):
    user_id = "123"
    address = "test_address"
    
    # Create user first
    user = await user_service.create_user(user_id)
    
    # Add tracked wallet
    result = await user_service.add_tracked_wallet(user_id, address)
    assert result is True
    
    # Verify wallet was added
    user = await user_service.get_user(user_id)
    assert len(user.tracked_wallets) == 1
    assert user.tracked_wallets[0].address == address 