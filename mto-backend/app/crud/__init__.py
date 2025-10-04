"""
CRUD Operations
Exports repository functions and legacy CRUD operations.
"""

# Import all repository functions from repositories subfolder
from app.crud.repositories import (
    # Customer
    create_customer,
    get_customer_by_id,
    list_customers,
    update_customer,
    delete_customer,
    # Product
    create_product,
    get_product_by_id,
    list_products,
    update_product,
    delete_product,
    # Order
    create_order,
    get_order_by_id,
    list_orders,
    list_orders_with_details,
    get_order_with_details,
    update_order,
    delete_order,
    # OrderItem
    create_order_item,
    get_order_item_by_id,
    list_order_items,
    update_order_item,
    delete_order_item,
    # PlannedOrder
    create_planned_order,
    get_planned_order_by_id,
    list_planned_orders,
    update_planned_order,
    delete_planned_order,
    # WorkOrder
    create_work_order,
    get_work_order_by_id,
    list_work_orders,
    update_work_order,
    delete_work_order,
    # Component
    create_component,
    get_component_by_id,
    list_components,
    update_component,
    delete_component,
    # ComponentUsage
    create_component_usage,
    get_component_usage_by_id,
    list_component_usages,
    update_component_usage,
    delete_component_usage,
    # Delivery
    create_delivery,
    get_delivery_by_id,
    list_deliveries,
    update_delivery,
    delete_delivery,
    # Invoice
    create_invoice,
    get_invoice_by_id,
    list_invoices,
    update_invoice,
    delete_invoice,
    # OrderComponentUsage (view)
    list_order_component_usage,
)

__all__ = [
    # Customer
    "create_customer",
    "get_customer_by_id",
    "list_customers",
    "update_customer",
    "delete_customer",
    # Product
    "create_product",
    "get_product_by_id",
    "list_products",
    "update_product",
    "delete_product",
    # Order
    "create_order",
    "get_order_by_id",
    "list_orders",
    "list_orders_with_details",
    "get_order_with_details",
    "update_order",
    "delete_order",
    # OrderItem
    "create_order_item",
    "get_order_item_by_id",
    "list_order_items",
    "update_order_item",
    "delete_order_item",
    # PlannedOrder
    "create_planned_order",
    "get_planned_order_by_id",
    "list_planned_orders",
    "update_planned_order",
    "delete_planned_order",
    # WorkOrder
    "create_work_order",
    "get_work_order_by_id",
    "list_work_orders",
    "update_work_order",
    "delete_work_order",
    # Component
    "create_component",
    "get_component_by_id",
    "list_components",
    "update_component",
    "delete_component",
    # ComponentUsage
    "create_component_usage",
    "get_component_usage_by_id",
    "list_component_usages",
    "update_component_usage",
    "delete_component_usage",
    # Delivery
    "create_delivery",
    "get_delivery_by_id",
    "list_deliveries",
    "update_delivery",
    "delete_delivery",
    # Invoice
    "create_invoice",
    "get_invoice_by_id",
    "list_invoices",
    "update_invoice",
    "delete_invoice",
    # OrderComponentUsage (view)
    "list_order_component_usage",
]

