import React, { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useTTS } from '@/hooks/useTTS';
import { ttsApi } from '@/services/ttsApi';
import { TTSPollingService } from '@/services/ttsPollingService';
import { TextToSpeechInput } from './TextToSpeechInput';
import { VoiceSelector } from './VoiceSelector';
import { ProviderSelector } from './ProviderSelector';

export function GenerationSubmitForm() {
  const auth = useAuth();
  const {
    generationText,
    selectedVoice,
    selectedProvider,
    rateLimit,
    dispatch,
  } = useTTS();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const canSubmit =
    generationText.trim().length > 0 &&
    selectedVoice &&
    selectedProvider &&
    (!rateLimit || rateLimit.remaining > 0);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!canSubmit || !auth.token) return;

    setIsSubmitting(true);

    try {
      // Submit generation
      const generation = await ttsApi.submitGeneration(
        generationText,
        selectedVoice.id,
        selectedProvider,
        auth.token
      );

      dispatch({ type: 'START_GENERATION' });
      dispatch({ type: 'UPDATE_GENERATION', payload: generation });

      if (generation.status === 'ready') {
        dispatch({ type: 'GENERATION_COMPLETE', payload: generation });
        dispatch({ type: 'ADD_TO_HISTORY', payload: generation });
        return;
      }

      // Start polling for completion
      TTSPollingService.startPolling(generation.id, auth.token, {
        onProgress: (gen) => {
          dispatch({ type: 'UPDATE_GENERATION', payload: gen });
        },
        onComplete: (gen) => {
          dispatch({ type: 'GENERATION_COMPLETE', payload: gen });
          dispatch({ type: 'ADD_TO_HISTORY', payload: gen });
        },
        onError: (error) => {
          dispatch({ type: 'GENERATION_FAILED', payload: error });
        },
      }).catch((error) => {
        dispatch({
          type: 'GENERATION_FAILED',
          payload: error instanceof Error ? error.message : 'Generation failed',
        });
      });
    } catch (error) {
      dispatch({
        type: 'GENERATION_FAILED',
        payload: error instanceof Error ? error.message : 'Failed to submit generation',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const rateLimitPercentage = rateLimit
    ? Math.round((rateLimit.used / rateLimit.totalLimit) * 100)
    : 0;
  const rateLimitExceeded = rateLimit && rateLimit.remaining <= 0;

  return (
    <form onSubmit={handleSubmit} className="space-y-4" data-testid="generation-form">
      <TextToSpeechInput />

      <VoiceSelector />

      <ProviderSelector />

      {/* Rate Limit Display */}
      {rateLimit && (
        <div
          className={`p-3 rounded-lg ${
            rateLimitExceeded
              ? 'bg-red-50 border border-red-200'
              : rateLimitPercentage > 90
              ? 'bg-yellow-50 border border-yellow-200'
              : 'bg-blue-50 border border-blue-200'
          }`}
          data-testid="rate-limit-info"
        >
          <div className="flex justify-between items-center mb-1">
            <span className="text-sm font-medium text-gray-900">Rate Limit</span>
            <span className="text-sm font-semibold text-gray-900">
              {rateLimit.used} / {rateLimit.totalLimit}
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all ${
                rateLimitExceeded
                  ? 'bg-red-600'
                  : rateLimitPercentage > 90
                  ? 'bg-yellow-600'
                  : 'bg-green-600'
              }`}
              style={{ width: `${Math.min(rateLimitPercentage, 100)}%` }}
            />
          </div>
          {rateLimitPercentage > 90 && (
            <p className="text-xs text-red-600 mt-1">
              {rateLimitExceeded ? '❌ Quota exceeded' : '⚠️ Approaching quota limit'}
            </p>
          )}
        </div>
      )}

      <button
        type="submit"
        disabled={!canSubmit || isSubmitting}
        className={`w-full py-2 px-4 rounded-lg font-medium transition ${
          canSubmit && !isSubmitting
            ? 'bg-blue-600 text-white hover:bg-blue-700'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
        data-testid="generate-button"
      >
        {isSubmitting ? 'Generating...' : 'Generate Speech'}
      </button>
    </form>
  );
}
