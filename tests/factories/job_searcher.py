from polyfactory.factories.pydantic_factory import ModelFactory

from src.job_searcher.models import JobDetails


class JobDetailsFactory(ModelFactory[JobDetails]):
    __model__ = JobDetails
