# Requirements: Audio Download & Persistence

**Work Item:** audio-download-persistence  
**Status:** PLANNING  
**Date:** 2026-11-05

---

## Overview

Enable users to download generated audio files and persist generation history across browser sessions and service restarts. Currently, audio is lost when the browser closes or the service restarts because it's stored only in memory.

---

## Functional Requirements

### F1: Download Generated Audio
**Requirement:** User can download any generated audio as a playable WAV file immediately after generation.

- Download button appears in generation results UI
- File format: WAV (same as generated)
- Filename pattern: `{voice-name}_{timestamp}.wav` (e.g., `en-US-Neural2-A_2026-11-05_19-05-30.wav`)
- File is valid, playable WAV with correct audio data
- Download works from browser (no errors, proper content-type headers)

**Acceptance:** User generates audio, clicks Download, receives valid WAV file playable in any audio player.

---

### F2: Persist Audio After Generation
**Requirement:** Generated audio is stored persistently and survives browser close, service restart, and page refresh.

- Audio saved to disk immediately after Google Cloud TTS generates it
- Audio metadata stored in database (text, voice, duration, timestamp)
- Audio accessible for minimum 30 days (configurable retention)
- Automatic cleanup of audio older than retention period
- No data loss on service restart

**Acceptance:** Generate audio → Close browser → Restart service → Audio still exists and can be replayed.

---

### F3: Generation History
**Requirement:** User can view all previous audio generations with metadata.

- New "History" tab or section in UI
- List shows: text, voice name, generation timestamp, duration
- Can scroll/paginate through large history (100+ items)
- Sorted by newest first (most recent at top)
- Shows generation status (complete, failed, etc.)

**Acceptance:** User can see list of all previous generations with full metadata.

---

### F4: Replay Previous Audio
**Requirement:** User can listen to any previous generation from history.

- Click on history entry to play audio
- Audio loads and plays in player
- Same quality as original generation
- Works from browser without re-generating

**Acceptance:** User clicks history entry, audio plays without issues.

---

### F5: Delete Generations
**Requirement:** User can remove unwanted generations to free storage.

- Delete button on each history entry
- Confirmation prompt before deletion
- Removes audio file and database record
- Frees storage space
- Cannot be undone (inform user)

**Acceptance:** User clicks delete, confirms, generation removed from history and disk.

---

### F6: Search/Filter History
**Requirement:** User can find specific generations in history.

- Filter by voice (e.g., show only Hindi)
- Filter by date range
- Search by text content
- Results update without page refresh

**Acceptance:** User selects voice filter, history updates to show only those generations.

---

## Non-Functional Requirements

### NF1: Use Real Services Only
**Constraint:** No mock services or in-memory storage.

- Must use **PostgreSQL** for database (not SQLite, not in-memory)
- Must use **Google Cloud TTS** (verified in current system)
- Must use **disk storage** for audio files (not database BLOB)
- Must not use mock provider for testing this feature
- Audio retrieval uses real service endpoints

**Rationale:** Ensure production-grade reliability for data persistence.

---

### NF2: Storage Scalability
**Constraint:** System must handle thousands of audio files.

- Support at least 10,000 generations
- Support concurrent access (multiple users/requests)
- Fast retrieval (< 1 second for download)
- Efficient disk usage (no duplication)
- Easy to upgrade to cloud storage (S3, Azure Blob) later

**Rationale:** Prepare for scale without rewriting storage layer.

---

### NF3: Performance
**Constraint:** All operations complete within acceptable time.

- Download audio: < 1 second
- List history (20 items): < 500ms
- Search/filter: < 1 second
- Delete generation: < 500ms
- Database queries indexed and optimized

**Rationale:** Ensure responsive user experience.

---

### NF4: Reliability & Safety
**Constraint:** Data must be safe and recoverable.

- No data loss on service crash
- Atomic operations (all-or-nothing)
- Database transactions for consistency
- Regular backups enabled (user's responsibility)
- Graceful error handling (no silent failures)
- Clear error messages to user

**Rationale:** Production-grade reliability.

---

### NF5: Security
**Constraint:** Proper access control and data safety.

- Cannot access other users' files (prepare for multi-user)
- Prevent directory traversal attacks
- Validate file paths before serving
- No sensitive data in error messages
- Log access for audit trail (future)

**Rationale:** Prepare for multi-user deployment.

---

## Out of Scope

The following are explicitly NOT included in this work item:

- ❌ User authentication (separate work item)
- ❌ Voice cloning or voice training (Phase 3)
- ❌ Batch generation or bulk operations
- ❌ Audio editing/trimming/mixing
- ❌ Audio format conversion (only WAV)
- ❌ Cloud storage integration (S3, Azure Blob) - disk only for now
- ❌ Advanced analytics or usage reporting
- ❌ Sharing audio with links or users
- ❌ Audio compression beyond current Google TTS format

These can be added in future phases.

---

## Current State

### Working Components (Verified in Current System)
- ✅ Frontend (React) on port 5173
- ✅ Voice Service (FastAPI) on port 8002
- ✅ TTS Service (FastAPI) on port 8003
- ✅ Google Cloud TTS API integration (real, not mock)
- ✅ CORS middleware enabled
- ✅ Audio generation produces 4+ second WAV files
- ✅ Hindi narration works
- ✅ Five professional voices available

### Current Limitations
- ❌ Audio only in memory (`_pending_inferences` dict)
- ❌ Lost on browser close
- ❌ Lost on service restart
- ❌ No download functionality
- ❌ No history
- ❌ Cannot replay previous generations
- ❌ No persistent storage

### Repository Structure
```
Voice-Narration/
├── frontend/                      # React app
│   └── src/
│       ├── services/ttsApi.ts     # TTS API client
│       └── components/            # UI components
├── voice_narration/
│   ├── simple_voices/             # Voice service (FastAPI)
│   ├── inference/                 # TTS service (FastAPI)
│   │   ├── application.py         # Main app with routes
│   │   └── providers/             # TTS providers (Google, etc.)
│   └── __main__.py
├── docs/.ai/                      # PDD work items
└── ...
```

---

## Dependencies

### External (Already Installed)
- ✅ Google Cloud Text-to-Speech API
- ✅ FastAPI web framework
- ✅ React 18 frontend

### Required for This Work
- 🔄 PostgreSQL 14+ (to be installed)
- 🔄 SQLAlchemy ORM (Python package)
- 🔄 Alembic migrations (Python package)
- 🔄 psycopg2 (PostgreSQL driver)
- 🔄 python-multipart (for file uploads)

---

## Success Criteria

### Functional Acceptance
- [ ] User can download any generated audio as WAV file
- [ ] Downloaded file is playable in any audio player
- [ ] Audio persists across browser close and service restart
- [ ] User can view complete generation history
- [ ] User can replay any previous generation
- [ ] User can delete old generations
- [ ] User can filter/search history

### Technical Acceptance
- [ ] Audio stored on disk (organized by date)
- [ ] Metadata stored in PostgreSQL database
- [ ] All queries indexed and performant
- [ ] No in-memory audio (truly persistent)
- [ ] No mock services in any test
- [ ] Real Google Cloud TTS used throughout
- [ ] Automatic cleanup of old files (30-day retention)

### Quality Acceptance
- [ ] All performance targets met (< 1s download)
- [ ] Zero data loss in any scenario
- [ ] Graceful error handling
- [ ] Clear error messages
- [ ] Production-grade reliability
- [ ] Security best practices followed

### Testing Acceptance
- [ ] Unit tests for storage layer
- [ ] Integration tests for API endpoints
- [ ] E2E tests for full workflow
- [ ] Manual testing in browser
- [ ] Performance testing under load

---

## Constraints

1. **Real Services Only:** Must use PostgreSQL (not SQLite), Google Cloud TTS (not mock), disk storage (not BLOB)
2. **No Breaking Changes:** Must not break existing audio generation functionality
3. **Backward Compatible:** Must work with existing voice service
4. **Production Ready:** Must be safe for production deployment
5. **Scalable:** Must not require rewrite as usage grows

---

## Assumptions

1. PostgreSQL 14+ can be installed and run locally (development)
2. Disk space available for audio storage (at least 10 GB for dev)
3. Google Cloud credentials continue to work
4. Frontend can be extended with new UI components
5. Service endpoints can be added without breaking existing clients

---

## Open Questions

1. Should audio retention be configurable per user or global setting?
2. Should history show failed generations or only completed ones?
3. Should download history be persisted (track what user downloaded)?
4. Should audio files be compressed or stored at full quality?
5. Should there be API rate limiting on downloads?

*To be clarified during Plan creation.*

---

**Prepared for:** Plan creation and decomposition  
**Next Step:** Create detailed Plan with milestones
