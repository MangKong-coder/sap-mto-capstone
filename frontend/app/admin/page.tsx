"use client"

import { useOrdersStore } from "@/lib/orders-store"
import { SalesOrderStatus } from "@/lib/types"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ShoppingCart, Factory, Truck, FileText } from "lucide-react"
import { Badge } from "@/components/ui/badge"

export default function AdminDashboard() {
  const { orders, productionOrders, deliveries, billings } = useOrdersStore()

  // Calculate KPIs
  const totalOrders = orders.length
  const ordersInProduction = orders.filter((o) => o.status === SalesOrderStatus.IN_PRODUCTION).length
  const ordersDelivered = orders.filter((o) => o.status === SalesOrderStatus.DELIVERED).length
  const ordersBilled = orders.filter((o) => o.status === SalesOrderStatus.BILLED).length

  // Orders by status
  const ordersByStatus = {
    created: orders.filter((o) => o.status === SalesOrderStatus.CREATED).length,
    in_production: orders.filter((o) => o.status === SalesOrderStatus.IN_PRODUCTION).length,
    ready_for_delivery: orders.filter((o) => o.status === SalesOrderStatus.READY_FOR_DELIVERY).length,
    delivered: orders.filter((o) => o.status === SalesOrderStatus.DELIVERED).length,
    billed: orders.filter((o) => o.status === SalesOrderStatus.BILLED).length,
  }

  // Top products by order count
  const productCounts = new Map<number, { name: string; count: number }>()
  orders.forEach((order) => {
    order.items.forEach((item) => {
      const current = productCounts.get(item.product_id) || { name: `Product ${item.product_id}`, count: 0 }
      productCounts.set(item.product_id, { ...current, count: current.count + item.quantity })
    })
  })
  const topProducts = Array.from(productCounts.entries())
    .map(([id, data]) => ({ id, ...data }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5)

  // Recent orders
  const recentOrders = [...orders]
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5)

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">Dashboard Overview</h2>
        <p className="text-sm text-zinc-400">Operational KPIs and summaries</p>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="border-zinc-800 bg-zinc-900">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-zinc-400">Total Sales Orders</CardTitle>
            <ShoppingCart className="h-4 w-4 text-zinc-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{totalOrders}</div>
            <p className="text-xs text-zinc-500">All time orders</p>
          </CardContent>
        </Card>

        <Card className="border-zinc-800 bg-zinc-900">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-zinc-400">In Production</CardTitle>
            <Factory className="h-4 w-4 text-zinc-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{ordersInProduction}</div>
            <p className="text-xs text-zinc-500">Currently being produced</p>
          </CardContent>
        </Card>

        <Card className="border-zinc-800 bg-zinc-900">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-zinc-400">Delivered</CardTitle>
            <Truck className="h-4 w-4 text-zinc-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{ordersDelivered}</div>
            <p className="text-xs text-zinc-500">Successfully delivered</p>
          </CardContent>
        </Card>

        <Card className="border-zinc-800 bg-zinc-900">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-zinc-400">Billed</CardTitle>
            <FileText className="h-4 w-4 text-zinc-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{ordersBilled}</div>
            <p className="text-xs text-zinc-500">Invoices generated</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Orders by Status */}
        <Card className="border-zinc-800 bg-zinc-900">
          <CardHeader>
            <CardTitle className="text-white">Orders by Status</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {Object.entries(ordersByStatus).map(([status, count]) => (
              <div key={status} className="flex items-center justify-between">
                <span className="text-sm text-zinc-400 capitalize">{status.replace(/_/g, " ")}</span>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-32 overflow-hidden rounded-full bg-zinc-800">
                    <div className="h-full bg-red-500" style={{ width: `${(count / totalOrders) * 100}%` }} />
                  </div>
                  <span className="w-8 text-right text-sm font-medium text-white">{count}</span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Top Products */}
        <Card className="border-zinc-800 bg-zinc-900">
          <CardHeader>
            <CardTitle className="text-white">Top 5 Products</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {topProducts.map((product, index) => (
                <div key={product.id} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-zinc-800 text-sm font-medium text-zinc-400">
                      {index + 1}
                    </div>
                    <span className="text-sm text-zinc-300">Product #{product.id}</span>
                  </div>
                  <Badge variant="secondary" className="bg-zinc-800 text-white">
                    {product.count} units
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Orders Table */}
      <Card className="border-zinc-800 bg-zinc-900">
        <CardHeader>
          <CardTitle className="text-white">Recent Orders</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-zinc-800">
                  <th className="pb-3 text-left text-sm font-medium text-zinc-400">Order ID</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-400">Customer</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-400">Date</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-400">Total</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-400">Status</th>
                </tr>
              </thead>
              <tbody>
                {recentOrders.map((order) => (
                  <tr key={order.id} className="border-b border-zinc-800/50">
                    <td className="py-3 text-sm text-white">#{order.id}</td>
                    <td className="py-3 text-sm text-zinc-300">Customer {order.customer_id}</td>
                    <td className="py-3 text-sm text-zinc-400">{new Date(order.created_at).toLocaleDateString()}</td>
                    <td className="py-3 text-right text-sm text-white">₱{order.total_amount.toFixed(2)}</td>
                    <td className="py-3">
                      <Badge
                        variant="secondary"
                        className={
                          order.status === SalesOrderStatus.BILLED
                            ? "bg-green-500/10 text-green-500"
                            : order.status === SalesOrderStatus.DELIVERED
                              ? "bg-blue-500/10 text-blue-500"
                              : "bg-yellow-500/10 text-yellow-500"
                        }
                      >
                        {order.status}
                      </Badge>
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
