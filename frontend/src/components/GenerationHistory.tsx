import React, { useEffect, useMemo, useState } from 'react';
import { useTTS } from '@/hooks/useTTS';
import { useAuth } from '@/hooks/useAuth';
import { ttsApi } from '@/services/ttsApi';
import { AudioPlayer } from './AudioPlayer';
import { TTSGeneration } from '@/types/tts';

const ITEMS_PER_PAGE = 10;

export function GenerationHistory() {
  const { generationHistory, isLoadingHistory, dispatch } = useTTS();
  const auth = useAuth();
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedGeneration, setSelectedGeneration] = useState<string | null>(null);
  const [audioUrls, setAudioUrls] = useState<Record<string, string>>({});
  const [searchTerm, setSearchTerm] = useState('');
  const [voiceFilter, setVoiceFilter] = useState('');

  const availableVoices = useMemo(
    () => Array.from(new Set(generationHistory.map((gen) => gen.voiceId).filter(Boolean))),
    [generationHistory]
  );

  useEffect(() => {
    const fetchHistory = async () => {
      if (!auth.token) return;

      dispatch({ type: 'SET_LOADING_HISTORY', payload: true });
      try {
        const data = await ttsApi.getGenerationHistory(1, 100, auth.token, {
          voiceId: voiceFilter || undefined,
          search: searchTerm || undefined,
        });
        dispatch({ type: 'SET_HISTORY', payload: data.data });
      } catch (error) {
        console.error('Failed to fetch history:', error);
      } finally {
        dispatch({ type: 'SET_LOADING_HISTORY', payload: false });
      }
    };

    fetchHistory();
  }, [auth.token, dispatch, voiceFilter, searchTerm]);

  const handleLoadAudio = async (generationId: string) => {
    if (audioUrls[generationId]) {
      setSelectedGeneration(generationId);
      return;
    }

    if (!auth.token) return;

    try {
      const blob = await ttsApi.getGenerationAudio(generationId, auth.token);
      const url = URL.createObjectURL(blob);
      setAudioUrls((prev) => ({ ...prev, [generationId]: url }));
      setSelectedGeneration(generationId);
    } catch (error) {
      console.error('Failed to load audio:', error);
    }
  };

  const handleDelete = async (generationId: string) => {
    if (!auth.token) return;

    try {
      await ttsApi.cancelGeneration(generationId, auth.token);
      dispatch({ type: 'DELETE_FROM_HISTORY', payload: generationId });
      if (selectedGeneration === generationId) {
        setSelectedGeneration(null);
      }
      if (audioUrls[generationId]) {
        URL.revokeObjectURL(audioUrls[generationId]);
        setAudioUrls((prev) => {
          const next = { ...prev };
          delete next[generationId];
          return next;
        });
      }
    } catch (error) {
      console.error('Failed to delete generation:', error);
    }
  };

  const totalPages = Math.ceil(generationHistory.length / ITEMS_PER_PAGE);
  const startIdx = (currentPage - 1) * ITEMS_PER_PAGE;
  const paginatedHistory = generationHistory.slice(startIdx, startIdx + ITEMS_PER_PAGE);

  if (isLoadingHistory) {
    return (
      <div className="text-center py-4 text-gray-500" data-testid="loading-spinner">
        Loading history...
      </div>
    );
  }

  if (generationHistory.length === 0) {
    return (
      <div className="space-y-4">
        <div className="flex flex-col gap-3 md:flex-row md:items-center">
          <input
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
            placeholder="Search generation text"
            className="w-full md:max-w-xs rounded border border-gray-300 px-3 py-2 text-sm"
            data-testid="history-search"
          />
          <select
            value={voiceFilter}
            onChange={(event) => setVoiceFilter(event.target.value)}
            className="rounded border border-gray-300 px-3 py-2 text-sm"
            data-testid="history-voice-filter"
          >
            <option value="">All voices</option>
            {availableVoices.map((voice) => (
              <option key={voice} value={voice}>{voice}</option>
            ))}
          </select>
        </div>
        <div className="text-center py-4 text-gray-500" data-testid="empty-state">
          No generations yet
        </div>
      </div>
    );
  }

  const selectedGen = generationHistory.find((g) => g.id === selectedGeneration);

  return (
    <div className="w-full space-y-4" data-testid="generation-history-container">
      <div className="flex flex-col gap-3 md:flex-row md:items-center">
        <input
          value={searchTerm}
          onChange={(event) => setSearchTerm(event.target.value)}
          placeholder="Search generation text"
          className="w-full md:max-w-xs rounded border border-gray-300 px-3 py-2 text-sm"
          data-testid="history-search"
        />
        <select
          value={voiceFilter}
          onChange={(event) => setVoiceFilter(event.target.value)}
          className="rounded border border-gray-300 px-3 py-2 text-sm"
          data-testid="history-voice-filter"
        >
          <option value="">All voices</option>
          {availableVoices.map((voice) => (
            <option key={voice} value={voice}>{voice}</option>
          ))}
        </select>
      </div>

      <h3 className="text-lg font-semibold text-gray-900">Generation History</h3>

      {selectedGen && (
        <AudioPlayer generation={selectedGen} audioUrl={audioUrls[selectedGeneration!]} />
      )}

      <div className="space-y-2">
        {paginatedHistory.map((generation: TTSGeneration) => (
          <div
            key={generation.id}
            className="p-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
            data-testid={`history-item-${generation.id}`}
          >
            <div className="flex justify-between items-start mb-2">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {generation.text.substring(0, 50)}...
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {new Date(generation.createdAt).toLocaleString()}
                </p>
              </div>
              <span className={`text-xs px-2 py-1 rounded ${
                generation.status === 'ready'
                  ? 'bg-green-100 text-green-700'
                  : generation.status === 'processing'
                  ? 'bg-blue-100 text-blue-700'
                  : 'bg-red-100 text-red-700'
              }`}>
                {generation.status.charAt(0).toUpperCase() + generation.status.slice(1)}
              </span>
            </div>

            <div className="flex gap-2">
              {generation.status === 'ready' && (
                <button
                  onClick={() => handleLoadAudio(generation.id)}
                  className="text-sm px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
                  data-testid={`play-button-${generation.id}`}
                >
                  Play
                </button>
              )}

              <button
                onClick={() => handleDelete(generation.id)}
                className="text-sm px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition"
                data-testid={`delete-button-${generation.id}`}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      {totalPages > 1 && (
        <div className="flex justify-center gap-2 mt-4">
          <button
            onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
            disabled={currentPage === 1}
            className="px-3 py-1 bg-gray-300 text-gray-700 rounded disabled:opacity-50"
            data-testid="prev-page"
          >
            Previous
          </button>

          <span className="px-3 py-1 text-gray-700">
            Page {currentPage} of {totalPages}
          </span>

          <button
            onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
            disabled={currentPage === totalPages}
            className="px-3 py-1 bg-gray-300 text-gray-700 rounded disabled:opacity-50"
            data-testid="next-page"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
