import os
from typing import List, Optional
import httpx
from ...interface import JobSearchVendor
from ...models import JobDetails
from .models import Job as JSearchJob, SearchParams, SearchResponse


class JSearchClient(JobSearchVendor):
    """JSearch API implementation for job searching"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("JSEARCH_API_KEY")
        if not self.api_key:
            raise ValueError("JSearch API key is required. Set JSEARCH_API_KEY environment variable.")
        
        # Using the Zyla Labs endpoint from the documentation
        self.base_url = "https://zylalabs.com/api/2526/jsearch+api"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _convert_to_job_details(self, jsearch_job: JSearchJob) -> JobDetails:
        """Convert JSearch job to JobDetails model"""
        return JobDetails(
            title=jsearch_job.job_title,
            description=jsearch_job.job_description,
            location=jsearch_job.location_string,
            company=jsearch_job.employer_name or "Unknown Company",
            job_url=jsearch_job.job_apply_link
        )
    
    def search_jobs(self, query: str) -> List[JobDetails]:
        """Search for jobs using JSearch API"""
        try:
            # Create search parameters with the query
            search_params = SearchParams(query=query)
            
            # Make synchronous request
            with httpx.Client() as client:
                query_params = search_params.to_jsearch_params()
                
                response = client.get(
                    f"{self.base_url}/2516/search",
                    headers=self.headers,
                    params=query_params,
                    timeout=30.0
                )
                response.raise_for_status()
                
                # Parse response
                data = response.json()
                search_response = SearchResponse(**data)
                
                # Convert to JobDetails
                return [self._convert_to_job_details(job) for job in search_response.data]
                
        except httpx.HTTPStatusError as e:
            raise Exception(f"JSearch API error: {e.response.status_code} - {e.response.text}")
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
                    f"{self.base_url}/2517/job+details",
                    headers=self.headers,
                    params=params,
                    timeout=30.0
                )
                response.raise_for_status()
                
                # Parse response - assuming similar structure to search response
                data = response.json()
                
                # Extract the first job from the response
                if data.get("data") and len(data["data"]) > 0:
                    job_data = data["data"][0]
                    jsearch_job = JSearchJob(**job_data)
                    return self._convert_to_job_details(jsearch_job)
                else:
                    raise Exception("Job not found")
                
        except httpx.HTTPStatusError as e:
            raise Exception(f"JSearch API error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            raise Exception(f"JSearch API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"JSearch API unexpected error: {str(e)}")
    
    def get_vendor_name(self) -> str:
        return "jsearch" 