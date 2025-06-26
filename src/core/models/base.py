from typing import Protocol, TypeVar, Optional

T = TypeVar('T')

class Model(Protocol):
    """Base protocol for all models in the application"""
    id: str

class Repository(Protocol[T]):
    """
    Base protocol for all repositories
    
    This protocol defines the standard interface that all repositories
    must implement for data persistence operations.
    
    Type Parameters:
        T: The type of model this repository handles
    """
    
    async def get(self, id: str) -> Optional[T]:
        """
        Retrieve an entity by its ID
        
        Args:
            id: Unique identifier of the entity
            
        Returns:
            The entity if found, None otherwise
            
        Raises:
            StorageError: If there's an error accessing storage
        """
        ...
        
    async def save(self, entity: T) -> T:
        """
        Save an entity
        
        Args:
            entity: The entity to save
            
        Returns:
            The saved entity
            
        Raises:
            StorageError: If there's an error saving to storage
            ValidationError: If entity validation fails
        """
        ... 