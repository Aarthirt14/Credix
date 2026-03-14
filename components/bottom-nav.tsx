"use client"

import { Home, Users, AlertCircle, BarChart3, Settings } from "lucide-react"
import { useLocale } from "@/lib/locale-context"
import { cn } from "@/lib/utils"

export type Page = "home" | "customers" | "outstanding" | "reports" | "settings"

interface BottomNavProps {
  activePage: Page
  onNavigate: (page: Page) => void
}

const navItems: { page: Page; icon: typeof Home; labelKey: "home" | "customers" | "outstanding" | "reports" | "settings" }[] = [
  { page: "home", icon: Home, labelKey: "home" },
  { page: "customers", icon: Users, labelKey: "customers" },
  { page: "outstanding", icon: AlertCircle, labelKey: "outstanding" },
  { page: "reports", icon: BarChart3, labelKey: "reports" },
  { page: "settings", icon: Settings, labelKey: "settings" },
]

export function BottomNav({ activePage, onNavigate }: BottomNavProps) {
  const { t } = useLocale()

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 border-t border-border bg-card" role="navigation" aria-label="Main navigation">
      <div className="mx-auto flex max-w-[480px] items-center justify-around py-1.5">
        {navItems.map(({ page, icon: Icon, labelKey }) => {
          const active = activePage === page
          return (
            <button
              key={page}
              onClick={() => onNavigate(page)}
              className={cn(
                "flex min-h-[48px] min-w-[48px] flex-col items-center justify-center gap-0.5 rounded-lg px-2 py-1 text-xs font-medium transition-colors",
                active
                  ? "text-[var(--primary)]"
                  : "text-muted-foreground hover:text-foreground"
              )}
              aria-current={active ? "page" : undefined}
            >
              <Icon className={cn("h-5 w-5", active && "stroke-[2.5]")} />
              <span className="text-[11px] leading-tight">{t(labelKey)}</span>
            </button>
          )
        })}
      </div>
      {/* Safe area padding for mobile */}
      <div className="h-[env(safe-area-inset-bottom)]" />
    </nav>
  )
}
