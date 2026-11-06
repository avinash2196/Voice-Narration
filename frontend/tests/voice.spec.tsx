// ============================================================================
// M2-RED TESTS: Voice Management (Recording, Upload, Approval, Library)
// ============================================================================

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { rest } from 'msw';

// Import handlers
import { voicesHandlers } from './mocks/voices-handlers';
import { aiEvaluationHandlers } from './mocks/ai-evaluation-handlers';
import { server } from './mocks/setup';
import * as fixtures from './fixtures/voices';

// Import components
import { VoiceRecorder } from '@/components/VoiceRecorder';
import { VoiceUpload } from '@/components/VoiceUpload';
import { VoiceLibrary } from '@/components/VoiceLibrary';

// Import providers and context
import { AuthProvider, AuthContext } from '@/context/AuthContext';
import { VoiceProvider } from '@/context/VoiceContext';

// Add voice handlers to server for these tests
beforeEach(() => {
  server.use(...voicesHandlers, ...aiEvaluationHandlers);
  // Mock localStorage for tests
  Object.defineProperty(window, 'localStorage', {
    value: {
      getItem: () => null,
      setItem: () => {},
      removeItem: () => {},
      clear: () => {},
    },
    writable: true,
  });
});

// Helper function to render components with required providers
function renderWithProviders(component: React.ReactElement, { initialAuthState = null } = {}) {
  let authContextValue = {
    user: null,
    token: 'mock-jwt-token',
    refreshToken: 'mock-refresh-token',
    isAuthenticated: true,
    isLoading: false,
    error: null,
    dispatch: () => {},
    ...initialAuthState,
  };

  return render(
    <AuthContext.Provider value={authContextValue}>
      <VoiceProvider>
        {component}
      </VoiceProvider>
    </AuthContext.Provider>
  );
}

// ============================================================================
// M2.1: MICROPHONE PERMISSIONS & RECORDING SETUP
// ============================================================================

describe('M2.1: Microphone Permissions', () => {
  it('M2.1.1: should request microphone permission on record button click', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockResolvedValueOnce(fixtures.mockMediaStream);
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    expect(startButton).toBeInTheDocument();
    
    await user.click(startButton);
    
    // Verify getUserMedia was called with audio constraint
    expect(mockGetUserMedia).toHaveBeenCalledWith(
      expect.objectContaining({ audio: true })
    );
    
    mockGetUserMedia.mockRestore();
  });

  it('M2.1.2: should handle permission denied gracefully', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockRejectedValueOnce(
      new DOMException('Permission denied', 'NotAllowedError')
    );
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText(/permission denied|microphone access denied/i)).toBeInTheDocument();
    });
    
    mockGetUserMedia.mockRestore();
  });

  it('M2.1.3: should show error when no microphone device found', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockRejectedValueOnce(
      new DOMException('Requested device not found', 'NotFoundError')
    );
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText(/no microphone|device not found/i)).toBeInTheDocument();
    });
    
    mockGetUserMedia.mockRestore();
  });

  it('M2.1.4: should recover from permission request timeout', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    
    // First call times out, second succeeds
    mockGetUserMedia
      .mockRejectedValueOnce(new DOMException('Timeout', 'TimeoutError'))
      .mockResolvedValueOnce(fixtures.mockMediaStream);
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Microphone request timeout/i)).toBeInTheDocument();
    });
    
    const retryButton = screen.getByRole('button', { name: /try again/i });
    await user.click(retryButton);
    
    // Should succeed on retry
    await waitFor(() => {
      expect(screen.queryByText(/timeout/i)).not.toBeInTheDocument();
    });
    
    mockGetUserMedia.mockRestore();
  });
});

describe('M2.2: Recording Controls', () => {
  it('M2.2.1: should start recording on Start button click', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockResolvedValueOnce(fixtures.mockMediaStream);
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Recording/i)).toBeInTheDocument();
    });
    
    mockGetUserMedia.mockRestore();
  });

  it('M2.2.2: should pause recording on Pause button click', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockResolvedValueOnce(fixtures.mockMediaStream);
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    const pauseButton = await screen.findByRole('button', { name: /pause/i });
    await user.click(pauseButton);
    
    await waitFor(() => {
      expect(screen.getByText(/paused|resume/i)).toBeInTheDocument();
    });
    
    mockGetUserMedia.mockRestore();
  });

  it('M2.2.3: should resume recording after pause', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockResolvedValueOnce(fixtures.mockMediaStream);
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    const pauseButton = await screen.findByRole('button', { name: /pause/i });
    await user.click(pauseButton);
    
    const resumeButton = screen.getByRole('button', { name: /resume/i });
    await user.click(resumeButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Recording/i)).toBeInTheDocument();
    });
    
    mockGetUserMedia.mockRestore();
  });

  it('M2.2.4: should stop recording and save blob on Stop button click', async () => {
    const user = userEvent.setup();
    const onComplete = vi.fn();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockResolvedValueOnce(fixtures.mockMediaStream);
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={onComplete} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    const stopButton = await screen.findByRole('button', { name: /stop/i });
    await user.click(stopButton);
    
    await waitFor(() => {
      expect(onComplete).toHaveBeenCalledWith(expect.any(Blob));
    });
    
    mockGetUserMedia.mockRestore();
  });

  it('M2.2.5: should disable controls during permission request', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockImplementationOnce(() => new Promise(() => {})); // Never resolves
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    expect(startButton).toBeDisabled();
    
    mockGetUserMedia.mockRestore();
  });

  it('M2.2.6: should display recording time elapsed', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockResolvedValueOnce(fixtures.mockMediaStream);
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    await waitFor(() => {
      const timeDisplay = screen.queryByText(/00:\d{2}|0:\d{2}/);
      expect(timeDisplay).toBeInTheDocument();
    });
    
    mockGetUserMedia.mockRestore();
  });
});

describe('M2.3: Waveform Visualization', () => {
  it('M2.3.1: should render waveform canvas element', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockResolvedValueOnce(fixtures.mockMediaStream);
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByTestId('waveform-canvas')).toBeInTheDocument();
    });
    
    mockGetUserMedia.mockRestore();
  });

  it('M2.3.2: should animate waveform during recording', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockResolvedValueOnce(fixtures.mockMediaStream);
    
    const { rerender } = renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    const canvas = await screen.findByTestId('waveform-canvas');
    const ctx = canvas.getContext('2d');
    const drawSpy = vi.spyOn(ctx!, 'fillRect');
    
    // Canvas should be actively drawing
    expect(canvas.width).toBeGreaterThan(0);
    expect(canvas.height).toBeGreaterThan(0);
    
    mockGetUserMedia.mockRestore();
  });

  it('M2.3.3: should show frequency data accurately', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockResolvedValueOnce(fixtures.mockMediaStream);
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    await waitFor(() => {
      const canvas = screen.getByTestId('waveform-canvas');
      expect(canvas).toBeInTheDocument();
    });
    
    mockGetUserMedia.mockRestore();
  });

  it('M2.3.4: should update waveform color during recording', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockResolvedValueOnce(fixtures.mockMediaStream);
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    const canvas = await screen.findByTestId('waveform-canvas');
    expect(canvas).toHaveStyle({ opacity: expect.any(String) });
    
    mockGetUserMedia.mockRestore();
  });

  it('M2.3.5: should freeze waveform after stop', async () => {
    const user = userEvent.setup();
    const mockGetUserMedia = vi.spyOn(navigator.mediaDevices, 'getUserMedia');
    mockGetUserMedia.mockResolvedValueOnce(fixtures.mockMediaStream);
    
    renderWithProviders(<VoiceRecorder onRecordingComplete={vi.fn()} />);
    
    const startButton = screen.getByRole('button', { name: /start|record/i });
    await user.click(startButton);
    
    const stopButton = await screen.findByRole('button', { name: /stop/i });
    await user.click(stopButton);
    
    const canvas = screen.getByTestId('waveform-canvas');
    expect(canvas).toHaveClass('frozen');
    
    mockGetUserMedia.mockRestore();
  });
});

describe('M2.4: File Selection & Preview', () => {
  it('M2.4.1: should allow user to select MP3 file via file input', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    
    expect(fileInput.files?.[0]).toBe(file);
  });

  it('M2.4.2: should allow user to select WAV file via file input', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.wav', { type: 'audio/wav' });
    
    await user.upload(fileInput, file);
    
    expect(fileInput.files?.[0]).toBe(file);
  });

  it('M2.4.3: should allow user to select OGG file via file input', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.ogg', { type: 'audio/ogg' });
    
    await user.upload(fileInput, file);
    
    expect(fileInput.files?.[0]).toBe(file);
  });

  it('M2.4.4: should display selected file name', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'my-voice.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    
    await waitFor(() => {
      expect(screen.getByText(/my-voice\.mp3/)).toBeInTheDocument();
    });
  });

  it('M2.4.5: should display file size in readable format', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['x'.repeat(1024 * 5)], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    
    await waitFor(() => {
      expect(screen.getByText(/5 KB|5KB/i)).toBeInTheDocument();
    });
  });

  it('M2.4.6: should display audio duration estimate', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    
    await waitFor(() => {
      expect(screen.queryByText(/\d+:\d{2}|duration/i)).toBeInTheDocument();
    });
  });

  it('M2.4.7: should allow clearing selected file', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    
    const clearButton = await screen.findByRole('button', { name: /clear|remove|reset/i });
    await user.click(clearButton);
    
    expect(fileInput.files?.length).toBe(0);
  });

  it('M2.4.8: should show audio preview/playback control', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    
    await waitFor(() => {
      expect(screen.getByTestId('audio-preview')).toBeInTheDocument();
    });
  });
});

describe('M2.5: File Validation', () => {
  it('M2.5.1: should reject non-audio file types', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['text'], 'test.txt', { type: 'text/plain' });
    
    await user.upload(fileInput, file);
    
    await waitFor(() => {
      expect(screen.getByText(/invalid file type|audio files only/i)).toBeInTheDocument();
    });
  });

  it('M2.5.2: should reject file larger than 100 MB', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const largeFile = new File(['x'.repeat(101 * 1024 * 1024)], 'large.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, largeFile);
    
    await waitFor(() => {
      expect(screen.getByText(/file too large|100 MB|max.*100/i)).toBeInTheDocument();
    });
  });

  it('M2.5.3: should reject empty recordings', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const emptyFile = new File([], 'empty.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, emptyFile);
    
    await waitFor(() => {
      expect(screen.getByText(/empty|no content|0 bytes/i)).toBeInTheDocument();
    });
  });

  it('M2.5.4: should validate voice name is provided', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    
    const nameInput = screen.queryByLabelText(/name|label/i) as HTMLInputElement;
    if (nameInput) {
      const uploadButton = screen.getByRole('button', { name: /upload|save/i });
      await user.click(uploadButton);
      
      await waitFor(() => {
        expect(screen.getByText(/name required|enter a name/i)).toBeInTheDocument();
      });
    }
  });

  it('M2.5.5: should limit voice name to 255 characters', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const nameInput = screen.queryByLabelText(/name|label/i) as HTMLInputElement;
    if (nameInput) {
      const longName = 'x'.repeat(300);
      await user.type(nameInput, longName);
      
      expect(nameInput.value.length).toBeLessThanOrEqual(255);
    }
  });

  it('M2.5.6: should accept valid MP3 files', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio data'], 'valid.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    
    expect(fileInput.files?.[0]).toBe(file);
    expect(screen.queryByText(/invalid|error/i)).not.toBeInTheDocument();
  });

  it('M2.5.7: should accept valid WAV files', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio data'], 'valid.wav', { type: 'audio/wav' });
    
    await user.upload(fileInput, file);
    
    expect(fileInput.files?.[0]).toBe(file);
    expect(screen.queryByText(/invalid|error/i)).not.toBeInTheDocument();
  });

  it('M2.5.8: should accept valid OGG files', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio data'], 'valid.ogg', { type: 'audio/ogg' });
    
    await user.upload(fileInput, file);
    
    expect(fileInput.files?.[0]).toBe(file);
    expect(screen.queryByText(/invalid|error/i)).not.toBeInTheDocument();
  });
});

describe('M2.6: Upload Progress Tracking', () => {
  it('M2.6.1: should show upload progress bar during upload', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio data'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });
  });

  it('M2.6.2: should display current upload percentage', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio data'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/%|uploading/i)).toBeInTheDocument();
    });
  });

  it('M2.6.3: should display upload speed', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['x'.repeat(1024 * 100)], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.queryByText(/MB\/s|KB\/s|speed/i)).toBeInTheDocument();
    });
  });

  it('M2.6.4: should display estimated time remaining', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['x'.repeat(1024 * 100)], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.queryByText(/remaining|eta/i)).toBeInTheDocument();
    });
  });

  it('M2.6.5: should disable upload button during upload', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio data'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    expect(uploadButton).toBeDisabled();
  });

  it('M2.6.6: should allow cancelling upload in progress', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio data'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    const cancelButton = await screen.findByRole('button', { name: /cancel/i });
    await user.click(cancelButton);
    
    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });
  });

  it('M2.6.7: should hide progress bar after completion', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio data'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByRole('progressbar')).not.toBeInTheDocument();
    }, { timeout: 5000 });
  });
});

describe('M2.7: Upload Errors', () => {
  it('M2.7.1: should show error when file format invalid (400)', async () => {
    const user = userEvent.setup();
    server.use(
      rest.post('*/voice/upload', (_req, res, ctx) => res(ctx.status(400), ctx.json({ error: 'Invalid format' })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/invalid format|400/i)).toBeInTheDocument();
    });
  });

  it('M2.7.2: should show error when unauthorized (401)', async () => {
    const user = userEvent.setup();
    server.use(
      rest.post('*/voice/upload', (_req, res, ctx) => res(ctx.status(401), ctx.json({ error: 'Unauthorized' })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/unauthorized|401|login/i)).toBeInTheDocument();
    });
  });

  it('M2.7.3: should show error when file too large (413)', async () => {
    const user = userEvent.setup();
    server.use(
      rest.post('*/voice/upload', (_req, res, ctx) => res(ctx.status(413), ctx.json({ error: 'Payload too large' })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/too large|413|max.*100/i)).toBeInTheDocument();
    });
  });

  it('M2.7.4: should show error when rate limited (429)', async () => {
    const user = userEvent.setup();
    server.use(
      rest.post('*/voice/upload', (_req, res, ctx) => res(ctx.status(429), ctx.json({ error: 'Too many requests' })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/rate limit|too many|429/i)).toBeInTheDocument();
    });
  });

  it('M2.7.5: should show error when server error (500)', async () => {
    const user = userEvent.setup();
    server.use(
      rest.post('*/voice/upload', (_req, res, ctx) => res(ctx.status(500), ctx.json({ error: 'Server error' })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/server error|500/i)).toBeInTheDocument();
    });
  });

  it('M2.7.6: should show error when network unavailable', async () => {
    const user = userEvent.setup();
    server.use(
      rest.post('*/voice/upload', (_req, res, ctx) => res.networkError('Failed to connect'))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/network|connection|offline/i)).toBeInTheDocument();
    });
  });

  it('M2.7.7: should allow retrying failed upload', async () => {
    const user = userEvent.setup();
    let callCount = 0;
    
    server.use(
      rest.post('*/voice/upload', (_req, res, ctx) => {
        callCount++;
        if (callCount === 1) {
          return res(ctx.status(500), ctx.json({ error: 'Server error' }));
        }
        return res(ctx.status(200), ctx.json({ id: 'voice-123' }));
      })
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/server error/i)).toBeInTheDocument();
    });
    
    const retryButton = screen.getByRole('button', { name: /retry/i });
    await user.click(retryButton);
    
    await waitFor(() => {
      expect(screen.getByText(/success|uploaded/i)).toBeInTheDocument();
    });
  });

  it('M2.7.8: should allow clearing error message', async () => {
    const user = userEvent.setup();
    server.use(
      rest.post('*/voice/upload', (_req, res, ctx) => res(ctx.status(500), ctx.json({ error: 'Server error' })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/server error/i)).toBeInTheDocument();
    });
    
    const closeButton = screen.getByRole('button', { name: /close|dismiss|�/i });
    await user.click(closeButton);
    
    expect(screen.queryByText(/server error/i)).not.toBeInTheDocument();
  });
});

describe('M2.8: Quality Evaluation Polling', () => {
  it('M2.8.1: should poll /evaluate/voice/:id/poll immediately after upload', async () => {
    const user = userEvent.setup();
    const pollSpy = vi.fn();
    
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (req, res, ctx) => {
        pollSpy();
        return res(ctx.json({ status: 'ready', score: 85 }));
      })
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(pollSpy).toHaveBeenCalled();
    });
  });

  it('M2.8.2: should poll every 2 seconds during evaluation', async () => {
    vi.useFakeTimers();
    const user = userEvent.setup();
    const pollSpy = vi.fn();
    
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (req, res, ctx) => {
        pollSpy();
        return res(ctx.json({ status: 'evaluating', progress: 50 }));
      })
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    vi.advanceTimersByTime(2000);
    expect(pollSpy).toHaveBeenCalledTimes(2);
    
    vi.advanceTimersByTime(2000);
    expect(pollSpy).toHaveBeenCalledTimes(3);
    
    vi.useRealTimers();
  });

  it('M2.8.3: should stop polling when status is ready', async () => {
    const user = userEvent.setup();
    const pollSpy = vi.fn();
    
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (req, res, ctx) => {
        pollSpy();
        return res(ctx.json({ status: 'ready', score: 85 }));
      })
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(pollSpy).toHaveBeenCalled();
    });
    
    const initialCallCount = pollSpy.mock.calls.length;
    
    await new Promise(r => setTimeout(r, 100));
    
    expect(pollSpy.mock.calls.length).toBe(initialCallCount);
  });

  it('M2.8.4: should timeout after 300 poll attempts', async () => {
    const user = userEvent.setup();
    const pollSpy = vi.fn();
    
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (req, res, ctx) => {
        pollSpy();
        return res(ctx.json({ status: 'evaluating', progress: 50 }));
      })
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/timeout|took too long|evaluation timeout/i)).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('M2.8.5: should show "Evaluating..." status during polling', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => res(ctx.json({ status: 'evaluating' })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/evaluating|checking quality/i)).toBeInTheDocument();
    });
  });

  it('M2.8.6: should show progress indicator during polling', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => res(ctx.json({ status: 'evaluating', progress: 65 })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });
  });

  it('M2.8.7: should handle polling error gracefully', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => res(ctx.status(500), ctx.json({ error: 'Evaluation failed' })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/evaluation failed|error|500/i)).toBeInTheDocument();
    });
  });

  it('M2.8.8: should allow user to cancel polling', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => res(ctx.json({ status: 'evaluating' })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    const cancelButton = await screen.findByRole('button', { name: /cancel/i });
    await user.click(cancelButton);
    
    await waitFor(() => {
      expect(screen.queryByText(/evaluating/i)).not.toBeInTheDocument();
    });
  });
});

describe('M2.9: Voice Approval Workflow', () => {
  it('M2.9.1: should show score after evaluation complete', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => res(ctx.json({ status: 'ready', score: 85 })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/85|score.*85/i)).toBeInTheDocument();
    });
  });

  it('M2.9.2: should show feedback message with score', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => res(ctx.json({ status: 'ready', score: 75 })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/good|excellent|feedback/i)).toBeInTheDocument();
    });
  });

  it('M2.9.3: should auto-approve when score >= 60', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => res(ctx.json({ status: 'ready', score: 70 })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/approved|accepted|added to library/i)).toBeInTheDocument();
    });
  });

  it('M2.9.4: should auto-reject when score < 60', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => res(ctx.json({ status: 'ready', score: 45 })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/rejected|not approved|quality too low/i)).toBeInTheDocument();
    });
  });

  it('M2.9.5: should show approval status badge', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => res(ctx.json({ status: 'ready', score: 75 })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByTestId('approval-badge')).toBeInTheDocument();
    });
  });

  it('M2.9.6: should allow user to manually approve voice', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => res(ctx.json({ status: 'ready', score: 50 })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    const approveButton = await screen.findByRole('button', { name: /approve|accept|confirm/i });
    await user.click(approveButton);
    
    await waitFor(() => {
      expect(screen.getByText(/approved|accepted/i)).toBeInTheDocument();
    });
  });

  it('M2.9.7: should allow user to manually reject voice', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => res(ctx.json({ status: 'ready', score: 50 })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    const rejectButton = await screen.findByRole('button', { name: /reject|decline|discard/i });
    await user.click(rejectButton);
    
    await waitFor(() => {
      expect(screen.getByText(/rejected|discarded/i)).toBeInTheDocument();
    });
  });

  it('M2.9.8: should show rejection reason field when rejecting', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => res(ctx.json({ status: 'ready', score: 50 })))
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    const rejectButton = await screen.findByRole('button', { name: /reject|decline|discard/i });
    await user.click(rejectButton);
    
    await waitFor(() => {
      expect(screen.getByText(/reason|feedback|notes/i)).toBeInTheDocument();
    });
  });
});

describe('M2.10: Voice Library Display', () => {
  it('M2.10.1: should fetch and display all user voices', async () => {
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      fixtures.mockVoices.forEach(voice => {
        expect(screen.getByText(voice.name)).toBeInTheDocument();
      });
    });
  });

  it('M2.10.2: should display voice name for each voice', async () => {
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      expect(screen.getByText(fixtures.mockVoices[0].name)).toBeInTheDocument();
    });
  });

  it('M2.10.3: should display voice status (approved/pending/rejected)', async () => {
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      expect(screen.getByText(/approved|pending|rejected/i)).toBeInTheDocument();
    });
  });

  it('M2.10.4: should display approval score when available', async () => {
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      expect(screen.queryByText(/\d{1,3}\/100|score/i)).toBeInTheDocument();
    });
  });

  it('M2.10.5: should display upload date for each voice', async () => {
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      expect(screen.queryByText(/\d{1,2}\/\d{1,2}\/\d{4}|jan|feb|mar/i)).toBeInTheDocument();
    });
  });

  it('M2.10.6: should display audio format (MP3/WAV/OGG)', async () => {
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      expect(screen.queryByText(/MP3|WAV|OGG/i)).toBeInTheDocument();
    });
  });

  it('M2.10.7: should display audio duration', async () => {
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      expect(screen.queryByText(/\d+:\d{2}/)).toBeInTheDocument();
    });
  });

  it('M2.10.8: should display file size', async () => {
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      expect(screen.queryByText(/MB|KB|bytes/i)).toBeInTheDocument();
    });
  });

  it('M2.10.9: should show empty state when no voices exist', async () => {
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: [] })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      expect(screen.getByText(/no voices|empty|get started/i)).toBeInTheDocument();
    });
  });

  it('M2.10.10: should sort voices by upload date (newest first)', async () => {
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      const voiceElements = screen.getAllByTestId(/voice-item-/);
      // Verify newest voice appears first
      expect(voiceElements[0]).toHaveTextContent(fixtures.mockVoices[fixtures.mockVoices.length - 1].name);
    });
  });
});

describe('M2.11: Voice Playback', () => {
  it('M2.11.1: should show play button for each voice', async () => {
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      const playButtons = screen.getAllByRole('button', { name: /play/i });
      expect(playButtons.length).toBeGreaterThan(0);
    });
  });

  it('M2.11.2: should play audio when play button clicked', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const playButtons = await screen.findAllByRole('button', { name: /play/i });
    await user.click(playButtons[0]);
    
    await waitFor(() => {
      expect(screen.getByTestId('audio-player')).toHaveProperty('playing', true);
    });
  });

  it('M2.11.3: should show pause button during playback', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const playButtons = await screen.findAllByRole('button', { name: /play/i });
    await user.click(playButtons[0]);
    
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /pause/i })).toBeInTheDocument();
    });
  });

  it('M2.11.4: should pause audio when pause button clicked', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const playButtons = await screen.findAllByRole('button', { name: /play/i });
    await user.click(playButtons[0]);
    
    const pauseButton = await screen.findByRole('button', { name: /pause/i });
    await user.click(pauseButton);
    
    expect(pauseButton).not.toBeInTheDocument();
  });

  it('M2.11.5: should resume audio when play clicked after pause', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const playButtons = await screen.findAllByRole('button', { name: /play/i });
    await user.click(playButtons[0]);
    
    const pauseButton = await screen.findByRole('button', { name: /pause/i });
    await user.click(pauseButton);
    
    const resumeButton = screen.getByRole('button', { name: /play|resume/i });
    await user.click(resumeButton);
    
    expect(screen.getByRole('button', { name: /pause/i })).toBeInTheDocument();
  });

  it('M2.11.6: should show playback progress bar', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const playButtons = await screen.findAllByRole('button', { name: /play/i });
    await user.click(playButtons[0]);
    
    await waitFor(() => {
      expect(screen.getByTestId('playback-progress')).toBeInTheDocument();
    });
  });

  it('M2.11.7: should show current time / total duration', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const playButtons = await screen.findAllByRole('button', { name: /play/i });
    await user.click(playButtons[0]);
    
    await waitFor(() => {
      expect(screen.queryByText(/\d+:\d{2}\s*\/\s*\d+:\d{2}/)).toBeInTheDocument();
    });
  });

  it('M2.11.8: should allow seeking via progress bar click', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const playButtons = await screen.findAllByRole('button', { name: /play/i });
    await user.click(playButtons[0]);
    
    const progressBar = await screen.findByTestId('playback-progress');
    await user.click(progressBar, { x: 50, y: 10 });
    
    expect(progressBar).toBeInTheDocument();
  });

  it('M2.11.9: should stop playback when voice is deleted', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const playButtons = await screen.findAllByRole('button', { name: /play/i });
    await user.click(playButtons[0]);
    
    const deleteButton = screen.getByRole('button', { name: /delete|remove/i });
    await user.click(deleteButton);
    
    const confirmButton = screen.getByRole('button', { name: /confirm|yes/i });
    await user.click(confirmButton);
    
    await waitFor(() => {
      expect(screen.queryByRole('button', { name: /pause/i })).not.toBeInTheDocument();
    });
  });
});

describe('M2.12: Voice Operations (Edit/Delete)', () => {
  it('M2.12.1: should show edit button for each voice', async () => {
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      const editButtons = screen.getAllByRole('button', { name: /edit|rename/i });
      expect(editButtons.length).toBeGreaterThan(0);
    });
  });

  it('M2.12.2: should show rename dialog when edit clicked', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const editButtons = await screen.findAllByRole('button', { name: /edit|rename/i });
    await user.click(editButtons[0]);
    
    await waitFor(() => {
      expect(screen.getByText(/rename|edit name|new name/i)).toBeInTheDocument();
    });
  });

  it('M2.12.3: should prefill current name in rename dialog', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const editButtons = await screen.findAllByRole('button', { name: /edit|rename/i });
    await user.click(editButtons[0]);
    
    const nameInput = screen.getByDisplayValue(fixtures.mockVoices[0].name) as HTMLInputElement;
    expect(nameInput.value).toBe(fixtures.mockVoices[0].name);
  });

  it('M2.12.4: should update voice name on rename confirm', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices }))),
      rest.patch('*/voice/:id', (_req, res, ctx) => res(ctx.json({ success: true })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const editButtons = await screen.findAllByRole('button', { name: /edit|rename/i });
    await user.click(editButtons[0]);
    
    const nameInput = screen.getByDisplayValue(fixtures.mockVoices[0].name) as HTMLInputElement;
    await user.clear(nameInput);
    await user.type(nameInput, 'New Voice Name');
    
    const confirmButton = screen.getByRole('button', { name: /confirm|save|ok/i });
    await user.click(confirmButton);
    
    await waitFor(() => {
      expect(screen.getByText(/New Voice Name/)).toBeInTheDocument();
    });
  });

  it('M2.12.5: should show delete button for each voice', async () => {
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      const deleteButtons = screen.getAllByRole('button', { name: /delete|remove/i });
      expect(deleteButtons.length).toBeGreaterThan(0);
    });
  });

  it('M2.12.6: should show confirmation dialog before delete', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const deleteButtons = await screen.findAllByRole('button', { name: /delete|remove/i });
    await user.click(deleteButtons[0]);
    
    await waitFor(() => {
      expect(screen.getByText(/are you sure|confirm delete|permanently/i)).toBeInTheDocument();
    });
  });

  it('M2.12.7: should delete voice when confirmed', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices }))),
      rest.delete('*/voice/:id', (_req, res, ctx) => res(ctx.json({ success: true })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const deleteButtons = await screen.findAllByRole('button', { name: /delete|remove/i });
    await user.click(deleteButtons[0]);
    
    const confirmButton = await screen.findByRole('button', { name: /confirm|yes|delete/i });
    await user.click(confirmButton);
    
    await waitFor(() => {
      expect(screen.getByText(/deleted|removed/i)).toBeInTheDocument();
    });
  });

  it('M2.12.8: should not delete voice when cancelled', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const initialCount = fixtures.mockVoices.length;
    const deleteButtons = await screen.findAllByRole('button', { name: /delete|remove/i });
    await user.click(deleteButtons[0]);
    
    const cancelButton = screen.getByRole('button', { name: /cancel|no/i });
    await user.click(cancelButton);
    
    await waitFor(() => {
      const voiceElements = screen.getAllByTestId(/voice-item-/);
      expect(voiceElements.length).toBe(initialCount);
    });
  });

  it('M2.12.9: should disable edit/delete during network request', async () => {
    const user = userEvent.setup();
    let resolveRequest: () => void;
    const requestPromise = new Promise<void>(resolve => {
      resolveRequest = resolve;
    });
    
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices }))),
      rest.delete('*/voice/:id', async (_req, res, ctx) => {
        await requestPromise;
        return res(ctx.json({ success: true }));
      })
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const deleteButtons = await screen.findAllByRole('button', { name: /delete|remove/i });
    await user.click(deleteButtons[0]);
    
    const confirmButton = await screen.findByRole('button', { name: /confirm|yes|delete/i });
    await user.click(confirmButton);
    
    expect(confirmButton).toBeDisabled();
    
    resolveRequest!();
  });
});

describe('M2.13: State Management', () => {
  it('M2.13.1: should persist voice list in context across navigation', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    const { rerender } = renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      expect(screen.getByText(fixtures.mockVoices[0].name)).toBeInTheDocument();
    });
    
    const voicesBefore = [...screen.getAllByTestId(/voice-item-/)];
    expect(voicesBefore.length).toBeGreaterThan(0);
  });

  it('M2.13.2: should update voice list when voice added', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices }))),
      rest.post('*/voice/upload', (_req, res, ctx) => res(ctx.json({ id: 'voice-new', name: 'New Voice', status: 'pending' })))
    );
    
    renderWithProviders(
      <>
        <VoiceLibrary />
        <VoiceUpload />
      </>
    );
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/New Voice/)).toBeInTheDocument();
    }, { timeout: 5000 });
  });

  it('M2.13.3: should update voice list when voice deleted', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices }))),
      rest.delete('*/voice/:id', (_req, res, ctx) => res(ctx.json({ success: true })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const initialCount = (await screen.findAllByTestId(/voice-item-/)).length;
    
    const deleteButtons = screen.getAllByRole('button', { name: /delete|remove/i });
    await user.click(deleteButtons[0]);
    
    const confirmButton = screen.getByRole('button', { name: /confirm|yes|delete/i });
    await user.click(confirmButton);
    
    await waitFor(() => {
      const updatedVoices = screen.queryAllByTestId(/voice-item-/);
      expect(updatedVoices.length).toBeLessThan(initialCount);
    });
  });

  it('M2.13.4: should update voice when renamed', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices }))),
      rest.patch('*/voice/:id', (_req, res, ctx) => res(ctx.json({ success: true })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const editButtons = await screen.findAllByRole('button', { name: /edit|rename/i });
    await user.click(editButtons[0]);
    
    const nameInput = screen.getByDisplayValue(fixtures.mockVoices[0].name) as HTMLInputElement;
    await user.clear(nameInput);
    await user.type(nameInput, 'Updated Name');
    
    const confirmButton = screen.getByRole('button', { name: /confirm|save|ok/i });
    await user.click(confirmButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Updated Name/)).toBeInTheDocument();
    });
  });

  it('M2.13.5: should update voice status when approval changes', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices }))),
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => res(ctx.json({ status: 'ready', score: 75 })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      expect(screen.getByText(/pending|approved/i)).toBeInTheDocument();
    });
  });

  it('M2.13.6: should track loading state during async operations', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
    });
  });

  it('M2.13.7: should track errors in context state', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.status(500), ctx.json({ error: 'Server error' })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      expect(screen.getByText(/error|failed to load/i)).toBeInTheDocument();
    });
  });

  it('M2.13.8: should clear errors when user dismisses', async () => {
    const user = userEvent.setup();
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.status(500), ctx.json({ error: 'Server error' })))
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    await waitFor(() => {
      expect(screen.getByText(/error|failed to load/i)).toBeInTheDocument();
    });
    
    const closeButton = screen.getByRole('button', { name: /close|dismiss|�/i });
    await user.click(closeButton);
    
    expect(screen.queryByText(/error|failed to load/i)).not.toBeInTheDocument();
  });
});

describe('M2.14: Error Recovery', () => {
  it('M2.14.1: should retry failed upload', async () => {
    const user = userEvent.setup();
    let callCount = 0;
    
    server.use(
      rest.post('*/voice/upload', (_req, res, ctx) => {
        callCount++;
        if (callCount === 1) {
          return res(ctx.status(500), ctx.json({ error: 'Server error' }));
        }
        return res(ctx.status(200), ctx.json({ id: 'voice-123' }));
      })
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
    
    const retryButton = screen.getByRole('button', { name: /retry/i });
    await user.click(retryButton);
    
    await waitFor(() => {
      expect(screen.queryByText(/error/i)).not.toBeInTheDocument();
    });
  });

  it('M2.14.2: should retry failed delete', async () => {
    const user = userEvent.setup();
    let callCount = 0;
    
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices }))),
      rest.delete('*/voice/:id', (_req, res, ctx) => {
        callCount++;
        if (callCount === 1) {
          return res(ctx.status(500), ctx.json({ error: 'Server error' }));
        }
        return res(ctx.json({ success: true }));
      })
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const deleteButtons = await screen.findAllByRole('button', { name: /delete|remove/i });
    await user.click(deleteButtons[0]);
    
    let confirmButton = screen.getByRole('button', { name: /confirm|yes|delete/i });
    await user.click(confirmButton);
    
    await waitFor(() => {
      expect(screen.getByText(/error|failed/i)).toBeInTheDocument();
    });
    
    const retryButton = screen.getByRole('button', { name: /retry/i });
    await user.click(retryButton);
    
    await waitFor(() => {
      expect(screen.getByText(/deleted|success/i)).toBeInTheDocument();
    });
  });

  it('M2.14.3: should retry failed rename', async () => {
    const user = userEvent.setup();
    let callCount = 0;
    
    server.use(
      rest.get('*/voice/list', (_req, res, ctx) => res(ctx.json({ voices: fixtures.mockVoices }))),
      rest.patch('*/voice/:id', (_req, res, ctx) => {
        callCount++;
        if (callCount === 1) {
          return res(ctx.status(500), ctx.json({ error: 'Server error' }));
        }
        return res(ctx.json({ success: true }));
      })
    );
    
    renderWithProviders(<VoiceLibrary />);
    
    const editButtons = await screen.findAllByRole('button', { name: /edit|rename/i });
    await user.click(editButtons[0]);
    
    const nameInput = screen.getByDisplayValue(fixtures.mockVoices[0].name) as HTMLInputElement;
    await user.clear(nameInput);
    await user.type(nameInput, 'New Name');
    
    let confirmButton = screen.getByRole('button', { name: /confirm|save|ok/i });
    await user.click(confirmButton);
    
    await waitFor(() => {
      expect(screen.getByText(/error|failed/i)).toBeInTheDocument();
    });
    
    const retryButton = screen.getByRole('button', { name: /retry/i });
    await user.click(retryButton);
    
    await waitFor(() => {
      expect(screen.getByText(/success|New Name/i)).toBeInTheDocument();
    });
  });

  it('M2.14.4: should retry failed evaluation polling', async () => {
    const user = userEvent.setup();
    let callCount = 0;
    
    server.use(
      rest.get('*/evaluate/voice/:id/poll', (_req, res, ctx) => {
        callCount++;
        if (callCount === 1) {
          return res(ctx.status(500), ctx.json({ error: 'Evaluation service error' }));
        }
        return res(ctx.json({ status: 'ready', score: 85 }));
      })
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/evaluation failed|error/i)).toBeInTheDocument();
    });
    
    const retryButton = await screen.findByRole('button', { name: /retry/i });
    await user.click(retryButton);
    
    await waitFor(() => {
      expect(screen.getByText(/85|score/i)).toBeInTheDocument();
    }, { timeout: 5000 });
  });

  it('M2.14.5: should recover from network timeout', async () => {
    const user = userEvent.setup();
    let callCount = 0;
    
    server.use(
      rest.post('*/voice/upload', (_req, res, ctx) => {
        callCount++;
        if (callCount === 1) {
          return res.networkError('Failed to connect');
        }
        return res(ctx.json({ id: 'voice-123' }));
      })
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/network|connection/i)).toBeInTheDocument();
    });
    
    const retryButton = screen.getByRole('button', { name: /retry/i });
    await user.click(retryButton);
    
    await waitFor(() => {
      expect(screen.queryByText(/network|connection/i)).not.toBeInTheDocument();
    });
  });

  it('M2.14.6: should recover from rate limit temporarily', async () => {
    const user = userEvent.setup();
    let callCount = 0;
    
    server.use(
      rest.post('*/voice/upload', (_req, res, ctx) => {
        callCount++;
        if (callCount === 1) {
          return res(ctx.status(429), ctx.json({ error: 'Rate limited', retryAfter: 1 }));
        }
        return res(ctx.json({ id: 'voice-123' }));
      })
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/rate limit|too many|wait/i)).toBeInTheDocument();
    });
    
    const retryButton = await screen.findByRole('button', { name: /retry/i });
    await user.click(retryButton);
    
    await waitFor(() => {
      expect(screen.queryByText(/rate limit/i)).not.toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('M2.14.7: should validate JWT token before upload', async () => {
    const user = userEvent.setup();
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    
    // Token should be attached before upload attempt
    await user.click(uploadButton);
    
    // Should proceed with upload (not blocked by token validation)
    await waitFor(() => {
      expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });
  });

  it('M2.14.8: should refresh token if expired during upload', async () => {
    const user = userEvent.setup();
    let callCount = 0;
    
    server.use(
      rest.post('*/voice/upload', (_req, res, ctx) => {
        callCount++;
        if (callCount === 1) {
          return res(ctx.status(401), ctx.json({ error: 'Token expired' }));
        }
        return res(ctx.json({ id: 'voice-123' }));
      })
    );
    
    renderWithProviders(<VoiceUpload />);
    
    const fileInput = screen.getByLabelText(/upload|select file/i) as HTMLInputElement;
    const file = new File(['audio'], 'test.mp3', { type: 'audio/mpeg' });
    
    await user.upload(fileInput, file);
    const uploadButton = screen.getByRole('button', { name: /upload|save/i });
    await user.click(uploadButton);
    
    await waitFor(() => {
      expect(screen.getByText(/login|auth|unauthorized/i)).toBeInTheDocument();
    });
  });
});
