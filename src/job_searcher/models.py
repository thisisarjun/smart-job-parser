from pydantic import BaseModel


class JobDetails(BaseModel):
    title: str
    description: str
    location: str
    company: str
    job_url: str
