import { useEffect, useMemo, useRef, useState } from 'react';

const VOICE_SERVICE_URL = import.meta.env.VITE_VOICE_API_BASE_URL || 'http://localhost:8002';
const INFERENCE_SERVICE_URL = import.meta.env.VITE_TTS_API_BASE_URL || 'http://localhost:8003';

function App() {
  const [voices, setVoices] = useState([]);
  const [selectedVoiceId, setSelectedVoiceId] = useState('');
  const [text, setText] = useState('Namaste, this is my cloned voice.');
  const [status, setStatus] = useState('');
  const [blobUrl, setBlobUrl] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [uploadMode, setUploadMode] = useState('record');
  const [audioFile, setAudioFile] = useState(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const selectedVoice = useMemo(
    () => voices.find((voice) => voice.id === selectedVoiceId) || null,
    [voices, selectedVoiceId]
  );

  async function loadVoices() {
    try {
      const response = await fetch(`${VOICE_SERVICE_URL}/voices?user_id=demo-user`);
      const data = await response.json();
      setVoices(Array.isArray(data) ? data : []);
      if (data.length && !selectedVoiceId) {
        setSelectedVoiceId(data[0].id);
      }
    } catch (error) {
      console.error(error);
      setStatus('Could not load voices from the voice service.');
    }
  }

  useEffect(() => {
    loadVoices();
  }, []);

  async function handleSaveVoice(event) {
    event.preventDefault();
    const formData = new FormData();
    const name = event.target.name.value.trim() || 'My Cloned Voice';
    const userId = event.target.userId.value.trim() || 'demo-user';
    const language = event.target.language.value || 'en-US';
    const consent = event.target.consent.value || 'I consent to using this sample for voice cloning.';
    const file = audioFile || new File([new Blob()], 'recording.wav', { type: 'audio/wav' });

    formData.append('name', name);
    formData.append('user_id', userId);
    formData.append('language', language);
    formData.append('consent', consent);
    formData.append('audio_file', file);

    try {
      const response = await fetch(`${VOICE_SERVICE_URL}/voices`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Voice enrollment failed');
      }
      setStatus(`Voice saved: ${data.name}`);
      setAudioFile(null);
      await loadVoices();
      setSelectedVoiceId(data.id);
    } catch (error) {
      setStatus(error.message);
    }
  }

  async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        chunksRef.current.push(event.data);
      }
    };
    recorder.onstop = () => {
      const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
      chunksRef.current = [];
      const nextFile = new File([blob], 'recording.webm', { type: 'audio/webm' });
      setAudioFile(nextFile);
      const url = URL.createObjectURL(blob);
      setBlobUrl((current) => {
        if (current) URL.revokeObjectURL(current);
        return url;
      });
      stream.getTracks().forEach((track) => track.stop());
    };
    mediaRecorderRef.current = recorder;
    chunksRef.current = [];
    recorder.start();
    setIsRecording(true);
    setStatus('Recording… speak clearly for 5–10 seconds.');
  }

  function stopRecording() {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    setIsRecording(false);
  }

  async function generateSpeech() {
    if (!selectedVoice) {
      setStatus('Select a cloned voice before generating audio.');
      return;
    }
    setStatus('Generating audio…');
    try {
      const response = await fetch(`${INFERENCE_SERVICE_URL}/inference/jobs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text,
          voice_profile_id: selectedVoice.id,
          voice_name: selectedVoice.name,
          user_id: selectedVoice.user_id,
        }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Generation failed');
      }
      const generatedUrl = data.audio_url;
      setAudioUrl(generatedUrl);
      setStatus('Audio generated successfully.');
    } catch (error) {
      setStatus(error.message);
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Voice Narration Studio</p>
          <h1>Clone your voice and generate narration</h1>
        </div>
      </header>

      <main className="layout">
        <section className="panel">
          <h2>Voice library</h2>
          <div className="voice-list">
            {voices.length === 0 && <p>No cloned voices yet.</p>}
            {voices.map((voice) => (
              <button
                key={voice.id}
                type="button"
                className={selectedVoiceId === voice.id ? 'voice-card selected' : 'voice-card'}
                onClick={() => setSelectedVoiceId(voice.id)}
              >
                <strong>{voice.name}</strong>
                <span>{voice.language}</span>
                <small>{voice.status}</small>
              </button>
            ))}
          </div>

          <form onSubmit={handleSaveVoice} className="voice-form">
            <label>
              Voice name
              <input name="name" placeholder="My Voice" defaultValue="My Cloned Voice" />
            </label>
            <label>
              User ID
              <input name="userId" defaultValue="demo-user" />
            </label>
            <label>
              Language
              <select name="language" defaultValue="en-US">
                <option value="en-US">English</option>
                <option value="hi-IN">Hindi</option>
              </select>
            </label>
            <label>
              Consent
              <textarea
                name="consent"
                rows="3"
                defaultValue="I consent to this audio sample being used for voice cloning and narration generation."
              />
            </label>

            <div className="mode-toggle">
              <button type="button" className={uploadMode === 'record' ? 'selected' : ''} onClick={() => setUploadMode('record')}>
                Record
              </button>
              <button type="button" className={uploadMode === 'upload' ? 'selected' : ''} onClick={() => setUploadMode('upload')}>
                Upload file
              </button>
            </div>

            {uploadMode === 'record' ? (
              <div className="record-block">
                <button type="button" className="record-btn" onClick={isRecording ? stopRecording : startRecording}>
                  {isRecording ? 'Stop recording' : 'Start recording'}
                </button>
                {blobUrl && (
                  <audio controls src={blobUrl} />
                )}
              </div>
            ) : (
              <label className="upload-box">
                <input
                  type="file"
                  accept="audio/*"
                  onChange={(event) => setAudioFile(event.target.files?.[0] || null)}
                />
                {audioFile ? <span>{audioFile.name}</span> : <span>Choose audio file</span>}
              </label>
            )}

            <button type="submit" className="primary-btn">Save voice profile</button>
          </form>
        </section>

        <section className="panel">
          <h2>Generate narration</h2>
          <label>
            Script
            <textarea
              rows="7"
              value={text}
              onChange={(event) => setText(event.target.value)}
            />
          </label>

          {selectedVoice && (
            <div className="selected-voice">
              <strong>Selected profile:</strong> {selectedVoice.name}
            </div>
          )}

          <button type="button" className="primary-btn" onClick={generateSpeech}>
            Generate speech
          </button>

          {status && <div className="status">{status}</div>}

          {audioUrl && (
            <div className="audio-output">
              <audio controls src={audioUrl} />
              <a href={audioUrl} target="_blank" rel="noreferrer" className="download-link">
                Download WAV
              </a>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
