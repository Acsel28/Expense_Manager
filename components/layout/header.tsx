"use client"

import { useRouter, usePathname } from "next/navigation"
import { LogOut, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { useAuthStore } from "@/store/auth-store"
import { toast } from "sonner"
import Link from "next/link"
import { motion } from "framer-motion"

const getBreadcrumbs = (pathname: string) => {
  const paths = pathname.split("/").filter(Boolean)
  const breadcrumbs = []

  const pathMap: Record<string, string> = {
    dashboard: "Dashboard",
  }

  // Always start with Home
  breadcrumbs.push({ name: "Home", href: "/dashboard" })

  paths.forEach((path, index) => {
    const href = `/${paths.slice(0, index + 1).join("/")}`
    breadcrumbs.push({
      name: pathMap[path] || path.charAt(0).toUpperCase() + path.slice(1),
      href,
    })
  })

  return breadcrumbs
}

export function Header() {
  const router = useRouter()
  const pathname = usePathname()
  const { user, logout } = useAuthStore()
  const breadcrumbs = getBreadcrumbs(pathname)

  const handleLogout = () => {
    logout()
    toast.success("Logged out successfully")
    router.push("/login")
  }

  const initials =
    user?.full_name
      ?.split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase() ||
    user?.email?.substring(0, 2).toUpperCase() ||
    "U"

  return (
    <header className="bg-card border-b border-border px-6 py-4 sticky top-0 z-10 backdrop-blur-sm bg-card/95">
      <div className="flex items-center justify-between mb-2">
        <nav className="flex items-center space-x-1 text-sm text-muted-foreground">
          {breadcrumbs.map((crumb, index) => (
            <motion.div
              key={`${crumb.href}-${index}`}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-center"
            >
              {index > 0 && <ChevronRight className="h-4 w-4 mx-1" />}
              {index === breadcrumbs.length - 1 ? (
                <span className="font-medium text-foreground">{crumb.name}</span>
              ) : (
                <Link href={crumb.href} className="hover:text-foreground transition-colors">
                  {crumb.name}
                </Link>
              )}
            </motion.div>
          ))}
        </nav>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="relative h-10 w-10 rounded-full">
              <Avatar>
                <AvatarFallback className="bg-primary text-primary-foreground">{initials}</AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuLabel>
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-medium">{user?.full_name || "User"}</p>
                <p className="text-xs text-muted-foreground">{user?.email}</p>
                <p className="text-xs text-muted-foreground capitalize">{user?.role}</p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleLogout}>
              <LogOut className="mr-2 h-4 w-4" />
              <span>Log out</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
        <h1 className="text-2xl font-bold">Welcome back, {user?.full_name?.split(" ")[0] || "User"}!</h1>
        <p className="text-sm text-muted-foreground">Manage your expenses and approvals</p>
      </motion.div>
    </header>
  )
}
