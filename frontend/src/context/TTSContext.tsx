import React, { createContext, useReducer, ReactNode } from 'react';
import { TTSState, TTSAction } from '@/types/tts';
import { Voice } from '@/types/voice';

export const TTSContext = createContext<{
  state: TTSState;
  dispatch: React.Dispatch<TTSAction>;
} | undefined>(undefined);

const initialState: TTSState = {
  selectedVoice: null,
  selectedProvider: 'google',
  generationText: '',
  isGenerating: false,
  currentGeneration: null,
  generationHistory: [],
  error: null,
  rateLimit: null,
  isLoadingHistory: false,
};

function ttsReducer(state: TTSState, action: TTSAction): TTSState {
  switch (action.type) {
    case 'SET_TEXT':
      return { ...state, generationText: action.payload };

    case 'SELECT_VOICE':
      return { ...state, selectedVoice: action.payload };

    case 'SELECT_PROVIDER':
      return { ...state, selectedProvider: action.payload };

    case 'START_GENERATION':
      return { ...state, isGenerating: true, error: null };

    case 'UPDATE_GENERATION':
      return {
        ...state,
        currentGeneration: action.payload,
        generationText: '',
      };

    case 'GENERATION_COMPLETE':
      return {
        ...state,
        isGenerating: false,
        currentGeneration: action.payload,
        generationHistory: [action.payload, ...state.generationHistory],
      };

    case 'GENERATION_FAILED':
      return {
        ...state,
        isGenerating: false,
        error: action.payload,
        currentGeneration: null,
      };

    case 'ADD_TO_HISTORY':
      return {
        ...state,
        generationHistory: [action.payload, ...state.generationHistory],
      };

    case 'DELETE_FROM_HISTORY':
      return {
        ...state,
        generationHistory: state.generationHistory.filter(
          (g) => g.id !== action.payload
        ),
      };

    case 'SET_HISTORY':
      return { ...state, generationHistory: action.payload };

    case 'SET_LOADING_HISTORY':
      return { ...state, isLoadingHistory: action.payload };

    case 'CLEAR_ERROR':
      return { ...state, error: null };

    case 'SET_RATE_LIMIT':
      return { ...state, rateLimit: action.payload };

    case 'UPDATE_RATE_LIMIT':
      return { ...state, rateLimit: action.payload };

    default:
      return state;
  }
}

interface TTSProviderProps {
  children: ReactNode;
}

export function TTSProvider({ children }: TTSProviderProps) {
  const [state, dispatch] = useReducer(ttsReducer, initialState);

  return (
    <TTSContext.Provider value={{ state, dispatch }}>
      {children}
    </TTSContext.Provider>
  );
}
