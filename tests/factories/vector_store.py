from polyfactory.factories.pydantic_factory import ModelFactory

from src.vector_store.models import JobVectorStore


class JobVectorStoreFactory(ModelFactory[JobVectorStore]):
    __model__ = JobVectorStore
