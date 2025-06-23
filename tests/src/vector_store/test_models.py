import pytest

from src.vector_store.models import JobVectorStore
from tests.factories.vector_store import JobVectorStoreFactory


class TestJobVectorStore:
    """Test cases for JobVectorStore model"""

    def test_init_with_all_fields(self):
        """Test initialization with all fields"""
        job = JobVectorStore(
            job_id="job_123",
            job_title="Senior Python Developer",
            job_description="Develop Python applications",
            job_apply_link="https://example.com/jobs/123",
            employer_name="Tech Corp",
            job_city="San Francisco",
            job_state="CA",
            job_country="USA",
            location_string="San Francisco, CA, USA",
        )

        assert job.job_id == "job_123"
        assert job.job_title == "Senior Python Developer"
        assert job.job_description == "Develop Python applications"
        assert job.job_apply_link == "https://example.com/jobs/123"
        assert job.employer_name == "Tech Corp"
        assert job.job_city == "San Francisco"
        assert job.job_state == "CA"
        assert job.job_country == "USA"
        assert job.location_string == "San Francisco, CA, USA"

    def test_init_with_required_fields_only(self):
        """Test initialization with only required fields"""
        job = JobVectorStore(
            job_id="job_456",
            job_title="Developer",
            job_description="Build software",
            job_apply_link="https://example.com/jobs/456",
        )

        assert job.job_id == "job_456"
        assert job.job_title == "Developer"
        assert job.job_description == "Build software"
        assert job.job_apply_link == "https://example.com/jobs/456"
        assert job.employer_name is None
        assert job.job_city is None
        assert job.job_state is None
        assert job.job_country is None
        assert job.location_string is None

    def test_get_combined_text_document_with_all_fields(self):
        """Test get_combined_text_document with all fields populated"""
        sample_job_vector_store = JobVectorStoreFactory.build(
            job_title="Senior Python Developer",
            employer_name="Tech Solutions Inc",
            location_string="San Francisco, CA, USA",
            job_description="We are looking for an experienced Python developer to "
            "join our team. You will work on backend services, APIs, and data "
            "processing pipelines.",
        )
        result = sample_job_vector_store.get_combined_text_document()

        expected = (
            "Job Title: Senior Python Developer\n"
            "Company: Tech Solutions Inc\n"
            "Location: San Francisco, CA, USA\n\n"
            "Description: We are looking for an experienced Python developer to "
            "join our team. You will work on backend services, APIs, and data "
            "processing pipelines."
        )

        assert result == expected

    def test_get_combined_text_document_with_none_fields(self):
        """Test get_combined_text_document with None optional fields"""
        result = JobVectorStore(
            job_id="job_456",
            job_apply_link="https://example.com/jobs/456",
            job_title="Test Job",
            job_description="Test description",
            employer_name=None,
            job_city=None,
            job_state=None,
            job_country=None,
            location_string=None,
        ).get_combined_text_document()

        expected = (
            "Job Title: Test Job\n"
            "Company: None\n"
            "Location: None\n\n"
            "Description: Test description"
        )

        assert result == expected

    def test_get_metadata_with_all_fields(self):
        """Test get_metadata with all fields populated"""
        sample_job_vector_store = JobVectorStoreFactory.build(
            job_id="job_123",
            job_title="Senior Python Developer",
            employer_name="Tech Solutions Inc",
            job_city="San Francisco",
            job_state="CA",
            job_country="USA",
            job_apply_link="https://example.com/jobs/123",
        )
        result = sample_job_vector_store.get_metadata()

        expected = {
            "job_id": "job_123",
            "job_title": "Senior Python Developer",
            "employer_name": "Tech Solutions Inc",
            "job_city": "San Francisco",
            "job_state": "CA",
            "job_country": "USA",
            "job_apply_link": "https://example.com/jobs/123",
        }

        assert result == expected
        assert isinstance(result, dict)

    def test_get_metadata_with_none_fields(self):
        """Test get_metadata with None optional fields"""
        result = JobVectorStore(
            job_id="minimal_job",
            job_title="Test Job",
            job_description="Test description",
            employer_name=None,
            job_city=None,
            job_state=None,
            job_country=None,
            job_apply_link="https://example.com/test",
            location_string=None,
        ).get_metadata()

        expected = {
            "job_id": "minimal_job",
            "job_title": "Test Job",
            "employer_name": None,
            "job_city": None,
            "job_state": None,
            "job_country": None,
            "job_apply_link": "https://example.com/test",
        }

        assert result == expected

    def test_get_metadata_returns_dict_type(self):
        """Test that get_metadata returns proper dict type annotation"""
        result = JobVectorStore(
            job_id="minimal_job",
            job_title="Test Job",
            job_description="Test description",
            employer_name=None,
            job_city=None,
            job_state=None,
            job_apply_link="https://example.com/test",
            job_country=None,
            location_string=None,
        ).get_metadata()

        assert isinstance(result, dict)
        # Check that all values are of expected types
        for key, value in result.items():
            assert isinstance(key, str)
            assert value is None or isinstance(value, str)

    @pytest.mark.parametrize(
        "field_name,field_value",
        [
            ("job_id", "test_id_123"),
            ("job_title", "Software Engineer"),
            ("job_description", "Build amazing software"),
            ("job_apply_link", "https://careers.example.com/apply"),
            ("employer_name", "Amazing Tech Company"),
            ("job_city", "Seattle"),
            ("job_state", "WA"),
            ("job_country", "United States"),
            ("location_string", "Seattle, WA, United States"),
        ],
    )
    def test_field_assignment(self, field_name, field_value):
        """Test individual field assignments"""
        job_data = {
            "job_id": "default_id",
            "job_title": "Default Title",
            "job_description": "Default description",
            "job_apply_link": "https://default.com",
        }
        job_data[field_name] = field_value

        job = JobVectorStore(**job_data)
        assert getattr(job, field_name) == field_value

    def test_pydantic_validation_missing_required_field(self):
        """Test that Pydantic validation catches missing required fields"""
        with pytest.raises(ValueError):
            JobVectorStore(  # type: ignore
                # Missing job_id - this should raise ValueError
                job_title="Test Job",
                job_description="Test description",
                job_apply_link="https://example.com/test",
            )
