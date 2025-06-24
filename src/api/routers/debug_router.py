from typing import Any, Dict

from fastapi import APIRouter, Depends

from src.api.dependencies import get_job_search_service, get_jsearch_vendor, get_vector_store_service
from src.job_searcher.vendors.jsearch.vendor import JSearchVendor
from src.services.job_search_service import JobSearchService
from src.vector_store.models import JobVectorStore
from src.vector_store.service import VectorStoreService

router = APIRouter()


@router.post("/debug/vector_store/add_job_details")
async def debug_add_job_details(
    vector_store_service: VectorStoreService = Depends(get_vector_store_service),  # noqa: B008
) -> Dict[str, str]:
    vector_store_service.add_job_details(
        job_details=JobVectorStore(
            job_id="2",
            job_title="Software Engineer",
            job_description=(
                "We are looking for a software engineer with 3 years of " "experience in Python and Django."
            ),
            job_apply_link="https://www.google.com",
            employer_name="Google",
            job_city="San Francisco",
            job_state="CA",
            job_country="USA",
            location_string="San Francisco, CA, USA",
        )
    )
    return {"message": "Debug endpoint"}


@router.get("/debug/vector_store/similarity_search")
async def debug_similarity_search(
    vector_store_service: VectorStoreService = Depends(get_vector_store_service),  # noqa: B008
) -> Any:
    results = vector_store_service.similarity_search(
        query="We are looking for a software engineer with 3 years of experience in Python and Django."  # noqa: E501
    )
    return results


@router.get("/debug/job_searcher/search_jobs")
async def debug_search_jobs(
    jsearch_vendor: JSearchVendor = Depends(get_jsearch_vendor),  # noqa: B008
) -> Any:
    results = jsearch_vendor.search_jobs(
        query="Senior Software Engineer visa sponsorship",  # noqa: E501
        filters={"country": "de"},
    )
    return results


@router.get("/debug/job_searcher/search_relevant_jobs")
async def debug_search_relevant_jobs(
    query: str,
    country: str,
    job_search_service: JobSearchService = Depends(get_job_search_service),  # noqa: B008
) -> Any:
    results = job_search_service.search_relevant_jobs(
        query=query,
        filters={"country": country},
    )
    return results
