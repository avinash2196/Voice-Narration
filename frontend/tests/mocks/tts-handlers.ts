// ============================================================================
// M3-RED MSW HANDLERS: TTS Service Mocking (Port 8003)
// ============================================================================

import { rest } from 'msw';
import { errorResponses, mockGeneration1, mockGenerationHistory, mockRateLimit } from '../fixtures/tts';

const TTS_API_BASE_URL = 'http://localhost:8003';

// ============================================================================
// TTS SERVICE HANDLERS (Port 8003)
// ============================================================================

export const ttsHandlers = [
  // ========================================================================
  // POST /generate - Submit text for TTS generation
  // ========================================================================
  rest.post(`${TTS_API_BASE_URL}/generate`, (req, res, ctx) => {
    const body = req.body as any;
    const { text, voiceId, provider } = body;

    // Validate text
    if (!text || text.trim() === '') {
      return res(ctx.status(400), ctx.json(errorResponses.emptyText));
    }

    if (text.length > 5000) {
      return res(ctx.status(400), ctx.json(errorResponses.textTooLong));
    }

    // Validate voice
    if (!voiceId) {
      return res(ctx.status(400), ctx.json(errorResponses.invalidVoice));
    }

    // Validate provider
    if (!provider) {
      return res(ctx.status(400), ctx.json(errorResponses.invalidProvider));
    }

    // Success: Return 202 Accepted with generation ID
    return res(
      ctx.status(202),
      ctx.json({
        id: `gen-${Date.now()}`,
        text,
        voiceId,
        provider,
        status: 'processing',
        createdAt: new Date().toISOString(),
      })
    );
  }),

  // ========================================================================
  // GET /generate/:id/status - Poll for generation status
  // ========================================================================
  rest.get(`${TTS_API_BASE_URL}/generate/:id/status`, (req, res, ctx) => {
    const { id } = req.params;

    // Simulate different statuses based on ID patterns
    if (id.includes('processing')) {
      return res(
        ctx.status(200),
        ctx.json({
          id,
          status: 'processing',
          progress: 45,
          estimatedTimeRemaining: 30,
        })
      );
    }

    if (id.includes('ready')) {
      return res(
        ctx.status(200),
        ctx.json({
          id,
          status: 'ready',
          progress: 100,
          audioFormat: 'mp3',
          audioSize: 15000,
          audioDuration: 1.5,
          quality: 95,
        })
      );
    }

    if (id.includes('failed')) {
      return res(
        ctx.status(200),
        ctx.json({
          id,
          status: 'failed',
          error: 'Provider error',
          errorCode: 'PROVIDER_ERROR',
        })
      );
    }

    // Default: Ready status
    return res(
      ctx.status(200),
      ctx.json({
        id,
        status: 'ready',
        progress: 100,
        audioFormat: 'mp3',
        audioSize: 15000,
        audioDuration: 1.5,
        quality: 92,
      })
    );
  }),

  // ========================================================================
  // GET /generate/:id/audio - Stream generated audio
  // ========================================================================
  rest.get(`${TTS_API_BASE_URL}/generate/:id/audio`, (req, res, ctx) => {
    const { id } = req.params;

    // Simulate audio stream
    const audioData = new Uint8Array([
      0xff, 0xfb, 0x90, 0x00, // MP3 header
      ...Array(14996).fill(0x00),
    ]);

    return res(
      ctx.status(200),
      ctx.set('Content-Type', 'audio/mp3'),
      ctx.set('Content-Length', '15000'),
      ctx.body(audioData)
    );
  }),

  // ========================================================================
  // DELETE /generate/:id - Cancel generation
  // ========================================================================
  rest.delete(`${TTS_API_BASE_URL}/generate/:id`, (req, res, ctx) => {
    const { id } = req.params;

    if (!id) {
      return res(ctx.status(400), ctx.json({ error: 'Generation ID required' }));
    }

    return res(
      ctx.status(200),
      ctx.json({
        success: true,
        message: 'Generation cancelled',
        generationId: id,
      })
    );
  }),

  // ========================================================================
  // GET /generations - Get generation history
  // ========================================================================
  rest.get(`${TTS_API_BASE_URL}/generations`, (req, res, ctx) => {
    const page = Number(req.url.searchParams.get('page')) || 1;
    const limit = Number(req.url.searchParams.get('limit')) || 10;

    return res(ctx.status(200), ctx.json(mockGenerationHistory));
  }),

  // ========================================================================
  // GET /rate-limit - Get rate limit status
  // ========================================================================
  rest.get(`${TTS_API_BASE_URL}/rate-limit`, (req, res, ctx) => {
    const provider = req.url.searchParams.get('provider') || 'google';

    const rateLimitData = {
      google: mockRateLimit.google,
      elevenlabs: mockRateLimit.elevenlabs,
      azure: mockRateLimit.azure,
    };

    const limit = rateLimitData[provider as keyof typeof rateLimitData] || mockRateLimit.google;

    return res(ctx.status(200), ctx.json(limit));
  }),

  // ========================================================================
  // GET /providers - Get available providers
  // ========================================================================
  rest.get(`${TTS_API_BASE_URL}/providers`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        {
          id: 'google',
          name: 'Google Text-to-Speech',
          available: true,
          maxCharsPerRequest: 5000,
        },
        {
          id: 'elevenlabs',
          name: 'ElevenLabs',
          available: true,
          maxCharsPerRequest: 3000,
        },
        {
          id: 'azure',
          name: 'Azure Speech Services',
          available: true,
          maxCharsPerRequest: 5000,
        },
      ])
    );
  }),

  // ========================================================================
  // GET /voices - Get voices approved for TTS
  // ========================================================================
  rest.get(`${TTS_API_BASE_URL}/voices`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        {
          id: 'voice-1',
          name: 'Alex - Male',
          language: 'en-US',
          provider: 'google',
          status: 'approved',
        },
        {
          id: 'voice-2',
          name: 'Samantha - Female',
          language: 'en-US',
          provider: 'elevenlabs',
          status: 'approved',
        },
        {
          id: 'voice-3',
          name: 'Morgan - Neutral',
          language: 'en-US',
          provider: 'azure',
          status: 'approved',
        },
      ])
    );
  }),
];

// ============================================================================
// ERROR SCENARIO HANDLERS (for testing error conditions)
// ============================================================================

export const ttsErrorHandlers = {
  emptyText: rest.post(`${TTS_API_BASE_URL}/generate`, (req, res, ctx) =>
    res(ctx.status(400), ctx.json(errorResponses.emptyText))
  ),

  textTooLong: rest.post(`${TTS_API_BASE_URL}/generate`, (req, res, ctx) =>
    res(ctx.status(400), ctx.json(errorResponses.textTooLong))
  ),

  invalidVoice: rest.post(`${TTS_API_BASE_URL}/generate`, (req, res, ctx) =>
    res(ctx.status(400), ctx.json(errorResponses.invalidVoice))
  ),

  voiceNotApproved: rest.post(`${TTS_API_BASE_URL}/generate`, (req, res, ctx) =>
    res(ctx.status(400), ctx.json(errorResponses.voiceNotApproved))
  ),

  invalidProvider: rest.post(`${TTS_API_BASE_URL}/generate`, (req, res, ctx) =>
    res(ctx.status(400), ctx.json(errorResponses.invalidProvider))
  ),

  unauthorized: rest.post(`${TTS_API_BASE_URL}/generate`, (req, res, ctx) =>
    res(ctx.status(401), ctx.json(errorResponses.unauthorized))
  ),

  quotaExceeded: rest.post(`${TTS_API_BASE_URL}/generate`, (req, res, ctx) =>
    res(ctx.status(429), ctx.json(errorResponses.quotaExceeded))
  ),

  providerUnavailable: rest.post(`${TTS_API_BASE_URL}/generate`, (req, res, ctx) =>
    res(ctx.status(503), ctx.json(errorResponses.providerUnavailable))
  ),

  generationTimeout: rest.get(`${TTS_API_BASE_URL}/generate/:id/status`, (req, res, ctx) =>
    res(ctx.status(504), ctx.json(errorResponses.generationTimeout))
  ),

  rateLimitOnStatus: rest.get(`${TTS_API_BASE_URL}/generate/:id/status`, (req, res, ctx) =>
    res(ctx.status(429), ctx.json(errorResponses.quotaExceeded))
  ),

  streamingFailed: rest.get(`${TTS_API_BASE_URL}/generate/:id/audio`, (req, res, ctx) =>
    res(ctx.status(500), ctx.json({ error: 'Streaming failed' }))
  ),
};
