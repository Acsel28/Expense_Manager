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

export default function DashboardPage() {
  const { user } = useAuthStore()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [recentExpenses, setRecentExpenses] = useState<Expense[]>([])
  const [loading, setLoading] = useState(true)

  // 🏢 Hardcoded company names
  const companyNames: Record<number, string> = {
    1: "Acme Corporation",
    2: "TechStart Inc",
  }

  const getCompanyName = (companyId: number) => companyNames[companyId] || "Unknown Company"

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      setLoading(true)
      const [statsRes, expensesRes] = await Promise.all([
        api.get("/expenses/stats"),
        api.get("/expenses?limit=5"),
      ])

      setStats(statsRes.data)
      setRecentExpenses(expensesRes.data)
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
      value: stats?.pending_count || 0,
      icon: Clock,
      color: "text-orange-500",
      bgColor: "bg-orange-500/10",
    },
    {
      title: "Approved Amount",
      value: `$${stats?.approved_amount?.toFixed(2) || "0.00"}`,
      icon: CheckCircle,
      color: "text-green-500",
      bgColor: "bg-green-500/10",
    },
    {
      title: "Total Expenses",
      value: stats?.total_expenses || 0,
      icon: FileText,
      color: "text-blue-500",
      bgColor: "bg-blue-500/10",
    },
    {
      title: "Total Amount",
      value: `$${stats?.total_amount?.toFixed(2) || "0.00"}`,
      icon: Users,
      color: "text-purple-500",
      bgColor: "bg-purple-500/10",
    },
  ]

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

        {/* Recent Activity */}
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
                  {recentExpenses.map((expense) => (
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
                        {/* 🏢 Show hardcoded company name */}
                        <p className="text-xs text-muted-foreground italic">
                          {getCompanyName(expense.company_id)}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold">${expense.amount.toFixed(2)}</p>
                        <p className="text-xs text-muted-foreground">
                          {new Date(expense.submitted_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                  ))}
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
