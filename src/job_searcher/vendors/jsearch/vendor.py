# TODO: make everything async
import logging
from typing import Any, Dict, List, Optional

import httpx

from config import settings
from src.job_searcher.interface import JobSearchVendor
from src.job_searcher.models import JobDetails
from src.job_searcher.vendors.jsearch.models import Job as JSearchJob
from src.job_searcher.vendors.jsearch.models import SearchParams, SearchResponse

# TODO: remove this
logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)


class JSearchVendor(JobSearchVendor):
    """JSearch API implementation for job searching via RapidAPI"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = settings.JSEARCH_API_KEY
        if not self.api_key:
            raise ValueError(
                "RapidAPI key is required. Set JSEARCH_API_KEY environment variable."
            )

        # Using the RapidAPI endpoint from the curl example
        self.base_url = settings.JSEARCH_BASE_URL
        self.jsearch_header_host = settings.JSEARCH_HEADER_HOST
        self.headers = {
            "x-rapidapi-host": self.jsearch_header_host,
            "x-rapidapi-key": self.api_key,
        }

    def _convert_to_job_details(self, jsearch_job: JSearchJob) -> JobDetails:
        """Convert JSearch job to JobDetails model"""
        return JobDetails(
            job_id=jsearch_job.job_id,
            title=jsearch_job.job_title,
            description=jsearch_job.job_description,
            location=jsearch_job.location_string,
            company=jsearch_job.employer_name or "Unknown Company",
            job_url=jsearch_job.job_apply_link,
            country=jsearch_job.job_country,
            city=jsearch_job.job_city,
            state=jsearch_job.job_state,
        )

    def search_jobs(
        self, query: str, filters: Optional[Dict[str, Any]] = None
    ) -> List[JobDetails]:
        """Search for jobs using JSearch API via RapidAPI"""
        try:
            search_params = SearchParams(query=query)
            if filters is not None:
                search_params.country = filters.get("country")

            # Make synchronous request
            with httpx.Client() as client:
                query_params = search_params.to_jsearch_params()
                query_params.update({"date_posted": "all"})
                # TODO: remove this
                logging.info(f"Query params: {query_params}")
                logging.info(f"Headers: {self.headers}")
                logging.info(f"Base URL: {self.base_url}")
                response = client.get(
                    f"{self.base_url}/search",
                    headers=self.headers,
                    params=query_params,
                    timeout=30.0,
                )
                response.raise_for_status()

                # Parse response
                data = response.json()
                search_response = SearchResponse(**data)

                # Return converted JobDetails
                return [
                    self._convert_to_job_details(job) for job in search_response.data
                ]

        except httpx.HTTPStatusError as e:
            raise Exception(
                f"JSearch API error: {e.response.status_code} - {e.response.text}"
            )
        except httpx.RequestError as e:
            raise Exception(f"JSearch API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"JSearch API unexpected error: {str(e)}")

    def get_job_details(self, job_id: str) -> JobDetails:
        """Get detailed information about a specific job"""
        try:
            with httpx.Client() as client:
                params = {"job_id": job_id}

                response = client.get(
                    f"{self.base_url}/job-details",
                    headers=self.headers,
                    params=params,
                    timeout=30.0,
                )
                response.raise_for_status()

                # Parse response
                data = response.json()

                # Extract the first job from the response
                if data.get("data") and len(data["data"]) > 0:
                    job_data = data["data"][0]
                    jsearch_job = JSearchJob(**job_data)
                    return self._convert_to_job_details(jsearch_job)
                else:
                    raise Exception("Job not found")

        except httpx.HTTPStatusError as e:
            raise Exception(
                f"JSearch API error: {e.response.status_code} - {e.response.text}"
            )
        except httpx.RequestError as e:
            raise Exception(f"JSearch API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"JSearch API unexpected error: {str(e)}")

    def get_vendor_name(self) -> str:
        return "jsearch"
