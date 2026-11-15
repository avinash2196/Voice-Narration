import { setupServer } from 'msw/node';
import { vi } from 'vitest';
import '@testing-library/jest-dom';

export const server = setupServer();

beforeAll(() => server.listen());

afterEach(() => server.resetHandlers());

afterAll(() => server.close());

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock navigator.mediaDevices for getUserMedia tests
if (!navigator.mediaDevices) {
  Object.defineProperty(navigator, 'mediaDevices', {
    value: {
      getUserMedia: vi.fn(),
      enumerateDevices: vi.fn(),
    },
    writable: true,
  });
}

// Mock BlobEvent if not available (must be defined before MediaRecorder)
if (typeof (window as any).BlobEvent === 'undefined') {
  (window as any).BlobEvent = class BlobEvent extends Event {
    data: Blob;
    constructor(type: string, eventInitDict: { data: Blob }) {
      super(type);
      this.data = eventInitDict.data;
    }
  };
}

// Mock MediaRecorder if not available
if (typeof MediaRecorder === 'undefined') {
  (window as any).MediaRecorder = class MockMediaRecorder {
    state: 'inactive' | 'recording' | 'paused' = 'inactive';
    ondataavailable: ((event: any) => void) | null = null;
    onstart: (() => void) | null = null;
    onstop: (() => void) | null = null;
    onerror: ((event: any) => void) | null = null;
    stream: MediaStream;

    constructor(stream: MediaStream) {
      this.stream = stream;
    }

    start() {
      this.state = 'recording';
      if (this.onstart) {
        this.onstart();
      }
    }

    stop() {
      this.state = 'inactive';
      // Create a mock Blob with some data
      const mockData = new Blob(['mock audio data'], { type: 'audio/wav' });
      if (this.ondataavailable) {
        const blobEvent = new (window as any).BlobEvent('dataavailable', { data: mockData });
        this.ondataavailable(blobEvent);
      }
      if (this.onstop) {
        this.onstop();
      }
    }

    pause() {
      this.state = 'paused';
    }

    resume() {
      this.state = 'recording';
    }

    static isTypeSupported(type: string): boolean {
      return ['audio/mp3', 'audio/wav', 'audio/ogg', 'audio/webm'].includes(type);
    }
  };
}

// Mock HTMLMediaElement methods
if (!HTMLMediaElement.prototype.play) {
  HTMLMediaElement.prototype.play = vi.fn().mockResolvedValue(undefined);
}
if (!HTMLMediaElement.prototype.pause) {
  HTMLMediaElement.prototype.pause = vi.fn();
}

// Mock URL.createObjectURL and URL.revokeObjectURL for audio preview
if (!URL.createObjectURL) {
  URL.createObjectURL = vi.fn(() => 'blob:mock-url');
}
if (!URL.revokeObjectURL) {
  URL.revokeObjectURL = vi.fn();
}

// Mock Canvas getContext for waveform visualization
const mockCanvasContext = {
  fillStyle: '#000',
  strokeStyle: '#000',
  lineWidth: 1,
  fillRect: vi.fn(),
  clearRect: vi.fn(),
  strokeRect: vi.fn(),
  beginPath: vi.fn(),
  moveTo: vi.fn(),
  lineTo: vi.fn(),
  stroke: vi.fn(),
  fill: vi.fn(),
  quadraticCurveTo: vi.fn(),
  arc: vi.fn(),
  arcTo: vi.fn(),
  closePath: vi.fn(),
  measureText: vi.fn(() => ({ width: 0 })),
  transform: vi.fn(),
  drawImage: vi.fn(),
  createImageData: vi.fn(),
  getImageData: vi.fn(),
  putImageData: vi.fn(),
  save: vi.fn(),
  restore: vi.fn(),
  scale: vi.fn(),
  rotate: vi.fn(),
  translate: vi.fn(),
};

if (!HTMLCanvasElement.prototype.getContext) {
  HTMLCanvasElement.prototype.getContext = vi.fn(() => mockCanvasContext);
}

