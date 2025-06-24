from pinecone.core.openapi.db_data.model.hit import Hit
from pinecone.core.openapi.db_data.model.search_records_response import SearchRecordsResponse
from pinecone.core.openapi.db_data.model.search_records_response_result import SearchRecordsResponseResult
from pinecone.core.openapi.db_data.model.search_usage import SearchUsage

pinecone_search_result = SearchRecordsResponse(
    result=SearchRecordsResponseResult(
        hits=[
            Hit(
                **{
                    "_id": "2",
                    "_score": 0.9997219443321228,
                    "fields": {
                        "description": "Job Title: Software Engineer\n"
                        "Company: Google\n"
                        "Location: San Francisco, CA, "
                        "USA\n"
                        "\n"
                        "Description: We are looking "
                        "for a software engineer with "
                        "3 years of experience in "
                        "Python and Django.",
                        "employer_name": "Google",
                        "job_apply_link": "https://www.google.com",
                        "job_city": "San Francisco",
                        "job_country": "USA",
                        "job_description": "We are looking for a "
                        "software engineer with 3 "
                        "years of experience in "
                        "Python and Django.",
                        "job_id": "2",
                        "job_state": "CA",
                        "job_title": "Software Engineer",
                        "location_string": "San Francisco, CA, " "USA",
                    },
                }
            )
        ]
    ),
    usage=SearchUsage(**{"embed_total_tokens": 21, "read_units": 6, "rerank_units": 1}),
)
