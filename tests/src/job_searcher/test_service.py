from typing import List

import pytest

from src.job_searcher.interface import JobSearchVendor
from src.job_searcher.models import JobDetails
from src.job_searcher.service import JobSearchService


class TestJobSearchService:
    """Test cases for JobSearchService"""

    def test_init_with_vendor(self, mock_vendor):
        """Test initialization with a vendor"""
        service = JobSearchService(vendor=mock_vendor)

        assert service.vendor == mock_vendor

    def test_search_jobs_with_vendor(self, mock_vendor, sample_job_details):
        """Test search_jobs with a vendor"""
        service = JobSearchService(vendor=mock_vendor)
        query = "python developer"

        result = service.search_jobs(query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(query)

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
    def test_search_jobs_with_different_queries(
        self, mock_vendor, sample_job_details, query
    ):
        """Test search_jobs with various query strings"""
        service = JobSearchService(vendor=mock_vendor)

        result = service.search_jobs(query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(query)

    def test_search_jobs_returns_empty_list(self, mock_vendor):
        """Test search_jobs when vendor returns empty list"""
        mock_vendor.search_jobs.return_value = []
        service = JobSearchService(vendor=mock_vendor)

        result = service.search_jobs("nonexistent job")

        assert result == []
        assert isinstance(result, list)
        mock_vendor.search_jobs.assert_called_once_with("nonexistent job")

    def test_search_jobs_preserves_vendor_exceptions(self, mock_vendor):
        """Test that search_jobs preserves exceptions from vendor"""
        mock_vendor.search_jobs.side_effect = ValueError("API error")
        service = JobSearchService(vendor=mock_vendor)

        with pytest.raises(ValueError, match="API error"):
            service.search_jobs("test query")

    def test_search_jobs_delegates_to_vendor(self, mock_vendor, sample_job_details):
        """Test that search_jobs properly delegates to the vendor"""
        service = JobSearchService(vendor=mock_vendor)
        query = "react developer"

        result = service.search_jobs(query)

        # Verify the call was made with correct parameters
        mock_vendor.search_jobs.assert_called_once_with(query)
        # Verify the result is returned unchanged
        assert result == sample_job_details
        assert result is mock_vendor.search_jobs.return_value

    def test_search_jobs_with_complex_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with complex query string"""
        service = JobSearchService(vendor=mock_vendor)
        complex_query = "senior python developer remote full-time"

        result = service.search_jobs(complex_query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(complex_query)

    def test_search_jobs_with_empty_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with empty query string"""
        service = JobSearchService(vendor=mock_vendor)

        result = service.search_jobs("")

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with("")

    def test_search_jobs_multiple_calls(self, mock_vendor, sample_job_details):
        """Test multiple calls to search_jobs"""
        service = JobSearchService(vendor=mock_vendor)

        # First call
        result1 = service.search_jobs("python")
        # Second call
        result2 = service.search_jobs("javascript")

        assert result1 == sample_job_details
        assert result2 == sample_job_details

        # Verify both calls were made
        assert mock_vendor.search_jobs.call_count == 2
        mock_vendor.search_jobs.assert_any_call("python")
        mock_vendor.search_jobs.assert_any_call("javascript")

    def test_search_jobs_with_none_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with None query - should let vendor handle it"""
        service = JobSearchService(vendor=mock_vendor)

        # This should pass the None to the vendor and let vendor decide behavior
        result = service.search_jobs(None)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(None)

    def test_search_jobs_with_special_characters(self, mock_vendor, sample_job_details):
        """Test search_jobs with special characters in query"""
        service = JobSearchService(vendor=mock_vendor)
        special_query = "C++ developer @$%^&*(){}[]|\\:;\"'<>?,./"

        result = service.search_jobs(special_query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(special_query)

    def test_search_jobs_with_unicode_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with Unicode characters in query"""
        service = JobSearchService(vendor=mock_vendor)
        unicode_query = "développeur python 工程师 разработчик"

        result = service.search_jobs(unicode_query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(unicode_query)

    def test_search_jobs_with_very_long_query(self, mock_vendor, sample_job_details):
        """Test search_jobs with very long query string"""
        service = JobSearchService(vendor=mock_vendor)
        long_query = "python developer " * 100  # Very long query

        result = service.search_jobs(long_query)

        assert result == sample_job_details
        mock_vendor.search_jobs.assert_called_once_with(long_query)

    def test_service_vendor_attribute_immutable(self, mock_vendor):
        """Test that vendor attribute is properly set and accessible"""
        service = JobSearchService(vendor=mock_vendor)

        # Vendor should be accessible
        assert service.vendor is mock_vendor

        # Should be the same object reference
        assert id(service.vendor) == id(mock_vendor)

    def test_search_jobs_vendor_returns_none(self, mock_vendor):
        """Test search_jobs when vendor returns None (edge case)"""
        mock_vendor.search_jobs.return_value = None
        service = JobSearchService(vendor=mock_vendor)

        result = service.search_jobs("test query")

        assert result is None
        mock_vendor.search_jobs.assert_called_once_with("test query")

    def test_search_jobs_vendor_side_effect_exception_types(self, mock_vendor):
        """Test different exception types from vendor"""
        service = JobSearchService(vendor=mock_vendor)

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

            # Reset for next iteration
            mock_vendor.search_jobs.side_effect = None
            mock_vendor.search_jobs.reset_mock()


class TestJobSearchServiceIntegration:
    """Integration tests for JobSearchService with realistic scenarios"""

    def test_search_jobs_with_real_vendor_interface(self):
        """Test with a more realistic vendor implementation"""

        class TestVendor(JobSearchVendor):
            def search_jobs(self, query: str) -> List[JobDetails]:
                return [
                    JobDetails(
                        title=f"Developer for {query}",
                        description=f"Job description for {query}",
                        location="Remote",
                        company="Test Company",
                        job_url="https://test.com/job",
                    )
                ]

            def get_job_details(self, job_id: str) -> JobDetails:
                return JobDetails(
                    title="Test Job",
                    description="Test Description",
                    location="Test Location",
                    company="Test Company",
                    job_url="https://test.com/job",
                )

            def get_vendor_name(self) -> str:
                return "test_vendor"

        vendor = TestVendor()
        service = JobSearchService(vendor=vendor)

        result = service.search_jobs("python")

        assert len(result) == 1
        assert result[0].title == "Developer for python"
        assert result[0].company == "Test Company"

    def test_service_with_different_vendors(self, sample_job_details):
        """Test service behavior with different vendor implementations"""

        class VendorA(JobSearchVendor):
            def search_jobs(self, query: str) -> List[JobDetails]:
                return [
                    JobDetails(
                        title="VendorA Job",
                        description="Job from Vendor A",
                        location="Location A",
                        company="Company A",
                        job_url="https://vendorA.com/job",
                    )
                ]

            def get_job_details(self, job_id: str) -> JobDetails:
                return JobDetails(
                    title="VendorA Detail",
                    description="Detail from Vendor A",
                    location="Location A",
                    company="Company A",
                    job_url="https://vendorA.com/job",
                )

            def get_vendor_name(self) -> str:
                return "vendor_a"

        class VendorB(JobSearchVendor):
            def search_jobs(self, query: str) -> List[JobDetails]:
                return [
                    JobDetails(
                        title="VendorB Job",
                        description="Job from Vendor B",
                        location="Location B",
                        company="Company B",
                        job_url="https://vendorB.com/job",
                    )
                ]

            def get_job_details(self, job_id: str) -> JobDetails:
                return JobDetails(
                    title="VendorB Detail",
                    description="Detail from Vendor B",
                    location="Location B",
                    company="Company B",
                    job_url="https://vendorB.com/job",
                )

            def get_vendor_name(self) -> str:
                return "vendor_b"

        # Test with VendorA
        service_a = JobSearchService(vendor=VendorA())
        result_a = service_a.search_jobs("test")
        assert result_a[0].title == "VendorA Job"
        assert result_a[0].company == "Company A"

        # Test with VendorB
        service_b = JobSearchService(vendor=VendorB())
        result_b = service_b.search_jobs("test")
        assert result_b[0].title == "VendorB Job"
        assert result_b[0].company == "Company B"

        # Results should be different
        assert result_a[0].title != result_b[0].title
