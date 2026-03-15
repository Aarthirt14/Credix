"use client"

import { useState } from "react"
import { Mic, Coffee } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useLocale } from "@/lib/locale-context"

interface LoginPageProps {
  onLogin: () => void
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const { t, locale, setLocale } = useLocale()
  const [phone, setPhone] = useState("")
  const [otpSent, setOtpSent] = useState(false)
  const [otp, setOtp] = useState("")
  const [error, setError] = useState("")
  const [isSending, setIsSending] = useState(false)

  function handleSendOtp() {
    if (phone.length < 10) return
    setIsSending(true)
    setTimeout(() => {
      setOtpSent(true)
      setIsSending(false)
    }, 800)
  }

  function handleVerify() {
    if (otp === "1234" || otp.length === 4) {
      setError("")
      onLogin()
    } else {
      setError(t("otpError"))
    }
  }

  return (
    <div className="flex min-h-dvh flex-col items-center justify-center bg-background px-6">
      <div className="w-full max-w-[360px] animate-in fade-in slide-in-from-bottom-4 duration-500">
        {/* Logo & Branding */}
        <div className="mb-10 flex flex-col items-center gap-3 text-center">
          <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-[var(--primary)] shadow-lg">
            <div className="relative">
              <Coffee className="h-9 w-9 text-[var(--primary-foreground)]" />
              <Mic className="absolute -bottom-1 -right-2 h-5 w-5 text-[var(--primary-foreground)]" />
            </div>
          </div>
          <h1 className="text-2xl font-bold text-foreground">{t("appName")}</h1>
          <p className="text-sm text-muted-foreground">{t("tagline")}</p>
        </div>

        {/* Phone Input */}
        <div className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="phone" className="sr-only">{t("phoneNumber")}</label>
            <Input
              id="phone"
              type="tel"
              inputMode="numeric"
              placeholder={t("phoneNumber")}
              value={phone}
              onChange={(e) => setPhone(e.target.value.replace(/\D/g, "").slice(0, 10))}
              className="h-14 rounded-xl border-border bg-card text-center text-lg tracking-widest text-foreground placeholder:text-muted-foreground placeholder:tracking-normal"
              maxLength={10}
              disabled={otpSent}
              autoComplete="tel"
            />
          </div>

          {!otpSent ? (
            <Button
              onClick={handleSendOtp}
              disabled={phone.length < 10 || isSending}
              className="h-14 w-full rounded-xl bg-[var(--primary)] text-base font-semibold text-[var(--primary-foreground)] hover:bg-[var(--primary)]/90"
            >
              {isSending ? t("loading") : t("getOtp")}
            </Button>
          ) : (
            <div className="animate-in fade-in slide-in-from-bottom-2 space-y-4 duration-300">
              <div className="space-y-2">
                <label htmlFor="otp" className="sr-only">{t("enterOtp")}</label>
                <Input
                  id="otp"
                  type="tel"
                  inputMode="numeric"
                  placeholder={t("enterOtp")}
                  value={otp}
                  onChange={(e) => {
                    setOtp(e.target.value.replace(/\D/g, "").slice(0, 4))
                    setError("")
                  }}
                  className="h-14 rounded-xl border-border bg-card text-center text-2xl tracking-[0.5em] text-foreground placeholder:text-base placeholder:tracking-normal"
                  maxLength={4}
                  autoFocus
                  autoComplete="one-time-code"
                />
              </div>

              {error && (
                <p className="text-center text-sm text-[var(--destructive)]" role="alert">{error}</p>
              )}

              <Button
                onClick={handleVerify}
                disabled={otp.length < 4}
                className="h-14 w-full rounded-xl bg-[var(--primary)] text-base font-semibold text-[var(--primary-foreground)] hover:bg-[var(--primary)]/90"
              >
                {t("verifyOtp")}
              </Button>
            </div>
          )}
        </div>

        {/* Language Toggle */}
        <div className="mt-8 flex justify-center">
          <button
            onClick={() => setLocale(locale === "ta" ? "en" : "ta")}
            className="min-h-[48px] rounded-full border border-border bg-card px-6 py-2 text-sm font-medium text-foreground transition-colors hover:bg-muted"
          >
            {locale === "ta" ? "English" : "தமிழ்"}
          </button>
        </div>
      </div>
    </div>
  )
}

# commit padding

# commit padding
 