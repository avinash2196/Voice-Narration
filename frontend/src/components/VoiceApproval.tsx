import { useState, useEffect } from 'react';
import type { EvaluationResult } from '@/types/voice';
import { VoiceEvaluationPoller } from '@/services/voiceEvaluationPoller';
import { useAuth } from '@/hooks/useAuth';

interface VoiceApprovalProps {
  voiceId: string;
  onApprovalComplete?: (approved: boolean) => void;
}

export function VoiceApproval({ voiceId, onApprovalComplete }: VoiceApprovalProps) {
  const { token } = useAuth();
  const [evaluationResult, setEvaluationResult] = useState<EvaluationResult | null>(null);
  const [isPolling, setIsPolling] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [rejectionReason, setRejectionReason] = useState('');
  const [showRejectionForm, setShowRejectionForm] = useState(false);

  useEffect(() => {
    if (!token) return;

    setIsPolling(true);
    setError(null);

    const handleUpdate = (result: EvaluationResult) => {
      setEvaluationResult(result);
    };

    const handleComplete = (result: EvaluationResult) => {
      setEvaluationResult(result);
      setIsPolling(false);

      // Auto-approve if score >= 60
      if (result.status === 'ready' && result.score !== null) {
        onApprovalComplete?.(result.score >= 60);
      }
    };

    const handleError = (errorMsg: string) => {
      setError(errorMsg);
      setIsPolling(false);
    };

    VoiceEvaluationPoller.startPolling(voiceId, token, handleUpdate, handleComplete, handleError);

    return () => {
      VoiceEvaluationPoller.stopPolling(voiceId);
    };
  }, [voiceId, token, onApprovalComplete]);

  if (error) {
    return (
      <div className="voice-approval p-4 border rounded bg-red-50">
        <p className="text-red-700">{error}</p>
        <button
          onClick={() => {
            if (token) {
              VoiceEvaluationPoller.startPolling(voiceId, token, () => {}, () => {}, () => {});
            }
          }}
          className="mt-2 px-3 py-1 bg-red-500 text-white rounded"
        >
          Retry
        </button>
      </div>
    );
  }

  if (isPolling || !evaluationResult) {
    return (
      <div className="voice-approval p-4 border rounded bg-blue-50">
        <div className="flex items-center gap-2">
          <div className="animate-spin rounded-full h-4 w-4 border-2 border-blue-500 border-t-transparent" />
          <p className="text-blue-700">Evaluating your voice...</p>
        </div>
      </div>
    );
  }

  const isApproved = evaluationResult.score !== null && evaluationResult.score >= 60;
  const statusBadgeColor = isApproved ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700';
  const statusText = isApproved ? 'Approved' : 'Rejected';

  return (
    <div className="voice-approval p-4 border rounded">
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold">Voice Evaluation</h3>
          <span className={`px-3 py-1 rounded font-semibold ${statusBadgeColor}`}>{statusText}</span>
        </div>

        {evaluationResult.score !== null && (
          <>
            <p className="text-2xl font-bold text-gray-800 mb-2">
              Score: {evaluationResult.score}/100
            </p>
            <p className="text-gray-600">{evaluationResult.feedback}</p>
          </>
        )}
      </div>

      {!showRejectionForm && (
        <div className="flex gap-2">
          <button
            onClick={() => onApprovalComplete?.(true)}
            className="flex-1 px-4 py-2 bg-green-500 text-white rounded"
          >
            Approve
          </button>
          <button
            onClick={() => setShowRejectionForm(true)}
            className="flex-1 px-4 py-2 bg-red-500 text-white rounded"
          >
            Reject
          </button>
        </div>
      )}

      {showRejectionForm && (
        <div className="mt-4">
          <textarea
            placeholder="Rejection reason"
            value={rejectionReason}
            onChange={(e) => setRejectionReason(e.target.value)}
            className="w-full px-3 py-2 border rounded mb-2"
            rows={3}
          />
          <button
            onClick={() => {
              onApprovalComplete?.(false);
              setShowRejectionForm(false);
            }}
            className="w-full px-4 py-2 bg-red-500 text-white rounded"
          >
            Confirm Rejection
          </button>
        </div>
      )}
    </div>
  );
}
