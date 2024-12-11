from typing import List, Dict, Any, Optional, Sequence, Mapping, cast
import chromadb
from chromadb.config import Settings
import numpy as np
from dataclasses import dataclass
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class VectorEntry:
    """Represents a single vector entry in the database"""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None

class VectorStore:
    """Manages vector storage and retrieval using ChromaDB"""
    def __init__(self, persist_directory: str = "./vectorstore") -> None:
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.create_collection(
            name="mastermind_memory",
            metadata={"description": "Long-term memory storage for MasterMind"}
        )
        self.logger = logging.getLogger(f"{__name__}.VectorStore")

    async def store(self, entry: VectorEntry) -> str:
        """Store a new entry in the vector database"""
        try:
            self.logger.debug(f"Storing entry: {entry.id}")
            self.collection.add(
                documents=[entry.content],
                metadatas=[entry.metadata],
                ids=[entry.id]
            )
            return entry.id
        except Exception as e:
            self.logger.error(f"Error storing entry: {str(e)}")
            raise

    async def query(
        self, 
        query_text: str, 
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[VectorEntry]:
        """Query the vector database for similar entries"""
        try:
            self.logger.debug(f"Querying with: {query_text}")
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=filter_metadata
            )
            
            entries: List[VectorEntry] = []
            
            # Safely handle potentially None values
            documents = results.get('documents', [[]])
            ids = results.get('ids', [[]])
            metadatas = results.get('metadatas', [[]])
            
            if documents and len(documents) > 0 and ids and len(ids) > 0 and metadatas and len(metadatas) > 0:
                docs = documents[0]
                id_list = ids[0]
                meta_list = metadatas[0]
                
                for i, (doc, id_str) in enumerate(zip(docs, id_list)):
                    if i < len(meta_list):
                        metadata = dict(meta_list[i])
                        entry = VectorEntry(
                            id=id_str,
                            content=doc,
                            metadata=metadata
                        )
                        entries.append(entry)
            
            return entries
        except Exception as e:
            self.logger.error(f"Error querying database: {str(e)}")
            raise

    async def update(self, entry: VectorEntry) -> None:
        """Update an existing entry"""
        try:
            self.logger.debug(f"Updating entry: {entry.id}")
            self.collection.update(
                ids=[entry.id],
                documents=[entry.content],
                metadatas=[entry.metadata]
            )
        except Exception as e:
            self.logger.error(f"Error updating entry: {str(e)}")
            raise

    async def delete(self, entry_id: str) -> None:
        """Delete an entry from the database"""
        try:
            self.logger.debug(f"Deleting entry: {entry_id}")
            self.collection.delete(ids=[entry_id])
        except Exception as e:
            self.logger.error(f"Error deleting entry: {str(e)}")
            raise

    async def get_by_id(self, entry_id: str) -> Optional[VectorEntry]:
        """Retrieve a specific entry by ID"""
        try:
            self.logger.debug(f"Fetching entry: {entry_id}")
            result = self.collection.get(ids=[entry_id])
            
            metadatas = result.get('metadatas', [])
            ids = result.get('ids', [])
            documents = result.get('documents', [])
            
            if metadatas and ids and documents and len(ids) > 0:
                metadata = dict(metadatas[0])
                return VectorEntry(
                    id=ids[0],
                    content=documents[0],
                    metadata=metadata
                )
            return None
        except Exception as e:
            self.logger.error(f"Error fetching entry: {str(e)}")
            raise

class EnhancedMemoryManager:
    """Manages memory using vector storage for improved retrieval"""
    def __init__(self, persist_directory: str = "./vectorstore") -> None:
        self.vector_store = VectorStore(persist_directory)
        self.logger = logging.getLogger(f"{__name__}.EnhancedMemoryManager")

    async def store_memory(
        self,
        content: str,
        category: str,
        importance: float = 0.5,
        additional_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Store a new memory with vector embedding"""
        try:
            metadata = {
                "category": category,
                "importance": importance,
                "timestamp": datetime.now().isoformat(),
                **(additional_metadata or {})
            }
            
            entry = VectorEntry(
                id=f"{category}_{datetime.now().timestamp()}",
                content=content,
                metadata=metadata
            )
            
            return await self.vector_store.store(entry)
        except Exception as e:
            self.logger.error(f"Error storing memory: {str(e)}")
            raise

    async def retrieve_relevant(
        self,
        query: str,
        category: Optional[str] = None,
        min_importance: float = 0.0,
        max_results: int = 5
    ) -> List[VectorEntry]:
        """Retrieve relevant memories using vector similarity"""
        try:
            filter_metadata: Dict[str, Any] = {}
            if category:
                filter_metadata["category"] = category
            if min_importance > 0:
                filter_metadata["importance"] = {"$gte": min_importance}

            return await self.vector_store.query(
                query_text=query,
                n_results=max_results,
                filter_metadata=filter_metadata
            )
        except Exception as e:
            self.logger.error(f"Error retrieving memories: {str(e)}")
            raise

    async def update_importance(self, entry_id: str, new_importance: float) -> None:
        """Update the importance score of a memory"""
        try:
            entry = await self.vector_store.get_by_id(entry_id)
            if entry:
                entry.metadata["importance"] = new_importance
                await self.vector_store.update(entry)
        except Exception as e:
            self.logger.error(f"Error updating importance: {str(e)}")
            raise

    async def cleanup_old_memories(
        self,
        max_age_days: int = 30,
        min_importance: float = 0.8
    ) -> None:
        """Clean up old memories based on age and importance"""
        try:
            # Calculate cutoff date
            cutoff_date = datetime.now().timestamp() - (max_age_days * 24 * 60 * 60)
            
            # Query for old memories
            filter_metadata = {
                "timestamp": {"$lt": cutoff_date},
                "importance": {"$lt": min_importance}
            }
            
            old_memories = await self.vector_store.query(
                query_text="",  # Empty query to match all
                n_results=1000,  # High number to get all matches
                filter_metadata=filter_metadata
            )
            
            # Delete old, unimportant memories
            for memory in old_memories:
                await self.vector_store.delete(memory.id)
                self.logger.debug(f"Cleaned up old memory: {memory.id}")
                
        except Exception as e:
            self.logger.error(f"Error cleaning up memories: {str(e)}")
            raise