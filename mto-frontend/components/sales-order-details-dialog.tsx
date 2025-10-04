"use client"

import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import type { SalesOrder } from "@/lib/types"
import { Calendar, Package, DollarSign, Factory, User } from "lucide-react"

interface SalesOrderDetailsDialogProps {
  order: SalesOrder
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function SalesOrderDetailsDialog({ order, open, onOpenChange }: SalesOrderDetailsDialogProps) {
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
            <Badge variant="outline" className={getStatusColor(order.status)}>
              {order.status}
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

          <div className="border-t border-border pt-4">
            <div className="text-sm font-semibold text-foreground mb-3">Document Flow</div>
            <div className="space-y-2">
              <div className="flex items-center gap-3 text-sm">
                <div className="w-32 text-muted-foreground">Sales Order:</div>
                <div className="font-medium text-foreground">{order.orderNumber}</div>
              </div>
              {order.status !== "Open" && (
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-32 text-muted-foreground">Planned Order:</div>
                  <div className="font-medium text-foreground">PO-{order.orderNumber.split("-")[2]}</div>
                </div>
              )}
              {(order.status === "In Production" || order.status === "Delivered" || order.status === "Billed") && (
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-32 text-muted-foreground">Production Order:</div>
                  <div className="font-medium text-foreground">PRO-{order.orderNumber.split("-")[2]}</div>
                </div>
              )}
              {(order.status === "Delivered" || order.status === "Billed") && (
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-32 text-muted-foreground">Delivery:</div>
                  <div className="font-medium text-foreground">DL-{order.orderNumber.split("-")[2]}</div>
                </div>
              )}
              {order.status === "Billed" && (
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-32 text-muted-foreground">Billing:</div>
                  <div className="font-medium text-foreground">INV-{order.orderNumber.split("-")[2]}</div>
                </div>
              )}
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
