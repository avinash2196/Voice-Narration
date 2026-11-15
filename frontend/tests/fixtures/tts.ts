// ============================================================================
// M3-RED TEST FIXTURES: TTS Generation Test Data & Mock Factories
// ============================================================================

import { Voice } from '../../src/types/voice';

// ============================================================================
// MOCK VOICES (reused from M2, marked for TTS compatibility)
// ============================================================================

export const mockVoice1: Voice & { provider?: string; ttsReady?: boolean } = {
  id: 'voice-1',
  name: 'Alex - Male',
  status: 'approved',
  format: 'mp3',
  duration: 2.5,
  fileSize: 50000,
  uploadedAt: new Date('2026-10-20').toISOString(),
  language: 'en-US',
  provider: 'google',
  ttsReady: true,
};

export const mockVoice2: Voice & { provider?: string; ttsReady?: boolean } = {
  id: 'voice-2',
  name: 'Samantha - Female',
  status: 'approved',
  format: 'wav',
  duration: 3.2,
  fileSize: 75000,
  uploadedAt: new Date('2026-10-22').toISOString(),
  language: 'en-US',
  provider: 'elevenlabs',
  ttsReady: true,
};

export const mockVoice3: Voice & { provider?: string; ttsReady?: boolean } = {
  id: 'voice-3',
  name: 'Morgan - Gender Neutral',
  status: 'approved',
  format: 'ogg',
  duration: 2.8,
  fileSize: 65000,
  uploadedAt: new Date('2026-10-25').toISOString(),
  language: 'en-US',
  provider: 'azure',
  ttsReady: true,
};

export const mockVoicePending: Voice & { provider?: string; ttsReady?: boolean } = {
  id: 'voice-4',
  name: 'Jordan - Pending',
  status: 'pending',
  format: 'mp3',
  duration: 2.2,
  fileSize: 45000,
  uploadedAt: new Date('2026-10-26').toISOString(),
  language: 'en-US',
  provider: 'google',
  ttsReady: false,
};

// ============================================================================
// MOCK TEXT SAMPLES (for generation testing)
// ============================================================================

export const textSamples = {
  short: 'Hello, world!',
  medium: 'The quick brown fox jumps over the lazy dog. This is a longer sentence with more words.',
  long: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
  specialChars: 'Hello! How are you? I\'m great. 123 numbers: @#$%^&*()_+-=[]{}|;:\'",.<>?/',
  utf8: '你好世界 مرحبا بالعالم Привет мир',
  empty: '',
  maxLength: 'a'.repeat(5000),
  exceedsMaxLength: 'a'.repeat(5001),
  numbers: '1 2 3 4 5 6 7 8 9 0',
  singleChar: 'A',
};

// ============================================================================
// MOCK PROVIDERS
// ============================================================================

export const providers = {
  google: {
    id: 'google-tts',
    name: 'Google Text-to-Speech',
    available: true,
    rateLimitPerHour: 1000,
    maxCharsPerRequest: 5000,
    formats: ['mp3', 'wav', 'ogg'],
  },
  elevenlabs: {
    id: 'elevenlabs-tts',
    name: 'ElevenLabs',
    available: true,
    rateLimitPerHour: 500,
    maxCharsPerRequest: 3000,
    formats: ['mp3', 'wav', 'pcm'],
  },
  azure: {
    id: 'azure-speech',
    name: 'Azure Speech Services',
    available: true,
    rateLimitPerHour: 2000,
    maxCharsPerRequest: 5000,
    formats: ['mp3', 'wav', 'ogg', 'flac'],
  },
  unavailable: {
    id: 'unavailable-tts',
    name: 'Unavailable Provider',
    available: false,
    rateLimitPerHour: 0,
    maxCharsPerRequest: 0,
    formats: [],
  },
};

// ============================================================================
// MOCK GENERATION OBJECTS
// ============================================================================

export const mockGeneration1 = {
  id: 'gen-1',
  text: 'Hello, this is a test generation.',
  voiceId: 'voice-1',
  provider: 'google',
  status: 'ready' as const,
  audioFormat: 'mp3',
  audioSize: 15000,
  audioDuration: 1.5,
  createdAt: new Date().toISOString(),
  completedAt: new Date().toISOString(),
  quality: 95,
};

export const mockGeneration2 = {
  id: 'gen-2',
  text: 'Another test generation with more content.',
  voiceId: 'voice-2',
  provider: 'elevenlabs',
  status: 'ready' as const,
  audioFormat: 'wav',
  audioSize: 22000,
  audioDuration: 2.2,
  createdAt: new Date(Date.now() - 3600000).toISOString(),
  completedAt: new Date(Date.now() - 3500000).toISOString(),
  quality: 92,
};

export const mockGenerationProcessing = {
  id: 'gen-3',
  text: 'This one is still processing.',
  voiceId: 'voice-1',
  provider: 'azure',
  status: 'processing' as const,
  progress: 35,
  createdAt: new Date().toISOString(),
};

export const mockGenerationFailed = {
  id: 'gen-4',
  text: 'This generation failed.',
  voiceId: 'voice-3',
  provider: 'google',
  status: 'failed' as const,
  error: 'Provider connection timeout',
  createdAt: new Date().toISOString(),
};

// ============================================================================
// MOCK RATE LIMIT RESPONSES
// ============================================================================

export const mockRateLimit = {
  google: {
    provider: 'google',
    totalLimit: 1000,
    used: 650,
    remaining: 350,
    resetAt: new Date(Date.now() + 3600000).toISOString(),
    percentageUsed: 65,
  },
  elevenlabs: {
    provider: 'elevenlabs',
    totalLimit: 500,
    used: 450,
    remaining: 50,
    resetAt: new Date(Date.now() + 1800000).toISOString(),
    percentageUsed: 90,
  },
  azure: {
    provider: 'azure',
    totalLimit: 2000,
    used: 200,
    remaining: 1800,
    resetAt: new Date(Date.now() + 7200000).toISOString(),
    percentageUsed: 10,
  },
};

// ============================================================================
// MOCK AUDIO BLOBS
// ============================================================================

export const mockAudioBlob = new Blob(['mock audio data'], { type: 'audio/mp3' });

export const mockAudioWav = new Blob(['mock wav data'], { type: 'audio/wav' });

export const mockAudioOgg = new Blob(['mock ogg data'], { type: 'audio/ogg' });

// ============================================================================
// ERROR FIXTURES
// ============================================================================

export const errorResponses = {
  emptyText: {
    status: 400,
    error: 'INVALID_TEXT',
    message: 'Text cannot be empty',
  },
  textTooLong: {
    status: 400,
    error: 'TEXT_TOO_LONG',
    message: 'Text exceeds maximum character limit (5000)',
  },
  invalidVoice: {
    status: 400,
    error: 'INVALID_VOICE',
    message: 'Voice not found or not approved for TTS',
  },
  voiceNotApproved: {
    status: 400,
    error: 'VOICE_NOT_APPROVED',
    message: 'Voice must be approved before TTS generation',
  },
  invalidProvider: {
    status: 400,
    error: 'INVALID_PROVIDER',
    message: 'Provider is not available or not supported',
  },
  unauthorized: {
    status: 401,
    error: 'UNAUTHORIZED',
    message: 'Authentication required',
  },
  quotaExceeded: {
    status: 429,
    error: 'RATE_LIMITED',
    message: 'Rate limit exceeded for this provider',
    retryAfter: 3600,
  },
  providerUnavailable: {
    status: 503,
    error: 'SERVICE_UNAVAILABLE',
    message: 'TTS provider is currently unavailable',
  },
  generationTimeout: {
    status: 504,
    error: 'TIMEOUT',
    message: 'Generation request timed out after 600 seconds',
  },
};

// ============================================================================
// FACTORY FUNCTIONS
// ============================================================================

export function createMockGeneration(overrides = {}) {
  return {
    ...mockGeneration1,
    id: `gen-${Math.random().toString(36).substr(2, 9)}`,
    createdAt: new Date().toISOString(),
    ...overrides,
  };
}

export function createMockVoice(overrides = {}) {
  return {
    ...mockVoice1,
    id: `voice-${Math.random().toString(36).substr(2, 9)}`,
    ...overrides,
  };
}

export function createMockRateLimit(provider: string, used: number = 0) {
  const baseLimit = {
    google: 1000,
    elevenlabs: 500,
    azure: 2000,
  }[provider] || 1000;

  return {
    provider,
    totalLimit: baseLimit,
    used,
    remaining: baseLimit - used,
    resetAt: new Date(Date.now() + 3600000).toISOString(),
    percentageUsed: Math.round((used / baseLimit) * 100),
  };
}

export function createMockAudioBlob(sizeKb: number = 15, type: string = 'audio/mp3') {
  const data = new Uint8Array(sizeKb * 1024).fill(0x00);
  return new Blob([data], { type });
}

// ============================================================================
// MOCK GENERATION HISTORY
// ============================================================================

export const mockGenerationHistory = {
  data: [
    mockGeneration1,
    mockGeneration2,
    createMockGeneration({
      id: 'gen-5',
      text: 'Third generation in history',
      status: 'ready',
      quality: 88,
    }),
  ],
  total: 3,
  page: 1,
  limit: 10,
};

// ============================================================================
// MOCK QUALITY METRICS
// ============================================================================

export const mockQualityMetrics = {
  excellent: {
    score: 95,
    format: 'mp3',
    bitrate: 192,
    duration: 1.5,
    fileSize: 15000,
    confidence: 0.98,
  },
  good: {
    score: 80,
    format: 'wav',
    bitrate: 128,
    duration: 2.2,
    fileSize: 22000,
    confidence: 0.92,
  },
  acceptable: {
    score: 70,
    format: 'ogg',
    bitrate: 96,
    duration: 2.0,
    fileSize: 18000,
    confidence: 0.85,
  },
  poor: {
    score: 50,
    format: 'mp3',
    bitrate: 64,
    duration: 1.8,
    fileSize: 12000,
    confidence: 0.65,
  },
};

// ============================================================================
// MOCK CONTEXT STATE
// ============================================================================

export const mockTTSContextState = {
  voices: [mockVoice1, mockVoice2, mockVoice3],
  selectedVoice: mockVoice1,
  selectedProvider: 'google',
  generationText: '',
  isGenerating: false,
  currentGeneration: null,
  generationHistory: [],
  error: null,
  rateLimit: mockRateLimit.google,
};

// ============================================================================
// MOCK RESPONSES FOR STREAMING
// ============================================================================

export function createMockStreamingResponse(chunkCount: number = 5) {
  const chunks = [];
  for (let i = 0; i < chunkCount; i++) {
    chunks.push({
      chunk: i,
      data: new Uint8Array([i, i + 1, i + 2]).buffer,
      progress: Math.round(((i + 1) / chunkCount) * 100),
    });
  }
  return chunks;
}

export const mockStreamingEventSource = {
  addEventListener: (event: string, callback: Function) => {},
  close: () => {},
};
