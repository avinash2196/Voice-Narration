import { http, HttpResponse } from 'msw';
import { AUTH_API_BASE_URL } from '../../src/utils/constants';
import type {
  AuthResponse,
  LoginRequest,
  SignupRequest,
  TokenRefreshRequest,
} from '../../src/types/auth';
import type { ApiError } from '../../src/types/api';

// Mock Auth Service responses
export const validAuthResponse: AuthResponse = {
  user: {
    id: 'user-123',
    email: 'test@example.com',
    name: 'Test User',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  token: 'mock-jwt-token-abc123',
  refreshToken: 'mock-refresh-token-xyz789',
};

export const authError: ApiError = {
  status: 401,
  message: 'Invalid credentials',
  code: 'INVALID_CREDENTIALS',
};

export const authHandlers = [
  // POST /auth/signup
  http.post(`${AUTH_API_BASE_URL}/auth/signup`, async ({ request }) => {
    const body = (await request.json()) as SignupRequest;

    // Validation: empty fields
    if (!body.email || !body.password || !body.confirmPassword) {
      return HttpResponse.json(
        {
          status: 400,
          message: 'Email and password are required',
          code: 'MISSING_FIELDS',
        } as ApiError,
        { status: 400 }
      );
    }

    // Validation: email format
    if (!body.email.includes('@')) {
      return HttpResponse.json(
        {
          status: 400,
          message: 'Invalid email format',
          code: 'INVALID_EMAIL',
        } as ApiError,
        { status: 400 }
      );
    }

    // Validation: password match
    if (body.password !== body.confirmPassword) {
      return HttpResponse.json(
        {
          status: 400,
          message: 'Passwords do not match',
          code: 'PASSWORD_MISMATCH',
        } as ApiError,
        { status: 400 }
      );
    }

    // Validation: password strength
    if (body.password.length < 8) {
      return HttpResponse.json(
        {
          status: 400,
          message: 'Password must be at least 8 characters',
          code: 'WEAK_PASSWORD',
        } as ApiError,
        { status: 400 }
      );
    }

    // Validation: terms acceptance
    if (!body.agreedToTerms) {
      return HttpResponse.json(
        {
          status: 400,
          message: 'Must agree to terms',
          code: 'TERMS_NOT_ACCEPTED',
        } as ApiError,
        { status: 400 }
      );
    }

    // Validation: duplicate email
    if (body.email === 'existing@example.com') {
      return HttpResponse.json(
        {
          status: 409,
          message: 'Email already registered',
          code: 'DUPLICATE_EMAIL',
        } as ApiError,
        { status: 409 }
      );
    }

    // Success
    return HttpResponse.json(validAuthResponse, { status: 201 });
  }),

  // POST /auth/login
  http.post(`${AUTH_API_BASE_URL}/auth/login`, async ({ request }) => {
    const body = (await request.json()) as LoginRequest;

    // Validation: empty fields
    if (!body.email || !body.password) {
      return HttpResponse.json(
        {
          status: 400,
          message: 'Email and password are required',
          code: 'MISSING_FIELDS',
        } as ApiError,
        { status: 400 }
      );
    }

    // Validation: email format
    if (!body.email.includes('@')) {
      return HttpResponse.json(
        {
          status: 400,
          message: 'Invalid email format',
          code: 'INVALID_EMAIL',
        } as ApiError,
        { status: 400 }
      );
    }

    // Validation: invalid credentials
    if (
      body.email !== 'test@example.com' ||
      body.password !== 'Test123456!'
    ) {
      return HttpResponse.json(
        {
          status: 401,
          message: 'Invalid credentials',
          code: 'INVALID_CREDENTIALS',
        } as ApiError,
        { status: 401 }
      );
    }

    // Success
    return HttpResponse.json(validAuthResponse, { status: 200 });
  }),

  // POST /auth/refresh
  http.post(`${AUTH_API_BASE_URL}/auth/refresh`, async ({ request }) => {
    const body = (await request.json()) as TokenRefreshRequest;

    // Validation: missing token
    if (!body.refreshToken) {
      return HttpResponse.json(
        {
          status: 401,
          message: 'Refresh token required',
          code: 'MISSING_REFRESH_TOKEN',
        } as ApiError,
        { status: 401 }
      );
    }

    // Validation: invalid token
    if (body.refreshToken === 'invalid-token') {
      return HttpResponse.json(
        {
          status: 401,
          message: 'Invalid or expired refresh token',
          code: 'INVALID_REFRESH_TOKEN',
        } as ApiError,
        { status: 401 }
      );
    }

    // Success: return new token
    return HttpResponse.json(
      {
        token: 'mock-jwt-token-new-' + Date.now(),
        refreshToken: 'mock-refresh-token-new-' + Date.now(),
      },
      { status: 200 }
    );
  }),

  // POST /auth/logout
  http.post(`${AUTH_API_BASE_URL}/auth/logout`, () => {
    return HttpResponse.json({ success: true }, { status: 200 });
  }),

  // GET /auth/validate
  http.get(`${AUTH_API_BASE_URL}/auth/validate`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');

    // Validation: missing token
    if (!authHeader) {
      return HttpResponse.json(
        {
          status: 401,
          message: 'Missing authorization header',
          code: 'MISSING_AUTH_HEADER',
        } as ApiError,
        { status: 401 }
      );
    }

    // Validation: invalid token
    if (authHeader === 'Bearer invalid-token') {
      return HttpResponse.json(
        {
          status: 401,
          message: 'Invalid token',
          code: 'INVALID_TOKEN',
        } as ApiError,
        { status: 401 }
      );
    }

    // Success: return user
    return HttpResponse.json(validAuthResponse.user, { status: 200 });
  }),
];
