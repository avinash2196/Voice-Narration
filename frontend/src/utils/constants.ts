// Rate Limiting
export const RATE_LIMIT_PER_HOUR = 10;
export const RATE_LIMIT_RESET_INTERVAL_MS = 3600000; // 1 hour in milliseconds

// File Constraints
export const MAX_FILE_SIZE_MB = 100;
export const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

// Text Constraints
export const MAX_TEXT_LENGTH = 20000;
export const MIN_TEXT_LENGTH = 1;

// Audio Constraints
export const AUDIO_SAMPLE_RATE = 16000;
export const AUDIO_CHANNELS = 1;
export const AUDIO_BIT_DEPTH = 16;

// API Timeouts (in milliseconds)
export const DEFAULT_REQUEST_TIMEOUT = 30000;
export const UPLOAD_REQUEST_TIMEOUT = 300000; // 5 minutes for file uploads

// Polling
export const JOB_POLL_INTERVAL_MS = 2000; // 2 seconds
export const MAX_JOB_POLL_ATTEMPTS = 300; // 10 minutes with 2-second intervals

// UI
export const TOAST_DURATION_MS = 5000;
export const MODAL_ANIMATION_DURATION_MS = 300;

// API Endpoints
export const AUTH_API_BASE_URL =
  import.meta.env.VITE_AUTH_API_URL || 'http://localhost:9000';
export const VOICES_API_BASE_URL =
  import.meta.env.VITE_VOICES_API_URL || 'http://localhost:9000';
export const JOBS_API_BASE_URL =
  import.meta.env.VITE_JOBS_API_URL || 'http://localhost:9000';
export const INFERENCE_API_BASE_URL =
  import.meta.env.VITE_INFERENCE_API_URL || 'http://localhost:9000';
export const EVALUATION_API_BASE_URL =
  import.meta.env.VITE_EVALUATION_API_URL || 'http://localhost:9000';

// Storage Keys
export const STORAGE_KEY_AUTH_TOKEN = 'auth_token';
export const STORAGE_KEY_REFRESH_TOKEN = 'refresh_token';
export const STORAGE_KEY_USER = 'user';
export const STORAGE_KEY_VOICES = 'voices';
export const STORAGE_KEY_GENERATIONS = 'generations';
export const STORAGE_KEY_RATE_LIMIT_RESET = 'rate_limit_reset';

// App Info
export const APP_NAME = import.meta.env.VITE_APP_NAME || 'Voice Cloning';
export const APP_VERSION = import.meta.env.VITE_APP_VERSION || '1.0.0';
export const LOG_LEVEL = import.meta.env.VITE_LOG_LEVEL || 'warn';
