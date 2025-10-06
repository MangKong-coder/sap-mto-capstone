"use client"

import { useOrdersStore } from "@/lib/orders-store"
import { useAdminStore } from "@/lib/admin-store"
import { ProductionOrderStatus } from "@/lib/types"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Play, CheckCircle, XCircle } from "lucide-react"
import Link from "next/link"

export default function ProductionOrdersPage() {
  const { orders, productionOrders } = useOrdersStore()
  const { updateProductionStatus } = useAdminStore()

  const getOrderDetails = (salesOrderId: number) => {
    return orders.find((o) => o.id === salesOrderId)
  }

  const getStatusColor = (status: ProductionOrderStatus) => {
    switch (status) {
      case ProductionOrderStatus.PLANNED:
        return "bg-yellow-500/10 text-yellow-500"
      case ProductionOrderStatus.IN_PROGRESS:
        return "bg-blue-500/10 text-blue-500"
      case ProductionOrderStatus.COMPLETED:
        return "bg-green-500/10 text-green-500"
      case ProductionOrderStatus.CANCELLED:
        return "bg-red-500/10 text-red-500"
      default:
        return "bg-zinc-500/10 text-zinc-500"
  }
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-zinc-900">Production Orders</h2>
        <p className="text-sm text-zinc-600">Track and manage production workflow</p>
      </div>

      <Card className="border-zinc-200 bg-white">
        <CardHeader>
          <CardTitle className="text-zinc-900">All Production Orders</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-zinc-200">
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Production ID</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Sales Order</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Items</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Start Date</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">End Date</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Status</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-600">Actions</th>
                </tr>
              </thead>
              <tbody>
                {productionOrders.map((po) => {
                  const order = getOrderDetails(po.sales_order_id)
                  return (
                    <tr key={po.id} className="border-b border-zinc-100">
                      <td className="py-4 text-sm font-medium text-zinc-900">PO-{po.id}</td>
                      <td className="py-4">
                        <Link href={`/orders/${po.sales_order_id}`} className="text-sm text-red-500 hover:underline">
                          #{po.sales_order_id}
                        </Link>
                      </td>
                      <td className="py-4 text-sm text-zinc-700">{order?.items.length || 0} items</td>
                      <td className="py-4 text-sm text-zinc-600">
                        {po.start_date ? new Date(po.start_date).toLocaleDateString() : "-"}
                      </td>
                      <td className="py-4 text-sm text-zinc-600">
                        {po.end_date ? new Date(po.end_date).toLocaleDateString() : "-"}
                      </td>
                      <td className="py-4">
                        <Badge variant="secondary" className={getStatusColor(po.status)}>
                          {po.status.replace(/_/g, " ")}
                        </Badge>
                      </td>
                      <td className="py-4 text-right">
                        <div className="flex justify-end gap-2">
                          {po.status === ProductionOrderStatus.PLANNED && (
                            <Button
                              size="sm"
                              onClick={() => updateProductionStatus(po.id, ProductionOrderStatus.IN_PROGRESS)}
                              className="bg-blue-500 text-white hover:bg-blue-600"
                            >
                              <Play className="mr-1 h-3 w-3" />
                              Start
                            </Button>
                          )}
                          {po.status === ProductionOrderStatus.IN_PROGRESS && (
                            <Button
                              size="sm"
                              onClick={() => updateProductionStatus(po.id, ProductionOrderStatus.COMPLETED)}
                              className="bg-green-500 text-white hover:bg-green-600"
                            >
                              <CheckCircle className="mr-1 h-3 w-3" />
                              Complete
                            </Button>
                          )}
                          {(po.status === ProductionOrderStatus.PLANNED || po.status === ProductionOrderStatus.IN_PROGRESS) && (
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => updateProductionStatus(po.id, ProductionOrderStatus.CANCELLED)}
                              className="border-zinc-300 text-zinc-700 hover:bg-zinc-100"
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
