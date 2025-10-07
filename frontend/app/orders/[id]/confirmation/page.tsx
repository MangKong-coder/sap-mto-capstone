import Link from "next/link"
import { CheckCircle2, Package, ArrowRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { getOrderDetail } from "@/lib/dal/orders"
import { SalesOrderStatus } from "@/lib/types"

interface PageProps {
  params: Promise<{ id: string }>
}

export default async function OrderConfirmationPage({ params }: PageProps) {
  const { id } = await params
  const orderId = Number.parseInt(id)

  // Fetch order details from backend
  let order
  try {
    order = await getOrderDetail(orderId)
  } catch (error) {
    console.error("Failed to fetch order:", error)
    return (
      <main className="px-12 py-16">
        <div className="mx-auto max-w-md text-center">
          <h1 className="font-bold text-2xl">Order not found</h1>
          <p className="mt-2 text-muted-foreground">The order you're looking for doesn't exist or failed to load.</p>
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

  const getStatusLabel = (status: SalesOrderStatus) => {
    return status.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())
  }

  return (
    <main className="px-12 py-8">
      <div className="mx-auto max-w-3xl">
        <div className="mb-8 flex flex-col items-center gap-4 text-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
            <CheckCircle2 className="h-8 w-8 text-green-600" />
          </div>
          <div>
            <h1 className="font-bold text-3xl">Order Confirmed!</h1>
            <p className="mt-2 text-muted-foreground">Thank you for your order!</p>
          </div>
        </div>

        <Card className="mb-6">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Order #{order.id}</CardTitle>
              <Badge className={getStatusColor(order.status)}>{getStatusLabel(order.status)}</Badge>
            </div>
            <p className="text-muted-foreground text-sm">
              Placed on{" "}
              {new Date(order.created_at).toLocaleDateString("en-US", {
                year: "numeric",
                month: "long",
                day: "numeric",
              })}
            </p>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h3 className="mb-3 font-semibold">Order Items</h3>
              <div className="space-y-3">
                {order.items.map((item) => (
                  <div key={item.id} className="flex justify-between text-sm">
                    <div className="flex-1">
                      <span className="font-medium">{item.product_name || `Product #${item.product_id}`}</span>
                      <span className="text-muted-foreground"> × {item.quantity}</span>
                    </div>
                    <span className="font-medium">₱{item.subtotal.toFixed(2)}</span>
                  </div>
                ))}
              </div>
            </div>

            <Separator />

            <div className="flex justify-between font-semibold text-lg">
              <span>Total Amount</span>
              <span className="text-primary">₱{order.total_amount.toFixed(2)}</span>
            </div>
          </CardContent>
        </Card>

        <Card className="mb-6">
          <CardContent className="flex items-start gap-4 p-6">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
              <Package className="h-5 w-5 text-primary" />
            </div>
            <div className="flex-1">
              <h3 className="font-semibold">What's Next?</h3>
              <p className="mt-1 text-muted-foreground text-sm text-pretty">
                Your order has been received and will be processed shortly. A production order has been automatically
                created. You can track your order status from the "My Orders" page.
              </p>
            </div>
          </CardContent>
        </Card>

        <div className="flex gap-3">
          <Button asChild variant="outline" className="flex-1 bg-transparent">
            <Link href="/">Continue Shopping</Link>
          </Button>
          <Button asChild className="flex-1">
            <Link href={`/orders/${order.id}`}>
              View Order Details
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
      </div>
    </main>
  )
}
