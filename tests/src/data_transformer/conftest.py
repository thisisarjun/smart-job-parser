import pytest

from src.job_searcher.vendors.jsearch.models import Job
from tests.fixtures.jsearch_result import sample_jsearch_result


@pytest.fixture
def sample_jsearch_jobs():
    """Create JSearchJob objects from fixture data"""
    jobs = []
    for job_data in sample_jsearch_result["data"][:3]:  # Use first 3 jobs
        job = Job(
            job_id=job_data["job_id"],
            job_title=job_data["job_title"],
            job_description=job_data["job_description"],
            job_apply_link=job_data["job_apply_link"],
            employer_name=job_data["employer_name"],
            job_city=job_data["job_city"],
            job_state=job_data["job_state"],
            job_country=job_data["job_country"],
        )
        jobs.append(job)
    return jobs


@pytest.fixture
def single_jsearch_job():
    """Create single JSearchJob object from fixture data"""
    job_data = sample_jsearch_result["data"][0]  # First job from fixture
    return Job(
        job_id=job_data["job_id"],
        job_title=job_data["job_title"],
        job_description=job_data["job_description"],
        job_apply_link=job_data["job_apply_link"],
        employer_name=job_data["employer_name"],
        job_city=job_data["job_city"],
        job_state=job_data["job_state"],
        job_country=job_data["job_country"],
    )
