import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useVoice } from '@/hooks/useVoice';
import { VoiceAPI } from '@/services/voiceApi';

interface VoiceUploadProps {
  onUploadStart?: () => void;
  onUploadComplete?: (voiceId: string) => void;
}

export function VoiceUpload({ onUploadStart, onUploadComplete }: VoiceUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadSpeed, setUploadSpeed] = useState('');
  const [timeRemaining, setTimeRemaining] = useState('');
  const [startTime, setStartTime] = useState<number | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  
  // M2.8: Polling state
  const [isPolling, setIsPolling] = useState(false);
  const [evaluationStatus, setEvaluationStatus] = useState<string | null>(null);
  const [evaluationProgress, setEvaluationProgress] = useState(0);
  const [pollError, setPollError] = useState<string | null>(null);
  const [pollAttemptCount, setPollAttemptCount] = useState(0);
  const [pollingVoiceId, setPollingVoiceId] = useState<string | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);
  const pollingIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const auth = useAuth();
  const { dispatch: voiceDispatch } = useVoice();

  // Create preview URL when file is selected, cleanup on unmount or file change
  useEffect(() => {
    if (selectedFile) {
      const url = URL.createObjectURL(selectedFile);
      setPreviewUrl(url);
      return () => {
        URL.revokeObjectURL(url);
      };
    }
    setPreviewUrl(null);
  }, [selectedFile]);

  // Calculate upload speed and time remaining
  useEffect(() => {
    if (!isUploading || !startTime || uploadProgress === 0 || !selectedFile) return;

    const elapsedMs = Date.now() - startTime;
    const bytesUploaded = (selectedFile.size * uploadProgress) / 100;
    const speedBytesPerMs = bytesUploaded / elapsedMs;

    if (speedBytesPerMs > 0) {
      const speedMBps = speedBytesPerMs * 1000 / (1024 * 1024);
      const speedText = speedMBps > 1 
        ? `${speedMBps.toFixed(2)} MB/s` 
        : `${(speedMBps * 1024).toFixed(0)} KB/s`;
      setUploadSpeed(speedText);

      const remainingBytes = selectedFile.size * (100 - uploadProgress) / 100;
      const remainingMs = speedBytesPerMs > 0 ? remainingBytes / speedBytesPerMs : 0;
      const remainingSeconds = Math.ceil(remainingMs / 1000);

      if (remainingSeconds > 0 && uploadProgress < 100) {
        const mins = Math.floor(remainingSeconds / 60);
        const secs = remainingSeconds % 60;
        setTimeRemaining(`${mins}m ${secs}s remaining`);
      }
    }
  }, [uploadProgress, isUploading, startTime, selectedFile]);

  // Cleanup polling interval on unmount
  useEffect(() => {
    return () => {
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
      }
    };
  }, []);

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  };

  const estimateDuration = (bytes: number) => {
    // Rough estimate: 128 kbps MP3 = 128,000 bits per second = 16,000 bytes per second
    const estimatedSeconds = Math.round(bytes / 16000);
    const minutes = Math.floor(estimatedSeconds / 60);
    const seconds = estimatedSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.currentTarget.files?.[0];
    if (!file) return;

    // Validate file type (check both MIME type and extension)
    const validTypes = ['audio/mpeg', 'audio/wav', 'audio/ogg'];
    const validExtensions = ['.mp3', '.wav', '.ogg'];
    const fileExtension = file.name.toLowerCase().slice(file.name.lastIndexOf('.'));
    const hasValidType = validTypes.includes(file.type) || validExtensions.includes(fileExtension);
    
    if (!hasValidType) {
      setError('Invalid file type: audio files only (MP3, WAV, OGG)');
      return;
    }

    // Validate file size (100 MB)
    if (file.size > 100 * 1024 * 1024) {
      setError('File too large: maximum 100 MB allowed');
      return;
    }

    // Validate not empty
    if (file.size === 0) {
      setError('Empty file: no content (0 bytes)');
      return;
    }

    setSelectedFile(file);
    setError(null);
  };

  const handleClearFile = () => {
    setSelectedFile(null);
    setUploadProgress(0);
    setUploadSpeed('');
    setTimeRemaining('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // M2.8: Start evaluation polling after upload
  const startEvaluationPolling = (voiceId: string | null) => {
    if (!voiceId) {
      setPollError('Voice id is required for evaluation polling');
      setError('Voice id is required for evaluation polling');
      return;
    }

    const authToken = auth.token;
    if (!authToken) {
      setPollError('Authentication required to poll evaluation');
      setError('Authentication required to poll evaluation');
      return;
    }

    setIsPolling(true);
    setPollingVoiceId(voiceId);
    setPollAttemptCount(0);
    setPollError(null);

    let attemptCount = 0;

    // Immediate poll - start it but don't block on it
    VoiceAPI.pollEvaluation(voiceId, authToken)
      .then((result) => {
        // M2.8.5: Show evaluating status
        setEvaluationStatus(result.status);
        
        // M2.8.6: Show progress indicator
        if (result.progress !== undefined) {
          setEvaluationProgress(result.progress);
        }

        // M2.8.3: Stop polling when status is ready
        if (result.status !== 'ready') {
          // Only start interval if not ready after first poll
          // M2.8.2: Setup polling interval (async to ensure it fires after microtasks)
          Promise.resolve().then(() => {
            const pollInterval = setInterval(async () => {
              try {
                attemptCount++;
                setPollAttemptCount(attemptCount);
                
                // M2.8.4: Timeout after 300 attempts
                if (attemptCount > 300) {
                  setError('Evaluation timeout: took too long to evaluate voice quality');
                  setIsPolling(false);
                  clearInterval(pollInterval);
                  pollingIntervalRef.current = null;
                  return;
                }

                const result = await VoiceAPI.pollEvaluation(voiceId, authToken);
                
                setEvaluationStatus(result.status);
                if (result.progress !== undefined) {
                  setEvaluationProgress(result.progress);
                }

                // M2.8.3: Stop polling when status is ready
                if (result.status === 'ready') {
                  setIsPolling(false);
                  clearInterval(pollInterval);
                  pollingIntervalRef.current = null;
                }
              } catch (err) {
                // M2.8.7: Handle polling errors
                const errorMsg = err instanceof Error ? err.message : 'Evaluation failed';
                setPollError(errorMsg);
                setError(errorMsg);
                setIsPolling(false);
                clearInterval(pollInterval);
                pollingIntervalRef.current = null;
              }
            }, 2000);
            
            pollingIntervalRef.current = pollInterval;
          });
        } else {
          setIsPolling(false);
        }
      })
      .catch((err) => {
        // M2.8.7: Handle polling errors
        const errorMsg = err instanceof Error ? err.message : 'Evaluation failed';
        setPollError(errorMsg);
        setError(errorMsg);
        setIsPolling(false);
      });
  };

  // M2.8.8: Cancel polling
  const handleCancelPolling = () => {
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current);
      pollingIntervalRef.current = null;
    }
    setIsPolling(false);
    setEvaluationStatus(null);
    setEvaluationProgress(0);
    setPollError(null);
    setPollAttemptCount(0);
    setPollingVoiceId(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file');
      return;
    }
    if (!auth.token) {
      setError('Authentication required');
      return;
    }

    try {
      setIsUploading(true);
      setUploadProgress(0);
      setUploadSpeed('');
      setTimeRemaining('');
      setStartTime(Date.now());
      abortControllerRef.current = new AbortController();
      onUploadStart?.();

      const formData = new FormData();
      formData.append('file', selectedFile);

      // Simulate progress
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => (prev < 90 ? prev + Math.random() * 30 : prev));
      }, 200);

      const voice = await VoiceAPI.uploadVoice(formData, auth.token);

      clearInterval(progressInterval);
      
      // Force progress to 100% and flush that render before clearing upload state
      setUploadProgress(100);
      
      // Small delay to allow progress update to render before clearing isUploading
      await new Promise(resolve => setTimeout(resolve, 50));
      
      voiceDispatch({ type: 'ADD_VOICE', payload: voice });
      onUploadComplete?.(voice.id);

      // M2.8: Start polling evaluation after successful upload
      startEvaluationPolling(voice.id);

      // Now reset upload state
      setIsUploading(false);
      setStartTime(null);
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Upload failed';
      setError(mapErrorToUserMessage(errorMsg));
      setIsUploading(false);
      setStartTime(null);
    }
  };

  const mapErrorToUserMessage = (error: string): string => {
    if (error.includes('400')) return 'Invalid format: file format not supported';
    if (error.includes('401')) return 'Unauthorized: please log in again';
    if (error.includes('413')) return 'File too large: maximum 100 MB allowed';
    if (error.includes('429')) return 'Rate limit: too many requests, please try later';
    if (error.includes('500')) return 'Server error: evaluation service temporarily unavailable';
    if (error.includes('Network') || error.includes('offline') || error.includes('Failed to fetch')) return 'Network error: connection failed';
    return error;
  };

  const handleCancel = () => {
    abortControllerRef.current?.abort();
    setIsUploading(false);
    setUploadProgress(0);
    setUploadSpeed('');
    setTimeRemaining('');
    setStartTime(null);
  };

  const handleRetry = async () => {
    setError(null);
    await handleUpload();
  };

  const handleDismissError = () => {
    setError(null);
  };

  return (
    <div className="voice-upload p-4 border rounded">
      <h3 className="text-lg font-semibold mb-4">Upload Voice</h3>

      {error && (
        <div className="mb-4 p-3 bg-red-100 border border-red-400 rounded">
          <p className="text-red-700 mb-2">{error}</p>
          <div className="flex gap-2">
            <button
              onClick={handleRetry}
              className="px-3 py-1 bg-red-500 text-white rounded text-sm hover:bg-red-600"
            >
              Retry
            </button>
            <button
              onClick={handleDismissError}
              className="px-3 py-1 bg-gray-500 text-white rounded text-sm hover:bg-gray-600"
            >
              Dismiss
            </button>
          </div>
        </div>
      )}

      <div className="mb-4">
        <label htmlFor="voice-file" className="block text-sm font-medium mb-1">
          Select File
        </label>
        <input
          id="voice-file"
          name="voice-file"
          ref={fileInputRef}
          type="file"
          onChange={handleFileSelect}
          disabled={isUploading}
          className="w-full mb-2"
        />

        {selectedFile && (
          <div className="mb-4 p-3 bg-gray-100 rounded">
            <p className="font-semibold">{selectedFile.name}</p>
            <p className="text-sm text-gray-600">Size: {formatFileSize(selectedFile.size)}</p>
            <p className="text-sm text-gray-600">Duration: {estimateDuration(selectedFile.size)}</p>
            <div className="mt-2">
              <audio 
                data-testid="audio-preview"
                controls 
                className="w-full"
              >
                <source src={previewUrl || ''} type={selectedFile.type} />
                Your browser does not support the audio element.
              </audio>
            </div>
          </div>
        )}

        {isUploading && (
          <div className="mb-4">
            <div 
              className="w-full bg-gray-200 rounded h-2"
              role="progressbar"
              aria-valuenow={uploadProgress}
              aria-valuemin={0}
              aria-valuemax={100}
            >
              <div
                className="bg-blue-500 h-2 rounded transition-all"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
            <div className="flex justify-between text-sm text-gray-600 mt-1 mb-1">
              <span>{Math.round(uploadProgress)}% uploaded</span>
              <span>{uploadSpeed}</span>
            </div>
            {timeRemaining && <p className="text-sm text-gray-600 mb-1">{timeRemaining}</p>}
          </div>
        )}

        {isPolling && (
          <div className="mb-4">
            <p className="text-sm font-semibold text-blue-600 mb-2">Evaluating...</p>
            {evaluationProgress > 0 && (
              <div 
                className="w-full bg-gray-200 rounded h-2"
                role="progressbar"
                aria-valuenow={evaluationProgress}
                aria-valuemin={0}
                aria-valuemax={100}
              >
                <div
                  className="bg-blue-500 h-2 rounded transition-all"
                  style={{ width: `${evaluationProgress}%` }}
                />
              </div>
            )}
          </div>
        )}

        {pollError && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 rounded">
            <p className="text-red-700">{pollError}</p>
          </div>
        )}

        <div className="flex gap-2">
          <button
            onClick={handleUpload}
            disabled={!selectedFile || isUploading || isPolling}
            className="flex-1 px-4 py-2 bg-green-500 text-white rounded disabled:bg-gray-300"
          >
            {isUploading ? 'In Progress...' : 'Upload'}
          </button>
          {(isUploading || isPolling) && (
            <button
              onClick={isPolling ? handleCancelPolling : handleCancel}
              className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Cancel
            </button>
          )}
          {!isUploading && !isPolling && (
            <button
              onClick={handleClearFile}
              disabled={!selectedFile}
              className="px-4 py-2 bg-gray-500 text-white rounded disabled:bg-gray-300"
            >
              Clear
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
