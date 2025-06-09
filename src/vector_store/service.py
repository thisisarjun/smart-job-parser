from langchain_core.embeddings import Embeddings

from src.vector_store.models import AvailableVectorStores, JobVectorStore
from src.vector_store.stores.memory_store import MemoryStore


class VectorStoreService:
    def __init__(self, vector_store_type: AvailableVectorStores, embedding: Embeddings):
        if vector_store_type == AvailableVectorStores.MEMORY:
            self.vector_store = MemoryStore(embedding=embedding)

    def add_job_details(self, job_details: JobVectorStore) -> None:
        self.vector_store.add_job_details(job_details)

    def similarity_search(self, query: str) -> list[JobVectorStore]:
        return self.vector_store.similarity_search(query)
