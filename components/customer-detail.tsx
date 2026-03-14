"use client"

import { useState } from "react"
import { ArrowLeft, Phone, CreditCard, Wallet, Bell, Plus, Minus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useLocale } from "@/lib/locale-context"
import { useAppState, type Customer } from "@/lib/app-state"
import { cn } from "@/lib/utils"

interface CustomerDetailProps {
  customer: Customer
  onBack: () => void
}

export function CustomerDetail({ customer: initialCustomer, onBack }: CustomerDetailProps) {
  const { t } = useLocale()
  const { customers, addTransaction } = useAppState()
  const [addingType, setAddingType] = useState<"credit" | "payment" | null>(null)
  const [amount, setAmount] = useState("")

  // Get live customer data
  const customer = customers.find((c) => c.id === initialCustomer.id) || initialCustomer

  function handleAdd() {
    if (!addingType || !amount || isNaN(Number(amount))) return
    addTransaction(customer.id, addingType, Number(amount))
    setAmount("")
    setAddingType(null)
  }

  return (
    <div className="flex flex-col pb-28">
      {/* Header */}
      <div className="sticky top-0 z-10 border-b border-border bg-card px-4 pb-4 pt-6">
        <button
          onClick={onBack}
          className="mb-4 flex min-h-[48px] items-center gap-2 text-base font-medium text-[var(--primary)]"
        >
          <ArrowLeft className="h-5 w-5" />
          <span>{t("customers")}</span>
        </button>

        <div className="flex items-start justify-between">
          <div className="flex flex-col gap-1">
            <h1 className="text-xl font-bold text-foreground">{customer.name}</h1>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Phone className="h-4 w-4" />
              <span>{customer.phone}</span>
            </div>
          </div>
          <a
            href={`tel:${customer.phone}`}
            className="flex h-10 w-10 items-center justify-center rounded-full bg-[var(--primary)]/10 text-[var(--primary)]"
            aria-label="Call customer"
          >
            <Phone className="h-5 w-5" />
          </a>
        </div>

        {/* Pending Amount */}
        <div className="mt-4 rounded-xl bg-muted/50 p-4 text-center">
          <p className="text-sm text-muted-foreground">{t("pendingAmount")}</p>
          <p
            className={cn(
              "mt-1 text-3xl font-bold",
              customer.pending > 0 ? "text-[var(--destructive)]" : "text-[var(--success)]"
            )}
          >
            {"\u20B9"}{customer.pending.toLocaleString("en-IN")}
          </p>
        </div>
      </div>

      {/* Add Transaction Form */}
      {addingType && (
        <div className="mx-4 mt-4 animate-in fade-in slide-in-from-top-2 rounded-xl border border-border bg-card p-4 shadow-sm duration-200">
          <div className="flex items-center gap-3">
            <Input
              type="tel"
              inputMode="numeric"
              placeholder={t("amount")}
              value={amount}
              onChange={(e) => setAmount(e.target.value.replace(/\D/g, ""))}
              className="h-12 flex-1 rounded-xl text-center text-lg text-foreground"
              autoFocus
            />
            <Button
              onClick={handleAdd}
              disabled={!amount}
              className={cn(
                "h-12 rounded-xl px-6 font-semibold text-[var(--primary-foreground)]",
                addingType === "credit" ? "bg-[var(--destructive)] hover:bg-[var(--destructive)]/90" : "bg-[var(--success)] hover:bg-[var(--success)]/90"
              )}
            >
              {addingType === "credit" ? <Plus className="h-5 w-5" /> : <Minus className="h-5 w-5" />}
            </Button>
          </div>
          <button
            onClick={() => { setAddingType(null); setAmount("") }}
            className="mt-2 w-full text-center text-sm text-muted-foreground"
          >
            {t("cancel")}
          </button>
        </div>
      )}

      {/* Transaction History */}
      <div className="px-4 pt-5">
        <h2 className="mb-3 text-base font-semibold text-foreground">{t("transactionHistory")}</h2>
        <div className="flex flex-col gap-2">
          {customer.transactions.length === 0 ? (
            <p className="py-8 text-center text-sm text-muted-foreground">{t("empty")}</p>
          ) : (
            customer.transactions.map((tx) => (
              <div
                key={tx.id}
                className="flex items-center justify-between rounded-xl border border-border bg-card p-3"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={cn(
                      "flex h-9 w-9 items-center justify-center rounded-lg",
                      tx.type === "credit" ? "bg-[var(--destructive)]/10" : "bg-[var(--success)]/10"
                    )}
                  >
                    {tx.type === "credit" ? (
                      <CreditCard className={cn("h-4 w-4 text-[var(--destructive)]")} />
                    ) : (
                      <Wallet className={cn("h-4 w-4 text-[var(--success)]")} />
                    )}
                  </div>
                  <div className="flex flex-col">
                    <span className="text-sm font-medium text-foreground">{t(tx.type)}</span>
                    <span className="text-xs text-muted-foreground">{tx.date}</span>
                  </div>
                </div>
                <span
                  className={cn(
                    "text-base font-semibold",
                    tx.type === "credit" ? "text-[var(--destructive)]" : "text-[var(--success)]"
                  )}
                >
                  {tx.type === "credit" ? "+" : "-"}{"\u20B9"}{tx.amount}
                </span>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Bottom Action Bar */}
      <div className="fixed bottom-16 left-0 right-0 z-30 border-t border-border bg-card px-4 py-3">
        <div className="mx-auto flex max-w-[480px] gap-2">
          <Button
            onClick={() => setAddingType("credit")}
            className="h-12 flex-1 rounded-xl bg-[var(--destructive)] text-sm font-semibold text-[var(--destructive-foreground)] hover:bg-[var(--destructive)]/90"
          >
            <CreditCard className="mr-2 h-4 w-4" />
            {t("addCredit")}
          </Button>
          <Button
            onClick={() => setAddingType("payment")}
            className="h-12 flex-1 rounded-xl bg-[var(--success)] text-sm font-semibold text-[var(--success-foreground)] hover:bg-[var(--success)]/90"
          >
            <Wallet className="mr-2 h-4 w-4" />
            {t("addPayment")}
          </Button>
          <Button
            variant="outline"
            className="h-12 rounded-xl px-4"
          >
            <Bell className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}
