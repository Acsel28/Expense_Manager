import { create } from "zustand"
import { persist } from "zustand/middleware"
import type { User } from "@/lib/types"

interface AuthState {
  user: User | null
  token: string | null
  setAuth: (user: User, token: string) => void
  logout: () => void
  isAuthenticated: () => boolean
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
  setAuth: (user, token) => {
    localStorage.setItem("token", token)
    if (user) {
      localStorage.setItem("user", JSON.stringify(user))
    }
    set({ user, token })
  },
      logout: () => {
        localStorage.removeItem("token")
        localStorage.removeItem("user")
        set({ user: null, token: null })
      },
      isAuthenticated: () => {
        return !!get().token
      },
    }),
    {
      name: "auth-storage",
    },
  ),
)
