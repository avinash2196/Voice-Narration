import React, { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useTTS } from '@/hooks/useTTS';
import { ttsApi } from '@/services/ttsApi';
import { Voice } from '@/types/voice';

export function VoiceSelector() {
  const auth = useAuth();
  const { selectedVoice, dispatch } = useTTS();
  const [voices, setVoices] = useState<Voice[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchVoices = async () => {
      if (!auth.token) return;

      setLoading(true);
      try {
        const approvedVoices = await ttsApi.getApprovedVoices(auth.token);
        const providerVoices = approvedVoices.filter((voice) => {
          const voiceId = (voice.id || '').trim();
          const provider = (voice as any).provider?.toLowerCase?.() || '';
          const isGoogleId = /^[a-z]{2,3}-[A-Z]{2,}[-A-Za-z0-9]+$/.test(voiceId);
          return provider === 'google' || isGoogleId;
        });

        const validVoices = providerVoices.length > 0 ? providerVoices : approvedVoices.filter((voice) => {
          const voiceId = (voice.id || '').trim();
          return /^[a-z]{2,3}-[A-Z]{2,}[-A-Za-z0-9]+$/.test(voiceId);
        });

        setVoices(validVoices.length > 0 ? validVoices : approvedVoices);

        const currentValidSelection = validVoices.some((voice) => voice.id === selectedVoice?.id);

        if (validVoices.length > 0 && (!selectedVoice || !currentValidSelection)) {
          dispatch({ type: 'SELECT_VOICE', payload: validVoices[0] });
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch voices');
      } finally {
        setLoading(false);
      }
    };

    fetchVoices();
  }, [auth.token, dispatch, selectedVoice]);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const voiceId = e.target.value;
    const voice = voices.find((v) => v.id === voiceId);
    if (voice) {
      dispatch({ type: 'SELECT_VOICE', payload: voice });
    }
  };

  if (loading) {
    return <div className="text-sm text-gray-500" data-testid="voice-selector-loading">Loading voices...</div>;
  }

  if (error) {
    return <div className="text-sm text-red-600" data-testid="voice-selector-error">{error}</div>;
  }

  if (voices.length === 0) {
    return (
      <div className="text-sm text-gray-500" data-testid="voice-selector-empty">
        No approved voices available
      </div>
    );
  }

  return (
    <div className="w-full" data-testid="voice-selector-container">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Select Voice ({voices.length} available)
      </label>

      <select
        value={selectedVoice?.id || ''}
        onChange={handleChange}
        className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        data-testid="voice-select"
      >
        <option value="">-- Choose a voice --</option>
        {voices.map((voice) => (
          <option key={voice.id} value={voice.id}>
            {voice.name} ({(voice as any).language || 'unknown'})
          </option>
        ))}
      </select>

      {selectedVoice && (
        <div className="mt-2 p-2 bg-blue-50 border border-blue-200 rounded text-sm" data-testid="voice-selected-info">
          <p className="text-gray-700">
            <span className="font-semibold">Selected:</span> {selectedVoice.name}
          </p>
        </div>
      )}
    </div>
  );
}
