from typing import List

from src.data_transformer.interface import BaseTransformer
from src.job_searcher.vendors.jsearch.models import Job
from src.vector_store.models import JobVectorStore


class JSearchTransformer(BaseTransformer):
    def transform(self, data: List[Job]) -> List[JobVectorStore]:
        return [
            JobVectorStore(
                job_id=job.job_id,
                job_title=job.job_title,
                job_description=job.job_description,
                job_apply_link=job.job_apply_link,
                employer_name=job.employer_name,
                job_city=job.job_city,
                job_state=job.job_state,
                job_country=job.job_country,
                location_string=job.location_string,
            )
            for job in data
        ]
