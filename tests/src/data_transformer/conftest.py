import pytest

from src.job_searcher.vendors.jsearch.models import Job
from tests.factories.search_vendors import JSearchJobFactory


@pytest.fixture
def sample_jsearch_jobs() -> list[Job]:
    """Create JSearchJob objects from fixture data"""
    return JSearchJobFactory.batch(3)


@pytest.fixture
def single_jsearch_job() -> Job:
    """Create single JSearchJob object from fixture data"""
    return JSearchJobFactory.build()
