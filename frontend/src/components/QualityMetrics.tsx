import React from 'react';
import { TTSGeneration } from '@/types/tts';

interface QualityMetricsProps {
  generation?: TTSGeneration | null;
  metrics?: {
    audioFormat?: string;
    audioSize?: number;
    audioDuration?: number;
    quality?: number;
  };
}

export function QualityMetrics({ generation, metrics }: QualityMetricsProps) {
  // Support both generation prop and metrics prop for testing
  const data = metrics || generation;
  
  if (!data || (!metrics && generation && generation.status !== 'ready')) {
    return null;
  }

  const formatBytes = (bytes: number | undefined) => {
    if (!bytes) return 'N/A';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const formatDuration = (seconds: number | undefined) => {
    if (!seconds) return 'N/A';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getQualityLevel = (quality: number) => {
    if (quality >= 90) return { level: 'Excellent', color: 'text-green-600' };
    if (quality >= 75) return { level: 'Good', color: 'text-green-500' };
    if (quality >= 60) return { level: 'Acceptable', color: 'text-yellow-600' };
    return { level: 'Poor', color: 'text-red-600' };
  };

  const quality = (data.quality ?? 0) as number;
  const qualityInfo = getQualityLevel(quality);

  return (
    <div
      className="p-4 bg-gray-50 border border-gray-300 rounded-lg"
      data-testid="quality-metrics-container"
    >
      <h3 className="text-sm font-semibold text-gray-900 mb-3">Audio Quality Metrics</h3>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <p className="text-xs text-gray-600">Format</p>
          <p className="text-sm font-medium text-gray-900" data-testid="audio-format">
            {data.audioFormat || 'MP3'}
          </p>
        </div>

        <div>
          <p className="text-xs text-gray-600">Size</p>
          <p className="text-sm font-medium text-gray-900" data-testid="audio-size">
            {formatBytes(data.audioSize)}
          </p>
        </div>

        <div>
          <p className="text-xs text-gray-600">Duration</p>
          <p className="text-sm font-medium text-gray-900" data-testid="audio-duration">
            {formatDuration(data.audioDuration)}
          </p>
        </div>

        <div>
          <p className="text-xs text-gray-600">Quality Score</p>
          <p
            className={`text-sm font-medium ${qualityInfo.color}`}
            data-testid="quality-score"
          >
            {quality} / 100
          </p>
        </div>
      </div>

      <div className="mt-3 p-2 bg-white border border-gray-300 rounded">
        <p
          className={`text-sm font-semibold ${qualityInfo.color}`}
          data-testid="quality-level"
        >
          Quality Level: {qualityInfo.level}
        </p>

        <div className="w-full bg-gray-300 rounded-full h-2 mt-2">
          <div
            className={`h-2 rounded-full ${
              quality >= 90
                ? 'bg-green-600'
                : quality >= 75
                ? 'bg-green-500'
                : quality >= 60
                ? 'bg-yellow-600'
                : 'bg-red-600'
            }`}
            style={{ width: `${Math.min(quality, 100)}%` }}
          />
        </div>
      </div>

      {quality < 70 && (
        <p className="text-xs text-yellow-700 mt-3" data-testid="quality-warning">
          ⚠️ Audio quality is below optimal. Consider retrying or selecting a different voice.
        </p>
      )}
    </div>
  );
}
