from typing import List, Optional

from src.job_searcher.interface import JobSearchVendor
from src.job_searcher.models import JobDetails


class JobSearchService:
    def __init__(self, vendor: JobSearchVendor):
        self.vendor = vendor

    def search_jobs(self, query: Optional[str]) -> List[JobDetails]:
        if query is None:
            return []
        return self.vendor.search_jobs(query)
