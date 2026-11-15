import React, { useRef, useState, useEffect } from 'react';
import { TTSGeneration } from '@/types/tts';

interface AudioPlayerProps {
  generation?: TTSGeneration | null;
  audioUrl?: string;
  generationId?: string;
}

export function AudioPlayer({ generation, audioUrl, generationId }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio || !audioUrl) return;

    audio.src = audioUrl;

    const updateTime = () => setCurrentTime(audio.currentTime);
    const updateDuration = () => setDuration(audio.duration);
    const handleEnded = () => setIsPlaying(false);

    audio.addEventListener('timeupdate', updateTime);
    audio.addEventListener('loadedmetadata', updateDuration);
    audio.addEventListener('ended', handleEnded);

    return () => {
      audio.removeEventListener('timeupdate', updateTime);
      audio.removeEventListener('loadedmetadata', updateDuration);
      audio.removeEventListener('ended', handleEnded);
    };
  }, [audioUrl]);

  const handlePlayPause = () => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const audio = audioRef.current;
    if (!audio) return;
    const newTime = parseFloat(e.target.value);
    audio.currentTime = newTime;
    setCurrentTime(newTime);
  };

  const formatTime = (seconds: number) => {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!audioUrl && (!generation || generation.status !== 'ready')) return null;
  const downloadFileName = `${generation?.voiceId || generationId || 'generated-audio'}-${generation?.id || Date.now()}.wav`;

  return (
    <div
      className="w-full p-4 bg-green-50 border border-green-200 rounded-lg"
      data-testid="audio-player-container"
    >
      <audio ref={audioRef} data-testid="audio-element" />

      <div className="flex items-center gap-3 mb-3">
        <button
          onClick={handlePlayPause}
          className="p-2 bg-green-600 text-white rounded-full hover:bg-green-700 transition"
          data-testid={isPlaying ? 'pause-button' : 'play-button'}
        >
          {isPlaying ? '⏸' : '▶️'}
        </button>

        <span className="text-sm font-medium text-gray-700">Generated Audio</span>

        {audioUrl && (
          <a
            href={audioUrl}
            download={downloadFileName}
            className="ml-auto text-sm px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
            data-testid="download-button"
          >
            Download
          </a>
        )}
      </div>

      <div className="space-y-2">
        <input
          type="range"
          min="0"
          max={duration || 0}
          value={currentTime}
          onChange={handleSeek}
          className="w-full h-2 bg-gray-300 rounded-full cursor-pointer accent-green-600"
          data-testid="progress-bar"
        />

        <div className="flex justify-between text-xs text-gray-600">
          <span data-testid="current-time">{formatTime(currentTime)}</span>
          <span data-testid="total-duration">{formatTime(duration)}</span>
        </div>
      </div>

      {generation && generation.audioSize && (
        <p className="text-xs text-gray-500 mt-2">
          Size: {(generation.audioSize / 1024).toFixed(1)} KB
        </p>
      )}
    </div>
  );
}
