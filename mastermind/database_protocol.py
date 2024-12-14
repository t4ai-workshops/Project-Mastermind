from typing import Protocol, List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid

@dataclass
class DatabaseEntry:
    """Generieke database entry met standaard metadata"""
    id: str = str(uuid.uuid4())
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    metadata: Dict[str, Any] = None

    def __init__(self, metadata: dict):
        self.metadata = metadata

    def to_dict(self) -> Dict[str, Any]:
        """Converteer entry naar dictionary"""
        return {
            **asdict(self),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class DatabaseInterface(Protocol):
    """Protocol voor database operaties"""
    
    async def create(self, entry: DatabaseEntry) -> str:
        """Maak een nieuwe entry aan"""
        ...

    async def read(self, entry_id: str) -> Optional[DatabaseEntry]:
        """Lees een specifieke entry"""
        ...

    async def update(self, entry_id: str, data: Dict[str, Any]) -> bool:
        """Update een bestaande entry"""
        ...

    async def delete(self, entry_id: str) -> bool:
        """Verwijder een entry"""
        ...

    async def query(self, 
                    filters: Optional[Dict[str, Any]] = None, 
                    limit: int = 10) -> List[DatabaseEntry]:
        """Zoek entries met optionele filters"""
        ...

class BaseDatabaseManager:
    """Basis database management klasse"""
    
    def __init__(self, database_interface: DatabaseInterface):
        self.db = database_interface
        
    async def store(self, data: Dict[str, Any]) -> str:
        """Generieke opslag methode"""
        entry = DatabaseEntry(metadata=data)
        return await self.db.create(entry)
    
    async def retrieve(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """Generieke ophaal methode"""
        result = await self.db.read(entry_id)
        return result.metadata if result else None 