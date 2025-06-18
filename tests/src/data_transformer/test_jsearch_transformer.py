import pytest

from src.data_transformer.transformers.jsearch_transformer import JSearchTransformer
from src.job_searcher.vendors.jsearch.models import Job as JSearchJob
from src.vector_store.models import JobVectorStore
from tests.fixtures.jsearch_result import sample_jsearch_result


class TestJSearchTransformerTransform:
    """Test transform method"""

    def test_transform_single_job(self, single_jsearch_job):
        """Test transforming a single JSearch job"""
        transformer = JSearchTransformer()

        # Execute transform
        result = transformer.transform([single_jsearch_job])

        # Verify result
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], JobVectorStore)

        vector_job = result[0]
        assert vector_job.job_id == "VnVsqdlLW-S4XAiNAAAAAA=="
        assert vector_job.job_title == "Software Developer"
        assert vector_job.employer_name == "United Airlines"
        assert vector_job.location_string == "Chicago, Illinois, US"

        # Test combined text document
        combined_text = vector_job.get_combined_text_document()
        assert "United Airlines" in combined_text
        assert "Software Developer" in combined_text
        assert "United Airlines" in combined_text
        assert "Chicago, Illinois, US" in combined_text
        assert (
            "never been a more exciting time to join United Airlines" in combined_text
        )

    def test_transform_multiple_jobs(self, sample_jsearch_jobs):
        """Test transforming multiple JSearch jobs"""
        transformer = JSearchTransformer()

        # Execute transform
        result = transformer.transform(sample_jsearch_jobs)

        # Verify result
        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(job, JobVectorStore) for job in result)

        # Check first job (United Airlines)
        assert result[0].job_id == "VnVsqdlLW-S4XAiNAAAAAA=="
        assert result[0].job_title == "Software Developer"
        assert result[0].employer_name == "United Airlines"

        # Check second job (Phoenix Recruitment)
        assert result[1].job_id == "vkjeB63QCA2uyqZ3AAAAAA=="
        assert result[1].job_title == "Mid-Level Front-End Developer"
        assert result[1].employer_name == "Phoenix Recruitment"

        # Check third job (Cloud Resources LLC)
        assert result[2].job_id == "A9BWoy_aC7zO2GuzAAAAAA=="
        assert result[2].job_title == ".Net  Developer"
        assert result[2].employer_name == "Cloud Resources LLC"

    def test_transform_job_with_missing_fields(self):
        """Test transforming job with missing optional fields"""
        transformer = JSearchTransformer()

        # Job with minimal required fields
        jsearch_job = JSearchJob(
            job_id="minimal_job",
            job_title="Developer",
            job_description="Write code.",
            job_apply_link="https://example.com/minimal",
            employer_name=None,  # Missing employer
            job_city=None,  # Missing city
            job_state=None,  # Missing state
            job_country=None,  # Missing country
        )

        # Execute transform
        result = transformer.transform([jsearch_job])

        # Verify result
        assert len(result) == 1
        vector_job = result[0]

        assert vector_job.job_id == "minimal_job"
        assert vector_job.employer_name is None
        assert vector_job.job_city is None
        assert vector_job.job_state is None
        assert vector_job.job_country is None
        assert vector_job.location_string == "Location not specified"

    def test_transform_empty_list(self):
        """Test transforming empty job list"""
        transformer = JSearchTransformer()

        result = transformer.transform([])

        assert isinstance(result, list)
        assert len(result) == 0

    @pytest.mark.parametrize(
        "job_index,expected_title,expected_employer",
        [
            (0, "Software Developer", "United Airlines"),
            (1, "Mid-Level Front-End Developer", "Phoenix Recruitment"),
            (2, ".Net  Developer", "Cloud Resources LLC"),
        ],
    )
    def test_transform_various_fixture_jobs(
        self, job_index, expected_title, expected_employer
    ):
        """Test transform with various jobs from fixture data"""
        transformer = JSearchTransformer()

        job_data = sample_jsearch_result["data"][job_index]
        jsearch_job = JSearchJob(
            job_id=job_data["job_id"],
            job_title=job_data["job_title"],
            job_description=job_data["job_description"],
            job_apply_link=job_data["job_apply_link"],
            employer_name=job_data["employer_name"],
            job_city=job_data["job_city"],
            job_state=job_data["job_state"],
            job_country=job_data["job_country"],
        )

        result = transformer.transform([jsearch_job])

        assert len(result) == 1
        assert result[0].job_title == expected_title
        assert result[0].employer_name == expected_employer

        combined_text = result[0].get_combined_text_document()
        assert expected_title in combined_text
        assert expected_employer in combined_text


class TestJSearchTransformerMetadata:
    """Test metadata extraction"""

    @pytest.fixture
    def fixture_job(self):
        """Create JSearchJob from fixture data"""
        job_data = sample_jsearch_result["data"][0]
        return JSearchJob(
            job_id=job_data["job_id"],
            job_title=job_data["job_title"],
            job_description=job_data["job_description"],
            job_apply_link=job_data["job_apply_link"],
            employer_name=job_data["employer_name"],
            job_city=job_data["job_city"],
            job_state=job_data["job_state"],
            job_country=job_data["job_country"],
        )

    def test_metadata_contains_all_fields(self, fixture_job):
        """Test that metadata contains all expected fields"""
        transformer = JSearchTransformer()

        result = transformer.transform([fixture_job])
        metadata = result[0].get_metadata()

        expected_keys = [
            "job_id",
            "job_title",
            "employer_name",
            "job_city",
            "job_state",
            "job_country",
            "job_apply_link",
        ]

        for key in expected_keys:
            assert key in metadata

        assert metadata["job_id"] == "VnVsqdlLW-S4XAiNAAAAAA=="
        assert metadata["job_title"] == "Software Developer"
        assert metadata["employer_name"] == "United Airlines"
        expected_url = (
            "https://careers.united.com/us/en/job/WHQ00024224/"
            "Software-Developer?utm_campaign=google_jobs_apply"
            "&utm_source=google_jobs_apply&utm_medium=organic"
        )
        assert metadata["job_apply_link"] == expected_url


class TestJSearchTransformerEdgeCases:
    """Test edge cases and error handling"""

    def test_transform_with_long_description(self):
        """Test transform with very long job description from fixture"""
        transformer = JSearchTransformer()

        # Use the United Airlines job which has a very long description
        job_data = sample_jsearch_result["data"][0]
        jsearch_job = JSearchJob(
            job_id=job_data["job_id"],
            job_title=job_data["job_title"],
            job_description=job_data["job_description"],
            job_apply_link=job_data["job_apply_link"],
            employer_name=job_data["employer_name"],
            job_city=job_data["job_city"],
            job_state=job_data["job_state"],
            job_country=job_data["job_country"],
        )

        result = transformer.transform([jsearch_job])

        assert len(result) == 1
        assert len(result[0].job_description) == len(job_data["job_description"])
        assert (
            "never been a more exciting time to join United Airlines"
            in result[0].get_combined_text_document()
        )

    def test_transform_with_special_characters(self):
        """Test transform with special characters in text from fixture"""
        transformer = JSearchTransformer()

        # Use the .Net Developer job which has special characters
        job_data = sample_jsearch_result["data"][2]
        jsearch_job = JSearchJob(
            job_id=job_data["job_id"],
            job_title=job_data["job_title"],
            job_description=job_data["job_description"],
            job_apply_link=job_data["job_apply_link"],
            employer_name=job_data["employer_name"],
            job_city=job_data["job_city"],
            job_state=job_data["job_state"],
            job_country=job_data["job_country"],
        )

        result = transformer.transform([jsearch_job])

        assert len(result) == 1
        combined_text = result[0].get_combined_text_document()
        assert ".Net  Developer" in combined_text
        assert "Cloud Resources LLC" in combined_text
        assert ".NET Core" in combined_text

    def test_transform_remote_job(self):
        """Test transform with remote job from fixture"""
        transformer = JSearchTransformer()

        # Use the Phoenix Recruitment job which is remote
        job_data = sample_jsearch_result["data"][1]
        jsearch_job = JSearchJob(
            job_id=job_data["job_id"],
            job_title=job_data["job_title"],
            job_description=job_data["job_description"],
            job_apply_link=job_data["job_apply_link"],
            employer_name=job_data["employer_name"],
            job_city=job_data["job_city"],
            job_state=job_data["job_state"],
            job_country=job_data["job_country"],
        )

        result = transformer.transform([jsearch_job])

        assert len(result) == 1
        combined_text = result[0].get_combined_text_document()
        assert "This is a remote position" in combined_text
        assert "Mid-Level Front-End Developer" in combined_text
        assert "Phoenix Recruitment" in combined_text
