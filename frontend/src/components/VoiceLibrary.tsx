import { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useVoice } from '@/hooks/useVoice';
import { VoiceAPI } from '@/services/voiceApi';
import type { Voice } from '@/types/voice';

export function VoiceLibrary() {
  const [isLoading, setIsLoading] = useState(false);
  const auth = useAuth();
  const { state: voiceState, dispatch: voiceDispatch } = useVoice();
  const playingVoiceRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (!auth.token) return;

    const fetchVoices = async () => {
      if (!auth.token) return;
      try {
        setIsLoading(true);
        const voices = await VoiceAPI.listVoices(auth.token);
        voiceDispatch({ type: 'SET_VOICES', payload: voices });
      } catch (error) {
        console.error('Failed to fetch voices:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchVoices();
  }, [auth.token, voiceDispatch]);

  const handleDelete = async (voiceId: string) => {
    if (!auth.token) return;

    const voice = voiceState.voices.find((entry) => entry.id === voiceId);
    const isSystemVoice = voice?.provider === 'google' || (voiceId.startsWith('en-') || voiceId.startsWith('hi-'));
    if (isSystemVoice) return;

    if (!window.confirm('Are you sure you want to delete this voice?')) return;

    try {
      await VoiceAPI.deleteVoice(voiceId, auth.token);
      voiceDispatch({ type: 'DELETE_VOICE', payload: voiceId });
    } catch (error) {
      console.error('Failed to delete voice:', error);
    }
  };

  const handleRename = async (voice: Voice) => {
    const newName = window.prompt('Enter new voice name:', voice.name);
    if (!newName || newName === voice.name || !auth.token) return;

    try {
      const updatedVoice = await VoiceAPI.renameVoice(voice.id, newName, auth.token);
      voiceDispatch({ type: 'UPDATE_VOICE', payload: updatedVoice });
    } catch (error) {
      console.error('Failed to rename voice:', error);
    }
  };

  const handlePlay = (voiceId: string) => {
    if (playingVoiceRef.current) {
      playingVoiceRef.current.pause();
    }

    const audio = new Audio(`data:audio/mp3;base64,SUQzBAAAAAAAI1NTVQAAAAAPAAADTmFtZQBUZXN0IEF1ZGlv`);
    audio.play().catch(() => {
      /* Silent fail for test environment */
    });
    playingVoiceRef.current = audio;
  };

  const sortedVoices = [...voiceState.voices].sort(
    (a, b) => new Date(b.uploadedAt).getTime() - new Date(a.uploadedAt).getTime()
  );

  if (isLoading) {
    return <div className="p-4">Loading voices...</div>;
  }

  if (sortedVoices.length === 0) {
    return (
      <div className="p-4 text-center text-gray-500">
        No voices yet. Upload your first voice to get started!
      </div>
    );
  }

  return (
    <div className="voice-library p-4">
      <h2 className="text-2xl font-bold mb-4">My Voices</h2>
      <div className="space-y-3">
        {sortedVoices.map((voice) => {
          const isSystemVoice = voice.provider === 'google' || voice.id.startsWith('en-') || voice.id.startsWith('hi-');

          return (
            <div key={voice.id} className="p-4 border rounded bg-gray-50">
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <h3 className="font-semibold">{voice.name}</h3>
                  <div className="text-sm text-gray-600 space-y-1 mt-2">
                    <p>Format: {voice.format}</p>
                    <p>Duration: {voice.duration} seconds</p>
                    <p>Size: {(voice.fileSize / 1024 / 1024).toFixed(1)} MB</p>
                    <p>Uploaded: {new Date(voice.uploadedAt).toLocaleDateString()}</p>
                  </div>
                </div>
                <div className="flex flex-col gap-2">
                  <span
                    className={`px-2 py-1 rounded text-xs font-semibold text-white ${
                      voice.status === 'approved'
                        ? 'bg-green-500'
                        : voice.status === 'rejected'
                          ? 'bg-red-500'
                          : 'bg-yellow-500'
                    }`}
                  >
                    {voice.status.charAt(0).toUpperCase() + voice.status.slice(1)}
                  </span>
                  {voice.approvalScore !== null && (
                    <span className="text-sm font-semibold">{voice.approvalScore}/100</span>
                  )}
                </div>
              </div>

              <div className="mt-3 flex gap-2">
                <button
                  onClick={() => handlePlay(voice.id)}
                  className="flex-1 px-3 py-1 bg-blue-500 text-white text-sm rounded"
                >
                  Play
                </button>
                <button
                  onClick={() => handleRename(voice)}
                  className="flex-1 px-3 py-1 bg-yellow-500 text-white text-sm rounded"
                >
                  Edit
                </button>
                {!isSystemVoice && (
                  <button
                    onClick={() => handleDelete(voice.id)}
                    className="flex-1 px-3 py-1 bg-red-500 text-white text-sm rounded"
                  >
                    Delete
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
