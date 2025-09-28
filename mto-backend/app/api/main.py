from fastapi import APIRouter

from app.api.v1 import products
from app.api.v1 import customers
from app.api.v1 import sales_orders

api_router = APIRouter()
api_router.include_router(products.router)
api_router.include_router(customers.router)
api_router.include_router(sales_orders.router)

