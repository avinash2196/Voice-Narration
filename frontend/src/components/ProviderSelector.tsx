import React, { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useTTS } from '@/hooks/useTTS';
import { ttsApi } from '@/services/ttsApi';
import { TTSProvider } from '@/types/tts';

export function ProviderSelector() {
  const auth = useAuth();
  const { selectedProvider, dispatch } = useTTS();
  const [providers, setProviders] = useState<TTSProvider[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProviders = async () => {
      if (!auth.token) return;

      setLoading(true);
      try {
        const availableProviders = await ttsApi.getAvailableProviders(auth.token);
        setProviders(availableProviders);

        // Set default to first available provider
        const defaultProvider = availableProviders.find((p) => p.available);
        if (defaultProvider && !selectedProvider) {
          dispatch({ type: 'SELECT_PROVIDER', payload: defaultProvider.id });
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch providers');
      } finally {
        setLoading(false);
      }
    };

    fetchProviders();
  }, [auth.token, dispatch, selectedProvider]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    dispatch({ type: 'SELECT_PROVIDER', payload: e.target.value });
  };

  if (loading) {
    return <div className="text-sm text-gray-500" data-testid="provider-loading">Loading providers...</div>;
  }

  if (error) {
    return <div className="text-sm text-red-600" data-testid="provider-error">{error}</div>;
  }

  if (providers.length === 0) {
    return (
      <div className="text-sm text-gray-500" data-testid="provider-empty">
        No providers available
      </div>
    );
  }

  return (
    <div className="w-full" data-testid="provider-selector-container">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Select TTS Provider
      </label>

      <div className="space-y-2">
        {providers.map((provider) => (
          <label
            key={provider.id}
            className={`flex items-center p-3 border rounded-lg cursor-pointer transition ${
              selectedProvider === provider.id
                ? 'bg-blue-50 border-blue-500'
                : 'border-gray-300 hover:border-gray-400'
            } ${!provider.available ? 'opacity-50 cursor-not-allowed' : ''}`}
            data-testid={`provider-option-${provider.id}`}
          >
            <input
              type="radio"
              name="provider"
              value={provider.id}
              checked={selectedProvider === provider.id}
              onChange={handleChange}
              disabled={!provider.available}
              className="mr-3"
              data-testid={`provider-radio-${provider.id}`}
            />

            <div className="flex-1">
              <p className="font-medium text-gray-900">{provider.name}</p>
              <p className="text-xs text-gray-600">
                Max {provider.maxCharsPerRequest} chars/request
              </p>
            </div>

            {!provider.available && (
              <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded">
                Unavailable
              </span>
            )}

            {provider.available && (
              <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                Available
              </span>
            )}
          </label>
        ))}
      </div>
    </div>
  );
}
