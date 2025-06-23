from functools import lru_cache

from src.job_searcher.service import JobSearcher
from src.job_searcher.vendors.jsearch.vendor import JSearchVendor
from src.services.job_search_service import JobSearchService
from src.vector_store.service import VectorStoreService
from src.vector_store.stores.pinecone_store import PineconeStore
from src.vector_transformer.service import DataTransformerService
from src.vector_transformer.transformers.jsearch_transformer import JSearchTransformer


@lru_cache()
def get_vector_store_service() -> VectorStoreService:
    """Dependency to get VectorStoreService instance"""
    return VectorStoreService(PineconeStore())


# TODO: remove this dependency
@lru_cache()
def get_jsearch_vendor() -> JSearchVendor:
    """Dependency to get JSearchVendor instance"""
    return JSearchVendor()


@lru_cache()
def get_data_transformer_service() -> DataTransformerService:
    """Dependency to get DataTransformerService instance"""
    return DataTransformerService(JSearchTransformer())


@lru_cache()
def get_job_searcher() -> JobSearcher:
    """Dependency to get JobSearcher instance"""
    return JobSearcher(vendor=get_jsearch_vendor())


@lru_cache()
def get_job_search_service() -> JobSearchService:
    """Dependency to get JobSearchService instance"""
    return JobSearchService(
        job_searcher=get_job_searcher(),
        vector_store_service=get_vector_store_service(),
        data_transformer_service=get_data_transformer_service(),
    )
