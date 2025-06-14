from src.vector_store.interface import VectorStore
from src.vector_store.models import JobVectorStore


class VectorStoreService:
    def __init__(self, vector_store: VectorStore) -> None:
        self.vector_store = vector_store

    def add_job_details(self, job_details: JobVectorStore) -> None:
        self.vector_store.add_job_details(job_details)

    def similarity_search(self, query: str) -> list[JobVectorStore]:
        return self.vector_store.similarity_search(query)
