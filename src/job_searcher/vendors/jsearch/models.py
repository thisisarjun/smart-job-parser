from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DatePosted(str, Enum):
    ALL = "all"
    TODAY = "today"
    THREE_DAYS = "3days"
    WEEK = "week"
    MONTH = "month"


class EmploymentType(str, Enum):
    FULLTIME = "FULLTIME"
    CONTRACTOR = "CONTRACTOR"
    PARTTIME = "PARTTIME"
    INTERN = "INTERN"


class JobRequirement(str, Enum):
    UNDER_3_YEARS = "under_3_years_experience"
    MORE_THAN_3_YEARS = "more_than_3_years_experience"
    NO_EXPERIENCE = "no_experience"
    NO_DEGREE = "no_degree"


class SearchParams(BaseModel):
    """Input parameters for job search"""

    query: str = Field(..., description="Search query (job title and location)")
    page: int = Field(default=1, ge=1, description="Page number")
    date_posted: DatePosted = Field(default=DatePosted.ALL, description="Filter by posting date")
    remote_jobs_only: bool = Field(default=False, description="Find remote jobs only")
    employment_types: Optional[List[EmploymentType]] = Field(default=None, description="Employment types filter")
    job_requirements: Optional[List[JobRequirement]] = Field(default=None, description="Job requirements filter")
    radius: Optional[int] = Field(default=None, ge=1, description="Search radius in km")
    num_pages: int = Field(default=1, ge=1, le=20, description="Number of pages to fetch")
    country: Optional[str] = Field(default=None, description="Country filter")

    def to_jsearch_params(self) -> Dict[str, Any]:
        """Convert to JSearch API parameters"""
        params = {"query": self.query}

        if self.page:
            params["page"] = str(self.page)
        if self.date_posted and self.date_posted != DatePosted.ALL:
            params["date_posted"] = self.date_posted.value
        if self.remote_jobs_only:
            params["remote_jobs_only"] = "true"
        if self.employment_types:
            params["employment_types"] = ",".join([et.value for et in self.employment_types])
        if self.job_requirements:
            params["job_requirements"] = ",".join([jr.value for jr in self.job_requirements])
        if self.radius:
            params["radius"] = str(self.radius)
        if self.num_pages:
            params["num_pages"] = str(self.num_pages)
        if self.country:
            params["country"] = self.country

        return params


class Job(BaseModel):
    """JSearch job model representing a job posting"""

    # Basic job information
    job_id: str
    job_title: str
    job_description: str
    job_apply_link: str

    # Employer information
    employer_name: Optional[str] = None

    # Location
    job_city: Optional[str] = None
    job_state: Optional[str] = None
    job_country: Optional[str] = None

    @property
    def location_string(self) -> str:
        """Get formatted location string"""
        parts = []
        if self.job_city:
            parts.append(self.job_city)
        if self.job_state:
            parts.append(self.job_state)
        if self.job_country:
            parts.append(self.job_country)
        return ", ".join(parts) if parts else "Location not specified"


class SearchResponse(BaseModel):
    """Response from job search API"""

    status: str
    request_id: str
    parameters: Dict[str, Any]
    data: List[Job]

    @property
    def total_jobs(self) -> int:
        """Get total number of jobs returned"""
        return len(self.data)
