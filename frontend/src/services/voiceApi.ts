import { API_CONFIG } from '@/utils/api-config';
import type { Voice, UploadProgress, EvaluationResult } from '@/types/voice';
import type { ApiError } from '@/types/api';

export class VoiceAPI {
  static async uploadVoice(formData: FormData, authToken: string): Promise<Voice> {
    const response = await fetch(`${API_CONFIG.VOICE_SERVICE}/voice/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${authToken}`,
      },
      body: formData,
    });

    if (!response.ok) {
      const error = (await response.json()) as ApiError;
      throw new Error(`${response.status}: ${error.message || 'API error'}`);
    }

    return response.json();
  }

  static async listVoices(authToken: string): Promise<Voice[]> {
    const response = await fetch(`${API_CONFIG.VOICE_SERVICE}/voices`, {
      headers: {
        'Authorization': `Bearer ${authToken}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch voices');
    }

    const data = (await response.json()) as { data: Voice[] };
    return data.data;
  }

  static async getVoice(id: string, authToken: string): Promise<Voice> {
    const response = await fetch(`${API_CONFIG.VOICE_SERVICE}/voices/${id}`, {
      headers: {
        'Authorization': `Bearer ${authToken}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch voice');
    }

    return response.json();
  }

  static async deleteVoice(id: string, authToken: string): Promise<void> {
    const response = await fetch(`${API_CONFIG.VOICE_SERVICE}/voices/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${authToken}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to delete voice');
    }
  }

  static async renameVoice(id: string, name: string, authToken: string): Promise<Voice> {
    const response = await fetch(`${API_CONFIG.VOICE_SERVICE}/voices/${id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`,
      },
      body: JSON.stringify({ name }),
    });

    if (!response.ok) {
      throw new Error('Failed to rename voice');
    }

    return response.json();
  }

  static async pollEvaluation(id: string, authToken: string): Promise<EvaluationResult> {
    const response = await fetch(`${API_CONFIG.EVALUATION_SERVICE}/evaluate/voice/${id}/poll`, {
      headers: {
        'Authorization': `Bearer ${authToken}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to poll evaluation');
    }

    return response.json();
  }

  static async getEvaluationScore(id: string, authToken: string): Promise<EvaluationResult> {
    const response = await fetch(`${API_CONFIG.EVALUATION_SERVICE}/evaluate/voice/${id}/score`, {
      headers: {
        'Authorization': `Bearer ${authToken}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to get evaluation score');
    }

    return response.json();
  }
}
