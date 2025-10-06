export enum SalesOrderStatus {
  CREATED = "created",
  IN_PRODUCTION = "in_production",
  READY_FOR_DELIVERY = "ready_for_delivery",
  DELIVERED = "delivered",
  BILLED = "billed",
  CANCELLED = "cancelled",
}

export enum ProductionOrderStatus {
  PLANNED = "planned",
  IN_PROGRESS = "in_progress",
  COMPLETED = "completed",
  CANCELLED = "cancelled",
}

export enum DeliveryStatus {
  PENDING = "pending",
  DELIVERED = "delivered",
  CANCELLED = "cancelled",
}

export interface Customer {
  id: number
  name: string
  email: string
  role: "student" | "faculty" | "department"
}

export interface Product {
  id: number
  name: string
  description: string
  price: number
  stock_qty: number
  image_url: string | null
}

export interface SalesOrderItem {
  id: number
  sales_order_id: number
  product_id: number
  quantity: number
  subtotal: number
}

export interface SalesOrder {
  id: number
  customer_id: number
  total_amount: number
  status: SalesOrderStatus
  created_at: string
  items: SalesOrderItem[]
}

export interface ProductionOrder {
  id: number
  sales_order_id: number
  status: ProductionOrderStatus
  start_date: string | null
  end_date: string | null
}

export interface Delivery {
  id: number
  sales_order_id: number
  delivery_date: string | null
  status: DeliveryStatus
}

export interface Billing {
  id: number
  sales_order_id: number
  invoice_number: string | null
  amount: number
  billed_date: string
}

export interface CartItem {
  product: Product
  quantity: number
}
