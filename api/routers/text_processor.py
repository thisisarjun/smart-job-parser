from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Any
import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.text_processor.text_processor import TextProcessor

text_processor = TextProcessor()

router = APIRouter(
    prefix="/text",
    tags=["text-processing"],
    responses={404: {"description": "Not found"}},
)


# Request model
class TextProcessRequest(BaseModel):
    text: str = Field(..., description="Text to be processed (split, embedded, and stored)")
    query: str = Field(..., description="Query to search in the processed text")
    chunk_size: int = Field(1000, description="Maximum size of each chunk", ge=1, le=10000)
    chunk_overlap: int = Field(200, description="Overlap between chunks", ge=0, le=1000)


# Response model
class TextProcessResponse(BaseModel):
    search_results: List[Any]  # Search results from vector store
    chunk_count: int
    original_length: int


@router.post("/process", response_model=TextProcessResponse)
async def process_text_endpoint(request: TextProcessRequest):
    """
    Process text: split into chunks, embed them, store in vector store, and search
    
    - **text**: The text to process
    - **query**: Query to search in the processed text
    - **chunk_size**: Maximum size of each chunk (default: 1000)
    - **chunk_overlap**: Overlap between chunks (default: 200)
    
    Returns search results from the vector store instead of raw embeddings.
    """
    try:
        # Split the text
        chunks = text_processor.split_text(
            text=request.text,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )
        
        # Add chunks to vector store (this handles embedding internally)
        text_processor.add_texts_to_vector_store(chunks)
        
        # Search the vector store with the query
        search_results = text_processor.vector_store.similarity_search(
            query=request.query,
            k=min(len(chunks), 5)  # Return top 5 results or fewer if less chunks
        )
        
        return TextProcessResponse(
            search_results=search_results,
            chunk_count=len(chunks),
            original_length=len(request.text)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}") 