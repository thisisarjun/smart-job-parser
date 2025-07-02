from typing import Any, Dict, List, Optional
from unittest.mock import Mock

import pytest

from src.job_searcher.interface import JobSearchVendor
from src.job_searcher.models import JobDetails
from src.job_searcher.service import JobSearcher
from tests.factories.job_searcher import JobDetailsFactory


class TestJobSearcher:
    """Test cases for JobSearcher"""

    def test_init_with_vendor(self, mock_vendor):
        """Test initialization with a vendor"""
        service = JobSearcher(vendor=mock_vendor)

        assert service.vendor == mock_vendor

    @pytest.mark.asyncio
    async def test_search_jobs_with_vendor(self, mock_vendor, sample_job_details):
        """Test search_jobs with a vendor"""
        service = JobSearcher(vendor=mock_vendor)
        query = "python developer"

        result = await service.search_jobs(query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(query, None)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "query",
        [
            "python developer",
            "frontend engineer",
            "data scientist",
            "DevOps engineer",
            "java spring boot",
        ],
    )
    async def test_search_jobs_with_different_queries(self, mock_vendor, sample_job_details, query):
        """Test search_jobs with various query strings"""
        service = JobSearcher(vendor=mock_vendor)

        result = await service.search_jobs(query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(query, None)

    @pytest.mark.asyncio
    async def test_search_jobs_returns_empty_list(self, mock_vendor):
        """Test search_jobs when vendor returns empty list"""
        mock_vendor.search_jobs.return_value = []
        service = JobSearcher(vendor=mock_vendor)

        result = await service.search_jobs("nonexistent job")

        assert result == []
        assert isinstance(result, list)
        mock_vendor.search_jobs.assert_called_once_with("nonexistent job", None)

    @pytest.mark.asyncio
    async def test_search_jobs_preserves_vendor_exceptions(self, mock_vendor):
        """Test that search_jobs preserves exceptions from vendor"""
        mock_vendor.search_jobs.side_effect = ValueError("API error")
        service = JobSearcher(vendor=mock_vendor)

        with pytest.raises(ValueError, match="API error"):
            await service.search_jobs("test query")

    @pytest.mark.asyncio
    async def test_search_jobs_delegates_to_vendor(self, mock_vendor, sample_job_details):
        """Test that search_jobs properly delegates to the vendor"""
        service = JobSearcher(vendor=mock_vendor)
        query = "react developer"

        result = await service.search_jobs(query)

        # Verify the call was made with correct parameters
        mock_vendor.search_jobs.assert_called_once_with(query, None)
        # Verify the result is returned unchanged
        assert result == sample_job_details
        assert result is mock_vendor.search_jobs.return_value

    @pytest.mark.asyncio
    async def test_search_jobs_with_complex_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with complex query string"""
        service = JobSearcher(vendor=mock_vendor)
        complex_query = "senior python developer remote full-time"

        result = await service.search_jobs(complex_query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(complex_query, None)

    @pytest.mark.asyncio
    async def test_search_jobs_with_empty_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with empty query string"""
        service = JobSearcher(vendor=mock_vendor)

        result = await service.search_jobs("")

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with("", None)

    @pytest.mark.asyncio
    async def test_search_jobs_multiple_calls(self, mock_vendor, sample_job_details):
        """Test multiple calls to search_jobs"""
        service = JobSearcher(vendor=mock_vendor)

        # First call
        result1 = await service.search_jobs("python")
        # Second call
        result2 = await service.search_jobs("javascript")

        assert result1 == sample_job_details
        assert result2 == sample_job_details

        # Verify both calls were made
        assert mock_vendor.search_jobs.call_count == 2
        mock_vendor.search_jobs.assert_any_call("python", None)
        mock_vendor.search_jobs.assert_any_call("javascript", None)

    @pytest.mark.asyncio
    async def test_search_jobs_with_none_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with None query - should return empty list"""
        service = JobSearcher(vendor=mock_vendor)

        # When query is None, service should return empty list without calling vendor
        result = await service.search_jobs(None)

        assert result == []
        mock_vendor.search_jobs.assert_not_called()

    @pytest.mark.asyncio
    async def test_search_jobs_with_special_characters(self, mock_vendor, sample_job_details):
        """Test search_jobs with special characters in query"""
        service = JobSearcher(vendor=mock_vendor)
        special_query = "C++ developer @$%^&*(){}[]|\\:;\"'<>?,./"

        result = await service.search_jobs(special_query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(special_query, None)

    @pytest.mark.asyncio
    async def test_search_jobs_with_unicode_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with Unicode characters in query"""
        service = JobSearcher(vendor=mock_vendor)
        unicode_query = "développeur python 工程师研发工程师"

        result = await service.search_jobs(unicode_query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(unicode_query, None)

    @pytest.mark.asyncio
    async def test_search_jobs_with_very_long_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with very long query string"""
        service = JobSearcher(vendor=mock_vendor)
        long_query = "python developer " * 100  # Very long query

        result = await service.search_jobs(long_query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(long_query, None)

    def test_service_vendor_attribute_immutable(self, mock_vendor):
        """Test that vendor attribute is properly set and accessible"""
        service = JobSearcher(vendor=mock_vendor)

        # Vendor should be accessible
        assert service.vendor is mock_vendor

        # Should be the same object reference
        assert id(service.vendor) == id(mock_vendor)

    @pytest.mark.asyncio
    async def test_search_jobs_vendor_returns_none(self, mock_vendor):
        """Test search_jobs when vendor returns None (edge case)"""
        mock_vendor.search_jobs.return_value = None
        service = JobSearcher(vendor=mock_vendor)

        result = await service.search_jobs("test query")

        mock_vendor.search_jobs.assert_called_once_with("test query", None)
        assert result == []

    @pytest.mark.asyncio
    async def test_search_jobs_vendor_side_effect_exception_types(self, mock_vendor):
        """Test different exception types from vendor"""
        service = JobSearcher(vendor=mock_vendor)

        # Test different exception types
        exception_types = [
            ValueError("Invalid query"),
            RuntimeError("Network error"),
            KeyError("Missing API key"),
            ConnectionError("Connection failed"),
            TimeoutError("Request timeout"),
        ]

        for exception in exception_types:
            mock_vendor.search_jobs.side_effect = exception

            with pytest.raises(type(exception)):
                await service.search_jobs("test query")

        # Reset after all iterations
        mock_vendor.search_jobs.side_effect = None
        mock_vendor.search_jobs.reset_mock()


class TestJobSearcherIntegration:
    """Integration tests for JobSearcher with real vendor implementations"""

    @pytest.mark.asyncio
    async def test_search_jobs_with_real_vendor_interface(self):
        """Test search_jobs with a real vendor implementation"""

        class TestVendor(JobSearchVendor):
            async def search_jobs(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[JobDetails]:
                # Return sample job details for testing
                return JobDetailsFactory.batch(3)

            async def get_job_details(self, job_id: str) -> JobDetails:
                # Return a single job detail for testing
                return JobDetailsFactory.build()

            def get_vendor_name(self) -> str:
                return "test_vendor"

        vendor = TestVendor()
        service = JobSearcher(vendor=vendor)

        result = await service.search_jobs("python developer")

        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(job, JobDetails) for job in result)

    @pytest.mark.asyncio
    async def test_service_with_different_vendors(self, sample_job_details):
        """Test JobSearcher with different vendor implementations"""

        class VendorA(JobSearchVendor):
            async def search_jobs(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[JobDetails]:
                # VendorA returns first 3 sample jobs
                return sample_job_details[:3]

            async def get_job_details(self, job_id: str) -> JobDetails:
                return sample_job_details[0]

            def get_vendor_name(self) -> str:
                return "vendor_a"

        class VendorB(JobSearchVendor):
            async def search_jobs(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[JobDetails]:
                # VendorB returns last 2 sample jobs
                return sample_job_details[-2:]

            async def get_job_details(self, job_id: str) -> JobDetails:
                return sample_job_details[-1]

            def get_vendor_name(self) -> str:
                return "vendor_b"

        # Test with VendorA
        service_a = JobSearcher(vendor=VendorA())
        result_a = await service_a.search_jobs("test query")
        assert len(result_a) == 3
        assert result_a[0] == sample_job_details[0]

        # Test with VendorB
        service_b = JobSearcher(vendor=VendorB())
        result_b = await service_b.search_jobs("test query")
        assert len(result_b) == 2
        assert result_b[0] == sample_job_details[-2]


class TestJobSearcherDeduplication:
    """Test job deduplication functionality"""

    def test_deduplicate_jobs_empty_list(self):
        """Test deduplication with empty list"""
        # Create a minimal mock vendor for initialization only
        vendor = Mock(spec=JobSearchVendor)
        vendor.get_vendor_name.return_value = "test_vendor"
        service = JobSearcher(vendor=vendor)

        result = service.deduplicate_jobs([])

        assert result == []

    def test_deduplicate_jobs_none_input(self):
        """Test deduplication with None input"""
        # Create a minimal mock vendor for initialization only
        vendor = Mock(spec=JobSearchVendor)
        vendor.get_vendor_name.return_value = "test_vendor"
        service = JobSearcher(vendor=vendor)

        result = service.deduplicate_jobs(None)

        assert result == []

    def test_deduplicate_jobs_no_duplicates(self):
        """Test deduplication with no duplicate jobs"""
        # Create a minimal mock vendor for initialization only
        vendor = Mock(spec=JobSearchVendor)
        vendor.get_vendor_name.return_value = "test_vendor"
        service = JobSearcher(vendor=vendor)

        # Create jobs with different URLs
        jobs = [
            JobDetails(
                job_id="1",
                title="Job 1",
                description="Description 1",
                location="Location 1",
                company="Company 1",
                job_url="https://example.com/job1",
            ),
            JobDetails(
                job_id="2",
                title="Job 2",
                description="Description 2",
                location="Location 2",
                company="Company 2",
                job_url="https://example.com/job2",
            ),
        ]

        result = service.deduplicate_jobs(jobs)

        assert len(result) == 2
        assert result == jobs

    def test_deduplicate_jobs_with_duplicates(self):
        """Test deduplication with duplicate jobs (same URLs)"""
        # Create a minimal mock vendor for initialization only
        vendor = Mock(spec=JobSearchVendor)
        vendor.get_vendor_name.return_value = "test_vendor"
        service = JobSearcher(vendor=vendor)

        # Create jobs with duplicate URLs
        jobs = [
            JobDetails(
                job_id="1",
                title="Job 1",
                description="Description 1",
                location="Location 1",
                company="Company 1",
                job_url="https://example.com/job1",
            ),
            JobDetails(
                job_id="2",
                title="Job 2",
                description="Description 2",
                location="Location 2",
                company="Company 2",
                job_url="https://example.com/job2",
            ),
            JobDetails(
                job_id="3",
                title="Job 1 Duplicate",
                description="Different description",
                location="Different location",
                company="Different company",
                job_url="https://example.com/job1",  # Same URL as first job
            ),
        ]

        result = service.deduplicate_jobs(jobs)

        assert len(result) == 2  # Should remove the duplicate
        assert result[0].job_id == "1"
        assert result[1].job_id == "2"
        # The third job should be filtered out as it has the same URL as the first
