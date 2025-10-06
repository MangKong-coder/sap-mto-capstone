"use client"

import { create } from "zustand"
import { type Billing, type Product, SalesOrderStatus, ProductionOrderStatus, DeliveryStatus } from "./types"
import { useOrdersStore } from "./orders-store"
import { mockProducts } from "./mock-data"

interface AdminStore {
  products: Product[]
  updateOrderStatus: (orderId: number, status: SalesOrderStatus) => void
  startProduction: (orderId: number) => void
  updateProductionStatus: (productionOrderId: number, status: ProductionOrderStatus) => void
  updateDeliveryStatus: (deliveryId: number, status: DeliveryStatus) => void
  createBilling: (orderId: number) => void
  updateProduct: (productId: number, updates: Partial<Product>) => void
  deleteProduct: (productId: number) => void
  addProduct: (product: Omit<Product, "id">) => Product
}

export const useAdminStore = create<AdminStore>((set, get) => ({
  products: mockProducts,

  updateOrderStatus: (orderId, status) => {
    const ordersStore = useOrdersStore.getState()
    const orders = ordersStore.orders.map((order) => (order.id === orderId ? { ...order, status } : order))
    useOrdersStore.setState({ orders })
  },

  startProduction: (orderId) => {
    const ordersStore = useOrdersStore.getState()
    const productionOrders = ordersStore.productionOrders.map((po) =>
      po.sales_order_id === orderId
        ? { ...po, status: ProductionOrderStatus.IN_PROGRESS, start_date: new Date().toISOString() }
        : po,
    )
    useOrdersStore.setState({ productionOrders })

    // Update order status
    get().updateOrderStatus(orderId, SalesOrderStatus.IN_PRODUCTION)
  },

  updateProductionStatus: (productionOrderId, status) => {
    const ordersStore = useOrdersStore.getState()
    const productionOrders = ordersStore.productionOrders.map((po) =>
      po.id === productionOrderId
        ? {
            ...po,
            status,
            end_date: status === ProductionOrderStatus.COMPLETED ? new Date().toISOString() : po.end_date,
          }
        : po,
    )
    useOrdersStore.setState({ productionOrders })

    // If completed, update order status
    if (status === ProductionOrderStatus.COMPLETED) {
      const po = ordersStore.productionOrders.find((p) => p.id === productionOrderId)
      if (po) {
        get().updateOrderStatus(po.sales_order_id, SalesOrderStatus.READY_FOR_DELIVERY)
      }
    }
  },

  updateDeliveryStatus: (deliveryId, status) => {
    const ordersStore = useOrdersStore.getState()
    const deliveries = ordersStore.deliveries.map((d) =>
      d.id === deliveryId
        ? {
            ...d,
            status,
            delivery_date: status === DeliveryStatus.DELIVERED ? new Date().toISOString() : d.delivery_date,
          }
        : d,
    )
    useOrdersStore.setState({ deliveries })

    // If delivered, update order status
    if (status === DeliveryStatus.DELIVERED) {
      const delivery = ordersStore.deliveries.find((d) => d.id === deliveryId)
      if (delivery) {
        get().updateOrderStatus(delivery.sales_order_id, SalesOrderStatus.DELIVERED)
      }
    }
  },

  createBilling: (orderId) => {
    const ordersStore = useOrdersStore.getState()
    const order = ordersStore.orders.find((o) => o.id === orderId)
    if (!order) return

    const newBilling: Billing = {
      id: ordersStore.billings.length + 1,
      sales_order_id: orderId,
      invoice_number: `INV-${orderId}-${Date.now()}`,
      amount: order.total_amount,
      billed_date: new Date().toISOString(),
    }

    useOrdersStore.setState({
      billings: [...ordersStore.billings, newBilling],
    })

    // Update order status
    get().updateOrderStatus(orderId, SalesOrderStatus.BILLED)
  },

  updateProduct: (productId, updates) => {
    set((state) => ({
      products: state.products.map((p) => (p.id === productId ? { ...p, ...updates } : p)),
    }))
  },

  deleteProduct: (productId) => {
    set((state) => ({
      products: state.products.filter((p) => p.id !== productId),
    }))
  },

  addProduct: (product) => {
    const newProduct: Product = {
      ...product,
      id: Math.max(...get().products.map((p) => p.id)) + 1,
    }
    set((state) => ({
      products: [...state.products, newProduct],
    }))
    return newProduct
  },
}))
