import { Voice } from './voice';

export interface TTSGeneration {
  id: string;
  text: string;
  voiceId: string;
  provider: 'google' | 'elevenlabs' | 'azure' | 'chatterbox';
  status: 'processing' | 'ready' | 'failed';
  audioFormat?: string;
  audioSize?: number;
  audioDuration?: number;
  quality?: number;
  createdAt: string;
  completedAt?: string | null;
  duration?: number;
  error?: string;
  progress?: number;
}

export interface TTSProvider {
  id: string;
  name: string;
  available: boolean;
}

// The languages a Chatterbox generation accepts (API-Contract.md, Inference Generation, `language`).
export type ChatterboxLanguage = 'en' | 'hi';

export interface RateLimit {
  provider: string;
  totalLimit: number;
  used: number;
  remaining: number;
  resetAt: string;
  percentageUsed: number;
}

export interface TTSState {
  selectedVoice: Voice | null;
  selectedProvider: string;
  selectedLanguage: ChatterboxLanguage;
  generationText: string;
  isGenerating: boolean;
  currentGeneration: TTSGeneration | null;
  generationHistory: TTSGeneration[];
  error: string | null;
  rateLimit: RateLimit | null;
  isLoadingHistory?: boolean;
}

export type TTSAction =
  | { type: 'SET_TEXT'; payload: string }
  | { type: 'SELECT_VOICE'; payload: Voice | null }
  | { type: 'SELECT_PROVIDER'; payload: string }
  | { type: 'SELECT_LANGUAGE'; payload: ChatterboxLanguage }
  | { type: 'START_GENERATION' }
  | { type: 'UPDATE_GENERATION'; payload: TTSGeneration }
  | { type: 'GENERATION_COMPLETE'; payload: TTSGeneration }
  | { type: 'GENERATION_FAILED'; payload: string }
  | { type: 'ADD_TO_HISTORY'; payload: TTSGeneration }
  | { type: 'DELETE_FROM_HISTORY'; payload: string }
  | { type: 'SET_HISTORY'; payload: TTSGeneration[] }
  | { type: 'SET_LOADING_HISTORY'; payload: boolean }
  | { type: 'CLEAR_ERROR' }
  | { type: 'SET_RATE_LIMIT'; payload: RateLimit }
  | { type: 'UPDATE_RATE_LIMIT'; payload: RateLimit };
