from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from src.job_searcher.models import JobDetails


class JobSearchVendor(ABC):
    @abstractmethod
    async def search_jobs(self, query: Optional[str], filters: Optional[Dict[str, Any]] = None) -> List[JobDetails]:
        pass

    @abstractmethod
    async def get_job_details(self, job_id: str) -> JobDetails:
        pass

    @abstractmethod
    def get_vendor_name(self) -> str:
        pass
