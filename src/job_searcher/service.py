from typing import Any, Dict, List, Optional

from src.job_searcher.interface import JobSearchVendor
from src.job_searcher.models import JobDetails


class JobSearcher:
    def __init__(self, vendor: JobSearchVendor):
        self.vendor = vendor

    def search_jobs(
        self, query: Optional[str], filters: Optional[Dict[str, Any]] = None
    ) -> List[JobDetails]:
        if query is None:
            return []
        return self.vendor.search_jobs(query, filters)
