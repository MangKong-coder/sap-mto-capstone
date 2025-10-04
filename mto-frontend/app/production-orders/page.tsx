"use client"

import { useState } from "react"
import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { DashboardHeader } from "@/components/dashboard-header"
import { Search, Filter } from "lucide-react"
import { ProductionOrderTable } from "@/components/production-order-table"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function ProductionOrdersPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")

  return (
    <div className="min-h-screen bg-background">
      <DashboardSidebar open={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />

      <div
        className="transition-all duration-300"
        style={{
          marginLeft: sidebarOpen ? "16rem" : "4rem",
        }}
      >
        <DashboardHeader />

        <main className="p-6">
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <div>
                <h1 className="text-3xl font-bold text-foreground">Fulfillment Orders</h1>
                <p className="text-sm text-muted-foreground mt-1">
                  Transaction Code: CO01 - Merchandise Fulfillment Order
                </p>
              </div>
            </div>
          </div>

          <div className="bg-card border border-border rounded-lg">
            <div className="p-4 border-b border-border">
              <div className="flex items-center gap-3">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="Search by fulfillment order, merchandise order, or item..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <Button variant="outline" className="gap-2 bg-transparent">
                  <Filter className="w-4 h-4" />
                  Filter
                </Button>
              </div>
            </div>

            <ProductionOrderTable searchQuery={searchQuery} />
          </div>
        </main>
      </div>
    </div>
  )
}
