# 🎨 Voice-Narration Frontend - Complete Requirements

## 📋 Overview

Frontend application for Voice-Narration platform that enables users to:
1. **Upload voice samples** (voice cloning source)
2. **Generate speech** in their voice using different texts
3. **Manage & replay** generated content

---

## 🎯 MVP Phase (Week 1-2)

**Goal:** Core voice cloning + TTS generation workflow

### **MVP Features:**

#### **1. Authentication**
- User registration (email + password)
- User login
- Session management (JWT token)
- Logout
- Password reset (email link)

#### **2. Voice Sample Management (Voice Cloning Source)**
- Upload voice sample (WAV/MP3, 5-60 seconds)
- Real-time quality feedback from backend
- Accept/reject flow
- Store voice metadata (name, language, duration)
- Preview uploaded voice

#### **3. TTS Generation (Voice Cloning Output)**
- Text input area (supports Hindi + English)
- Select uploaded voice from dropdown
- Generate button
- Real-time job status (pending → processing → complete)
- Audio player for result
- Download audio as WAV

#### **4. History & Playback**
- List of generated audios
- Show: text, voice used, date, duration
- Play audio inline
- Delete generated audio

#### **5. Settings**
- View profile
- Change password
- Accept/view privacy policy
- Consent management

### **MVP Tech Stack:**
- **Frontend:** React (or Vue/Next.js)
- **API Communication:** Axios/Fetch
- **Audio:** HTML5 Audio element
- **State:** React Context or Redux
- **Styling:** Tailwind CSS / Material UI

### **MVP Backend Integration:**
| Feature | Backend Service | Port |
|---------|-----------------|------|
| Auth | Auth Service | 8001 |
| Voice Upload | Voices Service | 8002 |
| Quality Check | AI Evaluation | 8006 |
| TTS Generate | Inference Service | 8005 |
| Job Status | Jobs Service | 8003 |
| Consent | Consent Service | 8004 |

---

## 📈 Phase 2 - Enhanced Voice Cloning (Week 3)

**Goal:** Multiple voices + advanced voice management

### **Phase 2 Features:**

#### **Voice Sample Management**
- ✅ Upload multiple voice samples
- ✅ Name each voice (e.g., "Professional", "Casual", "Hindi Speaker")
- ✅ Set default voice (auto-selected for new generation)
- ✅ Edit voice metadata (name, language tag)
- ✅ Delete voice samples
- ✅ Compare voice quality scores
- ✅ View audio waveform
- ✅ Re-record/replace voice sample

#### **TTS Generation Enhancement**
- ✅ Quick-generate with default voice
- ✅ Batch text generation (multiple texts, one voice)
- ✅ Adjust speech rate (0.5x - 2.0x)
- ✅ Adjust pitch/tone
- ✅ Save generation presets
- ✅ Copy audio link to clipboard
- ✅ Progress percentage display

#### **Content Organization**
- ✅ Organize generated audios by voice
- ✅ Add tags/categories
- ✅ Search generated content
- ✅ Favorite/star audios
- ✅ Export as ZIP

#### **Audio Management**
- ✅ Bulk download
- ✅ Share with link (24-48hr expiry)
- ✅ Embed audio in webpage
- ✅ Edit metadata of generated audio

---

## 🚀 Phase 3 - Advanced Voice Cloning (Week 4+)

**Goal:** Voice cloning quality improvements + analytics

### **Phase 3 Features:**

#### **Advanced Voice Cloning**
- ✅ Voice cloning quality levels (standard, high, ultra)
- ✅ Voice emotion control (happy, sad, neutral, excited)
- ✅ Accent variation (regional Hindi accents, English accents)
- ✅ Speaking style (formal, casual, storytelling)
- ✅ Voice gender conversion
- ✅ Voice age simulation (young/old voice)
- ✅ Background noise filtering before cloning

#### **Advanced TTS Features**
- ✅ SSML support (pause, emphasis, pronunciation)
- ✅ Multi-language in single text (Hindi + English mix)
- ✅ Voice blending (mix 2 voices)
- ✅ Real-time audio preview while typing
- ✅ Voice comparison (side-by-side playback)
- ✅ Audio enhancement (equalization, compression)

#### **Content Management Pro**
- ✅ Create voice projects (group related audios)
- ✅ Version control for audios
- ✅ Collaboration (share project with others)
- ✅ Comments & feedback on audios
- ✅ Voice cloning templates (save & reuse settings)

#### **Analytics & Insights**
- ✅ Usage dashboard (audios generated, total duration)
- ✅ Voice quality trends over time
- ✅ Most used voices/texts
- ✅ Generation time analytics
- ✅ Cost tracking (if using paid TTS)

#### **Integration Features**
- ✅ API key for 3rd party integration
- ✅ Webhooks for automation
- ✅ Export to cloud (Google Drive, Dropbox)
- ✅ Integrate with video editing tools
- ✅ Podcast publishing integration

#### **Advanced Voice Settings**
- ✅ Custom voice parameters per language
- ✅ Phoneme-level control
- ✅ Tone calibration UI
- ✅ Voice fingerprinting (biometric voice verification)

---

## 📊 Data Models

### **User**
```javascript
{
  id: uuid,
  email: string,
  password_hash: string,
  full_name: string,
  profile_pic: string,
  language_preference: string,
  created_at: timestamp,
  updated_at: timestamp
}
```

### **VoiceSample (Voice Cloning Source)**
```javascript
{
  id: uuid,
  user_id: uuid,
  name: string,
  language: string,
  duration_seconds: float,
  audio_path: string,
  quality_score: float (0-100),
  quality_status: "approved" | "rejected" | "pending",
  is_default: boolean,
  waveform_data: array,
  metadata: {
    accent: string,
    age: string,
    gender: string
  },
  created_at: timestamp,
  uploaded_at: timestamp
}
```

### **GeneratedAudio (Voice Cloning Output)**
```javascript
{
  id: uuid,
  user_id: uuid,
  voice_sample_id: uuid,
  input_text: string,
  output_audio_path: string,
  duration_seconds: float,
  status: "pending" | "processing" | "complete" | "failed",
  quality_score: float,
  generation_time_ms: number,
  settings: {
    speech_rate: float,
    pitch: float,
    emotion: string,
    style: string
  },
  is_favorite: boolean,
  tags: array<string>,
  share_token: string,
  share_expires_at: timestamp,
  created_at: timestamp,
  completed_at: timestamp
}
```

### **Project (Phase 3)**
```javascript
{
  id: uuid,
  user_id: uuid,
  name: string,
  description: string,
  voice_sample_ids: array<uuid>,
  generated_audio_ids: array<uuid>,
  collaborators: array<uuid>,
  created_at: timestamp
}
```

---

## 🔐 Authentication & Authorization

### **Auth Flow:**
```
1. User registers → Creates account
2. User logs in → Receives JWT token
3. Token stored in localStorage
4. All API requests include: Authorization: Bearer <token>
5. Token refresh before expiry (auto or manual)
6. Logout → Clear token
```

### **Permissions:**
- User can only access their own voice samples
- User can only access their own generated audios
- Share token allows read-only access to specific audio
- Collaborators (Phase 3) have specific permissions

---

## 🎨 UI/UX Components Needed

### **MVP Components:**
- Authentication forms (login, register, password reset)
- Voice upload area (drag-drop + file select)
- Quality feedback display
- Voice selector (dropdown)
- Text input area (textarea with character count)
- Generate button with loading state
- Job status indicator
- Audio player (play, pause, download, delete)
- Voice history list
- User settings panel

### **Phase 2 Components:**
- Voice card (display voice with metadata)
- Voice comparison view
- Tags input
- Batch generator modal
- Share link generator
- Audio waveform visualizer
- Preset manager

### **Phase 3 Components:**
- Voice emotion selector
- Accent picker
- Voice blending mixer
- SSML editor
- Analytics dashboard
- Project management UI
- Collaboration invite system

---

## 📡 API Endpoints (Frontend Needs)

### **Auth (Port 8001)**
```
POST   /auth/register        → Register user
POST   /auth/login           → Login user
POST   /auth/refresh         → Refresh token
POST   /auth/logout          → Logout user
POST   /auth/password-reset  → Reset password
```

### **Voices (Port 8002)**
```
POST   /voices/upload         → Upload voice sample
GET    /voices/list          → List user's voice samples
GET    /voices/{id}          → Get voice details
PATCH  /voices/{id}          → Update voice metadata
DELETE /voices/{id}          → Delete voice sample
POST   /voices/{id}/default  → Set as default
```

### **Inference/TTS (Port 8005)**
```
POST   /inference/jobs/{job_id}/infer   → Generate audio
GET    /inference/jobs/{job_id}/output  → Get audio result
GET    /inference/backends              → List available backends
```

### **Jobs (Port 8003)**
```
GET    /jobs/{job_id}        → Get job status
GET    /jobs/history         → List user's jobs
```

### **AI Evaluation (Port 8006)**
```
POST   /evaluate             → Evaluate audio quality
GET    /evaluate/{id}        → Get quality report
```

### **Consent (Port 8004)**
```
POST   /consent/record       → Record user consent
GET    /consent/status       → Get consent status
```

---

## 📱 Responsive Design

- **Desktop:** Full UI, side navigation
- **Tablet:** Responsive cards, collapsible nav
- **Mobile:** Bottom navigation, full-width forms, simplified controls

---

## 🎯 Success Criteria

### **MVP Success:**
- ✅ User can register & login
- ✅ User can upload voice sample
- ✅ Quality feedback visible
- ✅ User can generate TTS in their voice
- ✅ Audio plays & can be downloaded
- ✅ History shows previous generations

### **Phase 2 Success:**
- ✅ Multiple voices supported
- ✅ Batch generation works
- ✅ Voice management UI smooth
- ✅ Sharing works with expiry
- ✅ Performance <3s per generation

### **Phase 3 Success:**
- ✅ Voice emotion/style controls work
- ✅ Analytics dashboard accurate
- ✅ Collaboration functional
- ✅ Advanced features stable

---

## 📚 Technology Decisions

### **Framework Choice:**
- **Option A: React** - Large ecosystem, easy scaling
- **Option B: Next.js** - Full-stack, built-in optimization
- **Option C: Vue** - Lighter weight, good for this scope
- **Option D: Svelte** - Minimal JS, great performance

**Recommendation:** React or Next.js (better long-term support)

### **Component Library:**
- Material-UI (comprehensive)
- Tailwind CSS + Headless UI (minimal)
- Chakra UI (balanced)

### **Audio Library:**
- Wavesurfer.js (visualization)
- Tone.js (manipulation)
- Web Audio API (native)

### **State Management:**
- React Context (simple, MVP)
- Redux (complex, Phase 2+)
- Zustand (lightweight alternative)

### **API Client:**
- Axios (feature-rich)
- Fetch API (native, simpler)
- React Query (caching + sync)

---

## 🚀 Deployment

### **Hosting Options:**
- **Vercel** (Next.js optimized, free tier)
- **Netlify** (React optimized, free tier)
- **AWS Amplify** (enterprise, free tier)
- **Self-hosted** (full control, more setup)

### **Environment:**
- `.env.local` → Local development
- `.env.staging` → Staging environment
- `.env.production` → Production

---

## 📝 Next Steps

1. **Decide tech stack** (React/Next.js/Vue?)
2. **Create wireframes** (Figma/Adobe XD)
3. **Set up project structure**
4. **Build MVP components**
5. **Integrate with backend services**
6. **Test with real TTS**
7. **Deploy to staging**
8. **Plan Phase 2 & 3**

---

**Status:** Requirements complete ✅  
**Ready for:** Architecture planning & implementation planning
