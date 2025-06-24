from typing import List

from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore

from src.vector_store.interface import VectorStore
from src.vector_store.models import JobVectorStore


class MemoryStore(VectorStore):
    def __init__(self, embedding: Embeddings):
        self.vector_store = InMemoryVectorStore(embedding=embedding)

    def add_job_details(self, job_details: List[JobVectorStore]) -> None:

        for job_detail in job_details:
            metadata = job_detail.get_metadata()
            metadata["job_description"] = job_detail.job_description
            metadata["location_string"] = job_detail.location_string
            self.vector_store.add_texts(texts=[job_detail.get_combined_text_document()], metadatas=[metadata])

    def similarity_search(self, query: str) -> list[JobVectorStore]:
        documents = self.vector_store.similarity_search(query)

        job_vector_stores = []
        for doc in documents:
            job_vector_store = JobVectorStore(
                job_id=doc.metadata.get("job_id"),  # type: ignore
                job_title=doc.metadata.get("job_title"),  # type: ignore
                job_description=doc.metadata.get("job_description", ""),
                job_apply_link=doc.metadata.get("job_apply_link"),  # type: ignore
                employer_name=doc.metadata.get("employer_name"),
                job_city=doc.metadata.get("job_city"),
                job_state=doc.metadata.get("job_state"),
                job_country=doc.metadata.get("job_country"),
                location_string=doc.metadata.get("location_string"),
            )
            job_vector_stores.append(job_vector_store)
        return job_vector_stores
