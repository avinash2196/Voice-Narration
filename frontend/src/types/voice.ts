export type VoiceStatus = 'pending' | 'approved' | 'rejected';

export interface Voice {
  id: string;
  name: string;
  format: 'MP3' | 'WAV' | 'OGG';
  provider?: 'google' | 'azure' | 'elevenlabs';
  language?: string;
  duration: number;
  fileSize: number;
  uploadedAt: string;
  status: VoiceStatus;
  approvalScore: number | null;
}

export interface VoiceContextType {
  state: {
    voices: Voice[];
    isLoading: boolean;
    error: string | null;
    selectedVoice: Voice | null;
  };
  dispatch: (action: VoiceAction) => void;
}

export type VoiceAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'ADD_VOICE'; payload: Voice }
  | { type: 'DELETE_VOICE'; payload: string }
  | { type: 'UPDATE_VOICE'; payload: Voice }
  | { type: 'SET_VOICES'; payload: Voice[] }
  | { type: 'SELECT_VOICE'; payload: Voice | null }
  | { type: 'CLEAR_ERROR' };

export interface UploadProgress {
  percentage: number;
  speed: number;
  timeRemaining: number;
}

export interface EvaluationResult {
  status: 'processing' | 'ready' | 'error';
  score: number | null;
  feedback: string | null;
  progress?: number;
}
