from chromadb.config import Settings
from chromadb.utils import embedding_functions
from chromadb import Client

PERSIST_DIRECTORY = "/path/to/db"

class Database:
    def __init__(self):
        self.chroma_client = None
        self.settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=PERSIST_DIRECTORY,
        )

    def connect(self):
        self.chroma_client = Client(self.settings)

    def create_collection(self, name: str, embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")):
        return self.chroma_client.create_collection(name=name, embedding_function=embedding_function)
        
    def get_collection(self, name: str):
        return self.chroma_client.get_collection(name=name)

    def put_vectors(self, collection_name: str, vectors, documents):
        collection = self.get_collection(collection_name)
        return collection.add(embeddings=vectors, documents=documents, ids=[str(i) for i in range(len(documents))])

    def query(self, collection_name: str, query_vector, n_results=10):
        collection = self.get_collection(collection_name)
        results = collection.query(query_embeddings=query_vector, n_results=n_results, include=['documents', 'distances', 'ids'])
        return results

db = Database()
