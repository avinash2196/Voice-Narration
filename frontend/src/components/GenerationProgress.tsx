import React, { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useTTS } from '@/hooks/useTTS';
import { ttsApi } from '@/services/ttsApi';
import { TTSPollingService } from '@/services/ttsPollingService';

export function GenerationProgress() {
  const auth = useAuth();
  const { currentGeneration, isGenerating, error, dispatch } = useTTS();
  const [showCancelConfirm, setShowCancelConfirm] = useState(false);
  const [isCancelling, setIsCancelling] = useState(false);

  if (!isGenerating && !currentGeneration) {
    return null;
  }

  const progress = currentGeneration?.progress ?? 0;
  const elapsedTime = currentGeneration?.createdAt
    ? Math.floor((Date.now() - new Date(currentGeneration.createdAt).getTime()) / 1000)
    : 0;

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleCancel = async () => {
    if (!currentGeneration || !auth.token) return;

    setIsCancelling(true);
    try {
      await ttsApi.cancelGeneration(currentGeneration.id, auth.token);
      TTSPollingService.stopPolling(currentGeneration.id);
      dispatch({
        type: 'GENERATION_FAILED',
        payload: 'Generation cancelled by user',
      });
    } catch (err) {
      dispatch({
        type: 'GENERATION_FAILED',
        payload: err instanceof Error ? err.message : 'Failed to cancel generation',
      });
    } finally {
      setIsCancelling(false);
      setShowCancelConfirm(false);
    }
  };

  return (
    <div
      className="w-full p-4 bg-blue-50 border border-blue-200 rounded-lg"
      data-testid="generation-progress"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div
            className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"
            data-testid="loading-spinner"
          />
          <span className="font-medium text-gray-900">
            {isGenerating ? 'Generating speech...' : 'Generation complete'}
          </span>
        </div>

        {isGenerating && (
          <button
            onClick={() => setShowCancelConfirm(true)}
            className="text-sm px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition"
            data-testid="cancel-button"
            disabled={isCancelling}
          >
            {isCancelling ? 'Cancelling...' : 'Cancel'}
          </button>
        )}
      </div>

      {/* Progress Bar */}
      <div className="mb-3">
        <div className="w-full bg-gray-300 rounded-full h-3">
          <div
            className="h-3 bg-blue-600 rounded-full transition-all"
            style={{ width: `${Math.min(progress, 100)}%` }}
            data-testid="progress-bar"
          />
        </div>
        <div className="flex justify-between items-center mt-1">
          <span className="text-sm text-gray-700" data-testid="progress-percentage">
            {progress}%
          </span>
          <span className="text-sm text-gray-600" data-testid="elapsed-time">
            Elapsed: {formatTime(elapsedTime)}
          </span>
        </div>
      </div>

      {/* Status Display */}
      {currentGeneration && (
        <div className="text-sm text-gray-700 mb-3" data-testid="generation-status">
          <p>
            <span className="font-medium">Status:</span>{' '}
            <span className="capitalize">{currentGeneration.status}</span>
          </p>
          {currentGeneration.completedAt && (
            <p>
              <span className="font-medium">Completed:</span>{' '}
              {new Date(currentGeneration.completedAt).toLocaleTimeString()}
            </p>
          )}
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="p-2 bg-red-100 border border-red-300 rounded text-sm text-red-700 mb-3" data-testid="error-display">
          ❌ {error}
        </div>
      )}

      {/* Cancel Confirmation Modal */}
      {showCancelConfirm && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          data-testid="cancel-confirmation"
        >
          <div className="bg-white rounded-lg p-6 shadow-lg max-w-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Cancel Generation?
            </h3>
            <p className="text-gray-600 mb-6">
              Are you sure you want to cancel this generation? This action cannot be undone.
            </p>
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowCancelConfirm(false)}
                className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 transition"
                data-testid="cancel-confirm-no"
              >
                No, Keep it
              </button>
              <button
                onClick={handleCancel}
                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
                data-testid="cancel-confirm-yes"
              >
                Yes, Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
