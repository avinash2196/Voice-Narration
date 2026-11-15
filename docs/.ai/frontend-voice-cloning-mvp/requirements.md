# Frontend Voice Cloning MVP - Requirements

**Work Item:** `frontend-voice-cloning-mvp`  
**Status:** Requirements Captured ✅  
**Tech Stack:** React  
**Scope:** MVP Only  
**Date:** 2026-10-31

---

## 1. Overview

Voice-Narration Frontend MVP enables users to:
1. **Upload voice samples** (voice cloning source)
2. **Generate speech** in their voice using different texts
3. **Manage & replay** generated content

---

## 2. Functional Requirements

### 2.1 Authentication (FR-AUTH)

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-AUTH-001 | User can register with email + password | Core | User decision |
| FR-AUTH-002 | User can login with email + password | Core | User decision |
| FR-AUTH-003 | Session persists using JWT token | Core | User decision |
| FR-AUTH-004 | User can logout and clear session | Core | User decision |
| FR-AUTH-005 | User can reset password via email link | Core | User decision |
| FR-AUTH-006 | Tokens auto-refresh before expiry | Core | User decision |

**API Integration:** Auth Service (Port 8001)

**Success Criteria:** User registration → login → logout flow works end-to-end

---

### 2.2 Voice Sample Management (FR-VOICE)

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-VOICE-001 | User can upload voice sample (WAV/MP3) | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-VOICE-002 | User can record voice in browser (Web Audio API) | Core | User decision: "both recording + upload" |
| FR-VOICE-003 | Max voice file size: 100 MB | Constraint | User decision |
| FR-VOICE-004 | Real-time quality feedback from backend | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-VOICE-005 | Accept/reject quality flow (approve only if ≥ threshold) | Core | FRONTEND_REQUIREMENTS.md MVP + AI Evaluation Service |
| FR-VOICE-006 | Store voice metadata (name, language, duration) | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-VOICE-007 | User can preview uploaded voice | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-VOICE-008 | Quality score displayed (0-100) | Core | From M015 AI Evaluation Service |

**API Integration:** 
- Voices Service (Port 8002): upload, list, get, update, delete
- AI Evaluation Service (Port 8006): evaluate quality

**Success Criteria:** 
- User uploads voice → quality feedback displays
- Quality ≥ threshold → voice saved
- Quality < threshold → rejection with reason shown

---

### 2.3 TTS Generation / Voice Cloning Output (FR-TTS)

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-TTS-001 | User enters text for TTS generation | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-TTS-002 | Max text length: 20,000 characters | Constraint | User decision |
| FR-TTS-003 | User selects voice from dropdown (approved samples only) | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-TTS-004 | Generate button submits job to Jobs Service | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-TTS-005 | Real-time job status visible (pending → processing → complete) | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-TTS-006 | Audio player displays result when ready | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-TTS-007 | User can download audio as WAV file | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-TTS-008 | Rate limit: max 10 generations per hour per user | Constraint | User decision |
| FR-TTS-009 | Support Hindi (hi-IN) + English (en-US) text | Core | From M022/M024 backend |
| FR-TTS-010 | Error handling if generation fails | Core | Best practice |

**API Integration:**
- Jobs Service (Port 8003): submit job, poll status
- Inference Service (Port 8005): generate audio, get output
- Rate limiting enforced by backend

**Success Criteria:**
- User submits text → job created
- Status updates in real-time
- Audio plays in browser
- Download works

---

### 2.4 History & Playback (FR-HISTORY)

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-HISTORY-001 | List all generated audios for user | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-HISTORY-002 | Show metadata (text, voice, date, duration) | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-HISTORY-003 | Inline playback of generated audio | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-HISTORY-004 | User can delete generated audio | Core | FRONTEND_REQUIREMENTS.md MVP |

**API Integration:** Jobs Service (Port 8003), Voices Service (Port 8002)

**Success Criteria:** History displays all past generations with playback

---

### 2.5 Settings (FR-SETTINGS)

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-SETTINGS-001 | User can view profile (email, name) | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-SETTINGS-002 | User can change password | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-SETTINGS-003 | User can view privacy policy | Core | FRONTEND_REQUIREMENTS.md MVP |
| FR-SETTINGS-004 | User can accept/view consent status | Core | FRONTEND_REQUIREMENTS.md MVP |

**API Integration:** Consent Service (Port 8004)

**Success Criteria:** Settings page fully functional

---

## 3. Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-TECH-001 | Framework: React | Constraint | User decision |
| NFR-TECH-002 | Browser: Chrome (minimum) | Constraint | User decision |
| NFR-HOSTING-001 | Support local development + Docker | Constraint | User decision |
| NFR-PERF-001 | Audio player loads in < 2 seconds | Performance | Best practice |
| NFR-PERF-002 | UI responds to user actions in < 500ms | Performance | Best practice |
| NFR-SEC-001 | JWT token stored securely (no XSS) | Security | Standard practice |
| NFR-SEC-002 | HTTPS enforced in production | Security | Standard practice |
| NFR-COMPAT-001 | Support Chrome latest 2 versions | Compatibility | User decision |

---

## 4. Data Models

### 4.1 User
```javascript
{
  id: uuid,
  email: string (unique),
  password_hash: string,
  full_name: string,
  created_at: timestamp,
  updated_at: timestamp
}
```
**Provenance:** User decision - standard auth model

### 4.2 VoiceSample (Voice Cloning Source)
```javascript
{
  id: uuid,
  user_id: uuid,
  name: string,
  language: string,                    // e.g., "hi-IN", "en-US"
  duration_seconds: float,
  audio_path: string,
  quality_score: float (0-100),        // From AI Evaluation Service M015
  quality_status: "pending" | "approved" | "rejected",
  is_default: boolean,
  created_at: timestamp,
  updated_at: timestamp
}
```
**Provenance:** FRONTEND_REQUIREMENTS.md + AI Evaluation Service (M015)

### 4.3 GeneratedAudio (Voice Cloning Output)
```javascript
{
  id: uuid,
  user_id: uuid,
  voice_sample_id: uuid,              // References VoiceSample
  input_text: string,                 // Max 20,000 chars
  output_audio_path: string,          // WAV file, 16kHz mono 16-bit
  duration_seconds: float,
  status: "pending" | "processing" | "complete" | "failed",
  created_at: timestamp,
  completed_at: timestamp
}
```
**Provenance:** FRONTEND_REQUIREMENTS.md + M024 production inference code

---

## 5. API Integration

### 5.1 Auth Service (Port 8001)
```
POST   /auth/register        → User registration
POST   /auth/login           → User login
POST   /auth/refresh         → Token refresh
POST   /auth/logout          → Logout user
POST   /auth/password-reset  → Password reset
```
**Source:** `voice_narration/auth/application.py`

### 5.2 Voices Service (Port 8002)
```
POST   /voices/upload         → Upload voice sample
GET    /voices/list          → List user's voice samples
GET    /voices/{id}          → Get voice details
PATCH  /voices/{id}          → Update metadata
DELETE /voices/{id}          → Delete voice sample
```
**Source:** `voice_narration/voices/application.py`

### 5.3 Inference/TTS Service (Port 8005)
```
POST   /inference/jobs/{job_id}/infer   → Generate audio
GET    /inference/jobs/{job_id}/output  → Get audio result
GET    /inference/backends              → List backends
```
**Source:** `voice_narration/inference/application.py` (M024 GREEN)

### 5.4 Jobs Service (Port 8003)
```
GET    /jobs/{job_id}        → Get job status
GET    /jobs/history         → List user's jobs
```
**Source:** `voice_narration/jobs/application.py`

### 5.5 AI Evaluation Service (Port 8006)
```
POST   /evaluate             → Evaluate audio quality
GET    /evaluate/{id}        → Get quality report
```
**Source:** `voice_narration/ai/application.py` (M015)

### 5.6 Consent Service (Port 8004)
```
POST   /consent/record       → Record user consent
GET    /consent/status       → Get consent status
```
**Source:** `voice_narration/consent/application.py`

---

## 6. UI Components

### 6.1 Authentication Pages
- Login form (email, password)
- Register form (email, password, confirm)
- Password reset form
- Session timeout warning

### 6.2 Voice Management
- Upload area (drag-drop + file select)
- Record button (browser audio recording)
- Quality feedback display (score + message)
- Voice list (with approve/reject buttons)
- Preview player

### 6.3 TTS Generator
- Text input (textarea, char counter)
- Voice selector (dropdown)
- Generate button (with loading state)
- Progress indicator
- Audio player (play, pause, download)
- Error message display

### 6.4 History
- Generated audio list (table or cards)
- Metadata display (text, voice, date, duration)
- Playback player per item
- Delete button

### 6.5 Settings
- Profile display
- Password change form
- Privacy policy link
- Consent checkbox

---

## 7. Production Constraints (Explicit)

| Constraint | Value | Source |
|---|---|---|
| Max voice file size | 100 MB | User decision |
| Max TTS text length | 20,000 characters | User decision |
| Rate limit | 10 generations per hour per user | User decision |
| Browser support | Chrome | User decision |
| Audio format (input) | WAV, MP3 | User decision: "both recording + upload" |
| Audio format (output) | WAV, 16kHz mono 16-bit | From M024 production code |
| TTS languages | Hindi (hi-IN), English (en-US) | From M022 provider registry |
| Hosting | Local + Docker | User decision |

---

## 8. Operational Characteristics

| Characteristic | Specification | Source |
|---|---|---|
| **Availability** | User sessions persist across browser refresh | JWT token management |
| **Performance** | Job status updates in < 2 seconds | Real-time polling/WebSocket |
| **Reliability** | Failed TTS jobs show error message | Error handling |
| **Usability** | First-time user can upload + generate in < 5 minutes | MVP scope design |
| **Scalability** | Support single user locally | Local development + Docker |
| **Maintainability** | React component-based architecture | Tech stack decision |

---

## 9. Success Criteria

### 9.1 MVP Completion
- [ ] User registration works (creates account)
- [ ] User login works (JWT token issued)
- [ ] User can upload voice sample
- [ ] Quality feedback displayed (AI Evaluation Service response)
- [ ] User can generate TTS in their voice
- [ ] Audio plays in browser
- [ ] Audio can be downloaded
- [ ] Generation history shows all past audios
- [ ] Settings page fully functional
- [ ] Rate limiting enforced (10/hour)
- [ ] File size limit enforced (100 MB)
- [ ] Text length limit enforced (20K chars)

### 9.2 Browser Testing
- [ ] Chrome desktop version works
- [ ] Audio recording works in Chrome
- [ ] File upload works in Chrome
- [ ] Playback works in Chrome

### 9.3 Backend Integration
- [ ] All 6 backend services respond correctly
- [ ] JWT token exchanges work with Auth Service
- [ ] Voice uploads received by Voices Service
- [ ] Quality scores returned by AI Evaluation
- [ ] TTS generation works with Inference Service
- [ ] Job status tracked via Jobs Service

---

## 10. Exclusions (Explicit Non-Requirements for MVP)

| Feature | Reason | Phase |
|---|---|---|
| Multiple voice samples per user | Deferred to Phase 2 | Phase 2 |
| Batch TTS generation | Deferred to Phase 2 | Phase 2 |
| Advanced voice controls (emotion, accent) | Deferred to Phase 3 | Phase 3 |
| Analytics dashboard | Deferred to Phase 3 | Phase 3 |
| Collaboration/sharing | Deferred to Phase 3 | Phase 3 |
| Voice waveform visualization | Deferred to Phase 2 | Phase 2 |
| Mobile app | Out of scope | Future |
| Video integration | Out of scope | Future |
| Real-time voice conversion | Out of scope | Future |

---

## 11. Relationship to Product-Level Requirements

**Product Context:** Voice-Narration is a multi-milestone platform for user voice cloning + TTS generation.

| Product Milestone | Frontend MVP Dependency | Status |
|---|---|---|
| M015: AI Evaluation | Quality feedback requires Service | ✅ Implemented |
| M020: Inference Adapter | TTS generation requires Service | ✅ Implemented |
| M022: Multi-Provider TTS | Google TTS backend required | ✅ Implemented |
| M024: Production Inference | End-to-end workflow ready | ✅ Implemented |
| M025-M030: User Enrollment | Will use this Frontend | 🔄 Planned |

**The Frontend MVP directly depends on all 7 backend services being operational** (currently all ready ✅)

---

## 12. Provenance Check

Every requirement is traced to source:

### User Decisions (Verified from Task Input)
- Tech stack: React
- Scope: MVP only (Phase 2 & 3 deferred to separate doc)
- Hosting: Local + Docker
- Browser: Chrome
- Audio: Both browser recording + file upload
- Constraints: 100 MB file, 20K chars text, 10 gen/hour rate limit

### Repository Evidence
- **Auth Service:** `voice_narration/auth/application.py`
- **Voices Service:** `voice_narration/voices/application.py`
- **Jobs Service:** `voice_narration/jobs/application.py`
- **Inference Service:** `voice_narration/inference/application.py` (M024 GREEN)
- **AI Evaluation:** `voice_narration/ai/application.py` (M015)
- **Consent Service:** `voice_narration/consent/application.py`
- **Requirements Source:** `docs/planning/FRONTEND_REQUIREMENTS.md` (created this session)

### Derived Specifications
- Audio format (WAV, 16kHz mono 16-bit) from `voice_narration/inference/production.py`
- TTS languages (hi-IN, en-US) from `voice_narration/inference/registry.py`
- Voice quality scoring from `tests/test_linguistic_chunking_and_controls.py`

---

## 13. Clarification Log

**Q1. Work item name?**  
**A1.** `frontend-voice-cloning-mvp`

**Q2. Tech stack?**  
**A2.** React

**Q3. Scope - MVP only or all phases?**  
**A3.** MVP only in requirements, Phase 2 & 3 in separate planning doc

**Q4. Hosting?**  
**A4.** Local development + Docker

**Q5. Browser support?**  
**A5.** Chrome

**Q6. Audio input - recording, upload, or both?**  
**A6.** Both browser recording AND file upload

**Q7. Production constraints - file size, text length, rate limit?**  
**A7.** 100 MB file, 20,000 characters text, 10 generations per hour

---

## 14. Status

**✅ Requirements Captured**  
**Status:** Ready for Planning phase  
**Next Step:** Create Plan.md (separate task - Option A workflow)

---

**Last Updated:** 2026-10-31  
**Created By:** PDD Planner Agent  
**Approval Status:** Awaiting user review

