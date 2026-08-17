import { create } from 'zustand';
import api from '@/lib/api';
import type { User } from '@/types/user';

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string, password_confirm: string) => Promise<void>;
  logout: () => Promise<void>;
  fetchUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: true,
  isAuthenticated: false,

  login: async (email, password) => {
    await api.post('/api/v1/auth/token/', { email, password });
    const { data } = await api.get('/api/v1/users/me/');
    set({ user: data, isAuthenticated: true });
  },

  register: async (name, email, password, password_confirm) => {
    await api.post('/api/v1/auth/register/', { name, email, password, password_confirm });
    await api.post('/api/v1/auth/token/', { email, password });
    const { data } = await api.get('/api/v1/users/me/');
    set({ user: data, isAuthenticated: true });
  },

  logout: async () => {
    try {
      await api.post('/api/v1/auth/logout/');
    } catch {
      // Token may already be expired
    }
    set({ user: null, isAuthenticated: false });
  },

  fetchUser: async () => {
    try {
      set({ isLoading: true });
      const { data } = await api.get('/api/v1/users/me/');
      set({ user: data, isAuthenticated: true, isLoading: false });
    } catch {
      set({ user: null, isAuthenticated: false, isLoading: false });
    }
  },
}));
