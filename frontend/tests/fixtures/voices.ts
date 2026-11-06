// ============================================================================
// M2-RED TEST FIXTURES: Voice Objects, Factories, and Mock Responses
// ============================================================================

import { File, Blob } from 'buffer';

// ============================================================================
// MOCK VOICE OBJECTS
// ============================================================================

export const mockVoice1 = {
  id: 'voice-1',
  name: 'Professional Voice',
  format: 'MP3',
  duration: 45,
  fileSize: 7200000,
  uploadedAt: '2026-10-31T10:00:00Z',
  status: 'approved',
  approvalScore: 85,
};

export const mockVoice2 = {
  id: 'voice-2',
  name: 'Natural Voice',
  format: 'WAV',
  duration: 60,
  fileSize: 14400000,
  uploadedAt: '2026-10-31T09:00:00Z',
  status: 'approved',
  approvalScore: 78,
};

export const mockVoice3 = {
  id: 'voice-3',
  name: 'Pending Voice',
  format: 'OGG',
  duration: 30,
  fileSize: 3600000,
  uploadedAt: '2026-10-31T11:00:00Z',
  status: 'pending',
  approvalScore: null,
};

export const mockVoices = [mockVoice1, mockVoice2, mockVoice3];

// ============================================================================
// API RESPONSE FIXTURES
// ============================================================================

export const mockVoiceListResponse = {
  data: [mockVoice1, mockVoice2, mockVoice3],
  total: 3,
  page: 1,
  limit: 10,
};

export const mockUploadResponse = {
  id: 'voice-4',
  name: 'New Voice Sample',
  format: 'MP3',
  duration: 50,
  fileSize: 8000000,
  uploadedAt: '2026-10-31T12:00:00Z',
  status: 'pending',
};

export const mockEvaluationResponse = {
  status: 'ready',
  score: 82,
  feedback: 'Excellent voice sample with clear audio quality',
};

export const mockEvaluationProcessing = {
  status: 'processing',
  score: null,
  feedback: null,
};

export const mockEvaluationError = {
  status: 'error',
  score: null,
  feedback: 'Unable to evaluate voice sample',
};

// ============================================================================
// ERROR RESPONSE FIXTURES
// ============================================================================

export const mockErrors = {
  badRequest: {
    code: 'INVALID_FORMAT',
    message: 'Invalid audio format. Supported: MP3, WAV, OGG',
  },
  unauthorized: {
    code: 'UNAUTHORIZED',
    message: 'Missing or invalid authentication token',
  },
  fileTooLarge: {
    code: 'FILE_TOO_LARGE',
    message: 'File exceeds 100 MB limit',
  },
  rateLimited: {
    code: 'RATE_LIMITED',
    message: 'Rate limit exceeded. Maximum 10 uploads per hour',
  },
  serverError: {
    code: 'SERVER_ERROR',
    message: 'Internal server error. Please try again later',
  },
};

// ============================================================================
// FACTORY FUNCTIONS
// ============================================================================

export function createMockVoice(overrides: Partial<typeof mockVoice1> = {}) {
  return { ...mockVoice1, ...overrides };
}

export function createMockVoiceList(count: number = 3) {
  return Array.from({ length: count }, (_, i) => ({
    ...mockVoice1,
    id: `voice-${i + 1}`,
    name: `Voice Sample ${i + 1}`,
  }));
}

export function createMockFile(
  name = 'voice-sample.mp3',
  size = 5000000,
  type = 'audio/mpeg'
): File {
  const blob = new Blob(['mock audio content'], { type });
  return new File([blob], name, { type });
}

export function createMockAudioStream() {
  return {
    getTracks: () => [{ stop: () => {} }],
    getAudioTracks: () => [{ enabled: true, stop: () => {} }],
  };
}

export function createMockEvalScore(score = 82) {
  return {
    score,
    feedback: score >= 75 ? 'Excellent' : score >= 60 ? 'Good' : 'Fair',
    details: { clarity: 0.95, noise: 0.05 },
  };
}

export function createMockEvalError() {
  return mockErrors.serverError;
}

export function createMockUploadFormData(file: File, name: string, language: string = 'en') {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('name', name);
  formData.append('language', language);
  return formData;
}

// ============================================================================
// MOCK MEDIA RECORDER CLASS
// ============================================================================

export class MockMediaRecorder {
  state: 'inactive' | 'recording' | 'paused' = 'inactive';
  ondataavailable: ((event: any) => void) | null = null;
  onstart: (() => void) | null = null;
  onstop: (() => void) | null = null;
  onerror: ((event: any) => void) | null = null;

  constructor(stream: any) {
    this.stream = stream;
  }

  stream: any;

  start() {
    this.state = 'recording';
    this.onstart?.();
  }

  stop() {
    this.state = 'inactive';
    this.ondataavailable?.(
      new Event('dataavailable', {
        bubbles: true,
      })
    );
    this.onstop?.();
  }

  pause() {
    this.state = 'paused';
  }

  resume() {
    this.state = 'recording';
  }

  static isTypeSupported(type: string): boolean {
    return ['audio/mp3', 'audio/wav', 'audio/ogg'].includes(type);
  }
}

// ============================================================================
// TEST VALIDATORS
// ============================================================================

export function isValidMockVoice(voice: any): boolean {
  return (
    typeof voice.id === 'string' &&
    typeof voice.name === 'string' &&
    ['MP3', 'WAV', 'OGG'].includes(voice.format) &&
    typeof voice.duration === 'number' &&
    typeof voice.fileSize === 'number'
  );
}

export function isValidApiResponse(response: any, type: 'list' | 'single' | 'upload'): boolean {
  if (type === 'list') {
    return Array.isArray(response.data) && typeof response.total === 'number';
  } else if (type === 'single') {
    return isValidMockVoice(response);
  } else if (type === 'upload') {
    return response.id && response.status === 'pending';
  }
  return false;
}

// ============================================================================
// MOCK AUTH CONTEXT (for wrapped tests)
// ============================================================================

export const mockAuthContext = {
  state: {
    user: { id: 'user-1', email: 'test@example.com' },
    token: 'mock-jwt-token',
    refreshToken: 'mock-refresh-token',
    isAuthenticated: true,
    isLoading: false,
    error: null,
  },
  dispatch: () => {},
};

// ============================================================================
// MOCK VOICE CONTEXT (for wrapped tests)
// ============================================================================

export const mockVoiceContext = {
  state: {
    voices: [mockVoice1, mockVoice2],
    isLoading: false,
    error: null,
    selectedVoice: null,
  },
  dispatch: () => {},
};

// ============================================================================
// MOCK MEDIA STREAM (for getUserMedia tests)
// ============================================================================

export const mockMediaStream = {
  getTracks: () => [
    {
      kind: 'audio',
      enabled: true,
      stop: () => {},
    },
  ],
  getAudioTracks: () => [
    {
      kind: 'audio',
      enabled: true,
      stop: () => {},
    },
  ],
};
