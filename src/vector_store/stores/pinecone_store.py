from pinecone import Index, Pinecone

from src.config import config
from src.vector_store.interface import VectorStore
from src.vector_store.models import JobVectorStore


class PineconeStore(VectorStore):
    index: Index
    namespace: str

    def __init__(self):
        api_key = config["PINECONE_API_KEY"]
        index_name = config["PINECONE_INDEX"]
        # pinecone already has an embedding model
        pc = Pinecone(api_key=api_key)
        self.index = pc.Index(index_name)
        self.namespace = config["PINECONE_NAMESPACE"]

    def add_job_details(self, job_details: JobVectorStore) -> None:
        # TODO: better use of id, and testing required for this method
        record_id = job_details.job_id
        self.index.upsert_records(
            self.namespace,
            [
                {
                    "id": record_id,
                    "description": job_details.get_combined_text_document(),
                    **job_details.model_dump(),
                }
            ],
        )

    def similarity_search(self, query: str) -> list[JobVectorStore]:
        # TODO: need to test this
        reranked_results = self.index.search(
            namespace=self.namespace,
            query={"top_k": 5, "inputs": {"text": query}},
            rerank={
                "model": "bge-reranker-v2-m3",
                "top_n": 5,
                "rank_fields": ["job_description"],
            },
            fields=["job_description"],
        )
        return reranked_results
