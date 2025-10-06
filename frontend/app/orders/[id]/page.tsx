"use client"

import { use } from "react"
import Link from "next/link"
import Image from "next/image"
import { ArrowLeft, Package, Truck, FileText, Factory } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { useOrdersStore } from "@/lib/orders-store"
import { mockCustomer, mockProducts } from "@/lib/mock-data"
import { SalesOrderStatus, ProductionOrderStatus, DeliveryStatus } from "@/lib/types"

interface PageProps {
  params: Promise<{ id: string }>
}

export default function OrderDetailsPage({ params }: PageProps) {
  const { id } = use(params)
  const orderId = Number.parseInt(id)
  const order = useOrdersStore((state) => state.getOrderById(orderId))
  const productionOrder = useOrdersStore((state) => state.getProductionOrderByOrderId(orderId))
  const delivery = useOrdersStore((state) => state.getDeliveryByOrderId(orderId))
  const billing = useOrdersStore((state) => state.getBillingByOrderId(orderId))

  if (!order) {
    return (
      <main className="px-12 py-16">
        <div className="mx-auto max-w-md text-center">
          <h1 className="font-bold text-2xl">Order not found</h1>
          <p className="mt-2 text-muted-foreground">The order you're looking for doesn't exist.</p>
          <Button asChild className="mt-4">
            <Link href="/orders">View My Orders</Link>
          </Button>
        </div>
      </main>
    )
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

  const getProductionStatusColor = (status: ProductionOrderStatus) => {
    switch (status) {
      case ProductionOrderStatus.PLANNED:
        return "bg-gray-500"
      case ProductionOrderStatus.IN_PROGRESS:
        return "bg-orange-500"
      case ProductionOrderStatus.COMPLETED:
        return "bg-green-500"
      case ProductionOrderStatus.CANCELLED:
        return "bg-red-500"
      default:
        return "bg-gray-500"
    }
  }

  const getDeliveryStatusColor = (status: DeliveryStatus) => {
    switch (status) {
      case DeliveryStatus.PENDING:
        return "bg-gray-500"
      case DeliveryStatus.DELIVERED:
        return "bg-green-500"
      case DeliveryStatus.CANCELLED:
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
                {order.items.map((item) => {
                  const product = mockProducts.find((p) => p.id === item.product_id)
                  if (!product) return null

                  return (
                    <div key={item.id} className="flex gap-4">
                      <div className="relative h-20 w-20 flex-shrink-0 overflow-hidden rounded-md bg-muted">
                        <Image
                          src={product.image_url || "/placeholder.svg"}
                          alt={product.name}
                          fill
                          className="object-cover"
                        />
                      </div>
                      <div className="flex flex-1 justify-between">
                        <div>
                          <h4 className="font-semibold">{product.name}</h4>
                          <p className="text-muted-foreground text-sm">Quantity: {item.quantity}</p>
                          <p className="mt-1 text-sm">₱{product.price.toFixed(2)} each</p>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold">₱{item.subtotal.toFixed(2)}</p>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
              <Separator className="my-4" />
              <div className="flex justify-between font-semibold text-lg">
                <span>Total Amount</span>
                <span className="text-primary">₱{order.total_amount.toFixed(2)}</span>
              </div>
            </CardContent>
          </Card>

          {/* Production Order */}
          {productionOrder && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Factory className="h-5 w-5" />
                  Production Order
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground text-sm">Production Order ID</span>
                  <span className="font-medium">#{productionOrder.id}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground text-sm">Status</span>
                  <Badge className={getProductionStatusColor(productionOrder.status)}>
                    {getStatusLabel(productionOrder.status)}
                  </Badge>
                </div>
                {productionOrder.start_date && (
                  <div className="flex items-center justify-between">
                    <span className="text-muted-foreground text-sm">Start Date</span>
                    <span className="font-medium">
                      {new Date(productionOrder.start_date).toLocaleDateString("en-US", {
                        year: "numeric",
                        month: "short",
                        day: "numeric",
                      })}
                    </span>
                  </div>
                )}
                {productionOrder.end_date && (
                  <div className="flex items-center justify-between">
                    <span className="text-muted-foreground text-sm">End Date</span>
                    <span className="font-medium">
                      {new Date(productionOrder.end_date).toLocaleDateString("en-US", {
                        year: "numeric",
                        month: "short",
                        day: "numeric",
                      })}
                    </span>
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {/* Delivery */}
          {delivery && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Truck className="h-5 w-5" />
                  Delivery
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
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
              </CardContent>
            </Card>
          )}

          {/* Billing */}
          {billing && (
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
                  <span className="font-medium">{billing.invoice_number}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground text-sm">Amount</span>
                  <span className="font-semibold text-primary">₱{billing.amount.toFixed(2)}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground text-sm">Billed Date</span>
                  <span className="font-medium">
                    {new Date(billing.billed_date).toLocaleDateString("en-US", {
                      year: "numeric",
                      month: "short",
                      day: "numeric",
                    })}
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
                <p className="font-medium">{mockCustomer.name}</p>
              </div>
              <div>
                <p className="text-muted-foreground text-sm">Email</p>
                <p className="font-medium">{mockCustomer.email}</p>
              </div>
              <div>
                <p className="text-muted-foreground text-sm">Role</p>
                <Badge variant="secondary">{getStatusLabel(mockCustomer.role)}</Badge>
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

                {productionOrder && productionOrder.start_date && (
                  <div className="flex gap-3">
                    <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-orange-100">
                      <div className="h-2 w-2 rounded-full bg-orange-600" />
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-sm">Production Started</p>
                      <p className="text-muted-foreground text-xs">
                        {new Date(productionOrder.start_date).toLocaleDateString("en-US", {
                          month: "short",
                          day: "numeric",
                        })}
                      </p>
                    </div>
                  </div>
                )}

                {productionOrder && productionOrder.end_date && (
                  <div className="flex gap-3">
                    <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-blue-100">
                      <div className="h-2 w-2 rounded-full bg-blue-600" />
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-sm">Production Completed</p>
                      <p className="text-muted-foreground text-xs">
                        {new Date(productionOrder.end_date).toLocaleDateString("en-US", {
                          month: "short",
                          day: "numeric",
                        })}
                      </p>
                    </div>
                  </div>
                )}

                {delivery && delivery.delivery_date && (
                  <div className="flex gap-3">
                    <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-green-100">
                      <div className="h-2 w-2 rounded-full bg-green-600" />
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-sm">Delivered</p>
                      <p className="text-muted-foreground text-xs">
                        {new Date(delivery.delivery_date).toLocaleDateString("en-US", {
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
