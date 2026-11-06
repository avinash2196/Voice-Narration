import { useEffect, useState } from 'react';

export interface ApiNotification {
  id: string;
  title: string;
  message: string;
  severity: 'critical' | 'error' | 'warning' | 'info';
  timestamp: number;
}

/**
 * Component to display API error notifications
 * Listens to custom events from ApiErrorHandler
 */
export function ErrorNotificationCenter() {
  const [notifications, setNotifications] = useState<ApiNotification[]>([]);

  useEffect(() => {
    const handleApiError = (event: Event) => {
      const customEvent = event as CustomEvent;
      const notification: ApiNotification = customEvent.detail;

      setNotifications((prev) => {
        const updated = [...prev, notification];
        // Keep max 5 notifications
        if (updated.length > 5) {
          updated.shift();
        }
        return updated;
      });

      // Auto-remove after 5 seconds
      const timer = setTimeout(() => {
        setNotifications((prev) => prev.filter((n) => n.id !== notification.id));
      }, 5000);

      return () => clearTimeout(timer);
    };

    window.addEventListener('apiError', handleApiError);
    return () => window.removeEventListener('apiError', handleApiError);
  }, []);

  if (notifications.length === 0) {
    return null;
  }

  const getSeverityStyles = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-100 border-red-400 text-red-700';
      case 'error':
        return 'bg-red-50 border-red-300 text-red-600';
      case 'warning':
        return 'bg-yellow-50 border-yellow-300 text-yellow-600';
      case 'info':
        return 'bg-blue-50 border-blue-300 text-blue-600';
      default:
        return 'bg-gray-50 border-gray-300 text-gray-600';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return '🔴';
      case 'error':
        return '❌';
      case 'warning':
        return '⚠️';
      case 'info':
        return 'ℹ️';
      default:
        return '•';
    }
  };

  return (
    <div className="fixed top-4 right-4 z-50 max-w-md space-y-2">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`border-l-4 p-4 rounded shadow-lg animate-slideIn ${getSeverityStyles(
            notification.severity
          )}`}
        >
          <div className="flex items-start gap-3">
            <span className="text-xl flex-shrink-0">{getSeverityIcon(notification.severity)}</span>
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-sm">{notification.title}</h3>
              <p className="text-sm mt-1">{notification.message}</p>
            </div>
            <button
              onClick={() =>
                setNotifications((prev) => prev.filter((n) => n.id !== notification.id))
              }
              className="text-xl flex-shrink-0 leading-none opacity-70 hover:opacity-100"
            >
              ✕
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
