# Voice-Narration: Complete Application Workflow

## 🎯 Application Overview

Voice-Narration is a complete voice cloning and text-to-speech (TTS) generation platform with two main workflows:

1. **Voice Management** - Create and manage your voice library
2. **TTS Generation** - Convert text to speech using approved voices

---

## 🏠 Homepage

**URL**: `http://localhost:5173` or `http://localhost:5173/`

The homepage serves as your dashboard with:
- Project status overview
- Quick navigation buttons
- Feature descriptions
- Step-by-step workflow guide

### Quick Links from Homepage:
- 🎤 **Manage Voices** → `/voices` - Voice management interface
- 🎙️ **TTS Generation** → `/tts` - Text-to-speech interface

---

## 🎤 Workflow 1: Voice Management (`/voices`)

### Purpose
Upload or record audio files to create a personal voice library for TTS generation.

### Tabs Available

#### 1️⃣ **Record Voice** (Tab 1)
Record audio directly from your microphone
- Click "Start Recording" button
- Speak into your microphone
- Click "Stop Recording" when done
- Give your voice a name
- Voice will be added to your library with "pending" status
- Wait for admin approval

**Components Used**:
- `VoiceRecorder.tsx` - Recording interface
- `VoiceWaveform.tsx` - Real-time waveform visualization

#### 2️⃣ **Upload Voice** (Tab 2)
Upload existing audio files from your computer
- Click "Choose File" to select from your computer
- Supported formats: MP3, WAV, OGG
- Maximum file size: 100 MB
- Provide a name for the voice
- Click "Upload" to add to your library
- Voice status will be "pending" until approved

**Components Used**:
- `VoiceUpload.tsx` - File upload interface
- `VoicePlayback.tsx` - Audio preview

#### 3️⃣ **Voice Library** (Tab 3)
Browse all your recorded and uploaded voices
- View all your voices (approved, pending, rejected)
- See voice details: name, language, status, file size, duration
- Only "approved" voices can be used for TTS generation
- Play audio preview for each voice
- See approval status for each voice

**Components Used**:
- `VoiceLibrary.tsx` - Voice listing and management
- `VoicePlayback.tsx` - Audio preview player

#### 4️⃣ **Manage Voices** (Tab 4)
Advanced management options
- View detailed voice information
- Check approval status
- Delete voices you no longer need
- See usage history (how many TTS generations used this voice)

**Components Used**:
- `VoiceOperations.tsx` - Voice management operations
- `VoiceApproval.tsx` - Approval status tracking

### Voice Status Flow
```
Upload/Record → Pending → Approved → Available for TTS
                       ↓
                    Rejected (Not available)
```

**Note**: Admin approval is required before using a voice for TTS generation.

---

## 🎙️ Workflow 2: TTS Generation (`/tts`)

### Purpose
Convert text to natural-sounding audio using your approved voices.

### Main Components

#### 1️⃣ **Text Input Section**
```
Enter your text to convert to speech
- Maximum 5000 characters
- Character counter shows: "X / 5000"
- Warning appears at 90% (4500 chars)
- Supports special characters and UTF-8
```

**Component**: `TextToSpeechInput.tsx`

#### 2️⃣ **Voice Selection**
```
Select which voice to use
- Dropdown showing only APPROVED voices
- Shows voice name, language, and provider
- Selected voice is highlighted
```

**Component**: `VoiceSelector.tsx`

#### 3️⃣ **Provider Selection**
```
Choose which TTS provider to use
- Google Text-to-Speech
- ElevenLabs
- Azure Speech Services

Shows:
- Provider name
- Max characters per request
- Current rate limit usage
```

**Component**: `ProviderSelector.tsx`

#### 4️⃣ **Generate Button**
```
Submit for TTS generation
- Disabled if: text is empty, no voice selected, no provider selected
- Disabled if: rate limit exceeded (429)
- Shows loading state while processing
```

**Component**: `GenerationSubmitForm.tsx`

#### 5️⃣ **Progress Indicator** (During Generation)
```
Real-time progress display while audio is being generated
- Progress bar: 0-100%
- Status: "processing"
- Elapsed time counter
- Cancel button with confirmation
- Estimated time remaining
```

**Component**: `GenerationProgress.tsx`
**Service**: `TTSPollingService.ts` - Polls every 2 seconds

#### 6️⃣ **Audio Player** (When Ready)
```
Play the generated audio
- Play/Pause buttons
- Seek bar to navigate through audio
- Current time / Total duration display
- Volume control
```

**Component**: `AudioPlayer.tsx`

#### 7️⃣ **Quality Metrics**
```
Audio quality information
- Format: MP3, WAV, OGG, etc.
- File size in KB/MB
- Duration in seconds
- Quality score: 0-100
- Warning if quality is low
```

**Component**: `QualityMetrics.tsx`

#### 8️⃣ **Generation History**
```
Paginated list of all your past generations
- Text used
- Voice name
- Provider used
- Creation timestamp
- Audio duration
- Buttons: Play, Download, Delete
```

**Component**: `GenerationHistory.tsx`

#### 9️⃣ **Rate Limit Display**
```
Shows your current usage with current provider
- Used: X/Y quota
- Percentage: XX%
- Reset time
- Warning if usage > 90%
- Suggestion to switch providers if quota exceeded
```

**Component**: `RateLimitDisplay.tsx`

#### 🔟 **Error Display**
```
User-friendly error messages
- Input validation errors (empty text, text too long)
- Voice errors (not approved, invalid)
- Provider errors (unavailable, connection failed)
- Rate limit errors (quota exceeded)
- Retry button after errors
```

**Component**: `GenerationErrorDisplay.tsx`

---

## 📊 Complete User Journey

### Journey 1: First Time User

```
1. Start at Homepage (/)
   ↓
2. Click "🎤 Manage Voices" → /voices
   ↓
3. Choose "Record Voice" OR "Upload Voice" tab
   ↓
4. Create your voice
   ↓
5. Wait for admin approval
   ↓
6. Once approved, click "🎙️ TTS Generation" → /tts
   ↓
7. Generate speech:
   - Enter text
   - Select voice (now available)
   - Choose provider
   - Click Generate
   - Wait for progress
   - Play result
```

### Journey 2: Generate Text-to-Speech

```
1. Navigate to /tts (TTS Generation)
   ↓
2. Enter text (0-5000 chars)
   ↓
3. Select voice from dropdown
   ↓
4. Select provider (Google, ElevenLabs, Azure)
   ↓
5. Check rate limit (should have quota)
   ↓
6. Click "Generate" button
   ↓
7. Watch progress bar (0-100%)
   ↓
8. When ready (100%), audio player appears
   ↓
9. Play audio, seek through, or download
   ↓
10. View in "Generation History"
    - Play again anytime
    - Delete if no longer needed
```

---

## 🎯 Key Features by Workflow

### Voice Management Features
- ✅ Microphone recording with waveform visualization
- ✅ File upload (MP3, WAV, OGG - max 100 MB)
- ✅ Voice library browsing
- ✅ Audio preview player
- ✅ Approval status tracking
- ✅ Voice deletion
- ✅ Voice metadata display

### TTS Generation Features
- ✅ Text input with character validation (0-5000 chars)
- ✅ Voice selection from approved voices only
- ✅ Multi-provider support (Google, ElevenLabs, Azure)
- ✅ Real-time progress polling (2-second intervals)
- ✅ Progress bar with percentage
- ✅ Elapsed time counter
- ✅ Cancellation with confirmation
- ✅ Audio playback controls
- ✅ Seek bar navigation
- ✅ Generation history with pagination
- ✅ Rate limit visualization and warnings
- ✅ Quality metrics display
- ✅ Comprehensive error handling
- ✅ 90% usage warnings
- ✅ Alternative provider suggestions

---

## 📱 Navigation Summary

| Page | URL | Purpose | Tabs |
|------|-----|---------|------|
| Home | `/` | Dashboard | None |
| Voice Management | `/voices` | Create/upload voices | Record, Upload, Library, Manage |
| TTS Generation | `/tts` | Convert text to speech | None (Single page) |

---

## 🔄 State Management

### Authentication Context
- User login/logout
- JWT token management
- Authorization

### Voice Context
- List of all voices
- Selected voice
- Voice approval status
- Voice metadata

### TTS Context
- Selected voice for generation
- Selected provider
- Current generation status
- Generation history
- Rate limit information
- Error messages

---

## ⚙️ Backend Services (Microservices)

| Service | Port | Purpose |
|---------|------|---------|
| Auth | 8001 | User authentication |
| Voice Management | 8002 | Voice upload/management |
| TTS Generation | 8003 | Text-to-speech conversion |
| Evaluation | 8006 | Voice quality evaluation |
| Jobs | 8007 | Background processing |

---

## 🧪 Testing

### Run All Tests
```bash
cd frontend
npm run test
```

### Run TTS Tests Only
```bash
npm run test -- run tests/tts.spec.tsx
```

### Test Coverage
- ✅ 94 TTS tests (M3-GREEN)
- ✅ 106 Voice tests (M2-GREEN)
- ✅ 200+ total frontend tests
- ✅ 39 backend service tests

---

## 📚 Documentation

See these files for more information:
- **QUICK_START.md** - Getting started in 5 minutes
- **DEPLOYMENT.md** - Local deployment guide
- **GCP-DEPLOYMENT.md** - Cloud deployment
- **README.md** - Project overview
- **M3-GREEN-COMPLETE.md** - Milestone details

---

## 🚀 Deployment

### Local
```bash
docker-compose -f compose.harness.yaml up
```

### Development
```bash
cd frontend && npm run dev
```

### Production
See GCP-DEPLOYMENT.md for cloud deployment

---

## 📞 Quick Help

**Q: Where do I record/upload voices?**
A: Click "🎤 Manage Voices" on homepage or navigate to `/voices`

**Q: Can I use unapproved voices for TTS?**
A: No, only "approved" voices appear in the TTS voice dropdown

**Q: What if I exceed the rate limit?**
A: Switch to a different provider or wait for your quota to reset

**Q: How long does a voice take to approve?**
A: Typically 5-10 minutes (configurable by admin)

**Q: Can I delete my voices?**
A: Yes, in the "Manage Voices" tab of Voice Management page

**Q: What audio formats are supported?**
A: MP3, WAV, OGG (for upload); all formats for generation

---

**Application Status**: ✅ M3-GREEN Complete • Ready for Production

Last Updated: November 1, 2026
