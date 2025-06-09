from typing import List
from unittest.mock import Mock

import pytest

from src.job_searcher.interface import JobSearchVendor
from src.job_searcher.models import JobDetails


@pytest.fixture
def sample_job_details() -> List[JobDetails]:
    """Sample job details for testing"""
    return [
        JobDetails(
            title="Software Developer",
            description="Develop software applications",
            location="Chicago, IL",
            company="Tech Corp",
            job_url="https://example.com/job1",
        ),
        JobDetails(
            title="Frontend Developer",
            description="Build user interfaces",
            location="New York, NY",
            company="Web Solutions",
            job_url="https://example.com/job2",
        ),
    ]


@pytest.fixture
def mock_vendor(sample_job_details) -> Mock:
    """Create a mock vendor for testing"""
    vendor = Mock(spec=JobSearchVendor)
    vendor.search_jobs.return_value = sample_job_details
    vendor.get_vendor_name.return_value = "test_vendor"
    return vendor
