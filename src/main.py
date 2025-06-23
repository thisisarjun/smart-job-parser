import os
from contextlib import asynccontextmanager
from typing import Dict

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from src.api.routers.debug_router import router as debug_router
from src.api.routers.text_processor_router import router as text_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(
        f"🚀 Starting {settings.PROJECT_NAME} on {settings.HOST}:{settings.PORT} | ENV: {os.getenv('ENV')}"  # noqa: E501
    )
    yield
    # Shutdown
    print("👋 Shutting down...")


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
app.include_router(debug_router)


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": f"{settings.PROJECT_NAME} is running!"}


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint for deployment monitoring"""
    return {"status": "healthy", "message": "API is operational"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
