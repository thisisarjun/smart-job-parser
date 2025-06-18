from typing import List

from src.data_transformer.interface import BaseTransformer
from src.job_searcher.vendors.jsearch.models import Job
from src.vector_store.models import JobVectorStore


class DataTransformerService:
    def __init__(self, transformer: BaseTransformer):
        self.transformer = transformer

    def transform(self, data: List[Job]) -> List[JobVectorStore]:
        return self.transformer.transform(data)
