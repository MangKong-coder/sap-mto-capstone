import { Package } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"

export default function Loading() {
  return (
    <main className="px-12 py-8">
      <div className="mb-6">
        <h1 className="font-bold text-3xl">My Orders</h1>
        <p className="text-muted-foreground">Track and manage your Mapúa merchandise orders</p>
      </div>

      <div className="space-y-4">
        {Array.from({ length: 3 }).map((_, index) => (
          <Card key={index} className="transition-shadow hover:shadow-md">
            <CardContent className="p-6">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <div className="h-6 w-20 bg-muted animate-pulse rounded" />
                    <div className="h-6 w-24 bg-muted animate-pulse rounded-full" />
                  </div>
                  <div className="mt-1 h-4 w-32 bg-muted animate-pulse rounded" />
                  <div className="mt-3 space-y-1">
                    <div className="h-4 w-48 bg-muted animate-pulse rounded" />
                    <div className="h-4 w-36 bg-muted animate-pulse rounded" />
                  </div>
                </div>

                <div className="flex items-center gap-4 sm:flex-col sm:items-end">
                  <div className="text-right">
                    <div className="h-4 w-12 bg-muted animate-pulse rounded mb-1" />
                    <div className="h-7 w-20 bg-muted animate-pulse rounded" />
                  </div>
                  <div className="h-9 w-24 bg-muted animate-pulse rounded" />
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </main>
  )
}
