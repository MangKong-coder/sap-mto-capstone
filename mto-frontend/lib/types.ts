export interface SalesOrder {
  id: string
  orderNumber: string
  customer: string // Department or Campus
  customerType: "Department" | "Campus"
  material: string // School merchandise item
  quantity: number
  deliveryDate: string
  status: "Open" | "In Planning" | "In Production" | "Delivered" | "Billed" | "Cancelled"
  createdDate: string
  netValue: number
  plant: string // Bookstore location
  priority: "Standard" | "Urgent" | "Rush"
}

export interface PlannedOrder {
  id: string
  plannedOrderNumber: string
  salesOrderNumber: string
  material: string
  quantity: number
  startDate: string
  endDate: string
  status: "Created" | "Converted" | "Cancelled"
  plant: string
}

export interface ProductionOrder {
  id: string
  productionOrderNumber: string
  plannedOrderNumber: string
  salesOrderNumber: string
  material: string
  quantity: number
  startDate: string
  endDate: string
  status: "Created" | "Released" | "In Progress" | "Confirmed" | "Completed"
  confirmedQuantity: number
  plant: string
}

export interface Delivery {
  id: string
  deliveryNumber: string
  salesOrderNumber: string
  productionOrderNumber: string
  customer: string
  deliveryDate: string
  quantity: number
  status: "Created" | "Picked" | "Packed" | "Shipped" | "Delivered"
  trackingNumber?: string
}

export interface Billing {
  id: string
  billingNumber: string
  salesOrderNumber: string
  deliveryNumber: string
  customer: string
  billingDate: string
  netValue: number
  status: "Created" | "Posted" | "Paid" | "Cancelled"
  paymentTerms: string
}
