import pytest

from src.vector_store.models import JobVectorStore
from src.vector_store.vector_transformer.service import VectorTransformerService
from tests.factories.job_searcher import JobDetailsFactory


class TestVectorTransformerService:
    """Test VectorTransformerService transform method"""

    @pytest.fixture
    def transformer(self):
        """Create VectorTransformerService instance"""
        return VectorTransformerService()

    def test_transform_single_job_details(self, transformer):
        """Test transforming a single JobDetails"""
        job_details = JobDetailsFactory.build()

        result = transformer.transform([job_details])

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], JobVectorStore)

        vector_job = result[0]
        assert vector_job.job_id == job_details.job_id
        assert vector_job.job_title == job_details.title
        assert vector_job.job_description == job_details.description
        assert vector_job.job_apply_link == job_details.job_url
        assert vector_job.employer_name == job_details.company
        assert vector_job.job_city == job_details.city
        assert vector_job.job_state == job_details.state
        assert vector_job.job_country == job_details.country
        assert vector_job.location_string == job_details.location

    def test_transform_multiple_job_details(self, transformer):
        """Test transforming multiple JobDetails"""
        job_details_list = JobDetailsFactory.batch(3)

        result = transformer.transform(job_details_list)

        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(job, JobVectorStore) for job in result)

        for original, transformed in zip(job_details_list, result):
            assert transformed.job_id == original.job_id
            assert transformed.job_title == original.title
            assert transformed.job_description == original.description
            assert transformed.job_apply_link == original.job_url
            assert transformed.employer_name == original.company
            assert transformed.job_city == original.city
            assert transformed.job_state == original.state
            assert transformed.job_country == original.country
            assert transformed.location_string == original.location

    def test_transform_empty_list(self, transformer):
        """Test transforming empty list"""
        result = transformer.transform([])

        assert isinstance(result, list)
        assert len(result) == 0

    def test_transform_job_details_with_none_optional_fields(self, transformer):
        """Test transforming JobDetails with None optional fields"""
        job_details = JobDetailsFactory.build(
            city=None,
            state=None,
            country=None,
        )

        result = transformer.transform([job_details])

        assert len(result) == 1
        vector_job = result[0]

        assert vector_job.job_id == job_details.job_id
        assert vector_job.job_title == job_details.title
        assert vector_job.job_description == job_details.description
        assert vector_job.job_apply_link == job_details.job_url
        assert vector_job.employer_name == job_details.company
        assert vector_job.job_city is None
        assert vector_job.job_state is None
        assert vector_job.job_country is None
        assert vector_job.location_string == job_details.location

    def test_transform_preserves_required_fields(self, transformer):
        """Test that all required fields are preserved in transformation"""
        job_details = JobDetailsFactory.build()

        result = transformer.transform([job_details])
        vector_job = result[0]

        # Required fields should always be present
        assert vector_job.job_id is not None
        assert vector_job.job_title is not None
        assert vector_job.job_description is not None
        assert vector_job.job_apply_link is not None

    def test_transform_creates_valid_job_vector_store(self, transformer):
        """Test that transformed objects are valid JobVectorStore instances"""
        job_details = JobDetailsFactory.build()

        result = transformer.transform([job_details])
        vector_job = result[0]

        # Test that the transformed object has the expected methods
        assert hasattr(vector_job, "get_combined_text_document")
        assert hasattr(vector_job, "get_metadata")

        # Test that methods work correctly
        combined_text = vector_job.get_combined_text_document()
        assert isinstance(combined_text, str)
        assert job_details.title in combined_text
        assert job_details.description in combined_text

        metadata = vector_job.get_metadata()
        assert isinstance(metadata, dict)
        assert metadata["job_id"] == job_details.job_id
        assert metadata["job_title"] == job_details.title
