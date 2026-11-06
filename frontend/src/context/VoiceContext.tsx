import React, { createContext, useReducer, useCallback, ReactNode } from 'react';
import type { Voice, VoiceContextType, VoiceAction } from '@/types/voice';

export const VoiceContext = createContext<VoiceContextType | undefined>(undefined);

const initialState: {
  voices: Voice[];
  isLoading: boolean;
  error: string | null;
  selectedVoice: Voice | null;
} = {
  voices: [],
  isLoading: false,
  error: null,
  selectedVoice: null,
};

function voiceReducer(state: typeof initialState, action: VoiceAction): typeof initialState {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'CLEAR_ERROR':
      return { ...state, error: null };
    case 'SET_VOICES':
      return { ...state, voices: action.payload };
    case 'ADD_VOICE':
      return { ...state, voices: [...state.voices, action.payload] };
    case 'DELETE_VOICE':
      return { ...state, voices: state.voices.filter((v) => v.id !== action.payload) };
    case 'UPDATE_VOICE':
      return {
        ...state,
        voices: state.voices.map((v) => (v.id === action.payload.id ? action.payload : v)),
        selectedVoice: state.selectedVoice?.id === action.payload.id ? action.payload : state.selectedVoice,
      };
    case 'SELECT_VOICE':
      return { ...state, selectedVoice: action.payload };
    default:
      return state;
  }
}

interface VoiceProviderProps {
  children: ReactNode;
}

export function VoiceProvider({ children }: VoiceProviderProps) {
  const [state, dispatch] = useReducer(voiceReducer, initialState);

  return <VoiceContext.Provider value={{ state, dispatch }}>{children}</VoiceContext.Provider>;
}
