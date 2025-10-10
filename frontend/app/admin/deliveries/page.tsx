import { getOrders, getDeliveries, type OrderSummary, type Delivery } from "@/lib/dal"
import { updateDeliveryStatusAction } from "@/app/admin/actions"
import { DeliveryStatus, SalesOrderStatus } from "@/lib/types"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { CheckCircle, XCircle } from "lucide-react"
import Link from "next/link"

export default async function DeliveriesPage() {
  let orders: OrderSummary[] = []
  let deliveries: Delivery[] = []
  let error: string | null = null

  try {
    [orders, deliveries] = await Promise.all([
      getOrders(),
      getDeliveries()
    ])
  } catch (err) {
    error = err instanceof Error ? err.message : "Failed to load deliveries data"
  }

  const getOrderDetails = (salesOrderId: number): OrderSummary | undefined => {
    return orders.find((o) => o.id === salesOrderId)
  }

  const getStatusColor = (status: string) => {
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
        <h2 className="text-2xl font-bold text-zinc-900">Deliveries</h2>
        <p className="text-sm text-zinc-600">Track and manage order deliveries</p>
        {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
      </div>

      <Card className="border-zinc-200 bg-white">
        <CardHeader>
          <CardTitle className="text-zinc-900">All Deliveries</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-zinc-200">
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Delivery ID</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Sales Order</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Order Status</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Total Amount</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Delivery Date</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Status</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-600">Actions</th>
                </tr>
              </thead>
              <tbody>
                {deliveries.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="py-6 text-center text-sm text-zinc-500">
                      No deliveries available.
                    </td>
                  </tr>
                ) : (
                  deliveries
                    .sort((a, b) => {
                      // Deliveries that need action come first
                      const orderA = getOrderDetails(a.sales_order_id)
                      const orderB = getOrderDetails(b.sales_order_id)
                      
                      const aNeedsAction = a.status === DeliveryStatus.PENDING && 
                                          orderA?.status === SalesOrderStatus.READY_FOR_DELIVERY
                      const bNeedsAction = b.status === DeliveryStatus.PENDING && 
                                          orderB?.status === SalesOrderStatus.READY_FOR_DELIVERY
                      
                      if (aNeedsAction && !bNeedsAction) return -1
                      if (!aNeedsAction && bNeedsAction) return 1
                      
                      // Within same category, sort by ID ascending
                      return a.id - b.id
                    })
                    .map((delivery: Delivery) => {
                    const order = getOrderDetails(delivery.sales_order_id)
                    return (
                      <tr key={delivery.id} className="border-b border-zinc-100">
                        <td className="py-4 text-sm font-medium text-zinc-900">DEL-{delivery.id}</td>
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
                        <td className="py-4 text-sm text-zinc-900">
                          ₱{order?.total_amount.toFixed(2) || "0.00"}
                        </td>
                        <td className="py-4 text-sm text-zinc-600">
                          {delivery.delivery_date ? new Date(delivery.delivery_date).toLocaleDateString() : "-"}
                        </td>
                        <td className="py-4">
                          <Badge variant="secondary" className={getStatusColor(delivery.status)}>
                            {delivery.status}
                          </Badge>
                        </td>
                        <td className="py-4">
                          <div className="flex justify-end gap-2">
                            {delivery.status === DeliveryStatus.PENDING &&
                              order?.status === SalesOrderStatus.READY_FOR_DELIVERY && (
                                <form
                                  action={async (_formData: FormData) => {
                                    "use server"
                                    await updateDeliveryStatusAction(delivery.id, DeliveryStatus.DELIVERED)
                                  }}
                                >
                                  <Button
                                    size="sm"
                                    type="submit"
                                    className="bg-green-500 text-white hover:bg-green-600"
                                  >
                                    <CheckCircle className="mr-1 h-3 w-3" />
                                    Mark Delivered
                                  </Button>
                                </form>
                              )}
                            {delivery.status === DeliveryStatus.PENDING && (
                              <form
                                action={async (_formData: FormData) => {
                                  "use server"
                                  await updateDeliveryStatusAction(delivery.id, DeliveryStatus.CANCELLED)
                                }}
                              >
                                <Button
                                  size="sm"
                                  type="submit"
                                  variant="outline"
                                  className="border-zinc-300 text-zinc-700 hover:bg-zinc-100"
                                >
                                  <XCircle className="mr-1 h-3 w-3" />
                                  Cancel
                                </Button>
                              </form>
                            )}
                          </div>
                        </td>
                      </tr>
                    )
                  })
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
