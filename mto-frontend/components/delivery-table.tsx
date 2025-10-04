"use client"

import { useState } from "react"
import { mockDeliveries } from "@/lib/mock-data"
import type { Delivery } from "@/lib/types"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Eye, Truck } from "lucide-react"

interface DeliveryTableProps {
  searchQuery: string
}

export function DeliveryTable({ searchQuery }: DeliveryTableProps) {
  const [deliveries] = useState<Delivery[]>(mockDeliveries)

  const filteredDeliveries = deliveries.filter(
    (delivery) =>
      delivery.deliveryNumber.toLowerCase().includes(searchQuery.toLowerCase()) ||
      delivery.customer.toLowerCase().includes(searchQuery.toLowerCase()) ||
      delivery.salesOrderNumber.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  const getStatusColor = (status: Delivery["status"]) => {
    switch (status) {
      case "Created":
        return "bg-blue-500/10 text-blue-500 border-blue-500/20"
      case "Picked":
        return "bg-yellow-500/10 text-yellow-500 border-yellow-500/20"
      case "Packed":
        return "bg-orange-500/10 text-orange-500 border-orange-500/20"
      case "Shipped":
        return "bg-purple-500/10 text-purple-500 border-purple-500/20"
      case "Delivered":
        return "bg-green-500/10 text-green-500 border-green-500/20"
      default:
        return "bg-gray-500/10 text-gray-500 border-gray-500/20"
    }
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead className="bg-muted/50 border-b border-border">
          <tr>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Delivery Number</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Sales Order</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Customer</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Quantity</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Delivery Date</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Tracking Number</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Status</th>
            <th className="text-left p-4 text-sm font-semibold text-foreground">Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredDeliveries.map((delivery) => (
            <tr key={delivery.id} className="border-b border-border hover:bg-muted/30 transition-colors">
              <td className="p-4">
                <div className="flex items-center gap-2">
                  <Truck className="w-4 h-4 text-green-500" />
                  <span className="font-medium text-foreground">{delivery.deliveryNumber}</span>
                </div>
              </td>
              <td className="p-4">
                <span className="text-primary font-medium">{delivery.salesOrderNumber}</span>
              </td>
              <td className="p-4 text-foreground">{delivery.customer}</td>
              <td className="p-4 text-foreground">{delivery.quantity}</td>
              <td className="p-4 text-foreground">{new Date(delivery.deliveryDate).toLocaleDateString()}</td>
              <td className="p-4">
                {delivery.trackingNumber ? (
                  <span className="text-sm font-mono text-foreground">{delivery.trackingNumber}</span>
                ) : (
                  <span className="text-sm text-muted-foreground">-</span>
                )}
              </td>
              <td className="p-4">
                <Badge variant="outline" className={getStatusColor(delivery.status)}>
                  {delivery.status}
                </Badge>
              </td>
              <td className="p-4">
                <Button variant="ghost" size="sm" className="gap-2">
                  <Eye className="w-4 h-4" />
                  View
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
