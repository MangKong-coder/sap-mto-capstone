"""
Reporting Service - Cross-entity insights and aggregations.
Provides comprehensive views of order flow, production status, and component usage.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.repositories import (
    get_order_by_id,
    list_order_component_usage,
)
from app.models import (
    Order, WorkOrder, WorkOrderStatus, Delivery, Invoice,
    ComponentUsage, Component
)


class ReportingServiceError(Exception):
    """Base exception for reporting service errors."""
    pass


class ReportNotFoundError(ReportingServiceError):
    """Raised when report data is not found."""
    pass


def get_order_full_flow(db: Session, order_id: int) -> Dict[str, Any]:
    """
    Trace an order through the complete MTO flow:
    Order → Planned Orders → Work Orders → Component Usage → Delivery → Invoice
    
    Args:
        db: Database session
        order_id: Order ID
    
    Returns:
        Dictionary with complete order flow data
        
    Raises:
        ReportNotFoundError: If order not found
    """
    order = get_order_by_id(db, order_id)
    if not order:
        raise ReportNotFoundError(f"Order with ID {order_id} not found")
    
    # Customer information
    customer_info = {
        "id": order.customer.id,
        "name": order.customer.name,
        "email": order.customer.email,
    }
    
    # Order items
    items = []
    for item in order.items:
        item_data = {
            "id": item.id,
            "product_id": item.product_id,
            "product_name": item.product.name,
            "product_sku": item.product.sku,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "total_price": item.quantity * item.unit_price,
            "planned_orders": [],
            "work_orders": [],
        }
        
        # Planned orders for this item
        for planned in item.planned_orders:
            item_data["planned_orders"].append({
                "id": planned.id,
                "quantity": planned.quantity,
                "status": planned.status.value,
                "planned_start": planned.planned_start.isoformat() if planned.planned_start else None,
                "planned_end": planned.planned_end.isoformat() if planned.planned_end else None,
            })
        
        # Work orders for this item
        for wo in item.work_orders:
            wo_data = {
                "id": wo.id,
                "quantity": wo.quantity,
                "status": wo.status.value,
                "start_date": wo.start_date.isoformat() if wo.start_date else None,
                "end_date": wo.end_date.isoformat() if wo.end_date else None,
                "components_used": [],
            }
            
            # Component usage for this work order
            for usage in wo.component_usages:
                wo_data["components_used"].append({
                    "component_id": usage.component_id,
                    "component_name": usage.component.name,
                    "part_code": usage.component.part_code,
                    "quantity": usage.quantity,
                    "cost": usage.component.cost,
                    "total_cost": usage.quantity * usage.component.cost,
                })
            
            item_data["work_orders"].append(wo_data)
        
        items.append(item_data)
    
    # Deliveries
    deliveries = []
    for delivery in order.deliveries:
        deliveries.append({
            "id": delivery.id,
            "quantity": delivery.quantity,
            "status": delivery.status.value,
            "delivered_at": delivery.delivered_at.isoformat() if delivery.delivered_at else None,
        })
    
    # Invoices
    invoices = []
    for invoice in order.invoices:
        invoices.append({
            "id": invoice.id,
            "total_amount": invoice.total_amount,
            "status": invoice.status.value,
            "invoice_date": invoice.invoice_date.isoformat() if invoice.invoice_date else None,
        })
    
    return {
        "order_id": order.id,
        "status": order.status.value,
        "order_date": order.order_date.isoformat() if order.order_date else None,
        "delivery_date": order.delivery_date.isoformat() if order.delivery_date else None,
        "customer": customer_info,
        "items": items,
        "deliveries": deliveries,
        "invoices": invoices,
    }


def get_production_status_summary(db: Session) -> Dict[str, Any]:
    """
    Summarize work order statuses across the system.
    
    Args:
        db: Database session
    
    Returns:
        Dictionary with production status summary
    """
    # Count work orders by status
    status_counts = db.query(
        WorkOrder.status,
        func.count(WorkOrder.id).label('count')
    ).group_by(WorkOrder.status).all()
    
    summary = {
        "total_work_orders": 0,
        "by_status": {},
    }
    
    for status, count in status_counts:
        summary["by_status"][status.value] = count
        summary["total_work_orders"] += count
    
    # Get recent work orders
    recent_work_orders = db.query(WorkOrder).order_by(
        WorkOrder.created_at.desc()
    ).limit(10).all()
    
    summary["recent_work_orders"] = [
        {
            "id": wo.id,
            "status": wo.status.value,
            "quantity": wo.quantity,
            "order_item_id": wo.order_item_id,
            "start_date": wo.start_date.isoformat() if wo.start_date else None,
            "end_date": wo.end_date.isoformat() if wo.end_date else None,
        }
        for wo in recent_work_orders
    ]
    
    return summary


def get_component_consumption_summary(db: Session) -> List[Dict[str, Any]]:
    """
    Aggregate raw material usage across all production.
    
    Args:
        db: Database session
    
    Returns:
        List of dictionaries with component consumption data
    """
    # Group component usage by component
    consumption = db.query(
        Component.id,
        Component.part_code,
        Component.name,
        Component.cost,
        func.sum(ComponentUsage.quantity).label('total_used'),
        func.count(ComponentUsage.id).label('usage_count')
    ).join(
        ComponentUsage, Component.id == ComponentUsage.component_id
    ).group_by(
        Component.id, Component.part_code, Component.name, Component.cost
    ).all()
    
    summary = []
    for comp_id, part_code, name, cost, total_used, usage_count in consumption:
        summary.append({
            "component_id": comp_id,
            "part_code": part_code,
            "name": name,
            "cost": cost,
            "total_quantity_used": float(total_used) if total_used else 0.0,
            "total_cost": float(cost * total_used) if total_used else 0.0,
            "usage_count": usage_count,
        })
    
    # Sort by total cost descending
    summary.sort(key=lambda x: x["total_cost"], reverse=True)
    
    return summary


def get_order_component_usage_summary(db: Session, order_id: int) -> List[Dict[str, Any]]:
    """
    Get component usage summary for a specific order using the database view.
    
    Args:
        db: Database session
        order_id: Order ID
    
    Returns:
        List of dictionaries with component usage per order
        
    Raises:
        ReportNotFoundError: If order not found
    """
    order = get_order_by_id(db, order_id)
    if not order:
        raise ReportNotFoundError(f"Order with ID {order_id} not found")
    
    # Use the view accessor from repository
    view_results = list_order_component_usage(db, order_id=order_id)
    
    summary = []
    for record in view_results:
        # Get component details
        component = db.query(Component).filter(Component.id == record.component_id).first()
        
        summary.append({
            "order_id": record.order_id,
            "component_id": record.component_id,
            "component_name": component.name if component else "Unknown",
            "part_code": component.part_code if component else "Unknown",
            "cost": component.cost if component else 0.0,
            "total_used": record.total_used,
            "total_cost": (component.cost * record.total_used) if component else 0.0,
        })
    
    return summary


def get_customer_order_summary(db: Session, customer_id: int) -> Dict[str, Any]:
    """
    Get summary of all orders for a customer.
    
    Args:
        db: Database session
        customer_id: Customer ID
    
    Returns:
        Dictionary with customer order summary
    """
    from app.models import Customer, OrderStatus
    
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise ReportNotFoundError(f"Customer with ID {customer_id} not found")
    
    orders = customer.orders
    
    summary = {
        "customer_id": customer.id,
        "customer_name": customer.name,
        "total_orders": len(orders),
        "orders_by_status": {},
        "total_revenue": 0.0,
    }
    
    # Count by status and calculate revenue
    for order in orders:
        status = order.status.value
        summary["orders_by_status"][status] = summary["orders_by_status"].get(status, 0) + 1
        
        # Calculate order value
        order_value = sum(item.quantity * item.unit_price for item in order.items)
        summary["total_revenue"] += order_value
    
    return summary
