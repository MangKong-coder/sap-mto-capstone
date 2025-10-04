from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="MTO (Make-to-Order) Manufacturing Flow API",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include main API router with all domain routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": "MTO Backend API", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


