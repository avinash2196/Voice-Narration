import { API_CONFIG } from '@/utils/api-config';
import { TTSGeneration, TTSProvider, RateLimit } from '@/types/tts';
import { Voice } from '@/types/voice';

const VALID_GOOGLE_VOICE_PATTERN = /^[a-z]{2,3}-[A-Z]{2,}[-A-Za-z0-9]+$/;

export function normalizeVoiceIdForProvider(provider: string, voiceId?: string): string {
  const candidate = (voiceId || '').trim();
  if (!candidate) return 'en-US-Neural2-A';

  if (provider === 'google') {
    if (VALID_GOOGLE_VOICE_PATTERN.test(candidate)) {
      return candidate;
    }
    return 'en-US-Neural2-A';
  }

  return candidate;
}

export class TTSApiClient {
  private static normalizeGenerationStatus(status: unknown): TTSGeneration['status'] {
    if (status === 'ready' || status === 'processing' || status === 'failed') {
      return status;
    }
    if (status === 'complete' || status === 'completed') {
      return 'ready';
    }
    return 'ready';
  }

  static async submitGeneration(
    text: string,
    voiceId: string,
    provider: string,
    token: string
  ): Promise<TTSGeneration> {
    const jobId = `gen-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const normalizedProvider = provider as TTSGeneration['provider'];
    const normalizedVoiceId = normalizeVoiceIdForProvider(normalizedProvider, voiceId);

    const response = await fetch(`${API_CONFIG.TTS_SERVICE}/inference/jobs/${jobId}/infer`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        script: text,
        voice_id: normalizedVoiceId,
      }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.error || `Failed to submit generation: ${response.status}`);
    }

    const data = await response.json();

    const status = data.status === 'complete' || data.duration_seconds !== undefined ? 'ready' : 'processing';

    return {
      id: jobId,
      text,
      voiceId,
      provider: normalizedProvider,
      status,
      progress: 100,
      createdAt: new Date().toISOString(),
      completedAt: new Date().toISOString(),
      duration: data.duration_seconds,
    };
  }

  static async getGenerationStatus(generationId: string, token: string): Promise<TTSGeneration> {
    const response = await fetch(`${API_CONFIG.TTS_SERVICE}/inference/jobs/${generationId}/output`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to get generation status: ${response.status}`);
    }

    const data = await response.json();

    return {
      id: generationId,
      text: '',
      voiceId: '',
      provider: 'google' as const,
      status: data.audio_bytes ? 'ready' : 'processing',
      progress: data.audio_bytes ? 100 : 50,
      createdAt: new Date().toISOString(),
      completedAt: data.audio_bytes ? new Date().toISOString() : undefined,
      duration: data.duration_seconds,
    };
  }

  static async getGenerationAudio(generationId: string, token: string): Promise<Blob> {
    const response = await fetch(`${API_CONFIG.TTS_SERVICE}/inference/jobs/${generationId}/download`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to get audio: ${response.status}`);
    }

    return await response.blob();
  }

  static async cancelGeneration(generationId: string, token: string): Promise<void> {
    const response = await fetch(`${API_CONFIG.TTS_SERVICE}/inference/generations/${generationId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.error || `Failed to delete generation: ${response.status}`);
    }
  }

  static async getGenerationHistory(
    page: number,
    limit: number,
    token: string,
    filters?: { voiceId?: string; search?: string }
  ): Promise<{ data: TTSGeneration[]; total: number }> {
    const skip = (page - 1) * limit;
    const params = new URLSearchParams({ skip: String(skip), limit: String(limit) });

    if (filters?.voiceId) params.set('voice_id', filters.voiceId);
    if (filters?.search) params.set('search', filters.search);

    const response = await fetch(`${API_CONFIG.TTS_SERVICE}/inference/generations?${params.toString()}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to get generation history: ${response.status}`);
    }

    const data = await response.json();
    const items = Array.isArray(data.items) ? data.items : [];

    return {
      data: items.map((entry: any) => ({
        id: entry.job_id || entry.id,
        text: entry.text || '',
        voiceId: entry.voice_id ?? '',
        provider: 'google' as const,
        status: TTSApiClient.normalizeGenerationStatus(entry.status),
        progress: 100,
        createdAt: entry.created_at || new Date().toISOString(),
        completedAt: entry.created_at || new Date().toISOString(),
        duration: entry.duration_seconds || 0,
      })),
      total: data.total || 0,
    };
  }

  static async getRateLimit(provider: string, token: string): Promise<RateLimit> {
    return {
      provider,
      totalLimit: 10000,
      used: 0,
      remaining: 10000,
      resetAt: new Date(Date.now() + 86400000).toISOString(),
      percentageUsed: 0,
    };
  }

  static async getAvailableProviders(token: string): Promise<TTSProvider[]> {
    const response = await fetch(`${API_CONFIG.TTS_SERVICE}/inference/backends`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to get providers: ${response.status}`);
    }

    const data = await response.json();

    return (data.backends || []).map((backend: any) => ({
      id: backend.name,
      name: backend.description.split(' (')[0],
      available: true,
      maxCharsPerRequest: 5000,
    }));
  }

  static async getApprovedVoices(token: string): Promise<Voice[]> {
    const response = await fetch(`${API_CONFIG.VOICE_SERVICE}/voices/approved`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to get voices: ${response.status}`);
    }

    const data = await response.json();
    return data.data || [];
  }
}

export const ttsApi = TTSApiClient;
