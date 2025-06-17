from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from src.job_searcher.models import JobDetails


class JobSearchVendor(ABC):
    @abstractmethod
    def search_jobs(
        self, query: str, filters: Optional[Dict[str, Any]]
    ) -> List[JobDetails]:
        pass

    @abstractmethod
    def get_job_details(self, job_id: str) -> JobDetails:
        pass

    @abstractmethod
    def get_vendor_name(self) -> str:
        pass
