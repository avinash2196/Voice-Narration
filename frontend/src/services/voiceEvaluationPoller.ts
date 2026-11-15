import type { EvaluationResult } from '@/types/voice';
import { VoiceAPI } from './voiceApi';

export class VoiceEvaluationPoller {
  private static pollingIntervals: Record<string, ReturnType<typeof setInterval>> = {};
  private static attemptCounts: Record<string, number> = {};

  static startPolling(
    voiceId: string,
    authToken: string,
    onUpdate: (result: EvaluationResult) => void,
    onComplete: (result: EvaluationResult) => void,
    onError: (error: string) => void
  ): void {
    // Cleanup any existing polling for this voice
    this.stopPolling(voiceId);

    this.attemptCounts[voiceId] = 0;
    const maxAttempts = 300; // ~10 minutes at 2-second intervals

    const poll = async () => {
      try {
        this.attemptCounts[voiceId]++;

        if (this.attemptCounts[voiceId] > maxAttempts) {
          onError('Evaluation timed out after 10 minutes');
          this.stopPolling(voiceId);
          return;
        }

        const result = await VoiceAPI.pollEvaluation(voiceId, authToken);
        onUpdate(result);

        if (result.status === 'ready' || result.status === 'error') {
          onComplete(result);
          this.stopPolling(voiceId);
        }
      } catch (error) {
        onError(error instanceof Error ? error.message : 'Polling failed');
      }
    };

    // Start initial poll immediately
    poll();

    // Then poll every 2 seconds
    this.pollingIntervals[voiceId] = setInterval(poll, 2000);
  }

  static stopPolling(voiceId: string): void {
    if (this.pollingIntervals[voiceId]) {
      clearInterval(this.pollingIntervals[voiceId]);
      delete this.pollingIntervals[voiceId];
    }
    delete this.attemptCounts[voiceId];
  }

  static getAttemptCount(voiceId: string): number {
    return this.attemptCounts[voiceId] || 0;
  }

  static isPolling(voiceId: string): boolean {
    return !!this.pollingIntervals[voiceId];
  }
}
