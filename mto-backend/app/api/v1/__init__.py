from fastapi import APIRouter
from .auth import router as auth_router
from .sales import router as sales_router
from .production import router as production_router
from .inventory import router as inventory_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(sales_router, prefix="/sales", tags=["sales"])
api_router.include_router(production_router, prefix="/production", tags=["production"]) 
api_router.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
