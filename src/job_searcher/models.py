from enum import Enum
from typing import Optional

from pydantic import BaseModel


class JobDetails(BaseModel):
    job_id: str
    title: str
    description: str
    location: str
    company: str
    job_url: str
    city: Optional[str] = (None,)
    state: Optional[str] = (None,)
    country: Optional[str] = (None,)


# Add vendor list to the models
class VendorList(Enum):
    JSEARCH = "jsearch"
