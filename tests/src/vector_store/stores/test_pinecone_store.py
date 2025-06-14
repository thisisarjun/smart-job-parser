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
        print(pinecone_search_result)
        store = PineconeStore()
        store.index = mock_pinecone.Index
        upsert_records_spy = store.index.upsert_records = Mock()
        store.add_job_details(sample_job_vector_stores[0])
        upsert_records_spy.assert_called_once()
        upsert_records_spy.assert_called_with(
            "jobs",
            [
                {
                    "id": sample_job_vector_stores[0].job_id,
                    "job_id": sample_job_vector_stores[0].job_id,
                    "description": sample_job_vector_stores[
                        0
                    ].get_combined_text_document(),
                    "employer_name": sample_job_vector_stores[0].employer_name,
                    "job_title": sample_job_vector_stores[0].job_title,
                    "job_city": sample_job_vector_stores[0].job_city,
                    "job_state": sample_job_vector_stores[0].job_state,
                    "job_country": sample_job_vector_stores[0].job_country,
                    "job_description": sample_job_vector_stores[0].job_description,
                    "job_apply_link": sample_job_vector_stores[0].job_apply_link,
                    "location_string": sample_job_vector_stores[0].location_string,
                    "score": None,
                }
            ],
        )

    def test_similarity_search(
        self,
        mock_pinecone: Pinecone,
    ) -> None:
        store = PineconeStore()
        store.index = mock_pinecone.Index
        similarity_search_spy = store.index.search = Mock(
            return_value=pinecone_search_result
        )
        results = store.similarity_search(query="software engineer")
        similarity_search_spy.assert_called_once()
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
