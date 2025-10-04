"use client"

import { mockProductionOrders } from "@/lib/mock-data"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { CheckCircle, Clock, Factory } from "lucide-react"

export function ConfirmationList() {
  const activeOrders = mockProductionOrders.filter(
    (order) => order.status === "Released" || order.status === "In Progress",
  )

  return (
    <div className="grid gap-4">
      {activeOrders.map((order) => {
        const progress = (order.confirmedQuantity / order.quantity) * 100
        const remaining = order.quantity - order.confirmedQuantity

        return (
          <Card key={order.id} className="p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-lg bg-purple-500/10 flex items-center justify-center">
                  <Factory className="w-6 h-6 text-purple-500" />
                </div>
                <div>
                  <h3 className="font-semibold text-foreground text-lg">{order.productionOrderNumber}</h3>
                  <p className="text-sm text-muted-foreground mt-1">{order.material}</p>
                  <div className="flex items-center gap-3 mt-2">
                    <span className="text-xs text-muted-foreground">Sales Order: {order.salesOrderNumber}</span>
                    <span className="text-xs text-muted-foreground">Plant: {order.plant}</span>
                  </div>
                </div>
              </div>
              <Badge
                variant="outline"
                className={
                  order.status === "In Progress"
                    ? "bg-purple-500/10 text-purple-500 border-purple-500/20"
                    : "bg-cyan-500/10 text-cyan-500 border-cyan-500/20"
                }
              >
                {order.status}
              </Badge>
            </div>

            <div className="grid grid-cols-3 gap-6 mb-4">
              <div className="space-y-1">
                <div className="text-sm text-muted-foreground">Target Quantity</div>
                <div className="text-2xl font-bold text-foreground">{order.quantity}</div>
              </div>
              <div className="space-y-1">
                <div className="text-sm text-muted-foreground">Confirmed</div>
                <div className="text-2xl font-bold text-green-500">{order.confirmedQuantity}</div>
              </div>
              <div className="space-y-1">
                <div className="text-sm text-muted-foreground">Remaining</div>
                <div className="text-2xl font-bold text-yellow-500">{remaining}</div>
              </div>
            </div>

            <div className="space-y-2 mb-4">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Production Progress</span>
                <span className="font-medium text-foreground">{Math.round(progress)}%</span>
              </div>
              <Progress value={progress} className="h-2" />
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-border">
              <div className="flex items-center gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-muted-foreground" />
                  <span className="text-muted-foreground">
                    {new Date(order.startDate).toLocaleDateString()} - {new Date(order.endDate).toLocaleDateString()}
                  </span>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="outline" size="sm">
                  View Details
                </Button>
                <Button size="sm" className="gap-2">
                  <CheckCircle className="w-4 h-4" />
                  Confirm Production
                </Button>
              </div>
            </div>
          </Card>
        )
      })}

      {activeOrders.length === 0 && (
        <Card className="p-12">
          <div className="text-center">
            <div className="w-16 h-16 rounded-full bg-muted mx-auto mb-4 flex items-center justify-center">
              <CheckCircle className="w-8 h-8 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-semibold text-foreground mb-2">No Active Production Orders</h3>
            <p className="text-sm text-muted-foreground">
              There are no production orders currently in progress that require confirmation.
            </p>
          </div>
        </Card>
      )}
    </div>
  )
}
