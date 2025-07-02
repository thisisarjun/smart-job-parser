from typing import List
from unittest.mock import AsyncMock, Mock

import pytest

from src.job_searcher.interface import JobSearchVendor
from src.job_searcher.models import JobDetails
from tests.factories.job_searcher import JobDetailsFactory


@pytest.fixture
def sample_job_details() -> List[JobDetails]:
    """Sample job details for testing"""
    return JobDetailsFactory.batch(5)


@pytest.fixture
def mock_vendor(sample_job_details) -> Mock:
    """Create a mock vendor for testing"""
    vendor = Mock(spec=JobSearchVendor)
    vendor.search_jobs = AsyncMock(return_value=sample_job_details)
    vendor.get_job_details = AsyncMock(return_value=sample_job_details[0])
    vendor.get_vendor_name.return_value = "test_vendor"
    return vendor
