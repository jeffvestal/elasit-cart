'use client';

import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export interface GameItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
  store: string;
  category: string;
  image?: string;
}

export interface GameSession {
  sessionId: string;
  playerName: string;
  playerEmail: string;
  company?: string;
  accessCode: string;
  selectedAgent?: string;
  startTime?: Date;
  endTime?: Date;
  gameDuration?: number;
  totalPrice: number;
  targetPrice: number;
  score?: number;
  completed: boolean;
}

export interface Agent {
  id: string;
  name: string;
  description: string;
  personality: string;
  specialties: string[];
  avatar: string;
  color: string;
}

interface GameState {
  // Session management
  session: GameSession | null;
  isAuthenticated: boolean;
  
  // Game state
  currentItems: GameItem[];
  timeRemaining: number;
  gameStarted: boolean;
  gameEnded: boolean;
  isPlaying: boolean;
  
  // Agent selection
  availableAgents: Agent[];
  selectedAgent: Agent | null;
  
  // UI state
  showAgentSelector: boolean;
  showGameRules: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Leaderboard
  leaderboard: any[];
  
  // Actions
  setSession: (session: GameSession) => void;
  clearSession: () => void;
  setSelectedAgent: (agent: Agent) => void;
  addItem: (item: GameItem) => void;
  removeItem: (itemId: string) => void;
  updateItemQuantity: (itemId: string, quantity: number) => void;
  startGame: () => void;
  endGame: () => void;
  setTimeRemaining: (time: number) => void;
  setError: (error: string | null) => void;
  setLoading: (loading: boolean) => void;
  showRules: () => void;
  hideRules: () => void;
  showAgents: () => void;
  hideAgents: () => void;
  reset: () => void;
}

const MOCK_AGENTS: Agent[] = [
  {
    id: 'budget_master',
    name: 'Budget Master',
    description: 'Your savings expert who finds the best deals and maximizes value',
    personality: 'Enthusiastic about finding deals and stretching every dollar',
    specialties: ['Price comparisons', 'Store sales', 'Bulk discounts', 'Value optimization'],
    avatar: '💰',
    color: 'bg-green-500',
  },
  {
    id: 'health_guru',
    name: 'Health Guru',
    description: 'Wellness-focused companion for nutritious and balanced choices',
    personality: 'Knowledgeable about nutrition while staying budget-conscious',
    specialties: ['Nutrition facts', 'Dietary restrictions', 'Organic options', 'Seasonal produce'],
    avatar: '🥗',
    color: 'bg-emerald-500',
  },
  {
    id: 'gourmet_chef',
    name: 'Gourmet Chef',
    description: 'Culinary expert who creates amazing meal combinations',
    personality: 'Creative and inspiring about food possibilities',
    specialties: ['Recipe combinations', 'Premium ingredients', 'Meal planning', 'Flavor pairings'],
    avatar: '👨‍🍳',
    color: 'bg-orange-500',
  },
  {
    id: 'speed_shopper',
    name: 'Speed Shopper',
    description: 'Efficiency expert for quick, smart shopping decisions',
    personality: 'Fast-paced and decisive with proven winners',
    specialties: ['Popular items', 'Quick decisions', 'Time efficiency', 'Customer favorites'],
    avatar: '⚡',
    color: 'bg-blue-500',
  },
  {
    id: 'vegas_local',
    name: 'Vegas Local Expert',
    description: 'Las Vegas shopping insider with knowledge of local stores and deals',
    personality: 'Friendly local with insider tips and recommendations',
    specialties: ['Local stores', 'Vegas specialties', 'Store locations', 'Regional deals'],
    avatar: '🎰',
    color: 'bg-purple-500',
  },
];

export const useGameStore = create<GameState>()(
  devtools(
    (set, get) => ({
      // Initial state
      session: null,
      isAuthenticated: false,
      currentItems: [],
      timeRemaining: 300, // 5 minutes
      gameStarted: false,
      gameEnded: false,
      isPlaying: false,
      availableAgents: MOCK_AGENTS,
      selectedAgent: null,
      showAgentSelector: false,
      showGameRules: false,
      isLoading: false,
      error: null,
      leaderboard: [],

      // Actions
      setSession: (session) => set({ session, isAuthenticated: true }),
      
      clearSession: () => set({ 
        session: null, 
        isAuthenticated: false,
        currentItems: [],
        selectedAgent: null,
        gameStarted: false,
        gameEnded: false,
        isPlaying: false,
        timeRemaining: 300,
      }),

      setSelectedAgent: (agent) => set({ selectedAgent: agent }),

      addItem: (item) => set((state) => {
        const existingItem = state.currentItems.find(i => i.id === item.id);
        if (existingItem) {
          return {
            currentItems: state.currentItems.map(i =>
              i.id === item.id ? { ...i, quantity: i.quantity + item.quantity } : i
            )
          };
        }
        return { currentItems: [...state.currentItems, item] };
      }),

      removeItem: (itemId) => set((state) => ({
        currentItems: state.currentItems.filter(item => item.id !== itemId)
      })),

      updateItemQuantity: (itemId, quantity) => set((state) => ({
        currentItems: quantity <= 0
          ? state.currentItems.filter(item => item.id !== itemId)
          : state.currentItems.map(item =>
              item.id === itemId ? { ...item, quantity } : item
            )
      })),

      startGame: () => set({ 
        gameStarted: true, 
        isPlaying: true,
        gameEnded: false,
        timeRemaining: 300,
        currentItems: []
      }),

      endGame: () => set({ 
        gameEnded: true, 
        isPlaying: false 
      }),

      setTimeRemaining: (time) => set({ timeRemaining: time }),

      setError: (error) => set({ error }),

      setLoading: (loading) => set({ isLoading: loading }),

      showRules: () => set({ showGameRules: true }),
      hideRules: () => set({ showGameRules: false }),

      showAgents: () => set({ showAgentSelector: true }),
      hideAgents: () => set({ showAgentSelector: false }),

      reset: () => set({
        currentItems: [],
        timeRemaining: 300,
        gameStarted: false,
        gameEnded: false,
        isPlaying: false,
        selectedAgent: null,
        showAgentSelector: false,
        showGameRules: false,
        error: null,
      }),
    }),
    {
      name: 'game-store',
    }
  )
);
