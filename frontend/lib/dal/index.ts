/**
 * Data Access Layer (DAL) - Main Index
 * Central export point for all domain-specific data access functions
 */

// Products domain
export { getProducts, getProductById, ProductSchema } from './products'

// Dashboard domain
export {
  getDashboardSummary,
  DashboardSummaryResponseSchema,
  TopProductResponseSchema,
  RecentOrderResponseSchema,
} from './dashboard'

export type {
  DashboardSummaryResponse,
  TopProductResponse,
  RecentOrderResponse,
} from './dashboard'

// Orders domain
export {
  getOrders,
  getOrderDetail,
  updateOrderStatus,
  deleteOrder,
  startProduction,
  markProductionInProgress,
  completeProductionOrder,
  OrderDetailSchema,
  OrderSummarySchema,
} from './orders'

export type {
  OrderSummary,
  OrderDetail,
} from './orders'

// Billings domain
export { getBillings, createBilling, BillingSchema } from './billings'

export type { Billing } from './billings'

// Deliveries domain
export { getDeliveries, updateDeliveryStatus, DeliverySchema } from './deliveries'

export type { Delivery } from './deliveries'

// Production Orders domain
export { getProductionOrders, updateProductionStatus, ProductionOrderSchema } from './production-orders'

export type { ProductionOrder } from './production-orders'
