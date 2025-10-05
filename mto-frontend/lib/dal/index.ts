/**
 * Data Access Layer (DAL) - Main Export
 * 
 * This module exports all DAL functions for easy importing
 * throughout the frontend application.
 */

// Orders DAL
export {
  getOrders,
  getOrderById,
  createOrder,
  cancelOrder,
  getOrdersByCustomer,
  getOrderStatus,
  type OrderStatusResponse,
} from './orders'

// Customers DAL
export {
  getCustomers,
  getCustomerById,
  createCustomer,
  updateCustomer,
  type Customer,
  type CustomerCreate,
} from './customers'

// Products DAL
export {
  getProducts,
  getProductById,
  getProductBySku,
  createProduct,
  updateProduct,
  type Product,
  type ProductCreate,
} from './products'

// Work Centers DAL
export {
  getWorkCenters,
  getWorkCenterById,
  createWorkCenter,
  updateWorkCenter,
  deleteWorkCenter,
  type WorkCenter,
  type WorkCenterCreate,
} from './work-centers'
