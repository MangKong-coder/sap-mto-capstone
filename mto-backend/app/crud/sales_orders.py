# sales_order_crud.py

from sqlmodel import Session, select, func
from models import SalesOrders  # make sure this matches your models file
from typing import Dict, Any, Optional
from app.schemas.sales_orders import SalesOrderCreate, SalesOrderUpdate, SalesOrderResponse, SalesOrderSummaryResponse, SalesOrderListResponse


# Create
def create_sales_order(session: Session, sales_order: SalesOrderCreate) -> SalesOrderResponse:
    session.add(sales_order)
    session.commit()
    session.refresh(sales_order)
    return sales_order

# Read (Get by ID)
def get_sales_order(session: Session, sales_order_id: int) -> Optional[SalesOrders]:
    return session.get(SalesOrders, sales_order_id)

# Read (Get all - with pagination)
def get_sales_orders(session: Session, offset: int = 0, limit: int = 10) -> Dict[str, Any]:
    # Count total records
    total = session.exec(select(func.count()).select_from(SalesOrders)).one()
    
    # Fetch paginated results
    statement = select(SalesOrders).offset(offset).limit(limit)
    results = session.exec(statement).all()

    return {
        "data": results,
        "total": total,
        "count": len(results),
        "offset": offset,
        "limit": limit,
        "has_next": (offset + limit) < total,
        "has_prev": offset > 0
    }

# Update
def update_sales_order(session: Session, sales_order_id: int, sales_order_data: dict) -> Optional[SalesOrders]:
    db_sales_order = session.get(SalesOrders, sales_order_id)
    if not db_sales_order:
        return None
    for key, value in sales_order_data.items():
        setattr(db_sales_order, key, value)
    session.add(db_sales_order)
    session.commit()
    session.refresh(db_sales_order)
    return db_sales_order

# Delete
def delete_sales_order(session: Session, sales_order_id: int) -> bool:
    db_sales_order = session.get(SalesOrders, sales_order_id)
    if not db_sales_order:
        return False
    session.delete(db_sales_order)
    session.commit()
    return True

