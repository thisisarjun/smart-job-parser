from fastapi import FastAPI
import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from api.routers import text_processor

app = FastAPI(
    title="Text Processing API",
    description="API for testing text splitting and embedding functionality",
    version="1.0.0"
)

# Include routers
app.include_router(text_processor.router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Text Processing API",
        "version": "1.0.0",
        "endpoint": "/text/process",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 