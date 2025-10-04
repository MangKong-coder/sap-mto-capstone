"use client"

import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import type { ProductionOrder } from "@/lib/types"
import { Calendar, Package, Factory, LinkIcon } from "lucide-react"

interface ProductionOrderDetailsDialogProps {
  order: ProductionOrder
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function ProductionOrderDetailsDialog({ order, open, onOpenChange }: ProductionOrderDetailsDialogProps) {
  const getStatusColor = (status: ProductionOrder["status"]) => {
    switch (status) {
      case "Created":
        return "bg-blue-500/10 text-blue-500 border-blue-500/20"
      case "Released":
        return "bg-cyan-500/10 text-cyan-500 border-cyan-500/20"
      case "In Progress":
        return "bg-purple-500/10 text-purple-500 border-purple-500/20"
      case "Confirmed":
        return "bg-yellow-500/10 text-yellow-500 border-yellow-500/20"
      case "Completed":
        return "bg-green-500/10 text-green-500 border-green-500/20"
      default:
        return "bg-gray-500/10 text-gray-500 border-gray-500/20"
    }
  }

  const progress = (order.confirmedQuantity / order.quantity) * 100

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <div className="flex items-center justify-between">
            <DialogTitle>Production Order Details</DialogTitle>
            <Badge variant="outline" className={getStatusColor(order.status)}>
              {order.status}
            </Badge>
          </div>
        </DialogHeader>

        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <div className="text-sm text-muted-foreground mb-1">Production Order Number</div>
                <div className="text-lg font-semibold text-foreground">{order.productionOrderNumber}</div>
              </div>

              <div className="flex items-start gap-3">
                <LinkIcon className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <div className="text-sm text-muted-foreground">Linked Documents</div>
                  <div className="space-y-1 mt-1">
                    <div className="text-sm">
                      <span className="text-muted-foreground">Sales Order: </span>
                      <span className="font-medium text-primary">{order.salesOrderNumber}</span>
                    </div>
                    <div className="text-sm">
                      <span className="text-muted-foreground">Planned Order: </span>
                      <span className="font-medium text-foreground">{order.plannedOrderNumber}</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Package className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <div className="text-sm text-muted-foreground">Material</div>
                  <div className="font-medium text-foreground">{order.material}</div>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <Factory className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <div className="text-sm text-muted-foreground">Plant</div>
                  <div className="font-medium text-foreground">{order.plant}</div>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <Calendar className="w-5 h-5 text-muted-foreground mt-0.5" />
                <div>
                  <div className="text-sm text-muted-foreground">Production Dates</div>
                  <div className="space-y-1 mt-1">
                    <div className="text-sm">
                      <span className="text-muted-foreground">Start: </span>
                      <span className="font-medium text-foreground">
                        {new Date(order.startDate).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="text-sm">
                      <span className="text-muted-foreground">End: </span>
                      <span className="font-medium text-foreground">
                        {new Date(order.endDate).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-border pt-4">
            <div className="text-sm font-semibold text-foreground mb-3">Production Progress</div>
            <div className="space-y-3">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Target Quantity:</span>
                <span className="font-medium text-foreground">{order.quantity}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Confirmed Quantity:</span>
                <span className="font-medium text-foreground">{order.confirmedQuantity}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Remaining:</span>
                <span className="font-medium text-foreground">{order.quantity - order.confirmedQuantity}</span>
              </div>
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Completion:</span>
                  <span className="font-medium text-foreground">{Math.round(progress)}%</span>
                </div>
                <Progress value={progress} className="h-3" />
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
