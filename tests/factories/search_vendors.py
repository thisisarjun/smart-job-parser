from polyfactory.factories.pydantic_factory import ModelFactory

from src.job_searcher.vendors.jsearch.models import Job, SearchResponse


class JSearchJobFactory(ModelFactory[Job]):
    __model__ = Job


class JSearchSearchResponseFactory(ModelFactory[SearchResponse]):
    __model__ = SearchResponse
