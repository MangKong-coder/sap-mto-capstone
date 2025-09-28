from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from sqlmodel import Session
from app.database import engine
from app.crud.sales_orders import create_sales_order, get_sales_orders, get_sales_order, update_sales_order
from app.schemas.sales_orders import SalesOrderCreate, SalesOrderUpdate, SalesOrderResponse, SalesOrderSummaryResponse, SalesOrderListResponse

router = APIRouter(tags=["sales-orders"], prefix="/sales-orders")

@router.post("/", response_model=SalesOrderResponse)
def create_new_sales_order(so: SalesOrderCreate):
    with Session(engine) as session:
        try:
            db_so = create_sales_order(session, so)
            return SalesOrderResponse.model_validate(db_so)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=SalesOrderListResponse)
def get_sales_orders_list(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
):
    skip = (page - 1) * size
    limit = size
    with Session(engine) as session:
        sos, total = get_sales_orders(session, skip=skip, limit=limit, search=search)
        sos_response = [SalesOrderSummaryResponse.model_validate(so) for so in sos]
        pages = (total + size - 1) // size if size else 1
        return SalesOrderListResponse(
            sales_orders=sos_response,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

@router.get("/{so_id}", response_model=SalesOrderResponse)
def get_sales_order_by_id(so_id: int):
    with Session(engine) as session:
        db_so = get_sales_order(session, so_id)
        if not db_so:
            raise HTTPException(status_code=404, detail="Sales order not found")
        return SalesOrderResponse.model_validate(db_so)

@router.put("/{so_id}", response_model=SalesOrderResponse)
def update_sales_order_func(so_id: int, update_data: SalesOrderUpdate):
    with Session(engine) as session:
        db_so = update_sales_order(session, so_id, update_data)
        if not db_so:
            raise HTTPException(status_code=404, detail="Sales order not found")
        return SalesOrderResponse.model_validate(db_so)

