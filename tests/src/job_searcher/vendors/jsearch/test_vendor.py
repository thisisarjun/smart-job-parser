from unittest.mock import MagicMock, Mock, patch

import httpx
import pytest

from src.job_searcher.models import JobDetails
from src.job_searcher.vendors.jsearch.models import Job as JSearchJob
from src.job_searcher.vendors.jsearch.vendor import JSearchVendor


class TestJSearchVendorInit:
    """Test JSearchVendor initialization"""

    def test_init_with_api_key(self):
        """Test initialization with provided API key"""
        vendor = JSearchVendor()  # pragma: allowlist secret
        assert vendor.api_key == "test_api_key"  # pragma: allowlist secret
        assert vendor.base_url == "https://jsearch.p.rapidapi.com"
        assert vendor.headers["x-rapidapi-key"] == "test_api_key"
        assert vendor.headers["x-rapidapi-host"] == "jsearch.p.rapidapi.com"


class TestJSearchVendorConversion:
    """Test job conversion methods"""

    def test_convert_to_job_details(self, jsearch_vendor, sample_jsearch_job):
        """Test conversion from JSearch job to JobDetails"""
        job_details = jsearch_vendor._convert_to_job_details(sample_jsearch_job)

        assert isinstance(job_details, JobDetails)
        assert job_details.title == "Software Developer"
        assert (
            "never been a more exciting time to join United Airlines"
            in job_details.description
        )
        assert job_details.location == "Chicago, Illinois, US"
        assert job_details.company == "United Airlines"
        expected_url = (
            "https://careers.united.com/us/en/job/WHQ00024224/"
            "Software-Developer?utm_campaign=google_jobs_apply"
            "&utm_source=google_jobs_apply&utm_medium=organic"
        )
        assert job_details.job_url == expected_url

    def test_convert_to_job_details_no_employer(self, jsearch_vendor):
        """Test conversion with missing employer name"""
        job = JSearchJob(
            job_id="test_123",
            job_title="Developer",
            job_description="Code stuff",
            job_apply_link="https://example.com/apply",
            employer_name=None,
        )

        job_details = jsearch_vendor._convert_to_job_details(job)
        assert job_details.company == "Unknown Company"


class TestJSearchVendorSearchJobs:
    """Test search_jobs method"""

    @patch("httpx.Client")
    def test_search_jobs_success(
        self, mock_client_class, jsearch_vendor, sample_search_response
    ):
        """Test successful job search"""
        # Setup mock
        mock_client = MagicMock()
        mock_client_class.return_value.__enter__.return_value = mock_client

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = sample_search_response.dict()
        mock_client.get.return_value = mock_response

        # Execute
        result = jsearch_vendor.search_jobs("software engineer", {"country": "us"})

        # Verify
        assert len(result) == 10
        assert isinstance(result[0], JobDetails)
        assert result[0].title == "Software Developer"

        # Verify API call
        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert "search" in call_args[0][0]
        assert call_args[1]["params"]["query"] == "software engineer"
        assert call_args[1]["params"]["country"] == "us"
        assert call_args[1]["params"]["date_posted"] == "all"

    @pytest.mark.parametrize(
        "exception_type,expected_message",
        [
            (httpx.HTTPStatusError, "JSearch API error"),
            (httpx.RequestError, "JSearch API request failed"),
            (Exception, "JSearch API unexpected error"),
        ],
    )
    @patch("httpx.Client")
    def test_search_jobs_errors(
        self, mock_client_class, jsearch_vendor, exception_type, expected_message
    ):
        """Test search_jobs error handling"""
        # Setup mock to raise exception
        mock_client = MagicMock()
        mock_client_class.return_value.__enter__.return_value = mock_client

        if exception_type == httpx.HTTPStatusError:
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.text = "Bad Request"
            mock_client.get.side_effect = httpx.HTTPStatusError(
                "Error", request=Mock(), response=mock_response
            )
        else:
            mock_client.get.side_effect = exception_type("Test error")

        # Execute and verify
        with pytest.raises(Exception) as exc_info:
            jsearch_vendor.search_jobs("test query")

        assert expected_message in str(exc_info.value)


class TestJSearchVendorGetJobDetails:
    """Test get_job_details method"""

    @patch("httpx.Client")
    def test_get_job_details_success(
        self, mock_client_class, jsearch_vendor, sample_jsearch_job
    ):
        """Test successful job details retrieval"""
        # Setup mock
        mock_client = MagicMock()
        mock_client_class.return_value.__enter__.return_value = mock_client

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": [sample_jsearch_job.dict()]}
        mock_client.get.return_value = mock_response

        # Execute
        result = jsearch_vendor.get_job_details("test_job_123")

        # Verify
        assert isinstance(result, JobDetails)
        assert result.title == "Software Developer"

        # Verify API call
        mock_client.get.assert_called_once()
        call_args = mock_client.get.call_args
        assert "job-details" in call_args[0][0]
        assert call_args[1]["params"]["job_id"] == "test_job_123"

    @patch("httpx.Client")
    def test_get_job_details_not_found(self, mock_client_class, jsearch_vendor):
        """Test job details when job not found"""
        # Setup mock
        mock_client = MagicMock()
        mock_client_class.return_value.__enter__.return_value = mock_client

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"data": []}
        mock_client.get.return_value = mock_response

        # Execute and verify
        with pytest.raises(Exception, match="Job not found"):
            jsearch_vendor.get_job_details("nonexistent_job")

    @pytest.mark.parametrize(
        "exception_type,expected_message",
        [
            (httpx.HTTPStatusError, "JSearch API error"),
            (httpx.RequestError, "JSearch API request failed"),
            (Exception, "JSearch API unexpected error"),
        ],
    )
    @patch("httpx.Client")
    def test_get_job_details_errors(
        self, mock_client_class, jsearch_vendor, exception_type, expected_message
    ):
        """Test get_job_details error handling"""
        # Setup mock to raise exception
        mock_client = MagicMock()
        mock_client_class.return_value.__enter__.return_value = mock_client

        if exception_type == httpx.HTTPStatusError:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.text = "Not Found"
            mock_client.get.side_effect = httpx.HTTPStatusError(
                "Error", request=Mock(), response=mock_response
            )
        else:
            mock_client.get.side_effect = exception_type("Test error")

        # Execute and verify
        with pytest.raises(Exception) as exc_info:
            jsearch_vendor.get_job_details("test_job_id")

        assert expected_message in str(exc_info.value)


class TestJSearchVendorMisc:
    """Test miscellaneous vendor methods"""

    def test_get_vendor_name(self, jsearch_vendor):
        """Test vendor name retrieval"""
        assert jsearch_vendor.get_vendor_name() == "jsearch"


class TestJSearchVendorIntegration:
    """Integration tests for JSearchVendor"""

    @patch("httpx.Client")
    def test_full_search_workflow(self, mock_client_class, jsearch_vendor):
        """Test complete search workflow"""
        # Setup mock for search
        mock_client = MagicMock()
        mock_client_class.return_value.__enter__.return_value = mock_client

        search_response_data = {
            "status": "OK",
            "request_id": "test_123",
            "parameters": {"query": "python developer"},
            "data": [
                {
                    "job_id": "job_1",
                    "job_title": "Python Developer",
                    "job_description": "Build Python applications",
                    "job_apply_link": "https://example.com/apply/1",
                    "employer_name": "Python Corp",
                    "job_city": "New York",
                    "job_state": "NY",
                    "job_country": "US",
                },
                {
                    "job_id": "job_2",
                    "job_title": "Senior Python Engineer",
                    "job_description": "Lead Python development",
                    "job_apply_link": "https://example.com/apply/2",
                    "employer_name": "Tech Solutions",
                    "job_city": "Boston",
                    "job_state": "MA",
                    "job_country": "US",
                },
            ],
        }

        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = search_response_data
        mock_client.get.return_value = mock_response

        # Execute search
        results = jsearch_vendor.search_jobs("python developer")

        # Verify results
        assert len(results) == 2
        assert all(isinstance(job, JobDetails) for job in results)
        assert results[0].title == "Python Developer"
        assert results[0].company == "Python Corp"
        assert results[0].location == "New York, NY, US"
        assert results[1].title == "Senior Python Engineer"
        assert results[1].company == "Tech Solutions"
        assert results[1].location == "Boston, MA, US"
