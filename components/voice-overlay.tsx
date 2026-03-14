"use client"

import { useState, useEffect, useCallback, useRef } from "react"
import { Mic, X, Check, Pencil } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useLocale } from "@/lib/locale-context"
import { useAppState, type Customer } from "@/lib/app-state"
import { cn } from "@/lib/utils"
import { confirmCreditTransaction, ensureCustomersSynced, previewVoiceTransaction } from "@/lib/api"

interface VoiceOverlayProps {
  open: boolean
  onClose: () => void
}

type OverlayState = "listening" | "processing" | "preview" | "success"

interface ParsedCommand {
  customerName: string
  amount: number
  type: "credit" | "payment"
  matchedCustomer: Customer | null
  items: { name: string; qty: number; price: number }[]
}

const TAMIL_TO_LATIN: Record<string, string> = {
  "அ": "a", "ஆ": "aa", "இ": "i", "ஈ": "ii", "உ": "u", "ஊ": "uu", "எ": "e", "ஏ": "ee", "ஐ": "ai", "ஒ": "o", "ஓ": "oo", "ஔ": "au",
  "க": "k", "ங": "ng", "ச": "s", "ஜ": "j", "ஞ": "ny", "ட": "t", "ண": "n", "த": "th", "ந": "n", "ப": "p", "ம": "m", "ய": "y", "ர": "r", "ல": "l", "வ": "v", "ழ": "zh", "ள": "l", "ற": "r", "ன": "n",
  "ா": "aa", "ி": "i", "ீ": "ii", "ு": "u", "ூ": "uu", "ெ": "e", "ே": "ee", "ை": "ai", "ொ": "o", "ோ": "oo", "ௌ": "au", "்": "",
}

function transliterateTamil(input: string): string {
  return Array.from(input).map((char) => TAMIL_TO_LATIN[char] ?? char).join("")
}

function normalizeName(input: string): string {
  return transliterateTamil(input)
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .replace(/\s+/g, " ")
    .trim()
}

function phoneticKey(input: string): string {
  return normalizeName(input)
    .replace(/[aeiou]/g, "")
    .replace(/(.)\1+/g, "$1")
}

export function VoiceOverlay({ open, onClose }: VoiceOverlayProps) {
  const { t } = useLocale()
  const { customers, addTransaction } = useAppState()
  const [state, setState] = useState<OverlayState>("listening")
  const [transcription, setTranscription] = useState("")
  const [parsed, setParsed] = useState<ParsedCommand | null>(null)
  const [waveAmplitudes, setWaveAmplitudes] = useState<number[]>(Array(20).fill(0.3))
  const [error, setError] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [backendCustomerMap, setBackendCustomerMap] = useState<Record<string, number>>({})

  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const mediaStreamRef = useRef<MediaStream | null>(null)

  const getPreferredMimeType = useCallback((): string => {
    const candidates = [
      "audio/webm;codecs=opus",
      "audio/webm",
      "audio/mp4",
      "audio/ogg;codecs=opus",
      "audio/ogg",
    ]

    return candidates.find((mime) => MediaRecorder.isTypeSupported(mime)) ?? ""
  }, [])

  const reset = useCallback(() => {
    setState("listening")
    setTranscription("")
    setParsed(null)
    setError("")
    setIsRecording(false)
  }, [])

  const inferCustomerFromText = useCallback(
    (text: string): Customer | null => {
      const lowered = text.toLowerCase()
      const exact = customers.find((customer) => lowered.includes(customer.name.toLowerCase()))
      if (exact) return exact

      const normalizedText = normalizeName(text)
      const normalizedKey = phoneticKey(text)
      const tokenKeys = normalizedText
        .split(" ")
        .map((token) => phoneticKey(token))
        .filter((token) => token.length >= 2)

      let bestMatch: Customer | null = null
      let bestScore = 0

      for (const customer of customers) {
        const normalizedCustomer = normalizeName(customer.name)
        const customerKey = phoneticKey(customer.name)

        if (!normalizedCustomer || !customerKey) continue

        let score = 0
        if (normalizedText.includes(normalizedCustomer)) score = Math.max(score, 4)
        if (normalizedCustomer.includes(normalizedText) && normalizedText.length >= 3) score = Math.max(score, 2)
        if (normalizedKey.includes(customerKey) || customerKey.includes(normalizedKey)) score = Math.max(score, 3)
        if (tokenKeys.some((token) => token === customerKey || token.includes(customerKey) || customerKey.includes(token))) {
          score = Math.max(score, 3)
        }

        if (score > bestScore) {
          bestScore = score
          bestMatch = customer
        }
      }

      return bestMatch
    },
    [customers]
  )

  const ensureCustomerMap = useCallback(async (): Promise<Record<string, number>> => {
    if (Object.keys(backendCustomerMap).length > 0) {
      return backendCustomerMap
    }

    const mapping = await ensureCustomersSynced(
      customers.map((customer) => ({
        id: customer.id,
        name: customer.name,
        phone: customer.phone,
      }))
    )
    setBackendCustomerMap(mapping)
    return mapping
  }, [backendCustomerMap, customers])

  const processRecording = useCallback(
    async (audioBlob: Blob) => {
      if (!customers.length) {
        setError("No customers available")
        return
      }

      setState("processing")
      setError("")

      try {
        const customerMap = await ensureCustomerMap()
        const fallbackCustomerId = customerMap[customers[0].id]
        if (!fallbackCustomerId) {
          throw new Error("No backend customers available")
        }
        const preview = await previewVoiceTransaction(fallbackCustomerId, audioBlob)
        const matchText = `${preview.transcription} ${preview.items.map((item) => item.name).join(" ")}`
        const matched = inferCustomerFromText(matchText)

        setTranscription(preview.transcription)
        setParsed({
          customerName: matched?.name || "Unknown",
          amount: Number(preview.calculated_total),
          type: "credit",
          matchedCustomer: matched,
          items: preview.items,
        })
        setState("preview")
      } catch (processingError) {
        setError(processingError instanceof Error ? processingError.message : "Voice processing failed")
        setState("listening")
      }
    },
    [customers, ensureCustomerMap, inferCustomerFromText]
  )

  const stopRecording = useCallback(() => {
    const recorder = mediaRecorderRef.current
    if (recorder && recorder.state !== "inactive") {
      try {
        recorder.requestData()
      } catch {
      }
      recorder.stop()
    }
  }, [])

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaStreamRef.current = stream
      const preferredMimeType = getPreferredMimeType()
      const recorder = preferredMimeType
        ? new MediaRecorder(stream, { mimeType: preferredMimeType })
        : new MediaRecorder(stream)
      const chunks: BlobPart[] = []

      recorder.ondataavailable = (event: BlobEvent) => {
        if (event.data.size > 0) {
          chunks.push(event.data)
        }
      }

      recorder.onstop = async () => {
        setIsRecording(false)
        mediaRecorderRef.current = null
        mediaStreamRef.current?.getTracks().forEach((track) => track.stop())
        mediaStreamRef.current = null

        if (!chunks.length) {
          setError("No audio captured. Please record for at least 1 second.")
          return
        }

        const audioBlob = new Blob(chunks, { type: recorder.mimeType || preferredMimeType || "audio/webm" })
        await processRecording(audioBlob)
      }

      mediaRecorderRef.current = recorder
      setIsRecording(true)
      recorder.start(250)
    } catch {
      setError("Microphone permission denied")
    }
  }, [getPreferredMimeType, processRecording])

  // Animate waveform during listening
  useEffect(() => {
    if (!open || state !== "listening") return
    const interval = setInterval(() => {
      setWaveAmplitudes(
        Array.from({ length: 20 }, () => 0.2 + Math.random() * 0.8)
      )
    }, 120)
    return () => clearInterval(interval)
  }, [open, state])

  useEffect(() => {
    if (!open) {
      stopRecording()
      mediaStreamRef.current?.getTracks().forEach((track) => track.stop())
      mediaStreamRef.current = null
      reset()
      return
    }
    void startRecording()
    return () => {
      stopRecording()
      mediaStreamRef.current?.getTracks().forEach((track) => track.stop())
      mediaStreamRef.current = null
    }
  }, [open, reset, startRecording, stopRecording])

  async function handleConfirm() {
    if (!parsed?.matchedCustomer || !parsed.items.length) return
    setIsSubmitting(true)
    setError("")
    try {
      const customerMap = await ensureCustomerMap()
      const backendCustomerId = customerMap[parsed.matchedCustomer.id]
      if (!backendCustomerId) {
        throw new Error("Matched customer not found in backend")
      }
      await confirmCreditTransaction(backendCustomerId, parsed.items)
      addTransaction(parsed.matchedCustomer.id, "credit", parsed.amount)
      setState("success")
      setTimeout(() => {
        onClose()
      }, 1800)
    } catch (confirmError) {
      setError(confirmError instanceof Error ? confirmError.message : "Unable to confirm transaction")
    } finally {
      setIsSubmitting(false)
    }
  }

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-foreground/60 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative mx-4 w-full max-w-[400px] overflow-hidden rounded-2xl bg-card shadow-2xl animate-in zoom-in-95 duration-300">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute right-3 top-3 flex h-10 w-10 items-center justify-center rounded-full text-muted-foreground transition-colors hover:bg-muted"
          aria-label={t("cancel")}
        >
          <X className="h-5 w-5" />
        </button>

        <div className="p-6 pt-14">
          {state === "listening" && (
            <div className="flex flex-col items-center gap-6">
              {/* Listening indicator */}
              <div className="relative">
                <div className="flex h-20 w-20 items-center justify-center rounded-full bg-[var(--primary)]">
                  <Mic className="h-8 w-8 text-[var(--primary-foreground)] animate-pulse" />
                </div>
                <div className="absolute inset-0 animate-ping rounded-full bg-[var(--primary)] opacity-20" />
              </div>

              <p className="text-lg font-semibold text-foreground">{t("listening")}</p>

              {/* Transcription */}
              <div className="min-h-[48px] w-full text-center">
                <p className="text-xl font-medium text-foreground">{transcription || t("listening")}</p>
              </div>

              {/* Waveform */}
              <div className="flex h-12 items-end justify-center gap-1">
                {waveAmplitudes.map((amp, i) => (
                  <div
                    key={i}
                    className="w-1.5 rounded-full bg-[var(--primary)] transition-all duration-100"
                    style={{ height: `${amp * 48}px`, opacity: 0.4 + amp * 0.6 }}
                  />
                ))}
              </div>

              <Button
                onClick={stopRecording}
                disabled={!isRecording}
                className="h-12 w-full rounded-xl bg-[var(--destructive)] text-sm font-semibold text-[var(--destructive-foreground)] hover:bg-[var(--destructive)]/90"
              >
                Stop recording
              </Button>
            </div>
          )}

          {state === "processing" && (
            <div className="flex flex-col items-center gap-4 py-8">
              <p className="text-base font-semibold text-foreground">Processing audio...</p>
            </div>
          )}

          {state === "preview" && parsed && (
            <div className="flex flex-col gap-5 animate-in fade-in slide-in-from-bottom-2 duration-300">
              <h3 className="text-center text-lg font-semibold text-foreground">
                {transcription}
              </h3>

              {/* Parsed data card */}
              <div className="rounded-xl border border-border bg-muted/50 p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">{t("customer")}</span>
                  <span className="text-base font-semibold text-foreground">{parsed.customerName}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">{t("amount")}</span>
                  <span className="text-base font-semibold text-foreground">
                    {"\u20B9"}{parsed.amount}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">{t("type")}</span>
                  <span
                    className={cn(
                      "rounded-full px-3 py-0.5 text-sm font-medium",
                      parsed.type === "credit"
                        ? "bg-[var(--destructive)]/10 text-[var(--destructive)]"
                        : "bg-[var(--success)]/10 text-[var(--success)]"
                    )}
                  >
                    {t(parsed.type)}
                  </span>
                </div>
              </div>

              {/* Action buttons */}
              <div className="flex gap-3">
                <Button
                  variant="outline"
                  onClick={onClose}
                  className="h-12 flex-1 rounded-xl text-sm"
                >
                  {t("cancel")}
                </Button>
                <Button
                  variant="outline"
                  className="h-12 rounded-xl px-4 text-sm"
                >
                  <Pencil className="mr-1 h-4 w-4" />
                  {t("edit")}
                </Button>
                <Button
                  onClick={handleConfirm}
                  disabled={!parsed.matchedCustomer || isSubmitting}
                  className="h-12 flex-1 rounded-xl bg-[var(--primary)] text-sm font-semibold text-[var(--primary-foreground)] hover:bg-[var(--primary)]/90"
                >
                  <Check className="mr-1 h-4 w-4" />
                  {t("confirm")}
                </Button>
              </div>
            </div>
          )}

          {error && (
            <p className="mt-4 text-center text-sm text-[var(--destructive)]">{error}</p>
          )}

          {state === "success" && (
            <div className="flex flex-col items-center gap-4 py-4 animate-in zoom-in-50 duration-300">
              <div className="flex h-20 w-20 items-center justify-center rounded-full bg-[var(--success)]">
                <Check className="h-10 w-10 text-[var(--success-foreground)]" />
              </div>
              <p className="text-lg font-semibold text-foreground">{t("success")}</p>
              <p className="text-sm text-muted-foreground">
                {parsed?.type === "credit" ? t("creditAdded") : t("paymentAdded")}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
