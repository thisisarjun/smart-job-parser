from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


class JobVectorStore(BaseModel):
    job_id: str
    job_title: str
    job_description: str
    job_apply_link: str
    employer_name: Optional[str] = None
    job_city: Optional[str] = None
    job_state: Optional[str] = None
    job_country: Optional[str] = None
    location_string: Optional[str] = None

    def get_combined_text_document(self) -> str:
        return (
            f"Job Title: {self.job_title}\n"
            f"Company: {self.employer_name}\n"
            f"Location: {self.location_string}\n\n"
            f"Description: {self.job_description}"
        )

    def get_metadata(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "job_title": self.job_title,
            "employer_name": self.employer_name,
            "job_city": self.job_city,
            "job_state": self.job_state,
            "job_country": self.job_country,
            "job_apply_link": self.job_apply_link,
        }


class AvailableVectorStores(Enum):
    MEMORY = "memory"
    PINECONE = "pinecone"
