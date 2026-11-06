# Frontend Architecture Review & Flow Analysis

**Date**: November 1, 2026  
**Status**: ⚠️ CRITICAL - Frontend Missing Core Authentication Flow  
**Review Basis**: APPLICATION_WORKFLOW.md + Backend Architecture

---

## Executive Summary

The frontend is **incomplete** and missing critical components:

### What's Missing:
1. ❌ **No Login/Authentication Pages** - No route to `/auth/login` or `/auth/signup`
2. ❌ **No Protected Routes** - App allows direct access to `/voices` and `/tts` without auth token
3. ❌ **No Session Restoration** - Auth context doesn't check localStorage on app load
4. ❌ **No Logout Flow** - No logout button or flow to clear session
5. ❌ **No Error Handling** - Missing token expiration, refresh token logic
6. ❌ **Hardcoded Backend URLs** - No proper API configuration management

### Current Problems:
- Users see "Not authenticated. Please log in." immediately
- No way to log in from the frontend
- App loads directly to `/` (homepage) without checking auth state
- No authentication guard on protected routes

---

## Intended Flow (Per Architecture Docs)

### Backend Architecture (9 Microservices)

```
┌─────────────┐
│   Client    │ (React Frontend - PORT 5173)
└──────┬──────┘
       │
       ├─→ Auth Service (PORT 8001) → POST /auth/login, POST /auth/register
       ├─→ Voice Service (PORT 8002) → POST /voices, GET /voices
       ├─→ TTS Service (PORT 8003) → POST /jobs, GET /jobs/{id}
       ├─→ Evaluation Service (PORT 8006)
       └─→ Jobs Service (PORT 8007)
```

### Complete User Flow

```
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: REGISTRATION & LOGIN                               │
└─────────────────────────────────────────────────────────────┘

User opens app (http://localhost:5173)
    ↓
CURRENT: Lands on Homepage with "Not authenticated" error
SHOULD: Lands on Authentication Check
    ↓
    ├─ Is token in localStorage? 
    │   ├─ YES → Check if token valid with Auth Service
    │   │        ├─ Valid → Restore session → Redirect to /voices or /tts
    │   │        └─ Invalid → Clear localStorage → Redirect to /auth/login
    │   │
    │   └─ NO → Redirect to /auth/login
    ↓
Login Page (/auth/login)
    ├─ Email input
    ├─ Password input
    └─ Login button
    ↓
User submits email + password
    ↓
POST http://localhost:8001/auth/login
    ├─ Body: { email, password }
    └─ Response: { token, refreshToken, user }
    ↓
Save to localStorage + Update Auth Context
    ├─ localStorage[auth_token] = token
    ├─ localStorage[refresh_token] = refreshToken
    └─ AuthContext.dispatch({type: 'LOGIN', payload: {user, token, refreshToken}})
    ↓
Redirect to /voices (Voice Management)

┌─────────────────────────────────────────────────────────────┐
│ STEP 2: VOICE MANAGEMENT (/voices)                         │
└─────────────────────────────────────────────────────────────┘

User arrives at /voices
    ↓
ProtectedRoute checks auth.token
    ├─ Has token → Allow access
    └─ No token → Redirect to /auth/login
    ↓
Choose Tab: Record OR Upload OR Library
    ↓
Record/Upload Voice
    ├─ POST http://localhost:8002/voices
    ├─ Include: Bearer token in Authorization header
    ├─ Body: { FormData with audio file }
    └─ Response: { voice_id, status: "pending", created_at }
    ↓
Voice added to library with status="PENDING"
Wait for admin approval...

┌─────────────────────────────────────────────────────────────┐
│ STEP 3: TTS GENERATION (/tts)                              │
└─────────────────────────────────────────────────────────────┘

User navigates to /tts
    ↓
ProtectedRoute checks auth.token
    ├─ Has token → Allow access
    └─ No token → Redirect to /auth/login
    ↓
Form appears:
    ├─ Text Input (0-5000 chars)
    ├─ Voice Selector (dropdown with APPROVED voices only)
    ├─ Provider Selector (Google, ElevenLabs, Azure)
    └─ Generate Button
    ↓
User enters text + selects voice + selects provider
    ↓
POST http://localhost:8003/jobs
    ├─ Include: Bearer token in Authorization header
    ├─ Body: { text, voice_id, provider }
    └─ Response: { job_id, status: "queued" }
    ↓
Polling starts: GET http://localhost:8003/jobs/{job_id}
    ├─ Every 2 seconds
    ├─ Include: Bearer token in Authorization header
    └─ Response: { status, progress, audio_url }
    ↓
Progress bar updates (0% → 100%)
    ↓
When status="completed"
    ├─ Stop polling
    ├─ Show audio player with generated audio
    └─ Add to generation history
    ↓
User can play, seek, download audio

┌─────────────────────────────────────────────────────────────┐
│ STEP 4: LOGOUT                                              │
└─────────────────────────────────────────────────────────────┘

User clicks "Logout" button (top right)
    ↓
Clear localStorage (auth_token, refresh_token)
    ↓
Dispatch logout action
    ├─ AuthContext → { user: null, token: null, authenticated: false }
    └─ Reset VoiceContext, TTSContext
    ↓
Redirect to /auth/login
```

---

## Current Frontend Structure (Incomplete)

### Existing Files:
```
frontend/src/
├── context/
│   ├── AuthContext.tsx ✅ (reducer + state management)
│   ├── VoiceContext.tsx ✅ (voice state)
│   └── TTSContext.tsx ✅ (TTS state)
│
├── pages/
│   ├── Auth/
│   │   ├── Login.tsx ✅ (exists but not routed)
│   │   └── Signup.tsx ✅ (exists but not routed)
│   ├── VoiceManagement.tsx ✅ (3 tabs: record, upload, library)
│   └── TextToSpeech.tsx ✅ (form + progress + player + history)
│
├── components/
│   ├── VoiceRecorder.tsx ✅ (record audio)
│   ├── VoiceUpload.tsx ✅ (upload file)
│   ├── VoiceLibrary.tsx ✅ (list voices)
│   ├── TextToSpeechInput.tsx ✅
│   ├── VoiceSelector.tsx ✅
│   ├── ProviderSelector.tsx ✅
│   ├── GenerationSubmitForm.tsx ✅
│   ├── GenerationProgress.tsx ✅
│   ├── AudioPlayer.tsx ✅
│   ├── GenerationHistory.tsx ✅
│   ├── RateLimitDisplay.tsx ✅
│   ├── GenerationErrorDisplay.tsx ✅
│   └── QualityMetrics.tsx ✅
│
├── services/
│   ├── api/
│   │   ├── authClient.ts ✅ (calls Auth Service)
│   │   ├── httpClient.ts ✅ (HTTP wrapper)
│   │   └── voiceApi.ts ✅ (calls Voice Service)
│   ├── ttsApi.ts ✅ (calls TTS Service)
│   └── ttsPollingService.ts ✅
│
├── hooks/
│   ├── useAuth.ts ✅
│   ├── useVoice.ts ✅
│   └── useTTS.ts ✅
│
├── middleware/
│   └── tokenInterceptor.ts ✅
│
├── App.tsx ❌ (PROBLEM: No auth routes, no protected routes)
└── index.css ✅
```

### Key Problems in App.tsx:

```tsx
function App() {
  return (
    <Router>
      <AuthProvider>
        <VoiceProvider>
          <TTSProvider>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/voices" element={<VoiceManagement />} />
              <Route path="/tts" element={<TextToSpeech />} />
              {/* ❌ MISSING: /auth/login and /auth/signup routes */}
              {/* ❌ MISSING: Protected route guards */}
              {/* ❌ MISSING: Route that checks auth on app load */}
            </Routes>
          </TTSProvider>
        </VoiceProvider>
      </AuthProvider>
    </Router>
  );
}
```

---

## What Needs to Be Built

### 1. Protected Route Component
```tsx
// frontend/src/components/ProtectedRoute.tsx
export function ProtectedRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/auth/login" replace />;
  }
  
  return <>{children}</>;
}
```

### 2. Auth Layout Component
```tsx
// frontend/src/layouts/AuthLayout.tsx
// Minimal layout for login/signup pages (no navbar, no voice management nav)
```

### 3. Session Restoration Effect
```tsx
// In AuthProvider useEffect on mount:
// 1. Check localStorage for token
// 2. If token exists, call GET /auth/me (internal API)
// 3. If valid, restore session with user data
// 4. If invalid, clear localStorage
```

### 4. Updated App.tsx Routes
```tsx
<Routes>
  {/* Public routes */}
  <Route path="/auth/login" element={<Login />} />
  <Route path="/auth/signup" element={<Signup />} />
  
  {/* Protected routes */}
  <Route path="/" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
  <Route path="/voices" element={<ProtectedRoute><VoiceManagement /></ProtectedRoute>} />
  <Route path="/tts" element={<ProtectedRoute><TextToSpeech /></ProtectedRoute>} />
  
  {/* Fallback */}
  <Route path="*" element={<Navigate to="/" replace />} />
</Routes>
```

### 5. Updated HomePage
```tsx
// Current: Shows workflow info + navigation buttons
// Should also have: Logout button in top right corner
```

### 6. API Configuration
```tsx
// frontend/src/utils/config.ts
export const API_CONFIG = {
  AUTH_SERVICE: process.env.REACT_APP_AUTH_API || 'http://localhost:8001',
  VOICE_SERVICE: process.env.REACT_APP_VOICE_API || 'http://localhost:8002',
  TTS_SERVICE: process.env.REACT_APP_TTS_API || 'http://localhost:8003',
};
```

### 7. Environment Files
```
.env.local (development)
AUTH_API_BASE_URL=http://localhost:8001
VOICE_API_BASE_URL=http://localhost:8002
TTS_API_BASE_URL=http://localhost:8003
```

---

## Backend Service Ports (From Architecture Docs)

| Service | Port | Endpoint |
|---------|------|----------|
| **Auth Service** | 8001 | `http://localhost:8001` |
| **Voice Service** | 8002 | `http://localhost:8002` |
| **TTS Service** | 8003 | `http://localhost:8003` |
| **Evaluation Service** | 8006 | `http://localhost:8006` |
| **Jobs Service** | 8007 | `http://localhost:8007` |

---

## Implementation Priority

### Phase 1: Authentication (CRITICAL - Must do first)
- [ ] Create ProtectedRoute component
- [ ] Create AuthLayout for auth pages
- [ ] Add session restoration effect in AuthProvider
- [ ] Wire up /auth/login route
- [ ] Wire up /auth/signup route
- [ ] Add logout button to HomePage
- [ ] Test login flow end-to-end

### Phase 2: API Integration (REQUIRED - Do after auth)
- [ ] Configure proper API base URLs (use .env)
- [ ] Update authClient to use AUTH_SERVICE port (8001)
- [ ] Update voiceApi to use VOICE_SERVICE port (8002)
- [ ] Update ttsApi to use TTS_SERVICE port (8003)
- [ ] Add Bearer token to all API calls
- [ ] Test voice upload/list flow
- [ ] Test TTS generation flow

### Phase 3: Error Handling (IMPORTANT - Handle edge cases)
- [ ] Token expiration handling
- [ ] Refresh token flow
- [ ] Session timeout redirect
- [ ] API error responses (401, 403, 429)

### Phase 4: UX Improvements (NICE TO HAVE)
- [ ] Loading states during auth check
- [ ] Better error messages
- [ ] Automatic redirect after login
- [ ] Remember "last page" before logout

---

## Critical Bugs to Fix Immediately

### Bug #1: No Auth Routes Exist
**Problem**: Login.tsx and Signup.tsx exist but aren't routed  
**Impact**: User cannot log in  
**Fix**: Add routes to App.tsx

### Bug #2: No Session Restoration
**Problem**: Token is saved to localStorage but never restored on app load  
**Impact**: User loses session on page refresh  
**Fix**: Add useEffect in AuthProvider to check localStorage and restore session

### Bug #3: No Protected Routes
**Problem**: Anyone can access /voices and /tts without token  
**Impact**: Components will fail when trying to call APIs  
**Fix**: Wrap routes with ProtectedRoute component

### Bug #4: Missing Bearer Token in API Calls
**Problem**: API calls might not include Authorization header  
**Impact**: Backend returns 401 "Not authenticated"  
**Fix**: Ensure all API calls include `Authorization: Bearer {token}`

### Bug #5: Hardcoded API URLs
**Problem**: API URLs hardcoded, no environment variable support  
**Impact**: Cannot easily switch between dev/prod/local environments  
**Fix**: Create API_CONFIG using environment variables

---

## Testing Plan

### Manual Testing Checklist:

1. **Registration Flow** (if not already implemented)
   - [ ] Navigate to http://localhost:5173/auth/signup
   - [ ] Fill in email, password
   - [ ] Submit
   - [ ] Receive confirmation email (mock)
   - [ ] Verify email
   - [ ] Redirected to login

2. **Login Flow**
   - [ ] Navigate to http://localhost:5173/auth/login
   - [ ] Enter valid credentials (from Auth Service)
   - [ ] Submit
   - [ ] Receive token in response
   - [ ] Token saved to localStorage
   - [ ] Redirected to /voices (or /)

3. **Session Restoration**
   - [ ] Open developer console
   - [ ] Check localStorage → `auth_token` should exist
   - [ ] Refresh page (F5)
   - [ ] Should NOT redirect to /auth/login
   - [ ] Should show voice management interface

4. **Protected Routes**
   - [ ] In incognito window (no localStorage)
   - [ ] Navigate to http://localhost:5173/voices
   - [ ] Should redirect to /auth/login
   - [ ] Should NOT show voice management

5. **Logout Flow**
   - [ ] Click logout button
   - [ ] Should clear localStorage
   - [ ] Should redirect to /auth/login
   - [ ] Visiting /voices should now redirect to login

6. **Voice Management with Auth**
   - [ ] Log in successfully
   - [ ] Navigate to /voices
   - [ ] Record/upload voice
   - [ ] Should include Authorization header in API call
   - [ ] Should show voice in library

7. **TTS Generation with Auth**
   - [ ] Log in successfully
   - [ ] Navigate to /tts
   - [ ] Submit generation request
   - [ ] Should include Authorization header in API call
   - [ ] Should show progress and result

---

## API Headers Reference

All API calls to protected endpoints must include:

```
Authorization: Bearer {token}
Content-Type: application/json
```

Example:
```tsx
const response = await fetch('http://localhost:8002/voices', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${auth.token}`,
    'Content-Type': 'application/json',
  },
});
```

---

## Files to Create/Modify

### Create:
- `frontend/src/components/ProtectedRoute.tsx`
- `frontend/src/layouts/AuthLayout.tsx`
- `frontend/src/utils/config.ts` (API configuration)
- `.env.local` (environment variables)

### Modify:
- `frontend/src/App.tsx` (add routes + protected routes)
- `frontend/src/context/AuthContext.tsx` (add session restoration)
- `frontend/src/pages/HomePage.tsx` (add logout button)
- `frontend/src/pages/Auth/Login.tsx` (update to use proper API config)
- `frontend/src/services/api/authClient.ts` (use API_CONFIG)
- `frontend/src/services/voiceApi.ts` (use API_CONFIG)
- `frontend/src/services/ttsApi.ts` (use API_CONFIG)

---

## Next Steps

1. **Review this document** ✅
2. **Approve the flow** (does it match your backend?)
3. **Implement Phase 1: Authentication**
4. **Test login flow manually**
5. **Implement Phase 2: API Integration**
6. **Test voice + TTS flows**
7. **Deploy to cloud when ready**

---

## Related Documentation

- See `APPLICATION_WORKFLOW.md` for complete user workflows
- See `docs/architecture/System-Architecture.md` for backend design
- See `docs/architecture/Interaction-Flows.md` for API flows
- See `DEPLOYMENT.md` for running backend services

---

**Status**: 🔴 BLOCKING - Cannot use app without fixing authentication  
**Priority**: P0 - Do this immediately  
**Estimated Time**: 2-3 hours  

