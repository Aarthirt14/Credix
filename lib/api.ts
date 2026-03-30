const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1"
const DEMO_USERNAME = "demo_shopkeeper"
const DEMO_PASSWORD = "demoPassword123"
const TOKEN_KEY = "credit_api_token"

function buildLoopbackFallbackUrl(input: string): string | null {
  try {
    const url = new URL(input)
    const isLocalBackend =
      (url.hostname === "127.0.0.1" || url.hostname === "localhost") && url.port === "8000"

    if (!isLocalBackend) return null

    const fallback = new URL(input)
    fallback.hostname = url.hostname === "127.0.0.1" ? "localhost" : "127.0.0.1"
    return fallback.toString()
  } catch {
    return null
  }
}

interface AuthTokenResponse {
  access_token: string
  token_type: string
}

interface VoicePreviewItem {
  name: string
  qty: number
  price: number
}

interface VoicePreviewResponse {
  transcription: string
  normalized_text: string
  parsed?: {
    name?: string | null
    item?: string | null
    qty?: number | null
    amount?: number | null
    type?: string | null
    raw_text?: string
  }
  matched_customer_id: number | null
  matched_customer_name: string | null
  is_valid: boolean
  items: VoicePreviewItem[]
  calculated_total: number
  parsing_warnings: string[]
}

interface BackendCustomer {
  id: number
  name: string
  phone: string
  total_credit: number
  created_at: string
}

interface LocalCustomerInput {
  id: string
  name: string
  phone: string
}

function audioFileNameForType(contentType: string): string {
  const normalized = contentType.split(";", 1)[0].trim().toLowerCase()
  if (normalized.includes("wav")) return "recording.wav"
  if (normalized.includes("mp4") || normalized.includes("m4a")) return "recording.m4a"
  if (normalized.includes("ogg")) return "recording.ogg"
  if (normalized.includes("mpeg") || normalized.includes("mp3")) return "recording.mp3"
  return "recording.webm"
}

async function apiFetch(input: string, init?: RequestInit): Promise<Response> {
  try {
    return await fetch(input, init)
  } catch (error) {
    if (error instanceof TypeError) {
      const fallbackUrl = buildLoopbackFallbackUrl(input)
      if (fallbackUrl) {
        try {
          return await fetch(fallbackUrl, init)
        } catch {
          // Fall through to existing user-friendly message.
        }
      }
      throw new Error("Cannot reach backend API. Start backend on http://127.0.0.1:8000")
    }
    throw error
  }
}

function getStoredToken(): string | null {
  if (typeof window === "undefined") return null
  return window.localStorage.getItem(TOKEN_KEY)
}

function setStoredToken(token: string): void {
  if (typeof window === "undefined") return
  window.localStorage.setItem(TOKEN_KEY, token)
}

function clearStoredToken(): void {
  if (typeof window === "undefined") return
  window.localStorage.removeItem(TOKEN_KEY)
}

async function login(username: string, password: string): Promise<AuthTokenResponse> {
  const response = await apiFetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  })
  if (!response.ok) {
    throw new Error("Login failed")
  }
  return response.json() as Promise<AuthTokenResponse>
}

async function register(username: string, password: string): Promise<AuthTokenResponse> {
  const response = await apiFetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  })
  if (!response.ok) {
    throw new Error("Register failed")
  }
  return response.json() as Promise<AuthTokenResponse>
}

export async function ensureApiToken(): Promise<string> {
  const existing = getStoredToken()
  if (existing) return existing

  return getFreshApiToken()
}

async function getFreshApiToken(): Promise<string> {
  clearStoredToken()

  try {
    const loggedIn = await login(DEMO_USERNAME, DEMO_PASSWORD)
    setStoredToken(loggedIn.access_token)
    return loggedIn.access_token
  } catch {
    const registered = await register(DEMO_USERNAME, DEMO_PASSWORD)
    setStoredToken(registered.access_token)
    return registered.access_token
  }
}

async function authorizedFetch(path: string, init?: RequestInit): Promise<Response> {
  let token = await ensureApiToken()
  let response = await apiFetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      ...(init?.headers ?? {}),
      Authorization: `Bearer ${token}`,
    },
  })

  if (response.status !== 401) {
    return response
  }

  token = await getFreshApiToken()
  response = await apiFetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      ...(init?.headers ?? {}),
      Authorization: `Bearer ${token}`,
    },
  })
  return response
}

export async function previewVoiceTransaction(audioBlob: Blob, customerId?: number): Promise<VoicePreviewResponse> {
  const formData = new FormData()
  const contentType = audioBlob.type || "audio/webm"
  if (typeof customerId === "number") {
    formData.append("customer_id", String(customerId))
  }
  formData.append("audio", new File([audioBlob], audioFileNameForType(contentType), { type: contentType }))

  const response = await authorizedFetch("/voice-transaction", {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || "Voice processing failed")
  }

  return response.json() as Promise<VoicePreviewResponse>
}

export async function checkBackendHealth(): Promise<boolean> {
  const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1"
  const healthUrl = backendUrl.includes("/api/v1")
    ? backendUrl.replace(/\/api\/v1\/?$/, "/health")
    : `${backendUrl.replace(/\/$/, "")}/health`

  const response = await apiFetch(healthUrl, { method: "GET" })
  return response.ok
}

export async function confirmCreditTransaction(
  customerId: number,
  items: VoicePreviewItem[],
  transactionType: "credit" | "payment" = "credit"
): Promise<void> {
  const response = await authorizedFetch("/confirm-transaction", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ customer_id: customerId, items, transaction_type: transactionType }),
  })

  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || "Confirm transaction failed")
  }
}

async function fetchCustomers(): Promise<BackendCustomer[]> {
  const response = await authorizedFetch("/customers", {
    method: "GET",
  })
  if (!response.ok) {
    throw new Error("Failed to fetch customers")
  }
  return response.json() as Promise<BackendCustomer[]>
}

async function createCustomer(name: string, phone: string): Promise<BackendCustomer> {
  const response = await authorizedFetch("/customers", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, phone }),
  })
  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || "Failed to create customer")
  }
  return response.json() as Promise<BackendCustomer>
}

export async function ensureCustomersSynced(localCustomers: LocalCustomerInput[]): Promise<Record<string, number>> {
  const backendCustomers = await fetchCustomers()
  const byPhone = new Map<string, BackendCustomer>(
    backendCustomers.map((customer) => [customer.phone, customer])
  )

  for (const localCustomer of localCustomers) {
    if (!byPhone.has(localCustomer.phone)) {
      const created = await createCustomer(localCustomer.name, localCustomer.phone)
      byPhone.set(created.phone, created)
    }
  }

  const idMap: Record<string, number> = {}
  for (const localCustomer of localCustomers) {
    const backendCustomer = byPhone.get(localCustomer.phone)
    if (backendCustomer) {
      idMap[localCustomer.id] = backendCustomer.id
    }
  }

  return idMap
}
