import { HttpClient } from './httpClient';
import { API_CONFIG } from '../../utils/api-config';
import type { LoginRequest, SignupRequest, AuthResponse } from '../../types/auth';

export interface TokenRefreshRequest {
  refreshToken: string;
}

export interface TokenRefreshResponse {
  token: string;
  refreshToken: string;
}

export class AuthClient extends HttpClient {
  constructor(onUnauthorized?: () => void) {
    super({ 
      baseURL: API_CONFIG.AUTH_SERVICE,
      onUnauthorized
    });
  }

  async signup(request: SignupRequest): Promise<AuthResponse> {
    const response = await this.post<AuthResponse>('/auth/signup', request);
    return response.data;
  }

  async login(request: LoginRequest): Promise<AuthResponse> {
    const response = await this.post<AuthResponse>('/auth/login', request);
    return response.data;
  }

  async refreshToken(request: TokenRefreshRequest): Promise<TokenRefreshResponse> {
    const response = await this.post<TokenRefreshResponse>('/auth/refresh', request);
    return response.data;
  }

  async validateToken(): Promise<boolean> {
    try {
      await this.get<{ valid: boolean }>('/auth/validate');
      return true;
    } catch (error) {
      return false;
    }
  }

  async logout(): Promise<void> {
    await this.post<{ success: boolean }>('/auth/logout', {});
  }
}

export function createAuthClient(onUnauthorized?: () => void): AuthClient {
  return new AuthClient(onUnauthorized);
}
