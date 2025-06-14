from typing import Any, Dict

from fastapi import APIRouter

from src.vector_store.models import JobVectorStore
from src.vector_store.service import VectorStoreService
from src.vector_store.stores.pinecone_store import PineconeStore

router = APIRouter()

vector_store_service = VectorStoreService(PineconeStore())


@router.post("/debug/vector_store/add_job_details")
async def debug_add_job_details() -> Dict[str, str]:
    vector_store_service.add_job_details(
        job_details=JobVectorStore(
            job_id="2",
            job_title="Software Engineer",
            job_description=(
                "We are looking for a software engineer with 3 years of "
                "experience in Python and Django."
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
async def debug_similarity_search() -> Any:
    results = vector_store_service.similarity_search(
        query="We are looking for a software engineer with 3 years of experience in Python and Django."  # noqa: E501
    )
    return results
