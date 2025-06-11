from typing import Dict

from fastapi import APIRouter
from langchain_community.embeddings import OllamaEmbeddings

from src.vector_store.models import AvailableVectorStores, JobVectorStore
from src.vector_store.service import VectorStoreService

router = APIRouter()

vector_store_service = VectorStoreService(
    vector_store_type=AvailableVectorStores.MEMORY,
    embedding=OllamaEmbeddings(model="mxbai-embed-large"),
)


@router.get("/debug/vector_store/add_job_details")
async def debug() -> Dict[str, str]:
    vector_store_service.add_job_details(
        job_details=JobVectorStore(
            job_id="1",
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
