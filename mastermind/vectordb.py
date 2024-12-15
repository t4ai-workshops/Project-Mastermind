from typing import List, Dict, Any, Optional
import logging

from .database import Memory, async_session, get_session
from .database_protocol import DatabaseEntry
from sqlalchemy.future import select

logger = logging.getLogger(__name__)

class VectorEntry(DatabaseEntry):
    """Uitgebreide database entry specifiek voor vector opslag"""
    def __init__(
        self, 
        content: str, 
        embedding: Optional[List[float]] = None,
        category: str = 'default',
        importance: float = 0.5,
        **kwargs: Any
    ) -> None:
        metadata = {
            'content': content,
            'embedding': embedding,
            'category': category,
            'importance': importance,
            **kwargs
        }
        super().__init__(metadata=metadata)

class VectorDatabase:
    """Gespecialiseerde vector database met extra functionaliteiten"""
    
    def __init__(self, collection_name: Optional[str] = None) -> None:
        self.collection_name = collection_name
    
    async def store_vector(self, content: str, embedding: List[float], category: str = 'default', importance: float = 0.5) -> str:
        """
        Sla een vector op met extra metadata
        """
        async with async_session() as session:
            new_memory = Memory(content=content, category=category, importance=importance)
            session.add(new_memory)
            await session.commit()
            return f"Vector opgeslagen met ID: {new_memory.id}"

    async def query_vectors(self, n_results: int = 5, category: Optional[str] = None, min_importance: float = 0.0) -> List[VectorEntry]:
        """
        Zoek vectoren op basis van categorie en belang
        """
        async with async_session() as session:
            query = select(Memory)
            if category:
                query = query.filter_by(category=category)
            if min_importance > 0:
                query = query.filter(Memory.importance >= min_importance)
            
            result = await session.execute(query.limit(n_results))
            memories = result.scalars().all()
            return [VectorEntry(content=m.content, category=m.category, importance=m.importance) for m in memories]

    async def update_importance(self, entry_id: int, new_importance: float) -> bool:
        """
        Update de belang score van een vector
        """
        async with async_session() as session:
            memory = await session.get(Memory, entry_id)
            if memory:
                memory.importance = new_importance
                await session.commit()
                return True
            return False

    async def cleanup_vectors(self, min_importance: float = 0.3) -> List[int]:
        """
        Verwijder laag-belangrijke vectoren
        """
        async with async_session() as session:
            query = select(Memory).filter(Memory.importance < min_importance)
            result = await session.execute(query)
            memories_to_delete = result.scalars().all()
            
            deleted_ids = [m.id for m in memories_to_delete]
            for memory in memories_to_delete:
                await session.delete(memory)
            await session.commit()
            return deleted_ids