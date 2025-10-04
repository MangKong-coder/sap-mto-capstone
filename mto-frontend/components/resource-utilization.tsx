"use client"

import { Card } from "@/components/ui/card"
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"
import { mockProductionOrders } from "@/lib/mock-data"

export function ResourceUtilization() {
  const workCenters = ["Line A", "Line B", "Line C", "Line D", "Line E"]

  const data = workCenters.map((wc) => {
    const ordersOnLine = mockProductionOrders.filter((po) => po.workCenter === wc)
    const totalCapacity = 100
    const utilization = Math.min(
      95,
      Math.round((ordersOnLine.length / mockProductionOrders.length) * totalCapacity * 1.5),
    )

    return {
      resource: wc,
      utilization,
    }
  })

  return (
    <Card className="p-6">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-foreground">Resource Utilization</h3>
        <p className="text-sm text-muted-foreground">Production line capacity usage</p>
      </div>

      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
          <XAxis
            dataKey="resource"
            stroke="hsl(var(--muted-foreground))"
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <YAxis
            stroke="hsl(var(--muted-foreground))"
            fontSize={12}
            tickLine={false}
            axisLine={false}
            domain={[0, 100]}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--popover))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "8px",
            }}
            formatter={(value) => [`${value}%`, "Utilization"]}
          />
          <Bar dataKey="utilization" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </Card>
  )
}
