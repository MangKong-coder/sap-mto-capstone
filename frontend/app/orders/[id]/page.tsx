import { notFound } from "next/navigation"
import Link from "next/link"
import { ArrowLeft, Package, Truck, FileText, Factory } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { getOrderDetail, getOrders } from "@/lib/dal/orders"
import { SalesOrderStatus } from "@/lib/types"

interface PageProps {
  params: Promise<{ id: string }>
}

// Next.js will invalidate the cache when a
// request comes in, at most once every 5 minutes.
export const revalidate = 300

export async function generateStaticParams() {
  // Pre-generate the first 10 orders at build time
  // This is a reasonable subset for ISR
  try {
    // During build time, if backend is not available, return empty array
    // Pages will be generated on-demand when first requested
    const orders = await getOrders()

    return orders.slice(0, 10).map((order) => ({
      id: String(order.id),
    }))
  } catch (error) {
    console.warn('Backend not available during build, using fallback for ISR:', error)
    // Return empty array to allow ISR to work with on-demand generation
    return []
  }
}

export default async function OrderDetailsPage({ params }: PageProps) {
  const { id } = await params
  const orderId = Number.parseInt(id)

  if (isNaN(orderId)) {
    notFound()
  }

  let order
  try {
    order = await getOrderDetail(orderId)
  } catch (error) {
    console.error("Failed to fetch order details:", error)
    notFound()
  }

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

  const getStatusLabel = (status: string) => {
    return status.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())
  }

  const getProductionStatusColor = (status: string) => {
    switch (status) {
      case "planned":
        return "bg-gray-500"
      case "in_progress":
        return "bg-orange-500"
      case "completed":
        return "bg-green-500"
      case "cancelled":
        return "bg-red-500"
      default:
        return "bg-gray-500"
    }
  }

  const getDeliveryStatusColor = (status: string) => {
    switch (status) {
      case "pending":
        return "bg-gray-500"
      case "delivered":
        return "bg-green-500"
      case "cancelled":
        return "bg-red-500"
      default:
        return "bg-gray-500"
    }
  }

  return (
    <main className="px-12 py-8">
      <div className="mb-6">
        <Button variant="ghost" asChild className="mb-4">
          <Link href="/orders">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Orders
          </Link>
        </Button>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="font-bold text-3xl">Order #{order.id}</h1>
            <p className="text-muted-foreground">
              Placed on{" "}
              {new Date(order.created_at).toLocaleDateString("en-US", {
                year: "numeric",
                month: "long",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
              })}
            </p>
          </div>
          <Badge className={getStatusColor(order.status)}>{getStatusLabel(order.status)}</Badge>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="space-y-6 lg:col-span-2">
          {/* Order Items */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Package className="h-5 w-5" />
                Order Items
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {order.items.map((item) => (
                  <div key={item.id} className="flex gap-4">
                    <div className="relative h-20 w-20 flex-shrink-0 overflow-hidden rounded-md bg-muted">
                      <div className="flex h-full w-full items-center justify-center bg-muted">
                        <Package className="h-8 w-8 text-muted-foreground" />
                      </div>
                    </div>
                    <div className="flex flex-1 justify-between">
                      <div>
                        <h4 className="font-semibold">{item.product_name || `Product #${item.product_id}`}</h4>
                        <p className="text-muted-foreground text-sm">Quantity: {item.quantity}</p>
                        <p className="mt-1 text-sm">₱{(item.subtotal / item.quantity).toFixed(2)} each</p>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold">₱{item.subtotal.toFixed(2)}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <Separator className="my-4" />
              <div className="flex justify-between font-semibold text-lg">
                <span>Total Amount</span>
                <span className="text-primary">₱{order.total_amount.toFixed(2)}</span>
              </div>
            </CardContent>
          </Card>

          {/* Production Orders */}
          {order.production_orders.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Factory className="h-5 w-5" />
                  Production Orders
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {order.production_orders.map((production) => (
                  <div key={production.id}>
                    <div className="flex items-center justify-between">
                      <span className="text-muted-foreground text-sm">Production Order ID</span>
                      <span className="font-medium">#{production.id}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-muted-foreground text-sm">Status</span>
                      <Badge className={getProductionStatusColor(production.status)}>
                        {getStatusLabel(production.status)}
                      </Badge>
                    </div>
                    {production.start_date && (
                      <div className="flex items-center justify-between">
                        <span className="text-muted-foreground text-sm">Start Date</span>
                        <span className="font-medium">
                          {new Date(production.start_date).toLocaleDateString("en-US", {
                            year: "numeric",
                            month: "short",
                            day: "numeric",
                          })}
                        </span>
                      </div>
                    )}
                    {production.end_date && (
                      <div className="flex items-center justify-between">
                        <span className="text-muted-foreground text-sm">End Date</span>
                        <span className="font-medium">
                          {new Date(production.end_date).toLocaleDateString("en-US", {
                            year: "numeric",
                            month: "short",
                            day: "numeric",
                          })}
                        </span>
                      </div>
                    )}
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          {/* Deliveries */}
          {order.deliveries.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Truck className="h-5 w-5" />
                  Deliveries
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {order.deliveries.map((delivery) => (
                  <div key={delivery.id}>
                    <div className="flex items-center justify-between">
                      <span className="text-muted-foreground text-sm">Delivery ID</span>
                      <span className="font-medium">#{delivery.id}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-muted-foreground text-sm">Status</span>
                      <Badge className={getDeliveryStatusColor(delivery.status)}>{getStatusLabel(delivery.status)}</Badge>
                    </div>
                    {delivery.delivery_date && (
                      <div className="flex items-center justify-between">
                        <span className="text-muted-foreground text-sm">Delivery Date</span>
                        <span className="font-medium">
                          {new Date(delivery.delivery_date).toLocaleDateString("en-US", {
                            year: "numeric",
                            month: "short",
                            day: "numeric",
                          })}
                        </span>
                      </div>
                    )}
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          {/* Billing */}
          {order.billing && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Billing
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground text-sm">Invoice Number</span>
                  <span className="font-medium">{order.billing.invoice_number || "N/A"}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground text-sm">Amount</span>
                  <span className="font-semibold text-primary">₱{order.billing.amount.toFixed(2)}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground text-sm">Billed Date</span>
                  <span className="font-medium">
                    {order.billing.billed_date
                      ? new Date(order.billing.billed_date).toLocaleDateString("en-US", {
                          year: "numeric",
                          month: "short",
                          day: "numeric",
                        })
                      : "Not billed yet"
                    }
                  </span>
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Customer Info Sidebar */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Customer Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <p className="text-muted-foreground text-sm">Name</p>
                <p className="font-medium">{order.customer_name || "Unknown Customer"}</p>
              </div>
              <div>
                <p className="text-muted-foreground text-sm">Customer ID</p>
                <p className="font-medium">{order.customer_id}</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Order Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex gap-3">
                  <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-green-100">
                    <div className="h-2 w-2 rounded-full bg-green-600" />
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-sm">Order Created</p>
                    <p className="text-muted-foreground text-xs">
                      {new Date(order.created_at).toLocaleDateString("en-US", {
                        month: "short",
                        day: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  </div>
                </div>

                {order.production_orders.some(p => p.start_date) && (
                  <div className="flex gap-3">
                    <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-orange-100">
                      <div className="h-2 w-2 rounded-full bg-orange-600" />
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-sm">Production Started</p>
                      <p className="text-muted-foreground text-xs">
                        {new Date(order.production_orders.find(p => p.start_date)?.start_date || order.created_at).toLocaleDateString("en-US", {
                          month: "short",
                          day: "numeric",
                        })}
                      </p>
                    </div>
                  </div>
                )}

                {order.production_orders.some(p => p.end_date) && (
                  <div className="flex gap-3">
                    <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-blue-100">
                      <div className="h-2 w-2 rounded-full bg-blue-600" />
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-sm">Production Completed</p>
                      <p className="text-muted-foreground text-xs">
                        {new Date(order.production_orders.find(p => p.end_date)?.end_date || order.created_at).toLocaleDateString("en-US", {
                          month: "short",
                          day: "numeric",
                        })}
                      </p>
                    </div>
                  </div>
                )}

                {order.deliveries.some(d => d.delivery_date) && (
                  <div className="flex gap-3">
                    <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-green-100">
                      <div className="h-2 w-2 rounded-full bg-green-600" />
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-sm">Delivered</p>
                      <p className="text-muted-foreground text-xs">
                        {new Date(order.deliveries.find(d => d.delivery_date)?.delivery_date || order.created_at).toLocaleDateString("en-US", {
                          month: "short",
                          day: "numeric",
                        })}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  )
}
