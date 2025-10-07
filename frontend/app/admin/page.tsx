import { getDashboardSummary } from "@/lib/dal"
import type { DashboardSummaryResponse, RecentOrderResponse, TopProductResponse } from "@/lib/dal"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ShoppingCart, Factory, Truck, FileText } from "lucide-react"
import { Badge } from "@/components/ui/badge"

export default async function AdminDashboard() {
  let summary: DashboardSummaryResponse | null = null
  let error: string | null = null

  try {
    summary = await getDashboardSummary({ cache: "no-store" })
  } catch (err) {
    error = err instanceof Error ? err.message : "Failed to load dashboard data"
  }

  const totalOrders = summary?.total_orders ?? 0
  const ordersInProduction = summary?.in_production ?? 0
  const ordersDelivered = summary?.ready_for_delivery ?? 0
  const ordersBilled = summary?.billed ?? 0

  const ordersByStatus: Record<string, number> = summary
    ? {
        in_production: summary.in_production,
        ready_for_delivery: summary.ready_for_delivery,
        billed: summary.billed,
      }
    : {}

  const topProducts: TopProductResponse[] = summary?.top_products ?? []
  const recentOrders: RecentOrderResponse[] = summary?.recent_orders ?? []

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-zinc-900">Dashboard Overview</h2>
        <p className="text-sm text-zinc-600">Operational KPIs and summaries</p>
        {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="border-zinc-200 bg-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-zinc-600">Total Sales Orders</CardTitle>
            <ShoppingCart className="h-4 w-4 text-zinc-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-zinc-900">{totalOrders}</div>
            <p className="text-xs text-zinc-500">All time orders</p>
          </CardContent>
        </Card>

        <Card className="border-zinc-200 bg-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-zinc-600">In Production</CardTitle>
            <Factory className="h-4 w-4 text-zinc-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-zinc-900">{ordersInProduction}</div>
            <p className="text-xs text-zinc-500">Currently being produced</p>
          </CardContent>
        </Card>

        <Card className="border-zinc-200 bg-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-zinc-600">Delivered</CardTitle>
            <Truck className="h-4 w-4 text-zinc-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-zinc-900">{ordersDelivered}</div>
            <p className="text-xs text-zinc-500">Successfully delivered</p>
          </CardContent>
        </Card>

        <Card className="border-zinc-200 bg-white">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-zinc-600">Billed</CardTitle>
            <FileText className="h-4 w-4 text-zinc-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-zinc-900">{ordersBilled}</div>
            <p className="text-xs text-zinc-500">Invoices generated</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Orders by Status */}
        <Card className="border-zinc-200 bg-white">
          <CardHeader>
            <CardTitle className="text-zinc-900">Orders by Status</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {Object.entries(ordersByStatus).length === 0 && (
              <p className="text-sm text-zinc-500">No data available.</p>
            )}
            {Object.entries(ordersByStatus).map(([status, count]) => (
              <div key={status} className="flex items-center justify-between">
                <span className="text-sm text-zinc-600 capitalize">{status.replace(/_/g, " ")}</span>
                <div className="flex items-center gap-2">
                  <div className="h-2 w-32 overflow-hidden rounded-full bg-zinc-200">
                    <div
                      className="h-full bg-red-500"
                      style={{ width: totalOrders > 0 ? `${(count / totalOrders) * 100}%` : "0%" }}
                    />
                  </div>
                  <span className="w-8 text-right text-sm font-medium text-zinc-900">{count}</span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Top Products */}
        <Card className="border-zinc-200 bg-white">
          <CardHeader>
            <CardTitle className="text-zinc-900">Top 5 Products</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {topProducts.length === 0 && <p className="text-sm text-zinc-500">No data available.</p>}
              {topProducts.map((product, index) => (
                <div key={product.product_id} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-zinc-100 text-sm font-medium text-zinc-600">
                      {index + 1}
                    </div>
                    <span className="text-sm text-zinc-700">{product.name ?? `Product #${product.product_id}`}</span>
                  </div>
                  <Badge variant="secondary" className="bg-zinc-100 text-zinc-700">
                    {product.orders} units
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent Orders Table */}
      <Card className="border-zinc-200 bg-white">
        <CardHeader>
          <CardTitle className="text-zinc-900">Recent Orders</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-zinc-200">
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Order ID</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Customer</th>
                  <th className="pb-3 text-right text-sm font-medium text-zinc-600">Total</th>
                  <th className="pb-3 text-left text-sm font-medium text-zinc-600">Status</th>
                </tr>
              </thead>
              <tbody>
                {recentOrders.length === 0 && (
                  <tr>
                    <td colSpan={5} className="py-6 text-center text-sm text-zinc-500">
                      No recent orders available.
                    </td>
                  </tr>
                )}
                {recentOrders.map((order) => (
                  <tr key={order.id} className="border-b border-zinc-100">
                    <td className="py-3 text-sm text-zinc-900">#{order.id}</td>
                    <td className="py-3 text-sm text-zinc-700">{order.customer_name}</td>
                    <td className="py-3 text-sm text-zinc-600">{order.created_at.toLocaleDateString()}</td>
                    <td className="py-3 text-right text-sm text-zinc-900">₱{order.total_amount.toFixed(2)}</td>
                    <td className="py-3">
                      <Badge
                        variant="secondary"
                        className={
                          order.status === "billed"
                            ? "bg-green-100 text-green-700"
                            : order.status === "delivered"
                              ? "bg-blue-100 text-blue-700"
                              : "bg-yellow-100 text-yellow-700"
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
