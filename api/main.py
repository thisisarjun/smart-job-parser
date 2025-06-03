from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.text_processor.text_processor import split_text, embed_text

app = FastAPI(
    title="Text Processing API",
    description="API for testing text splitting and embedding functionality",
    version="1.0.0"
)


# Request model
class TextProcessRequest(BaseModel):
    text: str = Field(..., description="Text to be processed (split and embedded)")
    chunk_size: int = Field(1000, description="Maximum size of each chunk", ge=1, le=10000)
    chunk_overlap: int = Field(200, description="Overlap between chunks", ge=0, le=1000)


# Response model
class TextProcessResponse(BaseModel):
    chunks: List[str]
    embeddings: List[List[float]]
    chunk_count: int
    original_length: int


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Text Processing API",
        "version": "1.0.0",
        "endpoint": "/process-text",
        "docs": "/docs"
    }


@app.post("/process-text", response_model=TextProcessResponse)
async def process_text_endpoint(request: TextProcessRequest):
    """
    Split text into chunks and generate embeddings for each chunk
    
    - **text**: The text to process
    - **chunk_size**: Maximum size of each chunk (default: 1000)
    - **chunk_overlap**: Overlap between chunks (default: 200)
    """
    try:
        # Split the text
        chunks = split_text(
            text=request.text,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )
        
        # Generate embeddings for each chunk
        embeddings = []
        for chunk in chunks:
            embedding = embed_text(chunk)
            embeddings.append(embedding)
        
        return TextProcessResponse(
            chunks=chunks,
            embeddings=embeddings,
            chunk_count=len(chunks),
            original_length=len(request.text)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Text Processing API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 