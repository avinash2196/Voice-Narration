/**
 * API Error Handler
 * Centralized error handling for all API responses
 * Handles 401, 403, network errors, timeouts, etc.
 */

export type ErrorSeverity = 'critical' | 'error' | 'warning' | 'info';

export interface HandleErrorOptions {
  onLogout?: () => void;
  onRetry?: () => Promise<any>;
  showUI?: boolean;
}

export class ApiErrorHandler {
  /**
   * Handle 401 Unauthorized - User session expired or token invalid
   */
  static handle401(options: HandleErrorOptions = {}): void {
    console.warn('[ApiErrorHandler] 401 Unauthorized - Session expired');

    // Clear auth state
    if (options.onLogout) {
      options.onLogout();
    }

    // Optional: Show error UI
    if (options.showUI) {
      this.showErrorNotification(
        'Session Expired',
        'Your session has expired. Please log in again.',
        'critical'
      );
    }

    // Redirect to login (will be handled by ProtectedRoute)
    if (typeof window !== 'undefined') {
      // Set a flag so components know why they're being redirected
      sessionStorage.setItem('auth_redirect_reason', '401_unauthorized');
    }
  }

  /**
   * Handle 403 Forbidden - User lacks permission
   */
  static handle403(options: HandleErrorOptions = {}): void {
    console.warn('[ApiErrorHandler] 403 Forbidden - Access denied');

    if (options.showUI) {
      this.showErrorNotification(
        'Access Denied',
        'You do not have permission to access this resource.',
        'error'
      );
    }
  }

  /**
   * Handle timeout errors
   */
  static handleTimeout(options: HandleErrorOptions = {}): void {
    console.warn('[ApiErrorHandler] Request timeout');

    if (options.showUI) {
      this.showErrorNotification(
        'Request Timeout',
        'The request took too long. Please check your connection and try again.',
        'warning'
      );
    }

    if (options.onRetry) {
      // Could offer retry button
      console.log('[ApiErrorHandler] Retry available');
    }
  }

  /**
   * Handle network errors (no connection, CORS, etc.)
   */
  static handleNetworkError(error: Error, options: HandleErrorOptions = {}): void {
    console.error('[ApiErrorHandler] Network error:', error.message);

    if (options.showUI) {
      this.showErrorNotification(
        'Connection Error',
        'Unable to reach the server. Please check your internet connection.',
        'error'
      );
    }
  }

  /**
   * Handle server errors (5xx)
   */
  static handleServerError(status: number, options: HandleErrorOptions = {}): void {
    console.error('[ApiErrorHandler] Server error:', status);

    if (options.showUI) {
      const message =
        status === 503
          ? 'The service is temporarily unavailable. Please try again later.'
          : 'The server encountered an error. Please try again.';

      this.showErrorNotification(
        'Server Error',
        message,
        'error'
      );
    }
  }

  /**
   * Handle validation errors (4xx client errors)
   */
  static handleValidationError(status: number, message: string, options: HandleErrorOptions = {}): void {
    console.warn('[ApiErrorHandler] Validation error:', status, message);

    if (options.showUI) {
      this.showErrorNotification(
        'Invalid Request',
        message || 'Please check your input and try again.',
        'warning'
      );
    }
  }

  /**
   * Show error notification (could integrate with toast library)
   * For now, logs to console - can be extended with UI component
   */
  private static showErrorNotification(title: string, message: string, severity: ErrorSeverity): void {
    // Store in sessionStorage for UI components to display
    const notification = {
      title,
      message,
      severity,
      timestamp: Date.now(),
      id: `error-${Date.now()}-${Math.random()}`,
    };

    try {
      const notifications = JSON.parse(sessionStorage.getItem('api_notifications') || '[]');
      notifications.push(notification);
      // Keep only last 10 notifications
      if (notifications.length > 10) {
        notifications.shift();
      }
      sessionStorage.setItem('api_notifications', JSON.stringify(notifications));

      // Dispatch custom event so components can listen
      window.dispatchEvent(
        new CustomEvent('apiError', {
          detail: notification,
        })
      );
    } catch (e) {
      console.error('Failed to store error notification:', e);
    }
  }

  /**
   * Determine if error is retryable
   */
  static isRetryable(status: number, error?: Error): boolean {
    // Timeout errors are retryable
    if (error?.name === 'AbortError') return true;

    // Network errors are retryable
    if (error?.message.includes('Failed to fetch')) return true;

    // Server errors (5xx) are retryable
    if (status >= 500) return true;

    // Request timeout (408) is retryable
    if (status === 408) return true;

    // 429 Too Many Requests is retryable
    if (status === 429) return true;

    // Client errors (4xx) except 401, 403, 404, 422 are not retryable
    return false;
  }

  /**
   * Determine retry delay in milliseconds (with exponential backoff)
   */
  static getRetryDelay(attempt: number): number {
    // Start with 1 second, double for each attempt, max 30 seconds
    const delay = Math.min(1000 * Math.pow(2, attempt), 30000);
    // Add jitter to prevent thundering herd
    const jitter = Math.random() * 0.1 * delay;
    return delay + jitter;
  }
}

/**
 * Retry wrapper for API calls
 */
export async function withRetry<T>(
  fn: () => Promise<T>,
  maxAttempts: number = 3,
  onRetry?: (attempt: number, error: Error) => void
): Promise<T> {
  let lastError: Error | null = null;

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      const isRetryable = ApiErrorHandler.isRetryable(
        // Extract status if available
        (error as any)?.status || 0,
        error as Error
      );

      if (!isRetryable || attempt === maxAttempts - 1) {
        throw error;
      }

      const delay = ApiErrorHandler.getRetryDelay(attempt);
      onRetry?.(attempt + 1, error as Error);

      console.log(`[withRetry] Attempt ${attempt + 1} failed, retrying in ${delay}ms...`);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw lastError || new Error('Retry failed');
}
