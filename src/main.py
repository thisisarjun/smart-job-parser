from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.text_processor_router import router as text_processor_router

app = FastAPI(
    title="Smart Job Parser",
    description="API for parsing and analyzing job listings",
    version="0.1.0",
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
app.include_router(text_processor_router)


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Welcome to Smart Job Parser API"}


@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}
