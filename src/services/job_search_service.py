from typing import Any, Dict, Optional

from src.job_searcher.models import JobDetails
from src.job_searcher.service import JobSearcher
from src.logger import get_logger
from src.vector_store.service import VectorStoreService
from src.vector_store.vector_transformer.service import VectorTransformerService

logger = get_logger(__name__)


class JobSearchService:
    def __init__(
        self,
        job_searcher: JobSearcher,
        vector_store_service: VectorStoreService,
        vector_transformer_service: VectorTransformerService,
    ):
        self.job_searcher = job_searcher
        self.vector_store_service = vector_store_service
        self.vector_transformer_service = vector_transformer_service

    def get_semantic_search_query(self, query: str, filters: Optional[Dict[str, Any]] = None) -> str:
        query = f"{query}"
        if filters:
            for key, value in filters.items():
                query += f" {key}: {value}"
        return query

    def search_relevant_jobs(self, query: str, filters: Optional[Dict[str, Any]] = None) -> list[JobDetails]:
        jobs = self.job_searcher.search_jobs(query, filters)
        deduplicated_jobs = self.job_searcher.deduplicate_jobs(jobs)
        # transform jobs to job vector store
        if not deduplicated_jobs:
            return []
        job_vector_stores = self.vector_transformer_service.transform(deduplicated_jobs)
        self.vector_store_service.add_job_details(job_vector_stores)
        semantic_search_query = self.get_semantic_search_query(query, filters)
        logger.info(f"Semantic search query: {semantic_search_query}")
        semantic_search_results = self.vector_store_service.similarity_search(semantic_search_query)
        logger.info(f"Semantic search results: {semantic_search_results}")
        return semantic_search_results
