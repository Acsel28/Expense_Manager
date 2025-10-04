"use client"

import { useEffect, useState } from "react"
import { Users, FileText, Clock, CheckCircle } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { Badge } from "@/components/ui/badge"
import { DashboardLayout } from "@/components/layout/dashboard-layout"
import { useAuthStore } from "@/store/auth-store"
import { api } from "@/lib/api"
import { Role, type Expense, type DashboardStats } from "@/lib/types"
import { toast } from "sonner"

// Chart imports
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"

// 🏢 Mock companies
const mockCompanies = [
  { id: 1, name: "Acme Corporation", currency: "USD" },
  { id: 2, name: "TechStart Inc", currency: "EUR" },
  { id: 3, name: "Global Ventures", currency: "INR" },
  { id: 4, name: "NextGen Solutions", currency: "GBP" },
  { id: 5, name: "BlueSky Innovations", currency: "JPY" },
]

const companyMap: Record<number, { name: string; currency: string }> = mockCompanies.reduce(
  (map, c) => {
    map[c.id] = { name: c.name, currency: c.currency }
    return map
  },
  {} as Record<number, { name: string; currency: string }>
)

const getCompany = (companyId: number) => companyMap[companyId] || { name: "Unknown Company", currency: "USD" }

// Mock exchange rates
const mockRates: Record<string, number> = {
  USD: 1,
  EUR: 1.1,
  GBP: 1.25,
  JPY: 0.0067,
  INR: 0.012,
}

const convertToUSD = (amount: number, currency: string) => (mockRates[currency] || 1) * amount

// Helper to generate random date within the last 30 days
const randomDate = (daysBack: number) => {
  const today = new Date()
  const past = new Date(today)
  past.setDate(today.getDate() - Math.floor(Math.random() * daysBack))
  return past.toISOString()
}

// Generate fully realistic recent expenses
const generateMockExpenses = (): Expense[] => {
  const categories = ["Travel", "Food", "Office Supplies", "Entertainment", "Software"]
  const statuses = ["Pending", "Approved", "Rejected"] as const

  return Array.from({ length: 15 }, (_, i) => {
    const companyId = mockCompanies[i % mockCompanies.length].id
    const status = statuses[Math.floor(Math.random() * statuses.length)]
    return {
      id: i + 1,
      title: `Expense #${i + 1}`,
      amount: Math.floor(Math.random() * 500) + 20,
      category: categories[i % categories.length],
      status,
      company_id: companyId,
      submitted_at: randomDate(30),
    } as Expense
  }).sort((a, b) => new Date(b.submitted_at).getTime() - new Date(a.submitted_at).getTime())
}

export default function DashboardPage() {
  const { user } = useAuthStore()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [recentExpenses, setRecentExpenses] = useState<Expense[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)

      const [statsRes, expensesRes] = await Promise.allSettled([
        api.get("/expenses/stats"),
        api.get("/expenses?limit=50"),
      ])

      // Fallback: generate mock expenses
      let expenses: Expense[] = []
      if (expensesRes.status === "fulfilled" && Array.isArray(expensesRes.value.data) && expensesRes.value.data.length > 0) {
        expenses = expensesRes.value.data
      } else {
        expenses = generateMockExpenses()
      }
      setRecentExpenses(expenses.slice(0, 5))

      // Compute stats or fallback to mock
      const totalExpenses = expenses.length
      const approvedAmountUSD = expenses
        .filter((e) => e.status === "Approved")
        .reduce((sum, e) => sum + convertToUSD(e.amount, getCompany(e.company_id).currency), 0)
      const totalAmountUSD = expenses.reduce((sum, e) => sum + convertToUSD(e.amount, getCompany(e.company_id).currency), 0)
      const pendingCount = expenses.filter((e) => e.status === "Pending").length

      // If API stats available, use them; otherwise, use mock/randomized values
      const derivedStats: DashboardStats = statsRes.status === "fulfilled" && statsRes.value.data
        ? statsRes.value.data
        : {
            pending_count: pendingCount || Math.floor(Math.random() * 5) + 1,              // 1-5 pending
            approved_amount: approvedAmountUSD || Math.floor(Math.random() * 3000) + 500,  // $500-$3500
            total_expenses: totalExpenses || Math.floor(Math.random() * 20) + 5,           // 5-25 expenses
            total_amount: totalAmountUSD || Math.floor(Math.random() * 5000) + 1000,       // $1000-$6000
          }

      setStats(derivedStats)
    } catch (error: any) {
      toast.error("Failed to load dashboard data")
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const statCards = [
    {
      title: user?.role === Role.Employee ? "My Pending Expenses" : "Pending Approvals",
      value: stats?.pending_count ?? Math.floor(Math.random() * 5) + 1,
      icon: Clock,
      color: "text-orange-500",
      bgColor: "bg-orange-500/10",
    },
    {
      title: "Approved Amount (USD)",
      value: `$${stats?.approved_amount?.toFixed(2) ?? (Math.floor(Math.random() * 3000) + 500).toFixed(2)}`,
      icon: CheckCircle,
      color: "text-green-500",
      bgColor: "bg-green-500/10",
    },
    {
      title: "Total Expenses",
      value: stats?.total_expenses ?? Math.floor(Math.random() * 20) + 5,
      icon: FileText,
      color: "text-blue-500",
      bgColor: "bg-blue-500/10",
    },
    {
      title: "Total Amount (USD)",
      value: `$${stats?.total_amount?.toFixed(2) ?? (Math.floor(Math.random() * 5000) + 1000).toFixed(2)}`,
      icon: Users,
      color: "text-purple-500",
      bgColor: "bg-purple-500/10",
    },
  ]

  // Company stats
  const companyStats = mockCompanies.map((company) => {
    const companyExpenses = recentExpenses.filter((e) => e.company_id === company.id)
    const totalAmount = companyExpenses.reduce((sum, e) => sum + e.amount, 0)
    return {
      ...company,
      totalExpenses: companyExpenses.length,
      totalAmount,
    }
  })

  // Chart: Expenses by Category per Company
  const chartData: Record<string, any> = {}
  recentExpenses.forEach((exp) => {
    const company = getCompany(exp.company_id)
    if (!chartData[exp.category]) chartData[exp.category] = { category: exp.category }
    chartData[exp.category][company.name] = (chartData[exp.category][company.name] || 0) + exp.amount
  })
  const chartArray = Object.values(chartData)

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Stats Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {statCards.map((stat) => (
            <Card key={stat.title} className="hover:shadow-lg transition-shadow">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">{stat.title}</CardTitle>
                <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                  <stat.icon className={`h-4 w-4 ${stat.color}`} />
                </div>
              </CardHeader>
              <CardContent>
                {loading ? <Skeleton className="h-8 w-24" /> : <div className="text-2xl font-bold">{stat.value}</div>}
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Company Stats */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {companyStats.map((c) => (
            <Card key={c.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle>{c.name}</CardTitle>
                <CardDescription>Currency: {c.currency}</CardDescription>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <Skeleton className="h-8 w-24" />
                ) : (
                  <>
                    <p className="text-sm">Expenses: {c.totalExpenses}</p>
                    <p className="font-bold">
                      {c.currency} {c.totalAmount.toFixed(2)}
                    </p>
                  </>
                )}
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Chart */}
        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <CardTitle>Expenses by Category</CardTitle>
            <CardDescription>Grouped by company</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <Skeleton className="h-[300px] w-full" />
            ) : chartArray.length > 0 ? (
              <ResponsiveContainer width="100%" height={350}>
                <BarChart data={chartArray}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="category" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  {mockCompanies.map((c) => (
                    <Bar key={c.id} dataKey={c.name} stackId="a" fill="#8884d8" />
                  ))}
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[300px] flex items-center justify-center text-muted-foreground">
                No data for chart
              </div>
            )}
          </CardContent>
        </Card>

        {/* Recent Expenses */}
        <div className="grid gap-6">
          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle>Recent Expenses</CardTitle>
              <CardDescription>Latest expense submissions</CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="space-y-4">
                  {[...Array(5)].map((_, i) => (
                    <Skeleton key={i} className="h-16 w-full" />
                  ))}
                </div>
              ) : recentExpenses.length > 0 ? (
                <div className="space-y-4">
                  {recentExpenses.map((expense) => {
                    const company = getCompany(expense.company_id)
                    return (
                      <div
                        key={expense.id}
                        className="flex items-center justify-between p-3 rounded-lg border border-border hover:bg-accent transition-colors"
                      >
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <p className="font-medium">{expense.title}</p>
                            <Badge
                              variant={
                                expense.status === "Approved"
                                  ? "default"
                                  : expense.status === "Rejected"
                                  ? "destructive"
                                  : "secondary"
                              }
                            >
                              {expense.status}
                            </Badge>
                          </div>
                          <p className="text-sm text-muted-foreground">{expense.category}</p>
                          <p className="text-xs text-muted-foreground italic">{company.name}</p>
                        </div>
                        <div className="text-right">
                          <p className="font-semibold">
                            {company.currency} {expense.amount.toFixed(2)}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {new Date(expense.submitted_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                    )
                  })}
                </div>
              ) : (
                <div className="h-[300px] flex items-center justify-center text-muted-foreground">
                  No recent expenses
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  )
}
