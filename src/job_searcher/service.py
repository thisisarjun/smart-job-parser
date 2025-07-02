import hashlib
from typing import Any, Dict, List, Optional

from src.job_searcher.interface import JobSearchVendor
from src.job_searcher.models import JobDetails
from src.logger import get_logger

logger = get_logger(__name__)


class JobSearcher:
    def __init__(self, vendor: JobSearchVendor):
        self.vendor = vendor
        logger.info(f"JobSearcher initialized with vendor: {vendor.get_vendor_name()}")

    async def search_jobs(self, query: Optional[str], filters: Optional[Dict[str, Any]] = None) -> List[JobDetails]:
        logger.debug(f"Searching jobs with query: '{query}', filters: {filters}")

        if query is None:
            logger.warning("Search query is None, returning empty results")
            return []

        try:
            results = await self.vendor.search_jobs(query, filters)

            # Handle case where vendor returns None
            if results is None:
                logger.warning(f"Vendor returned None for query: '{query}', returning empty list")
                return []

            logger.info(f"Found {len(results)} jobs for query: '{query}'")
            return results
        except Exception as e:
            logger.error(f"Error searching jobs for query '{query}': {str(e)}")
            raise

    def deduplicate_jobs(self, jobs: Optional[List[JobDetails]] = None) -> List[JobDetails]:
        if jobs is None:
            return []
        job_hashes = set()
        deduplicated_jobs = []
        for job in jobs:
            job_hash = hashlib.sha256(job.job_url.encode()).hexdigest()
            if job_hash in job_hashes:
                continue
            job_hashes.add(job_hash)
            deduplicated_jobs.append(job)
        logger.info(f"Deduplicated {len(jobs)} jobs to {len(deduplicated_jobs)} jobs")
        return deduplicated_jobs
