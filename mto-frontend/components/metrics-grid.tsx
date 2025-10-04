"use client"

import { Card } from "@/components/ui/card"
import { TrendingUp, FileText, Cog, Package, DollarSign } from "lucide-react"
import { mockSalesOrders, mockProductionOrders, mockDeliveries, mockBillings } from "@/lib/mock-data"

export function MetricsGrid() {
  const metrics = [
    {
      label: "Sales Orders (VA01)",
      value: mockSalesOrders.length.toString(),
      change: "+12%",
      trend: "up",
      icon: FileText,
      color: "text-blue-500",
    },
    {
      label: "Production Orders (CO01)",
      value: mockProductionOrders.length.toString(),
      change: "+8%",
      trend: "up",
      icon: Cog,
      color: "text-purple-500",
    },
    {
      label: "Deliveries (VL01N)",
      value: mockDeliveries.length.toString(),
      change: "+5%",
      trend: "up",
      icon: Package,
      color: "text-green-500",
    },
    {
      label: "Billing Documents (VF01)",
      value: mockBillings.length.toString(),
      change: "+6%",
      trend: "up",
      icon: DollarSign,
      color: "text-emerald-500",
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {metrics.map((metric) => (
        <Card key={metric.label} className="p-6">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm text-muted-foreground mb-1">{metric.label}</p>
              <p className="text-3xl font-bold text-foreground mb-2">{metric.value}</p>
              <div className="flex items-center gap-1 text-sm">
                <TrendingUp className="w-4 h-4 text-green-500" />
                <span className="text-green-500 font-medium">{metric.change}</span>
                <span className="text-muted-foreground">vs last month</span>
              </div>
            </div>
            <div className={`p-3 rounded-lg bg-muted ${metric.color}`}>
              <metric.icon className="w-6 h-6" />
            </div>
          </div>
        </Card>
      ))}
    </div>
  )
}
