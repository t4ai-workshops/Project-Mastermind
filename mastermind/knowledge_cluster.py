import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Awaitable

from sentence_transformers import SentenceTransformer
from .vectordb import VectorDatabase, VectorEntry

class KnowledgeCluster:
    """Gelaagd kennisopslagsysteem"""
    
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
        """
        Sla kennis op in de juiste geheugendatabase
        
        :param content: Kennisinhoud
        :param category: Categorie van de kennis
        :param importance: Belang van de kennis
        :param is_context_specific: Of het context-specifiek is
        :return: Entry ID
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
        """
        Zoek relevante kennis over verschillende geheugenniveaus
        
        :param query: Zoekopdracht
        :param max_results: Maximum aantal resultaten
        :param include_short_term: Zoek in korte termijn geheugen
        :param include_long_term: Zoek in lange termijn geheugen
        :param include_context: Zoek in context geheugen
        :param min_importance: Minimale belang score
        :return: Lijst van relevante kennisitems
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