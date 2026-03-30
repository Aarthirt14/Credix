"use client"

import { useEffect, useState } from "react"
import { Mic, UserPlus, AlertCircle, Bell, Users, CreditCard, ArrowRightLeft, CalendarDays, Wifi, WifiOff } from "lucide-react"
import { useLocale } from "@/lib/locale-context"
import { useAppState } from "@/lib/app-state"
import { VoiceOverlay } from "@/components/voice-overlay"
import type { Page } from "@/components/bottom-nav"
import { checkBackendHealth } from "@/lib/api"
import { cn } from "@/lib/utils"

interface DashboardProps {
  onNavigate: (page: Page) => void
}

export function Dashboard({ onNavigate }: DashboardProps) {
  const { t } = useLocale()
  const { shopName, customers } = useAppState()
  const [voiceOpen, setVoiceOpen] = useState(false)
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null)

  useEffect(() => {
    let cancelled = false

    const checkStatus = async () => {
      try {
        const ok = await checkBackendHealth()
        if (!cancelled) {
          setBackendOnline(ok)
        }
      } catch {
        if (!cancelled) {
          setBackendOnline(false)
        }
      }
    }

    void checkStatus()
    const interval = window.setInterval(checkStatus, 15000)

    return () => {
      cancelled = true
      window.clearInterval(interval)
    }
  }, [])

  const totalCustomers = customers.length
  const customersWithDues = customers.filter((c) => c.pending > 0).length
  const totalOutstanding = customers.reduce((sum, c) => sum + c.pending, 0)
  const todayStr = new Date().toISOString().split("T")[0]
  const todaysTransactions = customers.reduce(
    (sum, c) => sum + c.transactions.filter((tx) => tx.date === todayStr).length,
    0
  )

  const today = new Date().toLocaleDateString("ta-IN", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  })

  const statCards = [
    {
      label: t("totalCustomers"),
      value: totalCustomers.toString(),
      icon: Users,
      color: "text-[var(--primary)]",
      bg: "bg-[var(--primary)]/10",
      page: "customers" as Page,
    },
    {
      label: t("customersWithDues"),
      value: customersWithDues.toString(),
      icon: AlertCircle,
      color: "text-[var(--accent)]",
      bg: "bg-[var(--accent)]/10",
      page: "outstanding" as Page,
    },
    {
      label: t("totalOutstanding"),
      value: `\u20B9${totalOutstanding.toLocaleString("en-IN")}`,
      icon: CreditCard,
      color: totalOutstanding > 0 ? "text-[var(--destructive)]" : "text-[var(--success)]",
      bg: totalOutstanding > 0 ? "bg-[var(--destructive)]/10" : "bg-[var(--success)]/10",
      page: "outstanding" as Page,
    },
    {
      label: t("todaysTransactions"),
      value: todaysTransactions.toString(),
      icon: ArrowRightLeft,
      color: "text-[var(--primary)]",
      bg: "bg-[var(--primary)]/10",
      page: "reports" as Page,
    },
  ]

  return (
    <div className="flex flex-col gap-5 px-4 pb-36 pt-6">
      {/* Greeting */}
      <div className="space-y-1">
        <h1 className="text-xl font-bold text-foreground">
          {t("greeting")}, {shopName}
        </h1>
        <div className="flex items-center justify-between gap-2 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <CalendarDays className="h-4 w-4" />
            <span>{today}</span>
          </div>
          <div
            className={cn(
              "inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs",
              backendOnline === false
                ? "border-[var(--destructive)]/30 bg-[var(--destructive)]/10 text-[var(--destructive)]"
                : "border-[var(--success)]/30 bg-[var(--success)]/10 text-[var(--success)]"
            )}
          >
            {backendOnline === false ? <WifiOff className="h-3.5 w-3.5" /> : <Wifi className="h-3.5 w-3.5" />}
            <span>{backendOnline === false ? "Voice backend offline" : "Voice backend ready"}</span>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-3">
        {statCards.map((card) => (
          <button
            key={card.label}
            onClick={() => onNavigate(card.page)}
            className="flex flex-col gap-2 rounded-xl border border-border bg-card p-4 text-left shadow-sm transition-shadow hover:shadow-md active:scale-[0.98]"
          >
            <div className={`flex h-9 w-9 items-center justify-center rounded-lg ${card.bg}`}>
              <card.icon className={`h-5 w-5 ${card.color}`} />
            </div>
            <span className={`text-xl font-bold ${card.color}`}>{card.value}</span>
            <span className="text-xs text-muted-foreground leading-tight">{card.label}</span>
          </button>
        ))}
      </div>

      {/* Main Mic Button */}
      <div className="flex flex-col items-center gap-3 py-4">
        <button
          onClick={() => {
            if (backendOnline === false) {
              return
            }
            setVoiceOpen(true)
          }}
          disabled={backendOnline === false}
          className="group relative flex h-[120px] w-[120px] items-center justify-center rounded-full bg-[var(--primary)] shadow-lg shadow-[var(--primary)]/30 transition-all hover:shadow-xl hover:shadow-[var(--primary)]/40 active:scale-95"
          aria-label={t("startSpeaking")}
        >
          <Mic className="h-12 w-12 text-[var(--primary-foreground)] transition-transform group-hover:scale-110" />
          {/* Pulse rings */}
          <div className="absolute inset-0 animate-ping rounded-full bg-[var(--primary)] opacity-10" />
          <div className="absolute -inset-2 animate-pulse rounded-full border-2 border-[var(--primary)]/20" />
        </button>
        <span className="text-base font-semibold text-foreground">{t("startSpeaking")}</span>
        <p className="text-center text-xs text-muted-foreground">
          Speak in Tamil naturally, for example: "ரவி இருபது ரூபாய்".
        </p>
      </div>

      {/* Quick Actions */}
      <div className="flex items-center justify-center gap-3">
        {[
          { label: t("addCustomer"), icon: UserPlus, action: () => onNavigate("customers") },
          { label: t("viewOutstanding"), icon: AlertCircle, action: () => onNavigate("outstanding") },
          { label: t("sendReminder"), icon: Bell, action: () => {} },
        ].map((item) => (
          <button
            key={item.label}
            onClick={item.action}
            className="flex min-h-[48px] flex-1 flex-col items-center gap-1.5 rounded-xl border border-border bg-card px-2 py-3 text-xs font-medium text-foreground shadow-sm transition-colors hover:bg-muted active:scale-[0.98]"
          >
            <item.icon className="h-5 w-5 text-[var(--primary)]" />
            <span className="text-center text-[11px] leading-tight">{item.label}</span>
          </button>
        ))}
      </div>

      {/* Voice Overlay */}
      <VoiceOverlay open={voiceOpen} onClose={() => setVoiceOpen(false)} />
    </div>
  )
}


 