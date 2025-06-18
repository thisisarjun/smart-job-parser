from abc import ABC, abstractmethod
from typing import List, Optional

from langchain_core.embeddings import Embeddings

from src.vector_store.models import JobVectorStore


class VectorStore(ABC):
    def __init__(self, embedding: Optional[Embeddings] = None):
        self.embedding = embedding

    @abstractmethod
    def add_job_details(self, job_details: List[JobVectorStore]) -> None:
        pass

    @abstractmethod
    def similarity_search(self, query: str, top_k: int = 5) -> list[JobVectorStore]:
        pass
