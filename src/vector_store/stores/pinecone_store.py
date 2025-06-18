from typing import List

from pinecone import Index, Pinecone

from config import settings
from src.vector_store.interface import VectorStore
from src.vector_store.models import JobVectorStore


class PineconeStore(VectorStore):
    index: Index
    namespace: str

    def __init__(self):
        api_key = settings.pinecone_api_key
        index_name = settings.pinecone_index
        # pinecone already has an embedding model
        pc = Pinecone(api_key=api_key)
        self.index = pc.Index(index_name)
        self.namespace = settings.pinecone_namespace

    def add_job_details(self, job_details: List[JobVectorStore]) -> None:
        # TODO: better id
        to_store_vector_stores = []
        for job_detail in job_details:
            record_id = job_detail.job_id
            to_store_vector_stores.append(
                {
                    "id": record_id,
                    "description": job_detail.get_combined_text_document(),
                    **job_detail.model_dump(),
                }
            )
        self.index.upsert_records(self.namespace, to_store_vector_stores)

    def similarity_search(self, query: str) -> list[JobVectorStore]:
        reranked_results = self.index.search(
            namespace=self.namespace,
            query={"top_k": 5, "inputs": {"text": query}},
            rerank={
                "model": "bge-reranker-v2-m3",
                "top_n": 5,
                "rank_fields": ["description"],
            },
            # fields=["description"],
        )
        reranked_results_hits = reranked_results.result.hits
        job_vector_stores = []
        for hit in reranked_results_hits:
            fields = hit.fields
            job_vector_store = JobVectorStore(
                job_id=fields.get("job_id"),
                job_title=fields.get("job_title"),
                job_description=fields.get("job_description"),
                job_apply_link=fields.get("job_apply_link"),
                employer_name=fields.get("employer_name"),
                job_city=fields.get("job_city"),
                job_state=fields.get("job_state"),
                job_country=fields.get("job_country"),
                location_string=fields.get("location_string"),
                score=hit._score,
            )
            job_vector_stores.append(job_vector_store)
        return job_vector_stores
