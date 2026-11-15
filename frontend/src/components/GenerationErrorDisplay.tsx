import React from 'react';
import { useTTS } from '@/hooks/useTTS';

export function GenerationErrorDisplay() {
  const { error, dispatch } = useTTS();

  if (!error) {
    return null;
  }

  const getErrorCode = () => {
    if (error.includes('400')) return 'BAD_REQUEST';
    if (error.includes('401')) return 'UNAUTHORIZED';
    if (error.includes('429')) return 'RATE_LIMITED';
    if (error.includes('500')) return 'SERVER_ERROR';
    return 'UNKNOWN_ERROR';
  };

  const getSuggestion = () => {
    if (error.includes('Rate limited') || error.includes('429')) {
      return 'Try a different provider or wait for quota reset.';
    }
    if (error.includes('not approved') || error.includes('invalid voice')) {
      return 'Please select a valid voice from the approved list.';
    }
    if (error.includes('provider')) {
      return 'The selected provider is unavailable. Try another one.';
    }
    return 'Please try again or contact support.';
  };

  const handleDismiss = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const handleRetry = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  return (
    <div
      className="p-4 bg-red-50 border border-red-300 rounded-lg"
      data-testid="error-display"
    >
      <div className="flex items-start gap-3">
        <span className="text-2xl">❌</span>
        <div className="flex-1">
          <h3 className="font-semibold text-red-900 mb-1">Generation Failed</h3>

          <p className="text-sm text-red-700 mb-2">{error}</p>

          <p className="text-xs text-red-600 mb-3">
            <span className="font-semibold">Error Code:</span> {getErrorCode()}
          </p>

          <p className="text-sm text-red-800 mb-3">
            <span className="font-semibold">Suggestion:</span> {getSuggestion()}
          </p>

          <div className="flex gap-2">
            <button
              onClick={handleRetry}
              className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 transition"
              data-testid="retry-button"
            >
              Try Again
            </button>

            <button
              onClick={handleDismiss}
              className="px-3 py-1 bg-gray-400 text-white text-sm rounded hover:bg-gray-500 transition"
              data-testid="dismiss-button"
            >
              Dismiss
            </button>
          </div>
        </div>
      </div>

      {error.includes('Rate limited') && (
        <div className="mt-3 p-2 bg-yellow-50 border border-yellow-200 rounded text-sm text-yellow-800">
          💡 Consider using a different provider that has available quota.
        </div>
      )}
    </div>
  );
}
