from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore

from src.vector_store.interface import VectorStore
from src.vector_store.models import JobVectorStore


class MemoryStore(VectorStore):
    def __init__(self, embedding: Embeddings):
        self.vector_store = InMemoryVectorStore(embedding=embedding)

    def add_job_details(self, job_details: JobVectorStore) -> None:
        metadata = job_details.get_metadata()
        metadata["job_description"] = job_details.job_description
        metadata["location_string"] = job_details.location_string

        self.vector_store.add_texts(
            texts=[job_details.get_combined_text_document()], metadatas=[metadata]
        )

    def similarity_search(self, query: str) -> list[JobVectorStore]:
        return self.vector_store.similarity_search(query)
