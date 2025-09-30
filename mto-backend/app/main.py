from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import sales_orders, production_orders, deliveries, users
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
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

# Include routers
app.include_router(sales_orders.router, prefix=f"{settings.API_V1_STR}/sales-orders", tags=["sales-orders"])
app.include_router(production_orders.router, prefix=f"{settings.API_V1_STR}/production-orders", tags=["production-orders"])
app.include_router(deliveries.router, prefix=f"{settings.API_V1_STR}/deliveries", tags=["deliveries"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])


@app.get("/")
def root():
    return {"message": "MTO Backend API", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

