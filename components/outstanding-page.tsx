"use client"

import { Bell } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useLocale } from "@/lib/locale-context"
import { useAppState } from "@/lib/app-state"

export function OutstandingPage() {
  const { t } = useLocale()
  const { customers } = useAppState()

  const customersWithDues = customers
    .filter((c) => c.pending > 0)
    .sort((a, b) => b.pending - a.pending)

  const totalOutstanding = customersWithDues.reduce((sum, c) => sum + c.pending, 0)

  return (
    <div className="flex flex-col gap-4 px-4 pb-28 pt-6">
      {/* Summary Card */}
      <div className="rounded-xl border border-border bg-card p-5 text-center shadow-sm">
        <p className="text-sm text-muted-foreground">{t("totalDueAmount")}</p>
        <p className="mt-1 text-3xl font-bold text-[var(--destructive)]">
          {"\u20B9"}{totalOutstanding.toLocaleString("en-IN")}
        </p>
      </div>

      {/* Customer List */}
      {customersWithDues.length === 0 ? (
        <div className="py-16 text-center">
          <p className="text-base text-muted-foreground">{t("empty")}</p>
        </div>
      ) : (
        <div className="flex flex-col gap-2">
          {customersWithDues.map((customer) => (
            <div
              key={customer.id}
              className="flex items-center justify-between rounded-xl border border-border bg-card p-4 shadow-sm"
            >
              <div className="flex flex-col gap-0.5">
                <span className="text-base font-semibold text-foreground">{customer.name}</span>
                <span className="text-sm text-muted-foreground">{customer.phone}</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-base font-bold text-[var(--destructive)]">
                  {"\u20B9"}{customer.pending.toLocaleString("en-IN")}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  className="h-9 rounded-lg px-3"
                >
                  <Bell className="mr-1 h-3.5 w-3.5" />
                  <span className="text-xs">{t("remind")}</span>
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

# commit padding

# commit padding
 