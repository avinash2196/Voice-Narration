import React, { useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useTTS } from '@/hooks/useTTS';
import { ttsApi } from '@/services/ttsApi';
import { GenerationSubmitForm } from '@/components/GenerationSubmitForm';
import { GenerationProgress } from '@/components/GenerationProgress';
import { GenerationErrorDisplay } from '@/components/GenerationErrorDisplay';
import { AudioPlayer } from '@/components/AudioPlayer';
import { GenerationHistory } from '@/components/GenerationHistory';
import { RateLimitDisplay } from '@/components/RateLimitDisplay';
import { QualityMetrics } from '@/components/QualityMetrics';

export function TextToSpeech() {
  const auth = useAuth();
  const { selectedProvider, currentGeneration, dispatch } = useTTS();
  const [audioUrl, setAudioUrl] = React.useState<string>();

  // Fetch rate limit on mount and when provider changes
  useEffect(() => {
    const fetchRateLimit = async () => {
      if (!auth.token || !selectedProvider) return;

      try {
        const limit = await ttsApi.getRateLimit(selectedProvider, auth.token);
        dispatch({ type: 'SET_RATE_LIMIT', payload: limit });
      } catch (error) {
        console.error('Failed to fetch rate limit:', error);
      }
    };

    fetchRateLimit();
  }, [auth.token, selectedProvider, dispatch]);

  // Load audio when generation is ready
  useEffect(() => {
    const loadAudio = async () => {
      if (!currentGeneration || currentGeneration.status !== 'ready' || !auth.token) {
        return;
      }

      try {
        const blob = await ttsApi.getGenerationAudio(currentGeneration.id, auth.token);
        const url = URL.createObjectURL(blob);
        setAudioUrl(url);
      } catch (error) {
        console.error('Failed to load audio:', error);
      }
    };

    loadAudio();
  }, [currentGeneration, auth.token]);

  return (
    <div className="min-h-screen bg-gray-100" data-testid="tts-page">
      <div className="max-w-4xl mx-auto py-8 px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Text to Speech</h1>
          <p className="text-gray-600">
            Convert your text into natural-sounding audio
          </p>
        </div>

        <div className="space-y-6">
          {/* Error Display */}
          <GenerationErrorDisplay />

          {/* Generation Form */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Generate Speech</h2>
            <GenerationSubmitForm />
          </div>

          {/* Rate Limit Display */}
          {selectedProvider && (
            <RateLimitDisplay provider={selectedProvider} />
          )}

          {/* Generation Progress */}
          {currentGeneration && (
            <GenerationProgress />
          )}

          {/* Audio Player */}
          {currentGeneration && audioUrl && (
            <AudioPlayer generation={currentGeneration} audioUrl={audioUrl} />
          )}

          {/* Quality Metrics */}
          {currentGeneration && (
            <QualityMetrics generation={currentGeneration} />
          )}

          {/* Generation History */}
          <div className="bg-white rounded-lg shadow p-6">
            <GenerationHistory />
          </div>
        </div>
      </div>
    </div>
  );
}
