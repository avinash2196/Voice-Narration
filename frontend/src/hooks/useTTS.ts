import { useContext } from 'react';
import { TTSContext } from '@/context/TTSContext';
import { TTSState, TTSAction } from '@/types/tts';

interface UseTTSReturn extends TTSState {
  dispatch: React.Dispatch<TTSAction>;
  isLoadingHistory: boolean;
}

export function useTTS(): UseTTSReturn {
  const context = useContext(TTSContext);

  if (context === undefined) {
    throw new Error('useTTS must be used within a TTSProvider');
  }

  return {
    ...context.state,
    dispatch: context.dispatch,
    isLoadingHistory: context.state.isLoadingHistory ?? false,
  };
}
