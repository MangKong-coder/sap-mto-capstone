from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from sqlmodel import Session
from app.database import engine
from app.crud.customers import get_customers as fetch_customers, create_customer, get_customer
from app.schemas.customers import CustomerCreate, CustomerResponse, CustomerListResponse

router = APIRouter(tags=["customers"], prefix="/customers")

@router.get("/")
def get_customers_list(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=10),
    search: Optional[str] = Query(None),
):
    skip = (page - 1) * size
    limit = size
    with Session(engine) as session:
        customers, total = fetch_customers(session, skip=skip, limit=limit, search=search)
        customers_response = [CustomerResponse.model_validate(c) for c in customers]
        pages = (total + size - 1) // size if size else 1
        return CustomerListResponse(
            customers=customers_response,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

@router.post("/")
def create_new_customer(customer: CustomerCreate):
    with Session(engine) as session:
        db_customer = create_customer(session, customer)
        return CustomerResponse.model_validate(db_customer)

@router.get("/{customer_id}")
def get_customer_by_id(customer_id: int):
    with Session(engine) as session:
        db_customer = get_customer(session, customer_id)
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return CustomerResponse.model_validate(db_customer)
