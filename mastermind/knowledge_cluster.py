from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from .vectordb import VectorDatabase, VectorEntry
from sentence_transformers import SentenceTransformer

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
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Genereer vector embedding voor tekst
        
        :param text: Invoer tekst
        :return: Embedding vector
        """
        return self.embedding_model.encode(text).tolist()
    
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
        embedding = self._generate_embedding(content)
        
        if is_context_specific:
            return self.context_db.store_vector(
                content=content,
                embedding=embedding,
                category=category,
                importance=importance
            )
        elif importance > 0.7:  # Hoge belangrijkheid naar lange termijn
            return self.long_term_db.store_vector(
                content=content,
                embedding=embedding,
                category=category,
                importance=importance
            )
        else:
            return self.short_term_db.store_vector(
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
        query_embedding = self._generate_embedding(query)
        results: List[VectorEntry] = []
        
        if include_short_term:
            short_term = self.short_term_db.query_vectors(
                n_results=max_results,
                min_importance=min_importance
            )
            results.extend(short_term)
        
        if include_long_term:
            long_term = self.long_term_db.query_vectors(
                n_results=max_results,
                min_importance=min_importance
            )
            results.extend(long_term)
        
        if include_context:
            context = self.context_db.query_vectors(
                n_results=max_results,
                min_importance=min_importance
            )
            results.extend(context)
        
        # Sorteer op relevantie
        return sorted(
            results, 
            key=lambda x: x.metadata.get('importance', 0), 
            reverse=True
        )[:max_results]
    
    async def cleanup_memories(self) -> None:
        """
        Ruim oude en minder belangrijke herinneringen op
        """
        # Korte termijn geheugen: verwijder items ouder dan ingestelde uren
        await self.short_term_db.cleanup_vectors(min_importance=0.2)
        
        # Lange termijn geheugen: verwijder zeer oude of irrelevante items
        await self.long_term_db.cleanup_vectors(min_importance=0.5)
    
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
        
        return await selected_db.update_importance(entry_id, new_importance) 