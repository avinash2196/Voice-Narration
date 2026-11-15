import type { HttpClient } from '../services/api/httpClient';
import { STORAGE_KEY_AUTH_TOKEN, STORAGE_KEY_REFRESH_TOKEN } from '../utils/constants';

export class TokenInterceptor {
  private httpClient: HttpClient;

  constructor(httpClient: HttpClient) {
    this.httpClient = httpClient;
  }

  setToken(token: string): void {
    this.httpClient.setAuthToken(token);
    localStorage.setItem(STORAGE_KEY_AUTH_TOKEN, token);
  }

  getToken(): string | null {
    return localStorage.getItem(STORAGE_KEY_AUTH_TOKEN);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(STORAGE_KEY_REFRESH_TOKEN);
  }

  setRefreshToken(refreshToken: string): void {
    localStorage.setItem(STORAGE_KEY_REFRESH_TOKEN, refreshToken);
  }

  clearTokens(): void {
    this.httpClient.clearAuthToken();
    localStorage.removeItem(STORAGE_KEY_AUTH_TOKEN);
    localStorage.removeItem(STORAGE_KEY_REFRESH_TOKEN);
  }

  restoreToken(): void {
    const token = this.getToken();
    if (token) {
      this.httpClient.setAuthToken(token);
    }
  }

  hasToken(): boolean {
    return !!this.getToken();
  }

  removeAuthHeader(): void {
    this.httpClient.clearAuthToken();
  }
}

export function createTokenInterceptor(httpClient: HttpClient): TokenInterceptor {
  return new TokenInterceptor(httpClient);
}
