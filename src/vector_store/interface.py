from abc import ABC, abstractmethod

from langchain_core.embeddings import Embeddings

from src.vector_store.models import JobVectorStore


class VectorStore(ABC):
    def __init__(self, embedding: Embeddings):
        self.embedding = embedding

    @abstractmethod
    def add_job_details(self, job_details: JobVectorStore) -> None:
        pass

    @abstractmethod
    def similarity_search(self, query: str) -> list[JobVectorStore]:
        pass
