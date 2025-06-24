from typing import Any, Dict, List, Optional

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

    def test_search_jobs_with_vendor(self, mock_vendor, sample_job_details):
        """Test search_jobs with a vendor"""
        service = JobSearcher(vendor=mock_vendor)
        query = "python developer"

        result = service.search_jobs(query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(query, None)

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
    def test_search_jobs_with_different_queries(self, mock_vendor, sample_job_details, query):
        """Test search_jobs with various query strings"""
        service = JobSearcher(vendor=mock_vendor)

        result = service.search_jobs(query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(query, None)

    def test_search_jobs_returns_empty_list(self, mock_vendor):
        """Test search_jobs when vendor returns empty list"""
        mock_vendor.search_jobs.return_value = []
        service = JobSearcher(vendor=mock_vendor)

        result = service.search_jobs("nonexistent job")

        assert result == []
        assert isinstance(result, list)
        mock_vendor.search_jobs.assert_called_once_with("nonexistent job", None)

    def test_search_jobs_preserves_vendor_exceptions(self, mock_vendor):
        """Test that search_jobs preserves exceptions from vendor"""
        mock_vendor.search_jobs.side_effect = ValueError("API error")
        service = JobSearcher(vendor=mock_vendor)

        with pytest.raises(ValueError, match="API error"):
            service.search_jobs("test query")

    def test_search_jobs_delegates_to_vendor(self, mock_vendor, sample_job_details):
        """Test that search_jobs properly delegates to the vendor"""
        service = JobSearcher(vendor=mock_vendor)
        query = "react developer"

        result = service.search_jobs(query)

        # Verify the call was made with correct parameters
        mock_vendor.search_jobs.assert_called_once_with(query, None)
        # Verify the result is returned unchanged
        assert result == sample_job_details
        assert result is mock_vendor.search_jobs.return_value

    def test_search_jobs_with_complex_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with complex query string"""
        service = JobSearcher(vendor=mock_vendor)
        complex_query = "senior python developer remote full-time"

        result = service.search_jobs(complex_query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(complex_query, None)

    def test_search_jobs_with_empty_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with empty query string"""
        service = JobSearcher(vendor=mock_vendor)

        result = service.search_jobs("")

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with("", None)

    def test_search_jobs_multiple_calls(self, mock_vendor, sample_job_details):
        """Test multiple calls to search_jobs"""
        service = JobSearcher(vendor=mock_vendor)

        # First call
        result1 = service.search_jobs("python")
        # Second call
        result2 = service.search_jobs("javascript")

        assert result1 == sample_job_details
        assert result2 == sample_job_details

        # Verify both calls were made
        assert mock_vendor.search_jobs.call_count == 2
        mock_vendor.search_jobs.assert_any_call("python", None)
        mock_vendor.search_jobs.assert_any_call("javascript", None)

    def test_search_jobs_with_none_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with None query - should return empty list"""
        service = JobSearcher(vendor=mock_vendor)

        # When query is None, service should return empty list without calling vendor
        result = service.search_jobs(None)

        assert result == []
        mock_vendor.search_jobs.assert_not_called()

    def test_search_jobs_with_special_characters(self, mock_vendor, sample_job_details):
        """Test search_jobs with special characters in query"""
        service = JobSearcher(vendor=mock_vendor)
        special_query = "C++ developer @$%^&*(){}[]|\\:;\"'<>?,./"

        result = service.search_jobs(special_query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(special_query, None)

    def test_search_jobs_with_unicode_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with Unicode characters in query"""
        service = JobSearcher(vendor=mock_vendor)
        unicode_query = "développeur python 工程师研发工程师"

        result = service.search_jobs(unicode_query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(unicode_query, None)

    def test_search_jobs_with_very_long_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with very long query string"""
        service = JobSearcher(vendor=mock_vendor)
        long_query = "python developer " * 100  # Very long query

        result = service.search_jobs(long_query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(long_query, None)

    def test_service_vendor_attribute_immutable(self, mock_vendor):
        """Test that vendor attribute is properly set and accessible"""
        service = JobSearcher(vendor=mock_vendor)

        # Vendor should be accessible
        assert service.vendor is mock_vendor

        # Should be the same object reference
        assert id(service.vendor) == id(mock_vendor)

    def test_search_jobs_vendor_returns_none(self, mock_vendor):
        """Test search_jobs when vendor returns None (edge case)"""
        mock_vendor.search_jobs.return_value = None
        service = JobSearcher(vendor=mock_vendor)

        result = service.search_jobs("test query")

        mock_vendor.search_jobs.assert_called_once_with("test query", None)
        assert result == []

    def test_search_jobs_vendor_side_effect_exception_types(self, mock_vendor):
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
                service.search_jobs("test query")

        # Reset after all iterations
        mock_vendor.search_jobs.side_effect = None
        mock_vendor.search_jobs.reset_mock()


class TestJobSearcherIntegration:
    """Integration tests for JobSearcher with realistic scenarios"""

    def test_search_jobs_with_real_vendor_interface(self):
        """Test with a more realistic vendor implementation"""

        class TestVendor(JobSearchVendor):
            def search_jobs(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[JobDetails]:
                return [
                    JobDetailsFactory.build(
                        title="Developer for python",
                        company="Test Company",
                    )
                ]

            def get_job_details(self, job_id: str) -> JobDetails:
                return JobDetailsFactory.build(
                    title="Developer for python",
                    company="Test Company",
                )

            def get_vendor_name(self) -> str:
                return "test_vendor"

        vendor = TestVendor()
        service = JobSearcher(vendor=vendor)

        result = service.search_jobs("python", filters={"location": "Remote"})

        assert len(result) == 1
        assert result[0].title == "Developer for python"
        assert result[0].company == "Test Company"

    def test_service_with_different_vendors(self, sample_job_details):
        """Test service behavior with different vendor implementations"""

        class VendorA(JobSearchVendor):
            def search_jobs(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[JobDetails]:
                return [
                    JobDetailsFactory.build(
                        title="VendorA Detail",
                        description="Detail from Vendor A",
                        location="Location A",
                        company="Company A",
                        job_url="https://vendorA.com/job",
                    )
                ]

            def get_job_details(self, job_id: str) -> JobDetails:
                return JobDetailsFactory.build(
                    title="VendorA Detail",
                    description="Detail from Vendor A",
                    location="Location A",
                    company="Company A",
                    job_url="https://vendorA.com/job",
                )

            def get_vendor_name(self) -> str:
                return "vendor_a"

        class VendorB(JobSearchVendor):
            def search_jobs(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[JobDetails]:
                return [
                    JobDetailsFactory.build(
                        title="VendorB Detail",
                        description="Detail from Vendor B",
                        location="Location B",
                        company="Company B",
                        job_url="https://vendorB.com/job",
                    )
                ]

            def get_job_details(self, job_id: str) -> JobDetails:
                return JobDetailsFactory.build(
                    title="VendorB Detail",
                    description="Detail from Vendor B",
                    location="Location B",
                    company="Company B",
                    job_url="https://vendorB.com/job",
                )

            def get_vendor_name(self) -> str:
                return "vendor_b"

        # Test with VendorA
        service_a = JobSearcher(vendor=VendorA())
        result_a = service_a.search_jobs("test", filters={"location": "Remote"})
        assert result_a[0].title == "VendorA Detail"
        assert result_a[0].company == "Company A"

        # Test with VendorB
        service_b = JobSearcher(vendor=VendorB())
        result_b = service_b.search_jobs("test", filters={"location": "Remote"})
        assert result_b[0].title == "VendorB Detail"
        assert result_b[0].company == "Company B"

        # Results should be different
        assert result_a[0].title != result_b[0].title
