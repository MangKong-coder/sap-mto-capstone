"use client"

import { useState } from "react"
import { mockProductionOrders } from "@/lib/mock-data"
import type { ProductionOrder } from "@/lib/types"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Eye, FileText, Play } from "lucide-react"
import { ProductionOrderDetailsDialog } from "./production-order-details-dialog"
import { Progress } from "@/components/ui/progress"

interface ProductionOrderTableProps {
  searchQuery: string
}

export function ProductionOrderTable({ searchQuery }: ProductionOrderTableProps) {
  const [orders] = useState<ProductionOrder[]>(mockProductionOrders)
  const [selectedOrder, setSelectedOrder] = useState<ProductionOrder | null>(null)
  const [detailsOpen, setDetailsOpen] = useState(false)

  const filteredOrders = orders.filter(
    (order) =>
      order.productionOrderNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
      order.salesOrderNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
      order.material.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  const getStatusColor = (status: ProductionOrder["status"]) => {
    switch (status) {
      case "Created":
        return "bg-blue-500/10 text-blue-500 border-blue-500/20"
      case "Released":
        return "bg-cyan-500/10 text-cyan-500 border-cyan-500/20"
      case "In Progress":
        return "bg-purple-500/10 text-purple-500 border-purple-500/20"
      case "Confirmed":
        return "bg-yellow-500/10 text-yellow-500 border-yellow-500/20"
      case "Completed":
        return "bg-green-500/10 text-green-500 border-green-500/20"
      default:
        return "bg-gray-500/10 text-gray-500 border-gray-500/20"
    }
  }

  const handleViewDetails = (order: ProductionOrder) => {
    setSelectedOrder(order)
    setDetailsOpen(true)
  }

  return (
    <>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-muted/50 border-b border-border">
            <tr>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Production Order</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Sales Order</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Material</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Quantity</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Progress</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Start Date</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">End Date</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Status</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredOrders.map((order) => {
              const progress = (order.confirmedQuantity / order.quantity) * 100
              return (
                <tr key={order.id} className="border-b border-border hover:bg-muted/30 transition-colors">
                  <td className="p-4">
                    <div className="flex items-center gap-2">
                      <FileText className="w-4 h-4 text-purple-500" />
                      <span className="font-medium text-foreground">{order.productionOrderNumber}</span>
                    </div>
                  </td>
                  <td className="p-4">
                    <span className="text-primary font-medium">{order.salesOrderNumber}</span>
                  </td>
                  <td className="p-4 text-foreground">{order.material}</td>
                  <td className="p-4 text-foreground">
                    {order.confirmedQuantity} / {order.quantity}
                  </td>
                  <td className="p-4">
                    <div className="flex items-center gap-2">
                      <Progress value={progress} className="w-24 h-2" />
                      <span className="text-sm text-muted-foreground">{Math.round(progress)}%</span>
                    </div>
                  </td>
                  <td className="p-4 text-foreground">{new Date(order.startDate).toLocaleDateString()}</td>
                  <td className="p-4 text-foreground">{new Date(order.endDate).toLocaleDateString()}</td>
                  <td className="p-4">
                    <Badge variant="outline" className={getStatusColor(order.status)}>
                      {order.status}
                    </Badge>
                  </td>
                  <td className="p-4">
                    <div className="flex items-center gap-2">
                      <Button variant="ghost" size="sm" onClick={() => handleViewDetails(order)} className="gap-2">
                        <Eye className="w-4 h-4" />
                        View
                      </Button>
                      {order.status === "Released" && (
                        <Button variant="default" size="sm" className="gap-2">
                          <Play className="w-4 h-4" />
                          Start
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

      {selectedOrder && (
        <ProductionOrderDetailsDialog order={selectedOrder} open={detailsOpen} onOpenChange={setDetailsOpen} />
      )}
    </>
  )
}
