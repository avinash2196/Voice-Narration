import React, { createContext, useReducer, ReactNode, useEffect } from 'react';
import type { User } from '../types/auth';
import { STORAGE_KEY_AUTH_TOKEN, STORAGE_KEY_REFRESH_TOKEN } from '../utils/constants';

export interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export type AuthAction =
  | { type: 'LOGIN'; payload: { user: User; token: string; refreshToken: string } }
  | { type: 'LOGOUT' }
  | { type: 'SET_ERROR'; payload: string }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'UPDATE_USER'; payload: User }
  | { type: 'RESTORE_SESSION'; payload: { user: User; token: string; refreshToken: string } }
  | { type: 'CLEAR_ERROR' }
  | { type: 'INIT_COMPLETE' };

export interface AuthContextType extends AuthState {
  dispatch: (action: AuthAction) => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

const initialState: AuthState = {
  user: null,
  token: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: true, // Start with true to show loading screen
  error: null,
};

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'LOGIN':
      localStorage.setItem(STORAGE_KEY_AUTH_TOKEN, action.payload.token);
      localStorage.setItem(STORAGE_KEY_REFRESH_TOKEN, action.payload.refreshToken);
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        refreshToken: action.payload.refreshToken,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };

    case 'LOGOUT':
      localStorage.removeItem(STORAGE_KEY_AUTH_TOKEN);
      localStorage.removeItem(STORAGE_KEY_REFRESH_TOKEN);
      return {
        ...state,
        user: null,
        token: null,
        refreshToken: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      };

    case 'SET_ERROR':
      return { ...state, error: action.payload, isLoading: false };

    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };

    case 'UPDATE_USER':
      return { ...state, user: action.payload };

    case 'RESTORE_SESSION':
      localStorage.setItem(STORAGE_KEY_AUTH_TOKEN, action.payload.token);
      localStorage.setItem(STORAGE_KEY_REFRESH_TOKEN, action.payload.refreshToken);
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        refreshToken: action.payload.refreshToken,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };

    case 'CLEAR_ERROR':
      return { ...state, error: null };

    case 'INIT_COMPLETE':
      return { ...state, isLoading: false };

    default:
      return state;
  }
}

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Session restoration on app load
  useEffect(() => {
    const restoreSession = async () => {
      try {
        const token = localStorage.getItem(STORAGE_KEY_AUTH_TOKEN);
        const refreshToken = localStorage.getItem(STORAGE_KEY_REFRESH_TOKEN);

        if (!token || !refreshToken) {
          // No token found, initialization complete
          dispatch({ type: 'INIT_COMPLETE' });
          return;
        }

        // Restore session from localStorage
        // In a real app, you would validate token with backend: GET /auth/me
        // For now, we restore the session if tokens exist
        const mockUser: User = {
          id: 'user-123',
          email: 'test@example.com',
          name: 'Test User',
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };

        dispatch({ 
          type: 'RESTORE_SESSION', 
          payload: { 
            user: mockUser, 
            token, 
            refreshToken 
          } 
        });
      } catch (error) {
        console.error('Session restoration failed:', error);
        localStorage.removeItem(STORAGE_KEY_AUTH_TOKEN);
        localStorage.removeItem(STORAGE_KEY_REFRESH_TOKEN);
        dispatch({ type: 'INIT_COMPLETE' });
      }
    };

    restoreSession();
  }, []);

  const value: AuthContextType = { ...state, dispatch };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

