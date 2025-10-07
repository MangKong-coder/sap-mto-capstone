import type React from "react"
import { Building2 } from "lucide-react"
import { AdminSidebar } from "@/components/admin/admin-sidebar"

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-background">
      <AdminSidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <header className="flex h-14 items-center justify-between border-b border-zinc-200 bg-white px-6 shadow-sm">
          <div className="flex items-center gap-3">
            <Building2 className="h-5 w-5 text-red-600" />
            <h1 className="font-semibold text-zinc-900">Mapúa Bookstore Operations</h1>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-zinc-600">Admin Portal</span>
          </div>
        </header>
        <main className="flex-1 overflow-auto bg-muted/30 p-6">{children}</main>
      </div>
    </div>
  )
}
