export enum Role {
  Admin = "Admin",
  Manager = "Manager",
  Employee = "Employee",
}

export enum ExpenseStatus {
  Pending = "Pending",
  Approved = "Approved",
  Rejected = "Rejected",
}

export interface User {
  id: number
  email: string
  role: Role
  company_id: number
  manager_id?: number
  full_name?: string
}

export interface Company {
  id: number
  name: string
  currency: string
  created_at: string
}

export interface Expense {
  id: number
  title: string
  amount: number
  category: string
  description?: string
  receipt_url?: string
  status: ExpenseStatus
  user_id: number
  company_id: number
  manager_id?: number
  submitted_at: string
  reviewed_at?: string
  created_at: string
  submitted_by?: User
  approved_by?: User
}

export interface DashboardStats {
  total_expenses: number
  pending_count: number
  approved_count: number
  rejected_count: number
  total_amount: number
  approved_amount: number
}
