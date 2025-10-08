import {
  type Product,
  type Customer,
  type SalesOrder,
  type ProductionOrder,
  type Delivery,
  type Billing,
  SalesOrderStatus,
  ProductionOrderStatus,
  DeliveryStatus,
} from "./types"

// Mock Products - Mapúa University Official Merchandise
export const mockProducts: Product[] = [
  {
    id: 1,
    name: "Mapúa Cardinals T-Shirt",
    description: "Official Mapúa Cardinals athletic t-shirt in cardinal red with university logo",
    price: 450,
    image_url: "/red-university-tshirt-with-cardinal-logo.jpg",
  },
  {
    id: 2,
    name: "Mapúa Hoodie",
    description: "Premium quality hoodie with embroidered Mapúa University seal",
    price: 1200,
    image_url: "/gray-university-hoodie-with-embroidered-seal.jpg",
  },
  {
    id: 3,
    name: "Engineering Notebook",
    description: "Professional engineering notebook with Mapúa branding, grid pages",
    price: 180,
    image_url: "/engineering-notebook-with-grid-pages.jpg",
  },
  {
    id: 4,
    name: "Mapúa Baseball Cap",
    description: "Adjustable baseball cap with embroidered Cardinals logo",
    price: 350,
    image_url: "/red-baseball-cap-with-university-logo.jpg",
  },
  {
    id: 5,
    name: "University Lanyard",
    description: "Official Mapúa ID lanyard with detachable buckle",
    price: 120,
    image_url: "/red-university-lanyard.jpg",
  },
  {
    id: 6,
    name: "Mapúa Tumbler",
    description: "Insulated stainless steel tumbler with university branding, 500ml",
    price: 550,
    image_url: "/stainless-steel-tumbler-with-university-logo.jpg",
  },
  {
    id: 7,
    name: "Cardinals Polo Shirt",
    description: "Professional polo shirt with Mapúa emblem, perfect for faculty",
    price: 650,
    image_url: "/white-polo-shirt-with-university-emblem.jpg",
  },
  {
    id: 8,
    name: "Mapúa Tote Bag",
    description: "Durable canvas tote bag with Cardinals print",
    price: 280,
    image_url: "/canvas-tote-bag-with-university-print.jpg",
  },
]

// Mock Customer (logged-in user)
export const mockCustomer: Customer = {
  id: 1,
  name: "Juan Dela Cruz",
  email: "juan.delacruz@mapua.edu.ph",
  role: "student",
}

// Mock Customers array for admin pages
export const mockCustomers: Customer[] = [
  mockCustomer,
  {
    id: 2,
    name: "Maria Santos",
    email: "maria.santos@mapua.edu.ph",
    role: "faculty",
  },
  {
    id: 3,
    name: "Engineering Department",
    email: "engineering@mapua.edu.ph",
    role: "department",
  },
]

// Mock Sales Orders
export const mockSalesOrders: SalesOrder[] = [
  {
    id: 1001,
    customer_id: 1,
    total_amount: 1650,
    status: SalesOrderStatus.DELIVERED,
    created_at: new Date("2025-01-15").toISOString(),
    items: [
      { id: 1, sales_order_id: 1001, product_id: 1, quantity: 2, subtotal: 900 },
      { id: 2, sales_order_id: 1001, product_id: 3, quantity: 1, subtotal: 180 },
      { id: 3, sales_order_id: 1001, product_id: 5, quantity: 1, subtotal: 120 },
      { id: 4, sales_order_id: 1001, product_id: 1, quantity: 1, subtotal: 450 },
    ],
  },
  {
    id: 1002,
    customer_id: 1,
    total_amount: 1200,
    status: SalesOrderStatus.IN_PRODUCTION,
    created_at: new Date("2025-01-20").toISOString(),
    items: [{ id: 5, sales_order_id: 1002, product_id: 2, quantity: 1, subtotal: 1200 }],
  },
]

// Mock Production Orders
export const mockProductionOrders: ProductionOrder[] = [
  {
    id: 1,
    sales_order_id: 1001,
    status: ProductionOrderStatus.COMPLETED,
    start_date: new Date("2025-01-16").toISOString(),
    end_date: new Date("2025-01-20").toISOString(),
  },
  {
    id: 2,
    sales_order_id: 1002,
    status: ProductionOrderStatus.IN_PROGRESS,
    start_date: new Date("2025-01-21").toISOString(),
    end_date: null,
  },
]

// Mock Deliveries
export const mockDeliveries: Delivery[] = [
  {
    id: 1,
    sales_order_id: 1001,
    delivery_date: new Date("2025-01-22").toISOString(),
    status: DeliveryStatus.DELIVERED,
  },
  {
    id: 2,
    sales_order_id: 1002,
    delivery_date: null,
    status: DeliveryStatus.PENDING,
  },
]

// Mock Billing
export const mockBillings: Billing[] = [
  {
    id: 1,
    sales_order_id: 1001,
    invoice_number: "INV-2025-001001",
    amount: 1650,
    billed_date: new Date("2025-01-22").toISOString(),
  },
]
