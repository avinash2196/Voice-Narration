import { TTSGeneration } from '@/types/tts';
import { ttsApi } from './ttsApi';

interface PollingCallbacks {
  onProgress?: (generation: TTSGeneration) => void;
  onComplete?: (generation: TTSGeneration) => void;
  onError?: (error: string) => void;
}

interface PollingState {
  intervalId: ReturnType<typeof setInterval> | null;
  attempts: number;
}

const MAX_ATTEMPTS = 300; // ~10 minutes at 2s interval
const POLL_INTERVAL = 2000; // 2 seconds

export class TTSPollingService {
  private static pollingStates = new Map<string, PollingState>();

  static async startPolling(
    generationId: string,
    token: string,
    callbacks: PollingCallbacks = {}
  ): Promise<TTSGeneration> {
    // Clean up any existing polling for this generation
    this.stopPolling(generationId);

    const state: PollingState = {
      intervalId: null,
      attempts: 0,
    };

    return new Promise((resolve, reject) => {
      const poll = async () => {
        state.attempts++;

        try {
          const generation = await ttsApi.getGenerationStatus(generationId, token);

          callbacks.onProgress?.(generation);

          if (generation.status === 'ready') {
            callbacks.onComplete?.(generation);
            this.stopPolling(generationId);
            resolve(generation);
            return;
          }

          if (generation.status === 'failed') {
            const error = generation.error || 'Generation failed';
            callbacks.onError?.(error);
            this.stopPolling(generationId);
            reject(new Error(error));
            return;
          }

          if (state.attempts >= MAX_ATTEMPTS) {
            const timeoutError = 'Generation polling timeout';
            callbacks.onError?.(timeoutError);
            this.stopPolling(generationId);
            reject(new Error(timeoutError));
            return;
          }
        } catch (error) {
          const errorMsg = error instanceof Error ? error.message : 'Polling failed';
          callbacks.onError?.(errorMsg);
          this.stopPolling(generationId);
          reject(error);
        }
      };

      state.intervalId = setInterval(poll, POLL_INTERVAL);
      this.pollingStates.set(generationId, state);

      // Initial poll immediately
      poll();
    });
  }

  static stopPolling(generationId: string): void {
    const state = this.pollingStates.get(generationId);
    if (state?.intervalId) {
      clearInterval(state.intervalId);
    }
    this.pollingStates.delete(generationId);
  }

  static stopAllPolling(): void {
    this.pollingStates.forEach((state) => {
      if (state.intervalId) {
        clearInterval(state.intervalId);
      }
    });
    this.pollingStates.clear();
  }
}
