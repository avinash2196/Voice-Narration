// ============================================================================
// MSW HANDLERS: AI Evaluation Service (Port 8006)
// ============================================================================

import { rest } from 'msw';
import * as fixtures from '../fixtures/voices';

const EVALUATION_API_BASE = 'http://localhost:8006';

// Track polling state for realistic simulations
const pollingStates: Record<string, { attempts: number; status: string }> = {};

export const aiEvaluationHandlers = [
  // GET /evaluate/voice/:id/poll - Poll for evaluation status
  rest.get(`${EVALUATION_API_BASE}/evaluate/voice/:id/poll`, (req, res, ctx) => {
    const { id } = req.params;

    // Initialize polling state if not exists
    if (!pollingStates[id]) {
      pollingStates[id] = { attempts: 0, status: 'processing' };
    }

    const state = pollingStates[id];
    state.attempts++;

    // Simulate: processing for 3 attempts, then ready
    if (state.attempts < 3) {
      return res(ctx.status(200), ctx.json(fixtures.mockEvaluationProcessing));
    }

    // After 3 attempts, return ready with score
    if (state.attempts >= 3 && state.status === 'processing') {
      state.status = 'ready';
      return res(
        ctx.status(200),
        ctx.json({
          status: 'ready',
          score: 82,
          feedback: 'Excellent voice quality',
        })
      );
    }

    // Continue returning ready
    return res(
      ctx.status(200),
      ctx.json({
        status: 'ready',
        score: 82,
        feedback: 'Excellent voice quality',
      })
    );
  }),

  // GET /evaluate/voice/:id/score - Get final evaluation score
  rest.get(`${EVALUATION_API_BASE}/evaluate/voice/:id/score`, (req, res, ctx) => {
    const { id } = req.params;

    return res(
      ctx.status(200),
      ctx.json({
        score: 82,
        feedback: 'Excellent voice sample with clear audio quality',
        details: {
          clarity: 0.95,
          noiseLevel: 0.05,
          dynamicRange: 0.88,
          pitchStability: 0.91,
        },
      })
    );
  }),
];

// Helper function to reset polling state (call in tests)
export function resetPollingStates() {
  Object.keys(pollingStates).forEach((key) => {
    delete pollingStates[key];
  });
}
