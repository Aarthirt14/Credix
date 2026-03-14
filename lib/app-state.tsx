"use client"

import { createContext, useContext, useState, type ReactNode } from "react"

export interface Transaction {
  id: string
  customerId: string
  type: "credit" | "payment"
  amount: number
  date: string
  note?: string
}

export interface Customer {
  id: string
  name: string
  phone: string
  pending: number
  transactions: Transaction[]
}

interface AppState {
  shopName: string
  isLoggedIn: boolean
  customers: Customer[]
  setLoggedIn: (v: boolean) => void
  addCustomer: (name: string, phone: string) => void
  deleteCustomer: (customerId: string) => void
  addTransaction: (customerId: string, type: "credit" | "payment", amount: number, note?: string) => void
}

const AppContext = createContext<AppState | undefined>(undefined)

const initialCustomers: Customer[] = [
  {
    id: "1",
    name: "Ravi",
    phone: "9876543210",
    pending: 450,
    transactions: [
      { id: "t1", customerId: "1", type: "credit", amount: 450, date: "2026-03-01", note: "Tea supplies" },
    ],
  },
  {
    id: "2",
    name: "Kumar",
    phone: "9876543211",
    pending: 1200,
    transactions: [
      { id: "t4", customerId: "2", type: "credit", amount: 1200, date: "2026-03-02" },
    ],
  },
  {
    id: "3",
    name: "Lakshmi",
    phone: "9876543212",
    pending: 0,
    transactions: [],
  },
  {
    id: "4",
    name: "Murugan",
    phone: "9876543213",
    pending: 800,
    transactions: [
      { id: "t7", customerId: "4", type: "credit", amount: 800, date: "2026-03-01" },
    ],
  },
  {
    id: "5",
    name: "Saravanan",
    phone: "9876543214",
    pending: 0,
    transactions: [],
  },
]

export function AppProvider({ children }: { children: ReactNode }) {
  const [isLoggedIn, setLoggedIn] = useState(false)
  const [customers, setCustomers] = useState<Customer[]>(initialCustomers)
  const shopName = "அருண் டீ ஸ்டால்"

  function addCustomer(name: string, phone: string) {
    const newCustomer: Customer = {
      id: Date.now().toString(),
      name,
      phone,
      pending: 0,
      transactions: [],
    }
    setCustomers((prev) => [...prev, newCustomer])
  }

  function deleteCustomer(customerId: string) {
    setCustomers((prev) => prev.filter((customer) => customer.id !== customerId))
  }

  function addTransaction(customerId: string, type: "credit" | "payment", amount: number, note?: string) {
    setCustomers((prev) =>
      prev.map((c) => {
        if (c.id !== customerId) return c
        const newTx: Transaction = {
          id: `t${Date.now()}`,
          customerId,
          type,
          amount,
          date: new Date().toISOString().split("T")[0],
          note,
        }
        return {
          ...c,
          pending: type === "credit" ? c.pending + amount : Math.max(0, c.pending - amount),
          transactions: [newTx, ...c.transactions],
        }
      })
    )
  }

  return (
    <AppContext.Provider
      value={{ shopName, isLoggedIn, customers, setLoggedIn, addCustomer, deleteCustomer, addTransaction }}
    >
      {children}
    </AppContext.Provider>
  )
}

export function useAppState() {
  const context = useContext(AppContext)
  if (!context) throw new Error("useAppState must be used within AppProvider")
  return context
}
