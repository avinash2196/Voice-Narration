import { useAuth } from '@/hooks/useAuth';
import { VoiceAPI } from '@/services/voiceApi';

interface VoiceOperationsProps {
  voiceId: string;
  currentName: string;
  onUpdate?: () => void;
  onDelete?: () => void;
}

export function VoiceOperations({ voiceId, currentName, onUpdate, onDelete }: VoiceOperationsProps) {
  const auth = useAuth();

  const handleRename = async () => {
    const newName = window.prompt('Enter new name:', currentName);
    if (!newName || !auth.token) return;

    try {
      await VoiceAPI.renameVoice(voiceId, newName, auth.token);
      onUpdate?.();
    } catch (error) {
      console.error('Failed to rename:', error);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Delete this voice?') || !auth.token) return;

    try {
      await VoiceAPI.deleteVoice(voiceId, auth.token);
      onDelete?.();
    } catch (error) {
      console.error('Failed to delete:', error);
    }
  };

  return (
    <div className="voice-operations flex gap-2">
      <button onClick={handleRename} className="px-3 py-1 bg-yellow-500 text-white rounded">
        Edit
      </button>
      <button onClick={handleDelete} className="px-3 py-1 bg-red-500 text-white rounded">
        Delete
      </button>
    </div>
  );
}
