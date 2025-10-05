"use client"

import { useEffect, useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import type { SalesOrder } from "@/lib/types"
import { getOrderStatus, type OrderStatusResponse } from "@/lib/dal"
import { Calendar, Package, DollarSign, Factory, User, Loader2, AlertCircle, Truck, Receipt } from "lucide-react"

interface SalesOrderDetailsDialogProps {
  order: SalesOrder
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function SalesOrderDetailsDialog({ order, open, onOpenChange }: SalesOrderDetailsDialogProps) {
  const [statusData, setStatusData] = useState<OrderStatusResponse | null>(null)
  const [statusError, setStatusError] = useState<string | null>(null)
  const [statusLoading, setStatusLoading] = useState(false)

  useEffect(() => {
    if (!open || !order?.id) {
      return
    }

    let active = true
    setStatusLoading(true)
    setStatusError(null)
    setStatusData(null)

    getOrderStatus(order.id)
      .then((data) => {
        if (!active) return
        setStatusData(data)
      })
      .catch((error) => {
        if (!active) return
        setStatusError(error instanceof Error ? error.message : "Failed to fetch order status")
      })
      .finally(() => {
        if (active) {
          setStatusLoading(false)
        }
      })

    return () => {
      active = false
    }
  }, [open, order?.id])

  const displayStatus: SalesOrder["status"] = statusData
    ? mapBackendStatus(statusData.status)
    : order.status

  const formatStatusLabel = (value: string) =>
    value
      .toLowerCase()
      .split("_")
      .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
      .join(" ")

  const formatDateTime = (value?: string | null) => (value ? new Date(value).toLocaleString() : "—")

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
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <div className="flex items-center justify-between">
            <DialogTitle>Sales Order Details</DialogTitle>
            <Badge variant="outline" className={getStatusColor(displayStatus)}>
              {displayStatus}
            </Badge>
          </div>
        </DialogHeader>

        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <div className="text-sm text-muted-foreground mb-1">Order Number</div>
                <div className="text-lg font-semibold text-foreground">{order.orderNumber}</div>
              </div>

              <div className="flex items-start gap-3">
                <User className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <div className="text-sm text-muted-foreground">Customer</div>
                  <div className="font-medium text-foreground">{order.customer}</div>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Package className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <div className="text-sm text-muted-foreground">Material</div>
                  <div className="font-medium text-foreground">{order.material}</div>
                  <div className="text-sm text-muted-foreground mt-1">Quantity: {order.quantity}</div>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <Calendar className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <div className="text-sm text-muted-foreground">Created Date</div>
                  <div className="font-medium text-foreground">{new Date(order.createdDate).toLocaleDateString()}</div>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Calendar className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <div className="text-sm text-muted-foreground">Delivery Date</div>
                  <div className="font-medium text-foreground">{new Date(order.deliveryDate).toLocaleDateString()}</div>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Factory className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <div className="text-sm text-muted-foreground">Plant</div>
                  <div className="font-medium text-foreground">{order.plant}</div>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <DollarSign className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <div className="text-sm text-muted-foreground">Net Value</div>
                  <div className="text-lg font-semibold text-foreground">${order.netValue.toLocaleString()}</div>
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-border pt-4 space-y-4">
            <div className="flex items-center justify-between">
              <div className="text-sm font-semibold text-foreground">Document Flow</div>
              {statusLoading && (
                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Loading status...
                </div>
              )}
            </div>

            {statusError && (
              <div className="flex items-center gap-2 text-sm text-destructive">
                <AlertCircle className="w-4 h-4" />
                <span>{statusError}</span>
              </div>
            )}

            {!statusError && statusData && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                  <div>
                    <div className="text-xs text-muted-foreground">Consolidated Status</div>
                    <Badge variant="outline" className={`mt-1 ${getStatusColor(displayStatus)}`}>
                      {displayStatus}
                    </Badge>
                  </div>
                  <div>
                    <div className="text-xs text-muted-foreground">Order Date</div>
                    <div className="text-sm font-medium text-foreground">{formatDateTime(statusData.order_date)}</div>
                  </div>
                  <div>
                    <div className="text-xs text-muted-foreground">Delivery Date</div>
                    <div className="text-sm font-medium text-foreground">{formatDateTime(statusData.delivery_date)}</div>
                  </div>
                  <div>
                    <div className="text-xs text-muted-foreground">Items</div>
                    <div className="text-sm font-medium text-foreground">{statusData.items_count}</div>
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-sm font-semibold text-foreground">
                    <Factory className="w-4 h-4" />
                    Work Orders
                  </div>
                  <div className="space-y-2">
                    {statusData.work_orders.length === 0 && (
                      <div className="text-sm text-muted-foreground">No work orders yet.</div>
                    )}
                    {statusData.work_orders.map((workOrder) => (
                      <div key={workOrder.id} className="rounded border border-border p-3">
                        <div className="flex items-center justify-between">
                          <div className="font-medium text-foreground">Work Order #{workOrder.id}</div>
                          <Badge variant="outline">{formatStatusLabel(workOrder.status)}</Badge>
                        </div>
                        <div className="mt-2 grid gap-1 text-xs text-muted-foreground">
                          <div>Quantity: {workOrder.quantity}</div>
                          <div>Start: {formatDateTime(workOrder.start_date)}</div>
                          <div>End: {formatDateTime(workOrder.end_date)}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-sm font-semibold text-foreground">
                    <Truck className="w-4 h-4" />
                    Deliveries
                  </div>
                  <div className="space-y-2">
                    {statusData.deliveries.length === 0 && (
                      <div className="text-sm text-muted-foreground">No deliveries yet.</div>
                    )}
                    {statusData.deliveries.map((delivery) => (
                      <div key={delivery.id} className="rounded border border-border p-3">
                        <div className="flex items-center justify-between">
                          <div className="font-medium text-foreground">Delivery #{delivery.id}</div>
                          <Badge variant="outline">{formatStatusLabel(delivery.status)}</Badge>
                        </div>
                        <div className="mt-2 grid gap-1 text-xs text-muted-foreground">
                          <div>Quantity: {delivery.quantity}</div>
                          <div>Delivered At: {formatDateTime(delivery.delivered_at)}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-sm font-semibold text-foreground">
                    <Receipt className="w-4 h-4" />
                    Invoices
                  </div>
                  <div className="space-y-2">
                    {statusData.invoices.length === 0 && (
                      <div className="text-sm text-muted-foreground">No invoices yet.</div>
                    )}
                    {statusData.invoices.map((invoice) => (
                      <div key={invoice.id} className="rounded border border-border p-3">
                        <div className="flex items-center justify-between">
                          <div className="font-medium text-foreground">Invoice #{invoice.id}</div>
                          <Badge variant="outline">{formatStatusLabel(invoice.status)}</Badge>
                        </div>
                        <div className="mt-2 grid gap-1 text-xs text-muted-foreground">
                          <div>Amount: ${invoice.total_amount.toLocaleString()}</div>
                          <div>Invoice Date: {formatDateTime(invoice.invoice_date)}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {!statusError && !statusLoading && !statusData && (
              <div className="text-sm text-muted-foreground">Status information unavailable.</div>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}

const backendStatusMap: Record<string, SalesOrder["status"]> = {
  NEW: "Open",
  CONFIRMED: "In Planning",
  IN_PROGRESS: "In Production",
  COMPLETED: "Delivered",
  BILLED: "Billed",
  CANCELLED: "Cancelled",
}

function mapBackendStatus(status: string): SalesOrder["status"] {
  return backendStatusMap[status] ?? "Open"
}
