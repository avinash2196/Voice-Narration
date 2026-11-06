import type { LoginRequest, SignupRequest, User, AuthResponse } from '../../src/types/auth';

// Valid test user
export const testUser: User = {
  id: 'user-123',
  email: 'test@example.com',
  name: 'Test User',
  createdAt: '2026-10-31T00:00:00Z',
  updatedAt: '2026-10-31T00:00:00Z',
};

// Factory: create mock user
export const createMockUser = (overrides?: Partial<User>): User => {
  return {
    ...testUser,
    ...overrides,
  };
};

// Valid sign-up request
export const validSignupRequest: SignupRequest = {
  email: 'newuser@example.com',
  password: 'Test123456!',
  confirmPassword: 'Test123456!',
  agreedToTerms: true,
};

// Invalid sign-up requests
export const invalidSignupRequests = {
  emptyEmail: {
    email: '',
    password: 'Test123456!',
    confirmPassword: 'Test123456!',
    agreedToTerms: true,
  } as SignupRequest,

  emptyPassword: {
    email: 'test@example.com',
    password: '',
    confirmPassword: '',
    agreedToTerms: true,
  } as SignupRequest,

  invalidEmail: {
    email: 'not-an-email',
    password: 'Test123456!',
    confirmPassword: 'Test123456!',
    agreedToTerms: true,
  } as SignupRequest,

  weakPassword: {
    email: 'test@example.com',
    password: 'short',
    confirmPassword: 'short',
    agreedToTerms: true,
  } as SignupRequest,

  passwordMismatch: {
    email: 'test@example.com',
    password: 'Test123456!',
    confirmPassword: 'Different123!',
    agreedToTerms: true,
  } as SignupRequest,

  noTermsAgreement: {
    email: 'test@example.com',
    password: 'Test123456!',
    confirmPassword: 'Test123456!',
    agreedToTerms: false,
  } as SignupRequest,

  duplicateEmail: {
    email: 'existing@example.com',
    password: 'Test123456!',
    confirmPassword: 'Test123456!',
    agreedToTerms: true,
  } as SignupRequest,

  noUppercasePassword: {
    email: 'test@example.com',
    password: 'test123456!',
    confirmPassword: 'test123456!',
    agreedToTerms: true,
  } as SignupRequest,

  noNumberPassword: {
    email: 'test@example.com',
    password: 'TestPassword!',
    confirmPassword: 'TestPassword!',
    agreedToTerms: true,
  } as SignupRequest,
};

// Valid login request
export const validLoginRequest: LoginRequest = {
  email: 'test@example.com',
  password: 'Test123456!',
};

// Invalid login requests
export const invalidLoginRequests = {
  emptyEmail: {
    email: '',
    password: 'Test123456!',
  } as LoginRequest,

  emptyPassword: {
    email: 'test@example.com',
    password: '',
  } as LoginRequest,

  invalidEmail: {
    email: 'not-an-email',
    password: 'Test123456!',
  } as LoginRequest,

  wrongPassword: {
    email: 'test@example.com',
    password: 'WrongPassword123!',
  } as LoginRequest,

  nonexistentUser: {
    email: 'nonexistent@example.com',
    password: 'Test123456!',
  } as LoginRequest,
};

// Mock auth response
export const mockAuthResponse: AuthResponse = {
  user: testUser,
  token: 'mock-jwt-token-abc123',
  refreshToken: 'mock-refresh-token-xyz789',
};

// Mock auth error responses
export const mockAuthErrors = {
  missingFields: {
    status: 400,
    message: 'Email and password are required',
    code: 'MISSING_FIELDS',
  },

  invalidEmail: {
    status: 400,
    message: 'Invalid email format',
    code: 'INVALID_EMAIL',
  },

  weakPassword: {
    status: 400,
    message: 'Password must be at least 8 characters',
    code: 'WEAK_PASSWORD',
  },

  passwordMismatch: {
    status: 400,
    message: 'Passwords do not match',
    code: 'PASSWORD_MISMATCH',
  },

  termsNotAccepted: {
    status: 400,
    message: 'Must agree to terms',
    code: 'TERMS_NOT_ACCEPTED',
  },

  duplicateEmail: {
    status: 409,
    message: 'Email already registered',
    code: 'DUPLICATE_EMAIL',
  },

  invalidCredentials: {
    status: 401,
    message: 'Invalid credentials',
    code: 'INVALID_CREDENTIALS',
  },

  missingRefreshToken: {
    status: 401,
    message: 'Refresh token required',
    code: 'MISSING_REFRESH_TOKEN',
  },

  invalidRefreshToken: {
    status: 401,
    message: 'Invalid or expired refresh token',
    code: 'INVALID_REFRESH_TOKEN',
  },

  missingAuthHeader: {
    status: 401,
    message: 'Missing authorization header',
    code: 'MISSING_AUTH_HEADER',
  },

  invalidToken: {
    status: 401,
    message: 'Invalid token',
    code: 'INVALID_TOKEN',
  },

  serverError: {
    status: 500,
    message: 'Internal server error',
    code: 'INTERNAL_SERVER_ERROR',
  },
};
