"use client"

import { useOrdersStore } from "@/lib/orders-store"
import { useAdminStore } from "@/lib/admin-store"
import { DeliveryStatus, SalesOrderStatus } from "@/lib/types"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { CheckCircle, XCircle } from "lucide-react"
import Link from "next/link"

export default function DeliveriesPage() {
  const { orders, deliveries } = useOrdersStore()
  const { updateDeliveryStatus } = useAdminStore()

  const getOrderDetails = (salesOrderId: number) => {
    return orders.find((o) => o.id === salesOrderId)
  }

  const getStatusColor = (status: DeliveryStatus) => {
    switch (status) {
      case DeliveryStatus.PENDING:
        return "bg-yellow-500/10 text-yellow-500"
      case DeliveryStatus.DELIVERED:
        return "bg-green-500/10 text-green-500"
      case DeliveryStatus.CANCELLED:
        return "bg-red-500/10 text-red-500"
      default:
        return "bg-zinc-500/10 text-zinc-500"
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">Deliveries</h2>
        <p className="text-sm text-zinc-400">Track and manage order deliveries</p>
      </div>

      <Card className="border-zinc-800 bg-zinc-900">
        <CardHeader>
          <CardTitle className="text-white">All Deliveries</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-zinc-800">
                  <th className="pb-3 text-left text-sm font-medium text-zinc-400">Delivery ID</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-400">Sales Order</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-400">Order Status</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-400">Total Amount</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-400">Delivery Date</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-400">Status</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-400">Actions</th>
                </tr>
              </thead>
              <tbody>
                {deliveries.map((delivery) => {
                  const order = getOrderDetails(delivery.sales_order_id)
                  return (
                    <tr key={delivery.id} className="border-b border-zinc-800/50">
                      <td className="py-4 text-sm font-medium text-white">DEL-{delivery.id}</td>
                      <td className="py-4">
                        <Link
                          href={`/orders/${delivery.sales_order_id}`}
                          className="text-sm text-red-500 hover:underline"
                        >
                          #{delivery.sales_order_id}
                        </Link>
                      </td>
                      <td className="py-4">
                        <Badge
                          variant="secondary"
                          className={
                            order?.status === SalesOrderStatus.READY_FOR_DELIVERY
                              ? "bg-purple-500/10 text-purple-500"
                              : "bg-zinc-500/10 text-zinc-500"
                          }
                        >
                          {order?.status.replace(/_/g, " ") || "Unknown"}
                        </Badge>
                      </td>
                      <td className="py-4 text-right text-sm text-white">
                        ₱{order?.total_amount.toFixed(2) || "0.00"}
                      </td>
                      <td className="py-4 text-sm text-zinc-400">
                        {delivery.delivery_date ? new Date(delivery.delivery_date).toLocaleDateString() : "-"}
                      </td>
                      <td className="py-4">
                        <Badge variant="secondary" className={getStatusColor(delivery.status)}>
                          {delivery.status}
                        </Badge>
                      </td>
                      <td className="py-4 text-right">
                        <div className="flex justify-end gap-2">
                          {delivery.status === DeliveryStatus.PENDING &&
                            order?.status === SalesOrderStatus.READY_FOR_DELIVERY && (
                              <Button
                                size="sm"
                                onClick={() => updateDeliveryStatus(delivery.id, DeliveryStatus.DELIVERED)}
                                className="bg-green-500 text-white hover:bg-green-600"
                              >
                                <CheckCircle className="mr-1 h-3 w-3" />
                                Mark Delivered
                              </Button>
                            )}
                          {delivery.status === DeliveryStatus.PENDING && (
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => updateDeliveryStatus(delivery.id, DeliveryStatus.CANCELLED)}
                              className="border-zinc-700 text-zinc-300 hover:bg-zinc-800"
                            >
                              <XCircle className="mr-1 h-3 w-3" />
                              Cancel
                            </Button>
                          )}
                        </div>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
