import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useVoice } from '@/hooks/useVoice';
import { VoiceAPI } from '@/services/voiceApi';

interface VoiceRecorderProps {
  onRecordingComplete: (data: string | Blob) => void;
}

export function VoiceRecorder({ onRecordingComplete }: VoiceRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [voiceName, setVoiceName] = useState('');
  const [recordedBlob, setRecordedBlob] = useState<Blob | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isRequesting, setIsRequesting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const auth = useAuth();
  const { dispatch: voiceDispatch } = useVoice();

  // Cleanup on component unmount
  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop();
      }
    };
  }, []);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };

  const handleStart = async () => {
    try {
      setIsRequesting(true);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setIsRequesting(false);
      streamRef.current = stream;

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e?.data && e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        // Stop all audio tracks immediately
        stream.getTracks().forEach((track) => track.stop());
        
        // Create blob from collected chunks
        const blob = new Blob(chunksRef.current, { type: 'audio/wav' });
        console.log('Recording stopped, blob size:', blob.size, 'chunks:', chunksRef.current.length);
        
        // Ensure blob has data before setting state
        if (blob.size > 0) {
          setRecordedBlob(blob);
        } else {
          console.error('Recording blob is empty!');
          setError('Recording failed: No audio data captured. Try again.');
        }
      };

      mediaRecorder.start();
      setIsRecording(true);
      setElapsedTime(0);
      setError(null);

      timerRef.current = setInterval(() => {
        setElapsedTime((t) => t + 1);
      }, 1000);
    } catch (error) {
      setIsRequesting(false);
      let errorMessage = 'Microphone access denied';
      
      if (error instanceof DOMException) {
        if (error.name === 'NotFoundError') {
          errorMessage = 'No microphone device found';
        } else if (error.name === 'TimeoutError') {
          errorMessage = 'Microphone request timeout. Please try again.';
        } else if (error.name === 'NotAllowedError') {
          errorMessage = 'Microphone access denied';
        }
      }
      
      setError(errorMessage);
      console.error('Microphone access denied:', error);
    }
  };

  const handlePause = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.pause();
      setIsPaused(true);
      if (timerRef.current) clearInterval(timerRef.current);
    }
  };

  const handleResume = () => {
    if (mediaRecorderRef.current && isPaused) {
      mediaRecorderRef.current.resume();
      setIsPaused(false);
      timerRef.current = setInterval(() => {
        setElapsedTime((t) => t + 1);
      }, 1000);
    }
  };

  const handleStop = () => {
    if (mediaRecorderRef.current && isRecording) {
      if (timerRef.current) clearInterval(timerRef.current);
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setIsPaused(false);
    }
  };

  const handleUpload = async () => {
    // Defensive checks with clear error messages
    if (!recordedBlob) {
      setError('No recording found. Please record audio first.');
      return;
    }
    
    if (recordedBlob.size === 0) {
      setError('Recording is empty. Please try recording again.');
      return;
    }
    
    if (!voiceName || voiceName.trim().length === 0) {
      setError('Please enter a voice name');
      return;
    }
    
    if (!auth.token) {
      setError('Not authenticated. Please log in.');
      return;
    }

    try {
      setIsUploading(true);
      setError(null);

      const formData = new FormData();
      formData.append('file', recordedBlob, 'recording.wav');
      formData.append('name', voiceName);

      const voice = await VoiceAPI.uploadVoice(formData, auth.token);
      voiceDispatch({ type: 'ADD_VOICE', payload: voice });
      
      // Reset form
      setRecordedBlob(null);
      setVoiceName('');
      setElapsedTime(0);
      setIsUploading(false);
      
      // Call callback only after successful upload
      onRecordingComplete(voice.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
      setIsUploading(false);
    }
  };

  const handleReset = () => {
    setRecordedBlob(null);
    setVoiceName('');
    setElapsedTime(0);
    setError(null);
  };

  return (
    <div className="voice-recorder space-y-4">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded space-y-3">
          <div>{error}</div>
          <button
            onClick={handleStart}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded font-semibold text-sm"
          >
            🔄 Try Again
          </button>
        </div>
      )}

      <div className="bg-gray-100 p-4 rounded">
        <div className="text-center mb-4">
          <div className="text-4xl font-mono font-bold text-gray-900">{formatTime(elapsedTime)}</div>
          <p className="text-sm text-gray-600 mt-2">
            {isRecording ? '🔴 Recording...' : recordedBlob ? '✓ Recording ready' : 'No recording yet'}
          </p>
        </div>

        {/* Waveform Visualization */}
        <div className="mb-4 bg-white rounded p-2 border border-gray-300">
          <canvas
            data-testid="waveform-canvas"
            className="w-full h-16 bg-gradient-to-r from-blue-100 to-blue-50 rounded"
            style={{
              backgroundImage: isRecording
                ? 'repeating-linear-gradient(90deg, #3b82f6 0px, #3b82f6 2px, transparent 2px, transparent 4px)'
                : 'none',
              backgroundColor: recordedBlob ? '#dbeafe' : '#f3f4f6',
            }}
          />
        </div>

        <div className="flex gap-2 justify-center flex-wrap">
          <button
            onClick={handleStart}
            disabled={isRecording || recordedBlob !== null || isRequesting}
            className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300 font-semibold"
          >
            ◉ Start
          </button>
          <button
            onClick={handlePause}
            disabled={!isRecording || isPaused}
            className="px-4 py-2 bg-yellow-500 text-white rounded disabled:bg-gray-300 font-semibold"
          >
            ⏸ Pause
          </button>
          <button
            onClick={handleResume}
            disabled={!isPaused}
            className="px-4 py-2 bg-yellow-500 text-white rounded disabled:bg-gray-300 font-semibold"
          >
            ▶ Resume
          </button>
          <button
            onClick={handleStop}
            disabled={!isRecording && !isPaused}
            className="px-4 py-2 bg-red-500 text-white rounded disabled:bg-gray-300 font-semibold"
          >
            ⏹ Stop
          </button>
        </div>
      </div>

      {recordedBlob && (
        <div className="bg-white border border-gray-300 p-4 rounded space-y-3">
          <h3 className="font-semibold text-gray-900">Recording Ready</h3>
          <input
            type="text"
            placeholder="Enter voice name (e.g., 'My Voice')"
            value={voiceName}
            onChange={(e) => setVoiceName(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-600"
          />
          <div className="flex gap-2">
            <button
              onClick={handleUpload}
              disabled={!voiceName || isUploading}
              className="flex-1 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded disabled:bg-gray-300 font-semibold"
            >
              {isUploading ? '⏳ Uploading...' : '✓ Upload Recording'}
            </button>
            <button
              onClick={handleReset}
              disabled={isUploading}
              className="flex-1 px-4 py-2 bg-gray-400 hover:bg-gray-500 text-white rounded disabled:bg-gray-300 font-semibold"
            >
              ✕ Discard
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
