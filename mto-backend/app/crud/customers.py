from typing import List, Optional
from sqlmodel import Session, select, func, and_, or_, col
from app.models import Customers
from app.schemas.customers import CustomerCreate

def get_customers(
    session: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
) -> tuple[List[Customers], int]:
    query = select(Customers)
    count_query = select(func.count()).select_from(Customers)
    
    conditions = []
    
    if search:
        search_filter = or_(
            col(Customers.name).ilike(f"%{search}%"),
            col(Customers.code).ilike(f"%{search}%"),
            col(Customers.email).ilike(f"%{search}%")
        )
        conditions.append(search_filter)
    
    if conditions:
        filter_condition = and_(*conditions)
        query = query.where(filter_condition)
        count_query = count_query.where(filter_condition)
    
    total = session.exec(count_query).one()
    
    query = query.offset(skip).limit(limit)
    
    customers = list(session.exec(query).all())
    
    return customers, total

def create_customer(session: Session, customer_data: CustomerCreate) -> Customers:
    customer = Customers(**customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

def get_customer(session: Session, customer_id: int) -> Optional[Customers]:
    return session.get(Customers, customer_id)
