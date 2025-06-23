from typing import List

from src.data_transformer.interface import BaseTransformer
from src.job_searcher.models import JobDetails
from src.vector_store.models import JobVectorStore


class JSearchTransformer(BaseTransformer):
    def transform(self, data: List[JobDetails]) -> List[JobVectorStore]:
        return [
            JobVectorStore(
                job_id=job_detail.job_id,
                job_title=job_detail.title,
                job_description=job_detail.description,
                job_apply_link=job_detail.apply_link,
                employer_name=job_detail.company,
                job_city=job_detail.city,
                job_state=job_detail.state,
                job_country=job_detail.country,
                location_string=job_detail.location,
            )
            for job_detail in data
        ]
