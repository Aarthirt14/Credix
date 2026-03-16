"use client"

import { useState } from "react"
import { LocaleProvider } from "@/lib/locale-context"
import { AppProvider } from "@/lib/app-state"
import { LoginPage } from "@/components/login-page"
import { Dashboard } from "@/components/dashboard"
import { CustomersList } from "@/components/customers-list"
import { CustomerDetail } from "@/components/customer-detail"
import { OutstandingPage } from "@/components/outstanding-page"
import { ReportsPage } from "@/components/reports-page"
import { SettingsPage } from "@/components/settings-page"
import { BottomNav, type Page } from "@/components/bottom-nav"
import type { Customer } from "@/lib/app-state"

function AppContent() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [activePage, setActivePage] = useState<Page>("home")
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null)

  if (!isLoggedIn) {
    return <LoginPage onLogin={() => setIsLoggedIn(true)} />
  }

  // Customer Detail sub-view
  if (selectedCustomer) {
    return (
      <>
        <main className="mx-auto min-h-dvh max-w-[480px] bg-background">
          <CustomerDetail
            customer={selectedCustomer}
            onBack={() => setSelectedCustomer(null)}
          />
        </main>
        <BottomNav activePage="customers" onNavigate={(p) => { setSelectedCustomer(null); setActivePage(p) }} />
      </>
    )
  }

  return (
    <>
      <main className="mx-auto min-h-dvh max-w-[480px] bg-background">
        {activePage === "home" && <Dashboard onNavigate={setActivePage} />}
        {activePage === "customers" && (
          <CustomersList onSelectCustomer={setSelectedCustomer} />
        )}
        {activePage === "outstanding" && <OutstandingPage />}
        {activePage === "reports" && <ReportsPage />}
        {activePage === "settings" && <SettingsPage />}
      </main>
      <BottomNav activePage={activePage} onNavigate={setActivePage} />
    </>
  )
}

export default function Home() {
  return (
    <LocaleProvider>
      <AppProvider>
        <AppContent />
      </AppProvider>
    </LocaleProvider>
  )
}
 