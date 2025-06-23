from typing import Any, Dict, Optional

from src.data_transformer.service import DataTransformerService
from src.job_searcher.models import JobDetails
from src.job_searcher.service import JobSearcher
from src.vector_store.service import VectorStoreService


class JobSearchService:
    def __init__(
        self,
        job_searcher: JobSearcher,
        vector_store_service: VectorStoreService,
        data_transformer_service: DataTransformerService,
    ):
        self.job_searcher = job_searcher
        self.vector_store_service = vector_store_service
        self.data_transformer_service = data_transformer_service

    def search_relevant_jobs(
        self, query: str, filters: Optional[Dict[str, Any]] = None
    ) -> list[JobDetails]:
        jobs = self.job_searcher.search_jobs(query, filters)
        # transform jobs to job vector store
        if not jobs:
            return []
        job_vector_stores = self.data_transformer_service.transform(jobs)
        self.vector_store_service.add_job_details(job_vector_stores)
        return jobs
