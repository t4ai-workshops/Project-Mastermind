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
            documents = results.get('documents')
            ids = results.get('ids')
            metadatas = results.get('metadatas')
            
            if documents and ids and metadatas and len(documents) > 0:
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

    async def get_by_id(self, entry_id: str) -> Optional[VectorEntry]:
        """Retrieve a specific entry by ID"""
        try:
            self.logger.debug(f"Fetching entry: {entry_id}")
            result = self.collection.get(ids=[entry_id])
            
            ids = result.get('ids', [])
            documents = result.get('documents', [])
            metadatas = result.get('metadatas', [])
            
            if ids and documents and metadatas and len(ids) > 0:
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

# Rest of the file remains the same