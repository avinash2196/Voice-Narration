// ============================================================================
// MSW HANDLERS: Voices Service (Port 8002)
// ============================================================================

import { rest } from 'msw';
import * as fixtures from '../fixtures/voices';

const VOICES_API_BASE = 'http://localhost:8002';

export const voicesHandlers = [
  // POST /voice/upload - Handle voice file upload
  rest.post(`${VOICES_API_BASE}/voice/upload`, async (req, res, ctx) => {
    const formData = await req.text();
    
    // Basic validation - in real tests would parse FormData properly
    if (!formData) {
      return res(ctx.status(400), ctx.json(fixtures.mockErrors.badRequest));
    }

    // Check auth header
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      return res(ctx.status(401), ctx.json(fixtures.mockErrors.unauthorized));
    }

    // Simulate upload delay to allow progress bar to be visible in tests
    // 500ms allows at least 2 progress updates (which fire every 200ms) for speed calculation
    await new Promise(resolve => setTimeout(resolve, 500));

    // Return success response
    return res(
      ctx.status(200),
      ctx.json({
        id: `voice-${Date.now()}`,
        name: 'Uploaded Voice',
        format: 'MP3',
        duration: 45,
        fileSize: 5000000,
        uploadedAt: new Date().toISOString(),
        status: 'pending',
      })
    );
  }),

  // GET /voices - List all user voices
  rest.get(`${VOICES_API_BASE}/voices`, (req, res, ctx) => {
    // Check auth header
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      return res(ctx.status(401), ctx.json(fixtures.mockErrors.unauthorized));
    }

    return res(ctx.status(200), ctx.json(fixtures.mockVoiceListResponse));
  }),

  // GET /voices/:id - Fetch single voice details
  rest.get(`${VOICES_API_BASE}/voices/:id`, (req, res, ctx) => {
    const { id } = req.params;

    // Check auth header
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      return res(ctx.status(401), ctx.json(fixtures.mockErrors.unauthorized));
    }

    // Find mock voice
    const voice = [fixtures.mockVoice1, fixtures.mockVoice2, fixtures.mockVoice3].find(
      (v) => v.id === id
    );

    if (!voice) {
      return res(ctx.status(404), ctx.json({ message: 'Voice not found' }));
    }

    return res(ctx.status(200), ctx.json(voice));
  }),

  // DELETE /voices/:id - Delete voice
  rest.delete(`${VOICES_API_BASE}/voices/:id`, (req, res, ctx) => {
    const { id } = req.params;

    // Check auth header
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      return res(ctx.status(401), ctx.json(fixtures.mockErrors.unauthorized));
    }

    return res(
      ctx.status(200),
      ctx.json({ success: true, message: 'Voice deleted successfully' })
    );
  }),

  // PATCH /voices/:id - Rename or update voice
  rest.patch(`${VOICES_API_BASE}/voices/:id`, async (req, res, ctx) => {
    const { id } = req.params;
    const body = (await req.json()) as { name?: string };

    // Check auth header
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      return res(ctx.status(401), ctx.json(fixtures.mockErrors.unauthorized));
    }

    // Validate name
    if (body.name && body.name.length === 0) {
      return res(
        ctx.status(400),
        ctx.json({ code: 'INVALID_NAME', message: 'Name cannot be empty' })
      );
    }

    // Return updated voice
    return res(
      ctx.status(200),
      ctx.json({
        ...fixtures.mockVoice1,
        id,
        name: body.name || fixtures.mockVoice1.name,
      })
    );
  }),
];
