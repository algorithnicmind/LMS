import { create } from 'zustand';

interface Modal {
  id: string;
  open: boolean;
}

interface UIState {
  modals: Modal[];
  openModal: (id: string) => void;
  closeModal: (id: string) => void;
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  modals: [],
  openModal: (id) => set((state) => ({ modals: [...state.modals.filter((m) => m.id !== id), { id, open: true }] })),
  closeModal: (id) => set((state) => ({ modals: state.modals.map((m) => (m.id === id ? { ...m, open: false } : m)) })),
  isSidebarOpen: false,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  setSidebarOpen: (open) => set({ isSidebarOpen: open }),
}));
