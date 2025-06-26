from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')

class Repository(ABC, Generic[T]):
    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        """Get entity by ID"""
        pass
        
    @abstractmethod
    async def save(self, id: str, entity: T) -> T:
        """Save entity"""
        pass
        
    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete entity by ID"""
        pass
        
    @abstractmethod
    async def list(self) -> List[T]:
        """List all entities"""
        pass 