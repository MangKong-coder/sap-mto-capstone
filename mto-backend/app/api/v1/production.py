from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.db.models import ProductionOrder, WorkCenter, RoutingStep
from app.schemas.production import (
    ProductionOrderCreate, ProductionOrderResponse,
    WorkCenterCreate, WorkCenterResponse,
    RoutingStepCreate, RoutingStepResponse
)

router = APIRouter()


@router.get("/production-orders", response_model=List[ProductionOrderResponse])
def get_production_orders(db: Session = Depends(get_db)):
    return db.query(ProductionOrder).all()


@router.post("/production-orders", response_model=ProductionOrderResponse)
def create_production_order(production_order: ProductionOrderCreate, db: Session = Depends(get_db)):
    db_production_order = ProductionOrder(
        order_id=production_order.order_id,
        product_id=production_order.product_id,
        planned_quantity=production_order.planned_quantity,
        status=production_order.status,
        scheduled_date=production_order.scheduled_date
    )
    db.add(db_production_order)
    db.commit()
    db.refresh(db_production_order)
    return db_production_order


@router.get("/work-centers", response_model=List[WorkCenterResponse])
def get_work_centers(db: Session = Depends(get_db)):
    return db.query(WorkCenter).all()


@router.post("/work-centers", response_model=WorkCenterResponse)
def create_work_center(work_center: WorkCenterCreate, db: Session = Depends(get_db)):
    db_work_center = WorkCenter(
        name=work_center.name,
        capacity=work_center.capacity
    )
    db.add(db_work_center)
    db.commit()
    db.refresh(db_work_center)
    return db_work_center


@router.get("/routing-steps", response_model=List[RoutingStepResponse])
def get_routing_steps(db: Session = Depends(get_db)):
    return db.query(RoutingStep).all()


@router.post("/routing-steps", response_model=RoutingStepResponse)
def create_routing_step(routing_step: RoutingStepCreate, db: Session = Depends(get_db)):
    db_routing_step = RoutingStep(
        product_id=routing_step.product_id,
        work_center_id=routing_step.work_center_id,
        step_number=routing_step.step_number,
        description=routing_step.description,
        duration_minutes=routing_step.duration_minutes
    )
    db.add(db_routing_step)
    db.commit()
    db.refresh(db_routing_step)
    return db_routing_step
