from enum import Enum

from pydantic import BaseModel


class JobDetails(BaseModel):
    title: str
    description: str
    location: str
    company: str
    job_url: str


# Add vendor list to the models
class VendorList(Enum):
    JSEARCH = "jsearch"
