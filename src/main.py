import os
from contextlib import asynccontextmanager
from typing import Dict

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from src.api.routers.debug_router import router as debug_router
from src.api.routers.job_search_router import router as job_search_router
from src.api.routers.text_processor_router import router as text_router
from src.logger import get_logger, setup_logging_from_env

# Setup logging
setup_logging_from_env()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} on {settings.HOST}:{settings.PORT} | ENV: {os.getenv('ENV')}")
    yield
    # Shutdown
    logger.info("👋 Shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for parsing and processing job data",
    version="1.0.0",
    lifespan=lifespan,
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
app.include_router(text_router, prefix=settings.API_PREFIX, tags=["text_processor"])

if settings.ENV == "development":
    app.include_router(debug_router)


app.include_router(job_search_router)


@app.get("/")
async def root() -> Dict[str, str]:
    logger.debug("Root endpoint accessed")
    return {"message": f"{settings.PROJECT_NAME} is running!"}


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for deployment monitoring"""
    logger.debug("Health check endpoint accessed")
    return {"status": "healthy", "message": "API is operational"}


if __name__ == "__main__":
    logger.info(f"Starting application server on {settings.HOST}:{settings.PORT}")
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
