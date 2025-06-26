from typing import Optional, List
from ..core.models.user import User
from ..infrastructure.storage.base import Repository

class UserService:
    def __init__(self, user_repository: Repository[User]):
        self.user_repository = user_repository
        # Note: Repository is kept for session management only, not persistent tracking
        
    async def get_session_user(self, user_id: str) -> Optional[User]:
        """Get user session data (temporary only)"""
        return await self.user_repository.get(user_id)
        
    async def create_session_user(self, user_id: str) -> User:
        """Create temporary user session"""
        user = User(id=user_id)
        return await self.user_repository.save(user_id, user)
        
    async def get_or_create_session_user(self, user_id: str) -> User:
        """Get existing session or create new temporary session"""
        user = await self.get_session_user(user_id)
        if not user:
            user = await self.create_session_user(user_id)
        return user
        
    async def update_session_data(self, user_id: str, data: dict) -> User:
        """Update temporary session data only"""
        user = await self.get_or_create_session_user(user_id)
        user.session_data.update(data)
        return await self.user_repository.save(user.id, user)
        
    async def clear_user_session(self, user_id: str) -> None:
        """Clear user session for privacy"""
        user = await self.get_session_user(user_id)
        if user:
            user.clear_session()
            await self.user_repository.save(user.id, user) 