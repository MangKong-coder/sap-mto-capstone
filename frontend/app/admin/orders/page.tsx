"use client"

import { useState } from "react"
import { useOrdersStore } from "@/lib/orders-store"
import { useAdminStore } from "@/lib/admin-store"
import { mockCustomers } from "@/lib/mock-data"
import { SalesOrderStatus } from "@/lib/types"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Search, Play, CheckCircle } from "lucide-react"
import Link from "next/link"

export default function SalesOrdersPage() {
  const { orders } = useOrdersStore()
  const { startProduction, updateOrderStatus } = useAdminStore()
  const [searchTerm, setSearchTerm] = useState("")

  const filteredOrders = orders.filter(
    (order) =>
      order.id.toString().includes(searchTerm) ||
      mockCustomers
        .find((c) => c.id === order.customer_id)
        ?.name.toLowerCase()
        .includes(searchTerm.toLowerCase()),
  )

  const getCustomerName = (customerId: number) => {
    return mockCustomers.find((c) => c.id === customerId)?.name || "Unknown"
  }

  const getStatusColor = (status: SalesOrderStatus) => {
    switch (status) {
      case SalesOrderStatus.CREATED:
        return "bg-yellow-500/10 text-yellow-500"
      case SalesOrderStatus.IN_PRODUCTION:
        return "bg-blue-500/10 text-blue-500"
      case SalesOrderStatus.READY_FOR_DELIVERY:
        return "bg-purple-500/10 text-purple-500"
      case SalesOrderStatus.DELIVERED:
        return "bg-green-500/10 text-green-500"
      case SalesOrderStatus.BILLED:
        return "bg-emerald-500/10 text-emerald-500"
      case SalesOrderStatus.CANCELLED:
        return "bg-red-500/10 text-red-500"
      default:
        return "bg-zinc-500/10 text-zinc-500"
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-zinc-900">Sales Orders</h2>
          <p className="text-sm text-zinc-600">Manage customer orders and production workflow</p>
        </div>
      </div>

      <Card className="border-zinc-200 bg-white">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-zinc-900">All Orders</CardTitle>
            <div className="relative w-64">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-zinc-400" />
              <Input
                placeholder="Search orders..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="border-zinc-300 bg-white pl-9 text-zinc-900 placeholder:text-zinc-400"
              />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-zinc-200">
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Order ID</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Customer</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Date</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-600">Total</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Status</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-600">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredOrders.map((order) => (
                  <tr key={order.id} className="border-b border-zinc-100">
                    <td className="py-4">
                      <Link href={`/orders/${order.id}`} className="text-sm font-medium text-red-500 hover:underline">
                        #{order.id}
                      </Link>
                    </td>
                    <td className="py-4 text-sm text-zinc-700">{getCustomerName(order.customer_id)}</td>
                    <td className="py-4 text-sm text-zinc-600">{new Date(order.created_at).toLocaleDateString()}</td>
                    <td className="py-4 text-right text-sm font-medium text-zinc-900">₱{order.total_amount.toFixed(2)}</td>
                    <td className="py-4">
                      <Badge variant="secondary" className={getStatusColor(order.status)}>
                        {order.status.replace(/_/g, " ")}
                      </Badge>
                    </td>
                    <td className="py-4 text-right">
                      <div className="flex justify-end gap-2">
                        {order.status === SalesOrderStatus.CREATED && (
                          <Button
                            size="sm"
                            onClick={() => startProduction(order.id)}
                            className="bg-blue-500 text-white hover:bg-blue-600"
                          >
                            <Play className="mr-1 h-3 w-3" />
                            Start Production
                          </Button>
                        )}
                        {order.status === SalesOrderStatus.IN_PRODUCTION && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => updateOrderStatus(order.id, SalesOrderStatus.READY_FOR_DELIVERY)}
                            className="border-zinc-300 text-zinc-700 hover:bg-zinc-100"
                          >
                            <CheckCircle className="mr-1 h-3 w-3" />
                            Mark Ready
                          </Button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
