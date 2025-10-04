"use client"

import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { mockSalesOrders } from "@/lib/mock-data"
import { ArrowRight, FileText } from "lucide-react"
import Link from "next/link"
import type { SalesOrder } from "@/lib/types"

export function RecentOrdersTable() {
  const recentOrders = mockSalesOrders.slice(0, 5)

  const getStatusColor = (status: SalesOrder["status"]) => {
    switch (status) {
      case "Open":
        return "bg-blue-500/10 text-blue-500 border-blue-500/20"
      case "In Planning":
        return "bg-yellow-500/10 text-yellow-500 border-yellow-500/20"
      case "In Production":
        return "bg-purple-500/10 text-purple-500 border-purple-500/20"
      case "Delivered":
        return "bg-green-500/10 text-green-500 border-green-500/20"
      case "Billed":
        return "bg-gray-500/10 text-gray-500 border-gray-500/20"
      default:
        return "bg-gray-500/10 text-gray-500 border-gray-500/20"
    }
  }

  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-foreground">Recent Sales Orders</h3>
          <p className="text-sm text-muted-foreground">Latest orders in the MTO flow</p>
        </div>
        <Link href="/sales-orders">
          <Button variant="outline" size="sm" className="gap-2 bg-transparent">
            View All
            <ArrowRight className="w-4 h-4" />
          </Button>
        </Link>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="border-b border-border">
            <tr>
              <th className="text-left p-3 text-sm font-semibold text-foreground">Order Number</th>
              <th className="text-left p-3 text-sm font-semibold text-foreground">Customer</th>
              <th className="text-left p-3 text-sm font-semibold text-foreground">Material</th>
              <th className="text-left p-3 text-sm font-semibold text-foreground">Quantity</th>
              <th className="text-left p-3 text-sm font-semibold text-foreground">Delivery Date</th>
              <th className="text-left p-3 text-sm font-semibold text-foreground">Status</th>
            </tr>
          </thead>
          <tbody>
            {recentOrders.map((order) => (
              <tr key={order.id} className="border-b border-border hover:bg-muted/30 transition-colors">
                <td className="p-3">
                  <div className="flex items-center gap-2">
                    <FileText className="w-4 h-4 text-primary" />
                    <span className="font-medium text-foreground">{order.orderNumber}</span>
                  </div>
                </td>
                <td className="p-3 text-foreground">{order.customer}</td>
                <td className="p-3 text-foreground text-sm">{order.material}</td>
                <td className="p-3 text-foreground">{order.quantity}</td>
                <td className="p-3 text-foreground">{new Date(order.deliveryDate).toLocaleDateString()}</td>
                <td className="p-3">
                  <Badge variant="outline" className={getStatusColor(order.status)}>
                    {order.status}
                  </Badge>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}
