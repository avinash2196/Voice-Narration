/**
 * API Configuration
 * Uses environment variables to determine service endpoints
 * Defaults to localhost for local development
 */

export const API_CONFIG = {
  AUTH_SERVICE: import.meta.env.VITE_AUTH_API_BASE_URL || 'http://localhost:9000',
  VOICE_SERVICE: import.meta.env.VITE_VOICE_API_BASE_URL || 'http://localhost:8002',
  TTS_SERVICE: import.meta.env.VITE_TTS_API_BASE_URL || 'http://localhost:8003',
  EVALUATION_SERVICE: import.meta.env.VITE_EVALUATION_API_BASE_URL || 'http://localhost:9000',
  JOBS_SERVICE: import.meta.env.VITE_JOBS_API_BASE_URL || 'http://localhost:9000',
};

export const API_TIMEOUT = 30000; // 30 seconds
export const POLLING_INTERVAL = 2000; // 2 seconds
export const MAX_POLLING_ATTEMPTS = 300; // 10 minutes total
