from typing import Any

from fastapi import APIRouter, Depends

from src.api.dependencies import get_job_search_service
from src.services.job_search_service import JobSearchService

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def search_relevant_jobs(
    query: str,
    country: str,
    job_search_service: JobSearchService = Depends(get_job_search_service),  # noqa: B008
) -> Any:
    results = await job_search_service.search_relevant_jobs(
        query=query,
        filters={"country": country},
    )
    return results
