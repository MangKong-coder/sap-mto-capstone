"""
Business Logic Services Layer

This module exports all service functions for business logic operations.
Services coordinate between multiple repositories and enforce business rules.
"""

# Customer service
from app.services.customer_service import (
    register_customer,
    update_customer_profile,
    get_customer_orders,
    get_customer_by_id_service,
    list_customers_service,
    CustomerServiceError,
    CustomerValidationError,
    CustomerNotFoundError,
)

# Product service
from app.services.product_service import (
    add_new_product,
    update_product_details,
    get_product_availability,
    get_product_by_sku,
    get_product_by_id_service,
    list_products_service,
    ProductServiceError,
    ProductValidationError,
    ProductNotFoundError,
)

# Order service
from app.services.order_service import (
    place_order,
    cancel_order,
    get_order_status,
    list_orders_by_customer,
    get_order_by_id_service,
    list_orders_service,
    list_orders_enriched,
    get_order_enriched,
    OrderServiceError,
    OrderValidationError,
    OrderNotFoundError,
    OrderCancellationError,
)

# Planned order service
from app.services.planned_order_service import (
    generate_planned_order,
    update_planned_order_status,
    convert_to_work_order,
    get_planned_order_by_id_service,
    list_planned_orders_service,
    list_planned_orders_by_order,
    PlannedOrderServiceError,
    PlannedOrderValidationError,
    PlannedOrderNotFoundError,
    ConversionError,
)

# Work order service
from app.services.work_order_service import (
    start_work_order,
    confirm_work_order,
    consume_components,
    close_work_order,
    get_work_order_by_id_service,
    list_work_orders_service,
    get_work_order_component_usage,
    WorkOrderServiceError,
    WorkOrderValidationError,
    WorkOrderNotFoundError,
    WorkOrderStateError,
)

# Component service
from app.services.component_service import (
    add_component,
    update_component_details,
    get_component_availability,
    get_component_by_part_code,
    get_component_by_id_service,
    list_components_service,
    ComponentServiceError,
    ComponentValidationError,
    ComponentNotFoundError,
)

# Component usage service
from app.services.component_usage_service import (
    record_component_usage,
    get_usage_by_work_order,
    summarize_component_usage,
    get_component_usage_by_id_service,
    list_component_usages_service,
    get_component_usage_by_component,
    ComponentUsageServiceError,
    ComponentUsageValidationError,
    ComponentUsageNotFoundError,
)

# Delivery service
from app.services.delivery_service import (
    schedule_delivery,
    update_delivery_status,
    get_customer_deliveries,
    get_delivery_by_id_service,
    list_deliveries_service,
    list_deliveries_by_order,
    DeliveryServiceError,
    DeliveryValidationError,
    DeliveryNotFoundError,
)

# Invoice service
from app.services.invoice_service import (
    generate_invoice,
    mark_invoice_paid,
    post_invoice,
    cancel_invoice,
    get_outstanding_invoices,
    get_invoice_by_id_service,
    list_invoices_service,
    list_invoices_by_order,
    InvoiceServiceError,
    InvoiceValidationError,
    InvoiceNotFoundError,
)

# Reporting service
from app.services.reporting_service import (
    get_order_full_flow,
    get_production_status_summary,
    get_component_consumption_summary,
    get_order_component_usage_summary,
    get_customer_order_summary,
    ReportingServiceError,
    ReportNotFoundError,
)

__all__ = [
    # Customer service
    "register_customer",
    "update_customer_profile",
    "get_customer_orders",
    "get_customer_by_id_service",
    "list_customers_service",
    "CustomerServiceError",
    "CustomerValidationError",
    "CustomerNotFoundError",
    # Product service
    "add_new_product",
    "update_product_details",
    "get_product_availability",
    "get_product_by_sku",
    "get_product_by_id_service",
    "list_products_service",
    "ProductServiceError",
    "ProductValidationError",
    "ProductNotFoundError",
    # Order service
    "place_order",
    "cancel_order",
    "get_order_status",
    "list_orders_by_customer",
    "get_order_by_id_service",
    "list_orders_service",
    "OrderServiceError",
    "OrderValidationError",
    "OrderNotFoundError",
    "OrderCancellationError",
    # Planned order service
    "generate_planned_order",
    "update_planned_order_status",
    "convert_to_work_order",
    "get_planned_order_by_id_service",
    "list_planned_orders_service",
    "list_planned_orders_by_order",
    "PlannedOrderServiceError",
    "PlannedOrderValidationError",
    "PlannedOrderNotFoundError",
    "ConversionError",
    # Work order service
    "start_work_order",
    "confirm_work_order",
    "consume_components",
    "close_work_order",
    "get_work_order_by_id_service",
    "list_work_orders_service",
    "get_work_order_component_usage",
    "WorkOrderServiceError",
    "WorkOrderValidationError",
    "WorkOrderNotFoundError",
    "WorkOrderStateError",
    # Component service
    "add_component",
    "update_component_details",
    "get_component_availability",
    "get_component_by_part_code",
    "get_component_by_id_service",
    "list_components_service",
    "ComponentServiceError",
    "ComponentValidationError",
    "ComponentNotFoundError",
    # Component usage service
    "record_component_usage",
    "get_usage_by_work_order",
    "summarize_component_usage",
    "get_component_usage_by_id_service",
    "list_component_usages_service",
    "get_component_usage_by_component",
    "ComponentUsageServiceError",
    "ComponentUsageValidationError",
    "ComponentUsageNotFoundError",
    # Delivery service
    "schedule_delivery",
    "update_delivery_status",
    "get_customer_deliveries",
    "get_delivery_by_id_service",
    "list_deliveries_service",
    "list_deliveries_by_order",
    "DeliveryServiceError",
    "DeliveryValidationError",
    "DeliveryNotFoundError",
    # Invoice service
    "generate_invoice",
    "mark_invoice_paid",
    "post_invoice",
    "cancel_invoice",
    "get_outstanding_invoices",
    "get_invoice_by_id_service",
    "list_invoices_service",
    "list_invoices_by_order",
    "InvoiceServiceError",
    "InvoiceValidationError",
    "InvoiceNotFoundError",
    # Reporting service
    "get_order_full_flow",
    "get_production_status_summary",
    "get_component_consumption_summary",
    "get_order_component_usage_summary",
    "get_customer_order_summary",
    "ReportingServiceError",
    "ReportNotFoundError",
]

