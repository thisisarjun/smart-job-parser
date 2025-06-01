from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from src.job_searcher.models import Job, SearchParams, EstimatedSalaryParams, EstimatedSalary
from src.job_searcher.vendors.jsearch import (
    JSearchVendor, DatePosted, EmploymentType, JobRequirement
)

router = APIRouter()


@router.get("/search", response_model=List[Job])
async def search_jobs(
    query: str = Query(..., description="Search query (job title and location)"),
    page: Optional[int] = Query(1, ge=1, description="Page number"),
    date_posted: Optional[DatePosted] = Query(DatePosted.ALL, description="Filter by posting date"),
    remote_jobs_only: Optional[bool] = Query(False, description="Find remote jobs only"),
    employment_types: Optional[str] = Query(None, description="Employment types (comma-separated)"),
    job_requirements: Optional[str] = Query(None, description="Job requirements (comma-separated)"),
    radius: Optional[int] = Query(None, ge=1, description="Search radius in km"),
    num_pages: Optional[int] = Query(1, ge=1, le=20, description="Number of pages to fetch")
):
    """Search for jobs using JSearch API"""
    try:
        # Parse employment types
        employment_types_list = None
        if employment_types:
            employment_types_list = [EmploymentType(et.strip()) for et in employment_types.split(",")]
        
        # Parse job requirements
        job_requirements_list = None
        if job_requirements:
            job_requirements_list = [JobRequirement(jr.strip()) for jr in job_requirements.split(",")]
        
        # Create JSearch-specific filters
        jsearch_filters = {}
        if date_posted and date_posted != DatePosted.ALL:
            jsearch_filters["date_posted"] = date_posted
        if remote_jobs_only:
            jsearch_filters["remote_jobs_only"] = remote_jobs_only
        if employment_types_list:
            jsearch_filters["employment_types"] = employment_types_list
        if job_requirements_list:
            jsearch_filters["job_requirements"] = job_requirements_list
        if radius:
            jsearch_filters["radius"] = radius
        
        # Create generic search parameters
        search_params = SearchParams(
            query=query,
            page=page,
            num_pages=num_pages,
            filters=jsearch_filters
        )
        
        # Initialize JSearch vendor and search
        jsearch = JSearchVendor()
        jobs = await jsearch.search_jobs(search_params)
        
        return jobs
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/job/{job_id}", response_model=Job)
async def get_job_details(job_id: str):
    """Get detailed information about a specific job"""
    try:
        jsearch = JSearchVendor()
        job = await jsearch.get_job_details(job_id)
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return job
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get job details: {str(e)}")


@router.get("/salary-estimate", response_model=List[EstimatedSalary])
async def get_estimated_salary(
    job_title: str = Query(..., description="Job title for salary estimation"),
    location: str = Query(..., description="Location for salary estimation"),
    radius: Optional[int] = Query(200, ge=1, description="Search radius in km")
):
    """Get estimated salary information for a job title and location"""
    try:
        # Create JSearch-specific additional parameters
        jsearch_params = {"radius": radius}
        
        salary_params = EstimatedSalaryParams(
            job_title=job_title,
            location=location,
            additional_params=jsearch_params
        )
        
        jsearch = JSearchVendor()
        salaries = await jsearch.get_estimated_salary(salary_params)
        
        return salaries
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get salary estimates: {str(e)}")


@router.get("/health")
async def health_check():
    """Check if the JSearch API is accessible"""
    try:
        jsearch = JSearchVendor()
        is_healthy = await jsearch.health_check()
        
        return {
            "vendor": jsearch.vendor_name,
            "status": "healthy" if is_healthy else "unhealthy",
            "features": jsearch.get_supported_features(),
            "rate_limits": jsearch.get_rate_limits()
        }
        
    except Exception as e:
        return {
            "vendor": "jsearch",
            "status": "error",
            "error": str(e)
        } 