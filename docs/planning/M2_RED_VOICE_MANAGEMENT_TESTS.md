# M2-RED Test Specification: Voice Management

**Phase:** RED (Define tests before implementation)  
**Milestone:** M2 - Voice Management  
**Week:** 5  
**Status:** COMPLETE - Ready for Test Implementation  
**Created:** 2026-10-31

---

## Summary

**Total Tests:** 117 tests across 14 categories
**Backend Services Mocked:** Voices Service (8002), AI Evaluation Service (8006)
**Dependencies:** M1-GREEN (Authentication) must be complete
**Deliverables:**
- `tests/voice.spec.tsx` (117 test cases, all failing)
- `tests/fixtures/voices.ts` (test data and mock responses)
- `tests/mocks/voices-handlers.ts` (MSW handlers for Voices Service)
- `tests/mocks/ai-evaluation-handlers.ts` (MSW handlers for AI Evaluation)

---

## Test Categories & Coverage

| Category | ID Range | Count | Focus Area |
|----------|----------|-------|-----------|
| Microphone Permissions | M2.1.1-M2.1.8 | 8 | Browser audio access, permission flow, permission denied/revoked |
| Recording Controls | M2.2.1-M2.2.10 | 10 | Record/stop/pause/resume buttons, timer, state management |
| Waveform Visualization | M2.3.1-M2.3.6 | 6 | Real-time waveform drawing, frequency analysis, canvas rendering |
| File Selection & Drag-Drop | M2.4.1-M2.4.9 | 9 | File picker, drag-drop zone, file selection UI, drag-drop feedback |
| File Validation | M2.5.1-M2.5.8 | 8 | Format validation (MP3/WAV/OGG), size validation (100MB), type checking |
| Upload Progress & Submission | M2.6.1-M2.6.8 | 8 | Progress bar during upload, submit button, upload completion, redirect |
| Upload Error Handling | M2.7.1-M2.7.9 | 9 | Network errors, 400/401/413/429/500 responses, user feedback, retry |
| Quality Evaluation & Polling | M2.8.1-M2.8.10 | 10 | Poll /evaluate endpoint every 2s, timeout after 10min, status display |
| Approval Workflow | M2.9.1-M2.9.8 | 8 | Accept/reject based on score, score threshold, visual feedback, state update |
| Voice Library Display | M2.10.1-M2.10.9 | 9 | List all voices, sort/filter/search, pagination, metadata display, empty state |
| Voice Playback & Preview | M2.11.1-M2.11.8 | 8 | Play/pause controls, volume control, progress scrubber, duration display |
| Voice Management Operations | M2.12.1-M2.12.9 | 9 | Delete with confirmation, rename with validation, update metadata |
| State Management & Context | M2.13.1-M2.13.7 | 7 | VoiceContext reducer, action dispatch, state persistence, concurrent ops |
| Error Recovery & Edge Cases | M2.14.1-M2.14.8 | 8 | Network recovery, browser background, storage quota, double-submit |
| **TOTAL** | | **117** | |

---

## API Contracts (Voices Service - Port 8002)

### Success Responses

| Method | Endpoint | Request | Response | Status |
|--------|----------|---------|----------|--------|
| POST | /voices/upload | FormData(file, name, language) | `{ id, name, format, duration, fileSize, uploadedAt, status: "pending" }` | 200 |
| GET | /voices | Query: page, limit, sort | `{ data: Voice[], total, page, limit }` | 200 |
| GET | /voices/:id | - | `{ id, name, format, duration, fileSize, status, createdAt, updatedAt }` | 200 |
| DELETE | /voices/:id | - | `{ success: true, message: "Voice deleted" }` | 200 |
| PATCH | /voices/:id | `{ name: string }` | `{ id, name, format, duration, ... }` (updated) | 200 |

### Error Responses

| Status | Code | Scenario |
|--------|------|----------|
| 400 | INVALID_FORMAT | File not audio or unrecognized format |
| 400 | INVALID_NAME | Name empty or exceeds 100 chars |
| 401 | UNAUTHORIZED | Missing/expired JWT token |
| 413 | FILE_TOO_LARGE | File > 100 MB |
| 429 | RATE_LIMITED | User exceeded 10 uploads/hour |
| 500 | SERVER_ERROR | Unexpected server error |

---

## API Contracts (AI Evaluation Service - Port 8006)

| Method | Endpoint | Request | Response | Status |
|--------|----------|---------|----------|--------|
| GET | /evaluate/voice/:id/poll | - | `{ status: "processing"\|"ready"\|"error", score: 0-100\|null, feedback?: string }` | 200 |
| GET | /evaluate/voice/:id/score | - | `{ score: 0-100, feedback: string, details: object }` | 200 |

---

## Test Implementation Requirements

### Setup & Teardown

Each test file must:

```typescript
beforeEach(() => {
  localStorage.clear();
  vi.clearAllMocks();
  server.resetHandlers();
});

afterEach(() => {
  server.resetHandlers();
  cleanup();
});
```

### Component Rendering

Tests requiring component rendering must wrap with providers:

```typescript
render(
  <AuthContext.Provider value={mockAuthContext}>
    <VoiceContext.Provider value={mockVoiceContext}>
      <ComponentUnderTest />
    </VoiceContext.Provider>
  </AuthContext.Provider>
);
```

### Audio API Mocking

Tests must mock browser audio APIs:

```typescript
// Microphone access
vi.stubGlobal('navigator', {
  mediaDevices: {
    getUserMedia: vi.fn().mockResolvedValue(mockAudioStream)
  }
});

// MediaRecorder
vi.stubGlobal('MediaRecorder', MockMediaRecorder);

// Web Audio API
vi.stubGlobal('AudioContext', MockAudioContext);
```

### Polling Tests

Use fake timers for quality polling:

```typescript
vi.useFakeTimers();
vi.advanceTimersByTime(2000); // Advance to next poll
vi.useRealTimers(); // Restore
```

---

## Test Success Criteria

✅ All 117 tests defined and discoverable via `npm run test`  
✅ All tests fail initially (components don't exist yet)  
✅ Descriptive failure messages indicating what's missing  
✅ MSW handlers respond to all mocked endpoints  
✅ Test fixtures (mock voices, files, responses) available  
✅ No shared state between tests  
✅ No console warnings or unrelated errors  
✅ Each test covers one observable behavior  
✅ Tests follow BDD naming (should...)  
✅ Test IDs (M2.X.Y) consistent and traceable  

---

## Verification Commands

```bash
# Run all M2-RED tests
npm run test -- frontend/tests/voice.spec.tsx

# Run specific category
npm run test -- frontend/tests/voice.spec.tsx -t "M2.1"

# Run with coverage
npm run test -- --coverage frontend/tests/voice.spec.tsx

# Watch mode (for TDD)
npm run test:watch -- frontend/tests/voice.spec.tsx
```

Expected initial result: **117 tests FAIL** (components not implemented yet)

---

## Key Implementation Notes for M2-GREEN

When implementing M2-GREEN to satisfy these tests, the following files must be created:

- **`src/pages/VoiceUpload.tsx`** - Main voice recording/upload page
- **`src/components/VoiceRecorder.tsx`** - Microphone recording component
- **`src/components/VoiceList.tsx`** - Voice library list component
- **`src/components/VoicePlayback.tsx`** - Audio player controls
- **`src/services/voiceClient.ts`** - API client for /voices/* endpoints
- **`src/services/evaluationClient.ts`** - API client for /evaluate/* endpoints
- **`src/hooks/useVoiceQuality.ts`** - Hook for polling quality scores
- **`src/context/VoiceContext.tsx`** - Context + reducer for voice state
- **`src/types/voice.ts`** - TypeScript interfaces

---

## Deferred Features (Out of M2 Scope)

The following are explicitly **NOT** in M2-RED/M2-GREEN:

- ❌ TTS generation (that's M3)
- ❌ Generation history (that's M3)
- ❌ Batch uploads
- ❌ Voice sharing/collaboration
- ❌ Voice duplication
- ❌ Bulk operations
- ❌ Voice tagging/categories
- ❌ Analytics/metrics
- ❌ Advanced audio manipulation (SSML, emotion controls)

---

## Relationship to Other Phases

**Depends On:**
- ✅ M1-GREEN (Authentication with JWT tokens)
- ✅ M0-FOUNDATION (React scaffolding, MSW setup)

**Enables:**
- ➜ M2-GREEN (Voice management implementation)
- ➜ M3-RED (TTS generation tests - will use voices from M2)

---

## Sign-Off

**Specification:** ✅ COMPLETE  
**Test Count:** 117 across 14 categories  
**Ready for:** Test Engineer to implement in Vitest  
**Next Step:** Implement `tests/voice.spec.tsx` with all 117 tests failing  

All tests use observable behavior (what user sees/does), avoid implementation details, and are ready for RED→GREEN→REFACTOR cycle.
