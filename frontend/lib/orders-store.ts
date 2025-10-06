"use client"

import { create } from "zustand"
import { persist } from "zustand/middleware"
import {
  type SalesOrder,
  type SalesOrderItem,
  SalesOrderStatus,
  type ProductionOrder,
  ProductionOrderStatus,
  type Delivery,
  DeliveryStatus,
  type Billing,
} from "./types"
import { mockSalesOrders, mockProductionOrders, mockDeliveries, mockBillings } from "./mock-data"

interface OrdersStore {
  orders: SalesOrder[]
  productionOrders: ProductionOrder[]
  deliveries: Delivery[]
  billings: Billing[]
  nextOrderId: number
  createOrder: (
    customerId: number,
    items: Omit<SalesOrderItem, "id" | "sales_order_id">[],
    totalAmount: number,
  ) => SalesOrder
  getOrderById: (orderId: number) => SalesOrder | undefined
  getOrdersByCustomer: (customerId: number) => SalesOrder[]
  getProductionOrderByOrderId: (orderId: number) => ProductionOrder | undefined
  getDeliveryByOrderId: (orderId: number) => Delivery | undefined
  getBillingByOrderId: (orderId: number) => Billing | undefined
}

export const useOrdersStore = create<OrdersStore>()(
  persist(
    (set, get) => ({
      orders: mockSalesOrders,
      productionOrders: mockProductionOrders,
      deliveries: mockDeliveries,
      billings: mockBillings,
      nextOrderId: 1003,

      createOrder: (customerId, items, totalAmount) => {
        const orderId = get().nextOrderId

        const orderItems: SalesOrderItem[] = items.map((item, index) => ({
          id: orderId * 100 + index,
          sales_order_id: orderId,
          product_id: item.product_id,
          quantity: item.quantity,
          subtotal: item.subtotal,
        }))

        const newOrder: SalesOrder = {
          id: orderId,
          customer_id: customerId,
          total_amount: totalAmount,
          status: SalesOrderStatus.CREATED,
          created_at: new Date().toISOString(),
          items: orderItems,
        }

        // Auto-create production order
        const newProductionOrder: ProductionOrder = {
          id: get().productionOrders.length + 1,
          sales_order_id: orderId,
          status: ProductionOrderStatus.PLANNED,
          start_date: null,
          end_date: null,
        }

        // Auto-create delivery record
        const newDelivery: Delivery = {
          id: get().deliveries.length + 1,
          sales_order_id: orderId,
          delivery_date: null,
          status: DeliveryStatus.PENDING,
        }

        set((state) => ({
          orders: [...state.orders, newOrder],
          productionOrders: [...state.productionOrders, newProductionOrder],
          deliveries: [...state.deliveries, newDelivery],
          nextOrderId: orderId + 1,
        }))

        return newOrder
      },

      getOrderById: (orderId) => {
        return get().orders.find((order) => order.id === orderId)
      },

      getOrdersByCustomer: (customerId) => {
        return get().orders.filter((order) => order.customer_id === customerId)
      },

      getProductionOrderByOrderId: (orderId) => {
        return get().productionOrders.find((po) => po.sales_order_id === orderId)
      },

      getDeliveryByOrderId: (orderId) => {
        return get().deliveries.find((d) => d.sales_order_id === orderId)
      },

      getBillingByOrderId: (orderId) => {
        return get().billings.find((b) => b.sales_order_id === orderId)
      },
    }),
    {
      name: "mapua-orders-storage",
    },
  ),
)
