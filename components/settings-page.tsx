"use client"

import { useState } from "react"
import { Store, Globe, MessageSquare, Database, Trash2, AlertTriangle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useLocale } from "@/lib/locale-context"
import { useAppState } from "@/lib/app-state"
import { cn } from "@/lib/utils"

export function SettingsPage() {
  const { t, locale, setLocale } = useLocale()
  const { shopName } = useAppState()
  const [shopNameInput, setShopNameInput] = useState(shopName)
  const [phoneInput, setPhoneInput] = useState("9876500000")
  const [smsTemplate, setSmsTemplate] = useState(
    locale === "ta"
      ? "வணக்கம் {name}, உங்களிடம் ₹{amount} பாக்கி உள்ளது. தயவுசெய்து செலுத்தவும்."
      : "Hello {name}, you have a pending amount of ₹{amount}. Please pay soon."
  )
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)

  return (
    <div className="flex flex-col gap-5 px-4 pb-28 pt-6">
      <h1 className="text-xl font-bold text-foreground">{t("settings")}</h1>

      {/* Shop Details */}
      <div className="rounded-xl border border-border bg-card p-4 shadow-sm">
        <div className="mb-4 flex items-center gap-2">
          <Store className="h-5 w-5 text-[var(--primary)]" />
          <h2 className="text-base font-semibold text-foreground">{t("shopDetails")}</h2>
        </div>
        <div className="flex flex-col gap-3">
          <div className="flex flex-col gap-1.5">
            <label className="text-sm text-muted-foreground">{t("shopName")}</label>
            <Input
              value={shopNameInput}
              onChange={(e) => setShopNameInput(e.target.value)}
              className="h-12 rounded-xl text-foreground"
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="text-sm text-muted-foreground">{t("phone")}</label>
            <Input
              type="tel"
              value={phoneInput}
              onChange={(e) => setPhoneInput(e.target.value)}
              className="h-12 rounded-xl text-foreground"
            />
          </div>
        </div>
      </div>

      {/* Language */}
      <div className="rounded-xl border border-border bg-card p-4 shadow-sm">
        <div className="mb-4 flex items-center gap-2">
          <Globe className="h-5 w-5 text-[var(--primary)]" />
          <h2 className="text-base font-semibold text-foreground">{t("language")}</h2>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setLocale("ta")}
            className={cn(
              "min-h-[48px] flex-1 rounded-xl border py-2 text-base font-medium transition-colors",
              locale === "ta"
                ? "border-[var(--primary)] bg-[var(--primary)]/10 text-[var(--primary)]"
                : "border-border bg-card text-foreground hover:bg-muted"
            )}
          >
            {"தமிழ்"}
          </button>
          <button
            onClick={() => setLocale("en")}
            className={cn(
              "min-h-[48px] flex-1 rounded-xl border py-2 text-base font-medium transition-colors",
              locale === "en"
                ? "border-[var(--primary)] bg-[var(--primary)]/10 text-[var(--primary)]"
                : "border-border bg-card text-foreground hover:bg-muted"
            )}
          >
            English
          </button>
        </div>
      </div>

      {/* SMS Template */}
      <div className="rounded-xl border border-border bg-card p-4 shadow-sm">
        <div className="mb-4 flex items-center gap-2">
          <MessageSquare className="h-5 w-5 text-[var(--primary)]" />
          <h2 className="text-base font-semibold text-foreground">{t("smsTemplate")}</h2>
        </div>
        <textarea
          value={smsTemplate}
          onChange={(e) => setSmsTemplate(e.target.value)}
          className="min-h-[100px] w-full rounded-xl border border-border bg-background p-3 text-sm leading-relaxed text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-[var(--ring)]"
          rows={3}
        />
      </div>

      {/* Data Management */}
      <div className="rounded-xl border border-border bg-card p-4 shadow-sm">
        <div className="mb-4 flex items-center gap-2">
          <Database className="h-5 w-5 text-[var(--primary)]" />
          <h2 className="text-base font-semibold text-foreground">{t("dataManagement")}</h2>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="h-12 flex-1 rounded-xl text-sm">
            {t("backup")}
          </Button>
          <Button variant="outline" className="h-12 flex-1 rounded-xl text-sm">
            {t("restore")}
          </Button>
        </div>
      </div>

      {/* Danger Zone */}
      <div className="rounded-xl border border-[var(--destructive)]/30 bg-card p-4 shadow-sm">
        <div className="mb-4 flex items-center gap-2">
          <AlertTriangle className="h-5 w-5 text-[var(--destructive)]" />
          <h2 className="text-base font-semibold text-[var(--destructive)]">{t("dangerZone")}</h2>
        </div>

        {!showDeleteConfirm ? (
          <Button
            variant="outline"
            onClick={() => setShowDeleteConfirm(true)}
            className="h-12 w-full rounded-xl border-[var(--destructive)]/30 text-sm text-[var(--destructive)] hover:bg-[var(--destructive)]/10"
          >
            <Trash2 className="mr-2 h-4 w-4" />
            {t("deleteAllData")}
          </Button>
        ) : (
          <div className="animate-in fade-in space-y-3 duration-200">
            <p className="text-center text-sm text-[var(--destructive)]">{t("deleteConfirm")}</p>
            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={() => setShowDeleteConfirm(false)}
                className="h-12 flex-1 rounded-xl text-sm"
              >
                {t("cancel")}
              </Button>
              <Button
                onClick={() => setShowDeleteConfirm(false)}
                className="h-12 flex-1 rounded-xl bg-[var(--destructive)] text-sm font-semibold text-[var(--destructive-foreground)] hover:bg-[var(--destructive)]/90"
              >
                {t("deleteAllData")}
              </Button>
            </div>
          </div>
        )}
      </div>

      {/* Save */}
      <Button className="h-12 w-full rounded-xl bg-[var(--primary)] text-base font-semibold text-[var(--primary-foreground)] hover:bg-[var(--primary)]/90">
        {t("save")}
      </Button>
    </div>
  )
}

# commit padding

# commit padding
 