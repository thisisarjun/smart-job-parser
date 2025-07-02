from unittest.mock import AsyncMock, MagicMock, Mock, patch

import httpx
import pytest

from src.job_searcher.models import JobDetails
from src.job_searcher.vendors.jsearch.vendor import JSearchVendor
from tests.factories.search_vendors import JSearchJobFactory, JSearchSearchResponseFactory


class TestJSearchVendorInit:
    """Test JSearchVendor initialization"""

    def test_init_with_api_key(self):
        """Test initialization with provided API key"""
        vendor = JSearchVendor()  # pragma: allowlist secret
        assert vendor.api_key == "test_api_key"  # pragma: allowlist secret
        assert vendor.base_url == "https://jsearch.p.rapidapi.com"
        assert vendor.headers["x-rapidapi-key"] == "test_api_key"
        assert vendor.headers["x-rapidapi-host"] == "jsearch.p.rapidapi.com"
        assert vendor.http_client is not None


class TestJSearchVendorConversion:
    """Test job conversion methods"""

    def test_convert_to_job_details(self, jsearch_vendor):
        """Test conversion from JSearch job to JobDetails"""
        # Create sample JSearch job
        jsearch_job = JSearchJobFactory.build(
            job_id="test_123",
            job_title="Software Engineer",
            job_description="Build amazing software",
            job_apply_link="https://example.com/apply",
            employer_name="Tech Corp",
            job_city="San Francisco",
            job_state="CA",
            job_country="US",
        )

        # Convert to JobDetails
        job_details = jsearch_vendor._convert_to_job_details(jsearch_job)

        # Verify conversion
        assert isinstance(job_details, JobDetails)
        assert job_details.job_id == "test_123"
        assert job_details.title == "Software Engineer"
        assert job_details.description == "Build amazing software"
        assert job_details.job_url == "https://example.com/apply"
        assert job_details.company == "Tech Corp"
        assert job_details.city == "San Francisco"
        assert job_details.state == "CA"
        assert job_details.country == "US"

    def test_convert_to_job_details_no_employer(self, jsearch_vendor):
        """Test conversion when employer name is missing"""
        jsearch_job = JSearchJobFactory.build(employer_name=None)
        job_details = jsearch_vendor._convert_to_job_details(jsearch_job)
        assert job_details.company == "Unknown Company"


class TestJSearchVendorSearchJobs:
    """Test search_jobs method"""

    @pytest.mark.asyncio
    @patch("src.job_searcher.vendors.jsearch.vendor.HttpBaseClient")
    async def test_search_jobs_success(self, mock_http_client_class, jsearch_vendor):
        sample_search_response = JSearchSearchResponseFactory.build(
            data=[
                JSearchJobFactory.build(
                    job_title="Software Developer",
                    job_description="never been a more exciting time to join United Airlines",  # noqa: E501
                )
            ]
        )
        """Test successful job search"""
        # Setup mock
        mock_http_client = MagicMock()
        mock_http_client_class.return_value = mock_http_client
        jsearch_vendor.http_client = mock_http_client

        mock_response = Mock()
        mock_response.json.return_value = sample_search_response.dict()
        mock_http_client.get = AsyncMock(return_value=mock_response)

        # Execute
        result = await jsearch_vendor.search_jobs("software engineer", {"country": "us"})

        # Verify
        assert len(result) == 1
        assert isinstance(result[0], JobDetails)
        assert result[0].title == "Software Developer"

        # Verify API call
        mock_http_client.get.assert_called_once()
        call_args = mock_http_client.get.call_args
        assert call_args[0][0] == "/search"
        assert call_args[1]["params"]["query"] == "software engineer"
        assert call_args[1]["params"]["country"] == "us"
        assert call_args[1]["params"]["date_posted"] == "all"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "exception_type,expected_message",
        [
            (httpx.HTTPStatusError, "JSearch API error"),
            (httpx.RequestError, "JSearch API request failed"),
            (Exception, "JSearch API unexpected error"),
        ],
    )
    @patch("src.job_searcher.vendors.jsearch.vendor.HttpBaseClient")
    async def test_search_jobs_errors(self, mock_http_client_class, jsearch_vendor, exception_type, expected_message):
        """Test search_jobs error handling"""
        # Setup mock to raise exception
        mock_http_client = MagicMock()
        mock_http_client_class.return_value = mock_http_client
        jsearch_vendor.http_client = mock_http_client

        if exception_type == httpx.HTTPStatusError:
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.text = "Bad Request"
            mock_http_client.get = AsyncMock(
                side_effect=httpx.HTTPStatusError("Error", request=Mock(), response=mock_response)
            )
        else:
            mock_http_client.get = AsyncMock(side_effect=exception_type("Test error"))

        # Execute and verify
        with pytest.raises(Exception) as exc_info:
            await jsearch_vendor.search_jobs("test query")

        assert expected_message in str(exc_info.value)


class TestJSearchVendorGetJobDetails:
    """Test get_job_details method"""

    @pytest.mark.asyncio
    @patch("src.job_searcher.vendors.jsearch.vendor.HttpBaseClient")
    async def test_get_job_details_success(self, mock_http_client_class, jsearch_vendor):
        sample_jsearch_job = JSearchJobFactory.build(
            job_title="Software Developer",
            job_description="never been a more exciting time to join United Airlines",
        )
        """Test successful job details retrieval"""
        # Setup mock
        mock_http_client = MagicMock()
        mock_http_client_class.return_value = mock_http_client
        jsearch_vendor.http_client = mock_http_client

        mock_response = Mock()
        mock_response.json.return_value = {"data": [sample_jsearch_job.dict()]}
        mock_http_client.get = AsyncMock(return_value=mock_response)

        # Execute
        result = await jsearch_vendor.get_job_details("test_job_123")

        # Verify
        assert isinstance(result, JobDetails)
        assert result.title == "Software Developer"

        # Verify API call
        mock_http_client.get.assert_called_once()
        call_args = mock_http_client.get.call_args
        assert call_args[0][0] == "/job-details"
        assert call_args[1]["params"]["job_id"] == "test_job_123"

    @pytest.mark.asyncio
    @patch("src.job_searcher.vendors.jsearch.vendor.HttpBaseClient")
    async def test_get_job_details_not_found(self, mock_http_client_class, jsearch_vendor):
        """Test job details when job not found"""
        # Setup mock
        mock_http_client = MagicMock()
        mock_http_client_class.return_value = mock_http_client
        jsearch_vendor.http_client = mock_http_client

        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_http_client.get = AsyncMock(return_value=mock_response)

        # Execute and verify
        with pytest.raises(Exception, match="Job not found"):
            await jsearch_vendor.get_job_details("nonexistent_job")

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "exception_type,expected_message",
        [
            (httpx.HTTPStatusError, "JSearch API error"),
            (httpx.RequestError, "JSearch API request failed"),
            (Exception, "JSearch API unexpected error"),
        ],
    )
    @patch("src.job_searcher.vendors.jsearch.vendor.HttpBaseClient")
    async def test_get_job_details_errors(
        self, mock_http_client_class, jsearch_vendor, exception_type, expected_message
    ):
        """Test get_job_details error handling"""
        # Setup mock to raise exception
        mock_http_client = MagicMock()
        mock_http_client_class.return_value = mock_http_client
        jsearch_vendor.http_client = mock_http_client

        if exception_type == httpx.HTTPStatusError:
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.text = "Not Found"
            mock_http_client.get = AsyncMock(
                side_effect=httpx.HTTPStatusError("Error", request=Mock(), response=mock_response)
            )
        else:
            mock_http_client.get = AsyncMock(side_effect=exception_type("Test error"))

        # Execute and verify
        with pytest.raises(Exception) as exc_info:
            await jsearch_vendor.get_job_details("test_job_id")

        assert expected_message in str(exc_info.value)


class TestJSearchVendorMisc:
    """Test miscellaneous vendor methods"""

    def test_get_vendor_name(self, jsearch_vendor):
        """Test vendor name retrieval"""
        assert jsearch_vendor.get_vendor_name() == "jsearch"


class TestJSearchVendorIntegration:
    """Integration tests for JSearchVendor"""

    @pytest.mark.asyncio
    @patch("src.job_searcher.vendors.jsearch.vendor.HttpBaseClient")
    async def test_full_search_workflow(self, mock_http_client_class, jsearch_vendor):
        """Test complete search workflow"""
        # Setup mock for search
        mock_http_client = MagicMock()
        mock_http_client_class.return_value = mock_http_client
        jsearch_vendor.http_client = mock_http_client

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
        mock_response.json.return_value = search_response_data
        mock_http_client.get = AsyncMock(return_value=mock_response)

        # Execute search
        results = await jsearch_vendor.search_jobs("python developer")

        # Verify results
        assert len(results) == 2
        assert all(isinstance(job, JobDetails) for job in results)
        assert results[0].title == "Python Developer"
        assert results[0].company == "Python Corp"
        assert results[0].location == "New York, NY, US"
        assert results[1].title == "Senior Python Engineer"
        assert results[1].company == "Tech Solutions"
        assert results[1].location == "Boston, MA, US"
