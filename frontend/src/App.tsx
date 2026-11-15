import React from 'react';
import './index.css';
import { BrowserRouter as Router, Routes, Route, useNavigate, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { VoiceProvider } from './context/VoiceContext';
import { TTSProvider } from './context/TTSContext';
import { useAuth } from './hooks/useAuth';
import { TextToSpeech } from './pages/TextToSpeech';
import { VoiceManagement } from './pages/VoiceManagement';
import { Login } from './pages/Auth/Login';
import { Signup } from './pages/Auth/Signup';
import { ProtectedRoute } from './components/ProtectedRoute';
import { ErrorNotificationCenter } from './components/ErrorNotificationCenter';

// Home page content wrapper to use hooks inside Router context
function HomePageContent({ onLogout }: { onLogout: () => void }) {
  const navigate = useNavigate();

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(to bottom right, #4f46e5, #9333ea, #ec4899)', padding: '40px 20px' }}>
      {/* Header with Logout */}
      <div style={{ maxWidth: '1200px', margin: '0 auto', marginBottom: '40px', display: 'flex', justifyContent: 'flex-end' }}>
        <button
          onClick={onLogout}
          style={{
            backgroundColor: 'rgba(255,255,255,0.2)',
            color: 'white',
            padding: '10px 20px',
            fontSize: '14px',
            fontWeight: 'bold',
            border: '2px solid white',
            borderRadius: '6px',
            cursor: 'pointer',
            backdropFilter: 'blur(10px)',
          }}
        >
          🚪 Logout
        </button>
      </div>

      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', color: 'white', marginBottom: '60px', paddingTop: '40px' }}>
          <h1 style={{ fontSize: '56px', fontWeight: 'bold', marginBottom: '20px' }}>
            🎙️ Voice Narration Platform
          </h1>
          <p style={{ fontSize: '20px', marginBottom: '30px' }}>
            Record your voice, then generate speech from text
          </p>
          <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <button
              onClick={() => navigate('/voices')}
              style={{
                backgroundColor: 'white',
                color: '#4f46e5',
                padding: '15px 32px',
                fontSize: '18px',
                fontWeight: 'bold',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
              }}
            >
              🎤 Manage Voices
            </button>
            <button
              onClick={() => navigate('/tts')}
              style={{
                backgroundColor: '#FBBF24',
                color: '#1f2937',
                padding: '15px 32px',
                fontSize: '18px',
                fontWeight: 'bold',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
              }}
            >
              🎙️ Generate Speech
            </button>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px', marginBottom: '48px' }}>
          <div
            style={{
              backgroundColor: 'white',
              borderRadius: '12px',
              overflow: 'hidden',
              boxShadow: '0 20px 25px rgba(0,0,0,0.15)',
              cursor: 'pointer',
            }}
            onClick={() => navigate('/voices')}
          >
            <div
              style={{
                background: 'linear-gradient(to right, #a855f7, #ec4899)',
                color: 'white',
                padding: '24px',
              }}
            >
              <div style={{ fontSize: '48px', marginBottom: '12px' }}>🎤</div>
              <h2 style={{ fontSize: '24px', fontWeight: 'bold' }}>Step 1: Create Your Voice</h2>
            </div>
            <div style={{ padding: '32px' }}>
              <p style={{ color: '#374151', marginBottom: '16px', fontWeight: '600' }}>
                Choose how to create your voice:
              </p>
              <ul style={{ listStyle: 'none', padding: 0, marginBottom: '24px', color: '#6b7280' }}>
                <li style={{ marginBottom: '12px' }}>
                  <strong>🎙️ Record from Microphone</strong> - Use your microphone to record
                </li>
                <li>
                  <strong>📁 Upload Audio File</strong> - Upload MP3, WAV, or OGG files
                </li>
              </ul>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  navigate('/voices');
                }}
                style={{
                  width: '100%',
                  backgroundColor: '#9333ea',
                  color: 'white',
                  padding: '12px',
                  fontWeight: 'bold',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '16px',
                }}
              >
                ▶️ Go to Voice Management
              </button>
            </div>
          </div>

          <div
            style={{
              backgroundColor: 'white',
              borderRadius: '12px',
              overflow: 'hidden',
              boxShadow: '0 20px 25px rgba(0,0,0,0.15)',
              cursor: 'pointer',
            }}
            onClick={() => navigate('/tts')}
          >
            <div
              style={{
                background: 'linear-gradient(to right, #6366f1, #3b82f6)',
                color: 'white',
                padding: '24px',
              }}
            >
              <div style={{ fontSize: '48px', marginBottom: '12px' }}>🎙️</div>
              <h2 style={{ fontSize: '24px', fontWeight: 'bold' }}>Step 2: Generate Speech</h2>
            </div>
            <div style={{ padding: '32px' }}>
              <p style={{ color: '#374151', marginBottom: '16px', fontWeight: '600' }}>
                Convert text to speech:
              </p>
              <ol style={{ listStyle: 'decimal', paddingLeft: '20px', marginBottom: '24px', color: '#6b7280' }}>
                <li><strong>Enter text</strong> - Up to 5,000 characters</li>
                <li><strong>Select a voice</strong> - Choose from approved voices</li>
                <li><strong>Pick a provider</strong> - Google, ElevenLabs, or Azure</li>
                <li><strong>Generate</strong> - Watch progress and play audio</li>
              </ol>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  navigate('/tts');
                }}
                style={{
                  width: '100%',
                  backgroundColor: '#4f46e5',
                  color: 'white',
                  padding: '12px',
                  fontWeight: 'bold',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontSize: '16px',
                }}
              >
                ▶️ Go to TTS Generation
              </button>
            </div>
          </div>
        </div>

        <div style={{ backgroundColor: 'white', borderRadius: '12px', padding: '32px', marginBottom: '48px', boxShadow: '0 20px 25px rgba(0,0,0,0.15)' }}>
          <h2 style={{ fontSize: '32px', fontWeight: 'bold', color: '#1f2937', marginBottom: '32px', textAlign: 'center' }}>
            ✨ Features
          </h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '24px' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '36px', marginBottom: '12px' }}>🎤</div>
              <h3 style={{ fontWeight: 'bold', color: '#1f2937', marginBottom: '8px' }}>Voice Recording</h3>
              <p style={{ fontSize: '14px', color: '#6b7280' }}>Record from your microphone</p>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '36px', marginBottom: '12px' }}>📤</div>
              <h3 style={{ fontWeight: 'bold', color: '#1f2937', marginBottom: '8px' }}>Voice Upload</h3>
              <p style={{ fontSize: '14px', color: '#6b7280' }}>Upload MP3, WAV, OGG files</p>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '36px', marginBottom: '12px' }}>🔊</div>
              <h3 style={{ fontWeight: 'bold', color: '#1f2937', marginBottom: '8px' }}>TTS Generation</h3>
              <p style={{ fontSize: '14px', color: '#6b7280' }}>Convert text to speech</p>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '36px', marginBottom: '12px' }}>📊</div>
              <h3 style={{ fontWeight: 'bold', color: '#1f2937', marginBottom: '8px' }}>Quality Metrics</h3>
              <p style={{ fontSize: '14px', color: '#6b7280' }}>Monitor audio quality</p>
            </div>
          </div>
        </div>

        <div style={{ backgroundColor: 'white', borderRadius: '12px', padding: '32px', boxShadow: '0 10px 15px rgba(0,0,0,0.1)' }}>
          <h2 style={{ fontSize: '24px', fontWeight: 'bold', color: '#1f2937', marginBottom: '24px' }}>
            ❓ Quick Help
          </h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
            <div>
              <h3 style={{ fontWeight: 'bold', color: '#1f2937', marginBottom: '8px' }}>What's the workflow?</h3>
              <p style={{ fontSize: '14px', color: '#6b7280' }}>
                1️⃣ Record or upload voice → 2️⃣ Wait for approval → 3️⃣ Use to generate speech
              </p>
            </div>
            <div>
              <h3 style={{ fontWeight: 'bold', color: '#1f2937', marginBottom: '8px' }}>How long is approval?</h3>
              <p style={{ fontSize: '14px', color: '#6b7280' }}>
                Typically within minutes. Check your library for updates.
              </p>
            </div>
            <div>
              <h3 style={{ fontWeight: 'bold', color: '#1f2937', marginBottom: '8px' }}>Which providers?</h3>
              <p style={{ fontSize: '14px', color: '#6b7280' }}>
                Google TTS, ElevenLabs, and Azure Text-to-Speech
              </p>
            </div>
            <div>
              <h3 style={{ fontWeight: 'bold', color: '#1f2937', marginBottom: '8px' }}>Delete voice?</h3>
              <p style={{ fontSize: '14px', color: '#6b7280' }}>
                Yes! Go to Voice Management → Click delete on any voice
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Wrapper to use hooks inside Router context
function HomePageWrapper() {
  const navigate = useNavigate();
  const { dispatch: authDispatch } = useAuth();

  const handleLogout = () => {
    authDispatch({ type: 'LOGOUT' });
    navigate('/auth/login');
  };

  return <HomePageContent onLogout={handleLogout} />;
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <VoiceProvider>
          <TTSProvider>
            <ErrorNotificationCenter />
            <Routes>
              {/* Public routes */}
              <Route path="/auth/login" element={<Login />} />
              <Route path="/auth/signup" element={<Signup />} />

              {/* Protected routes */}
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <HomePageWrapper />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/voices"
                element={
                  <ProtectedRoute>
                    <VoiceManagement />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/tts"
                element={
                  <ProtectedRoute>
                    <TextToSpeech />
                  </ProtectedRoute>
                }
              />

              {/* Catch all - redirect to home */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </TTSProvider>
        </VoiceProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
