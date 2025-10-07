import Link from "next/link"
import { Package, ShoppingBag } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { getOrders } from "@/lib/dal/orders"
import { SalesOrderStatus } from "@/lib/types"

// For now, we'll use a placeholder customer ID until auth is implemented
// In a real app, this would come from authentication context or session
const PLACEHOLDER_CUSTOMER_ID = 1

export default async function OrdersPage() {
  // Fetch orders for the current customer from the backend
  const orders = await getOrders({}, { customer_id: PLACEHOLDER_CUSTOMER_ID })

  const getStatusColor = (status: SalesOrderStatus) => {
    switch (status) {
      case SalesOrderStatus.CREATED:
        return "bg-gray-500"
      case SalesOrderStatus.IN_PRODUCTION:
        return "bg-orange-500"
      case SalesOrderStatus.READY_FOR_DELIVERY:
        return "bg-blue-500"
      case SalesOrderStatus.DELIVERED:
        return "bg-green-500"
      case SalesOrderStatus.BILLED:
        return "bg-green-600"
      case SalesOrderStatus.CANCELLED:
        return "bg-red-500"
      default:
        return "bg-gray-500"
    }
  }

  const getStatusLabel = (status: SalesOrderStatus) => {
    return status.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())
  }

  if (orders.length === 0) {
    return (
      <main className="px-12 py-16">
        <div className="mx-auto flex max-w-md flex-col items-center gap-4 text-center">
          <div className="flex h-20 w-20 items-center justify-center rounded-full bg-muted">
            <Package className="h-10 w-10 text-muted-foreground" />
          </div>
          <h1 className="font-bold text-2xl">No orders yet</h1>
          <p className="text-muted-foreground text-pretty">
            You haven't placed any orders yet. Start shopping to see your orders here.
          </p>
          <Button asChild className="mt-4">
            <Link href="/">
              <ShoppingBag className="mr-2 h-4 w-4" />
              Start Shopping
            </Link>
          </Button>
        </div>
      </main>
    )
  }

  return (
    <main className="px-12 py-8">
      <div className="mb-6">
        <h1 className="font-bold text-3xl">My Orders</h1>
        <p className="text-muted-foreground">Track and manage your Mapúa merchandise orders</p>
      </div>

      <div className="space-y-4">
        {orders
          .sort((a, b) => new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime())
          .map((order) => (
            <Card key={order.id} className="transition-shadow hover:shadow-md">
              <CardContent className="p-6">
                <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <h3 className="font-semibold text-lg">Order #{order.id}</h3>
                      <Badge className={getStatusColor(order.status)}>{getStatusLabel(order.status)}</Badge>
                    </div>
                    <p className="mt-1 text-muted-foreground text-sm">
                      Placed on{" "}
                      {order.created_at
                        ? new Date(order.created_at).toLocaleDateString("en-US", {
                            year: "numeric",
                            month: "long",
                            day: "numeric",
                          })
                        : "Date not available"
                      }
                    </p>
                    <div className="mt-3 space-y-1">
                      {/* For now, show placeholder item info since we don't have item details in OrderSummary */}
                      <p className="text-sm text-muted-foreground">
                        Order details available in full view
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 sm:flex-col sm:items-end">
                    <div className="text-right">
                      <p className="text-muted-foreground text-sm">Total</p>
                      <p className="font-bold text-xl text-primary">₱{order.total_amount.toFixed(2)}</p>
                    </div>
                    <Button asChild>
                      <Link href={`/orders/${order.id}`}>View Details</Link>
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
      </div>
    </main>
  )
}
