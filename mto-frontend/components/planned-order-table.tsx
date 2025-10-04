"use client"

import { useState } from "react"
import { mockPlannedOrders } from "@/lib/mock-data"
import type { PlannedOrder } from "@/lib/types"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ArrowRight, FileText } from "lucide-react"
import { ConvertToProductionDialog } from "./convert-to-production-dialog"

interface PlannedOrderTableProps {
  searchQuery: string
}

export function PlannedOrderTable({ searchQuery }: PlannedOrderTableProps) {
  const [orders] = useState<PlannedOrder[]>(mockPlannedOrders)
  const [selectedOrder, setSelectedOrder] = useState<PlannedOrder | null>(null)
  const [convertDialogOpen, setConvertDialogOpen] = useState(false)

  const filteredOrders = orders.filter(
    (order) =>
      order.plannedOrderNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
      order.salesOrderNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
      order.material.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  const getStatusColor = (status: PlannedOrder["status"]) => {
    switch (status) {
      case "Created":
        return "bg-yellow-500/10 text-yellow-500 border-yellow-500/20"
      case "Converted":
        return "bg-green-500/10 text-green-500 border-green-500/20"
      case "Cancelled":
        return "bg-red-500/10 text-red-500 border-red-500/20"
      default:
        return "bg-gray-500/10 text-gray-500 border-gray-500/20"
    }
  }

  const handleConvert = (order: PlannedOrder) => {
    setSelectedOrder(order)
    setConvertDialogOpen(true)
  }

  return (
    <>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-muted/50 border-b border-border">
            <tr>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Planned Order</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Sales Order</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Material</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Quantity</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Start Date</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">End Date</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Plant</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Status</th>
              <th className="text-left p-4 text-sm font-semibold text-foreground">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredOrders.map((order) => (
              <tr key={order.id} className="border-b border-border hover:bg-muted/30 transition-colors">
                <td className="p-4">
                  <div className="flex items-center gap-2">
                    <FileText className="w-4 h-4 text-yellow-500" />
                    <span className="font-medium text-foreground">{order.plannedOrderNumber}</span>
                  </div>
                </td>
                <td className="p-4">
                  <span className="text-primary font-medium">{order.salesOrderNumber}</span>
                </td>
                <td className="p-4 text-foreground">{order.material}</td>
                <td className="p-4 text-foreground">{order.quantity}</td>
                <td className="p-4 text-foreground">{new Date(order.startDate).toLocaleDateString()}</td>
                <td className="p-4 text-foreground">{new Date(order.endDate).toLocaleDateString()}</td>
                <td className="p-4 text-foreground">{order.plant}</td>
                <td className="p-4">
                  <Badge variant="outline" className={getStatusColor(order.status)}>
                    {order.status}
                  </Badge>
                </td>
                <td className="p-4">
                  {order.status === "Created" ? (
                    <Button variant="default" size="sm" onClick={() => handleConvert(order)} className="gap-2">
                      <ArrowRight className="w-4 h-4" />
                      Convert to Production
                    </Button>
                  ) : (
                    <span className="text-sm text-muted-foreground">Converted</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedOrder && (
        <ConvertToProductionDialog order={selectedOrder} open={convertDialogOpen} onOpenChange={setConvertDialogOpen} />
      )}
    </>
  )
}
