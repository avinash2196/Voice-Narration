import React, { useState } from 'react';
import { VoiceRecorder } from '@/components/VoiceRecorder';
import { VoiceUpload } from '@/components/VoiceUpload';
import { VoiceLibrary } from '@/components/VoiceLibrary';
import { GenerationSubmitForm } from '@/components/GenerationSubmitForm';
import { GenerationProgress } from '@/components/GenerationProgress';
import { GenerationErrorDisplay } from '@/components/GenerationErrorDisplay';
import { AudioPlayer } from '@/components/AudioPlayer';
import { GenerationHistory } from '@/components/GenerationHistory';
import { RateLimitDisplay } from '@/components/RateLimitDisplay';
import { QualityMetrics } from '@/components/QualityMetrics';
import { useAuth } from '@/hooks/useAuth';
import { useTTS } from '@/hooks/useTTS';
import { ttsApi } from '@/services/ttsApi';

type TabType = 'record' | 'upload' | 'library' | 'tts';

export function VoiceManagement() {
  const [activeTab, setActiveTab] = useState<TabType>('library');
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const auth = useAuth();
  const { selectedProvider, currentGeneration, dispatch } = useTTS();
  const [audioUrl, setAudioUrl] = React.useState<string>();

  const handleVoiceCreated = () => {
    setRefreshTrigger(prev => prev + 1);
    setActiveTab('library');
  };

  // Fetch rate limit on mount and when provider changes
  React.useEffect(() => {
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
  React.useEffect(() => {
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
    <div className="min-h-screen bg-gray-100" data-testid="voice-management-page">
      <div className="max-w-6xl mx-auto py-8 px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Voice Management</h1>
          <p className="text-gray-600">
            Record, upload, and manage your custom voices for TTS generation
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-8 border-b border-gray-200 overflow-x-auto">
          <button
            onClick={() => setActiveTab('record')}
            className={`px-6 py-3 font-medium whitespace-nowrap border-b-2 transition ${
              activeTab === 'record'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            🎤 Record Voice
          </button>
          <button
            onClick={() => setActiveTab('upload')}
            className={`px-6 py-3 font-medium whitespace-nowrap border-b-2 transition ${
              activeTab === 'upload'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            📁 Upload Voice
          </button>
          <button
            onClick={() => setActiveTab('library')}
            className={`px-6 py-3 font-medium whitespace-nowrap border-b-2 transition ${
              activeTab === 'library'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            📚 Voice Library
          </button>
          <button
            onClick={() => setActiveTab('tts')}
            className={`px-6 py-3 font-medium whitespace-nowrap border-b-2 transition ${
              activeTab === 'tts'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            🎙️ Generate Speech
          </button>
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          {/* Record Voice Tab */}
          {activeTab === 'record' && (
            <div className="bg-white rounded-lg shadow p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Record Your Voice</h2>
              <p className="text-gray-600 mb-6">
                Record a new voice directly from your microphone and upload it to your voice library.
              </p>
              <VoiceRecorder onRecordingComplete={handleVoiceCreated} />
            </div>
          )}

          {/* Upload Voice Tab */}
          {activeTab === 'upload' && (
            <div className="bg-white rounded-lg shadow p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Upload Voice File</h2>
              <p className="text-gray-600 mb-6">
                Upload an audio file (MP3, WAV, or OGG) to add to your voice library.
                Supported formats: MP3, WAV, OGG (max 100 MB).
              </p>
              <VoiceUpload onUploadComplete={handleVoiceCreated} />
            </div>
          )}

          {/* Voice Library Tab */}
          {activeTab === 'library' && (
            <div className="bg-white rounded-lg shadow p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Voice Library</h2>
              <p className="text-gray-600 mb-6">
                Browse all your recorded and uploaded voices. Approved voices can be used for TTS generation.
              </p>
              <VoiceLibrary key={refreshTrigger} />
            </div>
          )}

          {/* TTS Generation Tab */}
          {activeTab === 'tts' && (
            <div className="space-y-6">
              <GenerationErrorDisplay />

              <div className="bg-white rounded-lg shadow p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Generate Speech</h2>
                <GenerationSubmitForm />
              </div>

              {selectedProvider && (
                <RateLimitDisplay provider={selectedProvider} />
              )}

              {currentGeneration && (
                <GenerationProgress />
              )}

              {currentGeneration && audioUrl && (
                <AudioPlayer generation={currentGeneration} audioUrl={audioUrl} />
              )}

              {currentGeneration && (
                <QualityMetrics generation={currentGeneration} />
              )}

              <div className="bg-white rounded-lg shadow p-8">
                <GenerationHistory />
              </div>
            </div>
          )}
        </div>

        {/* Info Box */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="font-bold text-blue-900 mb-2">💡 Quick Tips</h3>
          <ul className="text-blue-800 space-y-1 text-sm">
            <li>• Record or upload voices to create your personal voice library</li>
            <li>• Wait for admin approval before using voices for TTS generation</li>
            <li>• Each voice file can be up to 100 MB</li>
            <li>• Use approved voices in the TTS generation page to create audio</li>
            <li>• You can have multiple voices for different use cases</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
