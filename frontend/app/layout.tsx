import type React from "react"
import type { Metadata } from "next"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"
import "./globals.css"
import { Header } from "@/components/header"
import { Suspense } from "react"
import { Toaster } from "@/components/ui/sonner"

export const metadata: Metadata = {
  title: "SAP MTO",
  description: "SAP MTO",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${GeistSans.variable} ${GeistMono.variable} antialiased`}>
      <body>
        <Suspense fallback={<div>Loading...</div>}>
          <Header />
          {children}
        </Suspense>
        <Toaster />
      </body>
    </html>
  )
}
