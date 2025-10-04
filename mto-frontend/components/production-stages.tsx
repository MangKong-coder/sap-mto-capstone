"use client"

import { Card } from "@/components/ui/card"
import { ArrowRight } from "lucide-react"

const stages = [
  { name: "Order Received", count: 23, color: "bg-chart-1" },
  { name: "Material Sourcing", count: 18, color: "bg-chart-3" },
  { name: "In Production", count: 42, color: "bg-chart-2" },
  { name: "Quality Check", count: 15, color: "bg-chart-5" },
  { name: "Ready to Ship", count: 29, color: "bg-success" },
]

export function ProductionStages() {
  return (
    <Card className="p-6 bg-card border-border">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-card-foreground">Production Pipeline</h3>
        <p className="text-sm text-muted-foreground">Orders by production stage</p>
      </div>

      <div className="flex items-center gap-4 overflow-x-auto pb-2">
        {stages.map((stage, index) => (
          <div key={stage.name} className="flex items-center gap-4">
            <div className="flex-shrink-0 min-w-[180px]">
              <div className="p-4 rounded-lg bg-secondary/50 border border-border">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-card-foreground">{stage.name}</span>
                  <div className={`w-2 h-2 rounded-full ${stage.color}`} />
                </div>
                <div className="flex items-baseline gap-2">
                  <span className="text-2xl font-semibold text-card-foreground">{stage.count}</span>
                  <span className="text-sm text-muted-foreground">orders</span>
                </div>
              </div>
            </div>
            {index < stages.length - 1 && <ArrowRight className="w-5 h-5 text-muted-foreground flex-shrink-0" />}
          </div>
        ))}
      </div>
    </Card>
  )
}
