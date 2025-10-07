import { Card, CardContent } from "@/components/ui/card"

export default function Loading() {
  return (
    <main className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <div className="h-8 w-48 bg-muted animate-pulse rounded mb-2" />
        <div className="h-4 w-64 bg-muted animate-pulse rounded" />
      </div>

      <div className="rounded-md border">
        <div className="p-4">
          <div className="flex items-center justify-between mb-4">
            <div className="h-6 w-32 bg-muted animate-pulse rounded" />
            <div className="flex gap-2">
              <div className="h-9 w-20 bg-muted animate-pulse rounded" />
              <div className="h-9 w-24 bg-muted animate-pulse rounded" />
            </div>
          </div>

          {/* Table header skeleton */}
          <div className="grid grid-cols-5 gap-4 mb-4 pb-2 border-b">
            <div className="h-4 w-16 bg-muted animate-pulse rounded" />
            <div className="h-4 w-20 bg-muted animate-pulse rounded" />
            <div className="h-4 w-12 bg-muted animate-pulse rounded" />
            <div className="h-4 w-16 bg-muted animate-pulse rounded" />
            <div className="h-4 w-20 bg-muted animate-pulse rounded" />
          </div>

          {/* Table rows skeleton */}
          {Array.from({ length: 5 }).map((_, index) => (
            <div key={index} className="grid grid-cols-5 gap-4 py-3 border-b last:border-b-0">
              <div className="h-4 w-12 bg-muted animate-pulse rounded" />
              <div className="h-4 w-24 bg-muted animate-pulse rounded" />
              <div className="h-6 w-16 bg-muted animate-pulse rounded-full" />
              <div className="h-4 w-16 bg-muted animate-pulse rounded" />
              <div className="flex gap-2">
                <div className="h-8 w-16 bg-muted animate-pulse rounded" />
                <div className="h-8 w-16 bg-muted animate-pulse rounded" />
                <div className="h-8 w-16 bg-muted animate-pulse rounded" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  )
}
