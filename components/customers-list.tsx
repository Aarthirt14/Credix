"use client"

import { useState } from "react"
import { Search, CheckCircle2, Users, Plus, Trash2 } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { useLocale } from "@/lib/locale-context"
import { useAppState, type Customer } from "@/lib/app-state"
import { cn } from "@/lib/utils"

type Filter = "all" | "pending" | "exhausted"

interface CustomersListProps {
  onSelectCustomer: (customer: Customer) => void
}

export function CustomersList({ onSelectCustomer }: CustomersListProps) {
  const { t } = useLocale()
  const { customers, addCustomer, deleteCustomer } = useAppState()
  const [search, setSearch] = useState("")
  const [filter, setFilter] = useState<Filter>("all")
  const [addOpen, setAddOpen] = useState(false)
  const [name, setName] = useState("")
  const [phone, setPhone] = useState("")

  const filtered = customers.filter((c) => {
    const matchesSearch =
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.phone.includes(search)
    const matchesFilter =
      filter === "all" ||
      (filter === "pending" && c.pending > 0) ||
      (filter === "exhausted" && c.pending === 0)
    return matchesSearch && matchesFilter
  })

  const filters: { key: Filter; label: string }[] = [
    { key: "all", label: t("all") },
    { key: "pending", label: "Pending" },
    { key: "exhausted", label: "Exhausted" },
  ]

  function handleAddCustomer() {
    const trimmedName = name.trim()
    const trimmedPhone = phone.trim()
    if (!trimmedName || !trimmedPhone) return

    addCustomer(trimmedName, trimmedPhone)
    setName("")
    setPhone("")
    setAddOpen(false)
  }

  return (
    <div className="flex flex-col gap-4 px-4 pb-28 pt-6">
      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
        <Input
          type="search"
          placeholder={t("searchCustomer")}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="h-12 rounded-xl border-border bg-card pl-10 text-base text-foreground placeholder:text-muted-foreground"
        />
      </div>

      {/* Filter Toggles */}
      <div className="flex items-center justify-between gap-2">
        <div className="flex gap-2">
        {filters.map(({ key, label }) => (
          <button
            key={key}
            onClick={() => setFilter(key)}
            className={cn(
              "min-h-[40px] rounded-full px-4 py-1.5 text-sm font-medium transition-colors",
              filter === key
                ? "bg-[var(--primary)] text-[var(--primary-foreground)]"
                : "border border-border bg-card text-foreground hover:bg-muted"
            )}
          >
            {label}
          </button>
        ))}
        </div>

        <Button
          onClick={() => setAddOpen(true)}
          className="h-10 rounded-full px-4"
        >
          <Plus className="h-4 w-4" />
          {t("addCustomer")}
        </Button>
      </div>

      {/* Customer Cards */}
      {filtered.length === 0 ? (
        <div className="flex flex-col items-center gap-4 py-16">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-muted">
            <Users className="h-8 w-8 text-muted-foreground" />
          </div>
          <p className="text-base text-muted-foreground">{t("noCustomers")}</p>
        </div>
      ) : (
        <div className="flex flex-col gap-2">
          {filtered.map((customer) => (
            <div
              key={customer.id}
              className="flex items-center gap-2 rounded-xl border border-border bg-card p-2 shadow-sm"
            >
              <button
                onClick={() => onSelectCustomer(customer)}
                className="flex flex-1 items-center justify-between rounded-lg p-2 text-left transition-colors hover:bg-muted/60 active:scale-[0.99]"
              >
                <div className="flex flex-col gap-0.5">
                  <span className="text-base font-semibold text-foreground">{customer.name}</span>
                  <span className="text-sm text-muted-foreground">{customer.phone}</span>
                </div>
                <div className="flex items-center gap-2">
                  {customer.pending > 0 ? (
                    <span className="rounded-full bg-[var(--destructive)]/10 px-3 py-1 text-sm font-semibold text-[var(--destructive)]">
                      {"\u20B9"}{customer.pending.toLocaleString("en-IN")}
                    </span>
                  ) : (
                    <CheckCircle2 className="h-6 w-6 text-[var(--success)]" />
                  )}
                </div>
              </button>

              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button
                    variant="outline"
                    size="icon"
                    className="h-10 w-10 rounded-lg border-[var(--destructive)]/30 text-[var(--destructive)] hover:bg-[var(--destructive)]/10"
                    aria-label={`${t("delete")} ${customer.name}`}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>{t("deleteCustomer")}</AlertDialogTitle>
                    <AlertDialogDescription>
                      {customer.name} ({customer.phone})<br />
                      {t("deleteCustomerConfirm")}
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>{t("cancel")}</AlertDialogCancel>
                    <AlertDialogAction
                      className="bg-[var(--destructive)] text-white hover:bg-[var(--destructive)]/90"
                      onClick={() => deleteCustomer(customer.id)}
                    >
                      {t("delete")}
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          ))}
        </div>
      )}

      <Dialog open={addOpen} onOpenChange={setAddOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t("addCustomer")}</DialogTitle>
            <DialogDescription>{t("createCustomer")}</DialogDescription>
          </DialogHeader>
          <div className="flex flex-col gap-3">
            <Input
              placeholder={t("customerName")}
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <Input
              type="tel"
              inputMode="numeric"
              placeholder={t("enterPhone")}
              value={phone}
              onChange={(e) => setPhone(e.target.value.replace(/\D/g, ""))}
            />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setAddOpen(false)}>{t("cancel")}</Button>
            <Button onClick={handleAddCustomer} disabled={!name.trim() || !phone.trim()}>{t("createCustomer")}</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
