"use client"

import { Download, Clock, Wallet } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useLocale } from "@/lib/locale-context"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts"

const monthlyData = [
  { month: "Jan", credit: 4500, payment: 3200 },
  { month: "Feb", credit: 6200, payment: 4800 },
  { month: "Mar", credit: 3800, payment: 5100 },
  { month: "Apr", credit: 5100, payment: 3900 },
  { month: "May", credit: 7200, payment: 6000 },
  { month: "Jun", credit: 4800, payment: 4200 },
]

const trendData = [
  { month: "Jan", outstanding: 8200 },
  { month: "Feb", outstanding: 9600 },
  { month: "Mar", outstanding: 8300 },
  { month: "Apr", outstanding: 9500 },
  { month: "May", outstanding: 10700 },
  { month: "Jun", outstanding: 11300 },
]

export function ReportsPage() {
  const { t } = useLocale()

  return (
    <div className="flex flex-col gap-5 px-4 pb-28 pt-6">
      <h1 className="text-xl font-bold text-foreground">{t("reports")}</h1>

      {/* Credit vs Payment Bar Chart */}
      <div className="rounded-xl border border-border bg-card p-4 shadow-sm">
        <h2 className="mb-4 text-base font-semibold text-foreground">{t("creditVsPayment")}</h2>
        <div className="h-[220px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={monthlyData} barGap={4}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" />
              <XAxis
                dataKey="month"
                tick={{ fontSize: 12, fill: "var(--muted-foreground)" }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                tick={{ fontSize: 12, fill: "var(--muted-foreground)" }}
                axisLine={false}
                tickLine={false}
                width={45}
                tickFormatter={(v) => `${v / 1000}k`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "var(--card)",
                  border: "1px solid var(--border)",
                  borderRadius: "8px",
                  fontSize: "13px",
                  color: "var(--foreground)",
                }}
              />
              <Bar dataKey="credit" fill="var(--destructive)" radius={[4, 4, 0, 0]} name="Credit" />
              <Bar dataKey="payment" fill="var(--success)" radius={[4, 4, 0, 0]} name="Payment" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Outstanding Trend Line Chart */}
      <div className="rounded-xl border border-border bg-card p-4 shadow-sm">
        <h2 className="mb-4 text-base font-semibold text-foreground">{t("outstandingTrend")}</h2>
        <div className="h-[200px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" />
              <XAxis
                dataKey="month"
                tick={{ fontSize: 12, fill: "var(--muted-foreground)" }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                tick={{ fontSize: 12, fill: "var(--muted-foreground)" }}
                axisLine={false}
                tickLine={false}
                width={45}
                tickFormatter={(v) => `${v / 1000}k`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "var(--card)",
                  border: "1px solid var(--border)",
                  borderRadius: "8px",
                  fontSize: "13px",
                  color: "var(--foreground)",
                }}
              />
              <Line
                type="monotone"
                dataKey="outstanding"
                stroke="var(--accent)"
                strokeWidth={2.5}
                dot={{ fill: "var(--accent)", r: 4 }}
                name="Outstanding"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Summary Metrics */}
      <div className="grid grid-cols-2 gap-3">
        <div className="flex flex-col items-center gap-2 rounded-xl border border-border bg-card p-4 shadow-sm">
          <Clock className="h-6 w-6 text-[var(--primary)]" />
          <span className="text-xl font-bold text-foreground">12 {t("days")}</span>
          <span className="text-center text-xs text-muted-foreground">{t("avgRecoveryTime")}</span>
        </div>
        <div className="flex flex-col items-center gap-2 rounded-xl border border-border bg-card p-4 shadow-sm">
          <Wallet className="h-6 w-6 text-[var(--success)]" />
          <span className="text-xl font-bold text-foreground">{"\u20B9"}27,200</span>
          <span className="text-center text-xs text-muted-foreground">{t("monthlyCollection")}</span>
        </div>
      </div>

      {/* Export Buttons */}
      <div className="flex gap-3">
        <Button variant="outline" className="h-12 flex-1 rounded-xl text-sm">
          <Download className="mr-2 h-4 w-4" />
          {t("downloadPdf")}
        </Button>
        <Button variant="outline" className="h-12 flex-1 rounded-xl text-sm">
          <Download className="mr-2 h-4 w-4" />
          {t("downloadCsv")}
        </Button>
      </div>
    </div>
  )
}


 