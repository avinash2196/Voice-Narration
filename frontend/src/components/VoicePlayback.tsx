interface VoicePlaybackProps {
  voiceUrl?: string;
}

export function VoicePlayback({ voiceUrl }: VoicePlaybackProps) {
  return (
    <div className="voice-playback p-4 border rounded">
      <div className="flex gap-2 mb-4">
        <button className="px-4 py-2 bg-blue-500 text-white rounded">Play</button>
        <button className="px-4 py-2 bg-gray-500 text-white rounded">Pause</button>
      </div>
      <div className="w-full bg-gray-200 rounded h-2 mb-2" />
      <div className="text-sm text-gray-600">0:00 / 1:00</div>
    </div>
  );
}
