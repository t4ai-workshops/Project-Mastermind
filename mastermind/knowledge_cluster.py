import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Awaitable

from sentence_transformers import SentenceTransformer
from .vectordb import VectorDatabase, VectorEntry

class KnowledgeCluster:
    """Layered Knowledge Storage System
    
    Manages two main context functions:
    1. Memory Context: Persistent knowledge storage
       Flow: server.py -> store_knowledge() -> vectordb.store_vector
    
    2. Knowledge Retrieval: Fetching relevant knowledge
       Flow: MCPManager.get_context -> retrieve_knowledge() -> vectordb.query_vectors
    """
    
    def __init__(
        self, 
        embedding_model: str = 'all-MiniLM-L6-v2',
        short_term_retention_hours: int = 24,
        long_term_retention_days: int = 365
    ):
        """
        Initialiseer kenniscluster met verschillende geheugenniveaus
        
        :param embedding_model: Model voor vector generatie
        :param short_term_retention_hours: Retentie voor korte termijn geheugen
        :param long_term_retention_days: Retentie voor lange termijn geheugen
        """
        self.logger = logging.getLogger(__name__)
        
        # Embedding generator
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Vector databases voor verschillende lagen
        self.short_term_db = VectorDatabase(collection_name="short_term_memory")
        self.long_term_db = VectorDatabase(collection_name="long_term_memory")
        self.context_db = VectorDatabase(collection_name="context_memory")
        
        # Retentie parameters
        self.short_term_retention = short_term_retention_hours
        self.long_term_retention = long_term_retention_days
    
    async def get_vector_embedding(self, text: str) -> List[float]:
        """
        Genereer vector embedding voor tekst
        
        :param text: Invoer tekst
        :return: Embedding vector
        """
        loop = asyncio.get_running_loop()
        embedding = await loop.run_in_executor(None, self.embedding_model.encode, text)
        return [float(x) for x in embedding]
    
    async def store_knowledge(
        self, 
        content: str, 
        category: str = 'general',
        importance: float = 0.5,
        is_context_specific: bool = False
    ) -> str:
        """Store knowledge in the appropriate memory database
        
        This is the primary method for Memory Context - the persistent memory system.
        Flow: server.py endpoints -> this method -> vectordb.store_vector
        
        Args:
            content: The knowledge content to store
            category: Knowledge category
            importance: Importance score (0-1)
            is_context_specific: Whether this is context-specific knowledge
        """
        embedding = await self.get_vector_embedding(content)
        
        if is_context_specific:
            return await self.context_db.store_vector(
                content=content,
                embedding=embedding,
                category=category,
                importance=importance
            )
        elif importance > 0.7:  # Hoge belangrijkheid naar lange termijn
            return await self.long_term_db.store_vector(
                content=content,
                embedding=embedding,
                category=category,
                importance=importance
            )
        else:
            return await self.short_term_db.store_vector(
                content=content,
                embedding=embedding,
                category=category,
                importance=importance
            )
    
    async def retrieve_knowledge(
        self, 
        query: str, 
        max_results: int = 5,
        include_short_term: bool = True,
        include_long_term: bool = True,
        include_context: bool = True,
        min_importance: float = 0.3
    ) -> List[VectorEntry]:
        """Search for relevant knowledge across memory layers
        
        This is the primary method for Knowledge Retrieval - used by Prompt Context.
        Flow: MCPManager.get_context -> this method -> vectordb.query_vectors
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
        """
        query_embedding = await self.get_vector_embedding(query)
        results: List[VectorEntry] = []
        
        tasks = []
        if include_short_term:
            tasks.append(self.short_term_db.query_vectors(
                n_results=max_results,
                min_importance=min_importance
            ))
        
        if include_long_term:
            tasks.append(self.long_term_db.query_vectors(
                n_results=max_results,
                min_importance=min_importance
            ))
        
        if include_context:
            tasks.append(self.context_db.query_vectors(
                n_results=max_results,
                min_importance=min_importance
            ))
        
        if tasks:
            all_results = await asyncio.gather(*tasks)
            for result_set in all_results:
                results.extend(result_set)
        
        return sorted(
            results, 
            key=lambda x: x.metadata.get('importance', 0), 
            reverse=True
        )[:max_results]
    
    async def cleanup_memories(self) -> None:
        """Ruim oude en minder belangrijke herinneringen op"""
        tasks = []
        
        if self.short_term_db:
            tasks.append(self.short_term_db.cleanup_vectors(min_importance=0.2))
        
        if self.long_term_db:
            tasks.append(self.long_term_db.cleanup_vectors(min_importance=0.5))
        
        if tasks:
            await asyncio.gather(*tasks)
    
    async def update_knowledge_importance(
        self, 
        entry_id: int, 
        new_importance: float,
        memory_type: str = 'long_term'
    ) -> bool:
        """
        Update het belang van een specifiek kennisitem
        
        :param entry_id: ID van het kennisitem
        :param new_importance: Nieuwe belang score
        :param memory_type: Type geheugen (short_term, long_term, context)
        :return: Of update succesvol was
        """
        db_map = {
            'short_term': self.short_term_db,
            'long_term': self.long_term_db,
            'context': self.context_db
        }
        
        selected_db = db_map.get(memory_type)
        if not selected_db:
            self.logger.error(f"Ongeldig geheugentype: {memory_type}")
            return False
        
        try:
            return await selected_db.update_importance(entry_id, new_importance)
        except Exception as e:
            self.logger.error(f"Error updating importance: {e}")
            return False
    
    async def process_cluster(self, cluster_ids: List[int]) -> Any:
        """Process een cluster van geheugens"""
        # Implementatie hier
        pass
    
    async def verify_cluster(self, cluster_id: int) -> bool:
        """Verifieer een specifieke cluster"""
        # Implementatie hier
        return True