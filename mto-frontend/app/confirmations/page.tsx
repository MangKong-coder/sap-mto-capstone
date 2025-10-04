"use client"

import { useState } from "react"
import { DashboardSidebar } from "@/components/dashboard-sidebar"
import { DashboardHeader } from "@/components/dashboard-header"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"
import { ConfirmationList } from "@/components/confirmation-list"
import { CreateConfirmationDialog } from "@/components/create-confirmation-dialog"

export default function ConfirmationsPage() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [createDialogOpen, setCreateDialogOpen] = useState(false)

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
                <h1 className="text-3xl font-bold text-foreground">Production Confirmations</h1>
                <p className="text-sm text-muted-foreground mt-1">
                  Confirm production quantities and update order status
                </p>
              </div>
              <Button onClick={() => setCreateDialogOpen(true)} className="gap-2">
                <Plus className="w-4 h-4" />
                Create Confirmation
              </Button>
            </div>
          </div>

          <ConfirmationList />
        </main>
      </div>

      <CreateConfirmationDialog open={createDialogOpen} onOpenChange={setCreateDialogOpen} />
    </div>
  )
}
