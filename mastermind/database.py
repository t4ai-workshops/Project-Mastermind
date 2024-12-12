from typing import List, Optional, Any, Union
import chromadb
from chromadb.config import Settings
from chromadb.types import EmbeddingFunction
from chromadb import Client
from chromadb.api.types import QueryResult

PERSIST_DIRECTORY = "./chroma_db"

class Database:
    def __init__(self) -> None:
        self.chroma_client: Optional[Client] = None
        self.settings: Settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=PERSIST_DIRECTORY,
        )

    def connect(self) -> None:
        self.chroma_client = chromadb.Client(self.settings)

    def create_collection(self, name: str, embedding_function: Optional[EmbeddingFunction] = None) -> Any:
        if self.chroma_client is None:
            raise ValueError("Client not connected. Call connect() first.")
        return self.chroma_client.create_collection(name=name, embedding_function=embedding_function)
        
    def get_collection(self, name: str) -> Any:
        if self.chroma_client is None:
            raise ValueError("Client not connected. Call connect() first.")
        return self.chroma_client.get_collection(name=name)

    def put_vectors(self, collection_name: str, vectors: List[List[float]], documents: List[str]) -> Any:
        collection = self.get_collection(collection_name)
        return collection.add(embeddings=vectors, documents=documents, ids=[str(i) for i in range(len(documents))])

    def query(self, collection_name: str, query_vector: List[float], n_results: int = 10) -> QueryResult:
        collection = self.get_collection(collection_name)
        return collection.query(query_embeddings=query_vector, n_results=n_results, include=['documents', 'distances', 'ids'])

db = Database()
