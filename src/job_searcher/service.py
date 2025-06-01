from typing import List
from src.job_searcher.interface import JobSearchVendor


class JobSearchService:
    
    def __init__(self, vendors: List[JobSearchVendor]):
        self.vendors = vendors

    def search_jobs(self, query: str) -> List[JobDetails]:
        return self.vendors[0].search_jobs(query)
