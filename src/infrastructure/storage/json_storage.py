import json
import asyncio
from typing import Optional, List, TypeVar, Generic, Dict
from datetime import datetime
from pathlib import Path
from .base import Repository
from ...core.models.user import User

T = TypeVar('T')

class JsonRepository(Repository[T]):
    def __init__(self, file_path: Path, model_class: type):
        self.file_path = file_path
        self.model_class = model_class
        self.lock = asyncio.Lock()
        self._ensure_file_exists()
        
    def _ensure_file_exists(self):
        """Create storage file if it doesn't exist"""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=4)
                
    async def _read_data(self) -> Dict:
        """Read data from file with lock"""
        async with self.lock:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
    async def _write_data(self, data: Dict):
        """Write data to file with lock"""
        async with self.lock:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
    async def get(self, id: str) -> Optional[T]:
        data = await self._read_data()
        if id in data:
            return self.model_class(**data[id])
        return None
        
    async def save(self, id: str, entity: T) -> T:
        data = await self._read_data()
        data[id] = entity.__dict__
        await self._write_data(data)
        return entity
        
    async def delete(self, id: str) -> bool:
        data = await self._read_data()
        if id in data:
            del data[id]
            await self._write_data(data)
            return True
        return False
        
    async def list(self) -> List[T]:
        data = await self._read_data()
        return [self.model_class(**item) for item in data.values()] 