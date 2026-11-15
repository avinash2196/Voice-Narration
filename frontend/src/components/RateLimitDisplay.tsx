import React, { useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useTTS } from '@/hooks/useTTS';
import { ttsApi } from '@/services/ttsApi';

interface RateLimitDisplayProps {
  provider: string;
}

export function RateLimitDisplay({ provider }: RateLimitDisplayProps) {
  const auth = useAuth();
  const { rateLimit, dispatch } = useTTS();

  useEffect(() => {
    const fetchRateLimit = async () => {
      if (!auth.token || !provider) return;

      try {
        const limit = await ttsApi.getRateLimit(provider, auth.token);
        dispatch({ type: 'SET_RATE_LIMIT', payload: limit });
      } catch (error) {
        console.error('Failed to fetch rate limit:', error);
      }
    };

    fetchRateLimit();

    // Refresh every 30 seconds
    const interval = setInterval(fetchRateLimit, 30000);
    return () => clearInterval(interval);
  }, [auth.token, provider, dispatch]);

  if (!rateLimit) {
    return null;
  }

  const percentageUsed = Math.round(
    (rateLimit.used / rateLimit.totalLimit) * 100
  );
  const isWarning = percentageUsed >= 90;
  const isExceeded = percentageUsed >= 100;

  const getColorClass = () => {
    if (isExceeded) return 'bg-red-50 border-red-300';
    if (isWarning) return 'bg-yellow-50 border-yellow-300';
    return 'bg-blue-50 border-blue-300';
  };

  const getProgressBarColor = () => {
    if (isExceeded) return 'bg-red-600';
    if (isWarning) return 'bg-yellow-600';
    return 'bg-green-600';
  };

  const resetTime = new Date(rateLimit.resetAt).toLocaleTimeString();

  return (
    <div
      className={`p-4 border rounded-lg ${getColorClass()}`}
      data-testid="rate-limit-container"
    >
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-semibold text-gray-900">
          Quota Usage: <span data-testid="rate-limit-usage">{rateLimit.used}/{rateLimit.totalLimit}</span>
        </span>
        <span className="text-sm font-bold text-gray-900">{percentageUsed}%</span>
      </div>

      <div className="w-full bg-gray-300 rounded-full h-3 mb-2">
        <div
          className={`h-3 rounded-full transition-all ${getProgressBarColor()}`}
          style={{ width: `${Math.min(percentageUsed, 100)}%` }}
          data-testid="progress-indicator"
        />
      </div>

      <div className="flex justify-between text-xs text-gray-600">
        <span>Remaining: {Math.max(0, rateLimit.remaining)}</span>
        <span data-testid="rate-limit-reset">Resets: {resetTime}</span>
      </div>

      {isWarning && !isExceeded && (
        <p className="text-sm text-yellow-700 font-semibold mt-2" data-testid="rate-limit-warning">
          ⚠️ Approaching quota limit
        </p>
      )}

      {isExceeded && (
        <p className="text-sm text-red-700 font-semibold mt-2" data-testid="exceeded-message">
          ❌ Quota exceeded - Please wait for reset
        </p>
      )}
    </div>
  );
}
