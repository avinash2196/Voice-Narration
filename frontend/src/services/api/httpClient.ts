import type { ApiResponse, ApiError } from '../../types/api';
import type { RequestOptions } from '../../types/common';
import { ApiErrorHandler } from './errorHandler';

export interface HttpClientConfig {
  baseURL: string;
  timeout?: number;
  headers?: Record<string, string>;
  onUnauthorized?: () => void;
}

export interface HttpResponse<T> {
  data: T;
  status: number;
  headers: Record<string, string>;
}

export class HttpClient {
  private baseURL: string;
  private timeout: number;
  private defaultHeaders: Record<string, string>;
  private authToken: string | null = null;
  private onUnauthorized: (() => void) | null = null;

  constructor(config: HttpClientConfig) {
    this.baseURL = config.baseURL;
    this.timeout = config.timeout || 30000;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      ...config.headers,
    };
    this.onUnauthorized = config.onUnauthorized || null;
  }

  async get<T>(
    url: string,
    options?: RequestOptions
  ): Promise<HttpResponse<T>> {
    return this.request<T>('GET', url, undefined, options);
  }

  async post<T>(
    url: string,
    data: any,
    options?: RequestOptions
  ): Promise<HttpResponse<T>> {
    return this.request<T>('POST', url, data, options);
  }

  async put<T>(
    url: string,
    data: any,
    options?: RequestOptions
  ): Promise<HttpResponse<T>> {
    return this.request<T>('PUT', url, data, options);
  }

  async delete<T>(
    url: string,
    options?: RequestOptions
  ): Promise<HttpResponse<T>> {
    return this.request<T>('DELETE', url, undefined, options);
  }

  setAuthToken(token: string): void {
    this.authToken = token;
  }

  clearAuthToken(): void {
    this.authToken = null;
  }

  private async request<T>(
    method: string,
    url: string,
    data?: any,
    options?: RequestOptions
  ): Promise<HttpResponse<T>> {
    const headers: Record<string, string> = {
      ...this.defaultHeaders,
      ...options?.headers,
    };

    if (this.authToken) {
      headers['Authorization'] = `Bearer ${this.authToken}`;
    }

    const fullUrl = `${this.baseURL}${url}`;
    const controller = new AbortController();
    const timeoutId = setTimeout(
      () => controller.abort(),
      options?.timeout || this.timeout
    );

    try {
      const response = await fetch(fullUrl, {
        method,
        headers,
        body: data ? JSON.stringify(data) : undefined,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      // Handle 401 Unauthorized
      if (response.status === 401) {
        ApiErrorHandler.handle401({
          onLogout: this.onUnauthorized || undefined,
          showUI: true,
        });
        throw new Error('Unauthorized - Session expired');
      }

      // Handle 403 Forbidden
      if (response.status === 403) {
        ApiErrorHandler.handle403({ showUI: true });
        throw new Error('Forbidden - Access denied');
      }

      // Handle 5xx Server Errors
      if (response.status >= 500) {
        ApiErrorHandler.handleServerError(response.status, { showUI: true });
      }

      let responseData: any;
      try {
        responseData = await response.json();
      } catch {
        // Response is not JSON (e.g., empty response or HTML error page)
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        responseData = {};
      }

      if (!response.ok) {
        const statusCode = response.status;

        // Handle validation errors (4xx except 401, 403)
        if (statusCode >= 400 && statusCode < 500 && statusCode !== 401 && statusCode !== 403) {
          ApiErrorHandler.handleValidationError(
            statusCode,
            responseData.message || `HTTP ${statusCode}`,
            { showUI: false }
          );
        }

        const error: ApiError = {
          status: response.status,
          message: responseData.message || `HTTP ${response.status}`,
          code: responseData.code || 'UNKNOWN_ERROR',
          details: responseData.details,
        };
        throw error;
      }

      return {
        data: responseData,
        status: response.status,
        headers: Object.fromEntries(response.headers.entries()),
      };
    } catch (error) {
      clearTimeout(timeoutId);

      // Handle timeout
      if (error instanceof Error && error.name === 'AbortError') {
        ApiErrorHandler.handleTimeout({ showUI: true });
        throw new Error('Request timeout');
      }

      // Handle network errors
      if (error instanceof TypeError) {
        ApiErrorHandler.handleNetworkError(error, { showUI: true });
        throw error;
      }

      throw error;
    }
  }
}

export const createHttpClient = (
  baseURL: string,
  onUnauthorized?: () => void
): HttpClient => {
  return new HttpClient({ baseURL, onUnauthorized });
};
