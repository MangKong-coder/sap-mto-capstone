"use client"

import { Card } from "@/components/ui/card"
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts"

const data = [
  { date: "Jan 1", orders: 45, completed: 42 },
  { date: "Jan 5", orders: 52, completed: 48 },
  { date: "Jan 10", orders: 48, completed: 45 },
  { date: "Jan 15", orders: 61, completed: 58 },
  { date: "Jan 20", orders: 55, completed: 52 },
  { date: "Jan 25", orders: 67, completed: 63 },
  { date: "Jan 30", orders: 58, completed: 55 },
]

export function OrdersChart() {
  return (
    <Card className="p-6 bg-card border-border">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-card-foreground">Order Flow</h3>
          <p className="text-sm text-muted-foreground">New vs Completed orders</p>
        </div>
        <div className="flex items-center gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-chart-1" />
            <span className="text-muted-foreground">New Orders</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-chart-2" />
            <span className="text-muted-foreground">Completed</span>
          </div>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="colorOrders" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(var(--chart-1))" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(var(--chart-1))" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="colorCompleted" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="hsl(var(--chart-2))" stopOpacity={0.3} />
              <stop offset="95%" stopColor="hsl(var(--chart-2))" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" opacity={0.3} />
          <XAxis dataKey="date" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
          <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--popover))",
              border: "1px solid hsl(var(--border))",
              borderRadius: "8px",
            }}
          />
          <Area
            type="monotone"
            dataKey="orders"
            stroke="hsl(var(--chart-1))"
            strokeWidth={2}
            fillOpacity={1}
            fill="url(#colorOrders)"
          />
          <Area
            type="monotone"
            dataKey="completed"
            stroke="hsl(var(--chart-2))"
            strokeWidth={2}
            fillOpacity={1}
            fill="url(#colorCompleted)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </Card>
  )
}
