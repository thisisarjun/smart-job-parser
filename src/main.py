from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.debug_router import router as debug_router
from src.api.routers.text_processor_router import router as text_router
from src.config import config

app = FastAPI(
    title=config["PROJECT_NAME"],
    description="API for parsing and processing job data",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(text_router, prefix=config["API_PREFIX"], tags=["text_processor"])
app.include_router(debug_router)


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": f"{config['PROJECT_NAME']} is running!"}


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for deployment monitoring"""
    return {"status": "healthy", "message": "API is operational"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config["HOST"], port=config["PORT"])
