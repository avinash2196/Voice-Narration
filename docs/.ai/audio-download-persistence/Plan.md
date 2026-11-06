# Plan: Audio Download & Persistence

**Work Item:** audio-download-persistence  
**Status:** AWAITING APPROVAL  
**Created:** 2026-11-05

---

## Overview

Decomposition of F1-F6 (Download, Persistence, History, Replay, Delete, Search) into a sequence of implementation milestones that deliver persistent audio storage and generation history.

All milestones use real services: PostgreSQL, Google Cloud TTS, disk storage.

---

## Milestone Sequence

### M1: FOUNDATION — Database & Storage Infrastructure
**Type:** FOUNDATION  
**Status:** Pending  
**Owns:** Build infrastructure for persistence layers

Establish executable prerequisites before RED milestones can test persistence behavior.

**Changes:**
- Install and configure PostgreSQL 14+
- Create database schema for generations and voices tables
- Create schema for audit/metadata
- Add Alembic migration infrastructure
- Create disk directory structure for audio storage
- Add required Python dependencies (SQLAlchemy, psycopg2, etc.)
- Configure environment variables for database and storage

**Dependencies:** Current system state (all services running and verified)

**Serves:** M2-M5 (all persistence and download tests need working database and storage)

**Success Criteria:**
- PostgreSQL accepts connections
- Database schema created
- Migrations apply cleanly
- Storage directory structure ready
- All dependencies installed
- Environment variables configured

---

### M2: RED — Generation History Storage Tests
**Type:** RED  
**Status:** Pending  
**Owns:** Requirement F2 (Persist Audio After Generation)

Write tests verifying that audio generation results are persisted to database and disk.

**Tests to Write:**
- Test: Audio metadata stored in database after generation
- Test: Audio file saved to disk after generation
- Test: Audio survives service restart
- Test: Audio accessible by job_id
- Test: Metadata includes text, voice, duration, timestamp
- Test: Database record points to correct file path

**Repository State:** M1 complete, infrastructure ready

**Prerequisite Understanding:**
- Current code stores audio in `_pending_inferences` (in-memory dict)
- Tests need database to be running
- Tests need storage directory to exist

**Success Criteria:**
- All new tests fail with valid RED evidence (no persistence yet)
- Each test clearly expresses one persistence requirement
- No production code modified

---

### M3: GREEN — Implement Persistence Layer
**Type:** GREEN  
**Status:** Pending  
**Owns:** Requirement F2 (Persist Audio After Generation)
**Verifies:** M2 tests

Implement persistent storage: save to disk, record in database.

**Changes:**
- Add `Generation` SQLAlchemy model (id, job_id, text, voice_id, duration, file_path, created_at, expires_at)
- Add database connection pool to TTS service
- Modify `submit_for_inference()` to:
  - Save audio file to disk: `audio_storage/{date}/{voice}_{timestamp}.wav`
  - Create database record with metadata
  - Keep in-memory cache for recent (1 hour) for performance
- Add `AudioStorage` class for file operations
- Add database session management
- Run M2 tests → all pass

**Production Code:** voice_narration/inference/application.py, new storage.py

**Success Criteria:**
- M2 tests all pass
- Audio files stored on disk with correct filenames
- Database records created and queryable
- Audio survives service restart
- No breaking changes to existing generation flow

---

### M4: RED — Download & History Retrieval Tests
**Type:** RED  
**Status:** Pending  
**Owns:** Requirements F1, F3, F4 (Download, History, Replay)

Write tests for new API endpoints: download, list history, get details.

**Tests to Write:**
- Test: `GET /inference/jobs/{job_id}/download` returns WAV file
- Test: Downloaded file is valid WAV format
- Test: `GET /inference/generations` returns paginated list
- Test: History list includes text, voice, duration, timestamp
- Test: `GET /inference/generations/{id}` returns full details
- Test: History sorted by newest first
- Test: Pagination works (skip, limit)

**Repository State:** M3 complete, persistence working

**Success Criteria:**
- All new tests fail with valid RED evidence (no endpoints yet)
- Each test clearly expresses one endpoint requirement
- No production code modified

---

### M5: GREEN — Implement Download & History Endpoints
**Type:** GREEN  
**Status:** Pending  
**Owns:** Requirements F1, F3, F4 (Download, History, Replay)
**Verifies:** M4 tests

Add API endpoints for download, history retrieval, and generation details.

**Endpoints to Add:**
- `GET /inference/jobs/{job_id}/download` → returns WAV file as attachment
- `GET /inference/generations?skip=0&limit=20` → returns paginated list
- `GET /inference/generations/{id}` → returns single generation details
- Update response schemas to include all metadata

**Changes:**
- Add routes to TTS service (application.py)
- Add database queries (session management)
- Add file streaming for download (correct headers)
- Add pagination logic
- Run M4 tests → all pass

**Production Code:** voice_narration/inference/application.py

**Success Criteria:**
- M4 tests all pass
- Download endpoint streams valid WAV file
- History endpoints return correct data
- Pagination works
- No breaking changes

---

### M6: RED — Delete & Cleanup Tests
**Type:** RED  
**Status:** Pending  
**Owns:** Requirement F5 (Delete Generations)

Write tests for deletion and automatic cleanup.

**Tests to Write:**
- Test: `DELETE /inference/generations/{id}` removes record and file
- Test: File deleted from disk
- Test: Database record deleted
- Test: Cannot download after delete
- Test: Cleanup job removes files older than 30 days
- Test: Expired records marked in database

**Repository State:** M5 complete, endpoints working

**Success Criteria:**
- All new tests fail with valid RED evidence (no delete yet)
- Each test clearly expresses one delete/cleanup requirement
- No production code modified

---

### M7: GREEN — Implement Delete & Cleanup
**Type:** GREEN  
**Status:** Pending  
**Owns:** Requirement F5 (Delete Generations)
**Verifies:** M6 tests

Implement deletion logic and cleanup scheduler.

**Changes:**
- Add `DELETE /inference/generations/{id}` endpoint
- Implement file deletion (remove from disk)
- Implement database deletion (soft delete or hard delete)
- Add cleanup job (daily, removes files older than retention period)
- Add `expires_at` field update logic
- Run M6 tests → all pass

**Production Code:** voice_narration/inference/application.py, new cleanup.py

**Success Criteria:**
- M6 tests all pass
- Delete endpoint removes file and record
- Cleanup job works
- Old files automatically removed
- No breaking changes

---

### M8: RED — Search & Filter Tests
**Type:** RED  
**Status:** Pending  
**Owns:** Requirement F6 (Search/Filter History)

Write tests for filtering and searching generation history.

**Tests to Write:**
- Test: Filter by voice_id returns only that voice's generations
- Test: Filter by date range works
- Test: Search by text finds matching generations
- Test: Multiple filters combine (AND logic)
- Test: Results sorted correctly
- Test: Filters work with pagination

**Repository State:** M7 complete, delete/cleanup working

**Success Criteria:**
- All new tests fail with valid RED evidence (no filters yet)
- Each test clearly expresses one filter requirement
- No production code modified

---

### M9: GREEN — Implement Search & Filters
**Type:** GREEN  
**Status:** Pending  
**Owns:** Requirement F6 (Search/Filter History)
**Verifies:** M8 tests

Add filtering and search capabilities to history endpoints.

**Changes:**
- Update `GET /inference/generations` to accept filters:
  - `voice_id` (exact match)
  - `created_at_from`, `created_at_to` (date range)
  - `search` (text search in script field)
- Implement efficient database queries with WHERE clauses
- Build query dynamically based on filters provided
- Run M8 tests → all pass

**Production Code:** voice_narration/inference/application.py

**Success Criteria:**
- M8 tests all pass
- All filters work individually and combined
- Search returns correct results
- Performance acceptable (< 1s)
- No breaking changes

---

### M10: RED — Frontend Integration Tests
**Type:** RED  
**Status:** Pending  
**Owns:** Frontend delivery of F1-F6 to user

Write tests for frontend components handling download, history, replay, delete.

**Tests to Write:**
- Test: Download button appears on generation result
- Test: Clicking download triggers file download
- Test: History tab shows list of generations
- Test: History list displays text, voice, timestamp, duration
- Test: Click generation in history replays audio
- Test: Delete button appears and works
- Test: Filters/search update history without reload

**Repository State:** M9 complete, all backend APIs ready

**Success Criteria:**
- All new tests fail with valid RED evidence (no UI yet)
- Each test clearly expresses one UI requirement
- No production code modified

---

### M11: GREEN — Implement Frontend Components
**Type:** GREEN  
**Status:** Pending  
**Owns:** Frontend delivery of F1-F6
**Verifies:** M10 tests

Add UI components for download, history, replay, delete.

**Changes:**
- Update `GenerationResult` component to add Download button
- Add new `HistoryTab` component showing generation list
- Add `GenerationItem` component (text, voice, time, duration, actions)
- Add delete button with confirmation modal
- Add filter/search UI (voice dropdown, date picker)
- Integrate with updated ttsApi endpoints
- Run M10 tests → all pass

**Production Code:** frontend/src/components/*, frontend/src/services/ttsApi.ts

**Success Criteria:**
- M10 tests all pass
- Download button works
- History displays correctly
- Replay works from history
- Delete works with confirmation
- Filters work
- No breaking changes

---

### M12: OTHER — End-to-End Testing & Documentation
**Type:** OTHER  
**Status:** Pending  
**Owns:** Verification of entire flow, documentation

Verify complete flow and document the feature.

**Before Evidence:**
- Current system state: no persistence, no history, no downloads
- Services running, generation works

**After Evidence:**
- User can generate audio → downloads it → close browser → restart service → replay from history
- All acceptance criteria met
- Performance targets met (< 1s download, < 500ms history list)
- Documentation complete

**Manual Testing:**
1. Generate audio in English
2. Download file → play in external audio player
3. Generate audio in Hindi
4. Close and restart browser
5. History shows both generations
6. Click to replay → audio plays
7. Filter by Hindi → shows only Hindi
8. Delete one → removed from history
9. Restart service → history still there

**No Production Code Changes:** Only testing and documentation

**Success Criteria:**
- Complete end-to-end flow works
- All performance targets met
- Zero data loss
- Documented for users
- All manual tests pass

---

## Requirement Traceability

| Requirement | Owning Milestone | Verifying Milestone |
|------------|-----------------|-------------------|
| F1: Download Audio | M5 (GREEN) | M4 (RED) |
| F2: Persist Audio | M3 (GREEN) | M2 (RED) |
| F3: Generation History | M5 (GREEN) | M4 (RED) |
| F4: Replay Previous | M5 (GREEN) | M4 (RED) |
| F5: Delete Generations | M7 (GREEN) | M6 (RED) |
| F6: Search/Filter | M9 (GREEN) | M8 (RED) |
| NF1: Real Services Only | M1 (FOUNDATION) | M3, M5, M7, M9 (GREEN) |
| NF2: Scalability | M1 (FOUNDATION), M3 (GREEN) | M12 (OTHER) |
| NF3: Performance | M3, M5, M7, M9 (GREEN) | M12 (OTHER) |
| NF4: Reliability | M1, M3, M7 (FOUNDATION, GREEN) | M12 (OTHER) |
| NF5: Security | M5 (GREEN) | M12 (OTHER) |

---

## Decomposition Decisions

**Split into 12 milestones because:**

1. **FOUNDATION separate:** Database and storage infrastructure must exist before any persistence tests can run (Conditional SETUP / FOUNDATION rule).

2. **Persistence layer-wise:** Persistence (M2-M3) tested separately from API endpoints because it's a foundational concern that must work before download/history can be built on it.

3. **API endpoints layer-wise:** Download/history endpoints (M4-M5) separate from persistence because they're a distinct architectural layer that depends on working persistence.

4. **Delete separate:** Deletion and cleanup (M6-M7) tested separately because they're a distinct capability with different risk (data loss).

5. **Search separate:** Search/filters (M8-M9) separate because they add complexity to queries and can be tested independently once basic history works.

6. **Frontend separate:** Frontend (M10-M11) separate from backend because it's a distinct layer and requires all backend APIs ready first.

7. **E2E testing separate:** End-to-end testing (M12) separate because it verifies the complete integrated system and cannot run until all milestones before it are complete.

---

## Current State & Blockers

**Working & Verified:**
- ✅ Frontend (React) running on 5173
- ✅ Voice Service running on 8002
- ✅ TTS Service running on 8003
- ✅ Google Cloud TTS integration (real, not mock)
- ✅ CORS enabled
- ✅ Audio generation: 4+ seconds, real WAV files
- ✅ Hindi narration working

**Not Working Yet:**
- ❌ PostgreSQL (need to install)
- ❌ Audio persistence (only in-memory)
- ❌ Download endpoints
- ❌ History endpoints
- ❌ Frontend UI for history/download

**No Blockers:** Work can proceed immediately after M1 FOUNDATION.

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Database connection failure | HIGH | Use connection pooling, test connections on startup, fallback logging |
| Disk full during generation | HIGH | Check disk space before saving, cleanup old files proactively |
| Concurrent access conflicts | MEDIUM | Use database transactions, test under load |
| Performance degradation | MEDIUM | Index queries, cache recent results, test with large history |
| Data loss on crash | HIGH | Atomic transactions, backups enabled, test recovery |
| Security: directory traversal | MEDIUM | Validate file paths, use safe path operations, isolate storage |

---

## Verification Commands

**M1 (FOUNDATION):**
```bash
psql -U postgres -d voice_narration -c "SELECT 1"  # DB connection
ls -la audio_storage/                               # Storage directory
python -c "import sqlalchemy; print('OK')"          # Dependencies
```

**M2 & M3 (RED & GREEN):**
```bash
pytest tests/test_persistence.py -v                 # Run all persistence tests
# Expect: all pass after M3, all fail after M2
```

**M4 & M5 (RED & GREEN):**
```bash
pytest tests/test_download.py tests/test_history.py -v  # Run all API tests
# Expect: all pass after M5, all fail after M4
```

**M6 & M7 (RED & GREEN):**
```bash
pytest tests/test_delete.py tests/test_cleanup.py -v    # Run delete tests
# Expect: all pass after M7, all fail after M6
```

**M8 & M9 (RED & GREEN):**
```bash
pytest tests/test_search.py -v                      # Run search tests
# Expect: all pass after M9, all fail after M8
```

**M10 & M11 (RED & GREEN):**
```bash
npm run test -- --testPathPattern="history|download"    # Frontend tests
# Expect: all pass after M11, all fail after M10
```

**M12 (OTHER):**
```bash
# Manual E2E test sequence
# Generate → Download → Close browser → Restart → Replay → Filter → Delete
# Expected: all operations succeed, audio persists
```

---

## Constraints & Exclusions

**Must:**
- Use PostgreSQL (not SQLite, not in-memory)
- Use Google Cloud TTS (not mock)
- Use disk storage (not database BLOB)
- Not break existing audio generation
- Complete all milestones in order

**Must Not:**
- Add user authentication
- Implement voice cloning
- Add audio format conversion
- Integrate cloud storage (S3, etc.)
- Modify existing tests (only add new ones)

---

## Success Criteria

**All Milestones Complete When:**
1. ✅ Audio persists across service restart
2. ✅ Download endpoint returns valid WAV file
3. ✅ History endpoint returns all generations
4. ✅ Replay works from history
5. ✅ Delete removes generation
6. ✅ Search/filter works
7. ✅ Frontend UI complete
8. ✅ Manual E2E testing passes
9. ✅ Performance: download < 1s, history < 500ms
10. ✅ Zero data loss scenarios tested

---

## Execution Status

| Milestone | Type | Status | Evidence |
|-----------|------|--------|----------|
| M1 | FOUNDATION | Pending | — |
| M2 | RED | Pending | — |
| M3 | GREEN | Pending | — |
| M4 | RED | Pending | — |
| M5 | GREEN | Pending | — |
| M6 | RED | Pending | — |
| M7 | GREEN | Pending | — |
| M8 | RED | Pending | — |
| M9 | GREEN | Pending | — |
| M10 | RED | Pending | — |
| M11 | GREEN | Pending | — |
| M12 | OTHER | Pending | — |

---

## Approval Status

**Plan Status:** ⏳ AWAITING REVIEW & APPROVAL

This Plan is ready for human review. Requirements and milestones are complete. Once approved, M1 FOUNDATION Implementation Plan will be created.

**Next Step:** Approve Plan → Create M1 Implementation Plan → Execute

---

**Created:** 2026-11-05  
**Last Updated:** 2026-11-05  
**Work Item:** audio-download-persistence
