from typing import Any, Dict, Optional

from src.job_searcher.models import JobDetails
from src.job_searcher.service import JobSearcher
from src.vector_store.service import VectorStoreService
from src.vector_store.vector_transformer.service import VectorTransformerService


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

    def search_relevant_jobs(
        self, query: str, filters: Optional[Dict[str, Any]] = None
    ) -> list[JobDetails]:
        jobs = self.job_searcher.search_jobs(query, filters)
        # transform jobs to job vector store
        if not jobs:
            return []
        job_vector_stores = self.vector_transformer_service.transform(jobs)
        self.vector_store_service.add_job_details(job_vector_stores)
        return jobs
