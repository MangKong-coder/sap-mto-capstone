from fastapi import APIRouter
from sqlmodel import Session
from app.database import engine
from app.crud.products import get_products as fetch_products

router = APIRouter(tags=["products"], prefix="/products")

@router.get("/")
async def get_products():
    with Session(engine) as session:
        products = fetch_products(session)
        return {"products": products[0]}