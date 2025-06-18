from typing import List
from unittest.mock import Mock

from pinecone import Pinecone

from src.vector_store.models import JobVectorStore
from src.vector_store.stores.pinecone_store import PineconeStore
from tests.fixtures.pinecone_search_result import pinecone_search_result


class TestPineconeStore:

    def test_add_job_details(
        self,
        sample_job_vector_stores: List[JobVectorStore],
        mock_pinecone: Pinecone,
    ) -> None:
        # The mock_pinecone fixture is already applied via autouse=True
        # We just need to set up the mock chain properly
        mock_index = Mock()
        mock_pinecone.return_value.Index.return_value = mock_index

        store = PineconeStore()

        # Now test the method
        store.add_job_details([sample_job_vector_stores[0]])

        # Verify the mock was called correctly
        mock_index.upsert_records.assert_called_once()
        mock_index.upsert_records.assert_called_with(
            "test_namespace",  # This matches the default from settings
            [
                {
                    "id": sample_job_vector_stores[0].job_id,
                    "description": sample_job_vector_stores[
                        0
                    ].get_combined_text_document(),
                    **sample_job_vector_stores[0].model_dump(),
                }
            ],
        )

    def test_similarity_search(
        self,
        mock_pinecone: Pinecone,
    ) -> None:
        # Set up the mock chain
        mock_index = Mock()
        mock_pinecone.return_value.Index.return_value = mock_index
        mock_index.search.return_value = pinecone_search_result

        store = PineconeStore()

        results = store.similarity_search(query="software engineer")

        # Verify the mock was called
        mock_index.search.assert_called_once()
        assert results == [
            JobVectorStore(
                job_id="2",
                job_title="Software Engineer",
                job_description="We are looking for a software engineer with 3 years of experience in Python and Django.",  # noqa: E501
                job_apply_link="https://www.google.com",
                employer_name="Google",
                job_city="San Francisco",
                job_state="CA",
                job_country="USA",
                location_string="San Francisco, CA, USA",
                score=0.9997219443321228,
            )
        ]
